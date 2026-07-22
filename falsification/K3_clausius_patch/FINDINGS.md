# K3 — Findings: patchwise Clausius (δQ = TδS) fails at every patch size

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item K3
(Tier K), the most philosophically loaded of the first volley — it aims at the **one link both
emergent-gravity derivations only ASSUME** (the localization postulate, logged in leg X §115). **Verdict:
KILLED**, and the payout is the measured entropy-production curve. Reuses the K1 / leg X modular machinery.*

## Result in one line

The patchwise **modular first law** Δ⟨K_ℓ⟩ = ΔS_ℓ (the relative-entropy form of Clausius δQ = TδS) fails at
**every** patch size for a squeezed excitation, by a positive, relative-entropy-valued **entropy production**
Σ_ℓ = S_rel,ℓ that rises from 0.45·δQ (ℓ=1) to a saturated 0.71·δQ, is monotone in ℓ (relative-entropy
monotonicity, V1), **vanishes as the excitation strength → 0** (near-equilibrium, second-order), and is
degenerate for coherent excitations (ΔS=0 ⇒ Σ=δQ). Exact patchwise Clausius holds at *no* patch size.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **K3a** (KILL) | Σ_ℓ > 0 ∀ℓ and Σ/δQ > 0.10 ∀ℓ≥2 | Σ/δQ ∈ [0.45, 0.71] across all ℓ | **K3 KILLED** |
| **K3b** (V1 canary) | Σ_ℓ = S_rel ≥ 0, monotone ↑ in ℓ, saturating | monotone; plateaus past excitation scale | **PASS** |
| **K3c** (near-equilibrium) | Σ/δQ → 0 as excitation r → 0 | (Σ/δQ)\|_{0.1}=0.13 < 0.3·(Σ/δQ)\|_{0.6}=0.16 | **PASS** |
| **K3d** (coherent control) | displacement ⇒ ΔS=0 ⇒ Σ=δQ | ΔS = 0, Σ/δQ = 1.000000 | **PASS** |
| **K3e** (precision canary) | float64 vs mpmath at ℓ=8 | rel **2.6×10⁻¹⁰** | **PASS** (float64 wall begins at large ℓ) |

## The entropy-production curve (K3a/K3b — the ledger's ask)

Squeezed excitation straddling the cut, r = 0.6, patch A_ℓ = ℓ sites adjacent to the cut:

```
  ℓ |  δQ=Δ⟨K⟩ | TδS=ΔS  | Σ=S_rel |  Σ/δQ
  1 |  0.7586  | 0.4194  | 0.3393  | 0.447
  2 |  0.9898  | 0.4581  | 0.5317  | 0.537
  4 |  1.3062  | 0.4412  | 0.8650  | 0.662
  8 |  1.4811  | 0.4372  | 1.0439  | 0.705
 16 |  1.4886  | 0.4373  | 1.0513  | 0.706
 32 |  1.4888  | 0.4373  | 1.0515  | 0.706   (saturated)
```

Σ_ℓ is the relative entropy of the patch — it **increases monotonically** with ℓ (nested patches ⇒
relative-entropy monotonicity, a direct check of Ledger V1) and **saturates** once the patch covers the
excitation's support (the packet is localized at the cut). The saturation is physics, not a numerical
plateau. Exact Clausius (Σ = 0) holds at no ℓ.

## The physics of the violation (K3c/K3d — where localization actually stands)

- **Near-equilibrium (K3c):** the fractional violation Σ/δQ → 0 as the squeeze r → 0 (0.13 at r=0.1, 0.54 at
  r=0.6, 0.64 at r=0.8). The entropy production is a genuine **second-order, near-equilibrium** quantity: for
  weak driving, patchwise Clausius holds to good fractional accuracy; the correction grows to O(1) as you
  drive the system harder. This is the quantitative statement of *how* the localization approximation
  degrades — it is not exact, but it is controlled.
- **Coherent degenerate case (K3d):** for a coherent (displacement) excitation ΔS_ℓ = 0 exactly (K1's
  lesson), so Σ_ℓ = δQ_ℓ — the modular energy is *entirely* entropy production (Longo:
  S_rel(coherent) = Δ⟨K⟩). Coherent and squeezed bracket the extremes: Σ/δQ = 1 vs Σ/δQ < 1.

## Honest scope — what K3 does and does not touch

Exactly parallel to leg X (which validated the *hinge identity*, not the S = A/4 conclusion), K3 measures the
**entanglement/modular first law** Δ⟨K⟩ = ΔS and its entropy-production correction. It is **not** Jacobson's
horizon-*area* Clausius, which additionally invokes S = A/4 — a separate ASSUMED link. In particular the
coherent (classical) matter flux being the *maximal*-Σ case here (Σ/δQ = 1) is **not** a failure of Jacobson:
his δS is the horizon area response δA/4G, not the matter entanglement change ΔS_ℓ that vanishes for coherent
states. K3's value is the lattice witness that the *patchwise* identity carries a positive,
relative-entropy-valued correction at every scale — i.e. *why* the localization step is an assumption, not a
theorem, made quantitative on the family's own instrument.

## Method notes

- mpmath dps=60 throughout: float64 divides-by-zero on the deep-wedge modular spectrum for large patches
  (leg X's O4 wall); K3e confirms float64 = mpmath to 2.6×10⁻¹⁰ for small patches (ℓ≤8) and documents that
  the wall begins only where the patch reaches deep into the wedge — irrelevant here since Σ_ℓ saturates at
  the excitation scale (ℓ≈8) long before.
- A canary bug caught in-run: the first K3e clipped ν² at 0.5 (forcing ν≥0.71) instead of at 0.25 (ν≥½),
  faking a 44% float64 discrepancy; fixed to a genuine 2.6×10⁻¹⁰ agreement.

## Honest limits (frozen in advance)

- Toy model only — harmonic chain, one excitation family, μ=0.5; labeled as such.
- Tests the modular/entanglement first law, not the horizon-area Clausius. Tier-K expected kill: the payout
  is the measured Σ_ℓ curve and its near-equilibrium scaling.
- **Open extension (explicitly not claimed):** the a→0 continuum limit at fixed physical patch drifts over
  the 3 lattice points reachable here and is left as future work — it needs the bigger instrument (feeds
  G4/G7, the walls-are-instrument-relative theme).

## Inputs (read-only) & artifacts

Jacobson 1995 (gr-qc/9504004) · Dorau–Much 2026 (arXiv:2510.24491) · Casini 2008 · leg X §115 anatomy;
reuses K1 `k1_squeezed.py`. `code/k3_clausius.py` · `results/k3_clausius.json`. Interpreter:
conjecture_machine `.venv` (mpmath 1.3.0, numpy 2.4.6).
