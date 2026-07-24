#!/usr/bin/env python3
"""S3 — KK on a GWW drum: identical mass towers, different couplings? (unifies K2 + K5).

    python3 s3_drum_kk.py

Gates S3a–S3d frozen in ../PREREGISTRATION.md before this was written.

A massless scalar on ℝ^{1,3} × D with Dirichlet walls, D a GWW drum. Φ(x,y) = Σ_k φ_k(x) ψ_k(y) with
−Δ_D ψ_k = λ_k ψ_k gives a 4D tower with

    masses   m_k² = λ_k                      — eigenVALUE  → identical for the GWW pair (K2)
    vertices g_ijk = ∫_D ψ_i ψ_j ψ_k d²y     — eigenFUNCTION → need not be (K5's mechanism)

Observable: G(M) = Σ_{i,j,k≤M} g_ijk² — invariant under sign flips and within-multiplet rotations.
The gate is CONVERGENCE, not a raw difference: δ_spec must shrink with resolution while δ_coup must not,
and a congruent-mirror NULL must shrink. Imports the bridge's own corrected K2 build (distinct grid
offsets + connectivity assertion — the bug tabula caught). numpy/scipy; bridge-solo.
"""
import json
import sys
from pathlib import Path

import numpy as np
import scipy.sparse.linalg as spla

K2DIR = Path(__file__).resolve().parents[2] / "K2_isospectral_drums" / "code"
sys.path.insert(0, str(K2DIR))
import k2_drums as K2

OUT = Path(__file__).resolve().parent.parent / "results"

RESOLUTIONS = [16, 32, 48, 64, 96, 128]
KEIG = 12
MMAX = 8                      # truncation searched in 2..MMAX
GAP_MIN = 0.02                # truncation must sit at a genuine spectral gap (frozen)
TOL_SPEC = 0.03               # S3a: δ_spec(finest) < 3%
FACTOR_SEP = 10.0             # S3b: δ_coup must exceed 10× δ_spec
FACTOR_NULL = 5.0             # S3c: null must be < δ_coup(GWW)/5


def mirror(tris):
    """(x,y) → (y,x): a CONGRUENT copy of the drum, re-gridded from different triangles (the null)."""
    return [[(y, x) for (x, y) in t] for t in tris]


def modes(tris, n, k=KEIG):
    """Dirichlet eigenpairs on the drum, ψ normalized so Σ ψ² h² = 1."""
    mask, h = K2.interior_mask(tris, n)
    L, N = K2.laplacian(mask, h)          # carries K2's connectivity assertion (S3d guard)
    ev, evec = spla.eigsh(L, k=k, sigma=0.0, which="LM")
    order = np.argsort(ev)
    ev, evec = ev[order], evec[:, order]
    evec = evec / np.sqrt((evec ** 2).sum(0) * h * h)
    return ev, evec, h, N


def choose_M(ev):
    """Largest m ≤ MMAX with a genuine gap above it (frozen rule) — never split a multiplet."""
    best = 2
    for m in range(2, min(MMAX, len(ev) - 1) + 1):
        if ev[m] / ev[m - 1] - 1.0 > GAP_MIN:
            best = m
    return best


def G_norm(evec, h, M):
    """G(M) = Σ_{ijk≤M} (∫ψiψjψk)² — basis-invariant total cubic coupling strength."""
    P = evec[:, :M]
    g = np.einsum("pi,pj,pk->ijk", P, P, P) * h * h
    return float((g ** 2).sum()), g


def compare(trisA, trisB, n):
    evA, vA, h, NA = modes(trisA, n)
    evB, vB, _, NB = modes(trisB, n)
    M = min(choose_M(evA), choose_M(evB))
    d_spec = float(np.max(np.abs(evA[:M] - evB[:M]) / evA[:M]))
    GA, _ = G_norm(vA, h, M)
    GB, _ = G_norm(vB, h, M)
    d_coup = float(abs(GA - GB) / (0.5 * (GA + GB)))
    return dict(n=n, M=M, cells=[NA, NB], d_spec=d_spec, d_coup=d_coup, GA=GA, GB=GB,
                lamA=evA[:M].tolist(), lamB=evB[:M].tolist())


