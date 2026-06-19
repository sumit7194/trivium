# Move B — Pre-registration: the numeric ringdown bridge (leg 3b)

*Frozen 2026-06-19, before the eikonal Kerr QNM is compared to the measured ringdown.
Discipline: THE_BRIDGE.md §2, §4C, §10.2 Move B. Upgrades the spine's leg 3 from a
proposition-level proof↔test to a NUMERIC exact↔measured comparison.*

## Why this leg exists

Leg 3 closed the spine but the ansatz↔deepstrain link was **proposition-level only** — ansatz
had no QNM module, so "the proved no-hair statement vs the measured δ" could not be a numeric
comparison. Ansatz now has the QNM oracle (§56 `eikonal_qnm`, §72 ringdown/no-hair). This leg
makes the ringdown link numeric.

## 1. The two sides (both read-only)

**ansatz (exact, from the metric).** The eikonal/light-ring QNM (Cardoso correspondence,
§56): `ω = mΩ_c − i(n+½)λ`, with `Ω_c` the photon-ring orbital frequency and `λ` its Lyapunov
exponent. §56 gives this in closed form for a *static* lapse (Schwarzschild: `Ω_c=λ=1/(3√3 M)`,
`Q=2`). The GW250114 remnant is a *spinning* Kerr hole (χ≈0.79), so we compute the eikonal QNM
from ansatz's **exact Kerr metric** (read-only, the leg-1b pattern): the equatorial prograde
photon orbit `r_ph`, `Ω_c`, `λ` from the Hamiltonian radial potential. The method is gated by
the Schwarzschild limit (must reproduce `Ω_c=λ=1/(3√3)`, `Q=2`, `b_c=3√3`).

**deepstrain (measured, real data).** GW250114 (read-only from BlackHole results):
- remnant (SBI): `M = 78.8 [68.6, 89.5] M⊙`, `χ = 0.787 [0.641, 0.887]`;
- 220 mode (`06_no_hair`): `f₂₂₀ = 257.76 Hz`, `τ₂₂₀ = 4.944 ms` (and 220-self-consistent
  `M=74.8, χ=0.815`); 221: `f₂₂₁ = 214.1 Hz`, `τ₂₂₁ = 2.50 ms`;
- no-hair: `δ = −0.162 [−0.460, +0.334]`, Kerr inside 90%.

## 2. The comparisons (frozen)

- **Quality factor `Q₂₂₀` (the clean, M-independent test).** `Q = π f τ` is dimensionless
  (both `f` and `τ` scale as `1/M`), so it depends only on χ in the eikonal — no mass needed.
  Measured `Q₂₂₀ = π·257.76·0.004944 = 4.00`. Compare to ansatz's eikonal Kerr `Q(χ)`.
- **Dimensionless real frequency `Mω_R₂₂₀`.** `Mω_R = 2π f₂₂₀ · M_sec` (`M_sec = M⊙·4.9255e-6 s`).
  Using the 220-self-consistent `M=74.8`: `Mω_R ≈ 0.597`. Compare to ansatz eikonal `mΩ_c(χ)`.
- **The shadow–ringdown unification (exact, internal).** `Ω_c·b_c = 1 ⇒ ω_R = m/b_shadow`: the
  LIGO ringdown pitch and the EHT shadow are the same photon ring. Verified in ansatz, here on Kerr.

## 3. Predictions (frozen)

- **P1 (Q).** ansatz eikonal Kerr `Q₂₂₀(χ=0.787)` agrees with measured `Q₂₂₀=4.0` within **25%**
  (Q is the most eikonal-sensitive quantity; the band reflects honest eikonal error at ℓ=2).
- **P2 (Mω_R).** ansatz eikonal Kerr `Mω_R(χ)` agrees with the measured value within **15%**.
- **P3 (spin is essential).** The Schwarzschild eikonal (`Q=2`, `Mω_R=0.385`) is **far** from the
  measurement (`Q≈4`, `Mω_R≈0.6`); the Kerr spin correction at χ=0.787 brings ansatz into the P1/P2
  bands. (Confirms the agreement is physics — the light ring — not a coincidence.)
- **P4 (unification, exact).** `Ω_c·b_c = 1` holds for Kerr in ansatz (residual < 1e-6), so the
  measured ringdown frequency is `m` over the exact shadow radius.

## 4. Agreement criterion (frozen)

The leg **succeeds** iff P1 and P2 hold within their bands, P3 holds (Schwarzschild far, Kerr
close), and P4 is exact. This establishes the numeric ringdown bridge. Disagreement is a finding:
either the eikonal is too coarse at ℓ=2 (a known limit — the precise QNM needs Leaver, which
ansatz flags it does not do) or a real tension.

## 5. Honest scope (stated up front, per §7)

- **Eikonal limit.** ℓ=2 is not ℓ→∞; the eikonal QNM carries a few-to-~15% intrinsic error vs
  the exact (Leaver) Kerr 220. The precise overtone spectrum is numerical (Leaver / the `qnm`
  package) — ansatz supplies the exact potential and the exact eikonal limit, and says so (§56 D).
- **No new physics.** QNM↔light-ring, the no-hair test, and Kerr spectroscopy are textbook /
  LVK-active; the contribution is making the spine's ringdown link a real number instead of a
  proposition, by an exact engine cross-checked against real data.
- **Single event, dominant mode.** GW250114, the ℓ=m=2, n=0 mode. The δ / overtone (221) recast
  is noted but the headline is the 220 light-ring comparison.

## 6. Deliverables

- `code/eikonal_kerr_qnm.py` (ansatz venv) — eikonal Kerr QNM `(Ω_c, λ, Q, b_c)` from the exact
  metric, Schwarzschild-gated, swept over χ and evaluated at the remnant spin.
- `code/compare_ringdown.py` — assembles the measured-vs-eikonal comparison table + verdicts.
- `code/plot_ringdown.py` — `Q(χ)` and `Mω_R(χ)` curves with the GW250114 measurement overlaid.
- `FINDINGS.md` — the comparison, the verdicts, honest limits, and the spine-upgrade statement.
