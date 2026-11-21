# V26 findings: Fable's single-centre result via the lower axis (Bridge, 2026-11-20 evening)
Environment: Python 3.14.5 (conjecture_machine .venv), sympy 1.14.0, mpmath 1.3.0; macOS 27.0.1 arm64.
Bridge code only (code/). Fable's scripts were not run or reused.

## L-src: PASS (read in the original PDF)
Meinel & Neugebauer, "Asymptotically flat solutions to the Ernst equation with reflection symmetry", CQG 12 (1995)
2045, arXiv:gr-qc/0302114 (5 pages, read in full).
- Section III integrates the Ernst linear problem along both outer axis parts. It assumes only asymptotic flatness
  and regularity for ζ > ζ₊ and ζ < ζ₋; reflection symmetry is NOT used there.
- Eq. (35): f^(u)(ζ) = (1 + G(ζ))/F(ζ) and f^(l)(ζ) = F(ζ)/(1 + G(ζ)), with one pair of analytic functions F(K),
  G(K) (Eqs. 32–36; their analyticity is stated in Section IV).
- **Hence f^(l)(ζ) = 1/f^(u)(ζ),** with f^(u) continued analytically. That is rule (L).
- Their headline result (reflection symmetry ⟺ f^(u)(ζ) conj f^(u)(−ζ) = 1) is the symmetric special case.

## L-proof (Bridge, by hand): an independent parity argument
**Hypotheses.**
- Asymptotic flatness: ξ → 0, where ξ = (1 − e)/(1 + e).
- ξ is real-analytic for r > R on a full neighbourhood of both outer axis segments, so
  ξ = Σ_{n≥0} r^{−(n+1)} F_n(u) with u = cos θ and each F_n regular on [−1, 1].

**Ernst equation in ξ:** (ξ ξ̄ − 1) Δξ = 2 ξ̄ (∇ξ)².

**Order r^{−(n+3)}.** The equation reads L_n F_n = S_n, where L_n F = ((1 − u²)F′)′ + n(n+1)F.
- S_n is a sum of products F_a F̄_b (terms in F_c), with a + b + c = n − 2.
- ∇ contributes ∂_r, which keeps the angular parity, and the term (1 − u²)∂_u·∂_u, which takes two u-derivatives
  and so also keeps the product parity.
- So if F_k(−u) = (−1)^k F_k(u) for k < n, then S_n has parity (−1)^n.

**Induction.**
- L_n commutes with u → −u.
- Split F_n into its parity-(−1)^n part and its opposite part G. Then L_n G = 0.
- The solutions of L_n G = 0 regular at u = ±1 are multiples of P_n, which has parity (−1)^n (Q_n is log-singular at
  ±1). So G = 0.
- The base case n = 0 gives L₀F₀ = 0, so F₀ is constant.

**Lower axis** (u = −1, z = −r):
ξ_l(z) = Σ (−z)^{−(n+1)} (−1)^n F_n(1) = −Σ F_n(1) z^{−(n+1)} = −ξ_u(z). **QED.**

**What both proofs need.** Asymptotic flatness, and a REGULAR lower axis segment. The series form also needs
convergence for large r. That is standard for analytic asymptotically flat solutions, but it is an assumption here.

## L-num (own code, code/v26_L.py): PASS to order 10
Ernst equation for (ξ, η = ξ̄ as an independent field) solved order by order with exact Gaussian rationals, from random
upper-axis moments. At every order, the polynomial F_n of degree ≤ n exists and is unique given F_n(1); this confirms
the series form.
- **Result.** For 3 complex seeds and 1 real (static) seed, F_n(−1) = (−1)^n F_n(1) holds exactly at every order
  n = 0..10, i.e. ξ_l = −ξ_u.
- **Wrong guesses fail** for every seed: the mirror guess e_-(z) = e_+(−z) and the guess e_- = conj(e_+).

## Exact controls (code/v26_exact.py): PASS
Rule L holds identically in closed form for:
- Schwarzschild (ξ = x);
- Kerr (ξ = px + iqy);
- Kerr–NUT (e^{iα}(px + iqy), not reflection-symmetric);
- Tomimatsu–Sato δ = 2.

The mirror guess e_-(z) = e_+(−z) fails for Kerr, Kerr–NUT and TS. It holds for Schwarzschild only because ξ_u is odd
there.

