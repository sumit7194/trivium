#!/usr/bin/env python3
"""The bridge's STANDING emit criterion — R2's engine plus the two guards that were tested and adopted.

    python3 emit_guarded.py          # self-test on R2's known cases, including the O4 false positive

Why this file exists separately from R2's `emit_reproduce.py`: R2's run is banked and its FINDINGS cite its
numbers, so that file stays frozen and reproducible. This wrapper is what any FUTURE emit run should use.

Two guards, each earned rather than assumed:

  G-A  HELD-OUT (generalisation) guard  -- R7d, 684x separation on our own O4 case.
       Rationale (R7): O4's false emit sits FIVE ORDERS ABOVE the measured noise floor, so it is an
       APPROXIMATION phenomenon, not a noise one. No threshold on sigma_min -- hand-set or noise-calibrated
       -- can separate representation from approximation, because both produce a genuinely small sigma_min
       in-sample. Only generalisation can. R7 tested the noise-calibrated cutoff (Oellerich & Emelianenko
       Cor. 4.2) and it let O4 through by 28x.

  G-B  LIBRARY-CONDITIONING gate -- contributed by tabula (round 8, commit 4159a1d).
       At momentum degree >= 4 their polynomial library went numerically rank-deficient: degree 8 carried
       8 exact-zero singular values out of p=147 -- COLLINEAR COLUMNS, not conservation laws -- and a
       calibrated cutoff duly reported 9 "invariants". Null-space counting of any flavour manufactures
       invariants out of collinearity unless the library's conditioning is checked FIRST. Same disease that
       made our own R7c pick poly2 (a large gap between NON-null singular values).

Order matters: G-B runs BEFORE any null-space claim, because a rank-deficient library makes the emit
question meaningless rather than merely hard.
"""
import sys
from pathlib import Path

import numpy as np

R2DIR = Path(__file__).resolve().parents[2] / "R2_emit_theorem" / "code"
sys.path.insert(0, str(R2DIR))
import emit_reproduce as R2

TAU_REL = 1e-6           # retained; R7 showed replacing it is NOT the fix, so it stays as a first sieve
COND_MAX = 1e10          # G-B: library condition number ceiling (rank-deficiency ⇒ question is meaningless)
HELDOUT_MAX = 10.0       # G-A: emit only if held-out degrades by less than this factor


def _design(orbits, basis, normalize=True):
    M = R2.design_matrix(orbits, basis)
    if normalize:
        n = np.linalg.norm(M, axis=0, keepdims=True)
        M = M / np.where(n > 0, n, 1.0)
    return M


def library_conditioning(orbits, basis, n_gen=800, seed=7):
    """G-B: is the LIBRARY itself degenerate — independent of the dynamics?

    CRITICAL: this must be evaluated on GENERIC OFF-ORBIT points, never on the trajectory design matrix.
    A true conserved quantity MAKES the orbit design matrix rank-deficient — that null direction IS the
    invariant. Checking conditioning there would reject every genuine discovery (it did, in this file's
    first version: it threw out harmonic-poly2 and pendulum-poly4+cos as "degenerate").

    Collinearity of the basis FUNCTIONS is a property of the library alone, so it is measured where the
    dynamics cannot contribute: scattered points in the same domain the orbits occupy. This is R2's own
    O1/G1 rank guard, reused for tabula's conditioning catch.
    """
    Z = np.vstack(orbits)
    lo, hi = Z.min(axis=0), Z.max(axis=0)
    g = np.random.default_rng(seed).uniform(lo, hi, size=(n_gen, Z.shape[1]))
    B = np.column_stack([f(g) for f in basis])
    B = B - B.mean(axis=0, keepdims=True)                     # constants are removed, as in the design matrix
    n = np.linalg.norm(B, axis=0, keepdims=True)
    B = B / np.where(n > 0, n, 1.0)
    s = np.linalg.svd(B, compute_uv=False)
    cond = float(s[0] / s[-1]) if s[-1] > 0 else float("inf")
    tol = max(B.shape) * np.finfo(float).eps * s[0]
    exact_nulls = int(np.sum(s <= tol))
    return {"cond": cond, "exact_null_dims": exact_nulls, "p": B.shape[1], "on": "generic off-orbit points",
            "degenerate": bool(cond > COND_MAX or exact_nulls > 0)}


