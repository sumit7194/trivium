# V25 FINDINGS, part 1 (Fable's check P1): near-axis series. **CONFIRMED**

*2026-11-20. Pre-registration 1ac330d. One implementation fix before any result existed: the first run crashed in the
Vandermonde solve (an ill-conditioned matrix), so the fit was rescaled by t/1e−4. No result was seen before the fix.*

The Bridge's own TS2/Kerr/ZV metrics, its own static-Weyl ρ⁴ series (sympy), and mpmath at 50 digits; z ∈ {2.5, 4, 7}.

| | TS δ=2 (twisting) | Kerr (twisting) | ZV δ=2 (static) |
|---|---|---|---|
| Gate (12- vs 16-point fit) | ≤ 1.4e−24 | ≤ 1e−24 | ≤ 1.4e−24 |
| F1₂, F2₂ vs the twist-free formulas (relative) | ≤ 1.7e−29 | ≤ 1e−29 | ≤ 1.7e−29 |
| (F1₄ − F1₄^static) / (−(c0″)²/(64f0)) | **1.0000000000** (all 3 z) | **1.0** | — (difference ≤ 1.3e−26; twist 0) |
| (F2₄ − F2₄^static) / (−(c0″)²/(64f0³)) | **1.0** | **1.0** | — (≤ 2.6e−24) |
| Must-fail (1.1·c0″) | 0.8264 = 1/1.21: fires | | |

- The static ρ² formulas also match the claimed ones symbolically (difference 0).
- **Verdict: CONFIRMED.** The twist enters the near-axis Hamiltonian at ρ⁴ only, and exactly as −(c0″)²/(64f0)
  (F1) and −(c0″)²/(64f0³) (F2). That now holds on a twisting non-Kerr exact solution (TS δ=2) as well as on Kerr, with
  a static-Weyl ρ⁴ part derived independently.

**Still open (P2–P6 and the rest):**
- the third-order return maps on full metrics (P2: Kerr zero, static twin (−π/2, π));
- the residue sweep (P3); Lemma P and the invisible family (P4); the two-rod example (P5); ZV and Schwarzschild (P6);
- the Galois step;
- the inherited first-order classification.

## Addendum A: P3 and P4 (2026-11-20)
Code: code/v25_rmap.py (system R loop machinery), v25_p3.py, v25_p4.py. Results: results/v25_p3.json (first run),
v25_p3_A1.json (amendment A1), v25_p4.json.

### P4(i): Lemma P's three-term identity. CONFIRMED (exact)
- With F = v^k divided through by v^{k−2}, the difference lhs − rhs cancels to 0 exactly. This holds for symbolic k
  and w ∈ {2, 4}, and at 7 integer k spot values in the undivided form.
- **First attempt (my own issue):** sympy could not combine v^k powers for symbolic k and printed an unsimplified
  expression. The division form avoids that.

### P4(ii): admissible principal parts. CONFIRMED
- Own residues from local series in t = √(z − z1), 60 digits, pole order ≤ 12, 20 energies × weights 2 and 4.
- Kerr-type, Kerr–NUT-type and real-pole parameters.
- **In all three cases:**
  - the null space has dimension exactly 1 (singular-value gap ≥ 4.7e51);
  - the null vector equals the principal part of v³ − (3m2/(5m1))v to ≤ 6e−53;
  - |A·x| ≤ 2e−58.
- **First attempt:** the complex cases looked misaligned because I took a row of Vh instead of its conjugate (the null
  vector of A is conj(Vh row)). That was my bug, fixed before any verdict was recorded.

### P3 (closed-form residue sweep) and P4(iii) (invisible family) with own R-trunc
- **First run: VOID as registered.**
  - The VE_1 self-check code used d/ds = Δy d/dz (wrong), so it failed at relative error ~1.
  - 6/13 floors exceeded 1e−4, from the ε⁴ Richardson residual.
  - The values already agreed with the predictions to ≤ 1.7e−5.
