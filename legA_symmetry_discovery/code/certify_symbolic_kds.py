#!/usr/bin/env python3
"""Move A v2 (cont.) — bounded attempt at a SYMBOLIC Kerr–de Sitter Carter proof (§78).

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python certify_symbolic_kds.py

Kerr and Kerr–Newman are proven symbolically (certify_symbolic*.py). Kerr–de Sitter has a rational
Δ_θ = 1 + (Λ/3)a²u², so its Killing tensor and the residual are heavier. This builds the Kerr–dS
metric in rational u=cosθ coords and tests candidate Carter Killing-tensor forms with ansatz §78's
verifier as the oracle (it returns 0 iff K is genuinely Killing). If one closes, the proof extends to
Kerr–dS; if not, Move A's numeric certification stands and the symbolic proof is logged as deferred.
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
M, a, L3 = sp.symbols("M a Lambda3", positive=True)          # L3 = Λ/3


def kds_geometry():
    """Kerr–de Sitter (Carter form, u=cosθ). Δr=(1−L3 r²)(r²+a²)−2Mr, Δu=1+L3 a²u², Ξ=1+L3 a²."""
    s2 = 1 - u**2
    Sig = r**2 + a**2 * u**2
    Dr = (1 - L3 * r**2) * (r**2 + a**2) - 2 * M * r
    Du = 1 + L3 * a**2 * u**2
    Xi = 1 + L3 * a**2
    al = [1, 0, 0, -a * s2]                                  # α = dt − a s² dφ
    be = [a, 0, 0, -(r**2 + a**2)]                           # β = a dt − (r²+a²) dφ
    g = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            g[i, j] = (-(Dr / (Xi**2 * Sig)) * al[i] * al[j]
                       + (Du * s2 / (Xi**2 * Sig)) * be[i] * be[j])
    g[1, 1] = Sig / Dr
    g[2, 2] = Sig / (Du * s2)
    return Geometry(g, [t, r, u, ph]), Sig, Dr, Du, Xi, s2


def main():
    print("MOVE A v2 (cont.) — bounded SYMBOLIC Kerr–de Sitter Carter attempt (§78)\n")
    geo, Sig, Dr, Du, Xi, s2 = kds_geometry()
    g, gi = geo.g, geo.ginv

    # candidate principal nulls (contravariant), Ξ-scaled — Kerr's reduce at L3→0
    l = [Xi * (r**2 + a**2) / Dr, 1, 0, Xi * a / Dr]
    nv = [Xi * (r**2 + a**2) / (2 * Sig), -Dr / (2 * Sig), 0, Xi * a / (2 * Sig)]

    def lower(Kup):
        Kd = sp.Matrix(4, 4, lambda i, j: sum(g[i, p] * g[j, q] * Kup[p, q]
                                              for p in range(4) for q in range(4)))
        return sp.Matrix(4, 4, lambda i, j: sp.cancel(sp.together(Kd[i, j])))

    cands = {
        "Σ(ln+nl)+r²g": lower(sp.Matrix(4, 4, lambda i, j: Sig * (l[i]*nv[j] + l[j]*nv[i]) + r**2 * gi[i, j])),
        "Σ(ln+nl)−a²u²g": lower(sp.Matrix(4, 4, lambda i, j: Sig * (l[i]*nv[j] + l[j]*nv[i]) - a**2*u**2 * gi[i, j])),
    }
    proven = None
    for name, K in cands.items():
        try:
            ok = geo.is_killing_tensor(K)
        except Exception as e:
            print(f"  {name:18s}: verifier raised ({type(e).__name__}) — too heavy"); continue
        print(f"  {name:18s}: is_killing_tensor → {ok}  {'✅ PROVEN' if ok else '— residual ≠ 0'}")
        if ok:
            proven = name; break

    if proven:
        print(f"\n  RESULT: Kerr–de Sitter PROVEN symbolically via K = {proven} (∇₍ₐK_bc₎≡0 for all M,a,Λ).")
    else:
        print("\n  RESULT: neither closed-form candidate reduced to a Killing tensor symbolically here.")
        print("  Kerr–dS stays NUMERICALLY certified in Move A (residual 7.9e-4, four orders below the")
        print("  DESTROYED rung); the rational-Δ_θ symbolic proof is logged as deferred (needs the proper")
        print("  Kerr–NUT–(A)dS Killing tensor, not the Kerr-Schild form). Honest: asserted only when proven.")
    (LEGA / "certify_symbolic_kds.json").write_text(json.dumps(
        {"kerr_desitter_proven_symbolically": bool(proven), "form": proven}, indent=1))
    print("  wrote results/certify_symbolic_kds.json")


if __name__ == "__main__":
    main()