def emit_guarded(orbits, basis, n_test=2):
    """R2's emit criterion with both guards. Returns a verdict dict; `emit` is the guarded answer."""
    if len(orbits) <= n_test:
        raise ValueError("need more orbits than the held-out split")
    cond = library_conditioning(orbits, basis)
    raw = R2.emit(orbits, basis)

    tr, te = orbits[:-n_test], orbits[-n_test:]
    Mtr = _design(tr, basis)
    _, _, Vt = np.linalg.svd(Mtr, full_matrices=False)
    c = Vt[-1]
    Mte = _design(te, basis)
    ins = float(np.linalg.svd(Mtr, compute_uv=False)[-1] / np.linalg.svd(Mtr, compute_uv=False)[0])
    out = float(np.linalg.norm(Mte @ c) / (np.linalg.norm(Mte) + 1e-300))
    degrade = out / ins if ins > 0 else float("inf")

    if cond["degenerate"]:
        verdict, why = False, (f"REJECTED by G-B: library degenerate (cond={cond['cond']:.2e}, "
                               f"{cond['exact_null_dims']}/{cond['p']} exact-zero σ) — collinear columns, "
                               f"not invariants; the emit question is meaningless here")
    elif not raw["emit"]:
        verdict, why = False, f"no emit: σ_min/σ_max = {raw['ratio']:.2e} > τ = {TAU_REL:.0e}"
    elif degrade >= HELDOUT_MAX:
        verdict, why = False, (f"REJECTED by G-A: passes in-sample ({raw['ratio']:.2e}) but held-out "
                               f"degrades {degrade:.0f}× ({out:.2e}) — APPROXIMATION, not representation (O4)")
    else:
        verdict, why = True, (f"EMIT: σ_min/σ_max = {raw['ratio']:.2e}, held-out {out:.2e} "
                              f"({degrade:.1f}× — generalises), library well-conditioned")
    return {"emit": verdict, "why": why, "raw_ratio": raw["ratio"], "in_sample": ins,
            "held_out": out, "degradation": degrade, "conditioning": cond}


def main():
    rng = np.random.default_rng(20260726)
    print("Standing guarded emit criterion — self-test on R2's known cases\n")
    ho = [R2.orbit("harmonic", [rng.uniform(0.5, 2), rng.uniform(-1, 1)]) for _ in range(6)]
    pe = [R2.orbit("pendulum", [rng.uniform(1.6, 2.8), rng.uniform(-0.3, 0.3)]) for _ in range(6)]
    cos_atom = [lambda z: np.cos(z[:, 0])]

    cases = [("harmonic  poly2      (true)", ho, R2.poly_basis(2)),
             ("pendulum  poly2      (true neg)", pe, R2.poly_basis(2)),
             ("pendulum  poly6      (O4 FALSE POSITIVE)", pe, R2.poly_basis(6)),
             ("pendulum  poly4+cos  (true)", pe, R2.poly_basis(4) + cos_atom),
             ("harmonic  duplicated col (O1)", ho, [lambda z: z[:, 0], lambda z: z[:, 1],
                                                    lambda z: 2 * z[:, 0] + 3 * z[:, 1]])]
    ok = True
    expect = {0: True, 1: False, 2: False, 3: True, 4: False}
    for i, (lab, orbs, b) in enumerate(cases):
        r = emit_guarded(orbs, b)
        good = r["emit"] == expect[i]
        ok &= good
        print(f"  {lab:42s} emit={str(r['emit']):5s} {'✅' if good else '❌'}")
        print(f"      {r['why']}")
    print(f"\n  self-test {'PASS ✅ — O4 rejected, O1 rejected, true cases kept' if ok else 'FAIL ❌'}")
    print(f"  guards: G-A held-out (R7d, ours) · G-B library conditioning (tabula, round 8)")


if __name__ == "__main__":
    main()
