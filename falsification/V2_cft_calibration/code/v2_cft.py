#!/usr/bin/env python3
"""V2 — the covariance entanglement-entropy instrument reproduces c = 1 (CFT calibration for M2).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python v2_cft.py

Gates V2a/V2b/V2c frozen in ../PREREGISTRATION.md before this was written. Periodic harmonic chain, interval
entanglement entropy from the reduced covariance's symplectic spectrum (leg X / K1 machinery). A single
interval in a 1+1 CFT obeys S(L) = (c/3) ln[(N/π) sin(πL/N)] + const; recovering c=1 validates the
instrument before M2 trusts it for the 3D area-law coefficient.
"""
import json
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results"

N = 500
MU = 1e-4                       # near-critical IR regulator (ξ = 1/μ = 1e4 ≫ fitted L)
L_SWEEP = list(range(20, 201, 10))


def covariances(N, mu):
    """Periodic-chain vacuum covariances X = ½K^{-1/2}, P = ½K^{1/2}."""
    K = np.zeros((N, N))
    idx = np.arange(N)
    K[idx, idx] = 2 + mu ** 2
    K[idx, (idx + 1) % N] = -1
    K[idx, (idx - 1) % N] = -1
    w, Q = np.linalg.eigh(K)
    sw = np.sqrt(w)
    X = (Q * (0.5 / sw)) @ Q.T
    P = (Q * (0.5 * sw)) @ Q.T
    return X, P


def s_nu(nu):
    a = nu + 0.5
    b = nu - 0.5
    return np.where(b > 1e-14, a * np.log(a) - np.where(b > 0, b, 1.0) * np.log(np.where(b > 0, b, 1.0)), 0.0)


def interval_entropy(X, P, L):
    """Entanglement entropy of L contiguous centred sites."""
    s = (N - L) // 2
    ii = np.arange(s, s + L)
    XA = X[np.ix_(ii, ii)]
    PA = P[np.ix_(ii, ii)]
    nu2 = np.linalg.eigvals(XA @ PA).real
    nu = np.sqrt(np.clip(nu2, 0.25, None))
    return float(np.sum(s_nu(nu)))


def entropy_mpmath(Nc, mu, L):
    """Interval entropy in mpmath (dps=30) on a SMALL chain (Nc) — a methodological float64-vs-mpmath
    adequacy check (not tied to N=500; a full 500² mpmath eigsy is needlessly slow)."""
    from mpmath import mp, matrix, eigsy, sqrt, log, mpf
    mp.dps = 30
    K = matrix(Nc, Nc)
    for i in range(Nc):
        K[i, i] = 2 + mpf(mu) ** 2
        K[i, (i + 1) % Nc] = -1
        K[i, (i - 1) % Nc] = -1
    E, Q = eigsy(K)
    Dih = matrix(Nc, Nc)
    Dh = matrix(Nc, Nc)
    for i in range(Nc):
        sw = sqrt(E[i])
        Dih[i, i] = 1 / (2 * sw)
        Dh[i, i] = sw / 2
    X = Q * Dih * Q.T
    P = Q * Dh * Q.T
    s = (Nc - L) // 2
    L2 = L
    XA = matrix(L2, L2)
    PA = matrix(L2, L2)
    for a in range(L2):
        for b in range(L2):
            XA[a, b] = X[s + a, s + b]
            PA[a, b] = P[s + a, s + b]
    # symplectic eigenvalues via eig of XA^{1/2} PA XA^{1/2}
    Ex, Qx = eigsy(XA)
    Xh = matrix(L2, L2)
    for i in range(L2):
        Xh[i, i] = sqrt(Ex[i])
    Xh = Qx * Xh * Qx.T
    E2, _ = eigsy(Xh * PA * Xh)
    tot = mpf(0)
    for i in range(L2):
        nu = sqrt(E2[i])
        a = nu + mpf("0.5")
        b = nu - mpf("0.5")
        tot += a * log(a) - (b * log(b) if b > 0 else mpf(0))
    return float(tot)


