#!/usr/bin/env python3
"""Leg 5 — The Strong-field Curriculum (Shadow-edge Fidelity).

Compares a naive uniform training set (Curriculum A) against an ansatz-targeted
critical sampling training set (Curriculum B) for learning the photon shadow
and photon sphere. Both datasets have the exact same number of total training
points to control for capacity.
"""

import json
import os
import sys
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DPHI = 0.02
B_TRUE = 3 * np.sqrt(3)  # ~5.196
R_TRUE = 3.0
SEEDS = 3
N_SEGMENTS = 25000

np.seterr(all="ignore")


def ray(b, u0=0.01, nsteps=4000):
    """Integrate a null geodesic in phi. w'=3u^2-u, u'=w. M=1, u=1/r."""
    u = u0
    w = np.sqrt(max(1 / b**2 - u0**2 + 2 * u0**3, 0))
    U, W = [u], [w]
    for _ in range(nsteps):
        a = 3 * u**2 - u
        wh = w + 0.5 * DPHI * a
        u = u + DPHI * wh
        if u >= 0.5:  # Captured
            U.append(u)
            W.append(w)
            return "captured", np.array(U), np.array(W)
        if u <= 0.002 and w < 0:  # Escaped
            return "escaped", np.array(U), np.array(W)
        w = wh + 0.5 * DPHI * (3 * u**2 - u)
        U.append(u)
        W.append(w)
    return "undetermined", np.array(U), np.array(W)


def make_uniform_dataset(n_segments=N_SEGMENTS, seed=0):
    """Curriculum A: Uniform sampling of impact parameters b."""
    rng = np.random.default_rng(seed)
    X, Y = [], []
    while len(X) < n_segments:
        bs = rng.uniform(4.8, 14.0, 50)
        for b in bs:
            _, U, W = ray(b)
            for i in range(len(U) - 1):
                X.append([U[i], W[i]])
                Y.append([U[i+1], W[i+1]])
    return np.array(X[:n_segments], np.float32), np.array(Y[:n_segments], np.float32)


def make_targeted_dataset(n_segments=N_SEGMENTS, seed=0):
    """Curriculum B: Concentrate sampling near critical winding window."""
    rng = np.random.default_rng(seed)
    X_crit, Y_crit = [], []
    X_bg, Y_bg = [], []
    
    n_crit_target = int(n_segments * 0.6)
    n_bg_target = n_segments - n_crit_target
    
    # Critical winding segments (b near b_crit)
    while len(X_crit) < n_crit_target:
        bs = rng.uniform(5.1, 5.7, 50)
        for b in bs:
            _, U, W = ray(b)
            for i in range(len(U) - 1):
                X_crit.append([U[i], W[i]])
                Y_crit.append([U[i+1], W[i+1]])
                
    # Background segments (excluding the critical region)
    while len(X_bg) < n_bg_target:
        b_zones = [rng.uniform(4.8, 5.1), rng.uniform(5.7, 14.0)]
        b = rng.choice(b_zones)
        _, U, W = ray(b)
        for i in range(len(U) - 1):
            X_bg.append([U[i], W[i]])
            Y_bg.append([U[i+1], W[i+1]])
            
    X = X_crit[:n_crit_target] + X_bg[:n_bg_target]
    Y = Y_crit[:n_crit_target] + Y_bg[:n_bg_target]
    return np.array(X, np.float32), np.array(Y, np.float32)


class Photon(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 128), nn.GELU(),
            nn.Linear(128, 128), nn.GELU(),
            nn.Linear(128, 128), nn.GELU(),
            nn.Linear(128, 2)
        )

    def forward(self, x):
        return x + self.net(x)


def train(X, Y, steps=6000, seed=0):
    torch.manual_seed(seed)
    n = len(X)
    ntr = int(n * 0.9)
    idx = np.random.default_rng(seed).permutation(n)
    Xt = torch.from_numpy(X[idx])
    Yt = torch.from_numpy(Y[idx])
    m = Photon()
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    rng = np.random.default_rng(seed + 1)
    for step in range(steps):
        b = rng.integers(0, ntr, 256)
        loss = nn.functional.mse_loss(m(Xt[b]), Yt[b])
        opt.zero_grad()
        loss.backward()
        opt.step()
    m.eval()
    return m


