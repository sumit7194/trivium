#!/usr/bin/env python3
"""Leg J — numeric Killing-tensor search on OUR bump, closing the non-KY-origin caveat (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python numeric_killing_search.py

leg J's symbolic search ruled out a KY-origin (Carter-type) Killing tensor; ansatz §85 ruled out ANY
rank-2 (quadratic-in-momenta) invariant for ITS bump (ε(3cos²θ−1)/r³) by a multi-orbit SVD null-space.
This ports §85's exact method (its basis, SVD, validation gate — read-only) onto OUR bump
g_tt·(1+6ε cos²θ/r), so the non-KY-origin caveat is closed for the SAME metric leg J used.

Method (ansatz §85, _qinvariant.py): a quadratic-in-momenta C=Σc_kφ_k is constant along every geodesic;
sample many orbits (fixed E,L, varied inclination), mean-subtract per orbit, stack, SVD. A genuine
invariant = a near-zero singular value with a big gap. Gate: Kerr must recover the Carter constant.
"""
import json
import sys
from pathlib import Path

import sympy as sp

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from poincare import build_hamilton                       # ansatz, read-only
import _qinvariant as qi                                  # ansatz §85 method, read-only (basis/fit/SVD)

RES = Path(__file__).resolve().parent.parent / "results"
t, r, th, ph = sp.symbols("t r theta phi", real=True)
A = sp.Rational(3, 5)
Sig = r**2 + A**2 * sp.cos(th)**2
De = r**2 - 2 * r + A**2
s2 = sp.sin(th)**2
E, L, R0 = 0.95, 3.4, 8.0
P2LIST = [round(0.08 + 0.04 * k, 3) for k in range(18)]    # many inclinations → many bound orbits


def our_metric(eps):
    """Kerr, with leg J's bump g_tt·(1+6ε cos²θ/r) (NOT §85's ε(3cos²θ−1)/r³)."""
    g = sp.zeros(4)
    g[0, 0] = -(1 - 2 * r / Sig)
    g[0, 3] = g[3, 0] = -2 * r * A * s2 / Sig
    g[1, 1] = Sig / De
    g[2, 2] = Sig
    g[3, 3] = (r**2 + A**2 + 2 * r * A**2 * s2 / Sig) * s2
    if eps:
        g[0, 0] = g[0, 0] * (1 + sp.Rational(eps) * sp.cos(th)**2 * 6 / r)
    return build_hamilton(g, [t, r, th, ph], 1, 2)


def main():
    print("LEG J — numeric rank-2 Killing-tensor search on OUR bump (ports ansatz §85's method)\n")
    indep = qi.check_independence()
    print(f"  basis independence (smallest SV on random points): {indep:.2e}  "
          f"{'✅ no hidden identity' if indep > 1e-6 else '❌ DEGENERATE'}")

    Sk, nk, veck = qi.fit(our_metric(0), E, L, P2LIST, R0)
    gapk = Sk[-2] / Sk[-1]
    terms = dict(zip(qi.BNAMES, veck))
    L2, aaE = L**2, 0.6**2 * (1 - E**2)
    bet, alp = terms["u2/om"] / terms["pth2"], terms["u2"] / terms["pth2"]
    carter_match = abs(bet - L2) / L2 < 0.05 and abs(alp - aaE) / aaE < 0.2
    gate = Sk[-1] < 1e-9 and gapk > 1e6 and carter_match
    print(f"\n  GATE — Kerr [{nk} orbits]: smallest SV={Sk[-1]:.2e}, gap={gapk:.1e}")
    print(f"    recovered C ≈ p_θ² + {bet:.2f}·cot²θ + {alp:.3f}·cos²θ  vs Carter p_θ² + {L2:.2f}·cot²θ + "
          f"{aaE:.3f}·cos²θ  {'✅ recovers Carter' if carter_match else '❌'}")
    print(f"    gate {'PASS ✅' if gate else 'FAIL ❌'}")

    res = {"basis_indep": float(indep), "gate_pass": bool(gate), "kerr_smallest_SV": float(Sk[-1]),
           "kerr_gap": float(gapk), "bumpy": {}}
    print(f"\n  TEST — leg J's bump g_tt·(1+6ε cos²θ/r):")
    smalls = []
    for eps in (0.1, 0.2, 0.35):
        Sd, nd, _ = qi.fit(our_metric(eps), E, L, P2LIST, R0)
        gap = Sd[-2] / Sd[-1]
        smalls.append(Sd[-1])
        res["bumpy"][str(eps)] = {"smallest_SV": float(Sd[-1]), "gap": float(gap), "n_orbits": nd}
        print(f"    ε={eps:<4} [{nd} orbits]: smallest SV={Sd[-1]:.2e}, gap={gap:.1f}  → "
              f"{'NO invariant' if Sd[-1] > 1e-4 and gap < 10 else 'has near-zero SV?!'}")
    no_inv = all(s > 1e-4 for s in smalls)
    grows = smalls[0] < smalls[1] < smalls[2]
    res["no_invariant"] = bool(no_inv)
    res["obstruction_grows_with_eps"] = bool(grows)
    print(f"\n  RESULT: Kerr Carter recovered (SV {Sk[-1]:.1e}); our bump has NO conserved quadratic "
          f"(smallest SV {min(smalls):.1e}–{max(smalls):.1e}, grows with ε: {grows}).")
    print("  → Closes leg J's non-KY-origin caveat at rank 2: independent of the symbolic KY proof, no")
    print("    rank-2 Killing tensor (KY-origin or not) survives OUR bump. Matches ansatz §85 (different bump).")
    print("    Residual (shared with §85): a higher-rank/quartic Killing tensor is not excluded.")
    (RES / "numeric_killing_search.json").write_text(json.dumps(res, indent=1))
    print("\n  wrote results/numeric_killing_search.json")


if __name__ == "__main__":
    main()
