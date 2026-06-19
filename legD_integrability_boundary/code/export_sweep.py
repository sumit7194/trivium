#!/usr/bin/env python3
"""Move D — ANSATZ SIDE: sweep the deformation ε, emit blind geodesics + SALI chaos index.

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python export_sweep.py

Reuses Move A's validated metric/integration machinery (read-only import). For each ε it
builds the deformed Kerr metric g_tt→g_tt·(1+ε·cos²θ·R0/r) (ε=0 is exact Kerr), integrates
bound geodesics, writes ONLY trajectories (the Move A blindness boundary), and computes SALI
(Smaller ALignment Index) on a handful of orbits as an independent chaos indicator.
"""
import json
import math
import sys
from pathlib import Path

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from numeric_curvature import christoffel_numeric            # ansatz, read-only
sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as ex                                # Move A machinery, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"
N = 4
EPS_GRID = [0.00, 0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35]   # PREREGISTRATION §2 (frozen)
A, R0S, R_LO, R_HI = 0.6, (6, 7, 8, 9, 10), 2.2, 40.0
STEPS, DTAU = 2400, 0.25


def sali(gfun, x0, u0, steps=1600, dtau=DTAU, delta=1e-7):
    """SALI via two deviation vectors carried by nearby geodesics (finite-difference of the
    variational flow): regular orbit ⇒ SALI stays O(1); chaotic ⇒ SALI → 0 exponentially."""
    def rhs(s):
        x, u = s[:N], s[N:]
        G = christoffel_numeric(gfun, x)
        a = [-sum(G[i][b][c] * u[b] * u[c] for b in range(N) for c in range(N))
             for i in range(N)]
        return list(u) + a

    def rk4(s):
        k1 = rhs(s)
        k2 = rhs([s[i] + dtau / 2 * k1[i] for i in range(2 * N)])
        k3 = rhs([s[i] + dtau / 2 * k2[i] for i in range(2 * N)])
        k4 = rhs([s[i] + dtau * k3[i] for i in range(2 * N)])
        return [s[i] + dtau / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(2 * N)]

    ref = list(x0) + list(u0)
    s1 = list(ref); s1[2] += delta                # perturb θ
    s2 = list(ref); s2[6] += delta                # perturb u^θ
    salis = []
    for k in range(steps):
        if not (R_LO < ref[1] < R_HI):
            break
        ref, s1, s2 = rk4(ref), rk4(s1), rk4(s2)
        if k % 20 == 0 and k > 0:
            v1 = [s1[i] - ref[i] for i in range(2 * N)]
            v2 = [s2[i] - ref[i] for i in range(2 * N)]
            n1 = math.sqrt(sum(v * v for v in v1))
            n2 = math.sqrt(sum(v * v for v in v2))
            if n1 < 1e-30 or n2 < 1e-30:
                break
            v1 = [v / n1 for v in v1]
            v2 = [v / n2 for v in v2]
            sp = math.sqrt(sum((v1[i] + v2[i]) ** 2 for i in range(2 * N)))
            sm = math.sqrt(sum((v1[i] - v2[i]) ** 2 for i in range(2 * N)))
            salis.append(min(sp, sm))
            s1 = [ref[i] + delta * v1[i] for i in range(2 * N)]   # renormalize deviations
            s2 = [ref[i] + delta * v2[i] for i in range(2 * N)]
    return min(salis) if salis else float("nan")


def main():
    print("MOVE D — sweeping deformation ε (ansatz side)")
    RESULTS.mkdir(exist_ok=True)
    meta = {"eps_grid": EPS_GRID, "rows": []}
    for eps in EPS_GRID:
        gfun = (lambda e: (lambda x: ex.g_bumpy(x, A, e)))(eps)
        trajs, drifts, salis = [], [], []
        launches = ex.gen_launches(gfun, R0S)
        for j, (x0, u0) in enumerate(launches):
            out = ex.integrate(gfun, x0, u0, steps=STEPS, dtau=DTAU, r_lo=R_LO, r_hi=R_HI)
            if out is None or len(out["samples"]) < 60:
                continue
            trajs.append(out)
            cs = [ex.carter_value(gfun, [0.0, r, th, 0.0], [-out["E"], pr, pth, out["Lz"]], A)
                  for (r, th, pr, pth) in out["samples"]]
            drifts.append((max(cs) - min(cs)) / (max(abs(v) for v in cs) or 1.0))
            if len(salis) < 6:                      # SALI on a handful of orbits per ε
                salis.append(sali(gfun, x0, u0))
        (RESULTS / f"traj_eps{eps:.2f}.json").write_text(json.dumps(trajs))
        med = lambda a: (sorted(a)[len(a) // 2] if a else None)
        row = {"eps": eps, "n_traj": len(trajs),
               "median_kerrCarter_drift": med(drifts),
               "min_SALI": med([s for s in salis if s == s])}
        meta["rows"].append(row)
        print(f"  eps={eps:.2f}: {len(trajs)} orbits  KerrCarter drift={row['median_kerrCarter_drift']:.2e}"
              f"  SALI(med)={row['min_SALI']:.2e}")
    (RESULTS / "sweep_meta.json").write_text(json.dumps(meta, indent=1))
    print("\nwrote results/traj_eps*.json + sweep_meta.json")


if __name__ == "__main__":
    main()
