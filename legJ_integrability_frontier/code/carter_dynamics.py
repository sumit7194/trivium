#!/usr/bin/env python3
"""Leg J — Carter-constant dynamics: does C₀ break, and does it DIFFUSE or stay BOUNDED? (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python carter_dynamics.py

Two robust, calibrated measures of Kerr's exact Carter constant C₀ = K₀_{ab}u^a u^b along orbits of the
bumpy metric — neither needs the finicky controlled-eccentricity orbits the dimension scan demanded:

  • DRIFT  = (max−min)/|mean| over the orbit — HOW MUCH the canonical invariant is violated.
  • SATURATION ratio = spread(full) / spread(first quarter) — does the violation stay in a fixed band
    (≈1, a deformed torus → near-integrable, horn i) or keep GROWING (≫1, diffusion → chaos, horn ii)?

Gate G1 (Kerr ε=0): C₀ is exactly conserved → drift ≈ 0 (machine precision). Then the bumpy curve.
No outcome assumed.
"""
import json
import sys
from pathlib import Path

import numpy as np

RES = Path(__file__).resolve().parent.parent / "results"


def measures(series):
    s = np.asarray(series, float)
    mean = s.mean()
    drift = (s.max() - s.min()) / (abs(mean) + 1e-12)
    q = max(2, len(s) // 4)
    spread_q = s[:q].max() - s[:q].min()
    sat = (s.max() - s.min()) / (spread_q + 1e-30)        # ≈1 bounded/saturated, ≫1 still growing
    return drift, sat


def main():
    print("LEG J — Carter-constant dynamics (drift = breaking; saturation = bounded vs diffusing)\n")
    files = sorted(RES.glob("orbits_eps*.json"), key=lambda f: float(f.stem.split("eps")[1]))
    summary, kerr_drift = [], None
    for f in files:
        D = json.loads(f.read_text())
        eps = D["eps"]
        drifts, sats = [], []
        for o in D["orbits"]:
            dr, sa = measures(o["C0_series"])
            drifts.append(dr)
            sats.append(sa)
        drifts, sats = np.array(drifts), np.array(sats)
        med_dr, med_sa = float(np.median(drifts)), float(np.median(sats))
        frac_diff = float(np.mean(sats > 3.0))            # >3×: C₀ kept growing → diffusion
        if eps == 0.0:
            kerr_drift = med_dr
        summary.append({"eps": eps, "n": len(drifts), "drift_median": med_dr,
                        "sat_median": med_sa, "frac_diffusing": frac_diff})
        print(f"  ε={eps:.2f}: n={len(drifts):2d}  Carter drift median={med_dr:.2e}  "
              f"saturation median={med_sa:.2f}  frac diffusing(>3×)={frac_diff:.2f}")

    gate = kerr_drift is not None and kerr_drift < 1e-6
    print(f"\n  G1 gate (Kerr ε=0 → C₀ conserved, drift≈0): {'PASS ✅' if gate else 'FAIL ❌'} "
          f"(Kerr drift = {kerr_drift:.1e})")
    if gate:
        b = [s for s in summary if s["eps"] > 0]
        sat_lo, sat_hi = min(s["sat_median"] for s in b), max(s["sat_median"] for s in b)
        fdmax = max(s["frac_diffusing"] for s in b)
        print(f"  G2 result: canonical Carter drift grows {summary[0]['drift_median']:.1e} → "
              f"{summary[-1]['drift_median']:.1e}; saturation stays in [{sat_lo:.1f},{sat_hi:.1f}], "
              f"max diffusing fraction = {fdmax:.2f}.")
        print("  → bounded saturation (≈1–few) ⇒ C₀ is a deformed-but-bounded invariant (tori survive, "
              "near-integrable); growing saturation / high diffusing fraction ⇒ chaos. Resolution-limited: "
              "a bounded null over finite time is an upper bound on chaos, not a proof of integrability.")
    (RES / "carter_dynamics.json").write_text(json.dumps(
        {"gate_pass": bool(gate), "kerr_drift": kerr_drift, "by_eps": summary}, indent=1))
    print("\n  wrote results/carter_dynamics.json")


if __name__ == "__main__":
    main()