- **Amendment A1 run.** Corrected self-check at 5 loop points: ≤ 8.5e−10. Two-level Richardson. Floors 6e−9 to
  1.7e−7. **All 13 MATCH:**

| case | A from start (1, 0) | prediction |
|---|---|---|
| Kerr f0 (M=1, a=3/5), E=4/5, twist λ c_ref, λ = 0 / ½ / 1 / 3/2 | (−1.5707963, 3.1415927) / (−1.1780972, 2.3561945) / (1.6e−8, 1e−8) / (1.9634954, −3.9269908) | F = 1 − λ²: (−π/2, π)·F |
| the same, E = 7/10, λ = 0 | (−1.5707963, 3.1415927) | E-independent |
| Kerr a = 4/5, E = 13/10 (unbound), λ = 0 | (−1.1780972, 2.3561945) | (−3πM/(10a), 3πM/(5a)) |
| Kerr–NUT type, λ = 0 / 0.7 | (−1.8849556 − 0.7539822i, …) / (−0.9613274 − 0.3845309i, …) | to ≤ 4e−8 |
| real poles: c0 = 0 / real twist / complexified reference | −0.6283185i / −0.9075712i / ~1e−8 | F = 1 / 13/9 / 0 |
| P4(iii) Q1 (invisible family) / Q2 (non-admissible) | (~2e−8, ~2e−8) / (−0.1308997, 0.2617994) | (0, 0) / (−π/24, π/12) |

- **Reading:**
  - Fable's residue calculus, the closed form C(4,j)wκ·3m2/(40δ)·(1 + r1²/m1²), the return-map normalisation and
    Lemma P all agree with an independent construction. That construction is my own U through ρ⁴ (from my static
    series plus the P1-confirmed twist term), integrated numerically around the puncture. It uses no residues and
    not Fable's h_4.
  - The invisible family really is invisible at L = 0 third order. The non-admissible perturbation really is
    obstructed.
- **Not tested by P3/P4:** the reduction from the true geodesic flow. That is P2 (running), with the exact metrics.

## Addendum A: P2, P5, P6 with true geodesics (R-full: exact metrics, complexified), 2026-11-20
Code: code/v25_full.py, v25_p6.py, v25_p6_A3.py. Results: results/v25_full.json and .log, v25_p6.json and .log,
v25_p6_A3.json.

**Validation first:**
- The static twin and the two-rod Weyl sums: ρ² and ρ⁴ coefficients of F1 and F2 equal my own static series to
  ≤ 1e−16 relative, at z = 3 and 5 (mpmath Taylor, 50 digits).
- The Weyl equations for γ hold to ≤ 5e−52.
- **First attempt (my own issue):** a sympy symbolic series of the 16-factor product did not finish in 12 min. I
  stopped my own job (PID 14995) and switched to the mpmath Taylor method for the same registered test.

### P2: the Kerr control and the static twin. CONFIRMED
Prolate units, M = 5/4, a = 3/4; loop twice around z1 = −M + ia; radii 0.35 and 0.5; VE_1 self-check ≤ 3.8e−10;
floors 1.5e−8 to 3.5e−8.

| metric (exact) | E | A from start (1, 0) | A from start (0, 1) | prediction |
|---|---|---|---|---|
| Kerr | 0.8 | (2e−8, 3e−8) | (1e−8, 1e−8) | (0, 0) |
| Kerr | 0.7 | (3e−8, 3e−8) | (1e−8, 2e−8) | (0, 0) |
| static twin | 0.8 | (−1.5707963, 3.1415926) | (3.1415927, −1.5707964) | (−π/2, π) and (π, −π/2) |
| static twin | 0.7 | (−1.5707963, 3.1415926) | (3.1415926, −1.5707963) | the same (E-independent) |
| twin through R-trunc (cross-check) | 0.8 | (−1.5707963, 3.1415926) | (3.1415927, −1.5707963) | equals R-full |

