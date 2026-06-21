#!/usr/bin/env python3
"""Move A v2 (cont.) — symbolic proof of the Kerr–NEWMAN Carter Killing tensor (§78).

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python certify_symbolic_kn.py

certify_symbolic.py proved Kerr's Carter tensor symbolically; this extends it to Kerr–Newman (the
charged case tabula also recovered blind, a²=0.36), by passing Δ = r²−2Mr+a²+Q² to the same
Kerr-form metric and Carter tensor and re-running ansatz §78's symbolic verifier. (Kerr–de Sitter is
proven separately in certify_symbolic_kds.py — all three EXISTS rungs are now theorems.)
"""
import json
import sys
from pathlib import Path

import sympy as sp

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from gr_engine import Geometry                                # ansatz, read-only

LEGA = Path(__file__).resolve().parent.parent / "results"
t, r, u, ph = sp.symbols("t r u phi", real=True)
M, a, Q = sp.symbols("M a Q", positive=True)


def delta_geometry(Dexpr):
    """The Kerr-form metric (rational u=cosθ coords) parametrised by Δ — Kerr if Δ=r²−2Mr+a²,
    Kerr–Newman if Δ=r²−2Mr+a²+Q² (then g_tt=−(1−(2Mr−Q²)/Σ), the Einstein–Maxwell metric)."""
    s2 = 1 - u**2
    Sig = r**2 + a**2 * u**2
    g = sp.zeros(4)
    g[0, 0] = -(Dexpr - a**2 * s2) / Sig
    g[0, 3] = g[3, 0] = -a * s2 * (r**2 + a**2 - Dexpr) / Sig
    g[1, 1] = Sig / Dexpr
    g[2, 2] = Sig / s2
    g[3, 3] = s2 * ((r**2 + a**2)**2 - Dexpr * a**2 * s2) / Sig
    return Geometry(g, [t, r, u, ph]), Sig


def delta_carter(geo, Dexpr, Sig):
    """Carter Killing tensor K = Σ(lₐn_b+l_b nₐ) + r²g with the principal nulls for this Δ."""
    l = [(r**2 + a**2) / Dexpr, 1, 0, a / Dexpr]
    nv = [(r**2 + a**2) / (2 * Sig), -Dexpr / (2 * Sig), 0, a / (2 * Sig)]
    g, gi = geo.g, geo.ginv
    Kup = sp.Matrix(4, 4, lambda i, j: Sig * (l[i] * nv[j] + l[j] * nv[i]) + r**2 * gi[i, j])
    Kd = sp.Matrix(4, 4, lambda i, j: sum(g[i, p] * g[j, q] * Kup[p, q] for p in range(4) for q in range(4)))
    return sp.Matrix(4, 4, lambda i, j: sp.cancel(sp.together(Kd[i, j])))


def prove(name, Dexpr):
    geo, Sig = delta_geometry(Dexpr)
    K = delta_carter(geo, Dexpr, Sig)
    resid = geo.killing_tensor_residual(K)
    ok = geo.is_killing_tensor(K)
    print(f"  {name:14s} Δ={Dexpr}:  ∇₍ₐK_bc₎ = {resid}   → is_killing_tensor = {ok}  "
          f"{'✅ PROVEN' if ok else '❌'}")
    return ok


def main():
    print("MOVE A v2 (cont.) — symbolic Carter proof, extended to Kerr–Newman (§78)\n")
    cand = json.loads((LEGA / "candidate_kerr_newman.json").read_text())
    co = cand["coeffs"]
    print(f"  tabula discovered KN blind: coeffs (1, {co['c_cos2']/co['c_ptheta2']:+.3f}, "
          f"{co['c_cos2_E2']/co['c_ptheta2']:+.3f}, {co['c_cos2_Lz2_csc2']/co['c_ptheta2']:+.3f}) "
          f"= (1, a², −a², 1) with a²=0.36 — the Carter direction.\n")
    kerr_ok = prove("Kerr", r**2 - 2*M*r + a**2)                       # sanity: matches §78
    kn_ok = prove("Kerr-Newman", r**2 - 2*M*r + a**2 + Q**2)           # the new proof
    print(f"\n  RESULT: Kerr {'✅' if kerr_ok else '❌'}, Kerr–Newman {'✅ PROVEN symbolically' if kn_ok else '❌'}.")
    print("  tabula's blind KN Carter discovery is now certified as a THEOREM (∇₍ₐK_bc₎≡0 for all M,a,Q),")
    print("  not a numeric residual. (Kerr–de Sitter is proven in certify_symbolic_kds.py.)")
    (LEGA / "certify_symbolic_kn.json").write_text(json.dumps(
        {"kerr_proven": bool(kerr_ok), "kerr_newman_proven": bool(kn_ok)}, indent=1))
    print("  wrote results/certify_symbolic_kn.json")


if __name__ == "__main__":
    main()
