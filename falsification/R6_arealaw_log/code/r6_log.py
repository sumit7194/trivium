#!/usr/bin/env python3
"""R6 — is the subleading log coefficient of the 3D area law regulator-independent? (reuses M2).

    python3 r6_log.py

Gate frozen in ../PREREGISTRATION.md. M2 killed κ (scheme-dependent) with the exponent universal. R6 fits
S(n)=a·n²+b·log n+c on the same three regulators and asks whether b is universal, scheme-dependent, or
below our precision floor (UNDECIDED — the pre-registered most-likely outcome; the log term is ~1e-4 of the
leading area term).
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

M2DIR = Path(__file__).resolve().parents[2] / "M2_arealaw" / "code"
sys.path.insert(0, str(M2DIR))
import m2_arealaw as M2

OUT = Path(__file__).resolve().parent.parent / "results"
N, L0 = 200, 500
NS = [8, 12, 16, 20, 24, 28, 32, 36, 40]


def S_of(Kfun):
    return np.array(M2.extract_kappa(Kfun, N, NS, L0)["S_ext"])


def fit_log(ns, S):
    n = np.array(ns, float)
    A = np.vstack([n ** 2, np.log(n), np.ones_like(n)]).T
    coef, res, *_ = np.linalg.lstsq(A, S, rcond=None)
    resid = float(np.sqrt(np.mean((A @ coef - S) ** 2)))
    return dict(a=float(coef[0]), b=float(coef[1]), c=float(coef[2]), rms=resid)


def fit_nolog(ns, S):
    n = np.array(ns, float)
    A = np.vstack([n ** 2, np.ones_like(n)]).T
    coef, *_ = np.linalg.lstsq(A, S, rcond=None)
    return float(np.sqrt(np.mean((A @ coef - S) ** 2)))


def jackknife_b(ns, S):
    bs = []
    for i in range(len(ns)):
        keep = [j for j in range(len(ns)) if j != i]
        bs.append(fit_log([ns[j] for j in keep], S[keep])["b"])
    return float(np.mean(bs)), float(np.std(bs))


def main():
    t0 = time.time()
    print("R6 — subleading log coefficient of the 3D area law (gate frozen in PREREGISTRATION.md)")
    print(f"  reusing M2's V2-calibrated pipeline; N={N}, L0={L0}, radii n={NS}\n")

    regs = [("R1 bare NN", M2.K_bare), ("R2 improved", M2.K_impr), ("R3 higher-deriv", M2.K_hd)]
    rows = {}
    print(f"  {'regulator':18s} | {'κ (a)':>8} | {'b (log)':>10} | {'b jackknife':>18} | {'log resolvable?':>16}")
    for name, Kf in regs:
        S = S_of(Kf)
        f = fit_log(NS, S)
        bj_mean, bj_err = jackknife_b(NS, S)
        rms_no = fit_nolog(NS, S)
        improve = rms_no / f["rms"]                      # how much the log term reduces the residual
        resolvable = improve > 3 and abs(f["b"]) > 3 * bj_err
        rows[name] = dict(kappa=f["a"], b=f["b"], b_jk=bj_mean, b_err=bj_err,
                          rms_log=f["rms"], rms_nolog=rms_no, improve=improve, resolvable=bool(resolvable))
        print(f"  {name:18s} | {f['a']:8.4f} | {f['b']:10.4f} | {bj_mean:8.3f} ± {bj_err:7.3f} | "
              f"{'yes' if resolvable else 'NO (× %.1f)' % improve:>16}")

    Sctrl = S_of(M2.K_mid)
    fctrl = fit_log(NS, Sctrl)
    print(f"  {'control midpoint':18s} | {fctrl['a']:8.4f} | {fctrl['b']:10.4f} |  (coord change, not a regulator)")

    bs = np.array([rows[n]["b"] for n, _ in regs])
    errs = np.array([rows[n]["b_err"] for n, _ in regs])
    across = float(np.std(bs))
    within = float(np.mean(errs))
    any_resolvable = any(rows[n]["resolvable"] for n, _ in regs)

    print(f"\n  across-regulator spread of b: {across:.3f}   vs mean within-regulator jackknife error: {within:.3f}")
    if not any_resolvable:
        verdict = "UNDECIDED(precision)"
        print(f"  the log term is NOT robustly resolvable (adds little vs a·n²+c; |b| not ≫ its jackknife error).")
        print(f"  →  {verdict} — the instrument that resolves κ's scheme-dependence does NOT reach the")
        print(f"     subleading anomaly term. An honest floor, pre-registered as the likely outcome.")
    elif across <= within:
        verdict = "SURVIVES (b regulator-independent)"
        print(f"  →  {verdict}: b agrees across regulators within jackknife error while κ does not — universal.")
    else:
        verdict = "KILLED (b regulator-dependent)"
        print(f"  →  {verdict}: b differs across regulators like κ.")

    print(f"\n  R6c (framing): completes the 'what is universal in the area law' story — exponent ≈2 (M2:")
    print(f"  universal), κ (M2: scheme-dependent, 51%), log coefficient ({verdict.split()[0].lower()}).")
    print(f"  Lattice free-scalar sphere EE; not a black hole's S=A/4. No theoretical b asserted from memory.")

    OUT.mkdir(exist_ok=True)
    (OUT / "r6_log.json").write_text(json.dumps({
        "N": N, "L0": L0, "ns": NS, "regulators": rows, "control_b": fctrl["b"],
        "across_spread_b": across, "within_error_b": within, "any_resolvable": bool(any_resolvable),
        "verdict": verdict,
        "summary": (f"Subleading log coefficient of the 3D area law across three UV regulators: "
                    f"b = {[round(rows[n]['b'],3) for n,_ in regs]}, jackknife errors "
                    f"{[round(rows[n]['b_err'],3) for n,_ in regs]}. Verdict: {verdict}. Reuses M2's "
                    f"V2-calibrated pipeline; lattice free scalar, not a black hole."),
    }, indent=1))
    print(f"\n  wrote results/r6_log.json   ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
