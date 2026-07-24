#!/usr/bin/env python3
"""Leg Z — independent verification of the Jacobian-conjecture counterexample (exact SymPy).

    python3 verify_jacobian.py

Gates Z1/Z2/Z3 frozen in ../PREREGISTRATION.md. The map is Alpöge's degree-7 counterexample on C^3
(disproving the Jacobian conjecture in dim >= 3), transcribed from Tao's digestion (2026-07-21). Verified
exactly: constant Jacobian determinant -2, and a genuine three-point collision. Self-validating — a wrong
transcription breaks a gate rather than passing silently.
"""
import json
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parent.parent / "results"
z1, z2, z3 = sp.symbols("z1 z2 z3")

# --- the counterexample map (transcribed from Tao's digestion; hand-checked at all 3 collisions) ---
F1 = (1 + z1*z2)**3 * z3 + z2**2*(1 + z1*z2)*(4 + 3*z1*z2)
F2 = z2 + 3*z1*(1 + z1*z2)**2 * z3 + 3*z1*z2**2*(4 + 3*z1*z2)
F3 = 2*z1 - 3*z1**2*z2 - z1**3*z3
F = sp.Matrix([F1, F2, F3])
X = sp.Matrix([z1, z2, z3])


def main():
    print("LEG Z — Jacobian-conjecture counterexample, independent verification (gates in PREREGISTRATION.md)\n")

    # ---- Z1: constant Jacobian determinant = -2, identically
    J = F.jacobian(X)
    detJ = sp.expand(J.det())
    z1_ok = sp.simplify(detJ - (-2)) == 0
    print("  Z1 constant nonzero Jacobian:")
    print(f"     det(DF) expanded = {detJ}")
    print(f"     det(DF) − (−2) simplifies to 0 : {z1_ok}   →  {'PASS ✅' if z1_ok else 'FAIL ❌'}")

    # ---- Z2: three distinct points, one image, exactly
    R = sp.Rational
    pts = [(R(0), R(0), R(-1, 4)),
           (R(1), R(-3, 2), R(13, 2)),
           (R(-1), R(3, 2), R(13, 2))]
    imgs = [tuple(sp.nsimplify(c) for c in F.subs({z1: p[0], z2: p[1], z3: p[2]}))
            for p in pts]
    distinct = len({pts[0], pts[1], pts[2]}) == 3
    target = (R(-1, 4), R(0), R(0))
    all_hit = all(img == target for img in imgs)
    z2_ok = distinct and all_hit
    print("\n  Z2 global non-injectivity (exact rational arithmetic):")
    for p, img in zip(pts, imgs):
        print(f"     F{tuple(str(c) for c in p)} = {tuple(str(c) for c in img)}")
    print(f"     three preimages pairwise distinct : {distinct}")
    print(f"     all map to (−1/4, 0, 0)           : {all_hit}   →  {'PASS ✅' if z2_ok else 'FAIL ❌'}")

    # ---- Z3: shape
    deg = sp.Poly(sp.expand(F1), z1, z2, z3).total_degree()
    degs = [sp.Poly(sp.expand(f), z1, z2, z3).total_degree() for f in (F1, F2, F3)]
    z3_ok = (len(X) == 3) and (max(degs) == 7)
    print(f"\n  Z3 shape: F: C^3 → C^3; component degrees {degs}, total degree {max(degs)}"
          f"   →  {'PASS ✅' if z3_ok else 'FAIL ❌'}")

    allpass = z1_ok and z2_ok and z3_ok
    print(f"\n  VERDICT: {'✅ COUNTEREXAMPLE VERIFIED' if allpass else '❌ GATE FAILED — transcription suspect'}"
          f" — a degree-7 self-map of C^3 with constant Jacobian −2 that collides three points.")
    print("  The Jacobian conjecture is false in dimension 3 (hence all dimensions ≥ 3).")
    print("\n  Z4 (framing, not gated): the sharpest instance of 'locally-invertible-everywhere ⇏")
    print("  globally-invertible' — the same inference template as leg X's localization postulate; the")
    print("  conjecture was that template's best case and it failed. Verification of a published result,")
    print("  not a rederivation; no technical transfer into Jacobson's argument is claimed.")

    OUT.mkdir(exist_ok=True)
    (OUT / "jacobian_verify.json").write_text(json.dumps({
        "map": {"F1": str(F1), "F2": str(F2), "F3": str(F3)},
        "det_jacobian": str(detJ), "Z1_pass": bool(z1_ok),
        "collision_points": [tuple(str(c) for c in p) for p in pts],
        "images": [tuple(str(c) for c in img) for img in imgs],
        "distinct": bool(distinct), "common_image": "(-1/4, 0, 0)", "Z2_pass": bool(z2_ok),
        "component_degrees": degs, "total_degree": int(max(degs)), "Z3_pass": bool(z3_ok),
        "verified": bool(allpass),
        "source": "Tao, 'A digestion of the Jacobian conjecture counterexample', 2026-07-21; "
                  "counterexample by L. Alpoge (w/ Claude Fable 5)",
        "verdict": ("Independently verified in exact SymPy: a degree-7 polynomial self-map of C^3 with "
                    "constant Jacobian determinant -2 sends three distinct points to (-1/4,0,0), "
                    "disproving the Jacobian conjecture in dimension >= 3."),
    }, indent=1))
    print("\n  wrote results/jacobian_verify.json")


if __name__ == "__main__":
    main()
