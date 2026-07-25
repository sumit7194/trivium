#!/usr/bin/env python3
"""R8 — is kappa's scheme-dependence a property of the QUANTITY or of the REGIME? (applies L9 to ourselves).

    python3 r8_regime.py

Gates frozen in ../PREREGISTRATION.md. M2 killed kappa as scheme-dependent (0.30/0.41/0.51, a 51% spread)
and A2 filed it as a species-3 (definitional) wall. That was ONE POINT: M2's operators are massless.
quantum's L9 -- scan the regime, the interesting answer is usually a boundary -- says check.

Mass enters the Srednicki radial operator as K -> K + m^2 I (frozen: mass first, then regulator). The
regime knob is m*n = sphere radius / correlation length, the analogue of quantum's Lambda. Everything else
is M2 verbatim, so the m=0 row IS M2.
"""
import json
import sys
from pathlib import Path

import numpy as np

M2DIR = Path(__file__).resolve().parents[2] / "M2_arealaw" / "code"
sys.path.insert(0, str(M2DIR))
import m2_arealaw as M2

OUT = Path(__file__).resolve().parent.parent / "results"
N, L0 = 200, 500
NS = [15, 20, 25, 30, 35, 40]
MASSES = [0.0, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
GAMMA = 0.1
KAPPA_FLOOR = 0.01            # R8c: below this, kappa has collapsed and the spread is noise, not agreement


def make_regulators(m):
    """Mass first, then regulator (frozen ordering)."""
    m2 = m * m

    def K_bare_m(NN, l):
        return M2.K_bare(NN, l) + m2 * np.eye(NN)

    def K_impr_m(NN, l):
        return M2.K_impr(NN, l) + m2 * np.eye(NN)

    def K_hd_m(NN, l):
        K = K_bare_m(NN, l)
        return K + GAMMA * (K @ K)

    return [("R1 bare", K_bare_m), ("R2 improved", K_impr_m), ("R3 higher-deriv", K_hd_m)]


def main():
    print("R8 — is kappa's scheme-dependence a property of the QUANTITY or the REGIME?")
    print(f"  applying L9 (quantum's lesson) to our own banked M2 result")
    print(f"  M2 verbatim except K -> K + m^2 I;  N={N}, L0={L0}, ns={NS}\n")
    rep = {"N": N, "L0": L0, "ns": NS, "masses": MASSES, "kappa_floor": KAPPA_FLOOR}

    rows = []
    print(f"  {'m':>6} | {'m*n range':>12} | {'kappa bare':>10} {'impr':>8} {'hd':>8} | {'spread Δ':>9} | countable?")
    for m in MASSES:
        ks = []
        for _, Kf in make_regulators(m):
            ks.append(M2.extract_kappa(Kf, N, NS, L0)["kappa"])
        ks = np.array(ks)
        mean = float(np.mean(ks))
        spread = float((ks.max() - ks.min()) / mean) if mean != 0 else float("nan")
        countable = bool(ks.min() > KAPPA_FLOOR)
        rows.append({"m": m, "mn_lo": m * NS[0], "mn_hi": m * NS[-1],
                     "kappas": ks.tolist(), "mean": mean, "spread": spread,
                     "countable": countable})
        print(f"  {m:6.3f} | {m*NS[0]:5.2f}–{m*NS[-1]:5.2f} | {ks[0]:10.4f} {ks[1]:8.4f} {ks[2]:8.4f} | "
              f"{spread*100:8.1f}% | {'yes' if countable else 'NO (kappa collapsed)'}")
    rep["scan"] = rows

    # ---- R8a regression: m=0 must reproduce M2
    z = rows[0]
    m2_ref = [0.2998, 0.4113, 0.5104]                 # M2/R6's measured values
    dev = max(abs(a - b) / b for a, b in zip(z["kappas"], m2_ref))
    r8a = dev < 0.02
    print(f"\n  R8a — regression at m=0 vs M2's 0.2998/0.4113/0.5104: max deviation {dev*100:.2f}%")
    print(f"     →  R8a {'PASS ✅' if r8a else 'FAIL ❌ — massive extension untrustworthy, later gates VOID'}")
    rep["R8a"] = {"pass": bool(r8a), "max_dev": dev, "m2_reference": m2_ref}

    if not r8a:
        rep["verdict"] = "VOID — R8a regression failed"
        OUT.mkdir(exist_ok=True)
        (OUT / "r8_regime.json").write_text(json.dumps(rep, indent=1))
        print("\n  VERDICT: VOID")
        return

    # ---- R8b the scan
    d0 = z["spread"]
    countable = [r for r in rows if r["countable"]]
    uncount = [r for r in rows if not r["countable"]]
    dmin = min(r["spread"] for r in countable)
    dmin_at = [r["m"] for r in countable if r["spread"] == dmin][0]
    print(f"\n  R8b — the scan:  Δ(0) = {d0*100:.1f}%   minimum countable Δ = {dmin*100:.1f}% at m={dmin_at}")
    print(f"     thresholds (frozen): SURVIVES if Δ ≥ ½Δ(0) = {d0*50:.1f}% everywhere; "
          f"KILLED if Δ < ⅕Δ(0) = {d0*20:.1f}% anywhere")
    if dmin < 0.2 * d0:
        verdict = ("KILLED — κ's scheme-dependence is REGIME-BOUNDED: the regulators agree at "
                   f"m={dmin_at} (Δ={dmin*100:.1f}%). M2/A2's species-3 label needs a qualifier, and "
                   "quantum's single observation becomes a pattern.")
    elif dmin >= 0.5 * d0:
        verdict = ("SURVIVES — no switch-off: κ's scheme-dependence holds at every countable regime point. "
                   "M2 strengthened; the species-3 label on κ is unconditional.")
    else:
        verdict = (f"PARTIAL/UNDECIDED — minimum Δ={dmin*100:.1f}% lands between ⅕ and ½ of Δ(0); "
                   "a weakening, not a switch-off.")
    print(f"     →  {verdict}")
    rep["R8b"] = {"spread_at_0": d0, "min_spread": dmin, "min_at_m": dmin_at}

    # ---- R8c the collapse trap
    print(f"\n  R8c — collapse trap (a shrinking spread on near-zero κ is an ARTIFACT, not agreement):")
    if uncount:
        for r in uncount:
            print(f"     m={r['m']}: min κ = {min(r['kappas']):.4f} < {KAPPA_FLOOR} → NOT MEASURABLE "
                  f"(reported as such, never as agreement); its Δ={r['spread']*100:.1f}% is excluded")
    else:
        print(f"     no point collapsed — min κ across the whole scan = "
              f"{min(min(r['kappas']) for r in rows):.4f} > {KAPPA_FLOOR} ✅")
    rep["R8c"] = {"uncountable_masses": [r["m"] for r in uncount],
                  "min_kappa_overall": float(min(min(r["kappas"]) for r in rows))}

    print(f"\n  VERDICT: {verdict}")
    print(f"\n  Scope: zero novelty — massive-scalar lattice EE is textbook. What R8 decides is whether OUR")
    print(f"  banked species-3 label on κ survives a regime scan. κ only; R6's log b is out of scope (it was")
    print(f"  not robustly resolvable for one regulator even at m=0).")

    rep["verdict"] = verdict
    OUT.mkdir(exist_ok=True)
    (OUT / "r8_regime.json").write_text(json.dumps(rep, indent=1))
    print(f"\n  wrote results/r8_regime.json")


if __name__ == "__main__":
    main()
