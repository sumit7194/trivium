#!/usr/bin/env python3
"""Leg 6 — Leg-3 Regime Prediction (Direct vs. Indirect Observation).

Trains Generic and Orthogonal state-update models in both Direct and Indirect
observation regimes. Verifies that representation scrambling (high kNN, low linear R2)
occurs ONLY when the update is generic AND the observation is indirect.
"""

import json
import os
import sys
import numpy as np
import torch
from torch import nn
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_predict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

STEPS = 6000
T = 24
KOBS = 12
DEV = torch.device("cpu")  # CPU is fast and consistent for these MLPs

torch.manual_seed(0)
OMEGA = torch.randn(3, 2) * 0.30


def skew(w):
    z = torch.zeros(w.shape[:-1] + (1,), device=w.device, dtype=w.dtype)
    x, y, zc = w[..., 0:1], w[..., 1:2], w[..., 2:3]
    return torch.stack([
        torch.cat([z, -zc, y], -1),
        torch.cat([zc, z, -x], -1),
        torch.cat([-y, x, z], -1)
    ], -2)


def rot(omega):
    theta = omega.norm(dim=-1, keepdim=True).clamp_min(1e-8)
    K = skew(omega)
    a = (torch.sin(theta) / theta)[..., None]
    b = ((1 - torch.cos(theta)) / theta ** 2)[..., None]
    I = torch.eye(3, device=omega.device, dtype=omega.dtype).expand(K.shape)
    return I + a * K + b * (K @ K)


def readout(s):
    """Nonlinear, monotone, invertible observation function."""
    return s + 0.7 * s ** 3


def gen_batch(B, seed, indirect):
    g = torch.Generator().manual_seed(seed)
    c = torch.randn(B, T, 2, generator=g) * 0.8
    Q0 = torch.randn(B, 3, generator=g)
    Q0 = Q0 / Q0.norm(dim=-1, keepdim=True)
    Q = [Q0]
    for t in range(T - 1):
        Q.append((rot(c[:, t] @ OMEGA.T) @ Q[-1][..., None])[..., 0])
    Q = torch.stack(Q, 1)
    
    if indirect:
        P = torch.zeros(B, T, 3)
        P[..., 2] = 1.0  # Fixed e3 probe
        s = (P * Q).sum(-1)
        y = readout(s) + 0.01 * torch.randn(B, T, generator=g)
        y = y.unsqueeze(-1)  # [B, T, 1]
    else:
        P = torch.zeros(B, T, 3)  # Unused in direct
        # Direct observation is the full 3D state plus noise
        y = Q + 0.01 * torch.randn(B, T, 3, generator=g)  # [B, T, 3]
        
    return c, P, y, Q


