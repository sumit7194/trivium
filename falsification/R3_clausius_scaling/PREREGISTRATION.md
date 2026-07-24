# R3 — Pre-registration: the weak-drive scaling law of the patchwise Clausius violation

*Frozen 2026-07-24, before `code/r3_scaling.py` is written or run. Falsification v2, Tier R — bred from
K3. K3 KILLED patchwise Clausius (Σ_ℓ = S_rel > 0 at every patch size) and noted the fractional violation
**Σ/δQ → 0 as the drive r → 0** — but only sampled r ≥ 0.1. R3's job is to **measure the asymptotic
exponent** of that vanishing, at small r that K3 never reached, and to test whether the coefficient is
patch-size-independent. Reuses the K3/K1 Gaussian machinery unchanged (mpmath dps=60).*

## The postulate under test (and honest tension noted up front)

**"Σ/δQ = c·rᵖ + higher order, with p = 2 (second-order / near-equilibrium) and c(ℓ) independent of patch
size for ℓ ≫ ξ."**

**Rationale for p = 2:** relative entropy between nearby states is *quadratic* in the state distance (the
Fisher/Bures metric). If the squeeze's state perturbation enters δ⟨K⟩ at O(r²) and its r-linear part is
annihilated by the modular structure, then S_rel ~ r⁴ while δQ = Δ⟨K⟩ ~ r², giving Σ/δQ ~ r².

**Honest tension (disclosed before running):** K3c's own data over r ∈ [0.1, 0.8] grows only ~1.8× per
doubling of r near the bottom (local slope ≈ 0.85) — **closer to linear than quadratic.** That range is
**not** asymptotic. R3 goes to r ≤ 0.05 to resolve the true small-r exponent. **A KILL (p ≠ 2) is a live,
informative outcome:** it would say the entanglement-entropy change across the cut is *first*-order in the
drive, correcting the hypothesis and pinning the physics. The exponent is *measured either way* — the
postulate is my theoretically-motivated guess, offered to be killed.

## Method (reused, unchanged)

`K3.patch_pieces(X, P, v, r, ℓ) → (δQ = Δ⟨K⟩, ΔS, Σ = S_rel)` on the same chain (N, μ) and the same
cut-straddling Gaussian excitation `v` as K3/K1. Sweep **r ∈ {0.01, 0.015, 0.02, 0.03, 0.05, 0.08, 0.12,
0.2, 0.3}** × patch **ℓ ∈ {8, 16}**. Small-r window for the asymptotic fit: **r ≤ 0.05**. All quantities in
mpmath dps=60 (Σ = S_rel is a cancellation difference δQ − ΔS ~ o(r²); precision required).

## Frozen gates

- **R3a — the exponent (headline; a MEASUREMENT, verdict either way).** Fit `log(Σ/δQ)` vs `log r` in the
  small-r window (ℓ = 16); report **p_ratio**. Separately fit **p_Σ** (Σ vs r) and **p_δQ** (δQ vs r) and
  check the consistency **p_ratio ≈ p_Σ − p_δQ** (a self-check on the fits). Postulate **SURVIVES** iff
  `|p_ratio − 2| ≤ 0.2`; **KILLED** iff outside — and the measured p_ratio (and the decomposition p_Σ, p_δQ)
  is reported as the finding.
- **R3b — patch-independence of the coefficient.** `c(ℓ) = (Σ/δQ)/r^{p_ratio}` extrapolated to small r must
  agree across ℓ ∈ {8, 16} to within **15%** (both patches cover the excitation, ξ = 2 sites at μ = 0.5).
  PASS = the leading coefficient is a patch-size-independent (bulk) number, not an edge artifact.
- **R3c — framing (not a gated number).** The measured law is the quantitative statement of *how* the
  localization approximation degrades with drive — the closest a lattice gets to **bounding** (not proving)
  the localization postulate's domain of validity. Scope frozen: the **modular/entanglement** first law
  (not the horizon-area Clausius, which needs S = A/4), toy model, no continuum claim.

## Honest scope

- Whatever p comes out, R3 is a **measurement** completing the leg X → K3 arc, not a proof about gravity.
- Reuses K3's exact-arithmetic pipeline; a fit exponent has its own numerical error (reported), distinct
  from the mpmath precision of each Σ, δQ.
- Bridge-solo; no sister; no external dependency.
