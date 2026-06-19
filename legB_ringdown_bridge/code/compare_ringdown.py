#!/usr/bin/env python3
"""Move B — the comparison: ansatz's eikonal Kerr QNM vs deepstrain's measured GW250114 220.

Run with the ansatz venv (pure stdlib):
    /Users/sumit/Github/conjecture_machine/.venv/bin/python compare_ringdown.py

Reads deepstrain's measured ringdown READ-ONLY and ansatz's eikonal_kerr_qnm.json, and
assembles the M-independent quality factor and the dimensionless real frequency comparisons
with the frozen-prediction verdicts (PREREGISTRATION §2–4)."""
import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent.parent / "results"
BH = Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results")
M_SUN_SEC = 4.925490947e-6        # G·M_sun/c³ in seconds


def nearest(rows, chi):
    return min(rows, key=lambda r: abs(r["a"] - chi))


def main():
    nh = json.loads((BH / "06_no_hair_GW250114.json").read_text())
    sbi = json.loads((BH / "08_sbi_GW250114.json").read_text())
    rec = json.loads((BH / "10_recalibration.json").read_text())
    eik = json.loads((RESULTS / "eikonal_kerr_qnm.json").read_text())["rows"]

    f220, tau220 = nh["tone220"]["f"], nh["tone220"]["tau_ms"] * 1e-3
    M_sbi, chi_sbi = sbi["posterior"]["mass"][0], sbi["posterior"]["chi"][0]
    M_220, chi_220 = nh["tone220"]["mass"], nh["tone220"]["chi"]
    delta = rec["gw250114_delta"]

    # measured, M-independent
    Q_meas = math.pi * f220 * tau220
    # measured dimensionless real frequency (uses M); two self-consistent choices
    MwR_sbi = 2 * math.pi * f220 * (M_sbi * M_SUN_SEC)
    MwR_220 = 2 * math.pi * f220 * (M_220 * M_SUN_SEC)

    # ansatz eikonal at the measured spins
    e_sbi = nearest(eik, chi_sbi)
    e_220 = nearest(eik, chi_220)
    e_schw = nearest(eik, 0.0)

    def pct(a, b):
        return 100 * abs(a - b) / abs(b)

    print("MOVE B — eikonal Kerr QNM (ansatz, exact metric)  vs  measured GW250114 220 (deepstrain)\n")
    print(f"  measured 220:  f={f220:.2f} Hz  τ={tau220*1e3:.3f} ms   "
          f"remnant SBI (M={M_sbi:.1f} M⊙, χ={chi_sbi:.3f})   220-self-consistent (M={M_220:.1f}, χ={chi_220:.3f})")
    print(f"  measured no-hair δ = {delta[0]:.3f} [{delta[1]:.3f}, {delta[2]:.3f}]  (Kerr inside 90%)\n")

    print("  QUALITY FACTOR Q₂₂₀ (M-independent: Q = π f τ):")
    print(f"    measured                : {Q_meas:.3f}")
    print(f"    ansatz eikonal χ={chi_sbi:.3f} : {e_sbi['Q']:.3f}   ({pct(e_sbi['Q'], Q_meas):.1f}% from measured)")
    print(f"    ansatz eikonal χ={chi_220:.3f} : {e_220['Q']:.3f}   ({pct(e_220['Q'], Q_meas):.1f}%)")
    print(f"    Schwarzschild  χ=0      : {e_schw['Q']:.3f}   ({pct(e_schw['Q'], Q_meas):.1f}%  ← spin essential)")
    P1 = pct(e_sbi["Q"], Q_meas) < 25

    print("\n  DIMENSIONLESS REAL FREQUENCY Mω_R₂₂₀:")
    print(f"    measured (SBI M={M_sbi:.1f}) : {MwR_sbi:.4f}")
    print(f"    ansatz eikonal χ={chi_sbi:.3f} : {e_sbi['MwR']:.4f}   ({pct(e_sbi['MwR'], MwR_sbi):.1f}% from SBI-measured)")
    print(f"    measured (220 M={M_220:.1f}) : {MwR_220:.4f}")
    print(f"    ansatz eikonal χ={chi_220:.3f} : {e_220['MwR']:.4f}   ({pct(e_220['MwR'], MwR_220):.1f}% from 220-measured)")
    print(f"    Schwarzschild  χ=0      : {e_schw['MwR']:.4f}   ({pct(e_schw['MwR'], MwR_sbi):.1f}%  ← spin essential)")
    P2 = pct(e_sbi["MwR"], MwR_sbi) < 15

    P3 = pct(e_schw["Q"], Q_meas) > 25 and P1               # Schwarzschild far, Kerr close
    P4 = abs(e_sbi["unification"] - 1) < 1e-4               # Ω_c·b_c = 1 exact

    print("\n  VERDICTS (frozen bands):")
    print(f"    P1 (Q within 25%):        {P1}")
    print(f"    P2 (Mω_R within 15%):     {P2}")
    print(f"    P3 (spin essential):      {P3}")
    print(f"    P4 (Ω_c·b_c = 1 exact):   {P4}  (unification = {e_sbi['unification']:.6f})")
    ok = P1 and P2 and P3 and P4
    print(f"\n  NUMERIC RINGDOWN BRIDGE: {'ESTABLISHED ✅' if ok else 'incomplete ❌'}")

    out = {"measured": {"f220_Hz": f220, "tau220_ms": tau220 * 1e3, "Q220": Q_meas,
                        "MwR_sbi": MwR_sbi, "MwR_220": MwR_220, "delta": delta,
                        "M_sbi": M_sbi, "chi_sbi": chi_sbi, "M_220": M_220, "chi_220": chi_220},
           "ansatz_eikonal": {"chi_sbi": e_sbi, "chi_220": e_220, "schwarzschild": e_schw},
           "verdicts": {"P1": P1, "P2": P2, "P3": P3, "P4": P4, "bridge_established": ok}}
    (RESULTS / "compare_ringdown.json").write_text(json.dumps(out, indent=1, default=float))
    print("  wrote results/compare_ringdown.json")


if __name__ == "__main__":
    main()
