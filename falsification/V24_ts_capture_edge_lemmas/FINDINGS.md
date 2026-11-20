# V24 FINDINGS: Fable's capture-edge foundations (flat-plane reduction R; inequalities I1, I2)

*2026-11-20. Pre-registration 26aec7e; amendment A1 (post-result, implementation only). Code: the Bridge's own TS2
metric (V11 loader, ts45), sympy, and mpmath interval arithmetic with recursive bisection. Nothing from Fable's
checks/.*

| check | result |
|---|---|
| **R1** conformal flatness g_xx(x² − 1) = g_yy(1 − y²), plus the identity H = F⁻¹[½(p_u² + p_v²) + ½F(W + 1)] − ½ | **PASS, exact** (both cancel to 0) |
| **I1** ∂V/∂x > 0 on {V ≤ 0} ∩ 1.5 ≤ x ≤ 9.49 | **PASS**: 0 undecided, 0 violations (2067 boxes registered; 71 after A1). Float sample: min 0.0075 on 16,099 Hill points |
| **I2** ∂V/∂(y²) > 0 on {V ≤ 0} ∩ 9.3 ≤ x ≤ 77.1 | Registered: **INCONCLUSIVE** (11,165 undecided, all at y² ≥ 0.99988, the axis; 0 violations). Diagnosed: the (s − 1) factors in the denominators straddle 0 in interval arithmetic. After **A1** (removing factors of known sign exactly): **PASS**, decided on the first box. ∂V/∂s's numerator is positive on the whole box (float sample: min ∂V/∂s = 11.7 over 20,000 points of the full box, not only Hill's region) |
| NEG-I1 (extended to 9.6) | **FIRES**: 1230 proven-wrong-sign boxes near x ≈ 9.599 (Fable's ridge is 9.4995) |
| NEG-I2 (reversed sign) | **FIRES**: 39,738 proven violations |

**Verdict:**
- R1 CONFIRMED; I1 CONFIRMED.
- I2: registered INCONCLUSIVE (an implementation limit), CONFIRMED after A1 (a post-result fix to the implementation;
  no domain or rule change).
- The checker can see failures: both negative controls fired.

**What this establishes:** the flat-plane form, the funnel (Lemma F) and the alternating-returns inequality behind
Lemma R / L2′ are now independently confirmed, by interval arithmetic with the Bridge's own metric. Calling it a
*proof* would also need an audited interval library (mpmath.iv is not formally verified) and the exact rational
coefficients, which are used here.

**Not covered yet:**
- I3 (the convexity condition, which needs a validated γ);
- Lemmas G, Q, E and L3′;
- the hole lemma;
- the lobe conditions T, C1 and C2;
- Fable's R3 redesign (the separatrix map).

Environment: Python 3.14.5 (conjecture_machine .venv), sympy 1.14.0, mpmath 1.3.0, macOS 27.2.

## Addendum B: I3 (convexity on γ-adapted leaves), sample check
- **Registered run: VOID.** My Chebyshev fit of γ failed its self-checks: degree agreement 2.4e−6 against 1e−10, and
  |C(τ = 1)| = 1.9e−4 against 1e−6.
- **B1 (post-result; exact orbit derivatives replace the fit; v ≥ v_b + 1e−3):** **PASS.**
  - γ: x* = 9.804559168202442; brake point (9.854404, 0.857154), with p_u = −2e−14 and V = 5e−11. Both match Fable and V20.
  - Self-check |C(τ = 1)| = 5.4e−12 (γ is an orbit).
  - **C < 0 at every sampled point** (103 τ values × 400 v values; max C = −6.3e−5). Every point lies inside Hill's region.
  - **min −C/(1 − τ) = 0.6323, at the equator as τ → 1** (Fable: 0.63). Near the brake point: 3.04 (Fable: 3.0).
- **Negative control (straight leaves u = const, x ∈ [9.50, 9.80]): FIRES** (C ≥ 0 at 9417 Hill points).
- **Reading:** I3 holds on the sample, with Fable's margins reproduced by independent code. Like Fable's, this is a
  sample check, NOT a proof. A proof needs a validated enclosure of γ plus interval arithmetic over the leaf zone. The
  sliver beyond v_b + 1e−3 is not covered.

## Status of Fable result #2 (capture-edge reduction) after V24
- **Confirmed:** R (flat plane, exact); I1 and I2 (interval); I3 (sample, independent).
- **Hence, with the lemma logic (to be reviewed):** Lemma F (funnel), Lemma R (returns), and Lemma G (γ's curve is a
  global one-way gate). All have their inputs confirmed.
- **Still open:**
  - a review of the lemma logic (Lemmas G, Q, E and L3′; the hole lemma);
  - the 1D lobe conditions (T, C1, C2: follow W^u for ~8 returns);
  - Fable's separatrix-map test (R3 redesign).

## Addendum C (1D lobe conditions, sample): registered, amended twice, final C1′ PASS
Code: code/v24_lobes.py (C, C1); code/v24_lobes_diag.py and v24_lobes_diag2.py (diagnostics, post-result);
code/v24_lobes_C1p.py (C1′). Results: results/v24_lobes_C1*.json and .log. The section map is the Bridge's V20
(ts45, E = 97/100, L = 41/8).

- **U1/F-b′:**
  - W^u_out from z* (x* = 9.8045591682) reaches h at x_h ≈ 56.86.
  - 1915 points; min p_x on the interior of U is 6.0e−5 > 0; 0 seeds lost before h.
  - **OK.**
- **C1a:** every point beyond h returns at every step (400/400). **OK.**
- **C1b as first registered (a full fundamental domain beyond h): 200/400 "entered D". FAIL, mis-specified.** The
  arc in L3_ANALYTIC is W^u[h, m] only, and W^u past m lies inside D by geometry.
- **Amendment C1 (classification by first image, threshold 1e−9): 5/205 arc points "entered D". FAIL as registered.**
  - **Diagnosis:** all 5 sit next to a class change, within 5e−7 of S. U computed exactly there (seed root-finding,
    no interpolation) puts all 5 INSIDE cl(D), with exact gaps −7e−8 to −8e−7. They were misclassified.
  - **Root cause:** linear interpolation of U undershoots the concave curve. The 1e−9 threshold was set without
    measuring the interpolation floor, which turned out to be 6.5e−5. That is the same type of mistake as in V21–V23
    (control-clause rule).
- **Amendment C1′ (floor measured first; exact U wherever |gap| < δ = 6.5e−4): PASS.**
  - Interpolation floor: max 6.5e−5 at 30 points (median 9.9e−7).
  - In seed order W^u[h, P(h)) changes class 4 times (seeds 15, 115, 215, 315). So it crosses S 4 times per
    fundamental domain, and the outside part is two pieces of 100 seeds each.
  - **Outside points: 200. Exact D-hits within 6 returns: 0. All 200 go in through the gate.**
  - Inside points ([m, P(h)] and the second inside piece): 200, all re-enter D, as expected.
  - Reclassified: exactly the 5 diagnosed points, and no others. The smallest exact outside gap is 9.3e−8, at a
    crossing.
  - Controls (unchanged): the inward branch plunges 30/30; interior points return to D 10/10 (the must-fail fires).
- **Observation, not explained:** the four class changes are exactly a quarter of the fundamental domain apart in
  log s. A reversibility-related structure is a guess; it is not checked.
- **Reading:** C1 and C2 hold on this float64 sample of the outside arc (both pieces), for 6 returns. T (transversal
  corners) was not separately tested.
  - **Caveat:** close to the crossings the W^u–S gap falls to ~1e−7. There, a validated computation must resolve U
    exactly, which is what amendment C1′ did numerically.
  - This is a sample, not a proof.

## Status of Fable result #2 after V24 (updated)
- **Confirmed:**
  - R (exact); I1 and I2 (interval); I3 (sample, independent).
  - The lemma logic (REVIEW_LOGIC.md: sound, with the sliver unverified).
  - The lobe conditions C1 and C2 (sample, independent, with an exact boundary near the crossings).
- **Open for a proof:**
  - validated γ/I3 including the sliver;
  - hypothesis N (interval-Newton fixed point + cones);
  - validated lobe conditions (T, C1, C2) with the ~1e−7 gaps resolved;
  - rigorous transversality at h.
  These are the same items a CAPD-type horseshoe proof needs (B-5).

## Independent Arb confirmation of I1/I2 (quantum, sealed to the Bridge 2026-11-20; prereg 9f6a805, amendment b2c49cf)
- **Setup:** written from the V24 STATEMENTS, using quantum's own TS2 package and the Arb library. Outputs are in
  quantum's gitignored scratch.
- **I2: PASS** at registered depth 24 (0 undecided, 0 violations; certified lower bound of ∂V/∂s ≥ 1.114).
- **I1:** registered INCONCLUSIVE at depth 24. All 9,017 undecided boxes were at the domain's corner, x ∈ [9.488,
  9.49] and s < 0.005, and there were 0 violations. **PASS** after a post-result depth amendment (24 → 40): 0
  undecided, 0 violations; certified lower bound 9.9e−7 > 0.
