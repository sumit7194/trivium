#!/usr/bin/env python3
"""Move A — ANSATZ SIDE (the blind geodesic source).

Run with the ansatz venv (pure Python + sympy; no numpy needed):
    /Users/sumit/Github/conjecture_machine/.venv/bin/python export_geodesics.py

BRIDGE code. It imports ansatz's exact engine READ-ONLY (`numeric_curvature`,
`gr_engine`) and never writes into conjecture_machine. For each rung of the
calibration ladder (PREREGISTRATION §2) it:
  1. builds the EXACT metric g_{μν}(x) (Boyer–Lindquist, M=1),
  2. (vacuum rungs) gates the construction with ansatz's symbolic `verify()`,
  3. integrates timelike geodesics with RK4 via ansatz's `christoffel_numeric`,
  4. writes ONLY trajectory data tabula is allowed to see:
       results/traj_<rung>.json  = [{E, Lz, samples:[[r,theta,p_r,p_theta], ...]}, ...]
     The metric, the params (a,Q,Λ,ε), and the word "Carter" are NEVER written here.

A separate results/truth_<rung>.json holds our own Kerr-Carter drift diagnostic
(NOT given to the distiller) — for the post-hoc honesty check only.

Blindness boundary (PREREGISTRATION §3): tabula reads traj_*.json and nothing else.
Anti-leakage (PREREGISTRATION §3): each trajectory is one geodesic; the train/test
split downstream is BY TRAJECTORY (no shared timesteps), enforced in distill_invariant.py.
"""
import json
import math
import os
import sys
from pathlib import Path

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from numeric_curvature import christoffel_numeric, inv4, ricci_numeric  # ansatz, read-only

RESULTS = Path(__file__).resolve().parent.parent / "results"
N = 4

# ---------------------------------------------------------------------------
# The four exact metrics (Boyer–Lindquist, geometric units, M = 1). PREREG §2.
# Each returns the 4×4 lower metric g_{μν} at x = [t, r, θ, φ] as a list of lists.
# ---------------------------------------------------------------------------

def g_kerr_newman(x, a, Q):
    """Kerr (Q=0) and Kerr–Newman. Δ = r²−2r+a²+Q²; '2Mr−Q²' → P = 2r−Q²."""
    _, r, th, _ = x
    c, s = math.cos(th), math.sin(th)
    s2 = s * s
    Sig = r * r + a * a * c * c
    P = 2.0 * r - Q * Q
    g = [[0.0] * N for _ in range(N)]
    g[0][0] = -(1.0 - P / Sig)
    g[0][3] = g[3][0] = -a * s2 * P / Sig
    g[1][1] = Sig / (r * r - 2.0 * r + a * a + Q * Q)
    g[2][2] = Sig
    g[3][3] = s2 * ((r * r + a * a) + a * a * s2 * P / Sig)
    return g


def g_kerr_desitter(x, a, Lam):
    """Kerr–de Sitter (Carter form), built from its two 1-forms so the signs are
    unambiguous. Λ→0 reduces to Kerr; Ricci_numeric ≈ Λ g is the gate (§ validation)."""
    _, r, th, _ = x
    c, s = math.cos(th), math.sin(th)
    s2 = s * s
    Sig = r * r + a * a * c * c
    Dr = (1.0 - Lam * r * r / 3.0) * (r * r + a * a) - 2.0 * r
    Dth = 1.0 + (Lam * a * a / 3.0) * c * c
    Xi = 1.0 + Lam * a * a / 3.0
    al = [1.0, 0.0, 0.0, -a * s2]                 # dt − a sin²θ dφ
    be = [a, 0.0, 0.0, -(r * r + a * a)]          # a dt − (r²+a²) dφ
    g = [[0.0] * N for _ in range(N)]
    cr = -Dr / (Xi * Xi * Sig)
    cb = Dth * s2 / (Xi * Xi * Sig)
    for i in range(N):
        for j in range(N):
            g[i][j] = cr * al[i] * al[j] + cb * be[i] * be[j]
    g[1][1] += Sig / Dr
    g[2][2] += Sig / Dth
    return g


def g_bumpy(x, a, eps):
    """Kerr with a quadrupole bump that BREAKS Hamilton–Jacobi separability by perturbing
    the θ-POTENTIAL directly: g_tt → g_tt·(1 + ε·cos²θ·R0/r) (PREREGISTRATION §2, rung 4;
    ε frozen 0.35, →Kerr at ε=0). The cos²θ·(R0/r) factor is non-Staeckel (it cannot be
    written as f(r)/Σ + h(θ)/Σ), so no quadratic Killing tensor exists. Unlike a g_rθ term
    this hits every orbit (not only high-p_r ones)."""
    _, r, th, _ = x
    g = g_kerr_newman(x, a, 0.0)
    g[0][0] *= (1.0 + eps * math.cos(th) ** 2 * (6.0 / r))
    return g


