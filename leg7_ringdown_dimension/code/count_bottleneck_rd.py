#!/usr/bin/env python3
"""Leg 7 — Ringdown Intrinsic Dimension: bottleneck autoencoder sweep.

Trains bottleneck autoencoders of varying widths d on simulated/noise-injected
ringdowns. Finds the knee of the R²(d) curve.
"""

import json
import os
import sys
from pathlib import Path
import numpy as np
import torch
from torch import nn

RESULTS = Path(__file__).resolve().parent.parent.parent / "results"
DIMS = (0, 1, 2, 3, 4, 5)
SEEDS = (0, 1, 2)
STEPS = 4000
BATCH = 512
WHITEN_FLOOR = 1e-6


class AE(nn.Module):
    def __init__(self, m: int, d: int):
        super().__init__()
        self.d = d
        self.enc = nn.Sequential(
            nn.Linear(m, 128), nn.Tanh(), nn.Linear(128, 64), nn.Tanh(),
            nn.Linear(64, max(d, 1)),
        )
        self.dec = nn.Sequential(
            nn.Linear(max(d, 1), 64), nn.Tanh(), nn.Linear(64, 128), nn.Tanh(),
            nn.Linear(128, m),
        )

    def forward(self, x):
        if self.d == 0:
            code = torch.zeros(x.shape[0], 1, device=x.device)
        else:
            code = self.enc(x)
        return self.dec(code)


def r2(model, Xte):
    device = next(model.parameters()).device
    model.eval()
    with torch.no_grad():
        pred = model(torch.from_numpy(Xte).to(device)).cpu().numpy()
    sse = ((pred - Xte) ** 2).sum()
    sst = ((Xte - Xte.mean(0)) ** 2).sum()
    return 1.0 - sse / sst if sst > 0 else 1.0


def train_ae(Xtr, Xte, d, seed):
    torch.manual_seed(1000 + 17 * d + seed)
    device = torch.device("cpu")
    m = Xtr.shape[1]
    model = AE(m, d).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.MSELoss()
    Xt = torch.from_numpy(Xtr).to(device)
    rng = np.random.default_rng(seed)
    for _ in range(STEPS):
        idx = rng.integers(0, Xtr.shape[0], BATCH)
        xb = Xt[idx]
        opt.zero_grad()
        loss = lossf(model(xb), xb)
        loss.backward()
        opt.step()
    return r2(model, Xte)


def prep(X, n_train):
    Xtr_raw, Xte_raw = X[:n_train], X[n_train:]
    mu, sd = Xtr_raw.mean(0), Xtr_raw.std(0)
    keep = sd > 1e-7
    if keep.sum() == 0:
        return None
    
    std = lambda A: ((A[:, keep] - mu[keep]) / sd[keep]).astype(np.float32)
    Xtr_s, Xte_s = std(Xtr_raw), std(Xte_raw)
    
    # PCA Whitening on train standardized
    cov = np.cov(Xtr_s, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    # Sort descending
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    
    kept = eigvals / max(eigvals[0], 1e-9) > WHITEN_FLOOR
    comps = eigvecs[:, kept].T  # [k, m']
    scale = np.sqrt(eigvals[kept])
    
    # Prevent divide by zero on flat directions
    scale = np.clip(scale, 1e-9, None)
    
    white = lambda A: (((A - Xtr_s.mean(0)) @ comps.T) / scale).astype(np.float32)
    return {
        "std": (Xtr_s, Xte_s),
        "white": (white(Xtr_s), white(Xte_s)),
        "linear_spectrum": (eigvals / eigvals.sum()).round(5).tolist(),
        "n_linear_kept": int(kept.sum()),
        "n_features": int(keep.sum()),
    }


def main():
    report = {}
    files = {
        "locked": "obs_rd_locked.npz",
        "free": "obs_rd_free.npz",
        "noise": "obs_rd_noise.npz"
    }
    
    for key, filename in files.items():
        f = RESULTS / filename
        d_npz = np.load(f)
        X = d_npz["obs"].astype(np.float64)
        n_train = int(len(X) * 0.9)
        
        p = prep(X, n_train)
        if p is None:
            report[key] = {"count_note": "no varying features", "std_R2": {0: 1.0}, "white_R2": {0: 1.0}}
            print(f"{key}  (no varying features) -> 0")
            continue
            
        res = {
            "linear_spectrum": p["linear_spectrum"],
            "n_linear_kept": p["n_linear_kept"],
            "n_features": p["n_features"],
            "std_R2": {},
            "white_R2": {}
        }
        
        for space in ("std", "white"):
            Xtr, Xte = p[space]
            res[f"{space}_R2"] = {}
            for d in DIMS:
                vals = [train_ae(Xtr, Xte, d, s) for s in SEEDS]
                res[f"{space}_R2"][str(d)] = [float(np.mean(vals)), float(np.std(vals))]
                
        report[key] = res
        sp_str = ",".join(f"{v:.3f}" for v in p["linear_spectrum"][:4])
        print(f"\n{key} (features={p['n_features']}, linear PCs kept={p['n_linear_kept']}, spectrum[:4]={sp_str})")
        for space in ("std", "white"):
            row = "  ".join(f"d{d}:{res[f'{space}_R2'][str(d)][0]:.4f}" for d in DIMS)
            print(f"  {space:5s} R²(d): {row}")
            
    out = RESULTS / "leg7_count_bottleneck_rd.json"
    out.write_text(json.dumps(report, indent=1, default=str))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
