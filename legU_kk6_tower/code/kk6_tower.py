#!/usr/bin/env python3
"""Leg U — the 6D KK tower and its axion, on the bridge's own two-loop projection simulator.

    python3 kk6_tower.py

Gates U1/U2/U3 frozen in ../PREREGISTRATION.md before this was written. A massless wave on a hidden T²
(two curled-up loops) with internal metric M projects, in the visible dimension, to a tower of massive
particles: a winding sector (n1,n2) buzzes at rest at frequency m = sqrt((M^-1)^{ab} n_a n_b).

  U1  diagonal M = diag(1,1): measured buzz reproduces the sum-of-two-squares tower m = sqrt(n1²+n2²),
      with the within-shell degeneracy (1,1)≡(1,-1), (1,0)≡(0,1)  [ansatz §112's proven spectrum].
  U2  twisted M = [[1,χ],[χ,1]] (χ = the axion, ansatz §113): the cross-term −2χ n1 n2 SPLITS the
      (1,±1) pair (n1n2≠0) and leaves (1,0),(0,1) degenerate (n1n2=0 control) — the axion made measurable.

The internal metric enters ONLY through a finite-difference Laplace-Beltrami operator on the hidden torus
(the twist is the genuine cross-derivative 2 g12 ∂_{y1}∂_{y2}); the buzz frequency is MEASURED from the
time series (projected modal amplitude → FFT peak), never injected. Read-only from ansatz; own code.
Pure numpy. Consistency triangulation, not a claim about real extra dimensions (U3).
"""
import json
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "results"

NY = 64                      # hidden-torus grid per loop (both loops in [0, 2π))
DT = 0.02                    # leapfrog step (well under the CFL bound for this grid/metric)
T_TOTAL = 400.0             # long run → many periods → tight FFT resolution
TOL = 0.02                  # U1/U2 buzz tolerance (finite-difference instrument floor)
DEGEN_TOL = 0.01            # within-shell degeneracy / control-split tolerance (fraction of m)
SECTORS = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 0), (0, 2), (2, 1), (1, 2)]


def inv_metric(chi):
    """M = [[1, chi],[chi, 1]] → M^{-1} components (g11, g12, g22); det M = 1 - chi²."""
    det = 1.0 - chi * chi
    return 1.0 / det, -chi / det, 1.0 / det


def predicted_mass(n1, n2, chi):
    """Continuum KK mass m = sqrt((M^-1)^{ab} n_a n_b) = sqrt((n1²+n2² − 2χ n1n2)/(1−χ²))."""
    g11, g12, g22 = inv_metric(chi)
    return math.sqrt(g11 * n1 * n1 + 2 * g12 * n1 * n2 + g22 * n2 * n2)


def laplace_beltrami(phi, g11, g12, g22, dx):
    """FD ∇²_hidden = g11 ∂²_1 + 2 g12 ∂_1∂_2 + g22 ∂²_2, periodic (the twist = the cross term)."""
    d2_1 = (np.roll(phi, -1, 0) - 2 * phi + np.roll(phi, 1, 0)) / dx ** 2
    d2_2 = (np.roll(phi, -1, 1) - 2 * phi + np.roll(phi, 1, 1)) / dx ** 2
    dxy = (np.roll(np.roll(phi, -1, 0), -1, 1) - np.roll(np.roll(phi, -1, 0), 1, 1)
           - np.roll(np.roll(phi, 1, 0), -1, 1) + np.roll(np.roll(phi, 1, 0), 1, 1)) / (4 * dx ** 2)
    return g11 * d2_1 + 2 * g12 * dxy + g22 * d2_2


def measure_buzz(n1, n2, chi):
    """Rest-buzz of winding sector (n1,n2): evolve the massless 2D wave, MEASURE the oscillation ω."""
    dx = 2 * math.pi / NY
    y = np.arange(NY) * dx
    Y1, Y2 = np.meshgrid(y, y, indexing="ij")
    g11, g12, g22 = inv_metric(chi)

    phi0 = np.cos(n1 * Y1 + n2 * Y2)                 # a single winding mode, at visible rest
    norm = np.sum(phi0 * phi0)
    lap = lambda p: laplace_beltrami(p, g11, g12, g22, dx)

    phi_prev = phi0.copy()
    phi = phi0 + 0.5 * DT ** 2 * lap(phi0)           # zero-velocity leapfrog start
    nsteps = int(T_TOTAL / DT)
    amp = np.empty(nsteps + 1)
    amp[0] = 1.0
    for k in range(1, nsteps + 1):
        phi_next = 2 * phi - phi_prev + DT ** 2 * lap(phi)
        phi_prev, phi = phi, phi_next
        amp[k] = np.sum(phi * phi0) / norm           # modal amplitude a(t) = cos(ω t)

    # ω from the FFT peak of a(t), with parabolic sub-bin interpolation
    spec = np.abs(np.fft.rfft(amp - amp.mean()))
    w = 2 * math.pi * np.fft.rfftfreq(len(amp), d=DT)
    k0 = int(np.argmax(spec))
    if 0 < k0 < len(spec) - 1:                        # parabolic interpolation of the peak
        a, b, c = spec[k0 - 1], spec[k0], spec[k0 + 1]
        delta = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) != 0 else 0.0
        return w[k0] + delta * (w[1] - w[0])
    return w[k0]


def run(chi, label):
    print(f"\n  {label}  (χ = {chi}, det M = {1 - chi*chi:.4f})")
    print(f"  {'sector':>9} | {'m measured':>11} | {'m predicted':>11} | {'err':>7}")
    rows = []
    for (n1, n2) in SECTORS:
        m_meas = measure_buzz(n1, n2, chi)
        m_pred = predicted_mass(n1, n2, chi)
        err = abs(m_meas - m_pred) / m_pred
        rows.append({"n1": n1, "n2": n2, "m_meas": m_meas, "m_pred": m_pred, "rel_err": err})
        print(f"  ({n1:>2},{n2:>2})  | {m_meas:11.5f} | {m_pred:11.5f} | {err:6.2%}")
    return rows


