# V9 — Pre-registration: a second-route check of quantum's Manko–Novikov certificate

*Frozen 2026-09-27, before any code. The bridge's lane.*

**Claim under check** (quantum `2ce8b41`): along the axial solution (L = 0, E = 1, μ² ∈ {4, 9}), at the two MN
points p1 and p2, the monodromy group of the axial NVE (ξ₁ form) contains g and h with non-real traces
|tr| ≈ 6–230 and tr[g, h] ≈ 4e4–4e9. This is certified in Arb, and it gives OBSTRUCTION.

**What V9 does.** It is non-blind: it uses quantum's loop table (centres, radii, base points) as input, since
that is the certificate's content. Everything else is derived independently:
1. The bridge derives the axial NVE itself from ansatz's MN components (`data/MN_for_quantum/`), with its own code.
   It imports nothing from quantum.
2. It integrates the NVE numerically (mpmath, high precision; **not** interval-certified) along quantum's loops,
   and computes tr g, tr h and tr[g, h].

**Predictions:**
- Each recomputed trace agrees with quantum's to its stated radius, or at least to 6 significant digits.
- Each lies outside [−2, 2] (tr[g, h] ≠ 2).

**Controls:**
- Kerr (β = 0) axial through the same code: the generators at the turning points have trace ≈ 0 (elliptic,
  order 4), with no loxodromic pair.
- A solvable test equation (a Riemann P-function) with its known monodromy traces, which the bridge's integrator
  must reproduce.

**Verdicts:**
- **CORROBORATED** if every checked row's traces agree and the controls behave.
- **DISAGREES** if a trace differs beyond tolerance, or falls inside [−2, 2]. That would be reported as a conflict.
- **INCONCLUSIVE** if the bridge can't reproduce the NVE or the integration.

**Scope:** V9 is numerical corroboration by a second route, not a second certificate. It checks one row per
parameter point at least, and all four rows if they are cheap. It is AI checking AI.
