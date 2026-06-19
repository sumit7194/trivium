#!/usr/bin/env python3
"""Move G / Test 2 (data gen) — Kerr geodesics at five spins, for the generalization falsification.

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python export_multispin.py

Generates blind Kerr trajectories at a ∈ {0.1,0.3,0.5,0.7,0.9} (reusing Move A's exact-metric
machinery read-only) so the distiller can be checked for recovering the TRUE a², not a fixed answer.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as ex

RESULTS = Path(__file__).resolve().parent.parent / "results"
SPINS = [0.1, 0.3, 0.5, 0.7, 0.9]


def main():
    RESULTS.mkdir(exist_ok=True)
    for a in SPINS:
        gfun = (lambda aa: (lambda x: ex.g_kerr_newman(x, aa, 0.0)))(a)
        trajs = []
        for (x0, u0) in ex.gen_launches(gfun, (6, 7, 8, 9, 10)):
            out = ex.integrate(gfun, x0, u0, steps=2400, dtau=0.25, r_lo=2.2, r_hi=40.0)
            if out is not None and len(out["samples"]) >= 60:
                trajs.append(out)
        (RESULTS / f"traj_spin_{a:.1f}.json").write_text(json.dumps(trajs))
        print(f"  a={a}: {len(trajs)} bound trajectories")
    print("done")


if __name__ == "__main__":
    main()