- **Negative controls:** both fire.
- **Agreement:** with V24, both inequalities hold, by independent code, library and metric package.
- **CORRECTION to the V24 table above.** The I1 "float sample: min 0.0075" was a coarse sample that missed the corner.
  - Exact evaluation (sympy, 20 digits) gives ∂V/∂x = 3.3626e−3 at (x, y) = (9.49, 0), inside Hill (V = −35.3). That
    agrees with quantum's float minimum of 3.4e−3.
  - The true margin of I1 at its end x = 9.49 is therefore 3.4e−3, consistent with Fable's ridge at 9.4995.
  - The verdict does not change (my interval run was rigorous); only the quoted float margin was wrong.

## Addendum D: C¹ leaf continuation in the brake cap. PASS (float sample)
Code: code/v24_capD.py. Result: results/v24_capD.json.
- **D0:** γ's slope at the brake point, from the orbit (g′ = −0.00610607), equals the jet relation V_u/V_v there to
  1.1e−7 relative.
- **D1:** with the C¹ continuation g_τ(v) = g_τ(v_b) + g_τ′(v_b)(v − v_b) below v_b, C < 0 at all 592,076 cap points
  of Z (v ∈ [v_b − 2e−3, v_b), Hill, τ ∈ [0, 1]). The max is −0.0096. The cap has no Hill points beyond τ = 1, so the
  leaves cover it.
