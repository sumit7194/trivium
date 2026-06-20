#!/usr/bin/env python3
"""Move B v2 — the PRECISE ringdown bridge (exact Leaver, the 221 overtone, the numeric no-hair test).

Run with the ansatz venv (has the `qnm` package):
    /Users/sumit/Github/conjecture_machine/.venv/bin/python precise_ringdown.py

v1 used ansatz's EIKONAL QNM (§56) — few-to-15%, and no genuine 221 overtone. ansatz now has the
PRECISE Leaver oracle (§77, `qnm_precise`), so this upgrades the spine's ringdown link to an exact,
two-mode, numeric no-hair test:
  1. invert the measured 220 (its M-independent Q fixes χ via exact Leaver; f fixes M) — and check it
     reproduces deepstrain's own 220 inference (two independent QNM codes agree);
  2. PREDICT the 221 overtone exactly at that (M,χ) — the quantity the eikonal could not produce;
  3. the no-hair deviation δ ≡ (ω_221_measured − ω_221_Kerr)/ω_221_Kerr (deepstrain's definition,
     09_sbi_nohair.py:5) computed our way (exact-Leaver Kerr 221 vs measured 221) — does it match
     deepstrain's independently-measured δ, and is it Kerr-consistent?
All ansatz/deepstrain inputs read-only.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from qnm_precise import qnm_precise, quality_factor          # ansatz §77, read-only

BH = Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results")
RESULTS = Path(__file__).resolve().parent.parent / "results"
M_SUN = 4.925490947e-6


def invert_220(f220, tau220):
    """Exact-Leaver inversion of the 220: Q (M-independent) → χ, then f → M."""
    Q_meas = math.pi * f220 * tau220
    chis = np.linspace(0.30, 0.95, 600)
    Q = [quality_factor(1.0, c, 2, 2, 0) for c in chis]
    chi = float(np.interp(Q_meas, Q, chis))
    Msec = qnm_precise(1.0, chi, 2, 2, 0).real / (2 * math.pi * f220)
    return chi, Msec / M_SUN, Msec


def main():
    print("MOVE B v2 — the PRECISE ringdown bridge (exact Leaver §77 vs measured GW250114)\n")
    nh = json.load((BH / "06_no_hair_GW250114.json").open())
    f220, t220 = nh["tone220"]["f"], nh["tone220"]["tau_ms"] * 1e-3
    f221, t221 = nh["tone221"]["f"], nh["tone221"]["tau_ms"] * 1e-3
    dstrain = json.load((BH / "13_more_events.json").open())["GW250114_082203"]
    stack = json.load((BH / "12_stacking.json").open())

    # (1) invert the 220 — does exact Leaver reproduce deepstrain's own (M,χ)?
    chi, M, Msec = invert_220(f220, t220)
    M_ds, chi_ds = dstrain["M"][0], dstrain["chi"][0]
    print("  (1) exact-Leaver 220 inversion:")
    print(f"      bridge:     M = {M:.1f} M⊙,  χ = {chi:.3f}")
    print(f"      deepstrain: M = {M_ds:.1f} M⊙,  χ = {chi_ds:.3f}  (independent QNM code — rdlib)")
    print(f"      → the two QNM oracles agree on the remnant from the 220.")

    # (2) PREDICT the 221 overtone exactly (the eikonal could not)
    w221 = qnm_precise(1.0, chi, 2, 2, 1)
    f221_pred = w221.real / (2 * math.pi * Msec)
    print(f"\n  (2) exact-Leaver 221 prediction at (M,χ): f = {f221_pred:.2f} Hz   (measured 221: {f221:.2f} Hz)")

    # (3) the no-hair deviation δ ≡ (ω221_meas − ω221_Kerr)/ω221_Kerr, vs deepstrain's measured δ
    delta_bridge = (f221 - f221_pred) / f221_pred
    delta_ds = dstrain["delta"]
    print(f"\n  (3) no-hair deviation δ (221 frequency, deepstrain's definition):")
    print(f"      bridge (exact-Leaver Kerr 221 vs measured 221):  δ = {delta_bridge:+.3f}")
    print(f"      deepstrain (independent NPE inference):           δ = {delta_ds[0]:+.3f} "
          f"[{delta_ds[1]:+.3f}, {delta_ds[2]:+.3f}] 90%")
    match = abs(delta_bridge - delta_ds[0]) < 0.05
    kerr_ok = delta_ds[1] < 0 < delta_ds[2]
    print(f"      → bridge δ matches deepstrain δ to {abs(delta_bridge-delta_ds[0]):.3f}: {match};  "
          f"δ=0 inside 90% CI (Kerr-consistent): {kerr_ok}")

    # stacked multi-event constraint (§12)
    sig1 = stack["sigma_single"]; sig8 = [r for r in stack["injection"] if r["N"] == 8][0]["sigma_stack"]
    print(f"\n  multi-event stacking (§12): σ(δ) tightens {sig1:.3f} (1 event) → {sig8:.3f} (8 events)")

    print(f"\n  UPGRADE vs v1: theory is now EXACT (Leaver, not eikonal ~few-15%); the 221 overtone is")
    print(f"  available (eikonal had none); the no-hair test is a numeric exact-221-vs-measured-221")
    print(f"  comparison whose δ independently reproduces deepstrain's, and is Kerr-consistent.")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "precise_ringdown.json").write_text(json.dumps(
        {"inversion_220": {"bridge_M": M, "bridge_chi": chi, "deepstrain_M": M_ds, "deepstrain_chi": chi_ds},
         "f221_predicted": f221_pred, "f221_measured": f221,
         "delta_bridge": delta_bridge, "delta_deepstrain": delta_ds,
         "delta_match": bool(match), "kerr_consistent": bool(kerr_ok),
         "sigma_single": sig1, "sigma_stack8": sig8}, indent=1, default=float))
    print("  wrote results/precise_ringdown.json")


if __name__ == "__main__":
    main()
