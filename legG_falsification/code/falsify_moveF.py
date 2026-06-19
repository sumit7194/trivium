#!/usr/bin/env python3
"""Move G — falsifying Move F and the synthesis.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python falsify_moveF.py

Test 3 — break "metric divergence" as the driver of the bulk/edge effect:
  3a HEMISPHERE          curved (+) + FINITE-metric boundary  → should stay null if F is right
  3b UNBOUNDED-FLAT      flat, unbounded distance, CONSTANT sensitivity → isolates unboundedness
  3c FLAT-DIVERGING      FLAT coords, distance diverges (−log(1−r)) → if it FIRES, curvature is
                         irrelevant and the driver is purely the divergence (sharpens F)
Test 4 — is "exact owns the edge" fundamental or coordinate-dependent? recover the hyperbolic
  distance from the INTRINSIC radius r instead of Euclidean (x,y). If the edge stays hard → the
  divergence is irreducible (survives); if it vanishes → representation-dependent (qualified).
"""
import json
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

RESULTS = Path(__file__).resolve().parent.parent / "results"
RNG = np.random.default_rng(0)
N = 12000
NOISE = 0.02


def edge_bulk(emb, d, noise=NOISE):
    emb = emb if emb.ndim == 2 else emb[:, None]
    scale = emb.std(0).mean()
    obs = emb + noise * scale * RNG.standard_normal(emb.shape)
    tr = RNG.random(len(d)) < 0.7; te = ~tr
    sc = StandardScaler().fit(obs[tr])
    pred = KNeighborsRegressor(15).fit(sc.transform(obs[tr]), d[tr]).predict(sc.transform(obs[te]))
    rel = np.abs(pred - d[te]) / np.maximum(d[te], 1e-6)
    dte = d[te]; dmax = d.max()
    bulk = rel[(dte > 0.3 * dmax) & (dte < 0.6 * dmax)].mean()
    edge = rel[dte > 0.85 * dmax].mean()
    return bulk, edge, edge / max(bulk, 1e-9)


def main():
    print("MOVE G / Tests 3-4 — breaking 'metric divergence' (Move F) and the synthesis\n")
    out = {}

    # baselines (re-confirm)
    r = RNG.uniform(0.05, 0.95, N); psi = RNG.uniform(-np.pi, np.pi, N)
    zhyp = np.stack([r*np.cos(psi), r*np.sin(psi)], 1)
    b, e, hyp = edge_bulk(zhyp, 2*np.arctanh(r)); out["hyperbolic_baseline"] = hyp

    # 3a HEMISPHERE: upper half of S², boundary at equator (finite metric there)
    z3 = RNG.uniform(0, 1, N); phi = RNG.uniform(-np.pi, np.pi, N); s = np.sqrt(1-z3**2)
    emb = np.stack([s*np.cos(phi), s*np.sin(phi), z3], 1)
    _, _, hemi = edge_bulk(emb, np.arccos(np.clip(z3, -1, 1))); out["hemisphere"] = hemi

    # 3b UNBOUNDED-FLAT: flat plane to huge radius (unbounded distance, constant sensitivity)
    rb = RNG.uniform(0.05, 100.0, N); pb = RNG.uniform(-np.pi, np.pi, N)
    embf = np.stack([rb*np.cos(pb), rb*np.sin(pb)], 1)
    _, _, ufl = edge_bulk(embf, rb.copy()); out["unbounded_flat"] = ufl

    # 3c FLAT-DIVERGING: flat coords, but the distance diverges at a fake boundary
    rc = RNG.uniform(0.05, 0.95, N); pc = RNG.uniform(-np.pi, np.pi, N)
    embc = np.stack([rc*np.cos(pc), rc*np.sin(pc)], 1)
    _, _, fdiv = edge_bulk(embc, -np.log(1 - rc)); out["flat_diverging"] = fdiv

    # Test 4: hyperbolic distance recovered from the INTRINSIC radius r (1-D), not (x,y)
    _, _, intr = edge_bulk(r.copy(), 2*np.arctanh(r)); out["hyperbolic_from_intrinsic_r"] = intr

    print(f"  hyperbolic baseline (curved + diverging boundary): edge/bulk = {hyp:.2f}×  (the effect)")
    print(f"  [3a] hemisphere (curved + FINITE boundary):        edge/bulk = {hemi:.2f}×")
    print(f"  [3b] unbounded-flat (flat, constant sensitivity):  edge/bulk = {ufl:.2f}×")
    print(f"  [3c] FLAT but diverging distance (−log(1−r)):       edge/bulk = {fdiv:.2f}×")
    print(f"  [T4] hyperbolic from INTRINSIC r (1-D feature):    edge/bulk = {intr:.2f}×")

    fires = lambda x: x > 1.5
    print("\n  read-out (no result in mind):")
    print(f"    3a hemisphere fires?      {fires(hemi)}  → if True, F is wrong (curvature+boundary, not divergence)")
    print(f"    3b unbounded-flat fires?  {fires(ufl)}  → if True, mere unboundedness causes it")
    print(f"    3c flat-diverging fires?  {fires(fdiv)}  → if True, it is PURELY the divergence (curvature irrelevant)")
    print(f"    T4 edge survives intrinsic coord? {fires(intr)}  → if True, the edge failure is fundamental (divergence), not coordinate-artifact")

    # interpretation
    F_ok = (not fires(hemi)) and (not fires(ufl)) and fires(fdiv)
    print(f"\n  MOVE F: {'SURVIVES & SHARPENS ✅ — it is the metric DIVERGENCE (flat-diverging fires, curvature-only cells do not)' if F_ok else 'see table — a break-attempt fired'}")
    print(f"  SYNTHESIS (exact owns the edge): {'fundamental (divergence irreducible to coordinates)' if fires(intr) else 'representation-dependent — QUALIFIED'}")

    out["interpretation"] = {"F_survives_as_divergence": F_ok, "edge_fundamental": fires(intr)}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "falsify_moveF.json").write_text(json.dumps(out, indent=1, default=float))
    print("  wrote results/falsify_moveF.json")


if __name__ == "__main__":
    main()
