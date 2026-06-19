#!/usr/bin/env python3
"""Move G — falsifying Move B: is the QNM agreement meaningful, or a one-parameter fit?

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python falsify_moveB.py

The eikonal gives two independent observables as functions of spin: Q(χ) and Mω_R(χ). If the
agreement with GW250114 is genuine, inverting the MEASURED Q and the MEASURED Mω_R must yield the
SAME spin — and one consistent with deepstrain's measured remnant χ. If they imply DIFFERENT spins,
the 'few-% agreement' was a single tunable number, not a real two-observable consistency. We also
check the measured spin sits inside the band where both curves agree.
"""
import json
from pathlib import Path

import numpy as np

LEGB = Path("/Users/sumit/Github/TheBridge/legB_ringdown_bridge/results")
RESULTS = Path(__file__).resolve().parent.parent / "results"


def invert(grid_x, grid_y, y_meas):
    """spin χ such that the eikonal curve hits the measured value (monotonic interp)."""
    order = np.argsort(grid_y)
    return float(np.interp(y_meas, np.array(grid_y)[order], np.array(grid_x)[order]))


def main():
    print("MOVE G — falsifying Move B: do Q and Mω_R imply the SAME spin? (two-observable consistency)\n")
    eik = json.loads((LEGB / "eikonal_kerr_qnm.json").read_text())["rows"]
    cmp = json.loads((LEGB / "compare_ringdown.json").read_text())["measured"]
    chi = [r["a"] for r in eik]; Q = [r["Q"] for r in eik]; MwR = [r["MwR"] for r in eik]

    Q_meas = cmp["Q220"]; MwR_meas = cmp["MwR_sbi"]; chi_meas = cmp["chi_sbi"]
    chi_from_Q = invert(chi, Q, Q_meas)
    chi_from_MwR = invert(chi, MwR, MwR_meas)

    print(f"  measured remnant spin (deepstrain SBI):  χ = {chi_meas:.3f}  (90% CI ~[0.64, 0.89])")
    print(f"  spin implied by measured Q₂₂₀={Q_meas:.2f}:     χ_Q     = {chi_from_Q:.3f}")
    print(f"  spin implied by measured Mω_R={MwR_meas:.3f}:    χ_Mω_R  = {chi_from_MwR:.3f}")
    spread = abs(chi_from_Q - chi_from_MwR)
    near_meas = abs((chi_from_Q + chi_from_MwR) / 2 - chi_meas) < 0.06
    consistent = spread < 0.06
    print(f"\n  |χ_Q − χ_Mω_R| = {spread:.3f}  (two independent observables agree on the spin?)")
    print(f"  both consistent with the measured remnant spin?  {near_meas}")
    print(f"\n  TEST (Move B) VERDICT: {'SURVIVED ✅ — Q and Mω_R independently imply the same spin, consistent with the measured remnant (genuine 2-observable consistency, not a 1-parameter fit)' if (consistent and near_meas) else 'FALSIFIED ❌ — the two observables imply different spins (the agreement was a single tuned number)'}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "falsify_moveB.json").write_text(json.dumps(
        {"chi_measured": chi_meas, "chi_from_Q": chi_from_Q, "chi_from_MwR": chi_from_MwR,
         "spread": spread, "consistent": bool(consistent and near_meas)}, indent=1, default=float))
    print("  wrote results/falsify_moveB.json")


if __name__ == "__main__":
    main()