**Reading:**
- On the true L = 0 geodesic flow of the exact metrics, the cubic return map around the complex ring puncture
  vanishes for Kerr. It is exactly (−3πM/(10a), 3πM/(5a)) for the static twin, at two energies.
- This tests the reduction to system R, the near-axis series and the residue calculus all at once, with no
  truncation.

### P5: the real two-rod static metric. CONFIRMED
- Exact Weyl sum; loop twice around z1 = 1; E = 3/5.
- A = (−0.6283185i, 1.2566371i), vs the prediction (−0.6283185i, 1.2566371i); err 1.5e−8, floor 1.3e−8.
- So real two-pole data are obstructed, here on the exact metric.

### P6: the negative claims. CONFIRMED as far as tested
(ρ, p) coordinates; the linear map is from ε = 1e−7 runs.
- **(a) ZV δ = 2 (exact metric, E = 4/5):**
  - **Around infinity** (|z| = 15, 25): linear deviation from I 6.3e−13; cubic ≤ 1.5e−7 (floor 2.5e−7). **Identity,
    as predicted.**
  - **Around the zero of f0** (z = 1): VOID under A1 and under A2 (my ε choices; see the PREREGISTRATION amendments).
    Under A3: linear deviation 1.8e−10; cubic ≤ 9.2e−6 with floor 7.4e−5. **Identity, as predicted,** but the floor is
    weak, just under the VOID line: the cubic is zero only at the ~1e−5 level.
  - **Around the double pole (secondary):** linear multipliers 85.019695 and 0.011762, vs e^{±√2π} = 85.0196952 and
    0.0117620. They agree to all printed digits, so the first-order torus at the double pole is as Fable describes.
  - So on the ZV δ=2 axis the only non-identity loop is the double pole. Its group is cyclic, hence commutative: no
    axis obstruction at third order, as Fable claims (family C "not excluded").
- **(b) f0 = 1 − 2/z with c0 = 0.3/(z − 3) − 0.3/(z + 3) (R-trunc, E = 4/5):**
  - The linear return maps around z = 0 (2 turns), z = +3 and z = −3 are the identity (deviation ≤ 2.9e−10, at the
    floor). So there is no first-order torus, as predicted, and no third-order obstruction is possible.
  - The cubic parts at the twist poles are nonzero and depend on the base point. That is expected in (ρ, p)
    coordinates, and it is not verdict-bearing, as registered.

## Status of Fable result #3 ("only Kerr") after V25
- **Checks:**
  - P1: CONFIRMED.
  - P2: CONFIRMED (true geodesics, exact Kerr and exact static twin).
  - P3: CONFIRMED (13/13).
  - P4: CONFIRMED (identity exact; null space to pole order 12; invisible family zero).
  - P5: CONFIRMED (exact two-rod).
  - P6: CONFIRMED as tested (ZV and Schwarzschild-f0 loops; one weak floor).
- **Logic (REVIEW_LOGIC.md):** Theorem 1 is sound given its ingredients.
- **Supported claim:** among two-centre rational axis data, only Kerr–NUT, so only Kerr under asymptotic flatness, is
  meromorphically integrable near the complexified axis orbits. Conditional on:
  - G2 (Lemma X, critical case) and G3 (a minor point);
  - the literature theorem (MRRS).
- The Corollary additionally needs G1, the inherited first-order classification.
- **Not supported, and not claimed by Fable:** "only Kerr" in full. Single-centre data (G5) and the invisible
  non-rational family (G6) are open.
- **Process:** two VOIDs on my own check code (the self-check factor; Richardson and ε choices) and three of my own
  bugs (sympy power simplification; SVD conjugation; sympy series speed). All were caught before verdicts and are
  recorded in PREREGISTRATION amendments A1–A3.

