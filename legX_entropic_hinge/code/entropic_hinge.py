#!/usr/bin/env python3
"""Leg X — the entropic hinge on a lattice: S_rel(coherent‖vacuum on a wedge) = 2π × boost energy.

    /Users/sumit/Github/conjecture_machine/.venv/bin/python entropic_hinge.py

Gates X1/X2/X3 (+ observation O4) frozen in ../PREREGISTRATION.md before this was written. Harmonic chain,
exact Gaussian-state methods; the modular quadratic form is built from the reduced covariances in mpmath
(dps=60) because the boost weight 2πx lives exponentially deep in the symplectic spectrum (ν−1/2 ~ e^{-2πx})
— float64 caps at x≈5, which O4 exhibits deliberately.
"""
import json
import time
from pathlib import Path

from mpmath import mp, mpf, matrix, eigsy, sqrt, log, exp, pi

OUT = Path(__file__).resolve().parent.parent / "results"

N = 96                 # chain sites, Dirichlet
MU = mpf("0.5")        # mass (gap); correlation length ~2 sites
A_START = 49           # region A = sites 49..96 (1-indexed); cut at x_c = 48.5
XC = mpf("48.5")
SIGMA = mpf("2.5")     # packet width
X0_SWEEP = [8, 10, 12, 14]   # packet centers relative to the cut (baseline 12)
NU_FLOOR = mpf("1e-50")      # drop modular modes below nu - 1/2 < floor (dps=60)


def sym_funcs(M, fun):
    """fun applied to a symmetric mpmath matrix via eigendecomposition."""
    E, Q = eigsy(M)
    n = M.rows
    D = matrix(n, n)
    for i in range(n):
        D[i, i] = fun(E[i])
    return Q * D * Q.T


def build_chain():
    """Ground-state covariances X=(1/2)K^{-1/2}, P=(1/2)K^{1/2} for the Dirichlet chain (mp-exact)."""
    K = matrix(N, N)
    for i in range(N):
        K[i, i] = 2 + MU ** 2
        if i + 1 < N:
            K[i, i + 1] = K[i + 1, i] = -1
    E, Q = eigsy(K)
    n = N
    Dh = matrix(n, n)
    Dih = matrix(n, n)
    for i in range(n):
        s = sqrt(E[i])
        Dh[i, i] = s / 2          # (1/2)K^{1/2}
        Dih[i, i] = 1 / (2 * s)   # (1/2)K^{-1/2}
    P = Q * Dh * Q.T
    X = Q * Dih * Q.T
    return X, P


def modular_form(XA, PA):
    """A_q with S_rel = (1/2) f^T A_q f, from reduced covariances (same-covariance displaced Gaussians).

    X_A^{1/2} P_A X_A^{1/2} = W nu^2 W^T;  eps_k = ln((nu+1/2)/(nu-1/2));
    A_q = X_A^{-1/2} W diag(nu*eps) W^T X_A^{-1/2}.
    """
    Xh = sym_funcs(XA, lambda e: sqrt(e))
    Xih = sym_funcs(XA, lambda e: 1 / sqrt(e))
    S = Xh * PA * Xh
    E2, W = eigsy(S)
    L = XA.rows
    D = matrix(L, L)
    dropped = 0
    eps_max = mpf(0)
    for i in range(L):
        nu = sqrt(E2[i])
        gap = nu - mpf("0.5")
        if gap < NU_FLOOR:
            dropped += 1          # deep-wedge mode beyond precision floor: weight -> 0 (reported)
            D[i, i] = 0
            continue
        eps = log((nu + mpf("0.5")) / gap)
        eps_max = max(eps_max, eps)
        D[i, i] = nu * eps
    Aq = Xih * (W * D * W.T) * Xih
    return Aq, dropped, eps_max


def packet(j0):
    """Gaussian displacement f over the FULL chain (pi_f = 0), centered at site-coordinate j0."""
    return [exp(-((mpf(j + 1) - j0) ** 2) / (2 * SIGMA ** 2)) for j in range(N)]


