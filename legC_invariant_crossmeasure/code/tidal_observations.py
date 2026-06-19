#!/usr/bin/env python3
"""Move C — ANSATZ SIDE: the frame-randomized tidal field + ansatz's exact invariants.

Run with the ansatz venv:
    /Users/sumit/Github/conjecture_machine/.venv/bin/python tidal_observations.py

For each exact metric it computes the electric tidal tensor E_ij = R_{0i0j} in a static
orthonormal frame (numeric Riemann, read-only on ansatz's numeric track), rotates it by a random
SO(3) frame at every sample (so no coordinate frame is shared — the observation is frame-DEPENDENT),
and pairs it with ansatz's EXACT coordinate-free labels: the Kretschmann scalar K (symbolic, via
gr_engine — the §76 invariant) and the Petrov class (O conformally-flat / D black-hole). Gated by
Schwarzschild (E=(M/r³)diag(−2,1,1)) and de Sitter (E isotropic ∝ Λ)."""
import json
import math
import random
import sys
from pathlib import Path

import sympy as sp

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from numeric_curvature import christoffel_numeric, inv4      # ansatz, read-only
from gr_engine import Geometry                               # ansatz, read-only (exact Kretschmann)

RESULTS = Path(__file__).resolve().parent.parent / "results"
N = 4
RNG = random.Random(0)


# ---- numeric Riemann (the finite-difference companion, extending ansatz's numeric track) ----
def riemann_lower(gfun, x, h=1e-4):
    """R_{abcd} (all lower) numerically: R^a_bcd = ∂_c Γ^a_db − ∂_d Γ^a_cb + ΓΓ − ΓΓ, then lower."""
    G = christoffel_numeric(gfun, x, h)

    def Gsh(d, s):
        xx = list(x); xx[d] += s * h
        return christoffel_numeric(gfun, xx, h)
    dG = [[[[ (Gsh(d, 1)[a][b][c] - Gsh(d, -1)[a][b][c]) / (2 * h)
              for c in range(N)] for b in range(N)] for a in range(N)] for d in range(N)]
    Rup = [[[[ dG[c][a][d][b] - dG[d][a][c][b]
               + sum(G[a][c][e] * G[e][d][b] - G[a][d][e] * G[e][c][b] for e in range(N))
               for d in range(N)] for c in range(N)] for b in range(N)] for a in range(N)]
    g = gfun(x)
    return [[[[ sum(g[a][e] * Rup[e][b][c][d] for e in range(N))
               for d in range(N)] for c in range(N)] for b in range(N)] for a in range(N)]


def tidal_tensor(gfun, x):
    """Electric tidal tensor E_(i)(j) = R_{0i0j} in the static orthonormal frame (diagonal g)."""
    g = gfun(x)
    R = riemann_lower(gfun, x)
    e0 = 1.0 / math.sqrt(-g[0][0])
    es = [1.0 / math.sqrt(g[i][i]) for i in range(1, N)]    # spatial triad norms
    E = [[R[0][i + 1][0][j + 1] * e0 * e0 * es[i] * es[j] for j in range(3)] for i in range(3)]
    return E


def rand_rotation():
    """A random SO(3) rotation via axis-angle (Rodrigues), pure stdlib."""
    ax = [RNG.gauss(0, 1) for _ in range(3)]
    nrm = math.sqrt(sum(a * a for a in ax)); ax = [a / nrm for a in ax]
    th = RNG.uniform(0, 2 * math.pi)
    c, s = math.cos(th), math.sin(th)
    x, y, z = ax
    return [[c + x*x*(1-c),   x*y*(1-c)-z*s, x*z*(1-c)+y*s],
            [y*x*(1-c)+z*s,   c + y*y*(1-c), y*z*(1-c)-x*s],
            [z*x*(1-c)-y*s,   z*y*(1-c)+x*s, c + z*z*(1-c)]]


def rotate(E, Rm):
    M = [[sum(Rm[i][k] * E[k][l] for k in range(3)) for l in range(3)] for i in range(3)]
    return [[sum(M[i][l] * Rm[j][l] for l in range(3)) for j in range(3)] for i in range(3)]


# ---- the metrics: numeric g(x) + symbolic g for the exact Kretschmann label ----
t, r, th, ph = sp.symbols("t r theta phi", real=True)


def g_num_diag(ftt, frr, fthth, fphph):
    return lambda x: [[-ftt(x[1], x[2]) if i == j == 0 else
                       (frr(x[1], x[2]) if i == j == 1 else
                        (fthth(x[1], x[2]) if i == j == 2 else
                         (fphph(x[1], x[2]) if i == j == 3 else 0.0)))
                       for j in range(N)] for i in range(N)]


