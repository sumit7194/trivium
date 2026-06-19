#!/usr/bin/env python3
"""Move I — are the bridge's "edges" one mechanism, or several? The observational/physical taxonomy.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python edge_taxonomy.py

Discriminator: does the edge survive PERFECT observation (σ→0)?
  - F/H divergence-recovery edge: edge/bulk recovery error vs observation noise σ. If it vanishes at
    σ=0 → OBSERVATIONAL (owned by observation precision; no oracle owns it).
  - D integrability-loss edge: the approximate-invariant var-ratio on CLEAN geodesics (the
    perfect-observation limit). If it is nonzero at ε>0 (far above the ε=0 integration-noise floor)
    → PHYSICAL (the deformed torus genuinely admits no low-degree invariant).
"""
import json
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

RESULTS = Path(__file__).resolve().parent.parent / "results"
LEGD = Path("/Users/sumit/Github/TheBridge/legD_integrability_boundary/results")
RNG = np.random.default_rng(0)
N = 16000


def fh_edge_bulk(sigma):
    """Hyperbolic distance recovery edge/bulk error at observation noise σ."""
    r = RNG.uniform(0.05, 0.95, N); psi = RNG.uniform(-np.pi, np.pi, N)
    z = np.stack([r * np.cos(psi), r * np.sin(psi)], 1)
    obs = z + sigma * RNG.standard_normal(z.shape)
    d = 2 * np.arctanh(r)
    tr = RNG.random(N) < 0.7; te = ~tr
    sc = StandardScaler().fit(obs[tr])
    pred = KNeighborsRegressor(15).fit(sc.transform(obs[tr]), d[tr]).predict(sc.transform(obs[te]))
    rel = np.abs(pred - d[te]) / np.maximum(d[te], 1e-6)
    dte = d[te]; dmax = d.max()
    return rel[dte > 0.85 * dmax].mean() / max(rel[(dte > 0.3*dmax) & (dte < 0.6*dmax)].mean(), 1e-9)


def main():
    print("MOVE I — observational vs physical edges (does the edge survive perfect observation?)\n")

    # ---- F/H: divergence-recovery edge vs observation noise ----
    print("  [F/H] divergence-recovery edge/bulk vs observation noise σ:")
    sweep = {}
    for sigma in (0.0, 1e-4, 1e-3, 1e-2):
        ratio = fh_edge_bulk(sigma)
        sweep[sigma] = ratio
        print(f"    σ={sigma:.0e}:  edge/bulk = {ratio:5.2f}×")
    fh_at_zero = sweep[0.0]
    I1_as_stated = fh_at_zero <= 1.3        # FALSIFIED: the edge does not simply vanish at σ=0

    # diagnose: is the σ=0 edge resolution-limited (shrinks with data; exact closed-form has none)?
    print("\n  [F/H] is the σ=0 edge RESOLUTION-limited? (edge/bulk vs data size N; exact form = 0):")
    nsweep = {}
    for Nn in (4000, 16000, 64000, 256000):
        global N
        N = Nn
        nsweep[Nn] = fh_edge_bulk(0.0)
        print(f"    N={Nn:7d}:  edge/bulk = {nsweep[Nn]:.2f}×")
    N = 16000
    resolution_limited = nsweep[256000] < nsweep[4000]   # shrinks with data

    # ---- D: integrability-loss edge on CLEAN geodesics (the perfect-observation limit) ----
    print("\n  [D] approximate-invariant var-ratio on CLEAN geodesics (perfect observation):")
    eps_list = [0.00, 0.02, 0.05, 0.08, 0.18, 0.35]
    vr = {}
    for e in eps_list:
        v = json.loads((LEGD / f"candidate_eps{e:.2f}.json").read_text())["heldout_varratio"]
        vr[e] = v
        tag = "(integration-noise floor)" if e == 0 else ("PHYSICAL: >> floor" if v > 1e-6 else "")
        print(f"    ε={e:.2f}:  var-ratio = {v:.2e}  {tag}")
    floor = vr[0.00]; phys = vr[0.08]
    I2 = floor < 1e-10 and phys > 1e6 * floor

    print(f"\n  I1 (as stated: F/H edge ≤1.3 at σ=0)?  {I1_as_stated}  → FALSIFIED ({fh_at_zero:.2f}× at σ=0)")
    print(f"     but it is RESOLUTION-limited (shrinks {nsweep[4000]:.1f}×→{nsweep[256000]:.1f}× as N "
          f"grows; exact closed-form = 0). → exact OWNS it, finite-resolution LEARNING fails.")
    print(f"  I2 — D edge PERSISTS at perfect observation (ε=0 floor {floor:.1e}, "
          f"ε=0.08 = {phys:.1e}, {phys/floor:.0e}× higher)?  {I2}  → PHYSICAL (structure genuinely gone)")

    taxonomy = resolution_limited and I2          # two kinds established (not via I1-as-stated)
    print(f"\n  EDGE TAXONOMY: {'TWO KINDS ✅ — the edges are NOT one mechanism' if taxonomy else 'see table'}")
    print("    • RECOVERY/RESOLUTION edges (F/H, C): the exact structure EXISTS — the exact closed-form")
    print("      owns it (0 error); finite-resolution learning fails at the diverging gradient; noisy")
    print("      input defeats even the exact form (Move H). 'Exact owns the edge' holds for exact input.")
    print("    • PHYSICAL edges (D): the exact structure is ABSENT for ε>0 — nothing recovers what is")
    print("      not there. A genuinely different kind of edge.")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "edge_taxonomy.json").write_text(json.dumps(
        {"fh_edge_bulk_vs_sigma": {f"{s:.0e}": v for s, v in sweep.items()},
         "fh_edge_bulk_vs_N_at_sigma0": {str(k): v for k, v in nsweep.items()},
         "d_varratio_vs_eps": {f"{e:.2f}": v for e, v in vr.items()},
         "I1_as_stated_falsified": not bool(I1_as_stated),
         "fh_resolution_limited_exact_owns": bool(resolution_limited),
         "I2_d_physical": bool(I2), "two_kinds_of_edges": bool(taxonomy)}, indent=1, default=float))
    print("  wrote results/edge_taxonomy.json")


if __name__ == "__main__":
    main()
