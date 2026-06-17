#!/usr/bin/env python3
"""Plot the leg-2 probe ladder: linear vs nonlinear legibility of the overtone invariant,
per checkpoint, on REAL data -- showing the ABSENCE of a scramble gap (info-limited, not
legibility-limited). Run with the sklearn/curvature venv."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent.parent / "results"
r = json.load(open(RESULTS / "probe_ladder.json"))["rows"]
cks = list(r)
short = [c.replace("11_tonecount", "base").replace("base_", "") for c in cks]

lin = [r[c]["L_inv_cross"] for c in cks]      # linear legibility (fit SIM->REAL)
non = [r[c]["N_inv_real"] for c in cks]       # nonlinear info presence (REAL)
tr = [r[c]["T_real"] for c in cks]            # transfer axis (model real-noise AUC)

x = np.arange(len(cks))
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.bar(x - 0.2, lin, 0.38, label="linear decode (legibility)", color="steelblue")
ax.bar(x + 0.2, non, 0.38, label="nonlinear kNN (info present)", color="indianred")
ax.plot(x, tr, "ko--", label="transfer (model real-noise AUC)")
ax.axhline(0.5, color="gray", lw=0.8, ls=":")
ax.set_xticks(x); ax.set_xticklabels(short, rotation=15)
ax.set_ylabel("AUC")
ax.set_ylim(0.45, 0.75)
ax.set_title("Leg 2 — overtone invariant on REAL data: linear ≈ nonlinear (no scramble)\n"
             "the sim→real gap here is INFORMATION-limited, not legibility-limited")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout()
out = RESULTS / "leg2_probe_ladder.png"
fig.savefig(out, dpi=140)
print(f"wrote {out}")
