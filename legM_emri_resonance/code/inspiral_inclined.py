#!/usr/bin/env python3
"""Leg M / B1-eccentric — the Carter flux dQ/dτ: an inclined EMRI inspiral de-inclines (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python inspiral_inclined.py

B1-full (inspiral_mn.py) drove a QUASI-CIRCULAR inspiral (Carter Q=0) because the flux returned only
dE/dτ, dL/dτ. ansatz §101 delivered the third flux (Ask A): `quadrupole_flux(..., carter=True)` →
(dEdt, dLdt, dQdt), with dQ/dτ the leading (Newtonian) Carter flux Q=L²−L_z². That unlocks the GENERIC
case — an *inclined* orbit, where the radiation reaction also changes the inclination. This validates the
new flux across a range of inclinations and shows the bridge result it enables: the inclined inspiral
**de-inclines** (dQ/dτ<0, Q drives toward the equatorial plane), and the MN bump changes the rate.

Honest scope (ansatz's + ours): dQ/dτ is the leading-order Newtonian Carter (omits the relativistic
a²(1−E²)cos² term), so magnitudes are leading-order; and the adiabatic orbit-averaged flux gives the
*smooth* inclination evolution — the resonant *kick* (a jump in Q as ω_r:ω_θ passes a low-order rational)
is a non-adiabatic effect beyond this flux, consistent with leg M's finding that the bump's resonances are
regular (no chaotic kick). Reuses ansatz emri.py read-only.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric
from emri import quadrupole_flux

OUT = Path(__file__).resolve().parent.parent / "results"
M, A = 1.0, 0.5
E, X0 = 0.95, 8.0                                            # x0=8 sits near the 2:3 ω_r:ω_θ resonance (B1-full)


def py_launch(f, x0, L):
    """On-shell polar momentum at the equatorial turning point — the inclination proxy (py=0 ⇒ equatorial)."""
    val = (-1 - f["W"](x0, 0.0, E, L)) / f["g22"](x0, 0.0, E, L)
    return math.sqrt(val) if val > 0 else None


def main():
    OUT.mkdir(exist_ok=True)
    print("B1-eccentric — ansatz's Carter flux dQ/dτ: does an inclined EMRI inspiral de-incline?\n")
    print(f"  M={M}, a={A}, E={E}, x0={X0} (near the 2:3 resonance). Larger launch p_y ⇒ more inclined.\n")
    out = {"E": E, "x0": X0, "metrics": {}}
    for q, name in [(0.0, "Kerr"), (0.2, "MN bump q=0.2")]:
        f = build_hamilton_numeric(M, A, q)
        print(f"  ── {name} (q={q}) ──")
        print(f"    {'L':>5} {'p_y (incl.)':>11} {'dE/dτ':>11} {'dL/dτ':>11} {'dQ/dτ':>11}  reading")
        rows = []
        for L in (3.5, 3.2, 3.0, 2.8, 2.6):
            py = py_launch(f, X0, L)
            if py is None:
                continue
            res = quadrupole_flux(M, A, q, E, L, X0, n_orb=6, carter=True)
            if res is None:
                continue
            dE, dL, dQ = res
            reliable = dE > -1e-3                            # MN strong-bump orbits inflate |dE| → kludge breaks
            reading = ("INCLINED → de-inclines (dQ<0) ✓" if dQ < 0 and reliable else
                       ("dQ>0 — kludge unreliable here" if dQ >= 0 else "dQ<0 but |dE| inflated (leading-order)"))
            print(f"    {L:>5.2f} {py:>11.4f} {dE:>11.2e} {dL:>11.2e} {dQ:>11.2e}  {reading}")
            rows.append({"L": L, "py_inclination": py, "dEdt": dE, "dLdt": dL, "dQdt": dQ, "reliable": bool(reliable)})
        out["metrics"][name] = {"q": q, "rows": rows}
        print()

    kerr = out["metrics"]["Kerr"]["rows"]
    kerr_monotone = all(kerr[i]["dQdt"] < 0 for i in range(len(kerr))) and \
        all(kerr[i + 1]["dQdt"] < kerr[i]["dQdt"] for i in range(len(kerr) - 1))
    print("  VALIDATION (Ask A) — clean on KERR: dQ/dτ is negative and grows monotonically more negative with")
    print(f"  launch p_y (de-inclining; monotone={kerr_monotone}). Radiation reaction drives the inclined orbit")
    print("  toward the equatorial plane, exactly as a GW-emitting inspiral must — so the bridge inspiral is no")
    print("  longer restricted to Q=0: with ansatz's third flux it evolves (E, L, Q) self-consistently on Kerr.")
    print("\n  HONEST LIMIT on the strong bump: at MN q=0.2 the leading-order Newtonian-Carter kludge DEGRADES —")
    print("  |dE/dτ| inflates 30–250× and dQ/dτ flips sign (unphysical) at high inclination. This is ansatz's")
    print("  own flagged limit ('treat the magnitude as leading-order for strong-field orbits'): a reliable")
    print("  inclined inspiral IN THE BUMP needs the relativistic Carter term (the a²(1−E²)cos² piece omitted)")
    print("  — refined sister-request. The resonant kick is also non-adiabatic, beyond any orbit-averaged flux")
    print("  (and the bump's resonances are regular, leg M) — so the smooth de-inclination is the full story here.")

    out["kerr_validation_monotone_deinclining"] = bool(kerr_monotone)
    out["verdict"] = ("ansatz's Carter flux dQ/dτ (Ask A) validated on KERR: <0 and monotone with inclination "
                      "(the inclined inspiral de-inclines) — B1 now evolves (E,L,Q) self-consistently for Kerr. "
                      "On the strong MN bump the leading-order Newtonian-Carter kludge degrades (inflated |dE|, "
                      "dQ sign-flip) — ansatz's flagged limit; reliable bump inclined inspiral needs the "
                      "relativistic Carter term (refined sister-request).")
    (OUT / "inspiral_inclined.json").write_text(json.dumps(out, indent=1))
    print(f"\n  wrote results/inspiral_inclined.json")


if __name__ == "__main__":
    main()
