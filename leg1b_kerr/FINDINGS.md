# Leg 1b — Findings: the Kerr extension (rotating black holes)

*Run 2026-06-17. Predictions and agreement criterion were frozen in
[PREREGISTRATION.md](PREREGISTRATION.md) before any observable was computed.*

## Result in one line

Tabula's neural bottleneck count **matches ansatz's exact moduli count on all six
cells** — Kerr = 2, Kerr–Newman = 3 (the doc's literal headline), and the controlled
Δ-symmetric test confirms frame-dragging as the degeneracy-lifting observable.

## The outcome table (predicted → measured)

| Cell | ansatz resolvable count | tabula count (whitened) | predicted | verdict |
|---|---|---|---|---|
| Kerr, dimensionful | 2 | **2** | 2 | ✅ agree |
| KN (full), dimensionful | 3 | **3** | 3 | ✅ agree |
| **KN (Δ-symmetric), dimensionful** | **2** † | **2** | 2 | ✅ **degeneracy exposed** |
| Kerr, shape | 1 | **1** | 1 | ✅ agree |
| KN (full), shape | 2 | **2** | 2 | ✅ agree |
| **KN (Δ-symmetric), shape** | **1** † | **1** | 1 | ✅ **degeneracy exposed** |

Every cell landed on the frozen prediction. No off-by-one, no anomalies.

† The "ansatz count" column is the number of moduli that are *resolvable from the
observable set shown to tabula*. For Kerr and KN-full this equals the algebraic moduli
count (2 and 3). The **KN-Δ-symmetric** rows are not a different black hole — they are
the *same* 3-moduli Kerr–Newman family (algebraic moduli still 3 / shape 2), observed
through a restricted set of Δ-symmetric quantities that depend on charge and spin only
through `a²+Q²`. So "2" (and "1" for shape) there is the *resolvable* count under that
restriction, not a claim that KN has 2 algebraic moduli. This restricted-vs-full
contrast is exactly the controlled test: full observables resolve 3, Δ-symmetric
observables resolve 2.

## What this confirms — and how it contrasts with leg 1

**The headline:** rotating black holes are 2-number (Kerr) or 3-number (Kerr–Newman)
objects, as counted independently by ansatz's exact moduli and tabula's blind neural
measurement of the observable manifold. This is the literal claim of THE_BRIDGE.md §3.

**The controlled degeneracy test:** this is the rotating analogue of leg 1's dyonic
Q²+P² degeneracy, but with the *opposite* outcome:

- **Leg 1 (static dyonic):** ansatz moduli = 3 (M, Q, P), but every observable depends
  on charge only through Q² + P². No observable lifts the degeneracy → tabula counts 2.
  The third number is *algebraically present but observationally invisible*.

- **Leg 1b (rotating KN):** ansatz moduli = 3 (M, a, Q), and a² + Q² are degenerate
  *inside Δ* (horizons, Δ-probes see only a² + Q²). But:
  - `g_tt = −(r² − 2Mr + Q²)/r²` is **a-independent** → probes M and Q, not a;
  - frame-dragging `ω = −g_tφ/g_φφ ∝ a` → probes a directly.

  So the full observable set **breaks** the a²+Q² degeneracy. The third number *is*
  recoverable. The KN-full → KN-Δ-symmetric controlled test demonstrates this:
  - **KN-full (all observables):** count = 3 — frame-dragging lifts the degeneracy.
  - **KN-Δ-symmetric (horizons + Δ/r² only):** count = 2 — sees only a² + Q².

  This is exactly what the pre-registration predicted: the degeneracy lives in Δ
  (symmetric set → 2) and is broken by the symmetry-breaking observables (full set → 3).

**The through-line with leg 1:** the resolvable count is *measured, not assumed*. When
an observable degeneracy exists (dyonic Q²+P², or KN's Δ-symmetric subset), tabula
counts fewer than the algebraic moduli — correctly. When the degeneracy is broken (KN
full set via frame-dragging), tabula recovers the full count — also correctly.

## The R²(d) curves

See `results/leg1b_count_curves.png`. Key features:

- **Kerr dimensionful:** d₁=0.75, d₂=0.99 → sharp knee at 2, matching (M, a).
- **KN-full dimensionful:** d₁=0.59, d₂=0.89, d₃=0.99 → three genuine dimensions;
  the third dimension (charge Q, resolved by g_tt) carries less variance than M or a
  but is cleanly above the 2% marginal-gain threshold.
- **KN-Δ-symmetric dimensionful:** d₁=0.89, d₂=1.00 → saturates at 2; the a²+Q²
  degeneracy collapses the third dimension. Linear spectrum confirms: 84% in one PC,
  16% in a second, then < 0.1% — only two real directions.
- **Shape variants:** mass scale removed; Kerr reduces to 1 (a/M only), KN-full to 2
  (a/M, Q/M), KN-Δ-symmetric to 1 (sees only (a² + Q²)/M²). All match.

## Sanity validation (instrument check, not predictions)

Before generation, the exact metric-derived observables were validated against known
Bardeen values:
- Schwarzschild: r_ph = 3.000M ✅, r_isco = 6.000M ✅, ω = 0 ✅.
- Kerr a/M = 0.9: r_isco_pro = 2.321M (expected 2.32) ✅, r_isco_retro = 8.717M
  (expected 8.72) ✅, r_ph_pro = 1.558M (expected 1.56) ✅.
- KN a/M = 0.6, Q/M = 0.5: r+ = 1.624M (sub-extremal) ✅, frame-dragging present ✅.

## Honest limits

- **Equatorial plane only.** Off-equatorial geodesics (Carter constant, Lense-Thirring
  polar precession) would add observables; here we use the equatorial restriction where
  the stationary-axisymmetric conditions are simplest. The count result stands because
  equatorial observables already resolve all moduli for KN — more observables cannot
  reduce the count, only confirm it.
- **Sub-extremal (χ < 0.9).** Near-extremal Kerr (χ → 1) has photon orbit / ISCO
  coalescence that may stress the rootfinder; avoided by design.
- **Same knee rule as leg 1.** The whitened marginal R² gain > 2% criterion, with ≥3
  seeds, is carried from leg 1 without modification. Both legs use the identical AE
  architecture and training protocol.

## Artifacts

- `code/kerr_observables.py` — imports ansatz's `kerr_delta_metric` READ-ONLY; derives
  exact equatorial observables; samples Kerr / KN objects; writes obs `.npz`.
- `code/count_bottleneck_kerr.py` — tabula bottleneck AE; reads ONLY the `.npz`
  observations (§2 blindness enforced mechanically). Same instrument as leg 1.
- `code/plot_curves_kerr.py` — the figure.
- `results/obs_*.npz`, `results/count_bottleneck_kerr.json`,
  `results/leg1b_count_curves.png`.
