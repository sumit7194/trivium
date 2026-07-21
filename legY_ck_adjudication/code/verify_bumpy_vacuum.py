#!/usr/bin/env python3
"""Leg Y — independent verification of ansatz §119's claim: our 'bumpy' entry is NOT a vacuum spacetime.

    /Users/sumit/Github/conjecture_machine/.venv/bin/python verify_bumpy_vacuum.py

The bridge does not accept a sister's verdict unchecked. ansatz reports bumpy eps=0.35 has R_ab != 0
(R(4,0.3) = -0.0408) while MN q=0.5 is vacuum -> different Segre type -> rigorous INEQUIVALENT.
Recomputed here from the BRIDGE's own delta_metric construction, exactly (no sampling, no FD).
"""
import sys
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
import sympy as sp
from ck_adjudicate import delta_metric, A, r, u

for eps, tag in [(0, "eps=0 control (should be EXACTLY Kerr -> vacuum)"),
                 (sp.Rational(7, 20), "eps=0.35 (leg O/Q's 'bumpy' entry)")]:
    bump = 1 + eps * 6 * u**2 / r
    geo = delta_metric(A, r**2 - 2 * r + A**2, bump=bump)
    Rs = sp.simplify(geo.ricci_scalar)
    zero = (sp.simplify(Rs) == 0)
    print(f"\n  {tag}")
    print(f"     Ricci scalar identically zero? {zero}")
    if not zero:
        val = sp.N(Rs.subs({r: 4, u: sp.Rational(3, 10)}), 6)
        print(f"     R(r=4, u=0.3) = {val}   <- ansatz §119 reports -0.0408")
        Rab = sp.simplify(geo.ricci)
        nz = sum(1 for i in range(4) for j in range(4) if sp.simplify(Rab[i, j]) != 0)
        print(f"     nonzero R_ab components: {nz}/16  -> NOT Ricci-flat")
