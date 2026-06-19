#!/usr/bin/env python3
"""Move H figure: the horizon edge failure (H1) and the refuted recipe (H3).

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python plot_horizon.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"


def main():
    d = json.loads((RESULTS / "horizon_learnability.json").read_text())
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))

    # left: H1 — learned edge/bulk ratio (log), horizons vs flat null
    names = ["Schwarzschild", "Kerr", "flat null"]
    ratios = [d["schwarzschild"]["learned_edge_over_bulk"], d["kerr"]["learned_edge_over_bulk"],
              d["flat_null"]["learned_edge_over_bulk"]]
    ax[0].bar(names, ratios, color=["C3", "C3", "C7"])
    ax[0].axhline(1.0, ls=":", c="k", alpha=.5, label="no edge failure")
    ax[0].set_yscale("log"); ax[0].set_ylabel("learned edge/bulk error")
    ax[0].set_title("H1 ✅ — the horizon is a learnability edge\n(learned emulator fails 85–88× at the horizon; flat null doesn't)")
    ax[0].legend(fontsize=8); ax[0].grid(alpha=.3, axis="y")
    for i, r in enumerate(ratios):
        ax[0].text(i, r * 1.15, f"{r:.0f}×" if r > 2 else f"{r:.1f}×", ha="center", fontsize=10)

    # right: H3 — max-error of the three emulators (hybrid loses to learned)
    x = ["learned", "asymptotic", "hybrid"]
    sch = [d["schwarzschild"]["max_learned"], d["schwarzschild"]["max_asym"], d["schwarzschild"]["max_hybrid"]]
    ker = [d["kerr"]["max_learned"], d["kerr"]["max_asym"], d["kerr"]["max_hybrid"]]
    import numpy as np
    xi = np.arange(3)
    ax[1].bar(xi - 0.2, sch, 0.4, label="Schwarzschild", color="C0")
    ax[1].bar(xi + 0.2, ker, 0.4, label="Kerr", color="C1")
    ax[1].set_xticks(xi); ax[1].set_xticklabels(x)
    ax[1].set_ylabel("worst-region relative error")
    ax[1].set_title("H3 ✗ — the bulk/exact hybrid recipe FAILS\n(hybrid beats asymptotic but loses to pure-learned)")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=.3, axis="y")

    fig.suptitle("Move H — the horizon is a learnability edge (prediction holds), "
                 "but the exact-edge hybrid recipe is refuted", fontweight="bold")
    fig.tight_layout()
    out = RESULTS / "legH_horizon_learnability.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
