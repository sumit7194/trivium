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
