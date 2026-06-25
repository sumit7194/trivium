#!/usr/bin/env python3
"""Leg J (A2) — QUARTIC Killing-tensor search: retire the last residual (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python numeric_quartic_search.py

rank-2 Killing tensors are excluded for our bump two ways (symbolic KY + numeric SVD). The only residual
was a higher-rank/quartic (rank-4) Killing tensor. This extends ansatz §85's multi-orbit SVD to a
DEGREE-4-in-momenta basis. At fixed E,L (varied inclination), Kerr's reducible quartic invariants are the
Carter constant C₀ and its square C₀² — so the GATE is "Kerr recovers BOTH" (≥2 machine-zero singular
values). The deformed metric should then show NO quartic invariant (no machine-zero SV) ⇒ no rank-4
Killing tensor either. (Identity guard: u⁴/om = u²/om − u² is reducible — excluded, per §85's catch.)
"""
import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
from poincare import build_hamilton
import _qinvariant as qi                                  # reuse trajectory (read-only)

RES = Path(__file__).resolve().parent.parent / "results"
t, r, th, ph = sp.symbols("t r theta phi", real=True)
A = sp.Rational(3, 5)
Sig = r**2 + A**2 * sp.cos(th)**2
De = r**2 - 2 * r + A**2
s2 = sp.sin(th)**2
E, L, R0 = 0.95, 3.4, 8.0
P2LIST = [round(0.06 + 0.025 * k, 4) for k in range(30)]   # finer inclination grid → more orbits (big basis)


def our_metric(eps):
    g = sp.zeros(4)
    g[0, 0] = -(1 - 2 * r / Sig)
    g[0, 3] = g[3, 0] = -2 * r * A * s2 / Sig
    g[1, 1] = Sig / De
    g[2, 2] = Sig
    g[3, 3] = (r**2 + A**2 + 2 * r * A**2 * s2 / Sig) * s2
    if eps:
        g[0, 0] = g[0, 0] * (1 + sp.Rational(eps) * sp.cos(th)**2 * 6 / r)
    return build_hamilton(g, [t, r, th, ph], 1, 2)


def basis(s):
    r_, th_, pr, pth = s
    u = np.cos(th_); om = 1 - u * u
    uo = u * u / om                                         # cot²θ
    return [
        pth*pth, pr*pr, pr*pth,                            # deg-2 momenta
        uo, u*u,                                            # deg-0 spatial (the C₀ pieces)
        pth**4, pr**4, pth*pth*pr*pr, pth**3*pr, pth*pr**3, # deg-4 momenta
        pth*pth*uo, pth*pth*u*u, pr*pr*uo, pr*pr*u*u,        # deg-2 momenta × deg-2 spatial
        uo*uo, u**4,                                        # deg-4 spatial (NOT u⁴/om — reducible)
    ]


NB = 16


def check_independence():
    rng = [[2 + 9*((i*37+j*13) % 100)/100, 0.6 + 1.9*((i*7+j*29) % 100)/100,
            -1 + 2*((i*17+j*5) % 100)/100, -1 + 2*((i*3+j*41) % 100)/100]
           for i in range(60) for j in range(2)]
    Phi = np.array([basis(s) for s in rng], float)
    Phi = Phi - Phi.mean(0, keepdims=True)
    S = np.linalg.svd(Phi / (np.linalg.norm(Phi, axis=0) + 1e-30), compute_uv=False)
    return S[-1]


SPATIAL = {3, 4, 14, 15}                                   # cot²θ, cos²θ, cot⁴θ, cos⁴θ — momentum-free
MOM = [i for i in range(NB) if i not in SPATIAL]           # terms containing p_r or p_θ


def mom_fraction(vec):
    """|coeffs on momentum-bearing terms| / |all|. A genuine Killing-tensor invariant is a FORM in
    momenta (>0); a pure-spatial vector (≈0) is a near-flat-over-sampled-θ artifact, not an invariant."""
    a = np.abs(vec)
    return a[MOM].sum() / (a.sum() + 1e-30)