- **D2:** min of −C/r = 52.3 > 0, with r the distance to the brake point. So C → 0 only at the brake point, at most
  linearly.
- **Must-fail:** slope 2g′(v_b) gives max C = +0.99 (it fires).
- **Corner sanity:** Fable's straight continuation has a positive τ_v jump (0.018 to 0.096) at all 5 points. This
  reproduces the gap.
- **Reading:** the fix works on the sample. Lemma G holds with C¹ leaves.
  - What a proof still needs: interval arithmetic for C < 0 on the cap outside a small disc around the brake point,
    plus a jet lemma inside the disc (C ≈ −52r or better).
  - Both are now in recipe C-I3.

## Addendum E (symmetry of the W^u–S crossings): E and E1 inconclusive, E2 PASS
Code: code/v24_symE.py, v24_symE1.py, v24_symE2.py. Results: results/v24_symE*.json and .log. Two amendments are
in PREREGISTRATION.
- **E (Fix(R), Fix(PR) distances at the gap-located crossings).**
  - Control h: symmetric (d_R = 9.7e−10). x_h = 56.86108, matching the fleet value; Fable's 56.8606 was off.
  - The 4th class change is h itself.
  - The 3 crossings: 2 UNRESOLVED and 1 NON-SYMMETRIC as registered.
  - Diagnosed: near z* the d_R values are confounded, and the half-map H was omitted.
- **E1 (half-map H, Fix(HR)).**
  - Control H² = P: ≤ 1.2e−11. **PASS.**
  - The verdicts are still not usable. Thin-angle crossings are located only to ~1e−6 along W^u, and H iterates
    amplify that.
- **E2 (symmetric points found directly in the flow: p_x = 0 at an equator event (Fix(R) type) or at a p_y = 0
  turning event (brake type); 400 seeds; 809 roots, 17 root-finding failures at forbidden points).**
  - **Registered reading: PASS.** Each crossing has a symmetric root within |Δ log s| ≤ 1e−4: 8.3e−7, 4.7e−6 and
    3.4e−5.
  - **Confound, noted after the result.** Late events of orbits shadowing γ, a brake orbit, give roots that pile up
    toward ANY homoclinic point. So "a root nearby" alone is not decisive.
  - **Discriminator, applied after the result (labelled).**
    - Each crossing has an EARLY root, from a mid-excursion event: event 18 (brake), event 17 (Fix(R)) and event 16
      (brake) respectively.
    - Each early root coincides, to the digits shown (better than 1e−7 in log s), with the limit that the late pile-up
      converges to. That limit is the true homoclinic point; it sits 5e−6 to 3e−5 from my gap-located crossing, the
      location error diagnosed in E1.
    - A non-symmetric homoclinic point has no early root at the pile-up limit.
- **Reading.** All four W^u–S crossings per fundamental domain are symmetric homoclinic points. In order of s they
  are brake, Fix(R), brake, Fix(R) (= h). They alternate, a quarter period apart, as the reversible half-map H
  predicts (H² = P; the symmetric families sit half an H-period apart). This explains the quarter spacing seen in C1′.
