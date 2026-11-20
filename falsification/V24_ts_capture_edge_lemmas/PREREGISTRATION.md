# V24: independent check of Fable's capture-edge lemmas (fable_work/ts_capture_edge/L3_ANALYTIC.md), pre-registration

*2026-11-20 ~14:30 IST, written before any V24 code. Sumit: review the three Fable results one at a time.*

**Target.** Fable 5.2's claims (unreviewed):
- (R) the reduced L = 0-sector geodesic problem at TS δ=2, p = 4/5, E = 97/100, L = 41/8 is a particle in a flat (u, v)
  plane with potential V = ½F(W + 1), where x = cosh u, y = cos v and F = g_xx(x² − 1);
- (I1) on Hill's region {V ≤ 0} with 1.5 ≤ x ≤ 9.49: ∂V/∂x > 0;
- (I2) on {V ≤ 0} with 9.3 ≤ x ≤ 77.1: ∂V/∂(y²) > 0.

Fable says both inequalities were CHECKED by interval arithmetic, with no undecided boxes.

**Disclosure.** I read L3_ANALYTIC.md §0–§6, but none of Fable's check scripts or outputs.

**Independence.** The Bridge's own TS2 metric (V11 loader, ts45), sympy and mpmath interval arithmetic (mp.iv). Nothing
from Fable's checks/.

## Checks
- **R1 (exact).** With F := g_xx(x² − 1), verify symbolically:
  - g_xx(x² − 1) = g_yy(1 − y²) (the conformal-flat condition);
  - H = ½[g^xx p_x² + g^yy p_y² + W] equals F⁻¹·[½(p_u² + p_v²) + ½F(W + 1)] − ½, with p_u = p_x √(x² − 1) and
    p_v = −p_y √(1 − y²).

  sympy must cancel the difference to 0.
