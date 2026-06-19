#!/usr/bin/env python3
"""Move A — ANSATZ SIDE (the certifier).

Run with the ansatz venv (pure Python + ansatz's numeric track):
    /Users/sumit/Github/conjecture_machine/.venv/bin/python certify_killing.py

BRIDGE code. Reads ONLY results/candidate_<rung>.json (tabula's distilled coefficients +
library id + λ) and certifies, against ansatz's EXACT metric, whether the reconstructed
object is a genuine Killing tensor: ∇_(a K_bc) = 0. PREREGISTRATION §4B.

Shared feature→tensor convention with distill_invariant.py (coords t,r,θ,φ = 0,1,2,3):
the distilled conserved quantity is
    C = c1·p_θ² + c2·cos²θ + c3·cos²θ·E² + c4·cos²θ·Lz²/sin²θ          (library L1)
or the same over Δ_θ = 1 + λ·cos²θ                                       (library L2),
plus L3's extra [cos⁴θ, p_θ²·cos²θ]. With E=−p_t, Lz=p_φ and the timelike mass shell
g^{μν}p_μp_ν = −1, every term becomes quadratic in p, so C = K^{μν} p_μ p_ν with
    K^{μν} = (1/Δ_θ)[ diag_t(c3 cos²θ) + diag_θ(c1 + c6 cos²θ) + diag_φ(c4 cos²θ/sin²θ)
                      − (c2 cos²θ + c5 cos⁴θ) g^{μν} ]
(c5,c6 = 0 unless library L3). Adding the −(…)g^{μν} piece matters: it is a θ-dependent
multiple of g, not a constant one, so it is part of the genuine Carter tensor.

Certification (numerical, per the §58 pattern and PREREGISTRATION rule 10.0): a true
Killing tensor gives residual at the finite-difference floor; a false one gives O(1)
relative residual. We report raw max|∇_(a K_bc)|, the metric-scale-normalized residual,
and (for cross-check) the residual of the EXACT Kerr K as the FD floor reference.
"""
import json
import math
import random
import sys
from pathlib import Path

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from numeric_curvature import christoffel_numeric, inv4   # ansatz, read-only

sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_geodesics as ex                              # the rung metrics (read-only)

RESULTS = Path(__file__).resolve().parent.parent / "results"
N = 4


def K_upper_from_candidate(cand):
    """Build K^{μν}(x) as a function, from the distilled coefficients (shared convention)."""
    co = cand["coeffs"]
    lib, lam = cand["library"], cand["lam"]
    c1 = co.get("c_ptheta2", 0.0)
    c2 = co.get("c_cos2", 0.0)
    c3 = co.get("c_cos2_E2", 0.0)
    c4 = co.get("c_cos2_Lz2_csc2", 0.0)
    c5 = co.get("c_cos4", 0.0)            # L3 only
    c6 = co.get("c_ptheta2_cos2", 0.0)    # L3 only
    # canonical normalization: scale so the p_θ² coefficient is 1 (Carter convention)
    scale = c1 if abs(c1) > 1e-6 else (math.sqrt(sum(v * v for v in (c1, c2, c3, c4))) or 1.0)
    c1, c2, c3, c4, c5, c6 = (c / scale for c in (c1, c2, c3, c4, c5, c6))

    def Kup(x, gfun):
        _, r, th, _ = x
        c2t = math.cos(th) ** 2
        s2 = math.sin(th) ** 2
        Dth = 1.0 + lam * c2t
        gi = inv4(gfun(x))
        K = [[(-(c2 * c2t + c5 * c2t * c2t) / Dth) * gi[i][j] for j in range(N)]
             for i in range(N)]
        K[0][0] += (c3 * c2t) / Dth                       # tt  (from E²=p_t²)
        K[2][2] += (c1 + c6 * c2t) / Dth                  # θθ  (from p_θ²)
        K[3][3] += (c4 * c2t / s2) / Dth                  # φφ  (from p_φ²)
        return K
    return Kup


def K_lower_fn(Kup, gfun):
    def Kl(x):
        g, Ku = gfun(x), Kup(x, gfun)
        return [[sum(g[i][a] * g[j][b] * Ku[a][b] for a in range(N) for b in range(N))
                 for j in range(N)] for i in range(N)]
    return Kl


def killing_residual(Kl, gfun, x, h=1e-5):
    """max |∇_(a K_bc)| (fully symmetrized), and the K scale at x. Per 58_killing.py."""
    G = christoffel_numeric(gfun, x)

    def dK(d):
        xp, xm = list(x), list(x)
        xp[d] += h
        xm[d] -= h
        Kp, Km = Kl(xp), Kl(xm)
        return [[(Kp[i][j] - Km[i][j]) / (2 * h) for j in range(N)] for i in range(N)]

    dKa = [dK(d) for d in range(N)]
    K = Kl(x)

    def nab(a, b, c):
        return dKa[a][b][c] - sum(G[e][a][b] * K[e][c] + G[e][a][c] * K[b][e]
                                  for e in range(N))
    resid = max(abs(nab(a, b, c) + nab(b, c, a) + nab(c, a, b))
                for a in range(N) for b in range(N) for c in range(N))
    kscale = max(abs(K[i][j]) for i in range(N) for j in range(N))
    return resid, kscale


def sample_points(cfg, n, seed=0):
    rng = random.Random(seed)
    lo, hi = cfg["r0s"][0], cfg["r0s"][-1]
    return [[0.0, rng.uniform(lo, hi), rng.uniform(0.6, 1.5), 0.0] for _ in range(n)]


def main():
    print("MOVE A — certifying distilled candidates as Killing tensors (ansatz side)")
    rows = {}
    for rung, cfg in ex.RUNGS.items():
        cand = json.loads((RESULTS / f"candidate_{rung}.json").read_text())
        gfun = cfg["g"]
        Kup = K_upper_from_candidate(cand)
        Kl = K_lower_fn(Kup, gfun)
        pts = sample_points(cfg, 25)
        rr = [killing_residual(Kl, gfun, p) for p in pts]
        raw = max(r for r, _ in rr)
        ks = sum(k for _, k in rr) / len(rr)
        norm = raw / (ks if ks > 1e-12 else 1.0)
        # FD-floor reference: the EXACT Kerr Carter tensor on the same metric/points
        Kl_exact = lambda x: ex.kerr_K_lower(x, cfg["a"])
        floor = max(killing_residual(Kl_exact, gfun, p)[0] for p in pts)
        fscale = sum(killing_residual(Kl_exact, gfun, p)[1] for p in pts) / len(pts)
        floor_norm = floor / (fscale if fscale > 1e-12 else 1.0)
        verdict = "EXISTS" if norm < 1e-3 else "DESTROYED"
        rows[rung] = dict(raw_resid=raw, K_scale=ks, norm_resid=norm,
                          exact_kerrK_norm_resid=floor_norm, verdict=verdict,
                          tabula_verdict=cand["verdict"], library=cand["library"])
        (RESULTS / f"certify_{rung}.json").write_text(json.dumps(rows[rung], indent=1))
        agree = "AGREE" if verdict == cand["verdict"] else "*** MISMATCH ***"
        print(f"  {rung:14s} norm_resid={norm:.2e}  (Kerr-K floor on this metric "
              f"{floor_norm:.1e})  → ansatz:{verdict:9s} tabula:{cand['verdict']:9s}  {agree}")
    return rows


if __name__ == "__main__":
    main()