- **Consequence for the proof recipe (C-T and C-L).** Each crossing can be certified as a simple zero of ONE scalar
  function of the W^u parameter: p_x at a fixed mid-excursion event. Certifying that requires no comparison of U with
  S near the crossing.

## Addendum F: the brake cap in interval arithmetic. **PASS at ρ₀ = 1e−4** (prereg 2e1daf6; Bridge, 2026-11-20 evening)
Code: code/v24_capF.py. Results: results/v24_capF.json and v24_capF.log.
Environment: Python 3.14.5 (conjecture_machine .venv), mpmath 1.3.0 (iv, 30 digits), sympy 1.14.0, macOS 27.0.1 arm64.

**Gates**
- **F0a (containment) PASS.** At 5 rational points, the degenerate-box values of V, V_u, V_v, V_uu, V_uv and V_vv
  contain the 50-digit values from direct sympy differentiation. This is an independent route from the
  quotient-rule code.
- **F0b (identity) PASS.** C(p_b; B) = [−7.38e−4, +7.38e−4] contains 0. The width comes from the slope interval
  s = V_u/V_v over B (±1e−7), which is [−0.0061083, −0.0061038].

**The ρ₀ ladder** (rungs in registered order)
- **ρ₀ = 1e−5: F2 OK, F1 FAIL.** F1 left 20 boxes undecided at depth 40, all within ~1.3e−5 of p_b. There the
  parameter width (~7e−4 in C) beats the true margin (~52 r).
- **ρ₀ = 1e−4: F2 OK, F1 OK → F PASS.**
  - **F1:** 1145 boxes; no violation, no undecided box.
    - Discharged by: 361 outside Hill, 205 by C < 0, 2 by τ ∉ [0, 1], 5 inside the disc.
    - Largest certified C.upper is −5.06e−5.
  - **F2:**
    - den ≥ 0.0582 on D;
    - ∇C over D is C_u ∈ [46.97, 57.67], C_v ∈ [−8.94, 3.17];
    - the θ-intervals were discharged by Hill (2) and by C (1);
    - the certified linear rate is ∇C·e ≤ −26.9 on the cap cone. Addendum D's float value was −C/r ≥ 52.

**Must-fail controls (all fired)**
- **NEG-F1 (slope 2s):** 104,249 proven VIOLATIONS (C.lower up to ~0.99), as addendum D predicted.
- **NEG-F0b (slope 2s):** C(p_b) = [0.9972, 0.9994], which excludes 0.
- **NEG-F2 (no Hill constraint, θ ∈ [0, 2π]) at ρ₀ = 1e−4:** FAIL as required, with 1000 undecided θ-intervals near
  θ = 3π/2.
  - **Caveat:** that firing is by indeterminacy, because C_v's enclosure contains 0 at this radius.
  - **Supplementary, post-result, not registered:** the same control at ρ₀ = 1e−5 PROVES C > 0 on
    θ ∈ [3π/2, 7π/4] (∇C·e ≥ 1.61). So the Hill constraint does the real work in F2.

**Amendment F-a (POST-RESULT; implementation only)**
- As registered, NEG-F2 kept bisecting a band of θ where the enclosure straddles 0. It would have taken many hours.
- I killed my own PID 254 after the main results and NEG-F1 were saved, and reran NEG-F0b and NEG-F2 with an
  early stop: at the first proven-positive interval, or after 1000 depth-limited ones. The registered reading
  ("fails") is unchanged.
- Also before the registered run, found in a non-counted smoke test: a proven-positive θ-interval now ends that branch
  of the bisection. Previously it was split further, a bug.

**What this establishes.**
- For every brake point p_b in the box B (±1e−7 around the float value) with V(p_b) = 0, the C¹ slope-matched leaves
  below the brake latitude satisfy C < 0 at every Hill point they cover, except at p_b itself:
  - by direct enclosure for |p − p_b| ≥ 1e−4;
  - by the mean-value form for |p − p_b| < 1e−4, with C ≤ −26.9 r.
- So the cap part of C-I3 (gap C1b) is closed rigorously, modulo two items:
  - a validated brake-point enclosure inside B (from quantum's validated γ);
  - the brake-jet relation s = V_u/V_v. This is exact; D0 checked it in float.
- **Still open in C-I3:** ∂C/∂τ > 0 above v_b on the validated γ (quantum).
