# Tier 3 — Findings: opportunistic exact-bound consistency checks

*Run 2026-06-19. The cheap §10.2 Tier-3 checks — consistency statements against ansatz's exact
bounds, not new results.*

## Result in one line

Both of ansatz's exact merger bounds are consistent with the measured/published data: the **area
theorem** holds for GW150914 with a 1.56× margin (and radiated energy well under the cap), and
GR's **two polarization modes** are consistent with the measured (pure-tensor) polarization content.

## The checks

**§75 — area theorem** (`A_f ≥ A_1 + A_2`, i.e. `M_irr,f² ≥ M_irr,1² + M_irr,2²`). For GW150914
(published LVK progenitors `m₁=35.6, m₂=30.6 M⊙`; remnant `M_f=63.1, χ_f=0.69` — deepstrain
stores ringdown remnants only, not progenitors, so the published progenitor masses are used):
- `M_irr,final = 58.58 M⊙` vs `√(m₁²+m₂²) = 46.94 M⊙` → the horizon area increased (margin 1.56×). ✅
- radiated fraction `4.7%` vs ansatz's §75 equal-mass cap `29.3%` → comfortably below. ✅

**§74 — polarization mode-count.** Ansatz proves GR has exactly **2** tensor (transverse-traceless)
modes while a general metric theory allows up to **6** (2 tensor + 2 vector + 2 scalar). LVK
polarization tests favour pure tensor (no scalar/vector detected); the measured polarization
content is consistent with GR's 2. ✅ (A consistency statement — deepstrain did not run a
dedicated polarization test on these events.)

## Honest scope

Both are textbook consistency checks of established bounds, included to close the roadmap's Tier-3
items. The area-theorem progenitor masses are published LVK values (not a deepstrain measurement);
the polarization item is a consistency statement, not a computed test. No new physics.

## Artifacts
- `code/tier3_checks.py` — the area-theorem and polarization computations.
- `results/tier3_checks.json`.
