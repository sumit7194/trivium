# V7 — Findings: a second-session check of cuspis's n = 1 corner results

> **⚠ SEALED TOWARD QUANTUM.** This folder discusses the corner function's small-angle end and bounds routed
> through it. quantum must not open it while its sub-45° check is registered or could be reopened.

*Run 2026-09-24 against the pre-registration (`f437313`). Sections 1–5 were frozen **before** the bridge read
cuspis's derivation text or LP code. Section 6 is the post-run comparison, labelled as such.*

## Verdicts in one table

| Check | Verdict |
|---|---|
| **V7a1** κ ≥ 2·a(π/2) at n = 1, re-derived | **PASS** |
| **V7a2** Bueno–Witczak-Krempa's a(π/2) bound, read at source | **PASS**: holds at n = 1 without Rényi or conjectural input |
| **V7b** concavity at n = 1, step by step | **CONFIRMED WITH GAPS**: every step reconstructed, three gaps named, no counterexample |
| **V7c** LP constants, independent code | **MATCH**: 2.537868 and 2.893629, plus an independent analytic derivation of the closed form |
| **V7d** known answers | **PASS**: EMI, holography (including F(0) = κ/4) and the CHL09 free-field points; every live control fires |

**What this means.** A second session reconstructed cuspis's argument from its stated route and inputs, and
the argument holds together. The one piece that is still assumption-level is how the entropy of a region
behaves across widely separated scales (G1 below). That is the same assumption cuspis lists as A5. The check is
**not blind** and it is **still AI checking AI** (see the pre-registration).

---

## 1. V7a — the unconditional bound

**V7a1 (code/v7a1_rectangle.py).** Write a T × L rectangle's universal part as S_univ = −4a·log(L/ε) + G(T/L),
using A4 and the four π/2 corners.
1. SSA on equal-height rectangles [0, T₁+T₂] and [T₁, T₁+T₂+T₃] gives S(T₁+T₂) + S(T₂+T₃) ≥ S(T₁+T₂+T₃) + S(T₂).
   The perimeter term is linear in T, so **G is concave**.
2. The thin-strip limit (A5: the strip coefficient is the small-angle κ) gives G′(x) → −κ as x → ∞. A concave
   function has a nonincreasing derivative, so **G′(x) ≥ −κ for every x**.
3. Rotation symmetry S(T × L) = S(L × T) gives G(x) − G(1/x) = −4a·log x. Differentiating at x = 1 gives
   **G′(1) = −2a(π/2)**, checked symbolically.

Hence **κ ≥ 2a(π/2)**. Inputs used: SSA (A1), the rectangle's UV structure (A4), strip = small-angle κ (A5), and
rotation invariance. No Lorentz boosts, no Rényi input, no positivity conjecture. The derivation uses only
the first derivative of G, which matches cuspis's description ("SSA supplies only the first two orders").

**V7a2.** The bridge read BWK16 (arXiv:1511.04077) at source.
- Their eq. (II.1) is CHL09's SSA-plus-Lorentz inequality. Saturating it gives a_min(θ) = (π²C_T/3)·log(1/sin(θ/2))
  (eq. II.2).
- Appendix A.1 proves a ≥ a_min by a Chaplygin comparison. It uses only (II.1), a(π) = a′(π) = 0, the smooth-end
  normalisation σ = π²C_T/24, and reflection.
- At π/2 the bound becomes (π² ln 2/6)·C_T ≈ 1.1402·C_T (eq. II.4), identical to cuspis's (π²/3)·log√2·C_T.
- The paper's Rényi bounds are a separate §II.A; the EE bound does not use them.

Combined with V7a1: **κ/C_T ≥ π² ln 2/3 = 2.2804, unconditional at n = 1.**

## 2. V7b — concavity at n = 1

The bridge read Lanzetta–Moult–Wang 2609.04302 at source for the eye construction. Their proof uses the
variational principle for H(u) = (P₀ − uK₀)/2 on a fixed defect Hilbert space. That route doesn't exist at
n = 1. What follows is the bridge's own reconstruction of the n = 1 replacement named in cuspis's summary.

**b1 geometry (code/v7b_geometry.py, symbolic).** The facts:
- H(u) acts on the t = 0 plane as the holomorphic field (1 − uz²)/2, with fixed points ±1/√u.
- In w = log[(1 + √u z)/(1 − √u z)] it is the translation w → w + √u·τ.
- ζ(i) = e^{iθ(u)/2}, with tan(θ/4) = √u.
- The eye through ±i with cusps ±1/√u′ has opening angle 4·arctan√u′.
- The attractor contracts at rate √u.

