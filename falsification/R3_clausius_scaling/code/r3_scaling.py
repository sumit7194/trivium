#!/usr/bin/env python3
"""R3 — the weak-drive scaling law of the patchwise Clausius violation (measure the exponent).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python r3_scaling.py

Gates R3a/R3b frozen in ../PREREGISTRATION.md. Reuses K3.patch_pieces (mpmath dps=60). Measures the
asymptotic small-r exponent of Σ/δQ, δQ, Σ; tests the postulate p_ratio = 2 (relative-entropy-quadratic)
against the data K3 could not reach (r ≤ 0.05).
"""
import json
import sys
import time
from pathlib import Path

K3DIR = Path(__file__).resolve().parents[2] / "K3_clausius_patch" / "code"
sys.path.insert(0, str(K3DIR))

import numpy as np
from mpmath import mp, mpf
import k3_clausius as K3
import k1_squeezed as K1

OUT = Path(__file__).resolve().parent.parent / "results"
RS = [0.01, 0.015, 0.02, 0.03, 0.05, 0.08, 0.12, 0.2, 0.3]
LS = [8, 16]
SMALL = 0.05                                          # asymptotic-fit window r <= SMALL


def loglog_slope(rs, ys):
    """least-squares slope of log y vs log r."""
    lr, ly = np.log(np.array(rs, float)), np.log(np.array(ys, float))
    A = np.vstack([lr, np.ones_like(lr)]).T
    m, b = np.linalg.lstsq(A, ly, rcond=None)[0]
    return float(m), float(np.exp(b))


def main():
    mp.dps = 60
    t0 = time.time()
    print("R3 — weak-drive scaling of the patchwise Clausius violation (gates in PREREGISTRATION.md)")
    print(f"  reusing K3 chain N={K1.EH.N}, μ={K1.EH.MU}, cut-straddling excitation; dps={mp.dps}\n")
    X, P = K1.build_chain(K1.EH.N, K1.EH.MU)
    v = K1.gauss_profile(X.rows, K1.EH.XC, K1.EH.SIGMA)

    data = {l: [] for l in LS}
    print(f"  {'ℓ':>3} {'r':>6} | {'δQ=Δ⟨K⟩':>13} | {'Σ=S_rel':>13} | {'Σ/δQ':>10}")
    for l in LS:
        for rr in RS:
            dK, dS, sr = K3.patch_pieces(X, P, v, mpf(str(rr)), l)
            frac = float(sr / dK)
            data[l].append({"r": rr, "dQ": float(dK), "Sigma": float(sr), "frac": frac})
            print(f"  {l:>3} {rr:>6} | {float(dK):13.6e} | {float(sr):13.6e} | {frac:10.6e}")
        print()

    # ---- R3a: exponents in the small-r window at ℓ=16
    d16 = data[16]
    sw = [row for row in d16 if row["r"] <= SMALL]
    p_ratio, c_ratio = loglog_slope([r["r"] for r in sw], [r["frac"] for r in sw])
    p_sig, _ = loglog_slope([r["r"] for r in sw], [r["Sigma"] for r in sw])
    p_dQ, _ = loglog_slope([r["r"] for r in sw], [r["dQ"] for r in sw])
    consistency = abs(p_ratio - (p_sig - p_dQ))
    surv = abs(p_ratio - 2.0) <= 0.2
    print(f"  R3a — asymptotic exponents (small-r window r ≤ {SMALL}, ℓ=16, {len(sw)} points):")
    print(f"     p(Σ/δQ) = {p_ratio:.3f}     p(Σ) = {p_sig:.3f}     p(δQ) = {p_dQ:.3f}")
    print(f"     consistency p_ratio ≈ p_Σ − p_δQ: {p_ratio:.3f} vs {p_sig-p_dQ:.3f} (Δ={consistency:.3f})")
    print(f"     postulate p_ratio = 2: |{p_ratio:.3f}−2| = {abs(p_ratio-2):.3f}"
          f"   →  {'SURVIVES ✅' if surv else 'KILLED ❌ — measured exponent ≠ 2'}\n")

    # ---- R3b: coefficient c(ℓ) = frac / r^p_ratio, small-r, across ℓ
    def coeff(rows):
        vals = [row["frac"] / (row["r"] ** p_ratio) for row in rows if row["r"] <= SMALL]
        return float(np.mean(vals)), float(np.std(vals))
    c8, s8 = coeff(data[8]); c16, s16 = coeff(data[16])
    rel = abs(c8 - c16) / ((c8 + c16) / 2)
    r3b = rel < 0.15
    print(f"  R3b — coefficient c(ℓ) = (Σ/δQ)/r^{p_ratio:.2f} (small-r):")
    print(f"     c(ℓ=8) = {c8:.4f} ± {s8:.1e}     c(ℓ=16) = {c16:.4f} ± {s16:.1e}     rel diff {rel:.2%}")
    print(f"     →  {'PASS ✅ — patch-size-independent coefficient' if r3b else 'FAIL ❌ — c is ℓ-dependent'}\n")

    verdict = ("SURVIVES" if surv else "KILLED") + (" (postulate p=2)" if surv else " (postulate p=2)")
    print(f"  VERDICT: postulate '{('' if surv else 'NOT ')}second-order' — measured p(Σ/δQ) = {p_ratio:.2f}.")
    if not surv:
        print(f"  The fractional Clausius violation is ~r^{p_ratio:.1f} (≈ linear), NOT r²: the entanglement-")
        print(f"  entropy change across the cut is {'first' if abs(p_ratio-1)<0.3 else 'fractional'}-order in")
        print(f"  the drive. Decomposition: Σ=S_rel ~ r^{p_sig:.2f}, δQ=Δ⟨K⟩ ~ r^{p_dQ:.2f}.")
    print(f"\n  R3c (framing): the measured law quantifies HOW the localization approximation degrades with")
    print(f"  drive — Clausius holds fractionally to O(r^{p_ratio:.1f}); the near-equilibrium window, measured,")
    print(f"  not proved. Modular/entanglement first law only (not horizon-area Clausius). Toy model.")

    OUT.mkdir(exist_ok=True)
    (OUT / "r3_scaling.json").write_text(json.dumps({
        "N": K1.EH.N, "mu": float(K1.EH.MU), "dps": mp.dps, "rs": RS, "ls": LS, "small_window": SMALL,
        "data": data, "p_ratio": p_ratio, "p_Sigma": p_sig, "p_dQ": p_dQ,
        "consistency": consistency, "R3a_survives_p2": bool(surv),
        "c_l8": c8, "c_l16": c16, "c_reldiff": rel, "R3b_pass": bool(r3b),
        "verdict": (f"Measured asymptotic exponent of the fractional patchwise-Clausius violation: "
                    f"p(Σ/δQ) = {p_ratio:.2f} (Σ=S_rel ~ r^{p_sig:.2f}, δQ ~ r^{p_dQ:.2f}). Postulate p=2 "
                    f"{'SURVIVES' if surv else 'KILLED'}. Coefficient patch-independent to {rel:.1%} "
                    f"(ℓ=8 vs 16). Modular/entanglement first law; toy-model near-equilibrium window."),
    }, indent=1, default=str))
    print(f"\n  wrote results/r3_scaling.json   ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