def bcrit_capture(m, nsteps=9000):
    """Hardened batched ray-tracer: find capture/escape boundary in b."""
    bs = np.linspace(4.9, 7.4, 170)
    u = torch.tensor(bs * 0 + 0.01, dtype=torch.float32)
    w = torch.tensor(np.sqrt(np.maximum(1 / bs**2 - 0.01**2 + 2 * 0.01**3, 0)), dtype=torch.float32)
    status = torch.zeros(len(bs))
    active = torch.ones(len(bs), dtype=torch.bool)
    for _ in range(nsteps):
        with torch.no_grad():
            o = m(torch.stack([u, w], 1))
        u, w = o[:, 0], o[:, 1]
        bad = ~(torch.isfinite(u) & torch.isfinite(w))
        cap = (u >= 0.5) & active & ~bad
        esc = (((u <= 0.003) & (w < 0)) | bad) & active
        status[cap] = 1
        status[esc] = -1
        active = active & ~(cap | esc)
        u = torch.clamp(torch.where(active, u, torch.full_like(u, 0.3)), -0.05, 0.55)
        w = torch.clamp(torch.where(active, w, torch.zeros_like(w)), -6, 6)
        if not active.any():
            break
    cs = status.numpy()
    capi = np.where(cs == 1)[0]
    if not len(capi):
        return None
    last = capi.max()
    esci = np.where((cs == -1) & (np.arange(len(cs)) > last))[0]
    return float(bs[last]) if not len(esci) else float(0.5 * (bs[last] + bs[esci[0]]))


def get_photon_sphere(m, X):
    """Estimate photon sphere r_ps = 1/u_ps from learned force g(u)=0."""
    with torch.no_grad():
        gX = (m(torch.from_numpy(X)).numpy()[:, 1] - X[:, 1]) / DPHI
    uX = X[:, 0]
    edges = np.linspace(0.22, 0.47, 26)
    ctr = 0.5 * (edges[:-1] + edges[1:])
    bing = np.array([np.median(gX[(uX >= edges[i]) & (uX < edges[i + 1])]) if np.any((uX >= edges[i]) & (uX < edges[i + 1])) else np.nan for i in range(len(ctr))])
    ok = np.isfinite(bing)
    if ok.sum() < 3:
        return None
    Acol = np.stack([ctr[ok] ** 2, ctr[ok]], 1)
    (c2, c1), *_ = np.linalg.lstsq(Acol, bing[ok], rcond=None)
    roots = np.roots([c2, c1, 0.0])
    roots = roots[np.isreal(roots)].real
    cand = [r for r in roots if 0.1 < r < 0.49]
    u_ps = float(cand[0]) if cand else None
    return (1.0 / u_ps) if u_ps else None


