#!/usr/bin/env python3
"""Leg H (A7) — does the hybrid recipe (H3) work for a STRONGER divergence? (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python strong_divergence.py

leg H found H3 (the asymptotic+learned HYBRID beats both pure emulators) FAILS for the MILD 1/√(r−r_h)
divergences (blueshift, √g_rr) — there the learned emulator's edge error and the asymptotic's own error are
comparable, so the hybrid can't win. leg H predicted the recipe "would plausibly help only for a stronger
divergence." This tests it: g_rr = r/(r−2) diverges as 1/(r−r_h) (exponent −1, far stronger). Reproduces the
mild case as a control, then the strong case. If H3 flips to TRUE for the strong divergence, the recipe is
vindicated where it matters.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.neighbors import KNeighborsRegressor

OUT = Path(__file__).resolve().parent.parent / "results"
RNG = np.random.default_rng(0)
NOISE = 0.05
A = 0.6


def Q_mild(r):       # Schwarzschild blueshift 1/√(−g_tt) → 1/√(r−2) (exponent −1/2)
    return 1.0 / np.sqrt(np.maximum(1 - 2 / r, 1e-12))


def Q_strong(r):     # Schwarzschild g_rr = r/(r−2) → 1/(r−2) (exponent −1, STRONG)
    return r / np.maximum(r - 2, 1e-12)


def Q_kerr_strong(r):  # Kerr equatorial g_rr = r²/Δ → 1/(r−r_h) (exponent −1, STRONG)
    return r**2 / np.maximum(r**2 - 2 * r + A**2, 1e-12)


SPACES = {
    "Schw mild 1/√  (control)": dict(Qfn=Q_mild,        r_h=2.0,                    p=0.5, rlo=2.05, rhi=12.0),
    "Schw strong 1/Δ":          dict(Qfn=Q_strong,      r_h=2.0,                    p=1.0, rlo=2.05, rhi=12.0),
    "Kerr strong 1/Δ":          dict(Qfn=Q_kerr_strong, r_h=1 + math.sqrt(1 - A**2), p=1.0, rlo=1.85, rhi=12.0),
}


def run(cfg, noise=NOISE):
    Qfn, r_h, p = cfg["Qfn"], cfg["r_h"], cfg["p"]
    r = RNG.uniform(cfg["rlo"], cfg["rhi"], 8000)
    Q = Qfn(r)
    r_obs = r + noise * RNG.standard_normal(r.shape)
    tr = RNG.random(len(r)) < 0.7; te = ~tr
    learned = KNeighborsRegressor(15).fit(r_obs[tr, None], Q[tr]).predict(r_obs[te, None])
    eps = 1e-4
    c = float(Qfn(np.array([r_h + eps]))[0] * eps**p)          # exact leading coeff for exponent p
    asym = c / np.maximum(r_obs[te] - r_h, 1e-6) ** p
    hybrid = learned.copy()
    near = r_obs[te] <= r_h + 0.5
    hybrid[near] = c / np.maximum(r_obs[te][near] - r_h, 1e-6) ** p

    rel = lambda pred: np.abs(pred - Q[te]) / np.maximum(np.abs(Q[te]), 1e-9)
    dist = r[te] - r_h; dmax = cfg["rhi"] - r_h
    edge = dist < 0.25; bulk = (dist > 0.3 * dmax) & (dist < 0.6 * dmax)
    eb = lambda pr: (float(rel(pr)[bulk].mean()), float(rel(pr)[edge].mean()))
    (lb, le), (ab, ae), (hb, he) = eb(learned), eb(asym), eb(hybrid)
    maxl, maxa, maxh = max(lb, le), max(ab, ae), max(hb, he)
    h3 = maxh < maxl and maxh < maxa                           # hybrid beats BOTH pure emulators
    return dict(max_learned=maxl, max_asym=maxa, max_hybrid=maxh, h3_pass=bool(h3),
                edge_over_bulk=le / max(lb, 1e-9))


def main():
    print("LEG H (A7) — hybrid recipe (H3) vs divergence strength\n")
    print(f"  {'space':26s} {'edge/bulk':>9} {'max-err: learned':>17} {'asym':>7} {'hybrid':>7}  H3 (hybrid<both)?")
    out = {}
    for name, cfg in SPACES.items():
        r = run(cfg); out[name] = r
        print(f"  {name:26s} {r['edge_over_bulk']:>8.1f}× {r['max_learned']:>17.3f} {r['max_asym']:>7.3f} "
              f"{r['max_hybrid']:>7.3f}  {'✅ PASS' if r['h3_pass'] else '❌ fail'}")
    # noise sweep on the STRONG Schwarzschild divergence — the real bottleneck is observation noise:
    # the exact asymptotic at noisy r is noise-amplified near r_h, so H3 should flip only at low noise.
    print(f"\n  NOISE SWEEP (Schw strong 1/Δ) — the asymptotic at noisy position is noise-amplified near r_h:")
    print(f"    {'noise':>7} {'max-err: learned':>17} {'asym':>8} {'hybrid':>8}  H3?")
    sweep = {}
    for nz in (0.002, 0.005, 0.01, 0.02, 0.05):
        r = run(SPACES["Schw strong 1/Δ"], noise=nz)
        sweep[nz] = r
        print(f"    {nz:>7.3f} {r['max_learned']:>17.3f} {r['max_asym']:>8.3f} {r['max_hybrid']:>8.3f}  "
              f"{'✅' if r['h3_pass'] else '❌'}")
    flips = [nz for nz, r in sweep.items() if r["h3_pass"]]
    mild = out["Schw mild 1/√  (control)"]["h3_pass"]
    print(f"\n  VERDICT: H3 on the MILD control = {'pass' if mild else 'FAIL (reproduces leg H)'}.")
    if flips:
        print(f"  → For the STRONG divergence, H3 PASSES once observation noise ≤ {max(flips):.3f}: the exact")
        print(f"    near-horizon asymptotic rescues the learned emulator when the divergence is strong AND the")
        print(f"    position is measured well enough. At leg H's noise (0.05) it fails because the asymptotic,")
        print(f"    evaluated at NOISY r, is noise-amplified near r_h (the learned kNN's smoothing is more")
        print(f"    robust). So the recipe's bottleneck is OBSERVATION NOISE, not the asymptotic's form — a")
        print(f"    deeper reason than leg H's mild-case explanation, and a clean regime of validity.")
    else:
        print(f"  → H3 fails across the noise sweep too: the asymptotic-at-noisy-position is noise-amplified")
        print(f"    near the divergence; the learned kNN's smoothing wins. The recipe's bottleneck is")
        print(f"    OBSERVATION NOISE near the divergence, not the functional form — refines leg H's H3.")
    (OUT / "strong_divergence.json").write_text(json.dumps(
        {"spaces": out, "noise_sweep_schw_strong": {str(k): v for k, v in sweep.items()},
         "h3_flips_below_noise": max(flips) if flips else None}, indent=1))
    print("\n  wrote results/strong_divergence.json")


if __name__ == "__main__":
    main()
