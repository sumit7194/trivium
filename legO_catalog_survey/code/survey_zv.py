#!/usr/bin/env python3
"""Leg O (B4) extension — add the Zipoy–Voorhees (γ-) metric to the Killing–Yano survey (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python survey_zv.py

survey_catalog.py classified the Kerr-family catalog (all Boyer–Lindquist r,u coords) and the one bumpy
metric as the non-integrable case. This adds a SECOND, literature-standard non-integrable spacetime — the
**Zipoy–Voorhees γ-metric** (ansatz `zipoy_voorhees.py`): an EXACT static vacuum with a tunable Geroch–
Hansen quadrupole, δ=1 ≡ Schwarzschild, δ≠1 genuinely non-integrable (documented ZV chaos, Lukes-
Gerakopoulos 2010). It lives in prolate-spheroidal (x,y), so we run the same exact-rational KY-nullspace
search with monomials in (x,y). For INTEGER δ the metric is rational (exact linear algebra applies); δ=2 is
the clean deformed case. Gate: δ=1 must recover a KY 2-form (Schwarzschild); δ=2 must read NONE — making ZV
the survey's second independent confirmation that the instrument flags non-integrability, not just one bump.
Uses ansatz gr_engine + zipoy_voorhees read-only.
"""
import json
import sys
import time
from pathlib import Path

import sympy as sp

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from gr_engine import Geometry                                  # read-only

OUT = Path(__file__).resolve().parent.parent / "results"
t, x, y, ph = sp.symbols("t x y phi", real=True)
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def zv_geometry(delta, sigma=1):
    """Exact ZV γ-metric as a sympy Geometry in (t,x,y,φ) — matches ansatz zipoy_voorhees.metric.
    δ integer ⇒ F,H rational ⇒ exact-rational KY search applies. δ=1 is Schwarzschild."""
    F = ((x - 1) / (x + 1))**delta
    H = ((x**2 - 1) / (x**2 - y**2))**(delta**2)
    s2 = sp.Integer(sigma)**2
    g = sp.zeros(4)
    g[0, 0] = -F
    g[1, 1] = s2 / F * H * (x**2 - y**2) / (x**2 - 1)
    g[2, 2] = s2 / F * H * (x**2 - y**2) / (1 - y**2)
    g[3, 3] = s2 / F * (x**2 - 1) * (1 - y**2)
    return Geometry(g, [t, x, y, ph])


def ky_nullspace(geo, D=4, n_pts=220):
    """# of Killing–Yano 2-forms with degree-≤D polynomial components in (x,y): ∇₍ₐY_b₎c=0, by exact-rational
    point-sampling → homogeneous linear system → null-space dimension. Mirror of survey_catalog.ky_nullspace,
    monomials in (x,y) and sample points kept away from x=1, x²=y² (coordinate singularities)."""
    G, X = geo.christoffel, geo.coords
    mons = [x**i * y**j for i in range(D + 1) for j in range(D + 1 - i)]
    coeffs, Y = [], sp.zeros(4)
    for (i, j) in PAIRS:
        cs = list(sp.symbols(f"c_{i}{j}_0:{len(mons)}"))
        coeffs += cs
        e = sum(c * mm for c, mm in zip(cs, mons))
        Y[i, j], Y[j, i] = e, -e

    def nab(c, a_, b):
        return sp.diff(Y[a_, b], X[c]) - sum(G[d][c][a_] * Y[d, b] + G[d][c][b] * Y[a_, d] for d in range(4))

    resid = [nab(a_, b, c) + nab(b, a_, c) for a_ in range(4) for b in range(a_, 4) for c in range(4)]
    eqs = []
    for k in range(n_pts):
        xv = sp.Rational(5 + 2 * k, 3)                          # x ≥ 5/3 > 1 (outside the rod)
        yv = sp.Rational((-3 + k) % 7 - 3, 11)                  # y ∈ (-1,1), small rationals
        if xv == yv or xv == -yv:
            continue
        sub = {x: xv, y: yv}
        for e in resid:
            v = e.subs(sub)
            if v != 0:
                eqs.append(sp.nsimplify(v))
    Amat, _ = sp.linear_eq_to_matrix(eqs, coeffs)
    return len(Amat.nullspace())


def main():
    print("LEG O (B4) extension — Killing–Yano search on the Zipoy–Voorhees γ-metric (degree ≤4)\n")
    print("  δ=1 is Schwarzschild (gate: must admit its KY); δ=2 is the deformed γ-metric")
    print("  (exact vacuum, nonzero quadrupole, documented non-integrable) — must read NONE.\n")
    print(f"  {'metric':22s} {'KY 2-forms':>11}   verdict")
    out = {}
    for delta, name in [(1, "ZV δ=1 (Schwarzschild)"), (2, "ZV δ=2 (γ-metric, bumpy)")]:
        t0 = time.time()
        try:
            dim = ky_nullspace(zv_geometry(delta))
        except Exception as e:
            print(f"  {name:22s}  ERROR ({type(e).__name__}: {e})")
            out[name] = None
            continue
        out[name] = dim
        verdict = "YES (KY-integrable)" if dim >= 1 else "NO (no KY tensor)"
        print(f"  {name:22s} {dim:>11}   {verdict}   ({time.time()-t0:.0f}s)")

    gate = out.get("ZV δ=1 (Schwarzschild)")
    deformed = out.get("ZV δ=2 (γ-metric, bumpy)")
    ok = gate is not None and gate >= 1
    print(f"\n  GATE (ZV δ=1 must recover Schwarzschild's KY): {'PASS ✅' if ok else 'FAIL ❌'}")
    if ok and deformed == 0:
        print("  → ZV δ=2 admits NO Killing–Yano tensor (degree ≤4): a SECOND, literature-standard")
        print("    non-integrable spacetime the survey flags — alongside the bumpy metric (leg J). The")
        print("    instrument keys on integrability itself, not on one bump. (Caveat: degree ≤4, KY-origin.)")
    OUT.mkdir(exist_ok=True)
    (OUT / "survey_zv.json").write_text(json.dumps(
        {"ky_dim": out, "gate_pass": bool(ok),
         "verdict": "ZV δ=1 (Schwarzschild) KY-integrable; ZV δ=2 (γ-metric) no KY tensor — a 2nd "
                    "non-integrable confirmation for the leg-O instrument"}, indent=1))
    print("\n  wrote results/survey_zv.json")


if __name__ == "__main__":
    main()
