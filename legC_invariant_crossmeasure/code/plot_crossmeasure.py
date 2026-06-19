#!/usr/bin/env python3
"""Move C — the figure: the legibility ladder for ansatz's coordinate-free Weyl invariant.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python plot_crossmeasure.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"


def main():
    p = json.loads((RESULTS / "probe_invariants.json").read_text())
    r2 = p["r2_weyl"]
    acc = p["acc_OD"]

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))

    names = ["linear\n(Ridge)", "nonlinear\n(kNN)", "nonlinear\n(MLP)", "invariant\nfeatures\n(ceiling)"]
    vals = [r2["linear"], r2["knn"], r2["mlp"], r2["invariant_ref"]]
    cols = ["C3", "C1", "C0", "C2"]
    ax[0].bar(names, vals, color=cols)
    ax[0].axhline(0.9, ls="--", c="k", alpha=.4, label="P1 threshold 0.9")
    ax[0].set_ylabel("held-out R²  (Weyl invariant recovery)")
    ax[0].set_title("The legibility gap\nWeyl invariant: present (nonlinear) but NOT linearly legible")
    ax[0].set_ylim(-0.1, 1.05); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3, axis="y")
    for i, v in enumerate(vals):
        ax[0].text(i, v + 0.02 if v > 0 else 0.02, f"{v:.2f}", ha="center", fontsize=9)

    anames = ["via linear", "via MLP", "via ceiling"]
    avals = [acc["via_linear"], acc["via_nonlinear"], acc["via_invariant_ref"]]
    ax[1].bar(anames, avals, color=["C3", "C0", "C2"])
    ax[1].axhline(0.95, ls="--", c="k", alpha=.4, label="P3 threshold 0.95")
    ax[1].axhline(0.5, ls=":", c="gray", alpha=.5, label="chance")
    ax[1].set_ylabel("held-out accuracy")
    ax[1].set_title("Petrov O vs D (the fine boundary)\nrecovered in the large, NOT at the conformal-flat edge")
    ax[1].set_ylim(0, 1.05); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3, axis="y")
    for i, v in enumerate(avals):
        ax[1].text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=9)

    fig.suptitle("Move C — the coordinate-free invariant cross-measure\n"
                 "ansatz's exact Weyl invariant is present in frame-randomized tidal observations; "
                 "a net recovers its magnitude (not linearly), but not the fine Petrov boundary",
                 fontweight="bold")
    fig.tight_layout()
    out = RESULTS / "legC_invariant_crossmeasure.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