## N-count (code/v26_N.py): PASS
For e = 1 − 2/z + i b/z² (b = 1/2, 1, 3):
- f0^- has degree 4. P = E² − f0^- has 8 simple singular points (4 simple poles + 4 simple zeros), so s + 2h = 8 > 4.
- **Control** c0 = b/z (Kerr–NUT-type): degree 2, s + 2h = 4.

## N-search (adversarial): PASS (no counterexample)
**Random scan.** 6000 trials over classes D (f0 = 1 − 2/z), C (double pole) and f0 = 1. Twists had denominators of
degree 1–4, with roots placed at the centre, at f0's zero, at random rationals, or as irreducible quadratics.
Numerators were sometimes forced to vanish at f0's zero.
- Asymptotically flat twists (c0 = O(z⁻²)): minimum deg f0^- = 4 in all three classes. 0 hits with deg ≤ 2.
- **Must-find control (non-flat twists):** 700 hits with deg 2, all of Kerr–NUT type (c0 = b/z in class D, and
  c0 = b/(z − s) for f0 = 1). The search finds the known exceptions.

**Symbolic families, with resultant-forced cancellations:**
- generic degree 4–8;
- after any one parameter cancellation, the minimum is 4;
- the one exception is class C with c0 = a/z², which reaches degree 3, but only at q = ±i a, i.e. complex data, not a
  real metric. Even there, degree 3 is still obstructed at first order.

## Verdict so far
- **(L) CONFIRMED:** source read in full, own proof, own series code exact to order 10, exact closed-form controls.
- **(N) CONFIRMED** on every tested family, with no counterexample.
- **Consequence.** Twisted rational single-centre data, seen from a regular lower axis, have f0^- of degree ≥ 4. The
  first-order classification (deg ≤ 2 ⟺ solvable, at generic E; ansatz §158) then obstructs them.

**Still unchecked by the Bridge:**
- the static class-C third-order step (Fable's t4; the Bridge's B6);
- an end-to-end exact metric (B1);
- certified lower-axis monodromy (B3);
- the first-order classification itself.

**The physical caveat is now sharper.** The corollary needs BOTH outer axis segments regular, and integrals
meromorphic near BOTH axis families. A twisted single-centre solution may carry a singular lower axis (a string).
If so, it falls outside the hypotheses rather than being excluded. That needs stating explicitly in any write-up.

## Addendum A (B6): static double-pole data from below. **PASS** (code/v26_B6.py, Bridge V25 return-map machinery)
**Decomposition.** f0^- = z²/(z² − 2z + q) = 1 − m1/(z − z1) − m2/(z − z2). This is exact for:
- q = 3/4 (real roots 3/2 and 1/2; m = −2.25 and 0.25);
- q = 5/4 (roots 1 ± i/2; m = −1 ± 0.75i).

**Static (c0 = 0).** The cubic return-map coefficients match the closed form with F = 1 at E = 0.8 and 0.6 in both
cases:
- the error is 3e−9 to 3e−8, at or below the floor;
- the self-checks are ≤ 3e−10;
- the coefficients are nonzero (|A| ≈ 0.47–3.8). So the data are OBSTRUCTED at third order.

**Cancellation control** (the complexified reference twist): A ≈ 0 (≤ 3e−8), as predicted (F = 0).

**ZV δ = 2 control** (q = M²): f0^- = z²/(z − M)², a double pole. Seen from below it is again single-centre, so it is
undecided by the axis. That agrees with Fable's statement.

## Addendum B: lower outer axis regularity (no Misner string). **PASS** (code/v26_omega.py)
**Hand argument.** ∂_θ ω = r² sin θ ∂_r χ / f². So the ω jump between the outer axis segments along a semicircle is
−2 × (the 1/r coefficient of χ), the NUT parameter. The form is closed, so the value is independent of R.

**Numerics** (own Ernst series to order 10):
- **AF twisted data** e_+ = 1 − 2/z + i/z²: Δω = −5.7e−16, −7.9e−20 and 4.6e−22 at R = 20, 40, 80. That is zero up to
  series truncation.
- **NUT control** (+ i/(2z)): Δω = −1.0000000000 at every R, exactly −2n.

**Consequence.**
- For asymptotically flat data without NUT, ω is constant on each regular axis segment and has no jump between the
  outer segments, so ω = 0 on both. γ → 0 at infinity on both.
- So the far lower axis is automatically regular, with no string and no conical defect. **The regularity caveat in
  the verdict above is REMOVED for the outer segments at large |z|.**
