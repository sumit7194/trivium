#!/usr/bin/env python3
"""Move G — falsifying Move A: does the discovery pipeline HALLUCINATE invariants?

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python falsify_moveA.py

Test 1 (negative controls): feed the REAL distiller data with NO conserved quantity (noise,
shuffled p_θ, scrambled trajectory labels). A sound method must return DESTROYED. If it returns
EXISTS, Move A's "blind recovery of the Carter constant" is fitting spurious structure — falsified.
The controls reuse the exact Move A distiller (read-only import); only the INPUT is corrupted.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import distill_invariant as di                     # the real Move A distiller, read-only

LEGA = Path("/Users/sumit/Github/TheBridge/legA_symmetry_discovery/results")
RESULTS = Path(__file__).resolve().parent.parent / "results"
RNG = np.random.default_rng(0)


def load_traj(path):
    trajs = json.loads(Path(path).read_text())
    tid, rows = [], []
    for i, tr in enumerate(trajs):
        for (r, th, pr, pth) in tr["samples"]:
            tid.append(i); rows.append((th, pth, tr["E"], tr["Lz"]))
    return np.array(tid), np.array(rows, float)


def distill(tid, meta):
    """Run the frozen Move A library ladder; return (verdict, best held-out var-ratio)."""
    uids = np.unique(tid); RNG.shuffle(uids)
    cut = int(0.7 * len(uids))
    tr = np.isin(tid, uids[:cut]); te = ~tr
    best = 1e9
    for lib in ("L1", "L2", "L3"):
        for lam in (di.LAM_GRID if lib == "L2" else [0.0]):
            c = di.fit_combo(tid[tr], di.features(meta, lib, lam)[tr])
            ho = di.evaluate(tid[te], meta[te], lib, lam, c)
            best = min(best, ho)
    return ("EXISTS" if best < di.EPS_T else "DESTROYED"), best


def main():
    print("MOVE G / Test 1 — does the discovery pipeline hallucinate invariants? (Move A controls)\n")
    tid, meta = load_traj(LEGA / "traj_kerr.json")

    # baseline (positive control): real Kerr → must be EXISTS (re-confirm the instrument works)
    v0, h0 = distill(tid, meta)
    print(f"  [positive control] real Kerr trajectories      : {v0:9s}  var-ratio={h0:.2e}")

    # 1a NOISE: same shape, pure Gaussian noise (no conserved quantity)
    meta_noise = RNG.standard_normal(meta.shape)
    v1, h1 = distill(tid, meta_noise)

    # 1b SHUFFLE: permute p_θ across timesteps WITHIN each trajectory (break θ–p_θ relation)
    meta_shuf = meta.copy()
    for u in np.unique(tid):
        idx = np.where(tid == u)[0]
        meta_shuf[idx, 1] = meta_shuf[RNG.permutation(idx), 1]
    v2, h2 = distill(tid, meta_shuf)

    # 1c SCRAMBLE: randomly reassign each sample's trajectory label (break per-traj conservation)
    tid_scram = RNG.permutation(tid)
    v3, h3 = distill(tid_scram, meta)

    print(f"  [1a NOISE]   random data, no invariant          : {v1:9s}  var-ratio={h1:.2e}")
    print(f"  [1b SHUFFLE] p_θ shuffled within trajectory      : {v2:9s}  var-ratio={h2:.2e}")
    print(f"  [1c SCRAMBLE] trajectory labels permuted         : {v3:9s}  var-ratio={h3:.2e}")

    halluc = [name for name, v in [("noise", v1), ("shuffle", v2), ("scramble", v3)] if v == "EXISTS"]
    survived = (v0 == "EXISTS") and not halluc
    print(f"\n  positive control recovers the invariant: {v0 == 'EXISTS'}")
    print(f"  negative controls that FALSELY found one: {halluc if halluc else 'none'}")
    print(f"\n  TEST 1 VERDICT: {'SURVIVED ✅ (no hallucination; controls all DESTROYED)' if survived else 'FALSIFIED ❌ — the method found structure in: ' + str(halluc)}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "falsify_moveA_test1.json").write_text(json.dumps(
        {"positive_real_kerr": {"verdict": v0, "varratio": h0},
         "noise": {"verdict": v1, "varratio": h1},
         "shuffle": {"verdict": v2, "varratio": h2},
         "scramble": {"verdict": v3, "varratio": h3},
         "hallucinated_on": halluc, "survived": survived}, indent=1, default=float))
    print("  wrote results/falsify_moveA_test1.json")


if __name__ == "__main__":
    main()
