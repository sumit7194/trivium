#!/usr/bin/env python3
"""Move D — TABULA SIDE: distill the (approximate) invariant blind, for each ε.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python distill_sweep.py

Reuses Move A's frozen library ladder and held-out (split-by-trajectory) conservation metric
(read-only import). Blind: reads only results/traj_eps*.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import distill_invariant as di                     # Move A distiller helpers, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"
EPS_GRID = [0.00, 0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35]
SEED = 0


def load_eps(eps):
    trajs = json.loads((RESULTS / f"traj_eps{eps:.2f}.json").read_text())
    rows = []
    for tid, tr in enumerate(trajs):
        for (r, th, pr, pth) in tr["samples"]:
            rows.append((tid, th, pth, tr["E"], tr["Lz"]))
    return np.array([r[0] for r in rows]), np.array([r[1:] for r in rows], float)


def run_eps(eps):
    tid, meta = load_eps(eps)
    rng = np.random.default_rng(SEED)
    uids = np.unique(tid); rng.shuffle(uids)
    cut = int(0.7 * len(uids))
    tr = np.array([t in set(uids[:cut]) for t in tid]); te = ~tr

    best = None
    for lib in ("L1", "L2", "L3"):
        lams = di.LAM_GRID if lib == "L2" else [0.0]
        lib_best = min(((lib, float(lam), di.fit_combo(tid[tr], di.features(meta, lib, lam)[tr]))
                        for lam in lams),
                       key=lambda z: di.evaluate(tid[te], meta[te], z[0], z[1], z[2]))
        ho = di.evaluate(tid[te], meta[te], lib_best[0], lib_best[1], lib_best[2])
        if best is None or ho < best[3]:
            best = (lib_best[0], lib_best[1], lib_best[2], ho)
        if ho < di.EPS_T:
            best = (lib_best[0], lib_best[1], lib_best[2], ho)
            break

    lib, lam, c, ho = best
    verdict = "EXISTS" if ho < di.EPS_T else "DESTROYED"
    names = ["c_ptheta2", "c_cos2", "c_cos2_E2", "c_cos2_Lz2_csc2"]
    out = {"eps": eps, "library": lib, "lam": lam, "verdict": verdict,
           "heldout_varratio": ho, "coeffs": {n: float(v) for n, v in zip(names, c[:4])},
           "n_traj": len(uids)}
    (RESULTS / f"candidate_eps{eps:.2f}.json").write_text(json.dumps(out, indent=1))
    print(f"  eps={eps:.2f}  {verdict:9s} lib={lib} heldout_varratio={ho:.2e}")
    return out


def main():
    print("MOVE D — distilling (approximate) invariants across ε (tabula side, blind)")
    for eps in EPS_GRID:
        run_eps(eps)
    print("\nwrote results/candidate_eps*.json")


if __name__ == "__main__":
    main()
