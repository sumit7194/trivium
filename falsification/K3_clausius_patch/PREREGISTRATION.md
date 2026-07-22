# K3 — Pre-registration: patchwise Clausius (δQ = TδS) fails at every patch size

*Frozen 2026-07-23, before `code/k3_clausius.py` is written or run (the entropy-production curve was scouted
in a scratchpad to set honest thresholds; the production script re-derives it under the gates). Ledger item
K3 (Tier K). Reuses the K1 / leg X modular machinery. The most philosophically loaded of the first volley:
it aims at the **one link both emergent-gravity derivations only assume**.*

## The postulate under attack (Ledger K3)

> **"Clausius δQ = TδS holds exactly at every patch size"** — the lattice analog of the **localization
> postulate**.

Leg X's §115 anatomy labeled the localization postulate — *"integral equality for all local Rindler
horizons ⟹ integrand equality"* — as the **one ASSUMED, non-proven link** in Jacobson's chain (1995 and the
2026 Dorau–Much upgrade alike). Its lattice analog is the claim that the thermodynamic identity holds not
just integrated over a wedge but **patchwise, at every sub-patch size**, exactly.

## The precise relation tested (and its honest scope)

In modular units (Bisognano–Wichmann: K_vac = 2π × boost, so the 2π's cancel), "δQ = TδS" for a patch A_ℓ is
the **modular / entanglement first law**

    Δ⟨K_ℓ⟩  =  ΔS_ℓ        ( δQ = modular-energy flux;  TδS = entanglement-entropy change ) ,

and its exact failure is the **entropy production**

    Σ_ℓ  ≡  Δ⟨K_ℓ⟩ − ΔS_ℓ  =  S_rel(ρ_ℓ ‖ vac_ℓ)  ≥  0

— the relative entropy of the patch (Σ = 0 ⇔ exact Clausius ⇔ reversible). **Honest scope, frozen:** this is
the *entanglement-thermodynamics* form of Clausius (the relative-entropy first law), the lattice witness of
the localization *assumption*. It is **not** Jacobson's horizon-*area* Clausius, which additionally invokes
S = A/4 (leg X's separate ASSUMED link). Exactly as leg X validated the *hinge identity*, not the S = A/4
conclusion, K3 measures the *entropy-production correction*, not the area law.

## Setup (frozen — inherits K1)

- Chain N = 96, μ = 0.5, entangling cut x_c = 48.5 (region A = sites 49…96); mpmath **dps = 60** (float64
  divides-by-zero on the deep-wedge modular spectrum for large patches — leg X's O4 wall — so the exact
  instrument is used throughout).
- **Excitation:** a squeezed packet **straddling the cut** (K1's kill geometry: v = unit Gaussian centred on
  x_c, width σ = 2.5, squeeze r), so ΔS_ℓ ≠ 0 (cross-cut entanglement — the only kind that moves the entropy;
  K1's lesson). Coherent (displacement) excitation used for the degenerate control K3d.
- **Patch:** A_ℓ = the first ℓ sites of region A, adjacent to the cut (a sub-wedge slab of width ℓ);
  **ℓ ∈ {1, 2, 3, 4, 6, 8, 12, 16, 24, 32}**. Per patch: vacuum modular form G of A_ℓ (K1 `modular_blocks`),
  Δ⟨K_ℓ⟩ = ½Tr(G(γ_ρ,ℓ − γ_vac,ℓ)), ΔS_ℓ from the reduced symplectic spectra, Σ_ℓ = Δ⟨K_ℓ⟩ − ΔS_ℓ.

## Frozen gates

- **K3a — the KILL (primary).** For a squeezed excitation (r = 0.6), the entropy production is nonzero at
  every accessible patch size: **Σ_ℓ / δQ_ℓ > 0.10 for all ℓ ≥ 2** (and Σ_ℓ > 0 for ℓ = 1). → **KILLED**:
  exact patchwise Clausius holds at *no* patch size. → SURVIVES only if Σ_ℓ ≈ 0 (< 1% of δQ) at all ℓ.

- **K3b — entropy production IS the relative entropy (positive + monotone; V1 built-in).** Σ_ℓ = S_rel,ℓ ≥ 0
  and **monotone non-decreasing in ℓ** (nested patches ⇒ relative-entropy monotonicity, Ledger V1). A
  decrease ⇒ machinery bug, not physics. Certifies Σ is a genuine irreversibility measure, and it **saturates**
  once ℓ exceeds the excitation support (the packet is localized at the cut) — a physical, not numerical,
  plateau.

- **K3c — near-equilibrium scaling (the curve's physics).** At fixed patch (ℓ = 2), the fractional violation
  Σ/δQ **→ 0 as the excitation strength r → 0** (entropy production is second-order / near-equilibrium) and
  grows toward O(1) for strong driving. Frozen: **(Σ/δQ)|_{r=0.1} < 0.3 · (Σ/δQ)|_{r=0.6}**. This is the
  quantitative statement of *how* the localization/near-equilibrium approximation degrades with driving.

- **K3d — the coherent degenerate control.** For a coherent (displacement) excitation, ΔS_ℓ = 0 exactly
  (K1), so **Σ_ℓ = δQ_ℓ** (Σ/δQ = 1 to < 1e-6): the modular energy is *entirely* entropy production
  (Longo: S_rel(coherent) = Δ⟨K⟩). Reported to bracket the two extremes — coherent (Σ/δQ = 1) vs squeezed
  (Σ/δQ < 1) — and to flag honestly that a *classical* (coherent) matter flux is the maximal-Σ case in this
  entanglement-first-law reading (which is why the horizon-area version, not this one, is what Jacobson uses).

- **K3e — precision canary.** The largest float64-safe patch (ℓ = 8) recomputed in float64 agrees with mpmath
  to < 1e-6 (documents where the float64 wall begins — small patches safe, large patches need mpmath).

## Honest limits (fixed in advance)

- Toy model only — harmonic chain, one excitation family; labeled as such. Not a statement about nature.
- Tests the **entanglement/modular first law** (relative-entropy Clausius), *not* the horizon-area Clausius
  (needs S = A/4). The measured Σ_ℓ curve is the payout: a home-built witness that the patchwise identity
  carries a positive, relative-entropy-valued, near-equilibrium correction at every scale — i.e. *why*
  localization is an assumption, not a theorem.
- **Open extension (explicitly not claimed here):** the a → 0 continuum limit at fixed physical patch is
  under-determined by 3 lattice points and is left as future work (needs the bigger instrument — feeds G4/G7).

## Anchors (read-only)

Jacobson 1995 (gr-qc/9504004; the localization postulate) · Dorau–Much 2026 (arXiv:2510.24491) · Casini 2008
(relative entropy & the Bekenstein bound) · leg X §115 anatomy · reuses K1 `k1_squeezed.py`. Interpreter:
conjecture_machine `.venv` (mpmath 1.3.0, numpy 2.4.6).