- What remains assumed is analyticity of the fields near infinity, which is standard for asymptotically flat
  solutions. Struts or strings between source components lie in the finite region and do not affect the outer axis
  orbits used.

## Item 3: the inherited first-order classification, re-checked by hand (Bridge)
Only the direction the theorem uses is checked: deg f0 ≥ 3 ⇒ the identity component is SL(2) at generic E.
- **The normal form.** The NVE v″ = r v with r = −(3/16)(P′/P)² is already in normal form.
- **Local exponents.**
  - At a point where P has order m: r ~ b/(z − p)², with b = −3m²/16. So √(1 + 4b) = √(1 − 3m²/4): 1/2 for |m| = 1,
    and non-real for |m| ≥ 2.
  - Infinity is ordinary when f0(∞) = 1 and E² ≠ μ² (r = O(z⁻⁴)).
- **Kovacic's necessary conditions** (standard sets E_c, E_∞):
  - **Case 1:** Σ Re α_c ≤ α_∞ ≤ 1 with Re α_c ≥ 1/4 (simple) or 1/2 (heavy), which needs s/4 + h/2 ≤ 1.
  - **Case 2:** E_c = {1, 2, 3} for simple points and {2} for heavy ones, with E_∞ = {0, 2, 4}. A nonnegative integer
    d needs s + 2h ≤ 4.
  - **Case 3:** E_c ⊂ {3, ..., 9} for simple points and {6} for heavy ones, with e_∞ ≤ 12. This needs
    3s + 6h ≤ 12.
  - All three reduce to s + 2h ≤ 4. If no case holds, the group is SL(2) (Kovacic).
- **Counting at generic E.**
  - f0 = E²/μ² has deg f0 simple roots, so s ≥ deg f0.
  - The poles of f0 add total order deg f0. All simple poles give s = 2 deg f0. Any multiple pole adds h ≥ 1. Either
    way, s + 2h ≥ deg f0 + 2 ≥ 5 when deg f0 ≥ 3.
  - **Hence SL(2). CONFIRMED by hand.**
  - This agrees with Fable's NOTES §2 and with ansatz §158 (numerical monodromy).
- **Inherited and not re-done here:** passing from the time parameter to z (a finite cover; MPS 2013 and
  Morales–Ramis), and the Fuchsian/global setting. Both were reviewed in V21/V25.

## Verdict (updated)
- **Fable's single-centre result is CONFIRMED** at the level of every step checked: (L), (N), static class C (B6),
  outer-axis regularity, and the first-order classification direction used.
- **Theorem SC + Corollary hold**, modulo:
  - the analyticity of asymptotically flat fields near infinity (standard);
  - the inherited literature theorems (Morales–Ramis–Simó, Kovacic);
  - ZV δ = 2, whose non-integrability rests on MPS 2013 (an equatorial orbit), since both its axes are single-centre.
- **Not done (optional extra rigour):** certified lower-axis monodromy (B3) and true-geodesic return maps (B7).

## Addendum C (B8): the invisible non-rational family seen from below. **PASS (obstructed at first order; numerical, not a certificate)** (code/v26_B8.py)
**Self-test.** The hand-coded f0, f0′, (c0″)² and its derivative agree with sympy to 7e−16.

**Gates** (every run): loop traces ≤ 1.4e−12; det − 1 ≤ 1e−10; c0 and c0′ return to their start values to ≤ 1e−13,
so c0 is single-valued on the loops in |z| > 1.3.

**Statistic.** S is the registered quantity: max ‖KK′ − K′K‖ over commutator pairs. The floor is |S(rtol 1e−13) −
S(rtol 1e−11)|.

| E | k = 0 (Kerr from below) | k = 1/100 | k = 1/30 | k = 1/10 |
|---|---|---|---|---|
| 0.8 | 1.1e−8 (floor 1.2e−6) | 10.31 | 34.41 | 103.4 |
| 0.7 | 1.6e−8 (floor 1.3e−6) | 56.63 | 188.6 | 564.5 |
| 0.9 | 6.4e−9 (floor 1.1e−6) | 1.354 | 4.533 | 13.76 |

- For k ≠ 0, the floors are ≤ 5e−7. Every k ≠ 0 entry exceeds 100 × (the k = 0 value) and 100 × its floor, by
  factors of 10⁶ or more.
- **Linearity in k** (E = 0.8; k = 1e−3, 3e−3, 1e−2): S = 1.031, 3.094, 10.32. The log–log slope is 1.0001
  (registered: 1 ± 0.2).
