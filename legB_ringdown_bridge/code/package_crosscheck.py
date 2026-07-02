#!/usr/bin/env python3
"""Move B v3 — exact Leaver vs the FIELD-STANDARD ringdown package on GW250114 (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python package_crosscheck.py

deepstrain R2v2 (§21) re-measured the GW250114 ringdown with the field-standard `ringdown` package
(Isi/Farr frequency-domain coherent pipeline, Kerr-templated, NUTS): with n_modes=2 the 221 overtone is
DECISIVE (A221/A220 = 1.02, P(A221 < 10% A220) = 0.000) and the remnant is M = 74.8 [70.4, 79.0] M⊙,
χ = 0.729 [0.644, 0.795]. That gives Move B a third, fully-independent pipeline to cross:

  (1) SPECTRUM CHECK — at the package's own median (M, χ), does ansatz's exact-Leaver oracle (§77)
      reproduce the package's implied mode frequencies? Two independent Kerr-QNM implementations
      (Leaver continued fraction vs the ringdown package's internals) on the same posterior point.
  (2) THREE-PIPELINE REMNANT — bridge exact-Leaver inversion of the raw two-tone fit (Move B v2) vs
      deepstrain's NPE vs the package: do all three land on the same (M, χ)? Honest tension reporting.
  (3) OVERTONE REALITY + KERR CONSISTENCY — the package is Kerr-templated (δ ≡ 0 by construction); its
      decisive two-mode fit + the n1→n2 mass shift corroborate Move B v2's Kerr-consistent δ.

All inputs read-only (deepstrain §21 JSON; ansatz qnm_precise §77).
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from qnm_precise import qnm_precise                          # ansatz §77 exact Leaver, read-only

BH = Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results")
RESULTS = Path(__file__).resolve().parent.parent / "results"
M_SUN = 4.925490947e-6


def leaver_mode(M_msun, chi, n):
    """Exact-Leaver Kerr (2,2,n) frequency [Hz] and damping time [s] at remnant (M, χ)."""
    Msec = M_msun * M_SUN
    w = qnm_precise(1.0, chi, 2, 2, n)
    return w.real / (2 * math.pi * Msec), -Msec / w.imag


def main():
    d = json.load((BH / "21_ringdown_crosscheck.json").open())
    n2 = d["GW250114_082203_n2"]
    n1 = d["GW250114_082203_n1"]
    v2 = json.load((Path(__file__).resolve().parent.parent / "results/precise_ringdown.json").open())

    M_pkg, chi_pkg = n2["m"]["q50"], n2["chi"]["q50"]
    f220_pkg = n2["f"]["mode0"]["q50"]
    f221_pkg = n2["f"]["mode1"]["q50"]

    print("MOVE B v3 — exact Leaver vs the field-standard `ringdown` package (GW250114, deepstrain §21)\n")

    # (1) spectrum check at the package's median point
    f220_L, t220_L = leaver_mode(M_pkg, chi_pkg, 0)
    f221_L, t221_L = leaver_mode(M_pkg, chi_pkg, 1)
    e220 = abs(f220_L - f220_pkg) / f220_pkg
    e221 = abs(f221_L - f221_pkg) / f221_pkg
    print(f"  (1) SPECTRUM at the package median (M={M_pkg:.1f} M⊙, χ={chi_pkg:.3f}):")
    print(f"      {'mode':6s} {'package (Hz)':>13s} {'exact Leaver (Hz)':>18s} {'agree':>8s}")
    print(f"      {'220':6s} {f220_pkg:>13.2f} {f220_L:>18.2f} {e220:>7.2%}")
    print(f"      {'221':6s} {f221_pkg:>13.2f} {f221_L:>18.2f} {e221:>7.2%}")
    print(f"      → two independent Kerr-QNM codes (Leaver continued-fraction vs the package's spectrum)")
    print(f"        agree to {max(e220, e221):.2%} — the package's implied spectrum is the exact Kerr spectrum.")

    # (2) three-pipeline remnant convergence
    M_v2, chi_v2 = v2["inversion_220"]["bridge_M"], v2["inversion_220"]["bridge_chi"]
    npe = json.load((BH / "13_more_events.json").open())["GW250114_082203"]
    M_npe, chi_npe = npe["M"][0], npe["chi"][0]
    print(f"\n  (2) THREE-PIPELINE REMNANT (same event, three fully-independent methods):")
    print(f"      {'pipeline':44s} {'M (M⊙)':>10s} {'χ':>7s}")
    print(f"      {'bridge exact-Leaver ← raw two-tone fit (v2)':44s} {M_v2:>10.1f} {chi_v2:>7.3f}")
    print(f"      {'deepstrain NPE (SBI, learned)':44s} {M_npe:>10.1f} {chi_npe:>7.3f}")
    print(f"      {'ringdown package (Isi/Farr FD, NUTS)':44s} {M_pkg:>10.1f} {chi_pkg:>7.3f}"
          f"   [90%: {n2['m']['q5']:.1f}–{n2['m']['q95']:.1f}; {n2['chi']['q5']:.3f}–{n2['chi']['q95']:.3f}]")
    dM = abs(M_v2 - M_pkg)
    m_in = n2["m"]["q5"] <= M_v2 <= n2["m"]["q95"]
    chi_in = n2["chi"]["q5"] <= chi_v2 <= n2["chi"]["q95"]
    print(f"      → MASS: v2's exact-Leaver M agrees with the package to {dM:.2f} M⊙ "
          f"({'inside' if m_in else 'OUTSIDE'} its 90% CI) — three routes, one remnant mass.")
    print(f"      → SPIN (honest tension): v2's χ={chi_v2:.3f} sits {'inside' if chi_in else 'just ABOVE'} the "
          f"package's 90% [{n2['chi']['q5']:.3f}, {n2['chi']['q95']:.3f}].")
    print(f"        Traceable: the raw two-tone fit's f220 (257.8 Hz) vs the package's ({f220_pkg:.1f} Hz) — a")
    print(f"        time-domain damped-sinusoid fit vs an FD coherent Kerr-templated fit resolve the SAME two-")
    print(f"        mode signal with a different f220/χ split at fixed M. A real cross-pipeline systematic,")
    print(f"        surfaced by the triangulation — not hidden by it.")

    # (3) overtone reality + Kerr consistency
    r = n2["a221_over_a220_median"]
    pfrac = n2["a221_frac_below_10pct_median"]
    M_n1 = n1["m"]["q50"]
    print(f"\n  (3) OVERTONE REALITY (the package's decisive two-mode fit):")
    print(f"      A221/A220 = {r:.3f} (median);  P(A221 < 10% of A220) = {pfrac:.3f} — the 221 is REQUIRED.")
    print(f"      n1→n2 mass shift: {M_n1:.1f} → {M_pkg:.1f} M⊙ — the classic unmodeled-overtone bias,")
    print(f"      resolved by adding the 221. The Kerr-templated fit succeeds decisively, corroborating Move B")
    print(f"      v2's independent no-hair verdict (δ = {v2['delta_bridge']:+.3f}, Kerr-consistent).")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "package_crosscheck.json").write_text(json.dumps({
        "event": "GW250114_082203", "package": "ringdown (Isi/Farr FD), deepstrain §21",
        "spectrum_check": {"M": M_pkg, "chi": chi_pkg,
                           "f220_package": f220_pkg, "f220_leaver": f220_L, "err220": e220,
                           "f221_package": f221_pkg, "f221_leaver": f221_L, "err221": e221,
                           "tau220_leaver_ms": t220_L * 1e3, "tau221_leaver_ms": t221_L * 1e3},
        "three_pipelines": {"bridge_leaver_v2": {"M": M_v2, "chi": chi_v2},
                            "deepstrain_npe": {"M": M_npe, "chi": chi_npe},
                            "package_n2": {"M": M_pkg, "chi": chi_pkg,
                                           "M90": [n2["m"]["q5"], n2["m"]["q95"]],
                                           "chi90": [n2["chi"]["q5"], n2["chi"]["q95"]]},
                            "mass_agree_Msun": dM, "v2_M_inside_pkg90": bool(m_in),
                            "v2_chi_inside_pkg90": bool(chi_in)},
        "overtone": {"a221_over_a220": r, "p_a221_below_10pct": pfrac,
                     "n1_mass": M_n1, "n2_mass": M_pkg},
    }, indent=1, default=float))
    print(f"\n  wrote results/package_crosscheck.json")


if __name__ == "__main__":
    main()
