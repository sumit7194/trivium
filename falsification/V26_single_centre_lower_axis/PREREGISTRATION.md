# V26: independent check of Fable's single-centre result (lower-axis route). Bridge, 2026-11-20 evening, before any code
**Claim under test** (fable_work/only_kerr_single_centre/REPORT.md):
- **(L)** On an asymptotically flat solution, the axis data below the source are e_-(z) = 1/e_+(z). Equivalently
  ξ_-(z) = −ξ_+(z), with ξ = (1 − e)/(1 + e) and e_+ continued analytically in z.
- **(N)** Rational, asymptotically flat, single-centre data (f0 with one pole, simple or double, or f0 ≡ 1) with
  c0 ≢ 0 give deg f0^- ≥ 4, where f0^- = f0/(f0² + c0²).
- Hence first-order obstruction on the lower axis.

The Bridge works only from the claim statements. Fable's scripts are NOT run or reused.

## Checks
**L-src.** Read Meinel–Neugebauer, CQG 12 (1995) 2045 (arXiv:gr-qc/0302114) in the original PDF, and quote the
relation they state between the two axis potentials.
- PASS if it states (L), or something equivalent to it, under stated hypotheses.

**L-proof (by hand, Bridge).** A parity induction on ξ = Σ r^{−(n+1)} F_n(cos θ).
- Show F_n(−u) = (−1)^n F_n(u), using:
  - the Ernst equation for ξ;
  - regularity of F_n on [−1, 1] (both axes regular);
  - the kernel of the order-n Legendre operator.
- Write it out in FINDINGS. It must identify every hypothesis used.

**L-num (own code).**
- **Method.** Solve the Ernst equation for ξ order by order in 1/r (sympy, exact rationals), from random complex
  upper-axis moments, to order 10. Use 3 random seeds and 1 seed with real moments (the static control).
- **PASS** if ξ(θ = π) = −ξ_+ exactly, at every order.
- **Must-fail.** At the same orders, the "mirror guess" e_-(z) = e_+(−z) and the guess e_- = conj(e_+(z)) must both
  be violated for a twisted, non-reflection-symmetric seed.
- **Exact controls (closed form, no series):**
  - Kerr–NUT with ξ = e^{iα}(px + iqy);
  - Tomimatsu–Sato δ = 2 from the V11 loader's Ernst potential (if available), or the standard α/β form;
  - Schwarzschild in Weyl coordinates.
  - Compare the actual axis values at y = ±1 with the rule.

**N-count.** For e = 1 − 2M/z + i b/z² (M = 1; b ∈ {1/2, 1, 3}): compute f0^- exactly, factor it, and list the
poles and zeros of P = E² − μ² f0^- at a generic E.
- **Expected:** 4 simple poles + 4 simple zeros (s + 2h = 8 > 4).
- **Control:** c0 = b/z (Kerr–NUT-type) gives s + 2h ≤ 4.

**N-search (adversarial).** Search for asymptotically flat rational e with single-centre f0 and c0 ≢ 0 such that
deg f0^- ≤ 2.
- **Families:**
  - e = (polynomial of degree d)/(polynomial of degree d), d ≤ 3, with the pole structure of f0 forced to one
    real point;
  - symbolic parametrisation for d ≤ 2;
  - random rational-parameter scans for d = 3.
- **PASS** (= supports N) if none is found.
- **Must-find control:** dropping asymptotic flatness, the search must find the Kerr–NUT-type twist in class D.

## Verdict
(L) and (N) are CONFIRMED if L-src, L-proof and L-num pass, and N-count and N-search pass.

**Not covered here:**
- B1 (an exact twisted single-centre metric off the axis);
- B3/B7 (certified lower-axis monodromy);
- the first-order classification, which is inherited from ansatz §158.

## Addendum A (2026-11-20, late evening, before code): B6, static double-pole data seen from below
**Claim.** Static class C, f0 = (z² − 2Mz + q)/z² with q ≠ 0 and q ≠ M² (distinct zeros). Seen from below,
f0^- = 1/f0 = z²/(z² − 2Mz + q) = 1 − m1/(z − z1) − m2/(z − z2), where:
- z1, z2 are the roots of z² − 2Mz + q;
- m1 = −z1²/(z1 − z2) and m2 = −z2²/(z2 − z1), both ≠ 0;
- c0^- = 0.

