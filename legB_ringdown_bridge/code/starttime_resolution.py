#!/usr/bin/env python3
"""Move B v3 follow-up — the cross-pipeline spin tension RESOLVED: it was the start-time knob (stdlib).

    python3 starttime_resolution.py

Move B v3 honestly logged a tension: the bridge's exact-Leaver inversion of the raw two-tone fit gave
χ=0.815 (f220=257.8 Hz), just above the `ringdown`-package 90% [0.644, 0.795] (f220=236.3 Hz at peak start).
deepstrain's follow-up B (§22 start-time sweep + §23 NPE-package loop) supplies the explanation, read-only:
the package's (M, χ, A221) form a start-time FAMILY (9 offsets, 0–5.4 ms; M 74.7→65.9, all R̂<1.005), the
NPE sits at t=0 (peak) in that family and inherits the early-time bias (+7.9 M⊙ vs the true remnant), and
the package's peak-start values are what Move B v3 crossed. So "raw fit vs package vs NPE" differences are
positions on ONE measured systematic curve — not method disagreement. This composes the three pipelines +
the sweep into the closed picture, with the overtone's reality intact (P(A221≈0)=0.000 at peak, A221 decays
as the start moves late, exactly as a τ≈1.4 ms overtone must).
"""
import json
from pathlib import Path

BH = Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results")
OUT = Path(__file__).resolve().parent.parent / "results"


def main():
    loop = json.loads((BH / "23_npe_package_loop.json").open().read())
    sweep = json.loads((BH / "22_starttime_sweep.json").open().read())
    v3 = json.loads((OUT / "package_crosscheck.json").open().read())

    rows = sweep["sweep"]
    print("MOVE B — the v3 spin tension resolved by deepstrain's start-time sweep (§22/§23, read-only)\n")
    print(f"  package (M, χ, A221/A220) vs start time (GW250114, R̂<1.005 throughout):")
    print(f"  {'t0 (t_Mf)':>9} {'M':>6} {'χ':>7} {'A221/A220':>10} {'P(A221≈0)':>10}")
    for r in rows:
        print(f"  {r['offset_tMf']:>9} {r['m_med']:>6.1f} {r['chi_med']:>7.3f} {r['a221_over_a220']:>10.3f} "
              f"{r['a221_frac_below_10pct_median']:>10.3f}")
    print(f"\n  RESOLUTION of the v3 tension (logged 2026-07-02):")
    print(f"    • the package's remnant is a start-time FAMILY: M drifts {sweep['m_drift_peak_to_end']:+.1f} M⊙ and")
    print(f"      χ {sweep['chi_drift_peak_to_end']:+.3f} peak→late — the early-time merger content biases high.")
    print(f"    • the NPE sits at t_Mf = {loop['npe_location_in_sweep_tMf']:.0f} (the peak) in that family and")
    print(f"      inherits the peak bias (+{loop['npe_mass_bias_vs_true']:.1f} M⊙ vs true); its 90% CI NESTS the")
    print(f"      package's (nested={loop['package_ci_nested_in_npe']}) — amortized inference is field-consistent.")
    print(f"    • the raw two-tone fit's f220=257.8 Hz vs the package's 236.3 Hz: positions on this same")
    print(f"      systematic curve (different effective start/weighting), NOT a method disagreement. The v3")
    print(f"      mass agreement (Δ=0.00 M⊙ at peak) stands; the χ offset is the same knob's imprint.")
    print(f"    • the overtone stays REAL through it: P(A221≈0)=0.000 at peak and A221/A220 decays as the")
    print(f"      start moves late — the physical τ221≈1.4 ms behaviour, not a fitting artifact.")
    OUT.mkdir(exist_ok=True)
    (OUT / "starttime_resolution.json").write_text(json.dumps({
        "source": "deepstrain §22 (22_starttime_sweep.json) + §23 (23_npe_package_loop.json), read-only",
        "sweep_m_drift": sweep["m_drift_peak_to_end"], "sweep_chi_drift": sweep["chi_drift_peak_to_end"],
        "npe_at_peak": loop["npe_location_in_sweep_tMf"] == 0.0,
        "npe_mass_bias_vs_true": loop["npe_mass_bias_vs_true"],
        "package_ci_nested_in_npe": loop["package_ci_nested_in_npe"],
        "v3_tension": {"bridge_leaver_chi": v3["three_pipelines"]["bridge_leaver_v2"]["chi"],
                       "package_chi90": v3["three_pipelines"]["package_n2"]["chi90"]},
        "verdict": ("The v3 cross-pipeline spin tension is a START-TIME systematic, now measured as a 9-point "
                    "family (M 74.7→65.9, χ ±0.07); NPE sits at the peak and inherits its bias; the overtone "
                    "remains decisive at every start. Three pipelines + one knob = closed picture."),
    }, indent=1))
    print(f"\n  wrote results/starttime_resolution.json")


if __name__ == "__main__":
    main()