- **Positive control** (rational twisted single-centre data from below): S = 1.5e5 at E = 0.8 and 2.1e6 at E = 0.7.
- **Extra, not registered:** the normalised statistic S/(‖K‖‖K′‖) is 4e−11 to 1.4e−10 at k = 0, and 9e−5 to 6e−2 for
  k ≠ 0. (These values come from the rtol 1e−11 pass.)

**Reading.**
- For every k ≠ 0 tested, the lower-axis first-order monodromy has a non-abelian derived subgroup.
- It contains elements arbitrarily close to the identity as k → 0, by linearity. So it is not finite.
- So the group is not virtually abelian, and **the invisible family is obstructed at first order on the lower
  axis**, as Fable's exploratory run indicated.

**Status: numerical, in double precision, with independent Bridge code.**

**Still needed for a theorem:**
- a certified (interval or high-precision) monodromy. ansatz has been asked for a blind 40–50-digit second
  implementation;
- convergence of the lower-axis rule for non-rational data that are analytic at infinity. The series proof covers
  analytic asymptotically flat data, but convergence is assumed.

## Addendum C, independent twin (ansatz §159, sealed 5c1b456; unblinded 2026-11-21 ~02:40)
- **Implementation:** 50-digit power-series monodromy; c0 by its Laurent series at ∞ (no logs, ρ_c = 0.600);
  argument-principle location of the singular points.
- **Verdict: OBSTRUCTED (non-virtually-abelian)** at all 9 (k, E). Kerr (k = 0) is VA at the 1e−23 to 1e−37 level, and
  its degree-3 control is NON-VA. **This AGREES with the Bridge's verdict.**
- **Singular-point locations** agree with the Bridge's refined loops.
- **OPEN DISCREPANCY in the statistic's trend.**
  - ansatz's statistic DECREASES with k at fixed E (E = 0.8: 2.0e−4, 4.4e−5, 5.4e−6 for k = 1/100, 1/30, 1/10).
  - The Bridge's normalised commutator statistic INCREASES linearly (3.2e−4, 1.06e−3, 3.2e−3; slope 1.0001).
  - The two are different statistics. ansatz will compute the Bridge's statistic from its 50-digit matrices
    (post-unblinding, labelled), plus a k → 0 scan, to locate the difference. The verdict doesn't depend on this, but
    the record stays open until it's explained.

## Addendum D (2026-11-21 ~03:05): basis-free trace cross-check with ansatz. **PASS**. The statistic-trend discrepancy is CLOSED
Code: code/v26_D.py, reusing the B8 model unchanged. Output: results/v26_D.txt and .json. Interpreter:
conjecture_machine .venv, Python 3.14.5, scipy 1.18.0.

**Result.** tr(g_in) − 2 on |z| = 1.35 at E = 0.8, against ansatz's 50-digit values:

| k | Bridge (tr − 2) | Relative difference from ansatz |
|---|---|---|
| 1e−3 | −4.785118e−9 | 4.9e−7 |
| 1e−2 | −4.790928e−7 | 3.4e−7 |
| 1/30 | −5.340084e−6 | not reported by ansatz |
| 1/10 | −4.850010e−5 | 6.1e−8 |

- The coefficient is −4.785e−3·k² plus a higher-order term.
- The integration floor is ≤ 3.2e−14.
- Free-homotopy invariance: |tr(r = 1.6) − tr(r = 1.35)| ≤ 5e−15.
- Gates: |det − 1| ≤ 3e−15; c0 returns to itself within 7e−13.

**Controls.**
- k = 0 gives tr − 2 = −9e−16.
- Must-fail: r = 2.5 is a different class (it encloses the turning point and the poles 2 ± 0.6i). There tr = 0.000,
  versus 2 − 4.85e−5 at r = 1.35. The control fires.

**Reading.**
- Two independent implementations agree on a basis-free, path-free invariant to about 5e−7. So the monodromy itself
  is cross-validated.
- The earlier statistic-trend discrepancy came from ansatz's statistic: commutators against large-norm generators
  amplify ||g_in − I|| ≈ 80k by about 1e7, so the statistic saturates. ansatz's S_B, computed from its own
  generators, is linear in k (slope 1.0002), matching the Bridge's 1.0001.
- Neither S statistic is a magnitude of obstruction. Both are zero/nonzero detectors only.
- The invisible-family finding (obstructed at first order for k ≠ 0) stands. It is numerical with two independent
  codes. It is not a certificate.

