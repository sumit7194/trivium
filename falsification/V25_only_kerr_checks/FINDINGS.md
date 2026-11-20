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
