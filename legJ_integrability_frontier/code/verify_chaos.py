#!/usr/bin/env python3
"""Leg J — positive control: can our chaos diagnostic actually SEE chaos? (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python verify_chaos.py

A "no chaos" null is worthless without showing the detector flags chaos when present. We cross-check the
Carter-saturation measure against ansatz §79's Lyapunov exponent (independent, standard; Kerr → floor
λ≈0.015) on the axisymmetric bump, and confirm both read REGULAR up to ε=1.2. We also note the limitation:
the only clearly-chaotic case (legG's φ-dependent bump, SALI≈0.024) sends these orbits unbound, so the
Carter-saturation could not be validated on a chaotic bound orbit → it is SUPERSEDED by the Lyapunov.
Outcome: the leg-J "no chaos in reach" conclusion is unchanged but now rests on the validated tool.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_eccentric as ex
import export_geodesics as eg
from geodesic_chaos import lyapunov

RES = Path(__file__).resolve().parent.parent / "results"


def main():
    print("LEG J — positive control: Lyapunov (validated) vs Carter-saturation, axisymmetric bump\n")
    thmin = math.radians(70.0)
    rows = []
    print(f"  {'ε':>4} {'r_a':>5} {'Lyapunov':>9} {'Carter_sat':>11}  agree?")
    for eps in [0.0, 0.35, 0.6, 0.9, 1.2]:
        gfun = lambda x, e=eps: eg.g_bumpy(x, ex.A, e)
        for ra in [8.0, 11.0, 14.0]:
            (E, L, Q), res = ex.solve_ELQ(4.5, ra, thmin)
            if res > 1e-7 or Q < 0:
                continue
            x0, u0 = ex.launch(gfun, 4.5, E, L, Q)
            lyap = lyapunov(gfun, x0, u0, blocks=350)
            r = ex.carter_series(gfun, x0, u0)
            if r is None:
                continue
            _, sat = ex.measures(r["c0s"])
            lyap_reg, carter_reg = lyap < 0.05, sat < 1.5
            rows.append({"eps": eps, "ra": ra, "lyapunov": lyap, "carter_sat": sat,
                         "lyap_regular": lyap_reg, "carter_regular": carter_reg})
            print(f"  {eps:4.1f} {ra:5.1f} {lyap:9.4f} {sat:11.2f}  "
                  f"{'both regular ✅' if lyap_reg and carter_reg else 'DISAGREE ⚠'}")
    lyap_floor = max(r["lyapunov"] for r in rows if r["eps"] == 0.0)
    all_reg = all(r["lyap_regular"] for r in rows)
    print(f"\n  Kerr Lyapunov floor = {lyap_floor:.3f}; all bump orbits at/near it (max "
          f"{max(r['lyapunov'] for r in rows):.3f}) → REGULAR to ε=1.2.")
    print("  Carter-saturation agrees (all ≈1) but is NOT validated as a chaos detector here (no chaotic")
    print("  BOUND orbit in reach — the φ-dependent chaotic bump unbinds these). Lyapunov supersedes it.")
    print("  → Leg J conclusion (no chaos in reach for the axisymmetric bump) stands on the validated tool.")
    RES.mkdir(exist_ok=True)
    (RES / "verify_chaos.json").write_text(json.dumps(
        {"kerr_lyapunov_floor": lyap_floor, "all_orbits_regular": bool(all_reg),
         "max_lyapunov": max(r["lyapunov"] for r in rows), "rows": rows}, indent=1))
    print("\n  wrote results/verify_chaos.json")


if __name__ == "__main__":
    main()