## Addendum E (2026-11-21 ~03:45): Neon T3's concrete claims. **E1 FAIL as registered (harness labelling), PASS under labelled amendment E-a; E2 PASS**
Code: code/v26_E.py. Outputs:
- results/v26_E_asregistered.txt (first run, kept);
- results/v26_E_amendedEa.txt.

**E1 (Class D degree classification).**
- In 62 seeded exact examples, every computed reduced-denominator degree equals Neon's formula. The four structural
  cases had 22, 6, 22 and 10 examples.
- The registered min-degree clause failed: the minimum was 2. The cause is that the random generator produced 8
  examples with c0 = c/z, which is Taub–NUT, and labelled them generic. The prereg text excludes NUT.
- **Amendment E-a (post-result, labelled).** Detect c0 = c/z as NUT. After that the minimum non-Schwarzschild,
  non-NUT degree is 3: PASS.
- The must-fail control works: the wrong formulas mismatch on 60 of 62 examples.

**E2 (ZV δ = 2 equatorial NVE1).**
- Bridge's independent derivation of r(x) equals Neon's EXACTLY.
- x² r = 3/4 − 7x + 11x² + …; exponents −1/2 and 3/2; Frobenius obstruction −38 ≠ 0, as Neon said.
- Exact Kovacic Case 1 search: 7 admissible exponent sets, no polynomial solution.
- Must-pass control, Schwarzschild δ = 1: r = −3/(4(x + 1)²(3x + 5)²). Case 1 finds solutions (d = 0), so the search
  works.
- Gal = SL2(C) is confirmed for the ZV δ = 2 radial equatorial NVE at E = 2. This re-derives the known result
  (Maciejewski–Przybylska–Stachowiak 2013).

**Not machine-checked here:**
- Neon's Sibgatullin proof of e_- = 1/e_+ (the same identity V26 already established by two routes);
- the Class C corollary;
- the upper-axis all-orders argument (conditional on horizon holomorphicity).

## Addendum F (2026-11-21 ~04:40): Neon T8's first-order proof of the invisible-family obstruction. **F1 FAIL as registered (write-up typo); F2 PASS, agreement 5e−7**
Code: code/v26_F.py. Outputs:
- results/v26_F_firstrun.txt (first run, kept);
- results/v26_F_diagnosis.txt;
- results/v26_F.txt.

**F1.**
- Neon's stated δc0″ = 75(4375z⁴ − 1350z² + 27)/((25z² − 3)(25z² + 9)³) is IDENTICAL to the Bridge's.
- Neon's written closed form for δc0 does NOT integrate to it: it differs from the independent ray integrals by
  0.235–0.269 on |z| = 1.35. **Registered verdict: FAIL.**
- Diagnosis: one sign. With 5/(48i) changed to 5i/48, the form satisfies δc0″ exactly and matches the ray integrals
  to 1e−32 at 3 test points.
- I₊ by quadrature with the independent ray-integral δc0 is −0.02433618209447682 + 0.02323006896108698i. That equals
  Neon's interval-certified value to 9e−16, and I₋ = −conj(I₊) holds exactly. Neon's computations used the correct
  function; the error is in its write-up.
- I₊ does not depend on constant shifts of δc0 (W₊ is holomorphic inside the circle), so Neon's E → ∞
  non-vanishing argument is unaffected.

**F2.**
- **First run, deviation recorded.** It used Neon's written closed form, contrary to the prereg ("δP from F1"), and
  gave c_pred = −2.84e−3: a 41% miss, caused by the typo.
- **Run as registered.** δc0 = the ray-integral function, implemented through the sign-corrected form proven
  identical above. The symbolic checks pass: P0 = N₋/D₋ exactly, and v± = (N₋D₋)^{1/4}e^{±κu} with
  κ² = −a²(E² − 1) solves the k = 0 NVE exactly.
- J0, J±, a first-order quantity, give the prediction c_pred = −(J₊J₋ − J0²)/(4κ²) = **−4.784472e−3**. The V26-D
  direct-ODE value (two independent codes, Bridge and ansatz) is −4.78447e−3. **Relative difference 5.2e−7. PASS.**
- The must-fail control (a wrong q1) misses by 100%.

**Reading.**
- Neon's first-order perturbation theory (δc0, q1, the k = 0 basis, the variation-of-parameters monodromy) is
  confirmed quantitatively against the basis-free invariant that two codes measured independently.
