#!/usr/bin/env python3
"""S1 — flat 4-tori are not spectrally determined: the Schiemann/Conway-Sloane isospectral pair, verified.

    python3 schiemann.py

Gates S1a/S1b frozen in ../PREREGISTRATION.md. Pure exact integer arithmetic. Source: Cerviño-Hein
arXiv:0910.2127, Schiemann's instance (a,b,c,d)=(1,7,13,19). Two index-9 sublattices L1,L2 with identical
theta series (S1a) but a differing degree-2 Siegel theta (S1b) => same KK tower, non-isometric hidden T^4.
"""
import json
from itertools import product
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results"

D = [1, 7, 13, 19]                                    # diag inner product on basis B
l0 = (-1, 3, -1, 1); l1 = (1, -1, -1, 3); l2 = (-1, -1, 1, 3); l3 = (-1, 1, -1, 3)
def sc(v, k): return tuple(k * x for x in v)
M1 = [l0, l1, sc(l2, 3), sc(l3, 3)]                  # columns = generators of L1
M2 = [l0, sc(l1, 3), l2, sc(l3, 3)]                  # columns = generators of L2


def gram(M):
    """G[i][j] = <col_i, col_j>_D  (exact integers)."""
    return [[sum(D[k] * M[i][k] * M[j][k] for k in range(4)) for j in range(4)] for i in range(4)]


def qform(G, n):
    return sum(G[i][j] * n[i] * n[j] for i in range(4) for j in range(4))


def bilin(G, p, q):
    return sum(G[i][j] * p[i] * q[j] for i in range(4) for j in range(4))


def det4(G):
    from sympy import Matrix
    return int(Matrix(G).det())


def box_radius(G, Nmax):
    """Safe per-coordinate bound: rad >= sqrt(Nmax / lambda_min(G)) (+1 safety)."""
    import numpy as np
    lam = float(np.linalg.eigvalsh(np.array(G, float))[0])
    import math
    return int(math.ceil((Nmax / lam) ** 0.5)) + 1


def enumerate_vectors(G, Nmax):
    """All n in Z^4 with 0 < nᵀGn <= Nmax; returns dict norm->list(n) and theta histogram."""
    rad = box_radius(G, Nmax)
    vecs, theta = {}, {}
    rng = range(-rad, rad + 1)
    for n in product(rng, rng, rng, rng):
        q = qform(G, n)
        if 0 < q <= Nmax:
            vecs.setdefault(q, []).append(n)
            theta[q] = theta.get(q, 0) + 1
    return vecs, theta, rad


