#!/usr/bin/env python3
"""Leg R stage 1 (v2) — raw geodesic TRAJECTORY ensembles for tabula's regime detector (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python generate_trajectories.py

tabula's robust detector (script 150) consumes raw trajectory ENSEMBLES (N_orbits, timesteps, D) and runs
the 0-1 test per orbit — NOT single Poincaré sections (the v1 mistake: feeding sections returned UNKNOWN +
scrambled K). This generates the representation the detector validated on, for three exact-GR classes whose
ground truth the bridge has independently established:

  C1  Kerr (manko_novikov q=0)          — integrable + regular          → expect EMIT-regular
  C2  MN q=0.5 outer (manko_novikov)    — NON-integrable (illegible §144, no KY leg O) but KAM-REGULAR (leg J)
                                          → expect EMIT-regular  [the off-menu dissociation case]
  C3  Majumdar–Papapetrou di-hole (§79) — chaotic (λ=2.09)              → expect CERTIFY-CHAOS

C1/C2 differ ONLY in q — a controlled integrability comparison at fixed everything else. Records the radial
coordinate time series per orbit (bounded oscillation → the 0-1 test's input). Reboot-resilient: per-orbit
checkpoint. Ground-truth labels live in a separate key the detector runner never reads.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from manko_novikov import manko_novikov
from emri import mn_bound_orbit
from geodesic_chaos import trajectory

OUT = Path(__file__).resolve().parent.parent / "results"
CKPT = OUT / "traj_ckpt.json"
E, L, A = 0.95, 2.8, 0.5
NSTEP, DTAU = 1500, 0.2
X0S = [round(3.8 + 0.18 * k, 3) for k in range(20)]        # 3.80 … 7.22 — 20 bound outer orbits (tori)


def kerr_mn_ensemble(q):
    g = manko_novikov(1.0, A, q)
    rows = []
    for x0 in X0S:
        ic = mn_bound_orbit(1.0, A, q, E, L, x0)
        if ic is None:
            continue
        pos, vel = ic
        path = trajectory(g, pos, vel, dtau=DTAU, steps=NSTEP)
        if len(path) < 900:                                # escaped/plunged — drop
            continue
        rows.append([s[1] for s in path])                  # x-coordinate (prolate radial) time series
    return rows


def dihole_ensemble():
    sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
    import importlib.util
    spec = importlib.util.spec_from_file_location("s79", "/Users/sumit/Github/conjecture_machine/scripts/79_geodesic_chaos.py")
    s79 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s79)
    rows = []
    for i in range(24):
        vy = 0.16 + 0.006 * i                              # perturb through the chaotic sea
        vz = 0.02 + 0.004 * (i % 5)
        xd = [0.0, 2.5, 0.0, 0.0]
        gd = s79.dihole(xd)
        utd = math.sqrt((gd[2][2] * vy * vy + gd[3][3] * vz * vz + 1) / (-gd[0][0]))
        path = trajectory(s79.dihole, xd, [utd, 0.0, vy, vz], dtau=0.15, steps=NSTEP)
        if len(path) < 900:
            continue
        rows.append([s[1] for s in path])                  # X-coordinate time series
        if len(rows) >= 20:
            break
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    done = json.loads(CKPT.read_text()) if CKPT.exists() else {}
    plan = [("C1", "Kerr q=0 (integrable, regular)", lambda: kerr_mn_ensemble(0.0)),
            ("C2", "MN q=0.5 outer (non-integrable, regular)", lambda: kerr_mn_ensemble(0.5)),
            ("C3", "di-hole (chaotic)", dihole_ensemble)]
    for tag, desc, fn in plan:
        if tag in done:
            print(f"  {tag}: cached ({len(done[tag])} orbits)", flush=True)
            continue
        print(f"  {tag}: generating — {desc} ...", flush=True)
        rows = fn()
        done[tag] = rows
        CKPT.write_text(json.dumps(done))
        lens = [len(r) for r in rows]
        print(f"  {tag}: {len(rows)} orbits, {min(lens)}–{max(lens)} steps each", flush=True)

    (OUT / "blind_trajectories.json").write_text(json.dumps({"ensembles": done}))
    print(f"\n  wrote results/blind_trajectories.json ({sum(len(v) for v in done.values())} orbits, 3 classes)")


if __name__ == "__main__":
    main()
