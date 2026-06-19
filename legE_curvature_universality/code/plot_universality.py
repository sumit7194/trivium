#!/usr/bin/env python3
"""Move E — the figure: the meta-findings vs curvature (curved domains vs flat controls).

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python plot_universality.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"


def main():
    d = json.loads((RESULTS / "curvature_universality.json").read_text())
    lg = d["legibility_gap"]; swB = d["sweep_edge_vs_rmax"]

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))

    # left: the legibility gap, curved vs flat
    ax[0].bar(["curved\n(S¹ ring)", "flat\n(line)"],
              [lg["curved_S1"]["gap"], lg["flat_line"]["gap"]], color=["C0", "C7"])
    ax[0].set_ylabel("legibility gap (nonlinear − linear R²)")
    ax[0].set_title("The legibility gap (Move C / leg 2)\n16× larger on the curved manifold")
    ax[0].grid(alpha=.3, axis="y")
    for i, v in enumerate([lg["curved_S1"]["gap"], lg["flat_line"]["gap"]]):
        ax[0].text(i, v + 0.003, f"{v:.3f}", ha="center", fontsize=10)

    # right: the bulk/edge boundary scaling toward the edge
    rms = [r[0] for r in swB]; hyp = [r[1] for r in swB]; euc = [r[2] for r in swB]
    ax[1].plot(rms, hyp, "o-", c="C0", label="curved (hyperbolic disk)")
    ax[1].plot(rms, euc, "s-", c="C7", label="flat (Euclidean control)")
    ax[1].axhline(1.0, ls=":", c="k", alpha=.4, label="no edge penalty")
    ax[1].set_xlabel("edge proximity  r_max → 1"); ax[1].set_ylabel("edge / bulk recovery error")
    ax[1].set_title("The bulk/edge boundary (Moves C, D)\ngrows toward the curved edge; flat stays flat")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)

    fig.suptitle("Move E — the bridge's meta-findings track CURVATURE, not GR\n"
                 "legibility gap & bulk/edge boundary appear in non-GR curved spaces, vanish in flat controls",
                 fontweight="bold")
    fig.tight_layout()
    out = RESULTS / "legE_curvature_universality.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