def make_metrics():
    M, Q, Lam = sp.symbols("M Q Lam", positive=True)
    metrics = {}
    # Minkowski (O)
    metrics["minkowski"] = dict(petrov="O", params=[{}],
        g_sym=sp.diag(-1, 1, r**2, r**2 * sp.sin(th)**2),
        g_num=lambda p: g_num_diag(lambda r, th: 1.0, lambda r, th: 1.0,
                                   lambda r, th: r*r, lambda r, th: r*r*math.sin(th)**2),
        rrange=(3.0, 10.0))
    # de Sitter (O, conformally flat) — static patch
    metrics["de_sitter"] = dict(petrov="O", params=[{"Lam": v} for v in (0.01, 0.03, 0.06)],
        g_sym=sp.diag(-(1 - Lam*r**2/3), 1/(1 - Lam*r**2/3), r**2, r**2*sp.sin(th)**2),
        g_num=lambda p: g_num_diag(lambda r, th: 1 - p["Lam"]*r*r/3, lambda r, th: 1/(1 - p["Lam"]*r*r/3),
                                   lambda r, th: r*r, lambda r, th: r*r*math.sin(th)**2),
        rrange=(2.0, 5.0))
    # Schwarzschild (D)
    metrics["schwarzschild"] = dict(petrov="D", params=[{"M": v} for v in (1.0, 1.5, 2.0)],
        g_sym=sp.diag(-(1 - 2*M/r), 1/(1 - 2*M/r), r**2, r**2*sp.sin(th)**2),
        g_num=lambda p: g_num_diag(lambda r, th: 1 - 2*p["M"]/r, lambda r, th: 1/(1 - 2*p["M"]/r),
                                   lambda r, th: r*r, lambda r, th: r*r*math.sin(th)**2),
        rrange=(4.0, 12.0))
    # Reissner–Nordström (D)
    metrics["reissner_nordstrom"] = dict(petrov="D",
        params=[{"M": 1.0, "Q": v} for v in (0.3, 0.5, 0.7)],
        g_sym=sp.diag(-(1 - 2*M/r + Q**2/r**2), 1/(1 - 2*M/r + Q**2/r**2), r**2, r**2*sp.sin(th)**2),
        g_num=lambda p: g_num_diag(lambda r, th: 1 - 2*p["M"]/r + p["Q"]**2/r**2,
                                   lambda r, th: 1/(1 - 2*p["M"]/r + p["Q"]**2/r**2),
                                   lambda r, th: r*r, lambda r, th: r*r*math.sin(th)**2),
        rrange=(3.5, 12.0))
    return metrics, (M, Q, Lam)


def kretschmann_fn(g_sym, syms, p):
    """Exact Kretschmann from ansatz's gr_engine, evaluated as a function of r (params fixed)."""
    M, Q, Lam = syms
    sub = {M: p.get("M", 1), Q: p.get("Q", 0), Lam: p.get("Lam", 0)}
    K = Geometry(g_sym.subs(sub), [t, r, th, ph]).kretschmann
    return sp.lambdify(r, K, "math")


def main():
    print("MOVE C — frame-randomized tidal field + ansatz exact invariants (ansatz side)\n")
    metrics, syms = make_metrics()

    # GATE: Schwarzschild and de Sitter tidal tensors
    gS = metrics["schwarzschild"]["g_num"]({"M": 1.0})
    ES = tidal_tensor(gS, [0.0, 8.0, math.pi / 2, 0.0])
    exp = 1.0 / 8.0 ** 3
    print(f"  Schwarzschild E(r=8) diag = [{ES[0][0]/exp:.3f}, {ES[1][1]/exp:.3f}, {ES[2][2]/exp:.3f}]·M/r³"
          f"  (expect [−2, 1, 1])")
    gD = metrics["de_sitter"]["g_num"]({"Lam": 0.03})
    ED = tidal_tensor(gD, [0.0, 3.0, math.pi / 2, 0.0])
    print(f"  de Sitter E(r=3) diag = [{ED[0][0]:.4f}, {ED[1][1]:.4f}, {ED[2][2]:.4f}]  (expect isotropic ≈ −Λ/3 = {-0.03/3:.4f})")
    gate = (abs(ES[0][0]/exp + 2) < 0.05 and abs(ES[1][1]/exp - 1) < 0.05
            and abs(ED[0][0] - ED[1][1]) < 1e-3)
    print(f"  gate {'PASSED ✅' if gate else 'FAILED ❌'}\n")

    rows = []
    inst = 0
    for name, spec in metrics.items():
        for p in spec["params"]:
            kfn = kretschmann_fn(spec["g_sym"], syms, p)
            gnum = spec["g_num"](p)
            lo, hi = spec["rrange"]
            for _ in range(40):
                rr = RNG.uniform(lo, hi)
                tt = RNG.uniform(0.5, math.pi - 0.5)
                E = tidal_tensor(gnum, [0.0, rr, tt, 0.0])
                # coordinate-free WEYL magnitude (traceless part) from the EXACT tidal tensor:
                # 0 for Petrov-O (conformally flat), > 0 for Petrov-D. Rotation-invariant label.
                trE = E[0][0] + E[1][1] + E[2][2]
                Et = [[E[i][j] - (trE / 3 if i == j else 0) for j in range(3)] for i in range(3)]
                weyl_mag = sum(Et[i][j] ** 2 for i in range(3) for j in range(3))
                E = rotate(E, rand_rotation())               # frame-randomize the OBSERVATION
                comps = [E[0][0], E[0][1], E[0][2], E[1][1], E[1][2], E[2][2]]
                rows.append({"metric": name, "instance": inst, "petrov": spec["petrov"],
                             "E6": comps, "kretschmann": float(kfn(rr)), "weyl_mag": weyl_mag})
            inst += 1

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "tidal_observations.json").write_text(json.dumps({"gate_ok": gate, "rows": rows}))
    print(f"  wrote {len(rows)} frame-randomized samples over {inst} metric instances "
          f"→ results/tidal_observations.json")


if __name__ == "__main__":
    main()
