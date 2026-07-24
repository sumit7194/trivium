# R3 — Findings: the weak-drive scaling law — postulate p=2 KILLED, and the first law holds to first order

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier R — measures the small-r exponent K3 could not reach (K3 stopped at r=0.1). Reuses K3/K1 mpmath dps=60.
The postulate (fractional Clausius violation Σ/δQ ∝ r²) is **KILLED** — and the kill decomposes into a
cleaner physical statement than the hypothesis.*

## Result in one line

The fractional patchwise-Clausius violation scales **~r (linear), not r²** — measured exponent
**p(Σ/δQ) = 0.89** (→ 1 as r→0), so the postulate p=2 is **KILLED**. But the decomposition is the finding:
**Σ = S_rel ~ r² (p = 2.02)** and **δQ = Δ⟨K⟩ ~ r (p = 1.12)** — the entropy *production* is genuinely
second-order, while the *heat* is first-order. Hence **the patchwise first law δQ = TδS holds exactly to
first order in the drive**; the violation Σ is the second-order residual. The r²-vs-r linear coefficient is
patch-size-independent to **0.76%** (R3b PASS).

## The gates

| gate | check | result |
|---|---|---|
| R3a | measure p(Σ/δQ); postulate SURVIVES iff \|p−2\|≤0.2 | **p = 0.891 → KILLED** (\|0.89−2\|=1.11). Decomposition p_Σ=2.015, p_δQ=1.124; consistency p_ratio = p_Σ−p_δQ exact to **0.000** |
| R3b | coefficient c(ℓ) patch-independent (ℓ=8 vs 16) to 15% | **PASS** — c=2.508 vs 2.527, rel diff **0.76%** |

## The decomposition (the real result)

| quantity | measured exponent | asymptotic | reading |
|---|---|---|---|
| Σ = S_rel (entropy production) | 2.015 | **2** | second-order — *the r² intuition was right here* (relative entropy is Fisher-quadratic) |
| δQ = Δ⟨K⟩ (modular heat) | 1.124 | **1** (→1 as r→0) | **first-order** — the piece the postulate got wrong |
| Σ/δQ (fractional violation) | 0.891 | **1** | linear = r²/r |

**What this means physically.** The postulate conflated two different things: *"the entropy production is
second-order"* (TRUE — Σ = S_rel ~ r²) and *"the fractional violation is second-order"* (FALSE — it is
linear, because the heat δQ is itself only first-order-small). Disentangling them gives a statement more
favorable to localization than the hypothesis assumed:

> **The patchwise modular first law δQ = TδS is exact to *first* order in the drive** — the linear parts of
> Δ⟨K⟩ and ΔS match. The violation Σ = S_rel is purely the **second-order residual**, and it is a genuine
> relative entropy (≥ 0). The *fractional* irreversibility Σ/δQ ≈ 4·r therefore degrades **linearly** with
> drive, patch-size-independently.

So K3's "Σ/δQ → 0 as r → 0" is now resolved: it vanishes *linearly*, not quadratically, and the reason is
that the first law holds to first order while the second-order residual rides on a first-order heat.

## Why this is a good kill (L3)

A survival would have said "p=2, as guessed." The kill instead **output a mechanism**: the exponent
decomposition (2, 1, 1), an exact internal consistency check (p_ratio = p_Σ − p_δQ to 0.000 — the fits are
self-certifying), and a sharper physical claim (first law exact to first order; fractional degradation
linear). That is Tier-K/R's stated payout — a kill that returns a curve and a reason, not a boolean.

## Honest scope

- **Modular/entanglement first law only** — Δ⟨K⟩ = ΔS for the reduced state — **not** the horizon-area
  Clausius δQ = TδA/4G that Jacobson uses (that needs S = A/4, a separate assumed link). This is the lattice
  witness of *how the localization approximation degrades*, quantified — not a statement about gravity.
- The finite-r fits (2.02, 1.12, 0.89) sit slightly off the clean asymptotics (2, 1, 1) because of
  subleading r² curvature; the local slope of Σ/δQ rises toward 1 at the smallest r (0.94 at r=0.01–0.015),
  consistent with p_ratio → 1. Reported honestly rather than rounded.
- Toy model (N=96 harmonic chain, μ=0.5), exact Gaussian arithmetic; a fit exponent carries its own error
  distinct from the mpmath precision of each Σ, δQ.

## Inputs & artifacts

Reuses `K3_clausius_patch/code/k3_clausius.py` (→ K1's leg-X Gaussian pipeline), mpmath dps=60 via ansatz
venv. · `code/r3_scaling.py` · `results/r3_scaling.json`.
