#!/usr/bin/env python3
"""Leg J — the DANGEROUS regime: controlled eccentric+inclined orbits, hunting chaos (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python export_eccentric.py

leg J's first pass used near-circular orbits (the stable ones); chaos in a near-integrable system hides at
RESONANCES, reached by eccentric/inclined orbits — which the velocity-kick launches couldn't make (zoom-whirl).
This builds them properly: specify (pericenter r_p, apocenter r_a, inclination θ_min) and solve the Kerr
turning-point conditions R(r_p)=R(r_a)=0, Θ(θ_min)=0 for the constants (E,L,Q) [Schmidt 2002], launch at the
equatorial pericenter (p_r=0, p_θ=√Q), and integrate in BOTH Kerr (calibration) and the bump. A fine scan in
r_a (eccentricity) crosses resonances. Measure Kerr's exact Carter constant C₀: bounded (torus) vs diffusing
(chaos). Reuses legA's export_geodesics (metric, Christoffels, Carter tensor) read-only.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/Users/sumit/Github/TheBridge/legA_symmetry_discovery/code")
import export_geodesics as eg

OUT = Path(__file__).resolve().parent.parent / "results"
N = eg.N
A = 0.6
STEPS, DTAU, EVERY = 10000, 0.15, 10
R_LO, R_HI = 1.5, 60.0


def Delta(r):
    return r * r - 2 * r + A * A


def Rrad(r, E, L, Q):
    return (E * (r * r + A * A) - A * L) ** 2 - Delta(r) * (r * r + (L - A * E) ** 2 + Q)


def Theta(th, E, L, Q):
    c, s = math.cos(th), math.sin(th)
    return Q - c * c * (A * A * (1 - E * E) + L * L / (s * s))


def solve3(J, b):                                       # 3×3 linear solve (Cramer)
    d = (J[0][0]*(J[1][1]*J[2][2]-J[1][2]*J[2][1]) - J[0][1]*(J[1][0]*J[2][2]-J[1][2]*J[2][0])
         + J[0][2]*(J[1][0]*J[2][1]-J[1][1]*J[2][0]))
    if abs(d) < 1e-30:
        return None
    x = []
    for k in range(3):
        Jk = [row[:] for row in J]
        for i in range(3):
            Jk[i][k] = b[i]
        dk = (Jk[0][0]*(Jk[1][1]*Jk[2][2]-Jk[1][2]*Jk[2][1]) - Jk[0][1]*(Jk[1][0]*Jk[2][2]-Jk[1][2]*Jk[2][0])
              + Jk[0][2]*(Jk[1][0]*Jk[2][1]-Jk[1][1]*Jk[2][0]))
        x.append(dk / d)
    return x


def solve_ELQ(rp, ra, thmin):
    def F(v):
        E, L, Q = v
        return [Rrad(rp, E, L, Q), Rrad(ra, E, L, Q), Theta(thmin, E, L, Q)]
    v = [0.95, 3.0, 1.0]
    for _ in range(80):
        f = F(v)
        if max(abs(x) for x in f) < 1e-13:
            break
        Jc = [[0.0]*3 for _ in range(3)]
        for j in range(3):
            dv = v[:]; h = 1e-7*max(1.0, abs(v[j])); dv[j] += h
            fj = F(dv)
            for i in range(3):
                Jc[i][j] = (fj[i] - f[i]) / h
        dx = solve3(Jc, [-x for x in f])
        if dx is None:
            break
        v = [v[i] + dx[i] for i in range(3)]
    return v, max(abs(x) for x in F(v))


def launch(gfun, rp, E, L, Q):
    x0 = [0.0, rp, math.pi/2, 0.0]
    gi = eg.inv4(gfun(x0))
    pl = [-E, 0.0, math.sqrt(max(Q, 0.0)), L]            # p_t=−E, p_r=0 (turning), p_θ=√Q, p_φ=L
    u = [sum(gi[i][j]*pl[j] for j in range(4)) for i in range(4)]
    return x0, u


def carter_series(gfun, x0, u0):
    def rhs(state):
        x, u = state[:N], state[N:]
        G = eg.christoffel_numeric(gfun, x)
        return list(u) + [-sum(G[i][b][c]*u[b]*u[c] for b in range(N) for c in range(N)) for i in range(N)]
    state = list(x0) + list(u0)
    c0s, rmin, rmax, thmax = [], 1e9, -1e9, 0.0
    for k in range(STEPS):
        x = state[:N]
        if not (R_LO < x[1] < R_HI):
            return None
        if k % EVERY == 0:
            u = state[N:]
            K = eg.kerr_K_lower(x, A)
            c0s.append(sum(K[i][j]*u[i]*u[j] for i in range(N) for j in range(N)))
            rmin, rmax = min(rmin, x[1]), max(rmax, x[1])
            thmax = max(thmax, abs(x[2] - math.pi/2))
        k1 = rhs(state)
        k2 = rhs([state[i]+DTAU/2*k1[i] for i in range(2*N)])
        k3 = rhs([state[i]+DTAU/2*k2[i] for i in range(2*N)])
        k4 = rhs([state[i]+DTAU*k3[i] for i in range(2*N)])
        state = [state[i]+DTAU/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(2*N)]
    return {"c0s": c0s, "dr": rmax - rmin, "incl_deg": math.degrees(thmax)}


def measures(c0s):
    n = len(c0s); mean = sum(c0s)/n
    drift = (max(c0s) - min(c0s))/(abs(mean) + 1e-12)
    q = max(2, n//4)
    sat = (max(c0s) - min(c0s))/((max(c0s[:q]) - min(c0s[:q])) + 1e-30)
    return drift, sat


def main():
    OUT.mkdir(exist_ok=True)
    rp, thmin = 4.5, math.radians(70.0)
    ras = [7.0 + 0.5*k for k in range(17)]               # fine eccentricity scan → crosses resonances
    for eps in [0.0, 0.35]:
        gfun = lambda x, e=eps: eg.g_bumpy(x, A, e)
        rows = []
        for ra in ras:
            (E, L, Q), res = solve_ELQ(rp, ra, thmin)
            if res > 1e-8 or Q < 0:
                continue
            x0, u0 = launch(gfun, rp, E, L, Q)
            r = carter_series(gfun, x0, u0)
            if r is None:
                continue
            dr, sat = measures(r["c0s"])
            ecc = (r["dr"]) / (2*rp + r["dr"] + 1e-9)
            rows.append({"ra": ra, "ecc_meas": ecc, "incl_deg": r["incl_deg"],
                         "drift": dr, "sat": sat})
        (OUT / f"eccentric_eps{eps:.2f}.json").write_text(json.dumps({"eps": eps, "rows": rows}, indent=1))
        sats = [x["sat"] for x in rows]
        drs = [x["drift"] for x in rows]
        nd = sum(1 for s in sats if s > 1.5)
        print(f"eps={eps:.2f}: {len(rows)} eccentric orbits  Δr~{rows[0]['ecc_meas']:.2f}-{rows[-1]['ecc_meas']:.2f}ecc "
              f"incl~{rows[0]['incl_deg']:.0f}°  drift[{min(drs):.1e},{max(drs):.1e}]  "
              f"sat[{min(sats):.2f},{max(sats):.2f}]  diffusing(>1.5)={nd}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
