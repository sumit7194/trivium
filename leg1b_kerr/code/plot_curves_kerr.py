#!/usr/bin/env python3
"""Plot the bottleneck R²(d) curves (whitened vs standardized) for leg-1b Kerr datasets.
Run with the curvature venv. Reads results/count_bottleneck_kerr.json, writes the figure.

Layout: 2 rows (dimensionful / shape) × 3 columns (kerr / kn_full / kn_deg).
Overlays the ansatz exact moduli count as a vertical line.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"
r = json.load(open(RESULTS / "count_bottleneck_kerr.json"))
FAMILIES = ["kerr", "kn_full", "kn_deg"]
CONV = ["dimensionful", "shape"]
# Ansatz exact moduli counts (from PREREGISTRATION.md §3):
#   Kerr:    dim 2, shape 1
#   KN full: dim 3, shape 2  (frame-dragging lifts degeneracy)
#   KN deg:  dim 2, shape 1  (Δ-symmetric → sees only a²+Q²)
ALG = {"kerr":    {"dimensionful": 2, "shape": 1},
       "kn_full": {"dimensionful": 3, "shape": 2},
       "kn_deg":  {"dimensionful": 2, "shape": 1}}
LABELS = {"kerr": "Kerr", "kn_full": "KN (full)", "kn_deg": "KN (Δ-symmetric)"}

fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharex=True, sharey=True)
for j, conv in enumerate(CONV):
    for i, fam in enumerate(FAMILIES):
        ax = axes[j, i]
        key = f"{fam}/{conv}"
        e = r.get(key, {})
        for space, style in (("white_R2", "o-"), ("std_R2", "s--")):
            c = e.get(space, {})
            if not isinstance(c, dict) or not c:
                continue
            ds = sorted(int(k) for k in c)
            vals = [c[str(d)][0] if isinstance(c[str(d)], (list, tuple)) else c[str(d)] for d in ds]
            ax.plot(ds, vals, style, label="whitened" if space == "white_R2" else "standardized")
        ax.axvline(ALG[fam][conv], color="crimson", ls=":", lw=1,
                   label=f"ansatz moduli = {ALG[fam][conv]}")
        ax.set_title(f"{LABELS[fam]} / {conv}")
        ax.set_ylim(-0.1, 1.05)
        ax.grid(alpha=0.3)
        if i == 0:
            ax.set_ylabel("held-out R²")
        if j == 1:
            ax.set_xlabel("bottleneck width d")
        ax.legend(fontsize=7, loc="lower right")
fig.suptitle("Leg 1b — neural bottleneck count: Kerr / Kerr-Newman\n"
             "(whitened readout = intrinsic dim; KN-full should recover 3, KN-Δ should collapse to 2)")
fig.tight_layout()
out = RESULTS / "leg1b_count_curves.png"
fig.savefig(out, dpi=140)
print(f"wrote {out}")
