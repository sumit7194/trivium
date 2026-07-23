#!/usr/bin/env python3
"""K4 — ad-hoc metric surgery essentially never preserves vacuum (the bumpy-BH warning theorem).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python k4_bumpy.py

Gates K4a-K4d frozen in ../PREREGISTRATION.md before this was written. Formalises leg Y's single-metric
check (ansatz §119) into a general obstruction for the deformation family bumpy-black-hole constructions
actually use: multiply g_tt by (1+εh(r)) and leave g_rr alone.

Result: vacuum ⟺ h′ = 0 ⟺ h constant ⟺ pure gauge (exact, all orders in ε). And the postulate's own
hypothesis fails: the Ricci SCALAR can vanish identically while the Ricci TENSOR does not.
"""
import json
import time
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parent.parent / "results"

t, r, th, ph = sp.symbols("t r theta phi", positive=True)
M, eps = sp.symbols("M epsilon", positive=True)
C1, C2 = sp.symbols("C1 C2")
X = [t, r, th, ph]


def ricci(A, B):
    """Exact Ricci tensor of ds² = −A dt² + B dr² + r²dΩ² (Christoffels → Riemann contraction)."""
    g = sp.diag(-A, B, r ** 2, r ** 2 * sp.sin(th) ** 2)
    gi = g.inv()
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b])
                                         - sp.diff(g[b, c], X[d])) for d in range(4)) / 2)
             for c in range(4)] for b in range(4)] for a in range(4)]
    Ric = sp.zeros(4, 4)
    for b in range(4):
        for c in range(4):
            e = 0
            for a in range(4):
                e += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                for d in range(4):
                    e += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = sp.simplify(e)
    return g, Ric


def nonzero_count(Ric):
    return sum(1 for i in range(4) for j in range(4) if sp.simplify(Ric[i, j]) != 0)