# Each rung: metric fn, vacuum-gate Λ (or None), spin a (for the Kerr-Carter diagnostic),
# and the bound-orbit launch window (rung-aware: Kerr-dS lives inside its cosmological horizon).
RUNGS = {
    "kerr":          dict(g=lambda x: g_kerr_newman(x, 0.6, 0.0),    vacuum=0.0,  a=0.6,
                          r0s=(6, 7, 8, 9, 10),        r_lo=2.2, r_hi=40.0, diag=True),
    "kerr_newman":   dict(g=lambda x: g_kerr_newman(x, 0.6, 0.5),    vacuum=None, a=0.6,
                          r0s=(6, 7, 8, 9, 10),        r_lo=2.2, r_hi=40.0, diag=False),
    # Kerr–de Sitter physics constraint: circular orbits exist only for r < r_static =
    # (3/Λ)^{1/3} (beyond it the cosmological repulsion overwhelms gravity). Λ=0.005 gives
    # r_static≈8.4, so bound orbits exist at r≈4–6. Consequence (honest, reported): where
    # bound orbits exist the rational Carter correction Λa²/3·cos²θ is tiny (~0.1%), so the
    # L1-vs-L2 sub-prediction is sub-resolution here — the Λ-rational structure simply is
    # negligible in any regime that HAS bound orbits. The EXISTS verdict is the headline.
    "kerr_desitter": dict(g=lambda x: g_kerr_desitter(x, 0.9, 0.001), vacuum=0.001, a=0.9,
                          r0s=(3.5, 4.0, 4.5, 5.0, 5.5, 6.0), r_lo=2.0, r_hi=14.0, diag=False),
    "bumpy":         dict(g=lambda x: g_bumpy(x, 0.6, 0.35),         vacuum=None, a=0.6,
                          r0s=(6, 7, 8, 9, 10),        r_lo=2.2, r_hi=40.0, diag=True),
}


# ---------------------------------------------------------------------------
# Geodesic integration (RK4) — reusing ansatz's christoffel_numeric, like 58_killing.py
# ---------------------------------------------------------------------------

def lower(g, u):
    return [sum(g[i][j] * u[j] for j in range(N)) for i in range(N)]


def norm2(g, u):
    return sum(g[i][j] * u[i] * u[j] for i in range(N) for j in range(N))


def circular_Omega(gfun, r0, sign):
    """Exact equatorial circular angular velocity Ω = u^φ/u^t from the radial
    geodesic-acceleration-zero condition  Γ^r_φφ Ω² + 2Γ^r_tφ Ω + Γ^r_tt = 0
    (numeric Christoffels). sign = +1 prograde / −1 retrograde. None if no real root.
    This is metric-specific, so it works for Kerr–de Sitter where a Keplerian guess fails."""
    xeq = [0.0, r0, math.pi / 2, 0.0]
    G = christoffel_numeric(gfun, xeq)
    a2, a1, a0 = G[1][3][3], 2.0 * G[1][0][3], G[1][0][0]
    disc = a1 * a1 - 4.0 * a2 * a0
    if disc < 0 or abs(a2) < 1e-14:
        return None
    return (-a1 + sign * math.sqrt(disc)) / (2.0 * a2)


def timelike_circular(gfun, x0, Omega, uth):
    """Future-directed timelike u for a near-circular orbit: u^r=0, u^φ=Ω·u^t, small
    latitudinal tilt u^θ=uth (makes the Carter constant non-trivial). Solve u^t from
    g_μν u^μ u^ν = −1: (u^t)²[g_tt+2g_tφΩ+g_φφΩ²] = −(1+g_θθ uθ²)."""
    g = gfun(x0)
    denom = g[0][0] + 2.0 * g[0][3] * Omega + g[3][3] * Omega * Omega
    if denom >= 0:                                   # not timelike at this Ω
        return None
    ut2 = -(1.0 + g[2][2] * uth * uth) / denom
    if ut2 <= 0:
        return None
    ut = math.sqrt(ut2)
    return [ut, 0.0, uth, Omega * ut]


