#!/usr/bin/env python3
"""Leg R stage 2 (v2) — tabula's robust detector on GR trajectory ENSEMBLES, blind (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python run_frontier_ensembles.py

Feeds each ensemble from results/blind_trajectories.json to tabula's detect_robust (script 150) as
{"kind":"traj", "X": (N_orbits, timesteps, 1)} — the exact format its menu uses. Records dtype, verdict,
and the frac_regular / frac_chaotic readout. NO ground-truth labels here (scoring is stage 3).
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/SpaceTime/curvature/scripts")
import importlib
s150 = importlib.import_module("150_robust_detector")

OUT = Path(__file__).resolve().parent.parent / "results"


def main():
    ens = json.loads((OUT / "blind_trajectories.json").read_text())["ensembles"]
    print("LEG R stage 2 (v2) — tabula robust detector on GR trajectory ensembles, blind\n")
    print(f"  {'class':>6} {'orbits':>7} {'steps':>6} {'dtype':>13} {'verdict':>15}  readout")
    out = {}
    for tag in sorted(ens):
        rows = ens[tag]
        T = np.array([[[v] for v in orbit] for orbit in rows], dtype=float)   # (N, steps, 1)
        dtype, verdict, info = s150.detect_robust({"kind": "traj", "X": T})
        out[tag] = {"n_orbits": int(T.shape[0]), "steps": int(T.shape[1]),
                    "dtype": dtype, "verdict": verdict,
                    "info": {k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                             for k, v in info.items()}}
        rd = {k: round(v, 3) for k, v in info.items() if isinstance(v, (int, float, np.floating))}
        print(f"  {tag:>6} {T.shape[0]:>7} {T.shape[1]:>6} {dtype:>13} {str(verdict):>15}  {rd}", flush=True)
    (OUT / "frontier_ensembles.json").write_text(json.dumps(out, indent=1))
    print(f"\n  wrote results/frontier_ensembles.json")


if __name__ == "__main__":
    main()