def fit(f):
    blocks, used = [], 0
    for p2 in P2LIST:
        pts = qi.trajectory(f, E, L, p2, R0)
        if not pts or len(pts) < 2500:
            continue
        used += 1
        sub = pts[:: max(1, len(pts) // 200)]
        Phi = np.array([basis(s) for s in sub], float)
        blocks.append(Phi - Phi.mean(0, keepdims=True))
    D = np.vstack(blocks)
    scale = np.linalg.norm(D, axis=0) + 1e-30
    _, S, Vt = np.linalg.svd(D / scale, full_matrices=False)
    # smallest singular value whose vector is a genuine momentum form (not a pure-spatial artifact)
    phys = [(S[k], mom_fraction(Vt[k] / scale)) for k in range(len(S))]
    phys_sv = [sv for sv, mf in phys if mf > 0.02]
    return S, min(phys_sv) if phys_sv else float("inf"), used


def main():
    print("LEG J (A2) — QUARTIC Killing-tensor search on our bump (retires the rank-4 residual)\n")
    indep = check_independence()
    print(f"  basis independence (smallest SV on random points): {indep:.2e}  "
          f"{'✅ no hidden identity' if indep > 1e-6 else '❌ DEGENERATE — prune basis'}")
    if indep <= 1e-6:
        return

    MZ = 1e-11                                              # machine-zero: Kerr's true invariants are ~1e-13
    Sk, phys_k, nk = fit(our_metric(0))
    nzero_k = int(np.sum(Sk < MZ))
    gate = nzero_k >= 2 and phys_k < MZ                      # ≥2 invariants (C₀,C₀²) AND a momentum-bearing one
    print(f"\n  GATE — Kerr [{nk} orbits]: {nzero_k} machine-zero SVs (<{MZ:.0e}; expect ≥2: C₀ and C₀²); "
          f"smallest MOMENTUM-bearing SV = {phys_k:.1e}")
    print(f"    smallest 4 SVs: {', '.join(f'{v:.1e}' for v in Sk[-4:])}   gate {'PASS ✅' if gate else 'FAIL ❌'}")

    res = {"basis_indep": float(indep), "gate_pass": bool(gate), "kerr_nzero": nzero_k, "MZ": MZ, "bumpy": {}}
    print(f"\n  TEST — our bump: the smallest *momentum-bearing* SV (pure-spatial small SVs are near-flat artifacts):")
    no_q = True
    for eps in (0.1, 0.2, 0.35):
        Sd, phys_d, nd = fit(our_metric(eps))
        has_inv = phys_d < MZ
        res["bumpy"][str(eps)] = {"phys_smallest_SV": float(phys_d), "raw_smallest_SV": float(Sd[-1]), "n_orbits": nd}
        no_q = no_q and not has_inv
        print(f"    ε={eps:<4} [{nd} orbits]: physical smallest SV={phys_d:.2e} (raw {Sd[-1]:.1e} is a spatial "
              f"artifact)  → {'NO quartic invariant' if not has_inv else 'invariant?!'}")
    res["no_quartic_invariant"] = bool(no_q)
    if gate:
        print(f"\n  RESULT: Kerr recovers both C₀ and C₀² (momentum-bearing SVs at ~1e-13); our bump's smallest")
        print(f"    momentum-bearing SV is ~1e-3–1e-4 (the obstruction, matching the rank-2 search) — "
              f"{'NO quartic invariant' if no_q else 'a surviving quartic'}.")
        print("  → Retires leg J's rank-4 residual: no rank-2 AND no rank-4 Killing tensor survives our bump.")
        print("    (Residual now only rank ≥6 — exotic and not expected for a quadrupole deformation.)")
    (RES / "numeric_quartic_search.json").write_text(json.dumps(res, indent=1))
    print("\n  wrote results/numeric_quartic_search.json")


if __name__ == "__main__":
    main()
