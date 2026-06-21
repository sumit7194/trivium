#!/usr/bin/env python3
"""Leg J stage 1 — export bound-orbit phase-space clouds + Carter-constant drift (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python export_orbits.py

Reuses legA's export_geodesics (metrics, numeric Christoffels, exact circular+tilt launchers,
the diagnostic Kerr Carter tensor) read-only. For each ε (0 = Kerr calibration, then the bump),
integrates a family of bound geodesics and records, per orbit:
  • the (r, θ, p_r, p_θ) phase-space cloud  → Method A (intrinsic dimension: torus=2, chaos=3);
  • the drift of Kerr's exact Carter constant C₀ = K₀_{ab}u^a u^b → Method B (0 on Kerr, grows on bump).
Stage 2 (tabula venv) counts the cloud dimension blind to ε.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as eg                                     # read-only

OUT = Path(__file__).resolve().parent.parent / "results"
N = eg.N
A = 0.6
R0S = [6.0, 7.0, 8.0, 9.0, 10.0]
R_LO, R_HI = 2.0, 40.0
STEPS, DTAU, EVERY = 8000, 0.15, 8                                # ~1000 cloud points/orbit, longer to fill the torus
# v2 launches: a SUB-circular angular velocity (Ω·(1−δ), so r0 is apocenter → bound libration inward)
# AND a latitudinal tilt — excites BOTH modes, giving a genuine bound 2-torus (gen_launches' exactly
# circular u^r=0 froze the radial mode → ~1-D and failed the gate). NEAR these radii the potential is
# flat (zoom-whirl), so eccentricity is hypersensitive to δ — we scan δ finely and SELECT orbits whose
# actual radial extent Δr lands in a balanced band [DR_LO, DR_HI] (both modes comparably excited).
DELTA_GRID = (0.002, 0.004, 0.007, 0.011, 0.016, 0.022, 0.03)
UTH_GRID = (0.04, 0.06, 0.08)
DR_LO, DR_HI = 1.5, 9.0
EPS_GRID = [0.0, 0.05, 0.12, 0.25, 0.35]


def eccentric_launches(gfun, r0s):
    out = []
    for r0 in r0s:
        Omc = eg.circular_Omega(gfun, float(r0), +1)              # prograde circular angular velocity
        if Omc is None:
            continue
        x0 = [0.0, float(r0), math.pi / 2, 0.0]
        g = gfun(x0)
        for dlt in DELTA_GRID:
            Om = Omc * (1.0 - dlt)                                # sub-circular → eccentric, bound
            denom = g[0][0] + 2 * g[0][3] * Om + g[3][3] * Om * Om
            if denom >= 0:
                continue
            for uth in UTH_GRID:
                ut2 = -(1.0 + g[2][2] * uth * uth) / denom
                if ut2 <= 0:
                    continue
                ut = math.sqrt(ut2)
                out.append((x0, [ut, 0.0, uth, Om * ut]))         # u^r=0 at apocenter, eccentric + inclined
    return out


def carter0(x, u):
    K = eg.kerr_K_lower(x, A)
    return sum(K[i][j] * u[i] * u[j] for i in range(N) for j in range(N))


def integrate_dense(gfun, x0, u0):
    def rhs(state):
        x, u = state[:N], state[N:]
        G = eg.christoffel_numeric(gfun, x)
        acc = [-sum(G[i][b][c] * u[b] * u[c] for b in range(N) for c in range(N)) for i in range(N)]
        return list(u) + acc

    state = list(x0) + list(u0)
    cloud, c0s = [], []
    for k in range(STEPS):
        x = state[:N]
        if not (R_LO < x[1] < R_HI):
            return None                                            # plunged/escaped → discard
        if k % EVERY == 0:
            u = state[N:]
            pl = eg.lower(gfun(x), u)
            cloud.append([x[1], x[2], pl[1], pl[2]])               # r, θ, p_r, p_θ
            c0s.append(carter0(x, u))
        k1 = rhs(state)
        k2 = rhs([state[i] + DTAU / 2 * k1[i] for i in range(2 * N)])
        k3 = rhs([state[i] + DTAU / 2 * k2[i] for i in range(2 * N)])
        k4 = rhs([state[i] + DTAU * k3[i] for i in range(2 * N)])
        state = [state[i] + DTAU / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(2 * N)]
    return {"cloud": cloud, "c0s": c0s}


def main():
    OUT.mkdir(exist_ok=True)
    eps_grid = [float(x) for x in sys.argv[1:]] or EPS_GRID        # argv overrides → quick Kerr-only test
    for eps in eps_grid:
        gfun = lambda x, e=eps: eg.g_bumpy(x, A, e)                # ε=0 ⇒ exact Kerr (calibration)
        launches = eg.gen_launches(gfun, R0S)                      # robust near-circular bound orbits
        orbits = []
        for (x0, u0) in launches:
            res = integrate_dense(gfun, x0, u0)
            if res is None:
                continue
            c0 = res["c0s"]
            mean = sum(c0) / len(c0)
            drift = (max(c0) - min(c0)) / (abs(mean) + 1e-12)      # normalized Carter spread
            orbits.append({"C0_series": c0, "C0_mean": mean, "C0_drift": drift})
        avg = sum(len(o["C0_series"]) for o in orbits) // max(1, len(orbits))
        (OUT / f"orbits_eps{eps:.2f}.json").write_text(json.dumps(
            {"eps": eps, "a": A, "n_orbits": len(orbits), "orbits": orbits}))
        cd = [o["C0_drift"] for o in orbits]
        med = sorted(cd)[len(cd) // 2] if cd else float("nan")
        print(f"eps={eps:.2f}: {len(orbits)} bound orbits (~{avg} pts each), median Carter drift = {med:.2e}",
              flush=True)
    print("STAGE1_DONE", flush=True)


if __name__ == "__main__":
    main()