def get(rows, n1, n2):
    return next(r for r in rows if r["n1"] == n1 and r["n2"] == n2)


def main():
    print("LEG U — 6D KK tower + axion, on the bridge's own T² projection simulator")
    print(f"  hidden grid {NY}×{NY}, dt {DT}, T {T_TOTAL:.0f}; gates frozen in PREREGISTRATION.md")

    diag = run(0.0, "U1 — diagonal tower (M = diag(1,1))")
    max_err_d = max(r["rel_err"] for r in diag)
    # within-shell degeneracy at χ=0
    d_10_01 = abs(get(diag, 1, 0)["m_meas"] - get(diag, 0, 1)["m_meas"]) / get(diag, 1, 0)["m_meas"]
    d_11 = abs(get(diag, 1, 1)["m_meas"] - get(diag, 1, -1)["m_meas"]) / get(diag, 1, 1)["m_meas"]
    d_21_12 = abs(get(diag, 2, 1)["m_meas"] - get(diag, 1, 2)["m_meas"]) / get(diag, 2, 1)["m_meas"]
    u1 = (max_err_d < TOL) and (d_10_01 < DEGEN_TOL) and (d_11 < DEGEN_TOL) and (d_21_12 < DEGEN_TOL)
    print(f"\n  U1: max buzz err {max_err_d:.2%} (<{TOL:.0%}); within-shell degeneracy |Δ|/m: "
          f"(1,0)≡(0,1) {d_10_01:.2%}, (1,1)≡(1,-1) {d_11:.2%}, (2,1)≡(1,2) {d_21_12:.2%} "
          f"(<{DEGEN_TOL:.0%})  →  {'PASS ✅' if u1 else 'FAIL ❌'}")

    CHI = 0.3
    tw = run(CHI, "U2 — twisted tower (M = [[1,χ],[χ,1]]) — the axion")
    # headline: (1,±1) split with correct sign & size; control (1,0),(0,1) does NOT split
    m11, m1m1 = get(tw, 1, 1)["m_meas"], get(tw, 1, -1)["m_meas"]
    e11 = get(tw, 1, 1)["rel_err"]
    e1m1 = get(tw, 1, -1)["rel_err"]
    dm2_meas = m1m1 ** 2 - m11 ** 2
    dm2_pred = 4 * CHI / (1 - CHI ** 2)
    split_ok = (e11 < TOL) and (e1m1 < TOL) and (m1m1 > m11) \
        and abs(dm2_meas - dm2_pred) / dm2_pred < TOL
    ctrl_split = abs(get(tw, 1, 0)["m_meas"] - get(tw, 0, 1)["m_meas"]) / get(tw, 1, 0)["m_meas"]
    ctrl_ok = ctrl_split < DEGEN_TOL
    u2 = split_ok and ctrl_ok
    print(f"\n  U2: axion channel (1,±1) split  m(1,1)={m11:.4f}  m(1,-1)={m1m1:.4f}  "
          f"(pred 1.24035 / 1.69031)")
    print(f"      Δ(m²) measured {dm2_meas:.4f} vs predicted 4χ/(1−χ²) {dm2_pred:.4f} "
          f"({abs(dm2_meas-dm2_pred)/dm2_pred:.2%})")
    print(f"      control (1,0)≡(0,1) split |Δ|/m = {ctrl_split:.2%} (<{DEGEN_TOL:.0%}, must NOT split)")
    print(f"      →  {'PASS ✅ — the twist is a measurable axion coupling' if u2 else 'FAIL ❌'}")

    print(f"\n  U3 (frozen framing): flat-torus KK spectrum — textbook. The result is the cross-repo")
    print(f"      triangulation: this independent numeric instrument reproduces ansatz §112's proven")
    print(f"      diagonal-M tower AND exhibits §113's axion (χ) as a degeneracy-splitting. NOT a claim")
    print(f"      about real extra dimensions; extends quantum's 5D demo + leg S's tower to 6D.")

    OUT.mkdir(exist_ok=True)
    (OUT / "kk6_tower.json").write_text(json.dumps({
        "grid": NY, "dt": DT, "T_total": T_TOTAL, "tol": TOL, "degen_tol": DEGEN_TOL,
        "diagonal": diag, "twisted_chi": CHI, "twisted": tw,
        "U1_max_err": max_err_d, "U1_degen_11": d_11, "U1_degen_10_01": d_10_01, "U1_pass": bool(u1),
        "U2_m11": m11, "U2_m1m1": m1m1, "U2_dm2_meas": dm2_meas, "U2_dm2_pred": dm2_pred,
        "U2_control_split": ctrl_split, "U2_pass": bool(u2),
        "verdict": ("The bridge's own T² projection simulator reproduces ansatz §112's diagonal-M "
                    "sum-of-two-squares KK tower (U1, max err %.2f%%) and exhibits §113's axion: turning on "
                    "the twist χ=0.3 splits the (1,±1) degeneracy by Δ(m²)=%.3f (coset-metric prediction "
                    "%.3f) while leaving the n1n2=0 control unsplit (%.2f%%). Cross-repo triangulation of a "
                    "machine-proven 6D structure; not a claim about real extra dimensions."
                    % (max_err_d * 100, dm2_meas, dm2_pred, ctrl_split * 100)),
    }, indent=1))
    print(f"\n  wrote results/kk6_tower.json")


if __name__ == "__main__":
    main()