All are exact: symbolic residuals 0, angle error 10⁻¹⁶.

**b2 nesting (numeric, 90 (u, u′, τ) cases).** Along every flow line of H(u), the flowed region
R(τ) = L ∪ slab[0, τ] ∪ φ_τ(U) is a single interval when u < u′ (the half-eye is interior to the band). Its
complement is a single interval when u > u′ (the exterior case). There are 0 failures.
- **Controls.** A notched half-eye breaks the interval structure in all 3 control cases (31, 37 and 13 broken
  rows). It breaks the set identities below in 2 of 3; in the third the notch happened not to disturb them at
  those τ, so the interval test is the sharper of the two.

**b3 SSA → concavity in flow time.** Take A = R(τₘ) and B = φ_Δ R(τₘ), with Δ = τₘ − τ₁ = τ₂ − τₘ.
- For u < u′: A ∪ B = R(τ₂) and A ∩ B = φ_Δ R(τ₁).
- For u > u′, the complements carry the interval structure. De Morgan swaps ∪ and ∩: A ∩ B = R(τ₂) and
  A ∪ B = φ_Δ R(τ₁). Purity makes SSA symmetric under complement, so the conclusion is the same.
- Checked pointwise on jittered grids: **0 mismatches in 90 cases**.
- The reversed assignment (each branch's identities applied to the other branch) fails in every case (≥ 8198
  mismatched points), so the test can fire.

With S(φ_Δ X) = S(X) up to the local terms of b4, SSA gives **2S(R(τₘ)) ≥ S(R(τ₁)) + S(R(τ₂))**.

**b4 UV bookkeeping.**
- The four regions' boundaries coincide piecewise as multisets, so perimeter and turning terms cancel in the SSA
  combination (A1, regions sharing boundary pieces). So do their cusps, the lower cusp of L and the flowed upper
  cusp, both at angle θ(u′).
- There are no new corners. Where a u′-eyelid meets a band edge, the two are tangent: both are perpendicular to
  Σ₀ at (0, ±1).
- The one non-cancelling piece is the corner log under the conformal map: S_fin(φX) = S_fin(X) − Σ_c a(θ_c) log|φ′(c)|,
  which is A3. The bridge absorbs it into a compensated function:

      ĝ(τ) = S_fin(R(τ)) − a(θ(u′)) · Σ_{cusps c of R(τ)} log|w′(c)|

  Since w′(φ(c))·φ′(c) = w′(c), ĝ is **exactly invariant** under the flow. So SSA makes **ĝ concave in τ**,
  modulo A1, A3 and A4.

**b5 slopes.**
- **Late time.** R(τ) near the attractor looks like a wedge of angle θ(u) from scale 1 down to ℓ_τ ~ e^{−√uτ},
  capped by the flowed cusp θ(u′). S_fin gains (a(θ(u)) − a(θ(u′)))·log ℓ_τ, and the compensation term adds
  −a(θ(u′))·√uτ. So the θ(u′) pieces cancel and **ĝ′(∞) = −√u·a(θ(u)) = −F(u)**.
- **Early time.** R(τ) is the u′-eye with its upper eyelid pushed by τ·H(u). So **ĝ′(0) = S_fin′(0) − a(θ(u′))·u/√u′**.
  S_fin′(0) is a linear functional of the deformation field (A6), and H(u) is affine in u, so ĝ′(0) is affine
  in u.
- **Touching.** At u = u′, R(τ) is the u′-eye itself (it is invariant), so S_fin′(0) = 0 and
  ĝ′(0) = −√u′·a(θ(u′)) = −F(u′) = ĝ′(∞). The inequality is saturated at u′.

**b6 conclusion.** Concavity gives ĝ′(0) ≥ ĝ′(∞), so F(u) ≥ ℓ_{u′}(u) := −ĝ′(0). ℓ_{u′} is affine in u and equals
F at u′. So F is the upper envelope of affine functions, i.e. **convex**. Also F(0) = κ/4 (since √u ≈ θ/4 and
a ≈ κ/θ) and F(1) = a(π) = 0.

**Gaps (named, none a counterexample).**
- **G1, multi-scale structure (late slope).** It assumes the entropy of a region with a wedge of angle θ(u)
  between scales ℓ and 1, capped by a cusp at scale ℓ, has log coefficients that add as written. This is the
  content of A5 (the strip-on-cylinder coefficient is the corner function). It is standard lore, not proved here.
