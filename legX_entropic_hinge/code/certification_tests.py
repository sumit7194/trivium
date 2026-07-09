#!/usr/bin/env python3
"""Leg X — certification tests C1-C3 (quantum's adversarial squeezed-state warning, answered).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python certification_tests.py

Gates frozen in ../PREREGISTRATION.md ADDENDUM (2026-07-10). C1/C2 run the PRODUCTION code path
(entropic_hinge.modular_form, mpmath) on states where the arccoth-ordering trap quantum warned about
would show; C3 is a Fock-basis end-to-end check with no Gaussian formulas anywhere.
"""
import json
import math
from pathlib import Path

from mpmath import mp, mpf, matrix, sqrt, log, exp, cos, sin

import entropic_hinge as EH

OUT = Path(__file__).resolve().parent.parent / "results"


def eps_of(nu):
    return log((nu + mpf("0.5")) / (nu - mpf("0.5")))


def bp_form(XA, PA):
    """The p-quadratic form B = X^{1/2} W diag(eps/nu) W^T X^{1/2} (same construction family as A_q)."""
    Xh = EH.sym_funcs(XA, lambda e: sqrt(e))
    S = Xh * PA * Xh
    from mpmath import eigsy
    E2, W = eigsy(S)
    L = XA.rows
    D = matrix(L, L)
    for i in range(L):
        nu = sqrt(E2[i])
        D[i, i] = eps_of(nu) / nu
    return Xh * (W * D * W.T) * Xh


def rel_err_mat(M, T):
    num = max(abs(M[i, j] - T[i, j]) for i in range(M.rows) for j in range(M.cols))
    den = max(abs(T[i, j]) for i in range(T.rows) for j in range(T.cols))
    return float(num / den)


def main():
    mp.dps = 60
    print("LEG X — certification C1-C3 (gates frozen in PREREGISTRATION.md ADDENDUM)\n")

    # ---- C1: single squeezed thermal mode through the PRODUCTION modular_form
    worst_a = worst_b = 0.0
    for nu_s, r_s in [("0.8", "0.5"), ("0.51", "1.0"), ("2.0", "-0.7"), ("5.0", "0.3"), ("0.6", "2.0")]:
        nu, r = mpf(nu_s), mpf(r_s)
        X = matrix([[nu * exp(2 * r)]])
        P = matrix([[nu * exp(-2 * r)]])
        Aq, _, _ = EH.modular_form(X, P)
        Bp = bp_form(X, P)
        eps = eps_of(nu)
        ea = abs(Aq[0, 0] - eps * exp(-2 * r)) / (eps * exp(-2 * r))
        eb = abs(Bp[0, 0] - eps * exp(2 * r)) / (eps * exp(2 * r))
        worst_a, worst_b = max(worst_a, float(ea)), max(worst_b, float(eb))
    c1 = worst_a < 1e-10 and worst_b < 1e-10
    print(f"  C1 squeezed discriminator (5 (ν,r) points, production code path):")
    print(f"     A_q vs ε·e^(−2r): worst rel err {worst_a:.2e};  B_p vs ε·e^(+2r): worst {worst_b:.2e}")
    print(f"     →  {'PASS ✅ — the ordering trap quantum warned about is absent here' if c1 else 'FAIL ❌ — ORDERING BUG'}")

    # ---- C2: rotated two-mode
    th = mpf("0.6")
    R = matrix([[cos(th), -sin(th)], [sin(th), cos(th)]])
    nus, rs = [mpf("0.8"), mpf("1.7")], [mpf("0.6"), mpf("-0.9")]
    Dx = matrix(2, 2)
    Dp = matrix(2, 2)
    Da = matrix(2, 2)
    for k in range(2):
        Dx[k, k] = nus[k] * exp(2 * rs[k])
        Dp[k, k] = nus[k] * exp(-2 * rs[k])
        Da[k, k] = eps_of(nus[k]) * exp(-2 * rs[k])
    X2m = R * Dx * R.T
    P2m = R * Dp * R.T
    Aq2, _, _ = EH.modular_form(X2m, P2m)
    e2 = rel_err_mat(Aq2, R * Da * R.T)
    c2 = e2 < 1e-10
    print(f"\n  C2 rotated two-mode: A_q vs R·diag(ε_k e^(−2r_k))·Rᵀ: rel err {e2:.2e}  →  "
          f"{'PASS ✅' if c2 else 'FAIL ❌'}")

    # ---- C3: Fock-basis end-to-end (no Gaussian formulas anywhere)
    import numpy as np
    NU, D_DISP, DIM = 0.8, 0.9, 60
    nbar = NU - 0.5
    qf = nbar / (nbar + 1)
    p = (1 - qf) * qf ** np.arange(DIM)
    rho0 = np.diag(p)
    a = np.diag(np.sqrt(np.arange(1, DIM)), 1)
    alpha = D_DISP / math.sqrt(2)                      # q-displacement d -> alpha = d/sqrt(2)
    from numpy.linalg import eigh
    Kd = alpha * (a.T - a)                             # alpha real: D = exp(alpha(a† − a))
    ev, evec = eigh(1j * Kd)                           # iK Hermitian
    Dop = evec @ np.diag(np.exp(-1j * ev)) @ evec.conj().T
    rho1 = Dop @ rho0 @ Dop.conj().T
    ln_rho0 = np.diag(np.log(p))
    S0 = -np.sum(p * np.log(p))
    s_rel_fock = float(np.real(-S0 - np.trace(rho1 @ ln_rho0)))
    eps_f = math.log((NU + 0.5) / (NU - 0.5))
    target = 0.5 * D_DISP ** 2 * eps_f
    e3 = abs(s_rel_fock - target) / target
    c3 = e3 < 1e-6
    print(f"\n  C3 Fock end-to-end (dim {DIM}, ν={NU}, d={D_DISP}): S_rel(matrices) = {s_rel_fock:.10f} "
          f"vs ½d²ε = {target:.10f} ({e3:.2e})  →  {'PASS ✅' if c3 else 'FAIL ❌'}")

    print(f"\n  C4 (record): two independent implementations agree with the formula on disjoint grids —")
    print(f"     bridge 1.5%/1.63% (dispersion-dominated, μ=0.5 σ=2.5) · quantum ≤0.06% clean-geometry")
    print(f"     (m≤0.1, wide packets; 0.2% rows = finite-wedge anatomy) — and the float64 wall measured")
    print(f"     twice: bridge 11.5% recovery ↔ quantum 10–14% clip bands. Cross-gate "
          f"{'CLOSED ✅' if (c1 and c2 and c3) else 'OPEN ❌'}.")

    OUT.mkdir(exist_ok=True)
    (OUT / "certification_tests.json").write_text(json.dumps({
        "C1": {"worst_Aq": worst_a, "worst_Bp": worst_b, "pass": bool(c1)},
        "C2": {"rel_err": e2, "pass": bool(c2)},
        "C3": {"S_rel_fock": s_rel_fock, "target": target, "rel_err": e3, "pass": bool(c3)},
        "C4_record": {"bridge": "1.5% offset / 1.63% slope (mu=0.5, sigma=2.5, dispersion-dominated)",
                      "quantum": "<=0.06% clean-geometry (m<=0.1); 0.2% rows finite-wedge",
                      "float64_wall": "bridge 11.5% recovery vs quantum 10-14% clip bands"},
        "cross_gate_closed": bool(c1 and c2 and c3),
    }, indent=1))
    print(f"\n  wrote results/certification_tests.json")


if __name__ == "__main__":
    main()
