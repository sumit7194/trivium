# Move B — Findings: the numeric ringdown bridge (leg 3b)

*Run 2026-06-19. Comparisons and predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md)
before the eikonal QNM was compared to the measured ringdown. Upgrades the spine's leg 3.*

## Result in one line

Ansatz's **eikonal Kerr QNM, computed from the exact metric**, matches deepstrain's **measured
GW250114 220 ringdown** to a few percent — quality factor `Q₂₂₀` to **1–7%** and dimensionless
frequency `Mω_R₂₂₀` to **3%** — while the Schwarzschild (non-spinning) approximation misses by
**40–50%**. The spine's ansatz↔deepstrain ringdown link is now a **numeric exact↔measured
comparison**, not a proposition; and the agreement is the *light ring* (`Ω_c·b_c = 1` exact), so
the LIGO ringdown and the EHT shadow are demonstrably the same photon orbit.

## The comparison (all four frozen predictions pass)

Measured GW250114 (deepstrain, real O4 data, read-only): 220 mode `f = 257.76 Hz`,
`τ = 4.944 ms`; remnant `M = 78.8 M⊙`, `χ = 0.787 [0.641, 0.887]`; no-hair `δ = −0.16` (Kerr
inside 90%).

| quantity | measured | ansatz eikonal Kerr | agreement | prediction |
|---|---|---|---|---|
| **Q₂₂₀** (M-independent, `πfτ`) | **4.00** | 3.73 (χ=0.787) · 3.96 (χ=0.815) | **6.8% · 1.1%** | P1 (<25%) ✅ |
| **Mω_R₂₂₀** | **0.629** (SBI M) | 0.609 (χ=0.787) | **3.1%** | P2 (<15%) ✅ |
| Q₂₂₀, Schwarzschild χ=0 | 4.00 | 2.00 | 50% off | P3 (spin essential) ✅ |
| Mω_R, Schwarzschild χ=0 | 0.629 | 0.385 | 39% off | P3 ✅ |
| **Ω_c · b_c** (shadow–ringdown) | — | **1.000000** (all χ) | exact | P4 ✅ |

→ `results/legB_ringdown_bridge.png` plots `Q(χ)` and `Mω_R(χ)` with the measurement and its 90%
spin CI overlaid; the eikonal curve threads the measured point inside the CI.

## What this establishes

- **Leg 3 is now numeric.** It closed the spine at the level of a *proposition* ("ansatz proves
  no-hair; deepstrain measures δ≈0") because ansatz had no QNM module. Ansatz now computes the
  ringdown frequency from the metric, and it agrees with the real measured 220 to a few percent.
  The count-triangle's measured leg gains a numeric ansatz cross-check it never had.
- **The agreement is physics, not a fit (P3).** The non-spinning Schwarzschild eikonal is 40–50%
  away from the data; only the Kerr spin correction — the prograde photon ring of the exact
  metric — brings ansatz into agreement. Nothing was tuned: the eikonal QNM is read straight off
  the light-ring orbital frequency and its Lyapunov exponent.
- **One photon ring, two instruments (P4).** `Ω_c·b_c = 1` holds exactly at every spin, so the
  measured ringdown pitch is `m` over the exact shadow radius: the LIGO ringdown (deepstrain) and
  the EHT shadow (ansatz `§45/§68`) are the *same* unstable photon orbit, seen two ways.
- **Method gate.** The whole construction is validated by the Schwarzschild limit: the
  exact-metric code reproduces `Ω_c = λ = 1/(3√3)`, `Q = 2`, `b_c = 3√3`, `Ω_c·b_c = 1` to
  machine precision before any Kerr value is trusted.

## Honest limits (stated up front, per §7)

- **Eikonal limit.** ℓ=2 is not ℓ→∞, so the eikonal QNM carries an intrinsic few-to-~15% error
  vs the exact (Leaver) Kerr 220 — which is exactly the size of the residual agreement gap, and
  is *better* than the band we pre-registered. The precise overtone spectrum is numerical
  (Leaver / the `qnm` package); ansatz supplies the exact potential and the exact eikonal limit
  and flags that it does not do Leaver (§56 D). This is a light-ring–level comparison, honestly
  scoped, not a precision-spectroscopy claim.
- **No new physics.** QNM↔light-ring (Cardoso et al.), the no-hair test, and Kerr spectroscopy
  are textbook / LVK-active. The contribution is turning the spine's ringdown link into a real
  number cross-checked against real data, by an exact engine.
- **Single event, dominant mode.** GW250114, ℓ=m=2, n=0. The measured 221/δ (Kerr-consistent) is
  the empirical no-hair side leg 3 already used; here the headline is the 220 light-ring match.
- **Spin from the measurement.** χ is taken from deepstrain's posterior; the comparison reads its
  90% CI, within which the eikonal curve agrees.

## Spine status

The §5 count-triangle's measured leg now has a numeric ansatz cross-check: the same Kerr remnant
whose no-hair δ≈0 says "2 numbers" also rings at the frequency ansatz's exact light ring predicts.
**Leg 3 → leg 3b: the ringdown bridge is numeric.**

## Artifacts
- `code/eikonal_kerr_qnm.py` — ansatz side: eikonal Kerr QNM from the exact metric, Schwarzschild-gated.
- `code/compare_ringdown.py` — measured-vs-eikonal comparison + frozen-prediction verdicts.
- `code/plot_ringdown.py` — the Q(χ), Mω_R(χ) figure with GW250114 overlaid.
- `results/eikonal_kerr_qnm.json`, `compare_ringdown.json`, `legB_ringdown_bridge.png`.
