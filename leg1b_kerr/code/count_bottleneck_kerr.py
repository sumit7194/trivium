#!/usr/bin/env python3
"""Leg-1b TABULA side — neural bottleneck count for Kerr / Kerr-Newman observables.

Run with the curvature venv (torch):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python count_bottleneck_kerr.py

BRIDGE code. Reuses leg 1's counting instrument EXACTLY (same AE, same sweep, same
knee rule) on the Kerr observable arrays written by `kerr_observables.py`.
Reads ONLY obs_.npz arrays — never imports ansatz, never sees (M,a,Q) — the §2
blindness, enforced mechanically.

Families: kerr, kn_full, kn_deg (each × dimensionful / shape).
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
from torch import nn

# ---- counting machinery, lifted from leg 1's count_bottleneck.py identically ----

RESULTS = Path(__file__).resolve().parent.parent / "results"
FAMILIES = ["kerr", "kn_full", "kn_deg"]
CONVENTIONS = ["dimensionful", "shape"]
DIMS = (0, 1, 2, 3, 4)
SEEDS = (0, 1, 2)
STEPS = 4000
BATCH = 512
WHITEN_FLOOR = 1e-7


class AE(nn.Module):
    """Bottleneck autoencoder. d=0 => the decoder sees a zero code and can only emit
    a learned constant (the mean), giving R²≈0 by construction (the baseline)."""

    def __init__(self, m: int, d: int):
        super().__init__()
        self.d = d
        self.enc = nn.Sequential(
            nn.Linear(m, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, max(d, 1)),
        )
        self.dec = nn.Sequential(
            nn.Linear(max(d, 1), 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(),
            nn.Linear(64, m),
        )

    def forward(self, x):
        if self.d == 0:
            code = torch.zeros(x.shape[0], 1)
        else:
            code = self.enc(x)
        return self.dec(code)


def r2(model, Xte):
    with torch.no_grad():
        pred = model(torch.from_numpy(Xte)).numpy()
    sse = ((pred - Xte) ** 2).sum()
    sst = ((Xte - Xte.mean(0)) ** 2).sum()
    return 1.0 - sse / sst if sst > 0 else 1.0


def train_ae(Xtr, Xte, d, seed):
    torch.manual_seed(1000 + 17 * d + seed)
    m = Xtr.shape[1]
    model = AE(m, d)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    lossf = nn.MSELoss()
    Xt = torch.from_numpy(Xtr)
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
    """Split, then return standardized and whitened versions (fit on train only)."""
    Xtr_raw, Xte_raw = X[:n_train], X[n_train:]
    mu, sd = Xtr_raw.mean(0), Xtr_raw.std(0)
    keep = sd > 1e-9
    if keep.sum() == 0:
        return None
    std = lambda A: ((A[:, keep] - mu[keep]) / sd[keep]).astype(np.float32)
    Xtr_s, Xte_s = std(Xtr_raw), std(Xte_raw)
    U, S, Vt = np.linalg.svd(Xtr_s - Xtr_s.mean(0), full_matrices=False)
    var = S ** 2
    kept = var / var.max() > WHITEN_FLOOR
    comps = Vt[kept]
    scale = S[kept] / np.sqrt(len(Xtr_s))
    white = lambda A: (((A - Xtr_s.mean(0)) @ comps.T) / scale).astype(np.float32)
    return {
        "std": (Xtr_s, Xte_s),
        "white": (white(Xtr_s), white(Xte_s)),
        "linear_spectrum": (var / var.sum()).round(5).tolist(),
        "n_linear_kept": int(kept.sum()),
        "n_features": int(keep.sum()),
    }


def count_dim(white_R2, dims):
    """Count = # widths d>=1 whose whitened marginal R² gain > 2%. Same rule as leg 1."""
    count = 0
    for d in dims:
        if d == 0:
            continue
        gain = white_R2[d][0] - white_R2[d-1][0]
        if gain > 0.02:
            count += 1
    return count


def main():
    report = {}
    summary_lines = []
    for conv in CONVENTIONS:
        for fam in FAMILIES:
            f = RESULTS / f"obs_{fam}_{conv}.npz"
            if not f.exists():
                print(f"SKIP {f} — not found")
                continue
            d_npz = np.load(f)
            X = d_npz["X"].astype(np.float64)
            n_train = int(d_npz["n_train"])
            key = f"{fam}/{conv}"
            p = prep(X, n_train)
            if p is None:
                report[key] = {"count_note": "no varying features -> 0",
                               "std_R2": {0: 1.0}, "white_R2": {0: 1.0},
                               "count": 0}
                print(f"{key:26s}  (no varying features) -> intrinsic dim 0")
                continue
            res = {"linear_spectrum": p["linear_spectrum"],
                   "n_linear_kept": p["n_linear_kept"],
                   "n_features": p["n_features"], "std_R2": {}, "white_R2": {}}
            for space in ("std", "white"):
                Xtr, Xte = p[space]
                for d in DIMS:
                    vals = [train_ae(Xtr, Xte, d, s) for s in SEEDS]
                    res[f"{space}_R2"][d] = [float(np.mean(vals)), float(np.std(vals))]
            res["count"] = count_dim(res["white_R2"], DIMS)
            report[key] = res
            sp_str = ",".join(f"{v:.3f}" for v in p["linear_spectrum"][:4])
            print(f"\n{key}  (features={p['n_features']}, linear PCs kept={p['n_linear_kept']}, "
                  f"spectrum[:4]={sp_str})")
            for space in ("std", "white"):
                row = "  ".join(f"d{d}:{res[f'{space}_R2'][d][0]:.4f}" for d in DIMS)
                print(f"   {space:5s} R²(d):  {row}")
            print(f"   → count = {res['count']}")
            summary_lines.append(f"{key:22s} count={res['count']}")

    out = RESULTS / "count_bottleneck_kerr.json"
    out.write_text(json.dumps(report, indent=1, default=str))
    print(f"\nwrote {out}")
    print("\n=== SUMMARY ===")
    for l in summary_lines:
        print(l)


if __name__ == "__main__":
    main()
