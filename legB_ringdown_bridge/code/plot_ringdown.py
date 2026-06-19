#!/usr/bin/env python3
"""Move B — the figure: eikonal Kerr QNM Q(χ) and Mω_R(χ) with GW250114 overlaid.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python plot_ringdown.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"


def main():
    eik = json.loads((RESULTS / "eikonal_kerr_qnm.json").read_text())["rows"]
    cmp = json.loads((RESULTS / "compare_ringdown.json").read_text())
    m = cmp["measured"]
    chis = [r["a"] for r in eik]
    Qs = [r["Q"] for r in eik]
    MwRs = [r["MwR"] for r in eik]
    chi_m, chi_lo, chi_hi = m["chi_sbi"], 0.641, 0.887

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))

    ax[0].plot(chis, Qs, "o-", c="C0", label="ansatz eikonal Kerr (exact metric)")
    ax[0].axhline(m["Q220"], ls="--", c="C3", label=f"measured Q₂₂₀ = {m['Q220']:.2f}")
    ax[0].axvspan(chi_lo, chi_hi, color="C3", alpha=.12, label="remnant χ 90% CI")
    ax[0].axvline(chi_m, ls=":", c="C3", alpha=.6)
    ax[0].set_xlabel("remnant spin χ"); ax[0].set_ylabel("quality factor Q₂₂₀")
    ax[0].set_title("Quality factor (M-independent)\nQ = πfτ"); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)

    ax[1].plot(chis, MwRs, "o-", c="C0", label="ansatz eikonal Kerr (exact metric)")
    ax[1].axhline(m["MwR_sbi"], ls="--", c="C3", label=f"measured Mω_R = {m['MwR_sbi']:.3f}")
    ax[1].axvspan(chi_lo, chi_hi, color="C3", alpha=.12, label="remnant χ 90% CI")
    ax[1].axvline(chi_m, ls=":", c="C3", alpha=.6)
    ax[1].set_xlabel("remnant spin χ"); ax[1].set_ylabel("Mω_R (220)")
    ax[1].set_title("Dimensionless real frequency\nMω_R = mΩ_c (light ring)"); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)

    fig.suptitle("Move B — eikonal Kerr QNM (ansatz exact metric) vs measured GW250114 ringdown\n"
                 "the spin correction is essential; Schwarzschild (χ=0) misses by 40–50%",
                 fontweight="bold")
    fig.tight_layout()
    out = RESULTS / "legB_ringdown_bridge.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
