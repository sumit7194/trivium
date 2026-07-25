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

  G-B  RANK-DIFFERENCE gate  genuine = null(W) - deficiency(F)  -- tabula's law (round 8, commit 4159a1d),
       adopted over my own first version, which was worse. Their catch: at momentum degree >= 4 a polynomial
       library goes rank-deficient (degree 8 carried 8 exact-zero singular values out of p=147 -- COLLINEAR
       COLUMNS, not conservation laws) and a calibrated cutoff duly reported 9 "invariants". Because
       centering is linear, every null of F is automatically a null of W, so the EXTRA nulls in W are
       exactly the conserved combinations.

THE TWO GUARDS CATCH DIFFERENT MECHANISMS, which is why both are kept:
  * G-B catches COLLINEARITY-manufactured nulls (O1 type): deficiency(F) > 0.
  * G-A catches APPROXIMATION-manufactured nulls (O4 type): deficiency(F) = 0, yet W carries a genuinely
    small-but-nonzero singular value. That is invisible to a rank difference at any single tolerance --
    tabula's deg-8 table is entirely the collinearity case, so their law does not see O4.
Order matters: G-B runs BEFORE any null-space claim, because a rank-deficient library makes the emit
question meaningless rather than merely hard.

NOTE on the self-test below: with column normalisation, poly6's ratio rises above tau, so G-B rejects it
first and G-A is not exercised on that row. G-A's independent competence on O4 is established by R7d
(884x held-out degradation), not by this run.
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


def _rank(M):
    n = np.linalg.norm(M, axis=0, keepdims=True)
    M = M / np.where(n > 0, n, 1.0)
    s = np.linalg.svd(M, compute_uv=False)
    tol = max(M.shape) * np.finfo(float).eps * s[0]
    return int(np.sum(s > tol)), M.shape[1]


def _F(orbits, basis, stride=1):
    """FEATURE matrix: the basis on the data, UNCENTERED. Collinearity lives here."""
    return np.vstack([np.column_stack([f(o[::stride]) for f in basis]) for o in orbits])


def invariant_count(orbits, basis, stride=1):
    """G-B, in tabula's formulation (their round 8, commit 4159a1d) — strictly better than my first version.

        genuine invariants = null(W) - deficiency(F)

    W is the per-orbit-CENTERED deviation matrix; F is the UNCENTERED feature matrix. Centering is linear,
    so every null direction of F is automatically a null direction of W. The EXTRA nulls in W are therefore
    exactly the conserved combinations, and every spurious "invariant" is exactly a rank deficiency of F.
    No threshold and no ε anywhere.

    THE TRAP, which tabula named and which I fell into first: measuring the conditioning on W deletes the
    finding — a true invariant IS a rank deficiency of W (that null vector is the invariant). Only F
    separates "redundant column" from "conserved combination". The conditioning gate belongs on the
    library, NEVER on the deviation matrix. My first version checked W and rejected every true case.

    THE TOLERANCES DIFFER, and that is L8 (state what each side is), not a fudge:
      * F's degeneracy is EXACT — algebraic collinearity among basis functions is identically zero, so it
        is measured at machine tolerance.
      * W's null is only APPROXIMATE — a real invariant is conserved to integrator accuracy (our pendulum
        H = ½p² − cos x sits at σ_min/σ_max = 2.4e-12, not at machine zero), so it is measured at τ.
      Using machine tolerance on W misses every true invariant; this file's previous version did exactly
      that and lost pendulum-poly4+cos.
    """
    rF, p = _rank(_F(orbits, basis, stride))                       # exact: algebraic collinearity
    W = _design([o[::stride] for o in orbits], basis)
    sW = np.linalg.svd(W, compute_uv=False)
    nullW = int(np.sum(sW <= TAU_REL * sW[0]))                     # approximate: numerically conserved
    defF = p - rF
    return {"p": p, "rank_F": rF, "deficiency_F": defF, "null_W": nullW,
            "genuine": nullW - defF}


def library_conditioning(orbits, basis):
    """G-B plus tabula's own stability caveat, implemented rather than assumed.

    Both terms are numerical rank estimates, so their difference inherits their sensitivity: tabula report
    that at half the time-samples their degree-6 case returns -1 instead of 0. They kept the method out of
    their regression battery for that reason and told us to check rank(F) is flat before trusting the
    difference. So we check it: recompute at stride 2 and require rank(F) to agree.
    """
    full = invariant_count(orbits, basis, stride=1)
    half = invariant_count(orbits, basis, stride=2)
    stable = full["rank_F"] == half["rank_F"] and full["genuine"] == half["genuine"]
    return {**full, "rank_F_half": half["rank_F"], "genuine_half": half["genuine"],
            "stable": bool(stable), "degenerate": bool(full["deficiency_F"] > 0)}


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

    if not cond["stable"]:
        verdict, why = False, (f"UNSTABLE — rank(F) moves under sampling ({cond['rank_F']}→"
                               f"{cond['rank_F_half']} at stride 2); the rank difference cannot be trusted "
                               f"(tabula's stated failure mode). Report, do not conclude.")
    elif cond["genuine"] < 1:
        verdict, why = False, (f"REJECTED by G-B: null(W)={cond['null_W']} − deficiency(F)="
                               f"{cond['deficiency_F']} ⇒ **{cond['genuine']} genuine invariants**; any null "
                               f"is collinearity of the library, not a conserved combination")
    elif not raw["emit"]:
        verdict, why = False, f"no emit: σ_min/σ_max = {raw['ratio']:.2e} > τ = {TAU_REL:.0e}"
    elif degrade >= HELDOUT_MAX:
        verdict, why = False, (f"REJECTED by G-A: passes in-sample ({raw['ratio']:.2e}) but held-out "
                               f"degrades {degrade:.0f}× ({out:.2e}) — APPROXIMATION, not representation (O4)")
    else:
        verdict, why = True, (f"EMIT: {cond['genuine']} genuine invariant(s) "
                              f"[null(W)={cond['null_W']} − def(F)={cond['deficiency_F']}]; "
                              f"σ_min/σ_max = {raw['ratio']:.2e}, held-out {out:.2e} ({degrade:.1f}× — generalises)")
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
