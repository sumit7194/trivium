#!/usr/bin/env python3
"""Move B — ANSATZ SIDE: the eikonal Kerr QNM from the exact metric (light-ring correspondence).

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python eikonal_kerr_qnm.py

Computes the eikonal/light-ring quasinormal mode ω = mΩ_c − i(n+½)λ for an equatorial Kerr
black hole, from ansatz's EXACT metric (read-only, the leg-1b pattern). §56's eikonal_qnm is
closed-form for a static lapse; the GW250114 remnant spins (χ≈0.79), so we get Ω_c (photon-ring
orbital frequency) and λ (its Lyapunov exponent) from the Hamiltonian radial potential of the
exact Kerr metric. The method is gated by the Schwarzschild limit: Ω_c=λ=1/(3√3), Q=2, b_c=3√3.

Hamiltonian radial potential (equatorial, null, p_t=−1, p_φ=ξ): ṙ² = g^{rr}·W(r,ξ),
  W = −(g^{tt} − 2g^{tφ}ξ + g^{φφ}ξ²). Circular photon orbit: W=W'=0 ⇒ (r_ph, ξ_c).
  affine Lyapunov κ = √(g^{rr}·W''/2);  dt/dλ = −g^{tt}+g^{tφ}ξ_c;  Ω_c = (−g^{tφ}+g^{φφ}ξ_c)/(dt/dλ);
  coordinate-time λ_Lyap = κ/(dt/dλ).  ω_R=mΩ_c, ω_I=(n+½)λ_Lyap, Q=ω_R/(2ω_I), b_c=ξ_c, Ω_c·b_c=1.
"""
import json
import math
import sys
from pathlib import Path

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from numeric_curvature import inv4                  # ansatz, read-only
sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as ex                       # exact Kerr metric, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"


def gi_eq(a, r):
    return inv4(ex.g_kerr_newman([0.0, r, math.pi / 2, 0.0], a, 0.0))


def W(a, r, xi):
    gi = gi_eq(a, r)
    return -(gi[0][0] - 2 * gi[0][3] * xi + gi[3][3] * xi * xi)


def eikonal_kerr(a, m=2, n=0, h=1e-5):
    # Bardeen prograde photon radius (a=0 → 3); the corotating (m>0) light ring
    r_ph = 2.0 * (1.0 + math.cos(2.0 / 3.0 * math.acos(-a)))
    gi = gi_eq(a, r_ph)
    A_, B_, C_ = gi[3][3], -2.0 * gi[0][3], gi[0][0]      # g^{φφ}ξ² − 2g^{tφ}ξ + g^{tt} = 0
    disc = B_ * B_ - 4.0 * A_ * C_
    roots = [(-B_ + math.sqrt(disc)) / (2 * A_), (-B_ - math.sqrt(disc)) / (2 * A_)]
    # the photon-orbit ξ is the root with W'(r_ph, ξ) ≈ 0 (double root in r)
    Wr = lambda xi: (W(a, r_ph + h, xi) - W(a, r_ph - h, xi)) / (2 * h)
    xi_c = min(roots, key=lambda xi: abs(Wr(xi)))
    gi = gi_eq(a, r_ph)
    Wrr = (W(a, r_ph + h, xi_c) - 2 * W(a, r_ph, xi_c) + W(a, r_ph - h, xi_c)) / h ** 2
    kappa = math.sqrt(max(gi[1][1] * Wrr / 2.0, 0.0))
    tdot = -gi[0][0] + gi[0][3] * xi_c
    phidot = -gi[0][3] + gi[3][3] * xi_c
    Om = phidot / tdot
    lyap = kappa / tdot
    wR, wI = m * Om, (n + 0.5) * lyap
    return dict(a=a, r_ph=r_ph, b_c=xi_c, Omega_c=Om, lyap=lyap,
                MwR=wR, MwI=wI, Q=wR / (2 * wI), unification=Om * xi_c, Wr_resid=abs(Wr(xi_c)))


def main():
    print("MOVE B — eikonal Kerr QNM from the exact metric (ansatz side)\n")
    # GATE: Schwarzschild limit must reproduce 1/(3√3), Q=2, b_c=3√3
    s = eikonal_kerr(1e-9)
    u = 1.0 / (3.0 * math.sqrt(3.0))
    print(f"  Schwarzschild gate: r_ph={s['r_ph']:.4f} (3)  Ω_c={s['Omega_c']:.5f} ({u:.5f})  "
          f"λ={s['lyap']:.5f} ({u:.5f})  Q={s['Q']:.4f} (2)  b_c={s['b_c']:.4f} ({3*math.sqrt(3):.4f})  "
          f"Ω·b={s['unification']:.6f} (1)")
    gate_ok = (abs(s['Omega_c'] - u) < 1e-3 and abs(s['lyap'] - u) < 1e-3
               and abs(s['Q'] - 2) < 0.02 and abs(s['unification'] - 1) < 1e-4)
    print(f"  gate {'PASSED ✅' if gate_ok else 'FAILED ❌'}\n")

    chi_grid = [0.0, 0.3, 0.5, 0.641, 0.787, 0.815, 0.887]   # incl remnant 90% CI edges
    rows = [eikonal_kerr(a) for a in chi_grid]
    print(f"  {'χ':>6} {'r_ph':>7} {'Ω_c':>8} {'λ_Lyap':>8} {'Mω_R(220)':>10} {'Q(220)':>8} {'Ω·b':>7}")
    for x in rows:
        print(f"  {x['a']:6.3f} {x['r_ph']:7.4f} {x['Omega_c']:8.5f} {x['lyap']:8.5f} "
              f"{x['MwR']:10.4f} {x['Q']:8.3f} {x['unification']:7.4f}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "eikonal_kerr_qnm.json").write_text(json.dumps(
        {"schwarzschild_gate_ok": gate_ok, "u_schwarzschild": u, "rows": rows}, indent=1))
    print(f"\n  remnant χ=0.787:  Mω_R(220)={rows[4]['MwR']:.4f}  Q(220)={rows[4]['Q']:.3f}  "
          f"b_shadow={rows[4]['b_c']:.4f}")
    print("  wrote results/eikonal_kerr_qnm.json")


if __name__ == "__main__":
    main()