- **G2, differentiability at the junctions.** The deformation's normal component is continuous at (0, ±1) but
  its derivative jumps, so the boundary stays C¹ with a curvature jump. A6 is stated for smooth deformations.
  First-order variations of this type should be fine, but that is an assumption.
- **G3, touching as a limit.** At u = u′ the compensation term is singular, because the cusp is then a fixed
  point. Touching needs ĝ′(0) to be continuous in u at u′, i.e. continuity of the shape derivative.
- Not a gap: the u > u′ branch rests on purity, which holds for the pure vacuum.

## 3. V7c — the LP constants (code/v7c_lp.py, the bridge's own code)

| θ_min \ N | 200 | 400 | 800 | 1600 | 3200 |
|---|---|---|---|---|---|
| LP1 min κ/a(π/2), 10⁻³ | 2.537840 | 2.537855 | 2.537866 | 2.537867 | **2.537868** |
| LP1, 10⁻⁴ | 2.537840 | 2.537855 | 2.537866 | 2.537867 | **2.537868** |
| LP2 κ/C_T, 10⁻³ | 2.893577 | 2.893609 | 2.893626 | 2.893629 | **2.893629** |
| LP2, 10⁻⁴ | 2.893576 | 2.893610 | 2.893626 | 2.893629 | **2.893629** |

- **Drift.** Monotone, ≤ 3·10⁻⁵ from N = 200 to 3200. It is insensitive to θ_min and far below the gap to
  2π/3 = 2.0944.
- **Controls.** Without CC, both LPs return 0. That control is necessary but weak, since κ enters only through CC.
  With CC but without C3, LP1 returns **2.000000**, the chord floor, so C3 is what lifts the bound.

**V7c2, the closed form, derived independently.** Write τ = tan(θ/4) and g = b·tan(θ/2), with b = −a′.
- The tangent-line intercept of F at u is F − uF′ = τa/2 + g·τ(1 − τ²)/(1 + τ²) (symbolic identity, residual 0).
- By CC, κ/4 ≥ F − uF′ at every u.
- C3 makes g nonincreasing, so g ≥ g(π) = 4σ. Since a(θ) = ∫_θ^π g·cot(ϑ/2) dϑ, this gives a ≥ 8σ·log(1/sin(θ/2)).
  Together: F − uF′ ≥ 4σ·φ(τ), with φ(τ) = τ[ln((1+τ²)/(2τ)) + (1−τ²)/(1+τ²)].
- Hence **κ ≥ 16σφ***, i.e. **κ/C_T ≥ (2π²/3)φ* = 2.893630**. Here φ* = 0.4397790 at τ* = 0.371519, θ* = 81.52°.
- Normalised instead at π/2: g(π/2) ≥ a(π/2)/ln 2 and g ≥ g(π/2) on θ ≤ π/2. Since θ* < 90°, this gives
  **κ/a(π/2) ≥ 4φ*/ln 2 = 2.537868**.
- C2 is not used. The extremal is BWK's a_min shape above θ* with F affine below θ*.

## 4. V7d — known answers (code/v7d_known.py, code/v7d_holo_F0.py)

Pass rule (frozen): the minimum second divided difference of F in u is ≥ −10⁻⁸·max|F|.

| Function | min second divided difference | Verdict | Control, must fail |
|---|---|---|---|
| EMI, a ∝ 1 + (π−θ)cot θ, nodes F(0) = π/4 and F(1) = 0 | +0.668 | PASS | bump: −206, fails ✓ · a_min (κ = 0): fails ✓ |
| Holography (Einstein), with F(0) = κ/4 | +0.161 | PASS | κ lowered 1% at the node: −4·10⁹, fails ✓ |
| CHL09 real scalar (κ, 90°, 135°, 180°) | +0.021 | PASS | the complex-scalar 90° value (0.02366): fails ✓ |
| CHL09 Dirac | +0.041 | PASS | — |

The holographic function is from the bridge's own derivation of the Hirata–Takayanagi surface, and it passes
its self-checks:
- σ/C_T = 0.411237 against π²/24 = 0.411234;
- the extrapolated κ equals Γ(3/4)⁴/π to 10⁻¹¹, i.e. κ/C_T = 3.709229;
- it is monotone;
- the fitted linear small-angle coefficient is −4·10⁻⁹, consistent with 0.

## 5. Instrument log: what went wrong during the run, and what was done

Recorded because each one could have produced a false verdict.
1. **b2, jitter.** Im w was first jittered per point, which moves points off their flow line and produced one
   spurious broken row. Fixed to per-row jitter. The re-run gave 0.
2. **V7c, sign.** The first C3 row had a sign error, making the LP infeasible. It was caught as infeasibility
   before any value existed.
