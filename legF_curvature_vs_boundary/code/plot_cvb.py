#!/usr/bin/env python3
"""Move F — the 2×2 figure: which cell shows the bulk/edge effect?

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python plot_cvb.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"


def main():
    d = json.loads((RESULTS / "curvature_vs_boundary.json").read_text())["rows"]
    order = ["hyperbolic", "sphere", "flat_disk", "flat_torus"]
    labels = ["hyperbolic\n(curved + boundary)", "sphere S²\n(curved, NO boundary)",
              "flat disk\n(flat + boundary)", "flat torus\n(flat, no boundary)"]
    ratios = [d[k]["ratio"] for k in order]
    cols = ["C3" if r > 1.5 else "C7" for r in ratios]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(labels, ratios, color=cols)
    ax.axhline(1.0, ls=":", c="k", alpha=.5, label="no edge effect")
    ax.axhline(1.5, ls="--", c="C3", alpha=.4, label="effect threshold")
    ax.set_ylabel("edge / bulk recovery error")
    ax.set_title("Move F — curvature or boundary?\nOnly the space with a CONFORMAL boundary "
                 "(diverging metric) shows the bulk/edge effect", fontweight="bold")
    ax.legend(fontsize=9); ax.grid(alpha=.3, axis="y")
    for b, r in zip(bars, ratios):
        ax.text(b.get_x() + b.get_width() / 2, r + 0.05, f"{r:.2f}×", ha="center", fontsize=10)
    fig.tight_layout()
    out = RESULTS / "legF_curvature_vs_boundary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