- **I1 (interval).** Write s = y². On the box [1.5, 9.49] × [0, 1] in (x, s), recursively bisect. A box is DECIDED if
  either the enclosure of W + 1 is > 0 (outside Hill's region), or the enclosure of ∂V/∂x is > 0. Depth limit 24.
  - **PASS:** 0 undecided boxes.
  - Report the box count and the minimum lower bound of ∂V/∂x on decided Hill boxes.
- **I2 (interval).** The same on [9.3, 77.1] × [0, 1], with ∂V/∂s.
- **Negative controls** (they must FAIL, i.e. leave undecided or violating boxes, to show the checker can see a
  failure):
  - I1 extended to x ≤ 9.6 (Fable says it fails beyond 9.4995);
  - I2 with the sign requirement reversed (∂V/∂s < 0).
  - **Measured BEFORE fixing anything:** I run the I1-extended control first and record its count. That's allowed by
    the control-floor rule, and it is not the target.

## Verdicts
- **CONFIRMED:** R1 exact, I1 and I2 with 0 undecided, and both negative controls show failures.
- **FALSIFIED:** an inequality has a box where the enclosure proves the wrong sign.
- **INCONCLUSIVE:** undecided boxes remain at the depth limit with no proven violation.
- **VOID:** a negative control shows no failure (the checker can't see failures).

**Not covered:** I3 (needs a validated γ), Lemmas G, Q, E, L3′, the hole lemma, and the lobe conditions T, C1 and C2.
Those come next, separately.

Resources: 1 core, nice 10, a footprint watcher at 1.5 GB.

## Registered results and Amendment A1 (POST-RESULT, implementation only)
- **R1: PASS (exact).** The conformal condition and the Hamiltonian identity both cancel to 0.
- **I1: PASS.** 2067 boxes, 0 undecided, 0 violations, 1.0 s.
- **NEG-I1 (extended to 9.6): FIRES.** 1230 boxes with a proven wrong sign near x ≈ 9.599, consistent with Fable's ridge at
  9.4995.
- **NEG-I2 (reversed): FIRES** (39742 proven violations).
- **I2: INCONCLUSIVE** as registered: 11165 undecided and 0 violations. Every undecided box sits at s ∈ [0.99988, 1],
  i.e. against the AXIS (y² → 1).
  - **Diagnosis:** the denominators of V and ∂V/∂s carry factors (s − 1) and (s − 1)². On a box touching s = 1 those
    straddle 0 in interval arithmetic, so the sign test can never decide, whatever the depth.
  - This is an implementation limitation of V24, not a property of V.
- **A1 (implementation only; no tolerance, domain or rule changes):** before the interval sign test, divide every
  denominator by its known factors (s − 1)^k, (x² − s)^k and (x − 1)^k(x + 1)^k, and multiply the sign by the exact,
  known sign of each removed factor on the domain (x > 1 ≥ s): (s − 1)^k has sign (−1)^k, and the others are positive.
  - Rerun I1, I2 and both negative controls. The registered I2 INCONCLUSIVE stays on record.

## Addendum B (2026-11-20, before any I3 code): Fable's third inequality I3, sample-checked independently
**Claim (L3_ANALYTIC §2).** In the flat (u, v) plane (x = cosh u, y = cos v), let u = u_γ(v) be γ's configuration curve
(a brake orbit from the equator v = π/2 to the brake latitude v_b), and u₁ = arcosh 9.3. Take the leaves
g_τ(v) = u₁ + τ(u_γ(v) − u₁). Then the tangency value C[g](v) = −V_u + g′V_v + 2Vg″/(1 + g′²) at (g(v), v) is < 0 for
0 ≤ τ < 1 and v ∈ [v_b, π − v_b]. Fable's sampled margin: −C/(1 − τ) ≥ 0.63 (equator) and ≥ 3.0 (brake).

**My γ.**
- Start at the equator at x*. The value 9.804559168 is the Bridge's own (V20); its Newton fixed point is recomputed
  here in the flat plane.
- p_u = 0 there, with p_v from K = 0. Integrate the flat-plane equations (scipy DOP853, rtol 1e−12, t_eval at the end
  only, no step history) until p_v = 0 (the brake point).
- **Gate:** the brake point lies on V = 0 to ≤ 1e−9, and the orbit is periodic: integrating back reproduces the start
  to ≤ 1e−9.
- u_γ(v) comes from a Chebyshev fit in v on [v_b, π/2] (degree chosen by convergence: two degrees agree to ≤ 1e−10 in
  g, g′ and g″), extended by the symmetry u_γ(π − v) = u_γ(v).

**Check I3s.** Evaluate C on τ ∈ {0, 0.01, …, 0.99, 0.999, 0.9999} × 400 values of v in [v_b + 1e−6, π/2].
- **PASS:** C < 0 everywhere, with min_τ,v(−C/(1 − τ)) reported and compared with Fable's 0.63.
- **Also:** C at τ = 1 must be |C| ≤ 1e−6 everywhere (γ is an orbit). That is a self-check of the γ fit.

**Negative control (must FIRE).**
- Straight leaves u = const for x = cosh u ∈ [9.50, 9.80] (Fable: "a foliation by lines fails between 9.4995 and γ").
  For a line, C = −V_u. It must be ≥ 0 at some sampled (u, v) in Hill's region.
- Control floor measured first: I'll evaluate the control alone before running I3s.

**Not covered:** the sliver beyond the brake latitude (Fable's straight-line continuation), and a validated γ (interval
enclosure). This addendum is a sample check, like Fable's own.

### Addendum B, registered result: VOID (my own γ-fit failed its self-checks). Amendment B1 (POST-RESULT)
- **γ: OK.** x* = 9.804559168202442 (V20: 9.804559168). Brake point (x, y) = (9.854404, 0.857154) with p_u = −2e−14 and
  V = 5e−11 (gate ≤ 1e−9: PASS). This matches Fable's (9.85440, 0.857154).
- **Fit gates FAILED:**
  - Chebyshev degrees 40 and 60 agree only to 2.4e−6 (gate 1e−10);
  - |C| at τ = 1 is 1.9e−4 (gate 1e−6).
  - So the fit error is as large as C itself near τ → 1, and the I3 numbers can't be trusted: max C = −6e−5 < 0
    everywhere; min −C/(1 − τ) = 0.596 at (τ = 0.9999, v = 1.5656); "equator" 2.50; "near brake" 3.04.
  - Registered verdict: **VOID** (self-check failed).
- **NEG (straight leaves): FIRED** (C ≥ 0 at 9417 points; max C = 0.97).
- **B1 (implementation of γ only; leaves, grid and every tolerance unchanged):** drop the Chebyshev fit.
  - Evaluate u_γ(v) and its derivatives EXACTLY from the orbit: invert v(t) by root-finding on the dense solution,
    then g′ = p_u/p_v and g″ = (p_v·(−V_u) − p_u·(−V_v))/p_v³ at that point.
  - Use v ∈ [v_b + 1e−3, π/2] (p_v → 0 at the brake makes g″ ill-conditioned; the last 1e−3 is left to the sliver
    treatment, not covered).
  - Rerun I3s with the same gates. |C| at τ = 1 should then be at integration-error level.

## Addendum C (2026-11-20, before any lobe-tracing code): sample check of the 1D lobe conditions (U1, F-b′, C1, C2)
Tracing uses the Bridge's own V20 section map (ts45, E = 97/100, L = 41/8; DOP853 with variational equations; rtol
1e−12). I have not read Fable's c04, c05 or c10 code or outputs.
1. **γ and U.**
   - Fixed point z* on p_x = 0 near 9.8046 (V20 scan plus polish); unstable direction e_u and λ.
   - Seeds z* + s e_u for 400 values of s, geometric in [s₀, s₀λ] with s₀ = 1e−6, on the outward branch.
   - Iterate until each seed's image first reaches p_x ≤ 0 (the crossing h). The union of the pre-crossing images
     forms U.
   - **F-b′/U1 check:** every point of U has p_x > 0 (except near the ends); every seed returns at every iterate up
     to h; U is a graph over x.
   - D := {x* < x < x_h, |p_x| < U(x)}, with U interpolated (the reversor gives S = R(U)).
2. **Beyond h (the first exit-lobe arc, C1/C2).** Keep iterating the seed images that have crossed below ℓ, for 6
   further returns. Record:
   - (C1a) every point returns at every step;
   - (C1b) no point lies strictly inside D at any step, where "inside" means |p_x| < U(x) − 1e−7, a margin above
     the gap floor;
   - (C2) every point eventually reaches x < x* with p_x < 0 (moving inward through the gate) within the 6 returns,
     and then plunges (x < 1.5) without a further return to Σ.

**PASS:** U1/F-b′ hold; C1a, C1b and C2 hold for all seeds.
**Control:** seeds on the INWARD branch W^u_in must all plunge within 2 returns (A2; Fable checked 60/60). That's a
must-pass. The must-fail control: points placed strictly INSIDE D (10 interior points, e.g. (x, ½U(x))) must NOT go
straight in; at least one must return to D.
**Disclosure:** Fable reports j₀ = 2, a W^u–S gap of 2e−6 to 1e−5, and 273/273 and 245/245 splitting-sign tests (c10).
This is a sample check, not a validated proof.

### Addendum C, registered result, and amendment C1 (POST-RESULT, diagnosed: my test applied to the wrong arc)
**Registered results:**
- U: 1915 points; x_h ≈ 56.859; min p_x on the interior of U = 6.0e−5 > 0 (F-b′ OK). 0 seeds lost before h (U1 OK).
- Beyond h: 400/400 return at every step (C1a OK). 223 went in through the gate.
- **C1b: 200/400 "entered D" (FAIL as registered).**
- Controls: inward branch 30/30 plunge (OK); interior points returning to D 10/10 (the must-fail fires).

**Diagnosis.** C1/C2 in L3_ANALYTIC concern ONLY the arc W^u[h, m] between h and the next primary homoclinic point m:
the arc that bounds the exterior lobe O₁. My registered test used every seed image beyond h, i.e. a full fundamental
domain W^u[h, P(h)]. Past m that arc legitimately lies inside D (it crosses S at m), so "entered D" for about half the
points is expected geometry, not a failure of C1. The test was mis-specified.

**C1 (fixed now; rule otherwise unchanged).** Classify the beyond-h points by their FIRST image below ℓ: outside cl(D),
meaning |p_x| > U(x) + 1e−9 or x ≥ x_h, marks the W^u[h, m] arc; inside marks the [m, P(h)] part. Apply C1b and C2 to the
[h, m] arc only.
- **PASS:** none of its points ever lies strictly inside D in the next 6 returns, and all of them go in through the gate.
- Report the arc's point count, and the count from [m, P(h)] that re-enter.

### Amendment C1 result, and amendment C1′ (POST-RESULT: written after seeing the C1 FAIL and diagnosing it)
**Registered C1 result:**
- Arc points: 205. Entered D: 5. Went in: 200. So **C1 FAILS as registered.**
- [m, P(h)] points: 195, all inside D. The controls were unchanged (30/30 and 10/10).

**Diagnosis** (results/v24_lobes_C1diag*.json, code/v24_lobes_diag*.py).
- All 5 flagged points are seeds 15–17 and 113–114. Each sits next to a class change in seed order, which means each
  is near a W^u ∩ S crossing.
- Their interpolated first-image gaps are 2e−8 to 5e−7. Over those stretches U is linearly interpolated across steps
  of 0.08 to 0.25 in x.
- U computed exactly at those x values, by root-finding the seed parameter with no interpolation, gives gaps of
  −7e−8 to −8e−7 for all 5. They are inside cl(D), so they belong to [m, P(h)] and were misclassified.
- Their later D-hit margins (4.5e−6 to 4.2e−5) agree between the exact and interpolated U to within 2e−8.
- Root cause: the 1e−9 classification threshold was set without measuring the interpolation floor. This is the
  same type of mistake as in V21–V23 (control-clause rule).
- Also seen: in seed order W^u[h, P(h)) changes class 4 times, not 2. So it crosses S at h, m and two further
  points. Its outside part is two pieces, [h, m] and one more (secondary) arc.

**C1′ (fixed before the rerun).**
1. **Floor.** Measure the interpolation floor first: |U_interp − U_exact| at 30 x values spread over (x*, x_h). Use
   δ = 10 × the max observed.
2. **Reclassification.** Classify every beyond-h first image whose interpolated gap satisfies |gap| < δ again, with
   exact U.
3. **Re-check hits.** For every point classified outside, re-check each D-hit with interpolated margin < δ against
   exact U.
4. **PASS:** no outside point has an exact D-hit within 6 returns, and all outside points go in through the gate. As
   in C1, both outside pieces are tested together; the counts are reported per piece.
5. **Also report:** every point whose class changed, and the [m, P(h)] re-entry count.

This is still a float64 sample check, not a validated proof.

## Addendum D (2026-11-20, before code): the C¹ leaf continuation in the brake cap (float sample; the recipe's C-I3 design)
**Context.** REVIEW_LOGIC addendum: Fable's straight continuation below v_b gives an upward τ-kink, so Lemma G fails
there as written. Proposed fix: for v < v_b, g_τ(v) = g_τ(v_b) + g_τ′(v_b)(v − v_b) (C¹; g″ = 0 below).
**Checks (float64, the V24 B1 exact-orbit machinery):**
- **D0.** g′(v_b), from the orbit (the limit of p_u/p_v), equals V_u/V_v at the brake point to ≤ 1e−6 relative.
  This is quantum's jet relation, used as an independent consistency check.
- **D1.** On the cap (Hill points with v ∈ [v_b − 2e−3, v_b), u ≥ u₁; grid 2001 × 2001), for every τ ∈ [0, 1] whose
  leaf passes through the point (τ is solved from u), C < 0.
- **D2.** The margin profile near the brake point: report min of −C/r, where r = |(u, v) − (u_b, v_b)|, on the cap.
  - PASS if min −C/r > 0 with no sign change. That shows C → 0 only at the brake point, and at most linearly, which
    is what a local lemma can handle.
- **Must-fail control.** A continuation with slope 2g′(v_b) must give C > 0 somewhere in the cap. This shows the check
  is sensitive to the slope.
- **Corner check (sanity).** Reproduce the sign of τ_v⁺ − τ_v⁻ > 0 for Fable's straight continuation at 5 points on
  v = v_b.
**Not claimed:** this is a sample. The rigorous version is interval arithmetic on the cap away from a small disc
around the brake point, plus a jet lemma at the brake point.

## Addendum E (2026-11-20, before code): are the 4 W^u–S crossings per fundamental domain symmetric points? (float; recipe C-T)
- **Reversibility.** R(x, p_x) = (x, −p_x) and P⁻¹ = RPR. Both R and PR are involutions.
- **A homoclinic orbit is symmetric iff it meets Fix(R) = ℓ or Fix(PR).**
- **Method.**
  - Locate each crossing c by root-finding the signed exact gap (V24 C1′ machinery, with exact U) in the seed
    parameter, between the two seeds of each class change (C1′: seeds 14/15, 114/115, 214/215, 314/315).
  - For k = −3..3, compute d_R(k) = |p_x(P^k c)| and d_PR(k) = |P(R P^k c) − P^k c|.
- **Reading:**
  - an orbit is called symmetric if min over k of d_R or d_PR is ≤ 1e−8. The root-finding precision is ~1e−12, so
    1e−8 allows for map error;
  - it is called non-symmetric if both are ≥ 1e−4;
  - otherwise unresolved.
- Also report: the parameter spacing of the 4 crossings in log s, and which pairs are R-images of each other
  (non-symmetric orbits come in R-pairs).
- **Control.** h (on ℓ by construction) must come out symmetric with d_R ≤ 1e−8. Every point of the orbit of z* is
  trivially symmetric, so that orbit is excluded.
