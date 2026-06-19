#!/usr/bin/env python3
"""Move G — falsifying THE SPINE: is the bottleneck counter calibrated, or biased toward 2?

Run with the tabula (curvature) venv (torch):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python falsify_spine.py

The spine's headline is "a black hole is a 2-number object", from tabula's bottleneck counter
returning 2 (Kerr) / 1 (Schwarzschild) / 3 (KN). The dangerous failure mode: the counter is just
biased toward small counts, so it would return ~2 for things that are NOT 2-dimensional — making
the agreement meaningless. We feed the EXACT leg-1 instrument synthetic manifolds of KNOWN intrinsic
dimension 1..6 (smooth nonlinear embeddings, like physical observables) and a pure-noise null, and
check whether the recovered count TRACKS the true dimension. Falsified if it collapses toward 2.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/TheBridge/leg1_moduli_count/code")
import count_bottleneck as cb                       # the REAL leg-1 instrument, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"
WIDTHS = (0, 1, 2, 3, 4, 5, 6, 7, 8)                # cap LIFTED from leg-1's (0..4)
SEEDS = (0, 1, 2)
K = 12                                              # observation channels (like physical observables)
N = 4000
TAU = 0.02                                          # the frozen knee threshold


def smooth_embed(d_true, n, rng):
    """A genuine d_true-dimensional manifold: latent z∈R^{d_true} → K channels via a random smooth
    nonlinear map (2-layer tanh MLP with random weights), like physical observables of d_true moduli."""
    z = rng.uniform(0, 1, (n, d_true))
    W1 = rng.standard_normal((d_true, 32)); b1 = rng.standard_normal(32)
    W2 = rng.standard_normal((32, K)); b2 = rng.standard_normal(K)
    h = np.tanh(z @ W1 + b1)
    return (np.tanh(h @ W2 + b2)).astype(np.float64)


def count(X, rng):
    """Run the EXACT leg-1 counter (whitened marginal-R²-gain > 2% knee), widths 0..8."""
    n_train = int(0.7 * len(X))
    p = cb.prep(X, n_train)
    if p is None:
        return 0, {}
    Xtr, Xte = p["white"]
    r2d = {}
    for d in WIDTHS:
        r2d[d] = float(np.mean([cb.train_ae(Xtr, Xte, d, s) for s in SEEDS]))
    # knee rule: number of widths d≥1 whose marginal gain exceeds TAU
    cnt = sum(1 for d in WIDTHS if d >= 1 and (r2d[d] - r2d[d - 1]) > TAU)
    return cnt, r2d


def main():
    print("MOVE G — falsifying the spine: is the bottleneck counter calibrated, or biased toward 2?\n")
    rng = np.random.default_rng(0)
    rows = []
    print(f"  {'true dim':>9} {'counted':>8}   whitened R²(d) 0..8")
    for d_true in (1, 2, 3, 4, 5, 6):
        X = smooth_embed(d_true, N, rng)
        cnt, r2d = count(X, rng)
        rows.append((d_true, cnt))
        r2s = " ".join(f"{r2d[d]:.2f}" for d in WIDTHS)
        flag = "" if cnt == d_true else "  <-- MISCOUNT"
        print(f"  {d_true:9d} {cnt:8d}   {r2s}{flag}")

    # pure-noise null: full-dimensional, should NOT return ~2
    Xn = rng.standard_normal((N, K))
    cnt_noise, r2n = count(Xn, rng)
    print(f"\n  noise null (K={K}, full-dim): counted = {cnt_noise}  "
          f"(should be HIGH, not ~2; biased-to-2 would say ~2)")

    trues = np.array([r[0] for r in rows]); counts = np.array([r[1] for r in rows])
    # where does it track, and where does it saturate?
    tracks_to = max([d for d, c in rows if c == d], default=0)
    corr = np.corrcoef(trues, counts)[0, 1]
    collapses = np.all(counts <= 2) and trues.max() >= 4   # the falsifying outcome
    print(f"\n  correlation(counted, true) = {corr:.3f};  tracks exactly up to d = {tracks_to};  "
          f"noise→{cnt_noise}")
    if collapses:
        verdict = "FALSIFIED ❌ — the counter collapses everything toward ~2 (biased; the spine's '2' is an artifact)."
    elif tracks_to >= 3 and cnt_noise > 3:
        verdict = (f"SURVIVED ✅ — the counter TRACKS true dimension up to d={tracks_to} and reports "
                   f"noise as high ({cnt_noise}); '2' for black holes sits in the calibrated range. "
                   f"(Saturation above d={tracks_to} is an honest instrument ceiling, not a 2-bias.)")
    else:
        verdict = f"PARTIAL — tracks to d={tracks_to}; see table for where it breaks."
    print(f"\n  SPINE-COUNTER VERDICT: {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "falsify_spine.json").write_text(json.dumps(
        {"rows": [{"true": int(d), "counted": int(c)} for d, c in rows],
         "noise_null_count": int(cnt_noise), "correlation": float(corr),
         "tracks_exactly_to": int(tracks_to), "collapsed_to_2": bool(collapses),
         "verdict": verdict}, indent=1, default=float))
    print("  wrote results/falsify_spine.json")


if __name__ == "__main__":
    main()
