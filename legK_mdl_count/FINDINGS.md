# Leg K — Findings: the information-theoretic count (§9's 4th lens)

*Run 2026-06-24. Predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md). Answers THE_BRIDGE §9's
"Do MDL, moduli, and measured DOF give the same count? Where do they part, and why?" by adding a fourth
lens — the information-theoretic dimension of the black-hole observation manifold.*

## Result in one line

A fourth, **information-geometric** lens **confirms the count-triangle's observable count** (Schwarzschild 1,
RN 2, dyonic 2 — including the Q²+P² degeneracy below the algebraic 3) — *provided the code is nonlinear*.
The §9 "parting" is real but it is **on the lens, not the physics**: a *linear* MDL overcounts badly via
curvature; the nonlinear intrinsic dimension agrees with moduli, measured-δ, and the neural knee.

## The two estimators (reusing leg 1's observation data)

| manifold | algebraic | observable | **linear MDL** (Minka PPCA) | **nonlinear ID** (Levina–Bickel MLE) |
|---|---|---|---|---|
| Schwarzschild | 1 | 1 | **5** | **1.31** |
| RN (M,Q) | 2 | 2 | **7** | **2.52** |
| dyonic (M,Qₑ,Qₘ) | 3 | 2 | **7** | **2.56** |

- **Linear MDL overcounts (5, 7, 7).** The observation manifold is *nonlinearly* embedded in the 8 features,
  so a linear code needs many directions to wrap the curved low-dim manifold — the leg-7b curvature
  inflation in the extreme. A linear information criterion is simply the wrong lens for this count.
- **Nonlinear ID recovers the observable count — read as steps, not absolutes.** The Levina–Bickel MLE is
  uniformly upward-biased (Schwarzschild reads 1.31 vs a true 1), so the signal is in the *increments*:
  - Schwarzschild → RN: **+1.21** — one genuinely new dimension (the charge Q). ✓
  - RN → dyonic: **+0.04** — *no* new dimension. **dyonic has the SAME dimension as RN (= 2), not 3.**

## The decisive sub-test — dyonic vs RN (the Q²+P² degeneracy)

The dyonic hole has three algebraic parameters (M, Qₑ, Qₘ) but its observables depend only on the
combination Qₑ²+Qₘ² (electric ≡ magnetic). If the information count saw all three, dyonic's ID would sit one
step above RN's; instead it is **identical to RN's** (2.56 vs 2.52). So the **nonlinear information count
sees the observable degeneracy** — the same 3→2 collapse the neural knee found (leg 1) and ansatz *proved*
(the Q²+P² mechanism). A fourth independent lens, agreeing.

## §9 answer

The lenses **part on the code, not the physics.** The count is the **nonlinear / observable** one
**(1, 2, 2)** — moduli (proved), measured-δ (leg 3), neural-knee (leg 1), and now nonlinear-ID all agree.
The single outlier is the **linear** code (MDL), and *why* it parts is exactly the curvature inflation
leg 7b and Move I already flagged: a flat (linear) description of a curved manifold over-reports its
dimension. So "how many numbers is a black hole" is well-posed as the curvature-aware count, and four
independent lenses now converge on it.

## Honest limits
- The MLE ID is biased and slightly noisy; the verdict rests on the **step** Δ(dyonic−RN)=+0.04 vs the
  unit step Δ(RN−Schwarzschild)=+1.21, not on absolute values rounding to 1/2/2.
- Same observation set as leg 1 (charged-static family, dimensionful features); the result inherits leg 1's
  family scope.

## Artifacts
- `code/mdl_count.py` — Minka PPCA-MDL + Levina–Bickel MLE intrinsic dimension on leg 1's data (read-only).
- `results/mdl_count.json`.