def boost_energy(f):
    """2*pi*sum (x - x_c) T00 with the frozen convention: mass term at sites, gradient at links."""
    tot = mpf(0)
    for j in range(N):
        x = mpf(j + 1) - XC
        if x > 0:
            tot += x * mpf("0.5") * MU ** 2 * f[j] ** 2
    for j in range(N - 1):
        xl = mpf(j + 1) + mpf("0.5") - XC
        if xl > 0:
            tot += xl * mpf("0.5") * (f[j + 1] - f[j]) ** 2
    return 2 * pi * tot


def packet_energy(f):
    e = sum(mpf("0.5") * MU ** 2 * fj ** 2 for fj in f)
    e += sum(mpf("0.5") * (f[j + 1] - f[j]) ** 2 for j in range(N - 1))
    return e


def s_rel(Aq, f):
    fA = matrix([f[A_START - 1 + i] for i in range(N - A_START + 1)])
    return (fA.T * Aq * fA)[0, 0] / 2


def main():
    mp.dps = 60
    t0 = time.time()
    print("LEG X — the entropic hinge on a lattice (gates frozen in PREREGISTRATION.md)")
    print(f"  chain N={N}, mu={MU}, region A=sites {A_START}..{N} (cut x_c={XC}), mp dps={mp.dps}\n")

    X, P = build_chain()
    L = N - A_START + 1
    XA = matrix(L, L)
    PA = matrix(L, L)
    for i in range(L):
        for j in range(L):
            XA[i, j] = X[A_START - 1 + i, A_START - 1 + j]
            PA[i, j] = P[A_START - 1 + i, A_START - 1 + j]
    Aq, dropped, eps_max = modular_form(XA, PA)
    print(f"  modular form built ({time.time()-t0:.0f}s): eps_max={float(eps_max):.1f} "
          f"(x-reach ≈ {float(eps_max/(2*pi)):.1f} sites), modes dropped at floor: {dropped}/{L}")

    # ---- X2 sweep (and X1 baseline inside it)
    rows = []
    for x0 in X0_SWEEP:
        f = packet(XC + x0)
        sr = s_rel(Aq, f)
        eb = boost_energy(f)
        rows.append((x0, sr, eb, packet_energy(f)))
    print(f"\n  {'x0':>4} | {'S_rel':>12} | {'2π·boostE':>12} | ratio")
    for x0, sr, eb, _ in rows:
        print(f"  {x0:>4} | {float(sr):12.6f} | {float(eb):12.6f} | {float(sr/eb):.4f}")

    # X1: baseline x0=12
    b = next(r for r in rows if r[0] == 12)
    x1_ratio = float(b[1] / b[2])
    x1 = abs(x1_ratio - 1) < 0.08
    print(f"\n  X1 identity @x0=12: S_rel/(2π Σ x·T00) = {x1_ratio:.4f}  (|Δ|<8%)  →  {'PASS ✅' if x1 else 'FAIL ❌'}")

    # X2: slope of S_rel vs x0 = 2π E (E constant across rigid shifts)
    xs = [mpf(r[0]) for r in rows]
    ys = [r[1] for r in rows]
    n = len(rows)
    mx = sum(xs) / n
    my = sum(ys) / n
    slope = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / sum((xs[i] - mx) ** 2 for i in range(n))
    E = rows[0][3]
    two_pi_meas = slope / E
    x2_dev = abs(float(two_pi_meas / (2 * pi)) - 1)
    x2 = x2_dev < 0.03
    print(f"  X2 the 2π, measured: slope/E = {float(two_pi_meas):.5f}  vs 2π = {float(2*pi):.5f}  "
          f"({x2_dev:.2%})  →  {'PASS ✅ — Bisognano–Wichmann constant recovered from entropy data' if x2 else 'FAIL ❌'}")

    # X3: control — packet in the complement
    f_ctrl = packet(XC - 10)
    sr_ctrl = s_rel(Aq, f_ctrl)
    x3_frac = float(sr_ctrl / b[1])
    x3 = x3_frac < 0.02
    print(f"  X3 control (packet at x0=−10): S_rel/baseline = {x3_frac:.2e}  (<2%)  →  {'PASS ✅' if x3 else 'FAIL ❌'}")

    # O4: exhibit the float64 wall
    import numpy as np
    Kn = np.zeros((N, N))
    for i in range(N):
        Kn[i, i] = 2 + float(MU) ** 2
        if i + 1 < N:
            Kn[i, i + 1] = Kn[i + 1, i] = -1
    w, q = np.linalg.eigh(Kn)
    Xn = q @ np.diag(0.5 / np.sqrt(w)) @ q.T
    Pn = q @ np.diag(0.5 * np.sqrt(w)) @ q.T
    XAn = Xn[A_START - 1:, A_START - 1:]
    PAn = Pn[A_START - 1:, A_START - 1:]
    ex, qx = np.linalg.eigh(XAn)
    Xhn = qx @ np.diag(np.sqrt(np.abs(ex))) @ qx.T
    Xihn = qx @ np.diag(1 / np.sqrt(np.abs(ex))) @ qx.T
    e2, wv = np.linalg.eigh(Xhn @ PAn @ Xhn)
    nu = np.sqrt(np.abs(e2))
    gap = np.clip(nu - 0.5, 1e-300, None)
    eps64 = np.where(gap > 1e-14, np.log((nu + 0.5) / gap), 0.0)
    Aq64 = Xihn @ (wv @ np.diag(nu * eps64) @ wv.T) @ Xihn
    f64 = np.array([float(v) for v in packet(XC + 12)])[A_START - 1:]
    sr64 = 0.5 * f64 @ Aq64 @ f64
    o4_ratio = sr64 / float(b[1])
    print(f"  O4 float64 wall (observation): same pipeline in double precision @x0=12 recovers "
          f"{o4_ratio:.2%} of S_rel")
    print(f"     (the boost weight lives at ν−½ ~ e^(−2πx); float64 caps ε≈32 ⇒ x≈5 — an arithmetic-")
    print(f"     precision wall: walls-are-instrument-relative, number-format edition)")

    print(f"\n  framing (frozen): validates the IDENTITY the Jacobson/Dorau–Much derivations hinge on —")
    print(f"  not their conclusion (S=A/4 is a separate input). quantum's blind twin cross-gates later.")

    OUT.mkdir(exist_ok=True)
    (OUT / "entropic_hinge.json").write_text(json.dumps({
        "N": N, "mu": float(MU), "sigma": float(SIGMA), "dps": mp.dps,
        "sweep": [{"x0": r[0], "S_rel": float(r[1]), "two_pi_boostE": float(r[2]),
                   "ratio": float(r[1] / r[2])} for r in rows],
        "X1_ratio": x1_ratio, "X1_pass": bool(x1),
        "two_pi_measured": float(two_pi_meas), "X2_dev": x2_dev, "X2_pass": bool(x2),
        "X3_control_frac": x3_frac, "X3_pass": bool(x3),
        "O4_float64_recovers": o4_ratio, "eps_max": float(eps_max), "modes_dropped": dropped,
        "verdict": ("Coherent-state relative entropy on a wedge equals 2π x boost energy on the lattice: "
                    "identity ratio %.4f at baseline (X1), Bisognano-Wichmann 2π measured from entropy "
                    "data to %.2f%% (X2), complement control %.1e (X3). float64 recovers only %.0f%% "
                    "(O4 precision wall). Validates the hinge identity of Jacobson 1995 / Dorau-Much 2026; "
                    "not their S=A/4 input." % (x1_ratio, x2_dev * 100, x3_frac, o4_ratio * 100)),
    }, indent=1))
    print(f"\n  wrote results/entropic_hinge.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