def main():
    print("S1 — Schiemann/Conway-Sloane isospectral 4-tori (gates frozen in PREREGISTRATION.md)\n")
    G1, G2 = gram(M1), gram(M2)
    d1, d2 = det4(G1), det4(G2)
    print(f"  G1 = {G1}")
    print(f"  G2 = {G2}")
    print(f"  det G1 = {d1}   det G2 = {d2}   (equal: {d1 == d2})\n")

    # ---- S1a: theta series agree up to Nmax
    NMAX = 400
    v1, th1, r1 = enumerate_vectors(G1, NMAX)
    v2, th2, r2 = enumerate_vectors(G2, NMAX)
    norms = sorted(set(th1) | set(th2))
    mism = [m for m in norms if th1.get(m, 0) != th2.get(m, 0)]
    s1a = (d1 == d2) and (len(mism) == 0) and len(norms) > 0
    print(f"  S1a isospectral (theta series to norm {NMAX}, box radius {r1}/{r2}):")
    shown = [m for m in norms if th1.get(m, 0)][:8]
    for m in shown:
        print(f"     ‖·‖²={m:>4}:  L1 has {th1.get(m,0):>3},  L2 has {th2.get(m,0):>3}"
              f"   {'✓' if th1.get(m,0)==th2.get(m,0) else '✗ MISMATCH'}")
    print(f"     … {len(shown)} of {len([m for m in norms if th1.get(m,0)])} occupied shells shown; "
          f"mismatches over all {len(norms)} norms: {len(mism)}")
    print(f"     →  {'PASS ✅ — identical mass tower' if s1a else 'FAIL ❌'}\n")

    # ---- S1b: degree-2 Siegel theta differs (rigorous non-isometry witness)
    B2 = min(400, NMAX)
    L1 = [n for m in v1 for n in v1[m]]
    L2 = [n for m in v2 for n in v2[m]]
    def siegel2(G, V):
        buckets = {}
        for p in V:
            qp = qform(G, p)
            for q in V:
                key = (qp, qform(G, q), bilin(G, p, q))
                buckets[key] = buckets.get(key, 0) + 1
        return buckets
    b1, b2 = siegel2(G1, L1), siegel2(G2, L2)
    diffkeys = sorted(k for k in set(b1) | set(b2) if b1.get(k, 0) != b2.get(k, 0))
    s1b = len(diffkeys) > 0
    print(f"  S1b non-isometric (degree-2 Siegel theta, {len(L1)}/{len(L2)} vectors ≤ {B2}):")
    if s1b:
        k = diffkeys[0]
        print(f"     first differing bucket (‖u‖²,‖v‖²,u·v) = {k}:  L1 count {b1.get(k,0)}, "
              f"L2 count {b2.get(k,0)}")
        print(f"     ({len(diffkeys)} differing buckets total) — an isometry preserves all pairwise Gram")
        print(f"     data, so a single differing bucket proves non-isometry rigorously.")
    else:
        print(f"     no differing bucket up to norm {B2} — UNDECIDED(bound); raise B2.")
    print(f"     →  {'PASS ✅ — non-isometric' if s1b else 'UNDECIDED(bound)'}\n")

    verdict = s1a and s1b
    print(f"  VERDICT: {'✅ POSTULATE KILLED' if verdict else 'INCOMPLETE'} — two non-isometric flat 4-tori")
    print(f"  with identical Laplace spectra. A KK mass tower does NOT determine the hidden T⁴ (dim ≥ 4).")
    print(f"\n  S1c (framing): ℝ⁴/Λ has Laplace spectrum {{4π²‖v‖² : v∈Λ*}}, so representation-equivalent")
    print(f"  lattices ⟺ isospectral dual tori. Audible ≤ 3 (V3 + Schiemann's theorem); deaf ≥ 4 (this")
    print(f"  pair, Milnor's 16D). Eigenfunction data (route 5 / K5's channel) is what could still separate.")

    OUT.mkdir(exist_ok=True)
    (OUT / "schiemann.json").write_text(json.dumps({
        "source": "Cervino-Hein arXiv:0910.2127; Schiemann (a,b,c,d)=(1,7,13,19); Conway-Sloane 1992",
        "G1": G1, "G2": G2, "det_G1": d1, "det_G2": d2,
        "Nmax": NMAX, "occupied_shells": [m for m in norms if th1.get(m, 0)][:20],
        "theta_mismatches": len(mism), "S1a_pass": bool(s1a),
        "n_vectors": [len(L1), len(L2)], "siegel2_diff_buckets": len(diffkeys),
        "first_diff_bucket": (list(diffkeys[0]) if s1b else None),
        "first_diff_counts": ([b1.get(diffkeys[0], 0), b2.get(diffkeys[0], 0)] if s1b else None),
        "S1b_pass": bool(s1b), "killed": bool(verdict),
        "verdict": ("Two non-isometric flat 4-tori with identical Laplace spectra (Schiemann/Conway-Sloane "
                    "lattices, exact integer theta match to norm %d; degree-2 Siegel theta differs). A KK "
                    "mass tower cannot determine the hidden T^4 in dim >= 4; contrast V3 (determined in 2D)."
                    % NMAX),
    }, indent=1))
    print(f"\n  wrote results/schiemann.json")


if __name__ == "__main__":
    main()