## Gap G1 (the inherited first-order classification): independently checked by ansatz (RESULTS §158, 5f14db2; prereg 5df9e05)
- **(a) Re-derivation.** The local exponents, the absence of log/apparent singularities (1 − ¾m² is never a rational
  square), infinity ordinary for E² ≠ μ², and the Kovacic case-by-case bound s + 2h ≤ 4 are all CONFIRMED.
- **New edge case.** Three merging zeros lower s + 2h by 1.
  - Explicit example: f0 = ½ + ½((z − 1)/(z + 1))³ at E² = μ²/2 is solvable (torus) despite degree 3.
  - So the statement holds at GENERIC E, which is all the theorem uses ("E in an interval"). Any "every E" wording
    would be false.
- **(b) Numerical monodromy.** 40–50 digits; 16 runs; all agree with the predictions.
  - Solvable: Kerr, ZV δ = 2, degree 1 and a generic degree 2.
  - Non-solvable: three degree-3 f0, plus a two-zero merge.
  - Disclosure: the registered verdict was UNDETERMINED (over-high threshold), and a labelled post-hoc truncation
    check settled it.
- **(c) Confidence.**
  - The necessary direction, d ≥ 3 ⇒ SL(2,C) at generic E, which is the one the Corollary uses: ansatz ~95%.
  - The sufficiency direction: ansatz rates it 80–85%. The Bridge notes that for two simple poles it is proven by the
    explicit Liouvillian solutions √Δ e^{±κu}; these were verified to solve VE_1 to ≤ 1e−9 in V25 for Kerr-type,
    Kerr–NUT-type and real-pole data. For the double pole, the V25 P6 multipliers e^{±√2π} match the explicit local
    solutions.
- **Effect on the Corollary:** G1 is now independently supported. The wording is: "for E in an interval (generic E)".

## Addendum B: Lemma X, critical case (gap G2). B1 PASS. B2 FAIL as registered, on an exactness artifact; PASS under amendment B2′. Controls PASS. (prereg b2c57b0; Bridge, 2026-11-20 evening)
Code: code/v25_B.py. Results: results/v25_B.json.
Environment: Python 3.14.5, sympy 1.14.0, mpmath 1.3.0 (60 digits), macOS 27.0.1 arm64.

**B1 (exact) PASS**
- **(a)** For two simple poles, κ²(E*) − μ² f0″(p)D(p)²/4 ≡ 0 modulo num f0′(p) (remainder 0).
- **(b)** The same for a double pole (remainder 0).
- **(c)** The resultants are 4m1²m2²(m1 + m2)(z1 − z2)⁶ and −2(b + 2z1)(z1² + bz1 + c). They vanish only on
  degree-drop loci:
  - m1 + m2 = 0, where num f0′ loses its p² term and a critical point moves to ∞;
  - Δ(z1) = 0 (the pole cancels) or b = −2z1.
  - At every finite critical point of a genuine degree-2 f0, f0″(p) ≠ 0. This also follows from the degree count.
- **Hence c′² = −w²/2 ∈ {−2, −8}.** This is never the square of a real integer, so every Taylor coefficient of
  e^{c′ arsinh ξ} is nonzero.

**B2 as registered: FAIL**
- In all 24 (case, w, m) rows, dev ≤ 1e−3 at ε = 1e−10.
- The 4 rows with m = 1 fail the "non-increasing" clause:
  - their dev is 1e−55 to 7e−52, which is rounding;
  - h₀σ = σ/(D_p√ε) = 1/(D_p√(−a)) = M₀ exactly, for every ε;
  - so the monotonicity clause was applied below the arithmetic floor. It should have been floor-first (the
    control-clause rule).
- **The other 20 rows** decrease by a factor √10 per decade of ε, i.e. dev ∝ σ, as predicted. At ε = 1e−10, dev is
  between 3.9e−6 and 7.4e−5.

**Amendment B2′ (POST-RESULT).** A row whose dev is below 1e−40 at every ε counts as exact. The monotonicity clause
applies only above that floor. No rerun is needed: the data are unchanged. Under B2′, B2 PASSES (24/24).

