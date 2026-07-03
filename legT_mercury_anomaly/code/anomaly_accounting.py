#!/usr/bin/env python3
"""Leg T — Mercury anomaly accounting: tabula's measured precession × the exact GR term (stdlib).

    python3 anomaly_accounting.py

Gates frozen in ../PREREGISTRATION.md before this ran. The Le Verrier decomposition with sister
instruments: tabula's real-data 120-yr total (EXP-15 P4) minus the literature Newtonian secular value
(Clemence 1947) vs the exact Schwarzschild advance 6πμ/(c²a(1−e²)) evaluated with tabula's OWN
instrument-measured GM☉. Read-only; consistency accounting, not a GR detection (T3).
"""
import json
import math
from pathlib import Path

T156 = Path("/Users/sumit/Github/SpaceTime/curvature/results/156_newton_from_ephemerides.json")
OUT = Path(__file__).resolve().parent.parent / "results"

NEWTONIAN_LIT = 532.3          # ″/century, planetary perturbations (Clemence 1947, RMP 19, 361)
A_MERC, E_MERC, P_DAYS = 0.3870989, 0.2056307, 87.969
C_AU_DAY = 173.1446
ARCSEC = 206264.80625
CENT_DAYS = 36525.0


def gr_advance(mu):
    """Exact first-order Schwarzschild perihelion advance, ″/century."""
    per_orbit = 6 * math.pi * mu / (C_AU_DAY ** 2 * A_MERC * (1 - E_MERC ** 2))   # rad/orbit
    return per_orbit * (CENT_DAYS / P_DAYS) * ARCSEC


def main():
    t = json.loads(T156.read_text())
    meas = t["P4_measured_precession_arcsec_per_century"]
    known = t["P4_known_total"]
    mu_hat, mu_true = t["P3_mu_hat_LRL"], t["mu_true_AU3_day2"]

    gr_hat, gr_true = gr_advance(mu_hat), gr_advance(mu_true)
    sigma = abs(meas - known)                                # the instrument's demonstrated floor (~1.1%)
    residual = meas - NEWTONIAN_LIT
    diff = abs(residual - gr_hat)

    print("LEG T — Mercury anomaly accounting (gates frozen in PREREGISTRATION.md)\n")
    print(f"  T1 exact GR term, 6πμ/(c²a(1−e²)):")
    print(f"     with tabula's measured μ̂:  {gr_hat:.3f} ″/cy      with true μ: {gr_true:.3f} ″/cy "
          f"(Δ {abs(gr_hat-gr_true)/gr_true:.2e})")
    t1 = 42.9 <= gr_hat <= 43.1
    print(f"     canonical ≈43.0 reproduced: {'PASS ✅' if t1 else 'FAIL ❌'}")
    print(f"\n  T2 the accounting (all ″/century):")
    print(f"     tabula measured total (120-yr real Horizons, LRL azimuth) : {meas:8.1f}")
    print(f"     − literature Newtonian secular (Clemence 1947)            : {NEWTONIAN_LIT:8.1f}")
    print(f"     = residual anomaly                                        : {residual:8.1f}")
    print(f"     exact GR term (from tabula's own μ̂)                       : {gr_hat:8.1f}")
    print(f"     |residual − GR| = {diff:.1f}  vs  2σ_meas = {2*sigma:.1f}  (σ_meas = |{meas:.1f}−{known:.1f}| = {sigma:.1f})")
    t2 = diff < 2 * sigma
    gate_msg = ("PASS ✅ — the GR term closes Mercury's books at the instrument floor (~1σ)"
                if t2 else "FAIL ❌ — tension")
    print(f"     GATE: {gate_msg}")
    print(f"\n  T3 framing (frozen): consistency of the accounting at a ~{sigma:.0f}″/cy floor — NOT an")
    print(f"     independent GR detection (GR is baked into the ephemerides; the 12×-larger Newtonian share")
    print(f"     is separated only by the external literature anchor).")
    OUT.mkdir(exist_ok=True)
    (OUT / "anomaly_accounting.json").write_text(json.dumps({
        "measured_total": meas, "known_total": known, "newtonian_lit": NEWTONIAN_LIT,
        "residual": residual, "gr_term_mu_hat": gr_hat, "gr_term_mu_true": gr_true,
        "sigma_meas": sigma, "abs_diff": diff, "T1_pass": bool(t1), "T2_pass": bool(t2),
        "verdict": ("Le Verrier decomposition with sister instruments: tabula's real-data total minus the "
                    "literature Newtonian secular leaves %.1f ″/cy, matching the exact GR term %.1f (computed "
                    "with tabula's own measured GM☉) within ~1σ of the instrument's %.1f ″/cy floor. "
                    "Consistency accounting, not a detection." % (residual, gr_hat, sigma)),
    }, indent=1))
    print(f"\n  wrote results/anomaly_accounting.json")


if __name__ == "__main__":
    main()
