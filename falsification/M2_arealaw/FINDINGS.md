# M2 — Findings: the S = A/4 coefficient is regulator-dependent (where the "1/4" hides)

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item M2
(Tier M). Depends on [V2](../V2_cft_calibration) (entropy instrument calibrated to c=1, float64 cleared).
**Verdict: KILLED** — as expected for a Tier-M "we hunt it in the kill-me direction"; the payout is the clean
separation of the universal from the scheme-dependent.*

## Result in one line

The 3D free-scalar entanglement area-law coefficient κ (S ≈ κ (R/a)²) takes **three clearly different values
— 0.301, 0.414, 0.511 (a 51% spread)** — under three UV regulators, while the **area-law exponent stays
≈ 2.0 in all three** and a coordinate-only change leaves κ fixed (0.296 vs 0.301). The "1/4" in S = A/4 lives
in the **regulator-dependent coefficient**; the area *law* is universal.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **M2a** (anchor) | R1 bare-NN reproduces Srednicki | κ = **0.3014** ∈ [0.28,0.32], p = 1.961 | **PASS** (Srednicki κ≈0.295) |
| **M2b** (KILL) | κ spread across regulators > 20% | (0.511−0.301)/0.409 = **51.2%** | **M2 KILLED** |
| **M2c** (universality) | area-law exponent ≈ 2 for all | p = **1.961 / 1.934 / 1.969** | **PASS** (law universal, κ is not) |
| **M2d** (coord control) | midpoint coordinates leave κ fixed | Δκ/κ = **1.77%** (0.296 vs 0.301) | **PASS** (coord change ≠ regulator change) |
| **M2e** (robustness) | R1<R2<R3 ordering stable under L₀, n-window, N | stable in all 3 variations | **PASS** |

## The three regulators (same IR theory, different UV)

| regulator | κ | exponent p | what differs in the UV |
|---|---|---|---|
| **R1** bare nearest-neighbour lattice (Srednicki) | **0.301** | 1.961 | standard sharp lattice cutoff |
| **R2** improved (Symanzik) 4th-order stencil | **0.414** | 1.934 | removes leading O(a²) dispersion artifact |
| **R3** higher-derivative smooth (K→K+0.1K²) | **0.511** | 1.969 | analytic UV stiffening (smooth-cutoff axis) |

All three have ω² → k² as k → 0 (the same continuum free scalar) and share the area-law exponent; they differ
only in short-distance modes — exactly the freedom that fixes κ. R1 reproduces Srednicki's published κ ≈ 0.295,
which anchors the machinery.

## Why this is the sharp statement of "where the 1/4 hides"

Two numbers come out of the same calculation, and M2 separates them cleanly:

- **The exponent (= 2) is universal** — the area law S ∝ R² is regulator-invariant to ~2% across all three
  schemes (M2c). This is real physics: entanglement of a local QFT lives on the boundary.
- **The coefficient κ is not** — it moves by 51% when the UV regulator changes (M2b), and it is precisely the
  coefficient that would have to equal 1/4G to make S = A/4 (Srednicki's motivation). A cutoff computation
  cannot pin it down; only a full quantum-gravity input (the Newton constant's own renormalisation) can.

The **coordinate control (M2d)** is what makes this a measurement rather than fitting noise: changing the
lattice *coordinates* (midpoint r_j = j−½ instead of r_j = j) — the *same* regulator — leaves κ fixed to 1.8%,
while changing the *regulator* moves it by tens of percent. The spread is regulator physics, not an artifact of
the extraction.

## Method notes (the two pitfalls, and how they were handled)

- **The ℓ-sum converges slowly.** S(n) = Σ_ℓ (2ℓ+1) S_ℓ(n) has a tail (2ℓ+1)S_ℓ ~ ℓ^{−q}, q ≈ 2.5–2.7. A
  naive cutoff at ℓ_max ≈ n gives κ **off by ~2×** (0.12 instead of 0.30 at n=40). The production run sums to
  L₀ = 500 and adds an analytic power-law tail; the extracted κ is stable under L₀ ∈ {400,500} (M2e).
- **Finite radial box.** N = 200 ≫ n keeps the exterior a faithful "rest of space"; κ is stable under
  N ∈ {150,200} (M2e). The residual drift of S/n² with n is the leading subleading term, absorbed by the
  constant c in the fit S = κn² + c.
- **Precision:** float64 throughout, licensed by V2c (float64 = mpmath to 5×10⁻⁹ for these shallow ball
  spectra — no leg-X modular precision wall here).

## Honest limits (frozen in advance)

- Toy model only — free scalar on a radial lattice. This is a statement about a **lattice fact** (the
  entanglement area-law coefficient is regulator-dependent), **not** about the actual S = A/4 of a black hole,
  which requires the gravitational path integral. Labeled as such, like every leg.
- Expected KILL (Tier M): the demonstration *is* the payout. No novelty is claimed — the scheme-dependence of
  the entanglement coefficient is well known (Srednicki; Bombelli et al; Solodukhin's reviews). The value is a
  calibrated, home-built, control-gated separation of exponent (universal) from κ (scheme) on the family's own
  instrument, a direct sequel to leg X and the emergent-gravity thread.
- "Cutoff-shape" regulator (R3) is realised at the field level (higher-derivative), not by literal
  boundary-smearing: in a free Gaussian theory boundary-smearing has no clean entanglement-entropy definition,
  whereas a smooth UV cutoff is rigorous and is the same mechanism — stated in the pre-registration.

## Inputs (read-only) & artifacts

Srednicki 1993 (hep-th/9303048) · Bombelli–Koul–Lee–Sorkin 1986 · Solodukhin 2011 (review) · calibrated by
[V2](../V2_cft_calibration); reuses the leg X / K1 / V2 covariance-entropy machinery. `code/m2_arealaw.py` ·
`results/m2_arealaw.json`. Interpreter: conjecture_machine `.venv` (numpy 2.4.6).
