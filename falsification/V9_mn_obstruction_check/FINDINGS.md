# V9 — Findings: quantum's Manko–Novikov certificate, checked by a second route

*2026-09-27. Pre-registration `f60ef96`. Non-blind: quantum's loop table (base points, centres, radii) was the
input, since that is the certificate's content. The NVE and the integrator are the bridge's own; nothing is
imported from quantum.*

## Verdict: **CORROBORATED**

| row | quantity | quantum (Arb-certified) | bridge (DOP853, rtol 1e-13; unchanged at 1e-11) |
|---|---|---|---|
| p1 (1,4) | tr g | −92.414085783 − 41.768358339i | −92.4140858 − 41.7683583i |
| | tr h | −6.18751016 − 0.62303983i | −6.18751016 − 0.623039832i |
| | tr[g,h] | 1.6720778e7 + 6.5281132e7i | 1.672078e7 + 6.528113e7i |
| p1 (1,9) | tr g | −31.827481193 − 4.849823092i | −31.8274812 − 4.84982309i |
| | tr h | −229.72253543 + 8.64635676i | −229.722535 + 8.64635676i |
| | tr[g,h] | −4.17436284e9 − 9.6709241e8i | −4.174363e9 − 9.670923e8i |
| p2 (1,4) | tr g | −4.660883019 + 94.697449816i | −4.66088302 + 94.6974498i |
| | tr h | −16.11372787 + 27.71917392i | −16.1137279 + 27.7191739i |
| | tr[g,h] | 189666.293 + 125077.964i | 189666.3 + 125078i |
| p2 (1,9) | tr g | 37.076560475 + 57.645082827i | 37.0765605 + 57.6450828i |
| | tr h | 8.1202420 + 26.4392511i | 8.120242 + 26.4392511i |
| | tr[g,h] | 39987.5528 − 91615.2974i | 39987.55 − 91615.3i |

- **Every trace agrees to 7–9 significant digits.**
- **Every one lies far outside [−2, 2]**, and tr[g, h] is far from 2.
- tr[g, h] doesn't depend on the product-order convention: it is identical for AB and BA.
- det error is below 3e-8 throughout.

## Independence of the route

- **The bridge transcribed the MN functions** from ansatz's manifest formulas, with its own branch choice
  R = x√(1 + (y² − 1)/x²). It checked them against ansatz's srepr components at 3 random points per parameter
  point: they agree to double precision (at most 1.2e-15 relative).
- **ω = 0 on the axis**, re-checked independently at real and complex x.
- **The axial NVE, derived by the bridge:** A = g^θθ|₀, B = −∂_y H|_{y=1} (with the ω²/(1−y²) limit taken
  analytically), ẋ² = F₁(E²/f − μ²), then the ξ₁ normal form z″ = r z.
- **The integrator** is scipy's DOP853 in complex double precision, not quantum's Arb code.

## Controls (`results/v9_controls.txt`)

- **Integrator test.** z″ = βz/x² around 0 gives traces equal to −2cos(π√(1 + 4β)) to 1e-14, for
  β = 0.1, −3/16 and 1.7.
- **Kerr (β = 0), axial, all 4 levels.** The bridge located the singular points itself: 4 per level. Every
  generator trace is 0 to 1e-12 (elliptic, order 4), so none is loxodromic.

## Scope

- **Numerical corroboration by a second route, not a second certificate.** Quantum's Arb enclosures remain the
  proof, and V9 shows an independent derivation and integrator reproduce them.
- It uses quantum's loop geometry as input.
- The verdict's other caveats carry over unchanged: post-failure (A1–A5); the L = 0 axial sector only; the tested
  points only; the positive control was equatorial; the metric is a transcription of the published MN form.
- AI checking AI.

## Instrument log

- The first attempt used mpmath RK4 at 30 digits. It was far too slow and was stopped (it was the bridge's own
  process). Replaced by DOP853 in double precision, which is ample for 7–9-digit agreement.
- The first controls run hung in a symbolic `cancel` of the full Kerr r and was stopped (again the bridge's own
  process). Replaced by locating the singular points piecewise, from A, ẋ² and B.

## V9-eq: equatorial row 0, reproduced by the bridge (2026-10-04, pre-registration `51fff74`)

**Verdict: REPRODUCED, after a post-failure amendment (V9-eq′) to fix a bug in the bridge's own code.**

