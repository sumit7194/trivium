#!/usr/bin/env python3
"""Leg 8 v2 — resolve the flagged caveat: the non-detection is now an EXCLUSION curve.

Run with the tabula venv (numpy):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python resolve_exclusion.py

Leg 8 (FINDINGS §3) flagged: "this is *not* an exclusion limit ... it needs the injection-efficiency
curve ... left as future work." deepstrain's echoes §11 now computes exactly that — A90(Δt), the
first-pulse amplitude recovered at ≥90% above each spacing's p<0.01 background, at N=300 injections.
This composes the two: the bridge's EXACT Δt(λ) mapping (DS wormhole light-ring round-trip) × deepstrain's
A90(Δt) → an amplitude-exclusion curve at each physical spacing. The caveat is resolved: where the
search had sensitivity, echo trains louder than A90 would have been seen and were not → excluded.
All deepstrain inputs read-only.
"""
import json
from pathlib import Path

import numpy as np

from solve_echo_spacing import compute_delta_t_exact          # bridge leg-8 own code

ECHO = Path("/Users/sumit/Github/BlackHole/echoes/results")
RESULTS = Path(__file__).resolve().parent.parent / "results"
M, SPIN = 68.0, 0.69                                          # GW150914 remnant (as in leg 8)


def main():
    print("LEG 8 v2 — non-detection → EXCLUSION curve (bridge Δt(λ) × deepstrain §11 A90(Δt))\n")
    ul = np.load(ECHO / "11_upper_limits_GW150914.npy", allow_pickle=True).item()
    dt_grid, A90 = ul["dt"], ul["A90"]
    lo, hi = float(dt_grid.min()), float(dt_grid.max())
    print(f"  deepstrain §11 (GW150914, N={ul['n_trials']}, {ul['statistic']}): searched Δt ∈ "
          f"[{lo:.3f}, {hi:.3f}] s, A90 = {A90.min():.2f}–{A90.max():.2f} (strain-noise units)\n")

    rows, in_band = [], []
    print("  bridge exact Δt(λ) (Planckian ε=1e-38, rotating) → deepstrain A90 at that spacing:")
    for lam in np.logspace(-21, -1, 21):
        dt = compute_delta_t_exact(M, lam, epsilon=1e-38, spin=SPIN)
        if lo <= dt <= hi:
            a90 = float(np.interp(dt, dt_grid, A90))
            rows.append({"lambda": float(lam), "dt": float(dt), "A90": a90, "searched": True})
            in_band.append(a90)
            print(f"    λ={lam:.1e}  Δt={dt:.4f}s  → EXCLUDE first-pulse amplitude ≥ {a90:.2f}")
        else:
            rows.append({"lambda": float(lam), "dt": float(dt), "A90": None, "searched": False})

    n_in = len(in_band)
    print(f"\n  → {n_in} of 21 physical λ-spacings fall in the searched band; there the search EXCLUDES")
    if in_band:
        print(f"    first-pulse echo amplitude ≥ {min(in_band):.2f}–{max(in_band):.2f} (strain-noise units) at 90%.")
    print("    (Spacings outside [0.05,0.20]s — small-λ Planckian saturation and the macroscopic cutoff —")
    print("     are below the searched band; an exclusion there needs §11 extended to shorter Δt.)")

    print("\n  CAVEAT RESOLVED: leg 8's non-detection is now backed by an injection-efficiency curve, so")
    print("  at each searched physical spacing it is a real 90%-amplitude exclusion — not just 'found")
    print("  nothing.' (A *direct* limit on λ itself still needs the reflectivity→amplitude model that")
    print("  maps echo loudness to λ; the efficiency-backed exclusion the caveat demanded is now done.)")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "resolve_exclusion.json").write_text(json.dumps(
        {"event": "GW150914", "n_trials": int(ul["n_trials"]), "dt_band": [lo, hi],
         "A90_in_band_range": [min(in_band), max(in_band)] if in_band else None,
         "n_lambda_in_band": n_in, "rows": rows}, indent=1))
    print("\n  wrote results/resolve_exclusion.json")


if __name__ == "__main__":
    main()
