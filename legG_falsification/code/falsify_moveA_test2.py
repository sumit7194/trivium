#!/usr/bin/env python3
"""Move G / Test 2 — does Move A recover the TRUE spin, or a fixed answer? (generalization)

Run with the tabula (curvature) venv (after export_multispin.py):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python falsify_moveA_test2.py

The distilled Carter coefficients are (1, a², −a², 1) in the order
[c_ptheta2, c_cos2, c_cos2_E2, c_cos2_Lz2_csc2]. So the recovered a² = −c_cos2_E2/c_ptheta2.
If "blind recovery" is real, recovered a² tracks the TRUE a² across spins the distiller never
'expected'. If it outputs a fixed value regardless of input, Move A's recovery is an artifact.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import distill_invariant as di

RESULTS = Path(__file__).resolve().parent.parent / "results"
SPINS = [0.1, 0.3, 0.5, 0.7, 0.9]
RNG = np.random.default_rng(0)


def load(path):
    trajs = json.loads(Path(path).read_text())
    tid, rows = [], []
    for i, tr in enumerate(trajs):
        for (r, th, pr, pth) in tr["samples"]:
            tid.append(i); rows.append((th, pth, tr["E"], tr["Lz"]))
    return np.array(tid), np.array(rows, float)


def recover_a2(tid, meta):
    """Fit the L1 Carter basis; return recovered a² = −c_cos2_E2/c_ptheta2 and the held-out var-ratio."""
    uids = np.unique(tid); RNG.shuffle(uids); cut = int(0.7 * len(uids))
    tr = np.isin(tid, uids[:cut]); te = ~tr
    c = di.fit_combo(tid[tr], di.features(meta, "L1", 0.0)[tr])
    ho = di.evaluate(tid[te], meta[te], "L1", 0.0, c)
    c = c / c[0]                                   # normalize so c_ptheta2 = 1
    return -c[2], ho                               # −c_cos2_E2 = a²


def main():
    print("MOVE G / Test 2 — does the distiller recover the TRUE a² across spins? (generalization)\n")
    print(f"  {'true a':>7} {'true a²':>9} {'recovered a²':>13} {'rel.err':>9} {'var-ratio':>11}")
    rows = []
    for a in SPINS:
        f = RESULTS / f"traj_spin_{a:.1f}.json"
        if not f.exists():
            print(f"  a={a}: missing {f.name} (run export_multispin.py first)"); continue
        tid, meta = load(f)
        rec, ho = recover_a2(tid, meta)
        true = a * a
        rows.append((a, true, rec, ho))
        print(f"  {a:7.1f} {true:9.3f} {rec:13.3f} {abs(rec-true)/true*100:8.1f}% {ho:11.2e}")

    if len(rows) >= 3:
        truths = np.array([r[1] for r in rows]); recs = np.array([r[2] for r in rows])
        corr = np.corrcoef(truths, recs)[0, 1]
        maxerr = np.max(np.abs(recs - truths) / truths)
        tracks = corr > 0.99 and maxerr < 0.1
        print(f"\n  correlation(recovered a², true a²) = {corr:.4f};  max rel.err = {maxerr*100:.1f}%")
        print(f"\n  TEST 2 VERDICT: {'SURVIVED ✅ — recovered a² tracks the true a² (genuine spin recovery, not a fixed answer)' if tracks else 'FALSIFIED ❌ — recovered a² does NOT track the true a²'}")
        (RESULTS / "falsify_moveA_test2.json").write_text(json.dumps(
            {"rows": [{"a": r[0], "true_a2": r[1], "recovered_a2": r[2], "varratio": r[3]} for r in rows],
             "correlation": corr, "max_rel_err": maxerr, "survived": bool(tracks)}, indent=1, default=float))
        print("  wrote results/falsify_moveA_test2.json")


if __name__ == "__main__":
    main()