| Run | Gates (provenance / Abel / convergence) | Agreement with quantum | Verdict |
|---|---|---|---|
| V9-eq as registered | PASS / PASS / PASS | tr²/det(g) off by a relative 0.86, tr²/det(h) off by 3.8, tr[g,h] off by 0.98 | **DISAGREES** |
| V9-eq′ (branch fix) | PASS (7e−42) / PASS (≤1.2e−10) / PASS (1.8e−10) | 7.0e−11, 5.9e−11 and 4.3e−11 | **REPRODUCED** |

**What V9-eq′ computes:**
- tr²/det(g) = −313428.51362 − 106383.32490i;
- tr²/det(h) = 26436.875182 (imaginary part 1e−6, numerically zero);
- tr[g,h] = −290240.66028 − 86714.14717i, the same in both composition orders.

So tr[g,h] ≠ 2, and tr²/det(g) is not real. This is a numerical reproduction, not a certificate (that is quantum's v2,
replayed by v1).

**Cause of the first disagreement.**
- The bridge wrote R(x, y) = √(R₀² + y²) with R₀ a plain symbol. sympy does not reduce √(R₀²) to R₀, so after the
  substitution R₀ = (t² − 1)/(2t), the code evaluated the *principal* root.
- That flips the sign of R on the t < 1 sheet, where loops a and c′ sit. So the bridge was integrating a different
  equation there. quantum's specification had warned about exactly this cut.
- Gate 1 couldn't catch it, because it checks only at t = 2 (R > 0). **Lesson: a provenance point must sample every
  sheet the loops visit, not just the convenient one.**

**The fix.** R₀ is declared positive, so √(R₀²) = R₀ before the substitution. An assertion now fails if any
square root of t survives in the coefficients. Results: `results/v9_equatorial_row0.json` (first run, kept) and
`results/v9_equatorial_row0_amended.json`.

**Scope.** Row 0 only (P1, (E, L, μ²) = (1, 0, 4)). Non-blind: the target values were known. It used the bridge's own
equations and integrator, with the loop recipe transcribed from quantum's message. No quantum file was read.

### V9-eq′, row 3 (P2 = (13, 5, −1/3), (1, 0, 4)): REPRODUCED (first run, no amendment)
- **Gates:** provenance 8e−42, Abel ≤ 5.8e−12, convergence 3.9e−11. All PASS.
- **Agreement with quantum** (relative): tr²/det(g) 2.2e−12, tr²/det(h) 4.6e−13, tr[g,h] 2.2e−12. The commutator is the
  same in both composition orders.
- **Values:** tr²/det(g) = 1345.2758406 − 1011.6353859i, tr²/det(h) = −2371.4390654 − 7787.8783024i, and
  tr[g,h] = −389140.59069 + 1464024.0755i ≠ 2. The second parameter point is now reproduced as well.
- Results: `results/v9_equatorial_row3.json`.

### V9-eq′, row 1 (P1, (1, 0, 9); A6 certificate): REPRODUCED, with a thin convergence margin
**Gates:**
- provenance 5e−42;
- Abel ≤ 1.1e−10;
- convergence **9.9e−8, against a gate of 1e−7**. This passes, but only just.

**Agreement with quantum** (relative):
- tr²/det(g) 5.1e−8;
- tr²/det(h) 1.7e−12;
- tr[g,h] 5.1e−8.

**What the numbers say.** The two loops near t ≈ 1.27 (about 0.3 from the essential point t = 1) cost the bridge's
complex128 integrator about 5 digits. That is consistent with quantum's v1 needing N = 140 there. Even so, about 7
significant digits agree, on tr[g,h] ≈ 5.12e7 + 3.09e7i, which is nowhere near 2.

**What it does NOT do.** It does not substitute for quantum's pending A7 v1 replay at N = 140. Until that lands, the
row's certificate grade stays as quantum reports it.

Results: `results/v9_equatorial_row1_a6.json`.

### V9-eq′, row 2 (P1, (1, 1, 4), so L = 1; the A6 certificate, v1-replayed): REPRODUCED
- **Gates:** provenance 5e−42, Abel ≤ 3.2e−10, convergence 1.1e−8. All PASS.
- **Agreement with quantum** (relative): tr²/det(g) 2.5e−10, tr²/det(h) 1.5e−11, tr[g,h] 8.9e−9.
- **Values:** tr[g,h] = 544.03465 − 550.27482i ≠ 2.
- This is the first L ≠ 0 equatorial row. Results: `results/v9_equatorial_row2_a6.json`.
