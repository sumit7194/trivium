#!/usr/bin/env python3
"""Plot the bottleneck R²(d) curves (whitened vs standardized) for all six datasets.
Run with the tabula venv. Reads results/count_bottleneck.json, writes the figure.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"
r = json.load(open(RESULTS / "count_bottleneck.json"))
FAMILIES = ["schwarzschild", "rn", "dyonic"]
CONV = ["dimensionful", "shape"]
ALG = {"schwarzschild": {"dimensionful": 1, "shape": 0},
       "rn": {"dimensionful": 2, "shape": 1},
       "dyonic": {"dimensionful": 3, "shape": 2}}

fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharex=True, sharey=True)
for j, conv in enumerate(CONV):
    for i, fam in enumerate(FAMILIES):
        ax = axes[j, i]
        e = r[f"{fam}/{conv}"]
        for space, style in (("white_R2", "o-"), ("std_R2", "s--")):
            c = e.get(space, {})
            if not isinstance(c, dict) or not c:
                continue
            ds = sorted(int(k) for k in c)
            vals = [c[str(d)][0] if isinstance(c[str(d)], (list, tuple)) else c[str(d)] for d in ds]
            ax.plot(ds, vals, style, label="whitened" if space == "white_R2" else "standardized")
        ax.axvline(ALG[fam][conv], color="crimson", ls=":", lw=1,
                   label=f"ansatz moduli = {ALG[fam][conv]}")
        ax.set_title(f"{fam} / {conv}")
        ax.set_ylim(-0.1, 1.05)
        ax.grid(alpha=0.3)
        if i == 0:
            ax.set_ylabel("held-out R²")
        if j == 1:
            ax.set_xlabel("bottleneck width d")
        ax.legend(fontsize=7, loc="lower right")
fig.suptitle("Leg 1 — neural bottleneck count vs ansatz exact moduli\n"
             "(whitened readout = intrinsic dim; dyonic shows the Q²+P² degeneracy)")
fig.tight_layout()
out = RESULTS / "leg1_count_curves.png"
fig.savefig(out, dpi=140)
print(f"wrote {out}")
