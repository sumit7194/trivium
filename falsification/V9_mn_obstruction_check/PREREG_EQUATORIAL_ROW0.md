# V9-eq — Pre-registration: the bridge reproduces quantum's MN equatorial row-0 monodromy

*2026-10-04, ~03:30 IST. Written and committed BEFORE any bridge integration of the equatorial loops. Not blind:
quantum's three target values are known (below). The bridge reads none of quantum's files. The loop
specification came as text in a cross-session message.*

## What quantum claims (row 0: P1 = (M, a, β) = (5, 3, 1/5); (E, L, μ²) = (1, 0, 4))
- Chart: x = (t + 1/t)/2, with R = (t² − 1)/(2t) as one rational branch.
- Equation: the non-reduced ξ₁ equation in t.
- Base point: z₀ = 2.0246153192247602 + 2.100243381102574i.
- Loops: 16-gon, counter-clockwise, each with a straight tail to z₀:
  - a: c = 0.18574683248165982, ρ = 0.10036930953180813;
  - b: c = −0.5601946717730222, ρ = 0.01330513017617667;
  - c′: c = −0.14881753262436728, ρ = 0.10036930953180813.
- Composition: g = M_a·M_b and h = M_c′·M_b.
- Target values:
  - tr²/det(g) = −313428.5136459282 − 106383.3249050493i;
  - tr²/det(h) = 26436.87518302681;
  - tr[g,h] = −290240.6602844212 − 86714.14718309702i.

## The bridge's independent route (`code/v9_equatorial_monodromy.py`)
- **Its own equations.** A, B and X are built from the bridge's own MN transcription (`v9_nve`), with
  R(x,y) = √(R₀² + y²). R₀ is a free symbol, so the y-derivatives at y = 0 are exact. Then x(t) and R₀(t) are
  substituted. So the coefficients are rational in t and exp(rational in t), with no square-root cuts.
- **Converting to t.** p_t = −(A_t/A − X_t/(2X)) − x″/x′ and q_t = x′²·AB/X, with all derivatives in t. This is
  derived from the bridge's own x-form, not taken from quantum's formula.
- **Integrator.** scipy DOP853 in complex128 at rtol 1e−11 and 1e−13, as in V9's axial fast path.
- **Order check.** It also reports the reversed products M_b·M_a and M_b·M_c′.

## Gates, in order
1. **Provenance self-check:** at t = 2 (x = 5/4), back-converting p_t, q_t to p_x, q_x must reproduce the bridge's
   own committed 50-digit values (`results/v9_equatorial_provenance.json`) to a relative error below 1e−12. If it
   fails, STOP; there is no monodromy verdict.
2. **Abel check:** for each loop, det M must equal exp(−∮p_t dt), computed independently by quadrature, to
   a relative error below 1e−8.
3. **Convergence:** the two tolerances must agree on all three invariants to at least 7 significant digits.

## Verdict rule
- **REPRODUCED:** all gates pass, and all three invariants agree with quantum's to at least 7 significant digits.
- **DISAGREES:** all gates pass, but some invariant differs beyond 1e−5 relative. In that case nothing is claimed,
  and the bridge and quantum find the cause together.
- **INCONCLUSIVE:** anything else.

The verdict is about numerical reproduction only (not a certificate). The certificate is quantum's v2, replayed by v1.
