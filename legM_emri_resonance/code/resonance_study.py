#!/usr/bin/env python3
"""Leg M (B1 + A3) step 2 — does the Carter constant misbehave AT a resonance? (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python resonance_study.py

Broken integrability concentrates at resonances. The bump has a 1:3 resonance near r_a≈9 (step 1). This
compares, ON vs OFF that resonance, the Carter-constant drift AND the Lyapunov exponent — for the bump and
the Kerr control. If the bump's resonance shows enhanced C₀ drift / chaos that off-resonance orbits don't,
that is the targeted A3 signal and the seed of the EMRI resonance-crossing signature (B1). Reuses
legJ/legM machinery read-only.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legJ_integrability_frontier/code")
sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_eccentric as ex
import export_geodesics as eg
from geodesic_chaos import lyapunov
from compute_freqs import orbit_freqs

OUT = Path(__file__).resolve().parent.parent / "results"
RP, THMIN = 4.5, math.radians(70.0)
RAS = [7.0, 9.0, 13.0]                                     # 9.0 ≈ bump 1:3 resonance; 7/13 off-resonance


def study(label, eps):
    gfun = lambda x, e=eps: eg.g_bumpy(x, ex.A, e)
    rows = []
    for ra in RAS:
        (E, L, Q), res = ex.solve_ELQ(RP, ra, THMIN)
        if res > 1e-7 or Q < 0:
            continue
        x0, u0 = ex.launch(gfun, RP, E, L, Q)
        fr = orbit_freqs(gfun, x0, u0)
        ratio = (fr[0] / fr[1]) if fr else float("nan")
        r = ex.carter_series(gfun, x0, u0)
        if r is None:
            continue
        drift, _ = ex.measures(r["c0s"])
        lyap = lyapunov(gfun, x0, u0, blocks=400)
        on_res = abs(ratio - 1/3) < 0.02
        rows.append({"ra": ra, "ratio": round(ratio, 4), "near_1_3": bool(on_res),
                     "carter_drift": drift, "lyapunov": round(lyap, 4)})
        print(f"  {label:5s} r_a={ra:4.1f}  ω_r/ω_θ={ratio:.4f}{'  ← on 1:3' if on_res else '':10s}  "
              f"Carter drift={drift:.2e}  λ={lyap:.4f}", flush=True)
    return rows


def main():
    print("LEG M (B1+A3) step 2 — Carter drift & Lyapunov, ON vs OFF the bump's 1:3 resonance\n")
    out = {}
    for label, eps in [("Kerr", 0.0), ("bump", 0.35)]:
        out[label] = study(label, eps)
        print()
    # is the bump's near-resonant orbit anomalous?
    bump = out.get("bump", [])
    onr = [r for r in bump if r["near_1_3"]]
    off = [r for r in bump if not r["near_1_3"]]
    print("  ASSESSMENT:")
    if onr and off:
        d_on = max(r["carter_drift"] for r in onr)
        d_off = max(r["carter_drift"] for r in off)
        l_on = max(r["lyapunov"] for r in onr)
        l_off = max(r["lyapunov"] for r in off)
        enhanced = d_on > 1.5 * d_off or l_on > 1.5 * l_off
        print(f"    on-resonance Carter drift {d_on:.2e} vs off {d_off:.2e}; λ on {l_on:.3f} vs off {l_off:.3f}")
        if enhanced:
            print("    → the 1:3 resonance shows ENHANCED Carter drift / Lyapunov: broken integrability bites")
            print("      AT the resonance (the targeted A3 signal; the EMRI resonance-crossing seed).")
        else:
            print("    → no enhancement: the bump's 1:3 is a REGULAR resonance (KAM tori survive, λ at floor),")
            print("      consistent with leg J. The EMRI observable is then the frequency-map SHIFT (step 1:")
            print("      bump near 1:3 vs Kerr near 1:2), not a chaotic resonance.")
    OUT.mkdir(exist_ok=True)
    (OUT / "resonance_study.json").write_text(json.dumps(out, indent=1, default=float))
    print("\n  wrote results/resonance_study.json")


if __name__ == "__main__":
    main()
