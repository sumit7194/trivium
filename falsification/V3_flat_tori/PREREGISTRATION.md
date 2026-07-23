# V3 — Pre-registration: 2D flat tori ARE determined by their spectrum (the converse of K2)

*Frozen 2026-07-23, before `code/v3_tori.py` is written or run (the modular controls were scouted to confirm
the lattice convention; the production script re-derives everything under the gates). Ledger item V3
(Tier V — validation, expected to SURVIVE). The honest converse to [K2](../K2_isospectral_drums)'s kill:
having shown you cannot hear the shape of a *drum*, show that you **can** hear the shape of a flat 2-torus —
and measure how well.*

## The postulate (Ledger V3)

> **"2D flat tori ARE determined by their spectrum"** — a real theorem, the converse of K2's kill.

**This is true, and it is dimension-dependent — which must be stated precisely or the postulate becomes a
self-inflicted kill.** Flat tori are spectrally determined in **low dimension only**: dimension 2 (and 3) yes;
**dimension 4** has isospectral non-isometric pairs (Conway–Sloane), and **dimension 16** is Milnor's famous
counterexample (two non-isometric flat 16-tori with identical spectra). V3 is therefore stated and tested
**strictly for 2D**, where it holds.

## The setup (frozen)

A flat torus is T² = ℝ²/Λ. Its Laplace spectrum is **λ = 4π²|w|², w ∈ Λ\*** (the dual lattice) — so the
spectrum is exactly the norm multiset of Λ\*. Weyl already fixes the area from the spectrum, so the only
question is **shape**: all tori are normalised to **unit covolume**, leaving the modulus
τ = x + iy in the standard fundamental domain **F = {|Re τ| ≤ ½, |τ| ≥ 1, Im τ > 0}**. Distinct points of F
are **non-isometric** tori; points related by SL(2,ℤ) are the *same* torus.

- Lattice basis (unit covolume): v₁ = (1/√y, 0), v₂ = (x/√y, √y); dual basis (B⁻¹)ᵀ.
- Spectrum: the **lowest K = 40** values of 4π²|w|² over w = a·w₁ + b·w₂, |a|,|b| ≤ 14.
- Spectral distance between two tori: **max|Δλ|/λ̄** over the lowest K eigenvalues.
- Moduli distance: the **hyperbolic** metric on the upper half-plane,
  d(τ₁,τ₂) = arccosh(1 + |τ₁−τ₂|²/(2y₁y₂)) — the natural metric on moduli space.

## Frozen gates

- **V3c — the modular control (canary; run first).** SL(2,ℤ)-equivalent moduli describe the *same* torus and
  so **must** be isospectral: τ vs τ+1, τ vs τ−1, τ vs −1/τ agree to **rel < 1e-12**. If this fails the
  lattice/dual convention is wrong and every other number is void.

- **V3a — no spurious isospectral pairs (the postulate).** Over **2000** random pairs of moduli sampled from
  F, **every** pair separated in moduli by hyperbolic distance > 0.1 has spectral distance
  **> 1e-6** — i.e. no two genuinely different flat 2-tori share a spectrum at this resolution.
  → **SURVIVES** if satisfied. → **KILLED** if any well-separated pair is isospectral to < 1e-9 (which would
  contradict the 2D theorem and mean a bug or a genuine discovery — either way it stops the run for review).

- **V3b — the resolution bound (the honest deliverable).** Perturbing a modulus by δ, the spectral distance
  scales **linearly** in δ (fit exponent p ∈ [0.9, 1.1] over δ ∈ [1e-6, 1e-2]) down to a numerical noise
  floor. Report the **resolving power**: the smallest moduli separation still distinguishable above the floor,
  and how it improves with the number of eigenvalues K ∈ {10, 40, 160}. This is what "bounds the instrument's
  resolution" means concretely — the spectrum determines the torus, but only to a finite precision set by how
  many eigenvalues you can measure.

- **V3d — the K2 contrast (the story, not a numeric gate).** State the pair explicitly: GWW **drums** are
  isospectral **but not** isometric (K2, killed); flat **2-tori** are isospectral **iff** isometric (V3,
  survives). "Can you hear the shape?" has no universal answer — it depends on the class of object and the
  dimension.

## Honest limits (fixed in advance)

- **Known theorem, zero novelty claimed.** The payout is Tier-V's stated one: instrument hardening plus a
  measured resolution bound, and completing the hearing-shapes story honestly alongside K2.
- **Strictly 2D.** The result does *not* generalise: 4D (Conway–Sloane) and 16D (Milnor) flat tori admit
  isospectral non-isometric pairs. Any statement about "flat tori" without a dimension is false.
- Finite eigenvalue count and finite dual-lattice enumeration are the only approximations; both are reported,
  and V3b measures exactly the resolution they impose.

## Anchors (read-only)

Milnor 1964 (16-D counterexample) · Conway–Sloane (4-D isospectral lattices) · Kac 1966 · Gordon–Webb–Wolpert
1992 · [K2](../K2_isospectral_drums). Interpreter: conjecture_machine `.venv` (numpy 2.4.6).