- The key non-vanishing constant I₊ is confirmed independently.
- The remaining steps of T8's proof have been read by the Bridge, not machine-checked:
  - the E → ∞ continuation;
  - the Kovacic-classification exclusion (Borel by tr[M1, M0] ≠ 2, D∞ by nonzero traces, finite groups by tr M1);
  - region monodromy ⊆ Gal over M(Ω).

  These are standard; tr M1 ∉ T_fin needs a number.
- **Status of the invisible-family obstruction:** "proved (Neon T8), with the first-order core verified (V26-F) and
  the non-vanishing constant independently confirmed". It is no longer "numerical only". A second fleet reader is
  wanted for the group-theory step before outreach.

## Addendum G (2026-11-21 ~06:00): Neon T11, all spins a. **G1 PASS; G2 FAIL as registered (Bridge tolerance slip), every substantive clause PASS**
Code: code/v26_G.py. Outputs: results/v26_G.txt; results/v26_G_postdiag.txt (labelled post-result).

**G1 PASS.**
- Neon's general-a δc0, which carries the corrected sign, satisfies δc0″ = Q/(2D³c_K″) to 1e−171 for
  a ∈ {1/10, 3/5, 1, 2}.
- It tends to 0, with leading term 7a/(30z²).
- (c0″)² = (8/(5a⁶(u² + 1)⁶))·B(u², k) holds identically, and disc_w B = 240k(k − 4).
- The T8-as-written sign fails the identity (7.2), so the control fires.

**G2.** By independent ray-integral quadrature:

| a | I₊(a) | Neon's |I₊| |
|---|---|---|
| 0.1 | −6.7546e−4 − 1.3417e−4 i (abs 6.887e−4) | 6.89e−4 ✓ |
| 0.6 | −0.0243362 + 0.0232301 i | (T8 value) |
| 1.0 | −0.135011 + 0.240097 i (abs 0.27545) | 0.275 ✓ |
| 2.0 | −0.565637 + 1.345780 i | — |

- I₊(0.6) on |z| = √1.36 equals the T8 value on |z| = 1.35 to 3.4e−18 (contour independence).
- Re I₊ < 0 at all four values of a.
- **Registered clause "|I₊/(−7πa³/30) − 1| < 1% at a = 0.01": FAIL** (0.0200).
  - Cause, the Bridge's: the tolerance ignored the O(a⁴) correction that Neon stated. This is a control-clause slip:
    the clause was not checked against what the true asymptotic can produce.
  - Post-result diagnostic (labelled): (ratio − 1)/a = 1.99824i, 1.99984i and 1.99998i at a = 0.01, 0.003 and
    0.001. So I₊(a) = −(7π/30)a³(1 + 2ia + O(a²)), and Neon's leading asymptotic is confirmed. The next
    coefficient, 2i, is new.
- The must-fail (7π/15) gives a ratio of ≈ 0.50, so the control fires.

**Reading.** T11's checkable core is confirmed for every a tested. I₊(a) ≢ 0 is then a rigorous consequence of
analyticity plus the small-a asymptotic. Not machine-checked here:
- the large-E loop construction in Re z > a;
- U_a = (−∞, 30/7), which Neon only marks CHECKED.

- **Timestamp correction (appended 2026-11-21 04:10 IST, system clock).** The '~hh:mm' times written by the Bridge in tonight's addenda (V25 C; V26 D–G) were estimated and run about 1.5–2 h FAST. The commit timestamps in git are authoritative.

## Addendum H (2026-11-21 ~05:50, received from ansatz plus a labelled Bridge extension): the group step of Neon T8 confirmed at 50 digits
**ansatz, blind to Neon's file (f67ae8f, 22969bd).**
- The k² coefficient of tr(g_in) − 2 is:
  - c(0.7) = −1.928286675e−2;
  - c(0.8) = −4.784472498e−3;
  - c(0.9) = −1.262102689e−3.
  These come from an exact cubic in k; the radius and step controls agree.
- Two-loop commutator at E = 0.8.
  - Loops: M0 is |z| = 1.35; M1 is a rectangle around {1.934, 2 + 0.6i} with a real-segment tail.
  - tr M1 = −0.98431 + 2.77728i at k = 0, varying slowly with k, so it matches Neon.
  - tr[M1, M0] − 2 = 1.94e−5 + 9.88e−6i at k = 1/100 (modulus 2.18e−5) and modulus 2.21e−3 at k = 1/10.
    Neon's numbers are these moduli.
  - k = 0 gives ≤ 3e−40.
  - Must-fail: a loop around the other class gives a different, real trace.
