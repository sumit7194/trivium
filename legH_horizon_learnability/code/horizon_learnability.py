#!/usr/bin/env python3
"""Move H — the horizon is a learnability edge: prediction + the bulk/exact hybrid recipe.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python horizon_learnability.py

Emulate a horizon-diverging GR quantity from noisy position, with three emulators (pure-learned,
pure-asymptotic, hybrid), on ansatz's EXACT Schwarzschild and Kerr metrics (read-only), plus a flat
null. Tests: H1 the learned emulator fails AT the horizon (edge≥3× bulk error); H2 the failure tracks
the divergence; H3 the hybrid beats both pure emulators; H4 holds on both metrics.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.neighbors import KNeighborsRegressor

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as ex                       # ansatz exact metric, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"
RNG = np.random.default_rng(0)
NOISE = 0.02


def Q_schwarzschild(r):
    g = np.array([ex.g_kerr_newman([0.0, ri, math.pi/2, 0.0], 0.0, 0.0) for ri in r])
    return 1.0 / np.sqrt(-g[:, 0, 0])                # blueshift factor 1/√(−g_tt) → ∞ at r=2


def Q_kerr(r, a=0.6):
    g = np.array([ex.g_kerr_newman([0.0, ri, math.pi/2, 0.0], a, 0.0) for ri in r])
    return np.sqrt(g[:, 1, 1])                       # √(g_rr)=√(Σ/Δ) → ∞ at the horizon


def Q_flat(r):
    return r.copy()                                  # no divergence (the null control)


SPACES = {
    "schwarzschild": dict(Qfn=Q_schwarzschild, r_h=2.0,            rlo=2.05, rhi=12.0),
    "kerr":          dict(Qfn=Q_kerr,          r_h=1.0+math.sqrt(1-0.36), rlo=1.85, rhi=12.0),
    "flat_null":     dict(Qfn=Q_flat,          r_h=0.0,            rlo=0.05, rhi=12.0),
}


def asymptotic_coeff(Qfn, r_h):
    """Exact leading near-horizon coefficient c in Q ≈ c/√(r−r_h), extracted numerically."""
    eps = 1e-3
    return float(Qfn(np.array([r_h + eps]))[0] * math.sqrt(eps))


def run_space(name, cfg):
    Qfn, r_h = cfg["Qfn"], cfg["r_h"]
    r = RNG.uniform(cfg["rlo"], cfg["rhi"], 8000)
    Q = Qfn(r)
    r_obs = r + NOISE * RNG.standard_normal(r.shape)
    tr = RNG.random(len(r)) < 0.7; te = ~tr

    # pure-learned: kNN on noisy r
    learned = KNeighborsRegressor(15).fit(r_obs[tr, None], Q[tr]).predict(r_obs[te, None])
    # pure-asymptotic: exact leading near-horizon form (everywhere)
    c = asymptotic_coeff(Qfn, r_h) if r_h > 0 else 0.0
    asym = (c / np.sqrt(np.maximum(r_obs[te] - r_h, 1e-6))) if r_h > 0 else np.full(te.sum(), np.nan)
    # hybrid: asymptotic near horizon, learned in the bulk
    r_match = r_h + 0.5 if r_h > 0 else None
    hybrid = learned.copy()
    if r_h > 0:
        near = r_obs[te] <= r_match
        hybrid[near] = c / np.sqrt(np.maximum(r_obs[te][near] - r_h, 1e-6))

    rel = lambda pred: np.abs(pred - Q[te]) / np.maximum(np.abs(Q[te]), 1e-9)
    dist = r[te] - r_h
    dmax = (cfg["rhi"] - r_h)
    edge = dist < (0.25 if r_h > 0 else 0.85 * dmax)            # near-horizon band (or outer, for flat)
    if r_h <= 0:                                                # flat null: "edge" = far-out region
        edge = r[te] > 0.85 * cfg["rhi"]
    bulk = (dist > 0.3 * dmax) & (dist < 0.6 * dmax)

    def eb(pred):
        rr = rel(pred)
        return float(rr[bulk].mean()), float(rr[edge].mean())

    lb, le = eb(learned)
    out = {"learned_bulk": lb, "learned_edge": le, "learned_edge_over_bulk": le / max(lb, 1e-9)}
    if r_h > 0:
        ab, ae = eb(asym); hb, he = eb(hybrid)
        # local-error vs divergence correlation (H2), in the edge band
        rho = spearmanr(rel(learned)[edge], Q[te][edge]).statistic
        out.update({"asym_bulk": ab, "asym_edge": ae, "hybrid_bulk": hb, "hybrid_edge": he,
                    "spearman_err_vs_Q": float(rho),
                    "max_learned": max(lb, le), "max_asym": max(ab, ae), "max_hybrid": max(hb, he)})
    return out


def main():
    print("MOVE H — the horizon is a learnability edge (prediction + hybrid recipe)\n")
    res = {}
    for name, cfg in SPACES.items():
        r = run_space(name, cfg); res[name] = r
        if cfg["r_h"] > 0:
            print(f"  {name:14s}  learned edge/bulk = {r['learned_edge_over_bulk']:5.1f}×   "
                  f"max-err  learned={r['max_learned']:.3f}  asym={r['max_asym']:.3f}  hybrid={r['max_hybrid']:.3f}   "
                  f"(err~Q ρ={r['spearman_err_vs_Q']:+.2f})")
        else:
            print(f"  {name:14s}  learned edge/bulk = {r['learned_edge_over_bulk']:5.1f}×   (flat null — should be ≈1)")

    # verdicts
    bh = ["schwarzschild", "kerr"]
    H1 = all(res[m]["learned_edge_over_bulk"] >= 3 for m in bh)
    H2 = all(res[m]["spearman_err_vs_Q"] >= 0.8 for m in bh)
    H3 = all(res[m]["max_hybrid"] < min(res[m]["max_learned"], res[m]["max_asym"]) for m in bh)
    null_ok = res["flat_null"]["learned_edge_over_bulk"] < 1.5
    print(f"\n  H1 learned fails at horizon (edge≥3× bulk, both metrics): {H1}")
    print(f"  H2 failure tracks the divergence (err~Q, ρ≥0.8):          {H2}")
    print(f"  H3 hybrid beats BOTH pure emulators (both metrics):       {H3}")
    print(f"  flat null shows NO edge failure (control):                {null_ok}")
    ok = H1 and H3 and null_ok
    print(f"\n  VERDICT: {'SUPPORTED ✅ — the horizon is a learnability edge, and the bulk/exact hybrid is the fix' if ok else 'see table'}")

    RESULTS.mkdir(exist_ok=True)
    res["verdicts"] = {"H1": H1, "H2": H2, "H3": H3, "flat_null_ok": null_ok, "supported": ok}
    (RESULTS / "horizon_learnability.json").write_text(json.dumps(res, indent=1, default=float))
    print("  wrote results/horizon_learnability.json")


if __name__ == "__main__":
    main()