def main():
    t0 = time.time()
    print("K4 — ad-hoc metric surgery never preserves vacuum (gates frozen in PREREGISTRATION.md)")
    print("  family: ds² = −f(1+εh(r))dt² + dr²/f + r²dΩ²,  f = 1−2M/r  (g_rr left alone)\n")

    f = 1 - 2 * M / r
    h = sp.Function("h")(r)
    A, B = f * (1 + eps * h), 1 / f
    g, Ric = ricci(A, B)

    # ---- K4d controls
    ric_eps0 = sp.simplify(Ric.subs(eps, 0))
    ctrl_eps0 = (ric_eps0 == sp.zeros(4, 4))
    hc = sp.Symbol("h0")
    _, Ric_const = ricci(f * (1 + eps * hc), 1 / f)
    ctrl_const = (sp.simplify(Ric_const) == sp.zeros(4, 4))
    k4d = ctrl_eps0 and ctrl_const
    print(f"  K4d controls: ε=0 → R_ab≡0? {ctrl_eps0}   h=const → R_ab≡0? {ctrl_const}   "
          f"→ {'PASS ✅' if k4d else 'FAIL ❌ — machinery void'}")

    # ---- K4b the obstruction (exact in ε)
    comb = sp.simplify(Ric[0, 0] / A + Ric[1, 1] / B)
    target = eps * (r - 2 * M) * sp.Derivative(h, r) / (r ** 2 * (1 + eps * h))
    matches = sp.simplify(comb - target.doit()) == 0
    hsol = sp.dsolve(sp.Eq(sp.simplify(comb * r ** 2 * (1 + eps * h) / eps), 0), h)
    k4b = matches and ("C1" in str(hsol.rhs) and not hsol.rhs.has(r))
    print(f"\n  K4b OBSTRUCTION (exact, all orders in ε):")
    print(f"      R_tt/A + R_rr/B = {comb}")
    print(f"      matches ε(r−2M)h′/(r²(1+εh))? {matches}")
    print(f"      ⇒ vacuum requires h′=0; solving gives  {hsol}")
    print(f"      → {'PASS ✅ — vacuum ⟺ h constant ⟺ PURE GAUGE (no nontrivial bumpy vacuum exists)' if k4b else 'FAIL ❌'}")

    # ---- K4a the kill by construction
    print(f"\n  K4a KILL — exact Ricci for sampled ad-hoc profiles h(r):")
    profiles = {"1/r": 1 / r, "1/r^2": 1 / r ** 2, "exp(-r)": sp.exp(-r),
                "gaussian bump exp(-(r-5)^2)": sp.exp(-(r - 5) ** 2), "§119-style 6/r": 6 / r}
    samples = {}
    for name, hp in profiles.items():
        _, Rp = ricci(f * (1 + eps * hp), 1 / f)
        nz = nonzero_count(Rp)
        val = sp.N(Rp[0, 0].subs({M: 1, eps: sp.Rational(1, 10), r: 4, th: sp.pi / 2}), 6)
        samples[name] = {"nonzero_components": int(nz), "R_tt_at_r4": str(val)}
        print(f"    h = {name:28s} nonzero R_ab: {nz}/16   R_tt(M=1,ε=0.1,r=4) = {val}")
    k4a = all(v["nonzero_components"] > 0 for v in samples.values())
    print(f"    → {'PASS ✅ — every ad-hoc profile breaks Ricci-flatness' if k4a else 'FAIL ❌'}")

    # ---- K4c the invariant trap
    print(f"\n  K4c INVARIANT TRAP — can the Ricci SCALAR vanish while R_ab does not?")
    Rs = sp.simplify(sum(g.inv()[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
    Rs1 = sp.simplify(sp.diff(Rs, eps).subs(eps, 0))                     # O(ε) Ricci scalar
    print(f"      O(ε) Ricci scalar R₁ = {Rs1}")
    # hand-derived solution (sympy's dsolve returns a bogus closed form here — verify by substitution)
    h_trap = C1 + C2 * sp.sqrt(r / (r - 2 * M))
    ode_check = sp.simplify(sp.diff(h_trap, r, 2) * r * (2 * M - r) + sp.diff(h_trap, r) * (M - 2 * r))
    verified = (sp.simplify(ode_check) == 0)
    print(f"      claimed solution h = C₁ + C₂·√(r/(r−2M));  substituted into R₁=0 ODE → {ode_check}  "
          f"({'VERIFIED ✅' if verified else 'FAILED ❌'})")
    # Take the pure C2 branch. Reuse the ALREADY-COMPUTED general-h Ricci and substitute h → h_c2
    # (recomputing Christoffels with the sqrt profile makes sympy's simplify thrash).
    h_c2 = sp.sqrt(r / (r - 2 * M))
    Ric1 = sp.Matrix(4, 4, lambda i, j: sp.diff(Ric[i, j], eps).subs(eps, 0))   # O(ε) Ricci, general h
    sub = {sp.Derivative(h, (r, 2)): sp.diff(h_c2, r, 2), sp.Derivative(h, r): sp.diff(h_c2, r), h: h_c2}
    Ric_trap1 = sp.Matrix(4, 4, lambda i, j: sp.simplify(Ric1[i, j].subs(sub).doit()))
    Rs_trap1 = sp.simplify(Rs1.subs(sub).doit())
    scalar_zero = (sp.simplify(Rs_trap1) == 0)
    # a nonzero NUMERIC value proves the component is not identically zero (decisive and instant)
    probe = {M: 1, r: 4, th: sp.pi / 2}
    nz_trap = sum(1 for i in range(4) for j in range(4)
                  if abs(sp.N(Ric_trap1[i, j].subs(probe))) > 1e-12)
    trap_vals = {f"R[{i},{i}]": str(sp.N(Ric_trap1[i, i].subs(probe), 6)) for i in range(4)}
    k4c = verified and scalar_zero and nz_trap > 0
    print(f"      on the C₂ branch:  O(ε) Ricci SCALAR ≡ 0? {scalar_zero}   "
          f"nonzero O(ε) R_ab components at (M=1,r=4): {nz_trap}/16")
    print(f"      diagonal values there: {trap_vals}")
    print(f"      → {'PASS ✅ — R≡0 but R_ab≠0: a vanishing scalar invariant does NOT certify vacuum' if k4c else 'FAIL ❌'}")

    verdict = "KILLED" if (k4a and k4b and k4c and k4d) else "UNDECIDED"
    print(f"\n  K4 {verdict}. The warning theorem, stated plainly:")
    print(f"    (1) multiplying g_tt by (1+εh) with g_rr untouched is vacuum ⟺ h is CONSTANT (pure gauge);")
    print(f"    (2) so every nontrivial 'bumpy' profile of this form has R_ab ≠ 0 — it is NOT a vacuum;")
    print(f"    (3) and checking a scalar invariant is not enough: R ≡ 0 is compatible with R_ab ≠ 0.")

    OUT.mkdir(exist_ok=True)
    (OUT / "k4_bumpy.json").write_text(json.dumps({
        "family": "ds^2 = -f(1+eps*h(r))dt^2 + dr^2/f + r^2 dOmega^2, f = 1-2M/r",
        "K4d_controls": {"eps0_ricci_flat": bool(ctrl_eps0), "h_const_ricci_flat": bool(ctrl_const),
                         "pass": bool(k4d)},
        "K4b_obstruction": {"combination": str(comb), "matches_closed_form": bool(matches),
                            "solution": str(hsol), "pass": bool(k4b)},
        "K4a_samples": samples, "K4a_pass": bool(k4a),
        "K4c_trap": {"O_eps_ricci_scalar": str(Rs1), "solution": str(h_trap),
                     "ode_substitution_check": str(ode_check), "verified": bool(verified),
                     "scalar_zero_on_C2_branch": bool(scalar_zero),
                     "nonzero_Rab_components_at_M1_r4": int(nz_trap),
                     "diagonal_values_at_M1_r4": trap_vals, "pass": bool(k4c)},
        "verdict": verdict, "all_pass": bool(k4a and k4b and k4c and k4d),
        "summary": ("K4 (KILLED): for the deformation family bumpy-BH constructions actually use — multiply "
                    "g_tt by (1+eps*h(r)), leave g_rr alone — the exact identity R_tt/A + R_rr/B = "
                    "eps*(r-2M)*h'/(r^2(1+eps*h)) holds to ALL orders in eps, so the metric is vacuum iff "
                    "h'=0, i.e. iff h is constant (a pure rescaling of t = pure gauge). No nontrivial bumpy "
                    "deformation of this form is ever Ricci-flat, confirmed on five sampled profiles. "
                    "Moreover the postulate's own hypothesis fails: at O(eps) the Ricci SCALAR vanishes on "
                    "the two-parameter family h = C1 + C2*sqrt(r/(r-2M)), and the C2 branch has R = 0 while "
                    "R_ab != 0 — a vanishing scalar invariant does not certify vacuum. (sympy's dsolve "
                    "returns a bogus closed form for that ODE; the solution was hand-derived and verified "
                    "by substitution.) Formalises leg Y / ansatz §119 into a general warning theorem."),
    }, indent=1))
    print(f"\n  wrote results/k4_bumpy.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
