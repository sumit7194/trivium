# V25: independent checks of Fable's "only Kerr" draft (fable_work/only_kerr/), part 1: Fable's P1 (near-axis series), pre-registration

*2026-11-20, written before any V25 code. Sumit: review the three Fable results one at a time.*

**Target.** VE_DERIVATION.md §2. Near a regular axis, F1 = f e^{−2γ} and F2 = 1/f − fω²/ρ² satisfy:
- F1₂ = −f0″/4 + f0′²/(2f0) and F2₂ = (f0 f0″ − f0′²)/(4f0³), both twist-free;
- F1₄ = F1₄^static(f0) − (c0″)²/(64 f0) and F2₄ = F2₄^static(f0) − (c0″)²/(64 f0³).

That is, the twist enters only at ρ⁴, and only as (c0″)². Fable tested it on Kerr (exact) and a static metric. The
twisting non-Kerr case (TS δ=2) is untested; that is its own proposed check P1.

**Disclosure.** I read VE_DERIVATION.md §0–§3, THEOREM_DRAFT.md §1–§3 and CHECKS_PROPOSED.md, but none of Fable's check
code or outputs. I do NOT use Fable's F1₄^static.

**Independence.**
- **F1₄^static and F2₄^static:** I derive them myself in sympy from the static Weyl equations. ψ is axisymmetric
  harmonic, ψ = Σ a_n(z)ρ^{2n} with a₀ = ½ ln f0; γ_ρ = ρ(ψ_ρ² − ψ_z²) with γ(0) = 0; F1 = e^{2ψ−2γ}; F2 = e^{−2ψ}.
- **TS:** the Bridge's own TS2 metric (V11 loader, ts45, σ = k = 1), converted to Weyl form:
  - f = −g_TT and ω = −g_Tφ/g_TT;
  - e^{2γ} = f g_xx(x² − 1)/(x² − y²);
  - (x, y) from (ρ, z) by R± = √(ρ² + (z ± 1)²), x = (R₊ + R₋)/2, y = (R₊ − R₋)/2.
- **Axis data f0(z) and c0(z):** from the TS Ernst potential at y = 1 (the form verified in outreach/PROBLEM; f0 checked
  equal to −g_TT(x, 1)), with c0 = Im of the Ernst E on the axis.

## Check (mpmath, 50 digits)
- **Coefficients.** At z ∈ {2.5, 4, 7} (real outer axis, z = x), extract the ρ², ρ⁴ coefficients of F1 and F2 by a
  degree-6 polynomial fit in ρ² over ρ ∈ [1e−3, 1e−2] (12 points).
  - **Gate:** the fit is stable. Coefficients from two point sets (12 and 16 points) agree to ≤ 1e−20 relative.
- **PASS (TS):**
  - F1₂ and F2₂ match the formulas to ≤ 1e−15 relative.
  - (F1₄ − F1₄^static(f0)) / (−(c0″)²/(64 f0)) = 1 ± 1e−12, and the same for F2 with f0³.
- **Controls:**
  - **Kerr** (kerr45, p = 4/5; the same pipeline, twisting): must also pass. That's the must-pass.
  - **Static Weyl** (ZV δ=2, c0 = 0): F1₄ = F1₄^static to ≤ 1e−15. A must-pass with zero twist.
  - **Must-fail:** replace c0″ by 1.1·c0″ in the TS prediction. The ratio must then be off by ~21%, which shows the
    check is sensitive.

## Verdicts
- **CONFIRMED:** the gate, TS, Kerr and ZV all pass.
- **FALSIFIED:** TS fails beyond tolerance while the controls pass. In particular, a ρ⁴ difference not proportional
  to (c0″)².
- **VOID:** the gate or a must-pass control fails.

**Not covered here:** P2–P6 (return maps; residues; Lemma P; the two-rod example; ZV and Schwarzschild), the Galois
step, and the inherited first-order classification.