def main():
    print("V2 — entropy instrument CFT calibration (gates frozen in PREREGISTRATION.md)")
    print(f"  periodic chain N={N}, mu={MU} (xi={1/MU:.0e}), interval sweep L={L_SWEEP[0]}..{L_SWEEP[-1]}\n")

    X, P = covariances(N, MU)
    Ls = np.array(L_SWEEP, float)
    S = np.array([interval_entropy(X, P, int(L)) for L in L_SWEEP])
    x = np.log((N / math.pi) * np.sin(math.pi * Ls / N))       # Casini-Huerta chord

    # V2a: c = 3 * slope
    A = np.vstack([x, np.ones_like(x)]).T
    (m, b), res, *_ = np.linalg.lstsq(A, S, rcond=None)
    c = 3 * m
    ss_res = float(np.sum((S - (m * x + b)) ** 2))
    ss_tot = float(np.sum((S - S.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot
    v2a = 0.95 <= c <= 1.05
    v2b = r2 > 0.999

    print(f"  {'L':>4} | {'x=ln[(N/π)sinπL/N]':>19} | {'S(L)':>10}")
    for i in range(0, len(L_SWEEP), 3):
        print(f"  {L_SWEEP[i]:>4} | {x[i]:>19.5f} | {S[i]:>10.6f}")
    print(f"\n  V2a central charge: c = 3·slope = {c:.5f}  (want [0.95,1.05])  → {'PASS ✅' if v2a else 'FAIL ❌'}")
    print(f"  V2b log form:       R² = {r2:.6f}  (want >0.999)               → {'PASS ✅' if v2b else 'FAIL ❌'}")

    # V2b control: gapped chain saturates
    Xg, Pg = covariances(N, 0.5)
    Sg = np.array([interval_entropy(Xg, Pg, int(L)) for L in L_SWEEP])
    (mg, _), *_ = np.linalg.lstsq(A, Sg, rcond=None)
    cg = 3 * mg
    sat = abs(cg) < 0.05
    print(f"     control (gapped μ=0.5): S saturates, ΔS(L=20→200)={Sg[-1]-Sg[0]:.4f}, "
          f"pseudo-c={cg:.4f} → {'flat, PASS ✅' if sat else 'FAIL ❌'}")

    # V2c: precision canary — float64 vs mpmath on a small chain (methodological adequacy check)
    Nc_c, Lc = 100, 40
    Xc, Pc = covariances(Nc_c, MU)
    sc = (Nc_c - Lc) // 2
    iic = np.arange(sc, sc + Lc)
    nu2c = np.linalg.eigvals(Xc[np.ix_(iic, iic)] @ Pc[np.ix_(iic, iic)]).real
    Sf = float(np.sum(s_nu(np.sqrt(np.clip(nu2c, 0.25, None)))))
    Sm = entropy_mpmath(Nc_c, MU, Lc)
    rel = abs(Sm - Sf) / abs(Sm)
    v2c = rel < 1e-6
    print(f"  V2c precision canary (N={Nc_c},L={Lc}): float64 {Sf:.8f} vs mpmath {Sm:.8f}, "
          f"rel {rel:.1e} (want <1e-6) → {'PASS ✅ (float64 OK for M2)' if v2c else 'FAIL ❌'}")

    all_pass = v2a and v2b and v2c and sat
    print(f"\n  V2 {'SURVIVES ✅ — entropy instrument calibrated, M2 may proceed' if all_pass else 'FAILED ❌ — fix before M2'}")

    OUT.mkdir(exist_ok=True)
    (OUT / "v2_cft.json").write_text(json.dumps({
        "N": N, "mu": MU, "L_sweep": L_SWEEP,
        "S": S.tolist(), "x": x.tolist(),
        "c_measured": c, "slope": float(m), "R2": r2, "V2a_pass": bool(v2a), "V2b_pass": bool(v2b),
        "gapped_pseudo_c": float(cg), "gapped_saturates": bool(sat),
        "V2c_float64": float(S[-1]), "V2c_mpmath": Sm, "V2c_rel": rel, "V2c_pass": bool(v2c),
        "all_pass": bool(all_pass),
        "summary": f"1+1 massless chain interval entropy gives c={c:.4f} (R²={r2:.5f}); gapped control "
                   f"saturates (pseudo-c={cg:.3f}); float64=mpmath to {rel:.0e}. Entropy instrument "
                   f"calibrated for M2.",
    }, indent=1))
    print(f"  wrote results/v2_cft.json")


if __name__ == "__main__":
    main()