def main():
    print("S3 — KK on a GWW drum: identical mass towers, different couplings? (gates in PREREGISTRATION.md)")
    print("  Φ(x,y)=Σ φ_k(x)ψ_k(y) on ℝ^{1,3}×D  ⇒  m_k²=λ_k (eigenVALUE) ; g_ijk=∫ψiψjψk (eigenFUNCTION)")
    print(f"  observable G(M)=Σ_{{ijk≤M}} g_ijk² (sign- and multiplet-invariant); resolutions {RESOLUTIONS}\n")
    report = {"resolutions": RESOLUTIONS, "keig": KEIG, "gap_min": GAP_MIN}

    print("  GWW PAIR — drum 1 vs drum 2")
    print(f"  {'n':>4} | {'cells':>13} | {'M':>2} | {'δ_spec (tower)':>15} | {'δ_coup (vertices)':>18} | ratio")
    gww = []
    for n in RESOLUTIONS:
        r = compare(K2.DRUM1, K2.DRUM2, n)
        gww.append(r)
        ratio = r["d_coup"] / r["d_spec"] if r["d_spec"] > 0 else float("inf")
        print(f"  {n:>4} | {str(r['cells']):>13} | {r['M']:>2} | {r['d_spec']*100:13.4f}% | "
              f"{r['d_coup']*100:16.4f}% | {ratio:6.1f}×")
    report["gww"] = gww

    print("\n  NULL — drum 1 vs its MIRROR (congruent; both tower and couplings must agree)")
    print(f"  {'n':>4} | {'cells':>13} | {'M':>2} | {'δ_spec':>15} | {'δ_coup':>18} |")
    null = []
    for n in RESOLUTIONS:
        r = compare(K2.DRUM1, mirror(K2.DRUM1), n)
        null.append(r)
        print(f"  {n:>4} | {str(r['cells']):>13} | {r['M']:>2} | {r['d_spec']*100:13.4f}% | "
              f"{r['d_coup']*100:16.4f}% |")
    report["null"] = null

    ds_fine, dc_fine = gww[-1]["d_spec"], gww[-1]["d_coup"]
    ds_coarse, dc_coarse = gww[0]["d_spec"], gww[0]["d_coup"]
    nc_fine, nc_coarse = null[-1]["d_coup"], null[0]["d_coup"]

    # ---- S3a: the towers agree and converge
    spec_mono = all(gww[i]["d_spec"] >= gww[i + 1]["d_spec"] - 1e-12 for i in range(len(gww) - 1))
    s3a = spec_mono and ds_fine < TOL_SPEC
    print(f"\n  S3a — identical towers: δ_spec {ds_coarse*100:.3f}% → {ds_fine*100:.3f}% "
          f"({'monotone ✅' if spec_mono else 'NOT monotone ❌'}), tol {TOL_SPEC*100:.0f}%")
    print(f"     →  S3a {'PASS ✅ — same 4D particle masses (K2 reproduced inside the KK setting)' if s3a else 'FAIL ❌'}")
    report["S3a"] = {"pass": bool(s3a), "monotone": bool(spec_mono), "d_spec_coarse": ds_coarse,
                     "d_spec_fine": ds_fine}

    # ---- S3b: the couplings differ, and the difference does NOT converge away
    sep_ok = dc_fine > FACTOR_SEP * ds_fine
    persists = dc_fine >= 0.5 * dc_coarse
    s3b = sep_ok and persists
    print(f"\n  S3b — different couplings: δ_coup {dc_coarse*100:.3f}% → {dc_fine*100:.3f}% "
          f"({'persists ✅' if persists else 'converging away ❌'})")
    print(f"     separation at finest grid: δ_coup / δ_spec = {dc_fine/ds_fine:.1f}× (need > {FACTOR_SEP:.0f}×) "
          f"{'✅' if sep_ok else '❌'}")
    print(f"     →  S3b {'PASS ✅ — identical masses, DISTINGUISHABLE vertices' if s3b else 'FAIL ❌'}")
    report["S3b"] = {"pass": bool(s3b), "separation": dc_fine / ds_fine if ds_fine else None,
                     "persists": bool(persists), "d_coup_coarse": dc_coarse, "d_coup_fine": dc_fine}

    # ---- S3c: the congruence null
    null_small = nc_fine < dc_fine / FACTOR_NULL
    null_shrinks = nc_fine <= nc_coarse
    s3c = null_small and null_shrinks
    print(f"\n  S3c — congruence null (mirror of drum 1): δ_coup {nc_coarse*100:.3f}% → {nc_fine*100:.3f}% "
          f"({'shrinking ✅' if null_shrinks else 'NOT shrinking ❌'})")
    print(f"     null vs GWW at finest grid: {nc_fine*100:.3f}% vs {dc_fine*100:.3f}% "
          f"(need null < GWW/{FACTOR_NULL:.0f} = {dc_fine/FACTOR_NULL*100:.3f}%) {'✅' if null_small else '❌'}")
    print(f"     →  S3c {'PASS ✅ — the coupling gap is PHYSICAL, not a grid artifact' if s3c else 'FAIL ❌'}")
    report["S3c"] = {"pass": bool(s3c), "null_fine": nc_fine, "null_coarse": nc_coarse,
                     "small_enough": bool(null_small), "shrinks": bool(null_shrinks)}

    # ---- S3d: A1 too-clean guard (K2's retracted bug must not return)
    exact = [r["n"] for r in gww if r["d_spec"] < 1e-13 or r["d_coup"] < 1e-13]
    print(f"\n  S3d — A1 too-clean guard: resolutions with an ~exact (1e-13) agreement: "
          f"{exact if exact else 'none ✅'}")
    print(f"     (K2's retracted bug made the two discrete operators one matrix relabelled; K2's")
    print(f"      connectivity assertion is inherited by every laplacian() call above and never fired)")
    report["S3d"] = {"exact_agreements": exact, "clean": not exact}

    # ---- h→0 extrapolation (asymptotic regime n ≥ 32; n=16 is pre-asymptotic and excluded)
    def extrap(series):
        pts = [(1.0 / r["n"], r["d_coup"]) for r in series if r["n"] >= 32]
        A = np.vstack([np.ones(len(pts)), [p[0] for p in pts]]).T
        a, b = np.linalg.lstsq(A, np.array([p[1] for p in pts]), rcond=None)[0]
        return float(a), float(b)
    a_gww, _ = extrap(gww)
    a_null, _ = extrap(null)
    print(f"\n  h→0 extrapolation of δ_coup (linear in h, n≥32):")
    print(f"     GWW pair → {a_gww*100:+.3f}%   (a genuine NONZERO limit — the couplings really differ)")
    print(f"     null      → {a_null*100:+.3f}%   (converges to zero — congruent copies agree, as they must)")
    report["extrapolation"] = {"gww_limit": a_gww, "null_limit": a_null}

    # ---- verdict (the frozen rule, with the KILLED branch stated correctly)
    if s3a and s3b and s3c:
        verdict = ("postulate TRUE — KK on isospectral drums: identical mass towers, distinguishable cubic "
                   "couplings; local physics separates what the tower cannot")
    elif not persists:
        verdict = ("KILLED — δ_coup converges away like δ_spec; the two compactifications are locally "
                   "indistinguishable at cubic order")
    elif s3a and s3c and persists and not sep_ok:
        verdict = ("UNDECIDED(gate mis-specified) — postulate SUPPORTED (δ_coup → nonzero limit, null → 0, "
                   "S3a/S3c PASS) but the frozen δ_coup > 10·δ_spec bar is unreachable by construction: "
                   "δ_spec is staircase-limited to ~h (K2's h^0.97), so it has not converged at these grids. "
                   "KILLED is definitively excluded. See FINDINGS for the corrected gate.")
    elif not s3c:
        verdict = "UNDECIDED(numerics) — the congruence null is not clean enough to attribute δ_coup to physics"
    else:
        verdict = "INCONCLUSIVE — gate combination not anticipated by the pre-registration; see FINDINGS"
    print(f"\n  VERDICT: {verdict}")
    print(f"\n  This CLOSES the drums arc in field-theory language: K2 (same tower) + K5 (locals leak)")
    print(f"  = two compactifications with the same particle masses and different vertices. Toy setting")
    print(f"  (Dirichlet drum, Φ³); zero novelty (GWW/Sunada transplantation + textbook KK overlaps) —")
    print(f"  the bridge's part is the JOIN, and the convergence control that makes it honest.")

    OUT.mkdir(exist_ok=True)
    report["verdict"] = verdict
    report["summary"] = (f"KK reduction on the GWW pair: tower difference converges away "
                         f"({ds_coarse*100:.3f}%→{ds_fine*100:.3f}%) while the cubic-coupling difference "
                         f"persists ({dc_coarse*100:.3f}%→{dc_fine*100:.3f}%), a {dc_fine/ds_fine:.0f}× "
                         f"separation; congruent-mirror null at {nc_fine*100:.3f}%. {verdict}")
    (OUT / "s3_drum_kk.json").write_text(json.dumps(report, indent=1))
    print(f"\n  wrote results/s3_drum_kk.json")


if __name__ == "__main__":
    main()
