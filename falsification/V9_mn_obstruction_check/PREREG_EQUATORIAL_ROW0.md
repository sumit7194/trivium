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

## Addendum, 2026-10-04 ~04:30 IST: row 3, under the same gates and verdict rule (before running)
Row 3 is P2 = (13, 5, −1/3), (E, L, μ²) = (1, 0, 4). The recipe came from quantum's message:
- base z₀ = 2.667119562555136 + 2.7667479123938024i;
- loops: a at c = 0.307967384242499 with ρ = 0.20760978472725028; b at c = −0.4751366065599529 + 0.22858319755496656i
  with ρ = 0.07700413164438846; c′ at c = −0.7703523566330759 + 0.37656494220755987i with ρ = 0.017435697281317466;
- composition: g = M_a·M_b, h = M_a·M_c′.

Targets:
- tr²/det(g) = 1345.2758406025942679 − 1011.6353858956783367i;
- tr²/det(h) = −2371.4390654371280839 − 7787.8783024198235091i;
- tr[g,h] = −389140.59069213841206 + 1464024.0755057192621i.

The code is the V9-eq′ code (positive R₀, no-√ assertion), unchanged, with only the row table added.

## Addendum, 2026-10-04 ~07:00 IST: row 1, the A6 certificate (before running)
Row 1 is P1, (E, L, μ²) = (1, 0, 9). quantum's v2 certificate was found under the post-failure A6 amendment. Its v1
replay at N=100 could not certify (commutator radius 1.3e11). The v1 replay at N=140 (quantum's A7) is pending. This
bridge run is a numerical reproduction only and does not stand in for A7.

The recipe came from quantum's message:
- base z₀ = 2.483596994071131 + 2.5763699891994527i;
- loops: a at c = 1.2614475105508947 + 0.32152725175852437i; b at c = 1.2874032225413898 + 0.23979070891675344i
  (both with ρ = 0.025727621885033154); c′ at c = −0.16003305636505147 with ρ = 0.1262521808340563;
- composition: g = M_a·M_b, h = M_a·M_c′.

Targets:
- tr²/det(g) = −2547891.7087019648 + 4172532.2257715459i;
- tr²/det(h) = −6817.1486392324403 + 7154.6410627524415i;
- tr[g,h] = 51202181.921165786 + 30889220.299715389i.

The gates and verdict rule are unchanged.

Expected stress: loops a and b sit about 0.3 from the essential point t = 1. If the Abel or convergence gate fails there,
the verdict is INCONCLUSIVE, and no tolerance tuning follows unless it is pre-registered.