3. **V7d, holographic quadrature.** Two drafts failed their own σ and monotonicity self-checks: a split point
   near t = 0 and a numerically cancelling 1/h² subtraction. Those runs' concavity verdicts are void. The fix
   was an exact cancellation-free integrand, (1+h²)²h0⁴ − P = (1+h²)(1+h0²)h⁴. The tolerance was not touched.
4. **V7d, with-F(0) node.** The first attempt estimated κ as Ω·a at the smallest angle. That forces the first
   chord slope to about 0 and reported a failure that was an estimator artefact. It was replaced by the closed-form
   κ, cross-checked by extrapolation, in 40-digit arithmetic.
5. **V7d, a control designed in the wrong direction.** The first holographic control raised κ by 1% and did not
   fire. It can't: raising the endpoint of a convex function keeps it convex, because CC bounds κ from below.
   It is kept in the record. The live control lowers κ by 1%, and fails as it should.

No tolerance was changed after seeing a result.

## 6. Post-run comparison with cuspis's derivation *(added after `a897549`; the bridge read cuspis's EXP-025 addendum, addendum 2 and EXP-025b only now)*

**Where the two routes agree.**
- **O1 is V7a1**: the same three steps (cuspis's h is the bridge's −G) and the same inputs.
- **O3 has the same skeleton as V7b**: the flow (1 − uz²)/2, a Killing frame in which it is a translation (cuspis's
  w has circumference 2π/√u, the bridge's 2π, which is the same frame rescaled), nesting read off the containment
  of one lens in the other, the late slope from A5, the early slope affine in u from A6, and touching at u′.
- **Constants.** The LP values agree to ~10⁻⁶, and both sides have the closed form 16σφ* and 4φ*/ln 2.
  The bridge derived it without reading EXP-025c.
- **Gaps.** cuspis's review named three. Its (i) (ξ_u is tangent to the boundary at ±i) is the bridge's **G2**, at the same
  point. Its (ii) (a cap window near u = u′) is the bridge's **G3**, the same cusp-at-a-fixed-point degeneracy
  regularised differently. Its (iii) (shape-differentiability and the ρ → 0 limit, i.e. A6) overlaps G2 and G3.
  The bridge's **G1** (multi-scale log structure) is cuspis's A5, which cuspis lists as an assumption rather than
  a gap. Same content either way.

**Where they differ: two different formalisations of the same idea.**
- **Region family.**
  - *cuspis:* reflected half-regions θH_a ∪ H_b, which uses A2 (CRT reflection). This mirrors LMW's ⟨ψ|e^{−τH}|ψ⟩.
  - *bridge:* translates of L ∪ slab ∪ φ_τ(U), with no reflection. So A2 is not needed on the bridge's route.
  - Both give concavity in the total flow time.
- **UV bookkeeping.**
  - *cuspis* caps the cusp at radius ρ and uses a Killing-covariant cutoff. That creates its gap (ii), closed by
    fixing (u, u′) first and then letting ρ → 0.
  - *bridge* keeps the cusps under a uniform cutoff and uses the compensated ĝ = S_fin − Σ a·log|w′(c)|, which is
    exactly flow-invariant. That avoids the cap window, but meets the same degeneracy as a singular compensation at
    u = u′ (G3).
- **LP discretisation of C3.**
  - *cuspis's final rows* are an exact relaxation, (a_i − a_{i+1})/∫cot(θ/2) nonincreasing, so every grid value is a
    certified lower bound.
  - *the bridge's midpoint rows* match cuspis's first LP run (`exp025b_output_run1_midpointC3.txt`), which is not a
    guaranteed relaxation. So the bridge's LP numbers corroborate the constants but do not certify them. The
    certificate is the analytic V7c2 argument, which both sides now have independently.
- **Known answers.**
  - *cuspis* has the EMI tangent-line identity (the step-4 Hellmann–Feynman test), built by its within-session
    reviewer and re-run to 10⁻¹⁰.
  - *the bridge* has holography with the F(0) node in 40-digit arithmetic, and did not repeat the EMI identity.
    Each side's known answer is one the other lacks.

**Net.** The idea survives being formalised two different ways, by two sessions, with different regularisations
and different region families. The load-bearing assumptions are the same on both routes: A5, the multi-scale log
structure, and A6, first-order shape differentiability, including at the C¹ junctions. So the honest grade stays
the same: **derived at physics-level rigour, now checked outside cuspis (non-blind); not a theorem.** Promoting it
further needs either a proof of A5 and A6 in this setting, or a human specialist.
