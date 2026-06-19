#!/usr/bin/env python3
"""Move F — curvature or boundary? Isolating the driver of Move E's bulk/edge effect.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python curvature_vs_boundary.py

Same recovery harness in four geometries (the 2×2 of curvature × boundary): give a net the noisy
extrinsic embedding coordinates, recover the exact intrinsic geodesic distance to a fixed
reference, measure relative recovery error in the bulk vs the edge (far end of the distance range).
The sphere (curved, NO boundary) is the cell that separates 'curvature' from 'boundary'.
"""
import json
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

RESULTS = Path(__file__).resolve().parent.parent / "results"
RNG = np.random.default_rng(0)
N = 12000
NOISE = 0.02            # fraction of each space's coordinate spread


def hyperbolic():
    r = RNG.uniform(0.05, 0.95, N); psi = RNG.uniform(-np.pi, np.pi, N)
    emb = np.stack([r * np.cos(psi), r * np.sin(psi)], axis=1)        # Poincaré disk (2D)
    d = 2 * np.arctanh(r)                                             # → ∞ at boundary
    return emb, d, "curved", "boundary"


def sphere():
    z3 = RNG.uniform(-1, 1, N); phi = RNG.uniform(-np.pi, np.pi, N)   # uniform on S²
    s = np.sqrt(1 - z3 ** 2)
    emb = np.stack([s * np.cos(phi), s * np.sin(phi), z3], axis=1)    # S² in R³ (3D)
    d = np.arccos(np.clip(z3, -1, 1))                                 # geodesic to north pole, [0,π]
    return emb, d, "curved", "no_boundary"


def flat_disk():
    r = RNG.uniform(0.05, 3.66, N); psi = RNG.uniform(-np.pi, np.pi, N)   # range matched to hyperbolic
    emb = np.stack([r * np.cos(psi), r * np.sin(psi)], axis=1)
    d = r.copy()                                                     # Euclidean, hard edge at r=R
    return emb, d, "flat", "boundary"


def flat_torus():
    u = RNG.uniform(0, 1, N); v = RNG.uniform(0, 1, N)               # periodic [0,1)²
    # embed the torus flatly into R⁴ (the standard isometric-ish flat embedding via 2 circles)
    emb = np.stack([np.cos(2*np.pi*u), np.sin(2*np.pi*u),
                    np.cos(2*np.pi*v), np.sin(2*np.pi*v)], axis=1) / np.sqrt(2)
    du = np.minimum(u, 1 - u); dv = np.minimum(v, 1 - v)             # toroidal distance to (0,0)
    d = np.sqrt(du ** 2 + dv ** 2)
    return emb, d, "flat", "no_boundary"


def recover_edge_bulk(emb, d):
    """kNN-recover d from noisy embedding; relative error in bulk (mid-range d) vs edge (far end)."""
    scale = emb.std(0).mean()
    emb_obs = emb + NOISE * scale * RNG.standard_normal(emb.shape)
    tr = RNG.random(len(d)) < 0.7; te = ~tr
    sc = StandardScaler().fit(emb_obs[tr])
    Xtr, Xte = sc.transform(emb_obs[tr]), sc.transform(emb_obs[te])
    pred = KNeighborsRegressor(15).fit(Xtr, d[tr]).predict(Xte)
    rel = np.abs(pred - d[te]) / np.maximum(d[te], 1e-6)
    dte = d[te]; dmax = d.max()
    bulk = rel[(dte > 0.3 * dmax) & (dte < 0.6 * dmax)].mean()
    edge = rel[dte > 0.85 * dmax].mean()
    return bulk, edge, edge / max(bulk, 1e-9)


def main():
    print("MOVE F — curvature or boundary? (the 2×2 isolation)\n")
    spaces = {"hyperbolic": hyperbolic, "sphere": sphere,
              "flat_disk": flat_disk, "flat_torus": flat_torus}
    rows = {}
    print(f"  {'space':12} {'curvature':10} {'boundary':12} {'bulk':>7} {'edge':>7} {'edge/bulk':>10}")
    for name, fn in spaces.items():
        emb, d, curv, bnd = fn()
        b, e, ratio = recover_edge_bulk(emb, d)
        rows[name] = {"curvature": curv, "boundary": bnd, "bulk": b, "edge": e, "ratio": ratio}
        print(f"  {name:12} {curv:10} {bnd:12} {b:7.3f} {e:7.3f} {ratio:9.2f}×")

    # the 2×2 read-out
    hyp, sph, fdisk, ftor = (rows[k]["ratio"] for k in ("hyperbolic", "sphere", "flat_disk", "flat_torus"))
    curved_show = hyp > 1.5 and sph > 1.5
    flat_quiet = fdisk <= 1.3 and ftor <= 1.3
    boundary_show = hyp > 1.5 and fdisk > 1.5
    print("\n  2×2 read-out:")
    print(f"    curved cells (hyperbolic {hyp:.2f}×, sphere {sph:.2f}×) show the effect:  {curved_show}")
    print(f"    flat cells (disk {fdisk:.2f}×, torus {ftor:.2f}×) stay quiet:            {flat_quiet}")
    if curved_show and flat_quiet:
        verdict = "CURVATURE — the effect needs curvature; the boundary is incidental (Move E sharpened)."
    elif boundary_show and sph <= 1.3:
        verdict = "BOUNDARY — the effect needs a boundary, not curvature (Move E corrected)."
    elif hyp > 1.5 and sph <= 1.3 and fdisk <= 1.3:
        verdict = "COMBINATION — needs curvature AND a boundary (a conformal/horizon-like edge)."
    else:
        verdict = "MIXED — see the table; neither clean hypothesis fully holds."
    print(f"\n  VERDICT: {verdict}")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "curvature_vs_boundary.json").write_text(json.dumps(
        {"rows": rows, "curved_show": curved_show, "flat_quiet": flat_quiet,
         "verdict": verdict}, indent=1, default=float))
    print("  wrote results/curvature_vs_boundary.json")


if __name__ == "__main__":
    main()
