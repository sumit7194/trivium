#!/usr/bin/env python3
"""Leg R stage 2 — run tabula's frontier detector BLIND on the bridge's GR section series (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python run_frontier_detector.py

Imports tabula's EXP-9/10 robust detector (script 150, read-only) and feeds it each series from
results/blind_series.json as an UNLABELED trajectory (shape (1, n, 2) = one orbit, (x, p_x) per crossing).
Records dtype, verdict, and the 0-1-test K per series. NO ground-truth labels are read here — the
comparison happens in stage 3 (score_verdicts.py) against the pre-registered table.

Secondary sub-floor diagnostic (pre-registered P3): for any series shorter than their N_MIN_TRAJ=800, also
report the raw zero_one_K (bypassing the abstain gate), explicitly flagged as below tabula's validated
floor — information only, no strong claim.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/SpaceTime/curvature/scripts")
import importlib
s150 = importlib.import_module("150_robust_detector")
s145 = importlib.import_module("145_regime_detector")

OUT = Path(__file__).resolve().parent.parent / "results"


def main():
    blind = json.loads((OUT / "blind_series.json").read_text())["series"]
    print("LEG R stage 2 — tabula robust detector (script 150), blind, on bridge GR section series\n")
    print(f"  {'tag':>4} {'n':>5} {'dtype':>13} {'verdict':>16} {'K (0-1 test)':>13}  info")
    out = {}
    for tag in sorted(blind):
        x = np.asarray(blind[tag]["x"], float)
        px = np.asarray(blind[tag]["px"], float)
        T = np.stack([np.stack([x, px], axis=1)])          # (1, n, 2)
        dtype, verdict, info = s150.detect_robust({"X": T})
        # per-orbit K for the record (their trajectory branch's own statistic, max over decimations)
        K = None
        if len(x) >= 40:
            K = float(max(s145.zero_one_K(x[::r], seed=0) for r in (3, 5, 10)))
        row = {"n": int(len(x)), "dtype": dtype, "verdict": verdict,
               "info": {k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                        for k, v in info.items()}, "K_raw": K}
        if len(x) < s150.N_MIN_TRAJ:
            row["subfloor_note"] = (f"n={len(x)} < tabula's validated floor N_MIN_TRAJ={s150.N_MIN_TRAJ}; "
                                    f"K_raw is information-only (pre-registered P3)")
        out[tag] = row
        kstr = f"{K:.3f}" if K is not None else "—"
        print(f"  {tag:>4} {len(x):>5} {dtype:>13} {str(verdict):>16} {kstr:>13}  "
              f"{ {k: round(v, 3) if isinstance(v, float) else v for k, v in list(info.items())[:3]} }", flush=True)

    (OUT / "frontier_verdicts.json").write_text(json.dumps(out, indent=1))
    print(f"\n  wrote results/frontier_verdicts.json  (verdicts recorded blind; scoring is stage 3)")


if __name__ == "__main__":
    main()
