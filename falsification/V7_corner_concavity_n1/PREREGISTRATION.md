# V7 — Pre-registration: a second-session check of cuspis's n = 1 corner results (CF-9 / EXP-025)

> **⚠ SEALED TOWARD QUANTUM.** This folder discusses the corner function's small-angle end (F(0) = κ/4) and
> bounds routed through it. quantum must not open it while its sub-45° check is registered or could be reopened.

*Frozen 2026-09-24, before any derivation or code. The user approved the check ("go ahead with V7").*

## Why

cuspis's EXP-025 (commits `f602652` … `e9a1aa9`) reports three things at n = 1:

1. **κ ≥ 2·a(π/2)**, unconditional, from strong subadditivity (SSA) on equal-height rectangles. With
   Bueno–Witczak-Krempa 2016's bound on a(π/2), this gives **κ/C_T ≥ π² ln2/3 ≈ 2.280**.
2. **Conformal concavity (CC) at n = 1**: F(u) = √u·a(θ), with u = tan²(θ/4), is convex in u. This is derived
   at physics-level rigour from SSA plus the vacuum's global conformal invariance.
3. **Given CC, a set of linear programs (LPs)** gives κ ≥ 2.538·a(π/2) and κ/C_T ≥ 2.894.

Item 2 has so far been checked only inside cuspis. Its "adversarial review" was a subagent of cuspis's own
session, given cuspis's derivation text; cuspis has corrected the grading itself. Until someone outside checks
it, the settled index grades it **PARTIAL**.

## What this check is, and what it is not

- **NOT blind.** Before freezing this, the bridge read cuspis's summary of the route: the conformal flow
  (P_x − uK_x)/2, nested half-eyes, slopes at zero and at infinity, and "supremum of affine functions". The
  bridge also read the frozen inputs: assumptions A1–A7 (report.md EXP-025) and constraints C2, C3, C5
  (EXP-025b pre-registration `a938baa`; RESULT.md §2). And it has already checked cuspis's constants
  arithmetically and run one known-answer spot check on EMI (Round message, 2026-09-24).
- **The bridge will not read** cuspis's derivation text, LP code or extremal function until its own run is
  finished and frozen here. The comparison happens after.
- So V7 asks: **can a second session reconstruct every step from the stated route and inputs, and do
  independent code and exact test functions agree?** A pass is evidence that the argument holds together. It
  is not a discovery-level replication, and it is still AI checking AI.

## Inputs taken as given (not re-checked here)

A1 SSA in the continuum, including regions sharing boundary pieces · A2 CRT reflection · A3 global conformal
invariance of the vacuum with a Weyl-covariant regulator · A4 the 3d UV structure (perimeter, turning,
corner-log terms, plus a finite universal part) · A5 the strip coefficient equals the corner function's κ ·
A6 differentiability under smooth deformations · A7 a is C² on (0, π) with finite κ. Constraints C2 (a ≥ 0,
a′ ≤ 0, a″ ≥ 0), C3 (a″ + a′/sin θ ≥ 0) and C5 (a = σε² + O(ε⁴) at θ = π − ε, σ = π²C_T/24) are cuspis's
cited inputs. Their validity at n = 1 is outside V7's scope, and V7c's result is conditional on them.

## The checks — each gets its own verdict

**V7a — the unconditional bound.**
- **V7a1:** derive κ ≥ 2·a(π/2) independently from A1, A4 and A5, plus the rectangle's T ↔ L symmetry. List
  every input actually used.
- **V7a2:** read Bueno–Witczak-Krempa 2016 at the source. Confirm the a(π/2) bound's exact form and constant,
  and that it holds at n = 1 without Rényi or conjectural input.
- **Verdicts:** PASS · FAIL (an input is invalid at n = 1, or the constant differs) · GAP (a step the bridge
  cannot close, named).

**V7b — concavity at n = 1, step by step.**
- **b1 geometry:** the flow of V_u = (P_x − uK_x)/2 on the t = 0 plane. Its fixed points, flow lines, and a
  conformal map taking the plane to a flat cylinder in which V_u is a translation. Checked symbolically.