This is two-centre data with zero twist. Theorem 1 (V25) then obstructs it at third order: closed form
F = 1 + r1²/m1² = 1.

**Check.** Bridge V25 code (v25_rmap.py return map on the truncated system R; V25 P3 machinery), applied to f0^-:
- **(i)** real roots: M = 1, q = 3/4 (z = 3/2, 1/2), at E = 0.8 and 0.6;
- **(ii)** complex roots: M = 1, q = 5/4 (z = 1 ± i/2), at E = 0.8 and 0.6.
- **PASS:** the cubic return-map coefficients A match the closed form with F = 1, by the V25 P3 rule (error
  ≤ max(100·floor, 1e−6·scale)), and are nonzero, with no VOID.

**Controls**
- **Cancellation control:** the same f0^- with the complexified reference twist (c0 = c_ref) must give A ≈ 0 (F = 0).
- **Exact check:** ZV δ = 2 (q = M²) from below has a double pole (f0^- = z²/(z − M)²). So it is not two-centre and
  stays undecided, as claimed.

## Addendum B (2026-11-20, late evening, before code): item 2 (regularity of the lower outer axis), instead of a full exact metric
**Why the change.**
- B1's first aim (does the lower-axis value equal 1/e_+?) is now settled by L-src, L-proof and L-num. The series IS
  the solution off the axis near infinity.
- What remains open is the physical caveat: is the lower outer axis regular, with no Misner string and no conical
  defect, for asymptotically flat twisted data?

**Argument (by hand, to check).** In Weyl–Papapetrou form, ∂_θ ω = r² sin θ ∂_r χ / f², where χ = Im e. So the jump of
ω between the two outer axis segments, along a large semicircle, tends to −2 × (the 1/r coefficient of χ), i.e. to
the NUT parameter. With c0 = O(z⁻²) there is no jump. ω is constant along each regular axis segment, so both are
zero. γ → 0 at infinity on both segments likewise.

**Check (own series code, v26_L solver).** Take e_+ = 1 − 2/z + i b/z² (b = 1), to order 10, and compute
Δω(R) = ∫₀^π R² sin θ ∂_r χ / f² dθ at R = 20, 40, 80.
- **PASS:** |Δω| decreases like R^{−1} or faster, towards 0.
- **Must-fail control:** add a NUT term (+ i n/z, n = 1/2). Δω must tend to −2n·(sign convention), i.e. a nonzero
  limit, within 1e−2 at R = 80.