**Controls PASS**
- **Generic p** (non-critical, both cases): slopes −0.5, −1.5, ..., −5.5 for m = 1..6, all within 1e−4 of −(m − ½).
- **Integer exception** (κ forced so that c′ = 1): the scaled m = 3 and m = 5 coefficients are 1.6e−5 and 1.4e−5 for
  Kerr, and 3.4e−5 and 2.8e−5 for the rods. That is O(σ), so the leading term vanishes, as predicted. m = 2 stays at
  1.0000. So the check does see the integer exception.

**Conclusion.**
- The critical-point case of Lemma X holds. Its residue grows like σ^{−m} ∝ |E² − E*²|^{−m/2}, with leading
  coefficient A_m M_{m−1} ≠ 0.
- So it cannot vanish for E in an interval.
- The argument is written in REVIEW_LOGIC, addendum G2.

## Addendum C (2026-11-21 ~02:45): Gemini Neon's Lemma X-∞ and G3. **C1 PASS, C2 PASS, C3 PASS**
Code: code/v25_C.py, written independently; no Neon code used. Output: results/v25_C.txt. Run under nice 10, in seconds.

- **C1 (exact sympy, symbolic parameters).** All four differences are identically 0: I, J, I³ − 27J², and
  j = 256(S + 3)³/(S + 4). So Neon's quartic-invariant formulas for two-pole data are right.
- **C2 (M ≠ 0).** The ratio to the claimed leading term, ∓binom(−1/2, m−1)(2Mμ²)^{m−1}ε^{−m+1/2}, tends to 1.
  - Kerr-type data: |ratio − 1| = 1.3e−8 to 1.6e−8 at ε = 1e−8, falling as O(ε).
  - Asymmetric data: |ratio − 1| = 9.8e−5 at ε = 1e−8, falling as O(ε^{1/2}).
  - This holds for m = 1..4; m = 1 is exact.
  - The m = 0 control returns 0. This control is **structural**: the series has no t⁻¹ term. It confirms the code
    path, not the mathematics.
- **C3 (M = 0 dipole).** The ratio to ε^{−m/2}·A·c^{(m−1)/2}∏(α + m − 2j)/(m − 1)! tends to 1: |ratio − 1| ≤ 2.5e−4
  at ε = 1e−8, falling as O(ε^{1/2}).
  - The claim does not depend on the branch of √c (the factors pair up).
  - Must-fail control, w = i√2 (α = ±1), m = 3: the leading term vanishes. The scaled residue is 1.5e−4 against
    1.13 for w = 2 (ratio 1.3e−4 ≤ 1e−2). The control behaves as required.
- **I2** (reviewed by reading only, Bridge, not machine-checked). The argument is the standard Morales–Ramis–Simó one:
  - restriction to the invariant manifold {p_t = −E, L = 0, H = −μ²/2};
  - an algebraic 3-jet inversion inside L_full;
  - finite base extensions leave G° unchanged;
  - π(G_full°) = G_R°.

  I found no gap. The one step that needs care is "K_R = K_full via p_z = g_zz ż0". Even if that fails, Neon's
  fallback (a quadratic extension at worst) covers it.

**Effect on the Only-Kerr gaps.** The computational cores of Lemma X-∞ and Lemma G3 are confirmed. The surrounding
logic is
- for X-∞: the identity theorem on an algebraic function, with an exact leading asymptotic;
- for G3: non-constancy of j, then countability, then infinite-order diagonal monodromy.

Both are standard, and they read correctly to the Bridge. Status moves from "open" to "proved (Neon), cores
machine-checked (Bridge V25-C), logic read once". A second reader (a sister) is still wanted before any outreach.

- **Timestamp correction (appended 2026-11-21 04:10 IST, system clock).** The '~hh:mm' times written by the Bridge in tonight's addenda (V25 C; V26 D–G) were estimated and run about 1.5–2 h FAST. The commit timestamps in git are authoritative.