- **b2 nesting:** define the eye with parameter u′ and its half-eye, flow the half-eye under V_u, and test
  the nesting claim: interior for u < u′, exterior for u > u′ (via purity). Tested numerically on a grid of
  (u, u′), with a deliberately wrong pairing as the control.
- **b3 SSA → concavity in flow time:** name the exact regions in the SSA inequality. Check that their union
  and intersection are the regions the argument needs, and where purity enters.
- **b4 UV bookkeeping:** check that the perimeter, turning and corner-log terms cancel in the SSA
  combination under a Weyl-covariant cutoff (A3, A4), or name the term that doesn't.
- **b5 slopes:** the late-time slope −√u·a(θ(u)), including the angle relation u = tan²(θ/4); the
  early-time slope, affine in u and touching at u′.
- **b6 conclusion:** "supremum of affine functions ⇒ F convex in u", and the endpoint F(0) = κ/4.
- **Overall verdicts:**
  - **CONFIRMED:** every step reconstructed and passes.
  - **CONFIRMED WITH GAPS:** some step could not be closed. Each gap is named, and none has a counterexample.
  - **REFUTED:** a step fails with an explicit counterexample (for example, a (u, u′) where nesting fails, an
    SSA configuration whose union or intersection is not the claimed region, or a wrong angle relation that
    changes the conclusion).
  - **INCONCLUSIVE:** the bridge could not reconstruct the argument's structure.
- **The V5 lesson, written in before the run:** "the bridge could not reconstruct a step" is a GAP or
  INCONCLUSIVE, never REFUTED. Only a counterexample refutes.

**V7c — the LP constants, with independent code.**
- The bridge writes its own LPs from the frozen constraint list: CC as second divided differences of F in u,
  including F(0) = κ/4; C2; C3 with b = −a′ at midpoints; C5 as a(π) = 0. Two objectives:
  - **LP1:** minimise κ with a(π/2) = 1.
  - **LP2:** minimise κ with b·tan(θ/2) = 4 at the last midpoint (σ = 1), reported as κ/C_T = LP2·π²/24.
- **Controls:** without CC, both LPs must fall toward 0 (below 2% of the CC value at the finest grid). With
  CC, LP1 ≥ 2 − drift (the chord floor).
- **MATCH:** LP1 within 10⁻³ (relative) of 2.5379, and κ/C_T within 10⁻³ of 2.8936, at the finest grid, with
  a drift across grids that is monotone and smaller than the gap to the next reference (2π/3 = 2.0944 for LP1).
- **MISMATCH:** otherwise. Both numbers are reported, the grid is not tuned after seeing the result, and the
  tolerance is not widened (L-rule: replace the reference, never widen the tolerance).
- **V7c2:** derive the closed form φ* = max_τ τ[ln((1+τ²)/(2τ)) + (1−τ²)/(1+τ²)] from the bridge's own
  extremal analysis, if it can. Not reaching it is a GAP, not a mismatch.

**V7d — known answers.**
- Test CC on exactly known corner functions. EMI: a ∝ 1 + (π − θ)cot θ, satisfying SSA exactly. The
  holographic Einstein-gravity corner function (Hirata–Takayanagi), computed by the bridge's own quadrature.
  The CHL09 free-scalar and Dirac values at θ → 0, π/2, 3π/4 and π, as a 4-point convexity check. Use the
  real-scalar entries, i.e. the complex-scalar entries halved; the bridge nearly used the complex value on
  2026-09-24.
- **Pass:** the minimum second divided difference is ≥ −10⁻⁸ relative to max F, and a perturbed control
  fails the same test.

## Kill conditions

- **V7a1 FAIL** kills cuspis's unconditional bound as stated.
- **V7b REFUTED** kills CC at n = 1 as stated, and with it every result routed through it: the 2.538 ratio,
  the 2.894 bound, and S7a at n = 1.
- **V7c MISMATCH** kills the constants, not CC.

## Afterwards

Only after V7a–d are frozen in FINDINGS.md does the bridge read cuspis's derivation text and LP code, and
record where the two routes agree and where they differ, labelled as post-run. Status goes to the settled
index as status only.