class Encoder(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.gru = nn.GRU(2 + 3 + obs_dim, 96, batch_first=True)
        self.out = nn.Linear(96, 3)

    def forward(self, c, P, y):
        tok = torch.cat([c[:, :KOBS], P[:, :KOBS], y[:, :KOBS]], -1)
        h, _ = self.gru(tok)
        return self.out(h[:, -1])


class Model(nn.Module):
    def __init__(self, orthogonal, obs_dim):
        super().__init__()
        self.orthogonal = orthogonal
        self.obs_dim = obs_dim
        self.enc = Encoder(obs_dim)
        self.f = nn.Sequential(
            nn.Linear(2 if orthogonal else 5, 96), nn.GELU(),
            nn.Linear(96, 96), nn.GELU(),
            nn.Linear(96, 3)
        )
        self.head = nn.Sequential(
            nn.Linear(6, 96), nn.GELU(),
            nn.Linear(96, 96), nn.GELU(),
            nn.Linear(96, obs_dim)
        )

    def rollout(self, c, P, y):
        w = self.enc(c, P, y)
        W = [w]
        for t in range(T - 1):
            w = (rot(self.f(c[:, t])) @ w[..., None])[..., 0] if self.orthogonal else w + self.f(torch.cat([w, c[:, t]], -1))
            W.append(w)
        W = torch.stack(W, 1)
        yhat = self.head(torch.cat([W, P], -1))
        return yhat, W


def train_model(orthogonal, indirect, tag):
    obs_dim = 1 if indirect else 3
    m = Model(orthogonal, obs_dim).to(DEV)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    for step in range(STEPS):
        c, P, y, _ = gen_batch(256, seed=step + 1, indirect=indirect)
        yhat, _ = m.rollout(c.to(DEV), P.to(DEV), y.to(DEV))
        loss = nn.functional.mse_loss(yhat[:, KOBS:], y.to(DEV)[:, KOBS:])
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 1000 == 0:
            print(f"  {tag} step {step}/{STEPS} loss = {float(loss):.5f}")
    return m


def decode_state(W, Q, knn=False):
    est = KNeighborsRegressor(15) if knn else Ridge(1.0)
    pred = cross_val_predict(est, W, Q, cv=5)
    return float(1 - np.sum((pred - Q) ** 2) / np.sum((Q - Q.mean(0)) ** 2))


def evaluate_model(m, indirect):
    c, P, y, Q = gen_batch(400, seed=99, indirect=indirect)
    m.eval()
    with torch.no_grad():
        yhat, W = m.rollout(c.to(DEV), P.to(DEV), y.to(DEV))
        
    yh = yhat[:, KOBS:].cpu().numpy().ravel()
    yt = y[:, KOBS:].numpy().ravel()
    r2 = float(1 - np.sum((yh - yt) ** 2) / np.sum((yt - yt.mean()) ** 2))
    
    Wn = W[:, KOBS:].reshape(-1, 3).cpu().numpy()
    Qn = Q[:, KOBS:].reshape(-1, 3).numpy()
    
    lin = decode_state(Wn, Qn, knn=False)
    non = decode_state(Wn, Qn, knn=True)
    
    ts = np.arange(KOBS, T)
    early = ts[: len(ts) // 2]
    late = ts[len(ts) // 2:]
    
    We = W[:, early].reshape(-1, 3).cpu().numpy()
    Qe = Q[:, early].reshape(-1, 3).numpy()
    Wl = W[:, late].reshape(-1, 3).cpu().numpy()
    Ql = Q[:, late].reshape(-1, 3).numpy()
    
    lin_early = decode_state(We, Qe, knn=False)
    lin_late = decode_state(Wl, Ql, knn=False)
    
    return r2, lin, non, lin_early, lin_late


def main():
    print("RUNNING LEG 6: DIRECT VS INDIRECT REGIME STUDY\n")
    
    # 1. Train models in Direct observation regime
    print("Training Direct regime models...")
    m_direct_ortho = train_model(orthogonal=True, indirect=False, tag="direct_ortho")
    m_direct_generic = train_model(orthogonal=False, indirect=False, tag="direct_generic")
    
    # 2. Train models in Indirect observation regime
    print("\nTraining Indirect regime models...")
    m_indirect_ortho = train_model(orthogonal=True, indirect=True, tag="indirect_ortho")
    m_indirect_generic = train_model(orthogonal=False, indirect=True, tag="indirect_generic")
    
    # 3. Evaluate all
    print("\nEvaluating all models...")
    eval_do = evaluate_model(m_direct_ortho, indirect=False)
    eval_dg = evaluate_model(m_direct_generic, indirect=False)
    eval_io = evaluate_model(m_indirect_ortho, indirect=True)
    eval_ig = evaluate_model(m_indirect_generic, indirect=True)
    
    results = {
        "Direct_Orthogonal": {
            "y_R2": eval_do[0], "Q_linear": eval_do[1], "Q_knn": eval_do[2],
            "gap": eval_do[2] - eval_do[1], "erosion": eval_do[3] - eval_do[4]
        },
        "Direct_Generic": {
            "y_R2": eval_dg[0], "Q_linear": eval_dg[1], "Q_knn": eval_dg[2],
            "gap": eval_dg[2] - eval_dg[1], "erosion": eval_dg[3] - eval_dg[4]
        },
        "Indirect_Orthogonal": {
            "y_R2": eval_io[0], "Q_linear": eval_io[1], "Q_knn": eval_io[2],
            "gap": eval_io[2] - eval_io[1], "erosion": eval_io[3] - eval_io[4]
        },
        "Indirect_Generic": {
            "y_R2": eval_ig[0], "Q_linear": eval_ig[1], "Q_knn": eval_ig[2],
            "gap": eval_ig[2] - eval_ig[1], "erosion": eval_ig[3] - eval_ig[4]
        }
    }
    
    # Check hypotheses
    h1 = (results["Direct_Generic"]["Q_linear"] >= 0.8 and
          results["Direct_Orthogonal"]["Q_linear"] >= 0.8 and
          results["Direct_Generic"]["gap"] < 0.15 and
          results["Direct_Orthogonal"]["gap"] < 0.15)
          
    h2 = (results["Indirect_Generic"]["gap"] >= 0.20 and
          results["Indirect_Generic"]["Q_linear"] < 0.70 and
          results["Indirect_Orthogonal"]["gap"] < 0.15 and
          results["Indirect_Orthogonal"]["Q_linear"] >= 0.75)
          
    h3 = (results["Indirect_Generic"]["erosion"] >= 0.15 and
          results["Indirect_Orthogonal"]["erosion"] < 0.10)
          
    verdict = {
        "H1_direct_legible": bool(h1),
        "H2_indirect_scramble": bool(h2),
        "H3_erosion_mismatch": bool(h3),
        "regime_prediction_confirmed": bool(h1 and h2 and h3),
        "results": results
    }
    
    print("\n--- Summary Results ---")
    for k, v in results.items():
        print(f"{k}:")
        print(f"  Observations R^2: {v['y_R2']:.4f}")
        print(f"  Conserved state Q decode - Linear: {v['Q_linear']:.4f} | kNN: {v['Q_knn']:.4f} | Gap: {v['gap']:.4f}")
        print(f"  Erosion (early - late): {v['erosion']:.4f}")
        
    print(f"\nH1 Direct Legibility: {h1}")
    print(f"H2 Indirect Scrambling: {h2}")
    print(f"H3 Erosion mismatch: {h3}")
    print(f"\nREGIME PREDICTION CONFIRMED: {verdict['regime_prediction_confirmed']}")
    
    os.makedirs("results", exist_ok=True)
    with open("results/leg6_regime_prediction.json", "w") as f:
        json.dump(verdict, f, indent=2)
        
    # Generate visualization
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    
    # Bar plot for scramble gaps
    labels = ["Direct\nOrtho", "Direct\nGeneric", "Indirect\nOrtho", "Indirect\nGeneric"]
    lin_decodes = [results["Direct_Orthogonal"]["Q_linear"], results["Direct_Generic"]["Q_linear"],
                   results["Indirect_Orthogonal"]["Q_linear"], results["Indirect_Generic"]["Q_linear"]]
    knn_decodes = [results["Direct_Orthogonal"]["Q_knn"], results["Direct_Generic"]["Q_knn"],
                   results["Indirect_Orthogonal"]["Q_knn"], results["Indirect_Generic"]["Q_knn"]]
    
    x = np.arange(4)
    width = 0.35
    ax[0].bar(x - width/2, lin_decodes, width, color="seagreen", label="Linear Decode")
    ax[0].bar(x + width/2, knn_decodes, width, color="slategray", label="kNN (Non-linear) Decode")
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(labels)
    ax[0].set_ylabel("Q(t) decode R²")
    ax[0].set_title("Scramble Gap across Regimes")
    ax[0].legend(fontsize=9)
    ax[0].axhline(0.7, color="k", ls="--", lw=0.8)
    
    # Erosion plot
    ax[1].plot([0, 1], [eval_do[3], eval_do[4]], "o-", color="seagreen", label="Direct Ortho")
    ax[1].plot([0, 1], [eval_dg[3], eval_dg[4]], "s-", color="darkorange", label="Direct Generic")
    ax[1].plot([0, 1], [eval_io[3], eval_io[4]], "d-", color="navy", label="Indirect Ortho")
    ax[1].plot([0, 1], [eval_ig[3], eval_ig[4]], "x-", color="crimson", label="Indirect Generic")
    ax[1].set_xticks([0, 1])
    ax[1].set_xticklabels(["Early Path", "Late Path"])
    ax[1].set_ylabel("Linear Decode R²")
    ax[1].set_title("State Legibility Erosion over time")
    ax[1].legend(fontsize=9)
    
    fig.suptitle("Direct vs. Indirect Observation Regime Prediction\n(Symmetry restores legibility only under indirect observation)")
    fig.tight_layout()
    fig.savefig("results/leg6_regime_comparison.png", dpi=140)
    print("Saved results/leg6_regime_prediction.json + .png")


if __name__ == "__main__":
    main()
