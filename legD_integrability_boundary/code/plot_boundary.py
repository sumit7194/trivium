#!/usr/bin/env python3
"""Move D — the integrability-boundary figure: three independent views vs deformation ε.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python plot_boundary.py

Overlays tabula's held-out variance-ratio, ansatz's Killing-tensor residual, and the SALI
chaos index across ε, with the EXISTS/DESTROYED thresholds, so the boundary ε* (and whether
the three methods agree on it) is visible."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"
EPS_GRID = [0.00, 0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35]


def main():
    meta = json.loads((RESULTS / "sweep_meta.json").read_text())
    sali = {r["eps"]: r["min_SALI"] for r in meta["rows"]}
    tab, ans = {}, {}
    for eps in EPS_GRID:
        tab[eps] = json.loads((RESULTS / f"candidate_eps{eps:.2f}.json").read_text())["heldout_varratio"]
        ans[eps] = json.loads((RESULTS / f"certify_eps{eps:.2f}.json").read_text())["norm_resid"]

    xs = EPS_GRID
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))

    ax[0].semilogy(xs, [tab[e] for e in xs], "o-", label="tabula: held-out var-ratio (blind)")
    ax[0].semilogy(xs, [ans[e] for e in xs], "s-", label="ansatz: Killing-tensor residual")
    ax[0].axhline(1e-2, ls="--", c="C0", alpha=.5, label="tabula EXISTS threshold (ε_T)")
    ax[0].axhline(1e-3, ls="--", c="C1", alpha=.5, label="ansatz EXISTS threshold")
    ax[0].set_xlabel("deformation ε"); ax[0].set_ylabel("(lower = more conserved)")
    ax[0].set_title("Where Kerr's hidden symmetry dies\n(two bridge oracles)")
    ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)

    ax[1].plot(xs, [sali[e] for e in xs], "^-", c="C2", label="SALI (chaos index)")
    ax[1].axhline(0.0, ls=":", c="k", alpha=.4)
    ax[1].set_xlabel("deformation ε"); ax[1].set_ylabel("SALI  (→0 chaotic, O(1) regular)")
    ax[1].set_title("Independent dynamics view\n(chaos onset)")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)

    fig.suptitle("Move D — the integrability boundary of a deformed black hole, three ways",
                 fontweight="bold")
    fig.tight_layout()
    out = RESULTS / "legD_integrability_boundary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