def main():
    print("RUNNING LEG 5: STRONG-FIELD CURRICULUM STUDY\n")
    
    results = {}
    
    for name, make_fn in [("Uniform (Curriculum A)", make_uniform_dataset),
                          ("Targeted (Curriculum B)", make_targeted_dataset)]:
        print(f"Evaluating {name}...")
        bcrits = []
        r_pss = []
        
        for s in range(SEEDS):
            # Generate dataset (independent seeds for dataset and training)
            X, Y = make_fn(seed=100 * s + 42)
            m = train(X, Y, seed=s)
            
            # Evaluate shadow boundary
            bc = bcrit_capture(m)
            if bc is not None:
                bcrits.append(bc)
                
            # Evaluate photon sphere
            rp = get_photon_sphere(m, X)
            if rp is not None:
                r_pss.append(rp)
                
            bc_str = f"{bc:.4f}" if bc is not None else "None"
            rp_str = f"{rp:.4f}" if rp is not None else "None"
            bc_err = f"{abs(bc-B_TRUE)/B_TRUE*100:.2f}%" if bc is not None else "N/A"
            rp_err = f"{abs(rp-R_TRUE)/R_TRUE*100:.2f}%" if rp is not None else "N/A"
            print(f"  Seed {s}: b_crit={bc_str} (error {bc_err}), r_ps={rp_str} (error {rp_err})")
            
        bcrits = np.array(bcrits)
        r_pss = np.array(r_pss)
        
        results[name] = {
            "b_crit_mean": float(bcrits.mean()) if len(bcrits) else float("nan"),
            "b_crit_std": float(bcrits.std()) if len(bcrits) else float("nan"),
            "b_crit_err": float(abs(bcrits.mean() - B_TRUE) / B_TRUE) if len(bcrits) else float("nan"),
            "r_ps_mean": float(r_pss.mean()) if len(r_pss) else float("nan"),
            "r_ps_std": float(r_pss.std()) if len(r_pss) else float("nan"),
            "r_ps_err": float(abs(r_pss.mean() - R_TRUE) / R_TRUE) if len(r_pss) else float("nan")
        }
        
    print("\n--- Summary Results ---")
    for name, res in results.items():
        print(f"{name}:")
        bc_mean_str = f"{res['b_crit_mean']:.4f} +- {res['b_crit_std']:.4f}" if np.isfinite(res['b_crit_mean']) else "N/A"
        bc_err_str = f"{res['b_crit_err']*100:.2f}%" if np.isfinite(res['b_crit_err']) else "N/A"
        rp_mean_str = f"{res['r_ps_mean']:.4f} +- {res['r_ps_std']:.4f}" if np.isfinite(res['r_ps_mean']) else "N/A"
        rp_err_str = f"{res['r_ps_err']*100:.2f}%" if np.isfinite(res['r_ps_err']) else "N/A"
        print(f"  b_crit = {bc_mean_str} (err: {bc_err_str})")
        print(f"  r_ps   = {rp_mean_str} (err: {rp_err_str})")
        
    # Check hypotheses
    uniform_res = results["Uniform (Curriculum A)"]
    targeted_res = results["Targeted (Curriculum B)"]
    
    h1 = targeted_res["b_crit_err"] < uniform_res["b_crit_err"] if (np.isfinite(targeted_res["b_crit_err"]) and np.isfinite(uniform_res["b_crit_err"])) else False
    h2 = targeted_res["r_ps_err"] < uniform_res["r_ps_err"] if (np.isfinite(targeted_res["r_ps_err"]) and np.isfinite(uniform_res["r_ps_err"])) else (np.isfinite(targeted_res["r_ps_err"]) and not np.isfinite(uniform_res["r_ps_err"]))
    h3 = uniform_res["b_crit_err"] / max(targeted_res["b_crit_err"], 1e-9) >= 1.5 if (np.isfinite(targeted_res["b_crit_err"]) and np.isfinite(uniform_res["b_crit_err"])) else False
    
    verdict = {
        "H1_shadow_edge_accuracy_improved": bool(h1),
        "H2_photon_sphere_accuracy_improved": bool(h2),
        "H3_relative_error_ratio_above_1_5": bool(h3),
        "curriculum_benefit_confirmed": bool(h1 and h2 and h3),
        "results": results
    }
    
    h1_str = f"(targeted {targeted_res['b_crit_err']*100:.2f}% vs uniform {uniform_res['b_crit_err']*100:.2f}%)" if (np.isfinite(targeted_res["b_crit_err"]) and np.isfinite(uniform_res["b_crit_err"])) else "N/A"
    h2_str = f"(targeted {targeted_res['r_ps_err']*100:.2f}% vs uniform {uniform_res['r_ps_err']*100:.2f}%)" if (np.isfinite(targeted_res["r_ps_err"]) and np.isfinite(uniform_res["r_ps_err"])) else ("(targeted resolved, uniform failed)" if np.isfinite(targeted_res["r_ps_err"]) else "N/A")
    h3_str = f"(ratio: {uniform_res['b_crit_err']/max(targeted_res['b_crit_err'], 1e-9):.2f}x)" if (np.isfinite(targeted_res["b_crit_err"]) and np.isfinite(uniform_res["b_crit_err"])) else "N/A"
    
    print(f"\nH1 shadow-edge error improved: {h1} {h1_str}")
    print(f"H2 photon sphere error improved: {h2} {h2_str}")
    print(f"H3 relative error improvement >= 1.5x: {h3} {h3_str}")
    
    os.makedirs("results", exist_ok=True)
    with open("results/leg5_curriculum_comparison.json", "w") as f:
        json.dump(verdict, f, indent=2)
        
    # Generate visualization
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    
    names = ["Curriculum A\n(Uniform)", "Curriculum B\n(Targeted)"]
    b_means = [uniform_res["b_crit_mean"], targeted_res["b_crit_mean"]]
    b_stds = [uniform_res["b_crit_std"] if np.isfinite(uniform_res["b_crit_std"]) else 0.0,
              targeted_res["b_crit_std"] if np.isfinite(targeted_res["b_crit_std"]) else 0.0]
    
    ax[0].errorbar(names, b_means, yerr=b_stds, fmt="o", color="crimson", capsize=5, elinewidth=2, ms=8)
    ax[0].axhline(B_TRUE, color="navy", ls="--", label=f"exact 3√3 = {B_TRUE:.3f}")
    ax[0].set_ylabel("shadow edge b_crit (M)")
    ax[0].set_title("Shadow Boundary Accuracy")
    ax[0].legend(fontsize=9)
    
    r_means = [uniform_res["r_ps_mean"], targeted_res["r_ps_mean"]]
    r_stds = [uniform_res["r_ps_std"] if np.isfinite(uniform_res["r_ps_std"]) else 0.0,
              targeted_res["r_ps_std"] if np.isfinite(targeted_res["r_ps_std"]) else 0.0]
    
    ax[1].errorbar(names, r_means, yerr=r_stds, fmt="s", color="darkorange", capsize=5, elinewidth=2, ms=8)
    ax[1].axhline(R_TRUE, color="navy", ls="--", label=f"exact r_ps = {R_TRUE}")
    ax[1].set_ylabel("photon sphere r_ps (M)")
    ax[1].set_title("Photon Sphere Radius Accuracy")
    ax[1].legend(fontsize=9)
    
    fig.suptitle("Theory-Guided Strong-Field Curriculum Comparison\n(Controlled total training segments N=25,000)")
    fig.tight_layout()
    fig.savefig("results/leg5_curriculum_curves.png", dpi=140)
    print("Saved results/leg5_curriculum_comparison.json + .png")


if __name__ == "__main__":
    main()
