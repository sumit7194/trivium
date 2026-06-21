#!/usr/bin/env python3
"""Leg J — the PROOF horn: a complete symbolic Killing–Yano search (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python symbolic_ky_search.py

By Eisenhart's theorem (used by Kerr-deformation studies, e.g. arXiv:1807.08594), an EXACT second-rank
Killing tensor of the Carter type exists iff a Killing–Yano (KY) 2-form Y exists (∇₍ₐY_b₎c = 0). The KY
tensor is the structural root and — crucially — in rational u=cosθ coordinates Kerr's KY is POLYNOMIAL of
degree ≤3 (Y_tr=−au, Y_tu=−ar, Y_rφ=−a²u(1−u²), Y_uφ=−r(r²+a²)), unlike the Carter tensor's degree-6
form. So a *complete* degree-D polynomial KY ansatz is decidable by exact linear algebra and is GUARANTEED
to contain Kerr's answer.

Method: ansatz Y antisymmetric, each component a degree-D polynomial in (r,u) with unknown coefficients;
impose ∇₍ₐY_b₎c = 0 at many exact-rational sample points → homogeneous linear system; the null-space
dimension = number of independent KY tensors of degree ≤D.
  • CALIBRATION GATE: on Kerr the null-space must be ≥1 (it must rediscover Kerr's KY), else void.
  • TEST: on the bumpy metric — does any KY tensor survive at degree ≤D? Literature predicts NO for a
    generic (non-engineered) deformation; this DECIDES it for our specific bump, up to degree D.
Prior art (so we neither repeat nor overclaim): Brink, Spacetime Encodings III/IV (arXiv:0911.1589,
0911.1595) — exact 2nd-order KTs in stationary-axisymmetric-vacuum are very restrictive; "Preserving Kerr
symmetries in deformed spacetimes" (arXiv:1807.08594) — generic deformations keep only an APPROXIMATE KT.
"""
import json
import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from gr_engine import Geometry                                          # read-only

RES = Path(__file__).resolve().parent.parent / "results"
t, r, u, ph = sp.symbols("t r u phi", real=True)
M_VAL, A_VAL = sp.Integer(1), sp.Rational(3, 5)                         # concrete metric (a=0.6 rung)
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def geom(eps):
    """Kerr (eps=0) or bumpy g_tt·(1+6ε u²/r), in rational u=cosθ coords, at M=1, a=3/5."""
    M, a = M_VAL, A_VAL
    Sig = r**2 + a**2 * u**2
    De = r**2 - 2 * M * r + a**2
    om = 1 - u**2
    g = sp.zeros(4)
    g[0, 0] = -(1 - 2 * M * r / Sig) * (1 + 6 * eps * u**2 / r)
    g[0, 3] = g[3, 0] = -2 * M * r * a * om / Sig
    g[1, 1] = Sig / De
    g[2, 2] = Sig / om
    g[3, 3] = (r**2 + a**2 + 2 * M * r * a**2 * om / Sig) * om
    return Geometry(g, [t, r, u, ph])


def ky_nullspace(eps, D=3, n_pts=140):
    geo = geom(eps)
    G, X = geo.christoffel, geo.coords
    mons = [r**i * u**j for i in range(D + 1) for j in range(D + 1 - i)]
    coeffs, Y = [], sp.zeros(4)
    for (i, j) in PAIRS:
        cs = list(sp.symbols(f"c_{i}{j}_0:{len(mons)}"))
        coeffs += cs
        e = sum(c * m for c, m in zip(cs, mons))
        Y[i, j], Y[j, i] = e, -e

    def nab(c, A, B):                                                   # ∇_c Y_AB
        return sp.diff(Y[A, B], X[c]) - sum(G[d][c][A] * Y[d, B] + G[d][c][B] * Y[A, d] for d in range(4))

    resid = []                                                         # the KY operator ∇_(a Y_b)c
    for A in range(4):
        for B in range(A, 4):
            for C in range(4):
                resid.append(nab(A, B, C) + nab(B, A, C))

    # sample at exact-rational points → homogeneous linear system in `coeffs`
    rng = [(sp.Rational(7 + k, 2), sp.Rational((-5 + 2 * k) % 9 - 4, 7)) for k in range(n_pts)]
    eqs = []
    for (r0, u0) in rng:
        sub = {r: r0, u: u0}
        for e in resid:
            val = e.subs(sub)
            if val != 0:
                eqs.append(sp.expand(val))
    Amat, _ = sp.linear_eq_to_matrix(eqs, coeffs)
    ns = Amat.nullspace()
    return len(ns), len(coeffs), coeffs, ns


def main():
    print("LEG J — symbolic Killing–Yano search (the proof horn): does an exact hidden symmetry survive?\n")
    D = 3
    out = {}
    for label, eps in [("Kerr (gate)", sp.Integer(0)), ("bumpy ε=0.20", sp.Rational(1, 5)),
                       ("bumpy ε=0.35", sp.Rational(7, 20))]:
        dim, n, coeffs, ns = ky_nullspace(eps, D=D)
        out[label] = dim
        print(f"  {label:14s}: KY null-space dimension (degree ≤{D}) = {dim}   "
              f"{'→ a KY tensor EXISTS' if dim >= 1 else '→ NO KY tensor (degree ≤%d)' % D}")
        if label.startswith("Kerr"):
            gate = dim >= 1
            print(f"      G1 gate (Kerr must rediscover its KY): {'PASS ✅' if gate else 'FAIL ❌'}")
            if not gate:
                print("      instrument void — aborting."); break
    if out.get("Kerr (gate)", 0) >= 1:
        bumpy_ok = all(out.get(k, 1) == 0 for k in out if k.startswith("bumpy"))
        print(f"\n  RESULT: Kerr has {out['Kerr (gate)']} KY tensor(s); the bumpy metric has "
              f"{'NONE at degree ≤%d' % D if bumpy_ok else 'a surviving KY'} "
              f"(ε=0.20 → {out.get('bumpy ε=0.20')}, ε=0.35 → {out.get('bumpy ε=0.35')}).")
        if bumpy_ok:
            print("  → By Eisenhart, NO exact Carter-type Killing tensor survives the bump (up to degree 3):")
            print("    the strict horn (a new exact hidden symmetry) is CLOSED for this deformation. Combined")
            print("    with leg J's bounded non-diffusing C₀, the picture is: formally non-integrable, but")
            print("    near-integrable (an APPROXIMATE invariant survives) — matching the deformation")
            print("    literature (Brink III/IV; arXiv:1807.08594). Caveat: rules out KY-origin (Carter-type)")
            print("    tensors up to degree 3; a higher-degree or non-KY-origin KT is not excluded.")
    (RES / "symbolic_ky_search.json").write_text(json.dumps(
        {f"{k}": v for k, v in out.items()} | {"degree": D}, indent=1))
    print("\n  wrote results/symbolic_ky_search.json")


if __name__ == "__main__":
    main()
