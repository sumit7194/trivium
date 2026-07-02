#!/usr/bin/env python3
"""Leg R stage 1 — generate the blind section-series inputs (ansatz venv; see PREREGISTRATION.md).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python generate_series.py

Builds S1–S4 fresh (Kerr regular, Kerr 1:3 island, MN q=0.5 outer, MN q=0.6 2/3-resonance centre; ≥800
y=0 up-crossings each, the frontier detector's N_MIN_TRAJ floor) and copies S5/S6 (MN inner orbit_A/orbit_B)
from ansatz's §104 export vendored in leg J. Output: results/blind_series.json — series only, ground-truth
tags kept in a separate key the detector runner never reads. Reboot-resilient: per-orbit checkpoint.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric
from poincare import section

OUT = Path(__file__).resolve().parent.parent / "results"
CKPT = OUT / "blind_series_ckpt.json"
INNER = Path(__file__).resolve().parents[2] / "legJ_integrability_frontier/results/mn_inner_sections_ansatz.json"
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))

SPECS = {  # tag: (a, q, E, L, x0)
    "S1": (0.5, 0.0, 0.95, 2.8, 5.0),
    "S2": (0.5, 0.0, 0.95, 2.8, 4.5),
    "S3": (0.5, 0.5, 0.95, 2.8, 4.0),
    "S4": (0.9, 0.6, 0.95, 3.0, 7.70),
}


def gen(a, q, E, L, x0, n=810):
    f = build_hamilton_numeric(1.0, a, q)
    val = (-1 - f["W"](x0, 0.0, E, L)) / f["g22"](x0, 0.0, E, L)
    if val <= 0:
        return None
    py = math.sqrt(val)
    pts, drift, _ = section(f, [x0, 0.0, 0.0, py], E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                            n=n, h=0.02, maxst=8_000_000, bounds=BOUNDS)
    return pts, drift


def main():
    OUT.mkdir(exist_ok=True)
    done = json.loads(CKPT.read_text()) if CKPT.exists() else {}
    for tag, (a, q, E, L, x0) in SPECS.items():
        if tag in done:
            print(f"  {tag}: cached ({len(done[tag]['x'])} crossings)", flush=True)
            continue
        print(f"  {tag}: generating (a={a}, q={q}, E={E}, L={L}, x0={x0}) ...", flush=True)
        r = gen(a, q, E, L, x0)
        if r is None:
            print(f"  {tag}: UNBOUND — skipped", flush=True)
            continue
        pts, drift = r
        done[tag] = {"x": [p[0] for p in pts], "px": [p[1] for p in pts], "H_drift": drift}
        CKPT.write_text(json.dumps(done))
        print(f"  {tag}: {len(pts)} crossings, H-drift {drift:.1e}", flush=True)

    inner = json.loads(INNER.read_text())["orbits"]
    done["S5"] = {"x": inner["orbit_A"]["x"], "px": inner["orbit_A"]["px"], "H_drift": inner["orbit_A"]["H_drift"]}
    done["S6"] = {"x": inner["orbit_B"]["x"], "px": inner["orbit_B"]["px"], "H_drift": inner["orbit_B"]["H_drift"]}
    print(f"  S5: {len(done['S5']['x'])} crossings (ansatz §104)   S6: {len(done['S6']['x'])} crossings (ansatz §104)")

    (OUT / "blind_series.json").write_text(json.dumps(
        {"series": {k: {"x": v["x"], "px": v["px"]} for k, v in done.items()},
         "provenance_do_not_read_in_runner": {k: {"H_drift": v.get("H_drift")} for k, v in done.items()}}))
    print(f"\n  wrote results/blind_series.json ({len(done)} series)")


if __name__ == "__main__":
    main()