- **Basis-free group step.**
  - tr[M1, M0] ≠ 2, so the pair is irreducible.
  - tr M1 ≠ 0 and tr M0 ≠ 0, so it is not imprimitive.
  - tr M1 is non-real, so the group is not finite.
  - Hence the Zariski closure is SL2 at k ∈ {1e−2, 1/30, 1/10} and E = 0.8.
- **Caution (ansatz).** tr[M1, M0] depends on the based class of the pair, i.e. M1's tail. Only the modulus is
  comparable with Neon unless the tails match.

**Bridge extension (post-registration, labelled, descriptive; results/v26_F_extension_E.txt).** The V26-F
first-order prediction c_pred = −(J₊J₋ − J0²)/(4κ²), against ansatz's 50-digit c(E):

| E | Relative difference |
|---|---|
| 0.7 | 8e−12 |
| 0.8 | 6e−11 |
| 0.9 | 4e−10 |

**Status of the invisible-family obstruction (K4).**
- Neon's analytic proof (T8, T11) has its first-order core verified to about 1e−11 at three energies, against an
  independent 50-digit direct computation.
- The group-theory step is confirmed numerically and basis-free by ansatz.
- The general-a identities are exact (V26-G).
- What remains:
  - U_a = (−∞, 30/7) is CHECKED, not proved (Neon T14 is attempting interval certification);
  - the large-E loop construction in T11 has been read, not machine-checked.

## Addendum I (2026-11-21 ~06:30): Neon T14, U_a certificate. **I1 PASS; I2 FAIL as registered (Bridge clause slip); every Neon bound consistent**
Code: code/v26_I.py. Outputs: results/v26_I_precheck.txt, v26_I.txt, v26_I_postdiag.txt (labelled).

**I1 PASS.** Neon's finite-interval ray representation of c0 matches the INDEPENDENT B8 ODE continuation to
≤ 6.7e−15 at 12 points. These cover k ∈ {−5, 0.1, 4.2}, including 4 < k < 30/7, and points on Re z = 1 and beyond.

**Controls (pre-checked).**
- The x²(1 − x) variant fires (0.42).
- At Neon's wall, k_wall = −22.5906090375, the B8 continuation gives |f0² + c0²| = 9.4e−8. That independently
  confirms the wall location.

**I2 FAIL as registered.**
- The clause compared the whole grid (η up to 200) with Neon's certified bound 7.006e−5, which only covers
  η ∈ [0, 10]. For η ≥ 10 Neon claims analytic tail bounds instead.
- The grid minimum, 1.09e−5 at (θ = 1, η = 200), is BELOW 7.006e−5 but above the regime-B tail bound
  0.062/(1 + η²) = 1.55e−6.
- This is a Bridge clause slip, the fourth tonight: the clause was not matched to the region of the claim. The
  pre-check rule covers controls, not target clauses. Extension: target clauses must also be matched to the
  claim's stated domain.

**Post-result diagnostic (labelled).**
- η ∈ [0, 10]: minimum 4.34e−3, consistent with the certified bound.
- η ∈ [10, 200], regime A: Re H̃ − 0.445 ≥ 0.036.
- η ∈ [10, 200], regime B: Re H̃ − 0.062/(1 + η²) ≥ 9.4e−6.
- Every bound Neon claims holds on the grid.

**Reading.**
- The representation is independently confirmed.
- The float grid is consistent with the certificate and with both analytic tail bounds.
- The inequality chain (|1 + w²| ≥ Re w for Re w > 0; c0/f0 = H/(y² + 1 − a²) on Re z = 1) and the θ-reparametrisation
  of B were checked by hand.
- The 935-box interval certificate itself has not been re-run by the Bridge.
- The minimum-principle step is standard. Branch points of the integrand lie at u = x·u_root, which is inside |u| < 1
  or on the imaginary axis, so the integrand is holomorphic on Re u ≥ 1.
- **Status of U_a = (−∞, 30/7) for all a ∈ (0, 1):** proved (Neon T14), with the representation verified, the
  bounds consistent, and the wall independently confirmed. Interval certificate not re-run.