## Addendum C (2026-11-20, late evening, before code): B8, the invisible non-rational family seen from below
**Family** (DEGREE2_FAMILIES §6; Kerr M = 1, a = 3/5; Fable's coordinates).
- f0 = 1 − 1/(z − ia) − 1/(z + ia).
- (c0″)² = (c_K″)² + α Q/D³, with:
  - c_K = −2a/(z² + a²);
  - D = z² + a²;
  - v = (z + ia)/(z − ia);
  - Q = v³ + v⁻³ − (3/5)(v + 1/v) − 4/5.
- c0 is fixed by asymptotic flatness: c0, c0′ → 0 at ∞, continued from z = +∞ along the real axis. The branch of c0″
  is continuous with c_K″.
- **Lower axis:** f0^- = f0/(f0² + c0²), P = E² − f0^-, NVE v″ = −(3/16)(P′/P)² v.

**Method (own code).**
- Integrate (c0, c0′, c0″) and the NVE fundamental matrix together along loops from a base point z_b = 4. The ODE
  for c0″ is c0‴ = (c0″²)′/(2c0″), which tracks the branch.
- Use 4 loops, each around one simple singular point of the lower NVE: the two poles of f0^- near 2 ± ia, and the
  two zeros of P on the base sheet. Locate them from the Kerr values, then refine by Newton on the continued
  functions. Each loop stays in |z| > 1.3.
- Integrator: DOP853 (complex) at rtol 1e−13, and repeat at rtol 1e−11 to measure the floor.

**Gates per run.**
- Each loop matrix has trace 0 (one simple point inside) to ≤ 1e−9, and determinant 1 to ≤ 1e−10.
- c0 and c0′ return to their start values after each loop to ≤ 1e−9. This shows c0 is single-valued there.

**Statistic.** S = max over pairs of commutators K = [M_i, M_j] of ‖K K′ − K′ K‖ (a non-abelian derived subgroup).

**Grid.** α ∈ {0, 1/100, 1/30, 1/10} × E ∈ {0.7, 0.8, 0.9}.

**PASS (obstructed)** if, for α ≠ 0:
- S ≥ 100 × the α = 0 value and ≥ 100 × the rtol-difference floor, at every E;
- S scales ~linearly in α for small α (fit α ∈ {1e−3, 3e−3, 1e−2} at E = 0.8; slope 1 ± 0.2 in log–log).

**Controls**
- **α = 0 (Kerr from below)** must sit at the floor.
- **Positive control:** the rational twisted single-centre data e = 1 − 2/z + i/z², seen from below (deg f0^- = 4),
  through the same pipeline (loops around its 8 singular points, or a subset of 4), must give S = O(1).

**Reading.**
- A non-abelian derived subgroup with elements arbitrarily close to the identity means the group is not virtually
  abelian, so it is obstructed.
- Numerical evidence, not a certificate. Fable's own numbers are known (REPORT §8). This is a reproduction with
  independent code, and those numbers are not used as a target.

## Addendum D (2026-11-21 ~03:00, before code): basis-free cross-check proposed by ansatz after unblinding
ansatz reports tr(g_in) − 2 = −4.7845e−3·k² at E = 0.8, where g_in is the monodromy of the lower-axis NVE (invisible
family) around the circle |z| = r, 1.3 < r < 1.9. The value is independent of basis and of any normalisation. The
Bridge recomputes it with the V26-B8 model code (Model, kerr_funcs, base_state_kerr), unchanged.

**Method.**
- Carry c0 only, along the real axis from z_b = 4 to z = r.
- Integrate the full system once round |z| = r, starting from the identity. Use DOP853 at rtol 1e−13, with 1e−11
  as the floor.

**D1 (PASS).**
- At r = 1.35, for each k ∈ {1e−3, 1e−2, 1/30, 1/10}, (tr − 2)/k² agrees with −4.7845e−3 to 1% at the smallest
  two k. At larger k, ansatz's own values set the target: k = 1/100 gives −4.79093e−7, k = 1/10 gives −4.85001e−5.
  Agreement to 1% is required.
- At every k, |tr(r = 1.6) − tr(r = 1.35)| ≤ 1e−9, the free-homotopy invariance check.
- The gates hold: |det − 1| ≤ 1e−10, and c0 returns to itself within 1e−9.

**D2 controls.**
- k = 0 must give |tr − 2| ≤ 1e−9.
- **Must-fail.** r = 2.5 is a different class: it also encloses the turning point near 1.93 and the poles 2 ± 0.6i.
  Its tr − 2 must differ from the r = 1.35 value by more than 1e−6 at k = 1/10, or by an O(1) amount.

## Addendum E (2026-11-21 ~03:30, before code): checking Gemini Neon T3's concrete claims
Neon's output: /Users/sumit/Github/neon_work/onlykerr/T3_REPORT_SUMMARY.md. It is UNVERIFIED until this check.

**E1 (Theorem 1, degree classification).** With z1 = 0, f0 = 1 − 2M/z, c0 = P/Q (deg P < deg Q = d, gcd 1, real
coefficients) and f_- = f0/(f0² + c0²), the claimed degree of the reduced denominator is:

| Case | Claimed degree |
|---|---|
| c0 = 0 | 1 |
| c0 = −2n/z | 2 |
| Q(0) ≠ 0 | 2(d + 1), or 2d + 1 when P(2M) = 0 |
| Q = z^k·Q̃, k ≥ 1 | 2d, or 2d − 1 when P(2M) = 0 |

The last two rows cover every other case, and all of them have degree ≥ 3.

- **Test.** sympy, exact: 60 seeded random examples spread over the four structural cases, with M = 1 and small
  integer or rational coefficients. Cases with P(2M) = 0 are built by construction.
- **PASS:** every computed degree equals the claimed one, and every non-Schwarzschild, non-NUT case has degree ≥ 3.
- **Must-fail control:** the claimed formula applied with k and Q̃ swapped, or without the P(2M) correction, must
  mismatch on at least one example.

**E2 (Theorem 2, ZV δ = 2).** Bridge's own derivation of the equatorial NVE1 from
2H = −E²/f + f e^{−2γ}(x² − y²)⁻¹[(x² − 1)p_x² + (1 − y²)p_y²], with f = ((x − 1)/(x + 1))², e^{2γ} = ((x² − 1)/(x² − y²))⁴,
L = 0, μ = 1, E = 2.
- Linearise in (y, p_y) at y = 0, use x as the independent variable, and take the Liouville normal form u″ = r(x)u.
- **PASS:**
  - r(x) equals Neon's r exactly (sympy simplify of the difference gives 0);
  - the Frobenius obstruction at x = 0 for the smaller exponent is nonzero (Neon: −38);
  - an exact Kovacic Case 1 search (all exponent choices; polynomial solvability) finds no solution.
- **Must-pass control:** Schwarzschild, δ = 1, f = (x − 1)/(x + 1), e^{2γ} = (x² − 1)/(x² − y²). Neon says q ≡ 0 there,
  so a Case 1 solution must exist. If the search finds none, the search code is wrong.
- **Literature note:** ZV non-integrability is known (Maciejewski–Przybylska–Stachowiak, PRD 88, 064003, 2013; it
  was cited in the T3 prompt). E2 tests Neon's re-derivation, not novelty.

## Addendum F (2026-11-21 ~04:25, before code): checking Neon T8's first-order proof of the invisible-family obstruction
Neon's output: neon_work/onlykerr/T8_INVISIBLE_FAMILY_SUMMARY.md.

**F1 (δc0 and I₊, independent route).**
- Compute δc0 and δc0′ on |z| = 1.35 by ray integration of δc0″ = Q/(2D³c_K″) from z to ∞ along z·s, s ∈ [1, ∞)
  (mpmath, 30 digits). Neon's closed form is NOT used for this.
- Compare with Neon's closed form at 8 points on the circle. **PASS:** agreement within 1e−15.
- Compute I₊ by quadrature on the circle. **PASS:** |I₊ − Neon| ≤ 1e−10·|I₊|, and I₋ = −conj(I₊) within 1e−12.
- **Must-fail:** Neon's closed form with its two log-ratio terms dropped must disagree by more than 1e−3.

**F2 (first-order theory against the V26-D ODE invariant).**
- At E = 0.8, from Neon's formulas (v±, u, κ, q1, with δP from F1), compute J±, J0 on |z| = 1.35 (base point 1.35).
- Predicted coefficient: c_pred = −det(Δ) = −(J₊J₋ − J0²)/(4κ²), with tr(g_in) − 2 = c·k² + O(k³).
- V26-D target: c = −4.78447e−3. This is the k → 0 linear extrapolation from k = 1e−3 and 1e−2; the k = 1e−3 value
  alone is −4.78512e−3.
- **PASS:** |c_pred/c − 1| ≤ 1e−3.
- **Must-fail:** the same computation with q1 replaced by (3/16)(δP/P0)′² (a wrong first-order variation) must miss
  by more than 1%.

## Addendum G (2026-11-21 ~05:40, before code): checking Neon T11 (all spins a)
**G1 (sympy, exact).**
- Neon's general-a δc0 satisfies δc0″ = Q/(2D³c_K″) identically, with symbolic a. Check at 3 rational points for each
  a ∈ {1/10, 3/5, 1, 2}, to exact 0.
- It tends to 0 at +∞, with leading term 7a/(30z²).
- (c0″)² equals (8/(5a⁶(u² + 1)⁶))·B(u², k) identically.
- disc_w B = 240k(k − 4).
- **Must-fail:** the T8-as-written sign must fail the δc0″ identity.

**G2 (independent quadrature).**
- Compute I₊(a) = ∮_{|z|=√(1+a²)} (f0^-)′(δP)′(z − 2 − ia)² dz, with δc0 and δc0′ from ray integrals of δc0″ (not
  Neon's closed form), for a ∈ {0.1, 0.6, 1.0, 2.0}, at 20 digits.
- **PASS:**
  - |I₊| matches Neon's 6.89e−4 (a = 0.1) and 0.275 (a = 1) to its 3 quoted figures;
  - I₊(0.6) on |z| = √1.36 equals the T8 value on |z| = 1.35 (contour independence) to 1e−12;
  - Re I₊ < 0 at all four values of a;
  - I₊(a)/(−7πa³/30) at a = 0.01 lies within 1% of 1.
- **Must-fail:** the asymptotic with 7π/30 replaced by 7π/15 must miss by more than 40% at a = 0.01.

Not checked here: the U_a separation claim, and the large-E loop construction (both read only).

## Addendum I (2026-11-21 ~06:20, before the target run; controls pre-checked per the new rule): checking Neon T14 (U_a = (−∞, 30/7) for all a)
Code: code/v26_I.py. Neon's output: neon_work/onlykerr/T14_UA_SUMMARY.md (to be written).

**I1.** Neon's finite-interval ray representation of c0(z; k) is
c0 = −(√(8/5)/a)∫₀¹ x(1 − x)u⁻²(1 + x²u⁻²)⁻³√(c4 + c2x²u⁻² + c0′x⁴u⁻⁴) dx.
- Compare it with the INDEPENDENT V26-B8 ODE continuation of c0 (path 4 → 4 + i·Im z → z, rtol 1e−12, a = 0.6).
- Values: k ∈ {−5, 0.1, 4.2}; z ∈ {1 + 0.5i, 1 + 3i, 1 − 2i, 2.5 + i}.
- **PASS:** max difference ≤ 1e−8.

**I2.** A dense float grid of Re H̃_θ(1 + iη):
- θ ∈ [0, 1], 201 points;
- η ∈ [0, 10] with 401 points, plus η ∈ [10, 200] with 191 points.
- **PASS:** the grid minimum is ≥ 7.006e−5, Neon's certified lower bound (a certificate lower bound must not exceed the
  true minimum), and is > 0.

**Control table (pre-checked; results/v26_I_precheck.txt).**

| Control | Type | Pre-check result | Status |
|---|---|---|---|
| x²(1 − x) instead of x(1 − x) at z = 1 + 0.5i, k = 0.1 | must disagree, > 1e−3 | 4.2e−1 | FIRES ✓ |
| Wall crossing (Neon's k_wall = −22.5906090375, z_wall = −0.36260544 + 1.10838499i), via B8 continuation | must give ≈ 0 | \|f0² + c0²\| = 9.4e−8 vs \|f0\|² = 7.67 | ✓ |

The wall control independently confirms Neon's wall location to the precision of the digits given.

## Addendum J (2026-11-21 ~09:30, before the target run; controls pre-checked): the Bridge's INDEPENDENT re-run of Neon T14's interval certificate (one of the pre-outreach checks Sumit asked for)
Code: code/v26_J.py. This is the Bridge's own complex-interval arithmetic on mpmath.iv; Neon's script was not used.

**Claim re-certified.** Re H̃_θ(1 + iη) > 0 for all (θ, η) ∈ [0, 1] × [0, 10].

**Method.**
- Lower bound for Re∫f dx = Σ_i (1/M)·min(Re f over x-cell × box).
- 1/u² is taken from the exact |u|² = 1 + η².
- The principal-sqrt enclosure uses the exact lower bounds of R + X; cells that touch the branch cut fall back to the
  rigorous bound Re f ≥ −|f|.
- Adaptive bisection in (θ, η), with M = 24, 48 or 96 x-cells by box size.

**PASS:** every box is certified, with a positive minimum certified lower bound.

**Control table (pre-checked; results/v26_J_precheck.txt).**

| Control | Type | Pre-check result | Status |
|---|---|---|---|
| Enclosure validity at 6 random tiny boxes (M = 400) | must-pass: lower ≤ float value | gaps 5.6e−4 to 9.2e−3 | ✓ |
| Must-fail: certify Re H̃ − 0.01 > 0 | must NOT certify | refused at (θ, η) ≈ (1, 10), where Re H̃ ≈ 4.3e−3 (V26-I grid) | FIRES ✓ |

**Scope.** The analytic tail for η ≥ 10 is not re-proved here; it was read, and checked on a grid in V26-I.