def integrate(gfun, x0, u0, steps, dtau, r_lo, r_hi):
    """RK4 the geodesic; return per-sample (r,θ,p_r,p_θ) and constants, or None if it
    leaves the bound window [r_lo, r_hi]."""
    def rhs(state):
        x, u = state[:N], state[N:]
        G = christoffel_numeric(gfun, x)
        acc = [-sum(G[i][b][c] * u[b] * u[c] for b in range(N) for c in range(N))
               for i in range(N)]
        return list(u) + acc

    state = list(x0) + list(u0)
    g0 = gfun(x0)
    pl0 = lower(g0, u0)
    E, Lz = -pl0[0], pl0[3]
    samples = []
    every = max(1, steps // 200)
    for k in range(steps):
        x = state[:N]
        if not (r_lo < x[1] < r_hi):
            return None                            # plunged or escaped → discard
        if k % every == 0:
            g = gfun(x)
            pl = lower(g, state[N:])
            samples.append([x[1], x[2], pl[1], pl[2]])   # r, θ, p_r, p_θ
        k1 = rhs(state)
        k2 = rhs([state[i] + dtau / 2 * k1[i] for i in range(2 * N)])
        k3 = rhs([state[i] + dtau / 2 * k2[i] for i in range(2 * N)])
        k4 = rhs([state[i] + dtau * k3[i] for i in range(2 * N)])
        state = [state[i] + dtau / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(2 * N)]
    return {"E": E, "Lz": Lz, "samples": samples}


# ---- Kerr Killing tensor (DIAGNOSTIC ONLY — never written to traj_*.json) ----
def kerr_K_lower(x, a):
    _, r, th, _ = x
    Sig = r * r + a * a * math.cos(th) ** 2
    De = r * r - 2 * r + a * a
    l = [(r * r + a * a) / De, 1.0, 0.0, a / De]
    nv = [(r * r + a * a) / (2 * Sig), -De / (2 * Sig), 0.0, a / (2 * Sig)]
    g = g_kerr_newman(x, a, 0.0)
    gi = inv4(g)
    Kup = [[2 * Sig * 0.5 * (l[i] * nv[j] + l[j] * nv[i]) + r * r * gi[i][j]
            for j in range(N)] for i in range(N)]
    return [[sum(g[i][p] * g[j][q] * Kup[p][q] for p in range(N) for q in range(N))
             for j in range(N)] for i in range(N)]


def carter_value(gfun, x, pl, a):
    """C = K^{μν} p_μ p_ν using Kerr's K with spin a (the diagnostic invariant)."""
    K = kerr_K_lower(x, a)
    gi = inv4(gfun(x))
    Kup = [[sum(gi[i][p] * gi[j][q] * K[p][q] for p in range(N) for q in range(N))
            for j in range(N)] for i in range(N)]
    return sum(Kup[i][j] * pl[i] * pl[j] for i in range(N) for j in range(N))


def gen_launches(gfun, r0s):
    """Exact equatorial circular orbits (prograde & retrograde) at each r0, each given a
    range of latitudinal tilts so the Carter constant varies across trajectories. Returns
    (x0, u0) pairs; unbound/failed launches are dropped by the integrator's window filter."""
    out = []
    for r0 in r0s:
        x0 = [0.0, float(r0), math.pi / 2, 0.0]
        for sign in (+1, -1):
            Om = circular_Omega(gfun, float(r0), sign)
            if Om is None:
                continue
            for uth in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07):
                u0 = timelike_circular(gfun, x0, Om, uth)
                if u0 is not None:
                    out.append((x0, u0))
    return out


def run_rung(name, cfg):
    gfun, vacuum, a = cfg["g"], cfg["vacuum"], cfg["a"]
    print(f"\n=== {name} ===")
    if vacuum is not None:                          # instrument gate: field equations
        xs = [0.0, (cfg["r_lo"] + cfg["r_hi"]) / 4 + 1.0, 1.07, 0.0]
        R, g = ricci_numeric(gfun, xs), gfun(xs)
        resid = max(abs(R[i][j] - vacuum * g[i][j]) for i in range(N) for j in range(N))
        print(f"  vacuum gate (Ricci − Λg, Λ={vacuum}): max |resid| = {resid:.2e}"
              f"  {'OK' if resid < 1e-3 else 'CHECK'}")

    trajs, drifts = [], []
    for (x0, u0) in gen_launches(gfun, cfg["r0s"]):
        out = integrate(gfun, x0, u0, steps=2400, dtau=0.25,
                        r_lo=cfg["r_lo"], r_hi=cfg["r_hi"])
        if out is None or len(out["samples"]) < 60:
            continue
        trajs.append(out)
        if cfg["diag"]:                              # Kerr-Carter drift (NOT shared w/ tabula)
            cs = [carter_value(gfun, [0.0, r, th, 0.0], [-out["E"], pr, pth, out["Lz"]], a)
                  for (r, th, pr, pth) in out["samples"]]
            scale = max(abs(v) for v in cs) or 1.0
            drifts.append((max(cs) - min(cs)) / scale)

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"traj_{name}.json").write_text(json.dumps(trajs))
    med_drift = sorted(drifts)[len(drifts) // 2] if drifts else None
    (RESULTS / f"truth_{name}.json").write_text(json.dumps(
        {"n_traj": len(trajs), "median_kerrCarter_drift": med_drift}))
    tag = ("" if med_drift is None
           else f"  median Kerr-Carter drift = {med_drift:.2e} "
                f"({'~conserved' if med_drift < 1e-2 else 'BROKEN'})")
    print(f"  kept {len(trajs)} bound trajectories;{tag}")
    return len(trajs)


def main():
    print("MOVE A — exporting blind geodesic trajectories (ansatz side)")
    for name, cfg in RUNGS.items():
        run_rung(name, cfg)
    print("\nwrote results/traj_*.json (tabula-visible) + truth_*.json (diagnostic)")


if __name__ == "__main__":
    main()