## Addendum J (2026-11-21 ~09:40): INDEPENDENT interval certificate of Neon T14. **PASS**
Code: code/v26_J.py. This is the Bridge's own complex-interval arithmetic on mpmath.iv (20 digits); Neon's code was
not used. Outputs: results/v26_J_precheck.txt, results/v26_J.txt.
- Re H̃_θ(1 + iη) > 0 is certified on all of [0, 1] × [0, 10]: **449 boxes, minimum certified lower bound 6.04e−6**.
  Neon independently reported 935 boxes with minimum ≥ 7.0e−5; the bounds differ because the box sizes differ, as
  expected.
- Controls (pre-checked):
  - the enclosure is valid at 6 random points;
  - the must-fail Re H̃ − 0.01 is refused at (θ, η) ≈ (1, 10).
- Development note, honest: the first three runs crashed on interval-arithmetic implementation issues (operator
  order, endpoint conversion, dependency in |u²| and in R + X). These were fixed by exact identities (|u|² = 1 + η²;
  R + X ≥ 2X, and R + X = Y²/(R − X)) BEFORE the target run. The pre-checks were re-run after each fix.
- **Status of U_a = (−∞, 30/7) for all a ∈ (0, 1):**
  - the compact region is certified twice, independently (Neon and the Bridge);
  - the ray representation is independently confirmed (V26-I);
  - the tail bounds hold on a grid (V26-I);
  - the analytic tail proof has been read once.
  - This pre-outreach item is DONE.

---
## Addendum K (2026-11-21, runs ~11:45-11:54 real clock; the "~12:20" in the prereg header was a mis-estimate, the commit times are the record): the Bridge's independent check of Neon T19 (G1 gap)
**VERDICT:** K2 is FAIL as registered (a Bridge enclosure defect). Every other clause PASSES, and the labelled
amendment K2′ PASSES. Together, every piece of T19's proof that the Bridge set out to check is independently confirmed.
Environment: CPython 3.14.5 (conjecture_machine/.venv), mpmath iv at dps 20, numpy as in ENVIRONMENT.

| Clause | Region (Neon's own) | Result |
|---|---|---|
| K0 E-elimination identity | exact | PASS (sympy) |
| K1 Re(H~^2) > 0 | theta [0, 7/37], eta [0, 10] | PASS: 251 boxes, min certified margin 0.0354 |
| K2 theta^-1/2 \|Im H~\| < 1 | theta [7/37, 1], eta [0, 5] | **FAIL as registered**: stuck at theta ~ 1, eta ~ 5 (enclosure blow-up) |
| **K2′** (amendment: tight enclosure) | same | **PASS**: 538 boxes, min certified margin 6.3e-4 (so the maximum is <= 0.99937; Neon's bound was 0.99844) |
| K3A Re H~ - \|Im H~\| > 0, left edge | theta [7/37, 1], eta [0, 1] | PASS: 2,389 boxes, min certified margin 6.6e-5 (374 s) |
| K3B the same, top edge | theta [7/37, 1], x0 [1, 5] | PASS: 749 boxes, min certified margin 4.2e-5 |
| K4 end-to-end winding = 2 | 24 random + 4 edge (a, k, E) | PASS: 28/28 give exactly 2.0000 |
| K5 tail sanity (float, not rigorous) | eta >= 10 / >= 5; x0 >= 5 | PASS: grid minimums 0.757 / 0.916 / 1.45e-3 |

**Notes:**
- K3A′ was not needed (K3A passed as registered). It was started early, as a precaution, and killed unread.
- K2′'s certified margin of 6.3e-4 is thin, as Neon's was. The bound that Case 2a needs (< 1) holds.
- K4 coverage is skewed: of the 24 random draws only 1 has k in (0, 30/7), because k was uniform on (-30, 4.28).
  That range is covered by the certificates and by the edge cases (k = 4.27 and 4.2857).
- The K3 tail grid minimum (1.45e-3, top edge for x0 >= 5) is small but positive, consistent with Neon's
  argument-angle bound. The tail arguments themselves were read by hand, not certified.

**Reading.** T19's closing of the G1 gap holds under an independent implementation:
- the exact E-elimination;
- all four interval certificates;
- an end-to-end zero count.
Together with V26-J (T14's U_a), the general-spin loop argument for the invisible family has no open numerical step.
The remaining caveat is that the tails and the inherited holomorphy (from U_a) were read by hand, not machine-checked.

**Process record:**
- The first pre-run caught three Bridge harness errors.
- A K5 control was found to be target-dependent and replaced (disclosed).
- K2's registered failure was an untested tightness property: a new rule in memory requires width checks at the
  domain corners.
