# V19: pre-registration. A Poincaré resonance obstruction for the MN quadrupole at first order (all valences)

*2026-11-17, ~21:45 IST. Written and committed BEFORE any V19 code exists or runs. Sumit's go: 2026-11-17 ("you can
also run your resonance check").*

## Question
V17 showed, by a local jet method, that no Kerr Killing tensor of valence ≤ 6 extends to first order in the MN quadrupole
β. V19 asks the stronger, global question with a completely different method:

> Does **any** smooth first-order integral F = F₀ + βF₁ exist, where F₀ is a function of Kerr's integrals
> (H₀, E, L_z, Q) that genuinely depends on Carter's Q?

That covers polynomial Killing tensors of any valence and non-polynomial integrals alike.

## Method: Poincaré's resonance argument, in Mino time
1. **The flow.** For fixed E and L_z (exactly conserved in MN, since it is stationary and axisymmetric), the reduced
   Kerr motion in (r, θ) is integrable and separates in Mino time λ:
   - (dr/dλ)² = R(r) and (dz/dλ)² = Z(z), with z = cos θ;
   - dλ_affine = Σ dλ, where Σ = r² + a² z².
2. **The function to expand.** The perturbation in Mino time is F(q_r, q_θ) = Σ · H₁, with
   H₁ = ½ G₁^{ab} p_a p_b and G₁ = −G₀ h G₀, where h = ∂g/∂β at β = 0.
   - It is taken from the bridge's V9 MN transcription in MN's (x, y) chart, with r = M + k x and y = z.
   - The momenta on the torus are p_t = −E, p_φ = L_z, p_x² = k² R/Δ² and p_y² = Z/(1 − z²)².
   - H₁ is quadratic with a diagonal (x, y) block, so the momentum signs don't matter.
   - F is evaluated on a uniform grid in the Mino angles q_r = Υ_r λ_r and q_θ = Υ_θ λ_θ. Here r(q_r) and z(q_θ) come
     from the separated quadratures, with q = 0 at periapsis and at z_max.
3. **The obstruction.**
   - If such an F exists, then on every resonant torus k·Υ = 0 the Fourier coefficient satisfies
     (k·∂F₀/∂J) · F_k = 0.
   - For F₀ depending on Q, k·∂F₀/∂J ≠ 0, because Q is functionally independent of H₀.
   - So a nonzero resonant coefficient F_k, for k ⟂ Υ, rules out every such integral on that torus. That holds for all
     valences and for non-polynomial integrals too.
4. **Resonances.** Υ_r : Υ_θ = 1 : 2 and 2 : 3, giving k = (2, −1) and (3, −2).
   - The tori are set by (r_p, r_a, z_max), and E, L_z and Q are solved from R(r_p) = R(r_a) = 0 and Z(z_max) = 0.
   - r_a is tuned with mpmath findroot until |Υ_r/Υ_θ − p/q| < 1e−20.

**Normalisation.** The statistic is ρ = |F_k| / max(|F₀₀|, |F₁₀|, |F₀₁|): the resonant coefficient relative to the
leading non-resonant ones. Arithmetic: mpmath, 40 digits; grid N = 64 and N = 128 (they must agree).

## Parameters
- Kerr base: (M, a) = (5, 3), so k = 4. This is V17's p1, in the same MN chart, with μ² = 1.
- Two tori per resonance, at different (r_p, z_max):
  - T1: r_p ≈ 4M, z_max ≈ 0.5;
  - T2: r_p ≈ 6M, z_max ≈ 0.3.
  - r_a is fixed by the resonance.

  The exact values are chosen by the code from these targets and recorded before F is computed.

## Gates and controls, run first; any failure means STOP
- **G1, the mass shell and chart.** At every grid point, H₀ evaluated from the MN g₀ in (x, y) with the momenta above
  must equal −1/2 within 1e−30. This catches chart, sign-of-a and momentum-mapping errors.
  - Both signs of a are tried; exactly one sign must pass. Unlike V17, H₀ itself is sign-sensitive through the
    E·L_z term.
- **G2, resonance and convergence.**
  - |Υ_r/Υ_θ − p/q| < 1e−20;
  - the F_k values at N = 64 and N = 128 agree to 1e−12 relative, or to 1e−25 absolute.
- **C1, integrable deformations must give no obstruction.**
  - h = ∂g/∂M at fixed (x, y), and h = ∂g/∂a, both at β = 0.
  - Either one must give ρ < 1e−15 at every resonant torus. (If ΣH₁ = h(J) + {K₀, χ}, then F_k ∝ k·Υ, which vanishes.)
- **C1b, a null deformation.** G₁ = −L_ξ G₀ with V17's ξ = (x³/3) ∂_x + y² ∂_y, computed exactly by symbolic
  differentiation. It must give ρ < 1e−15.
- **C2, a deformation that must obstruct.** V17's sabotage, x·y in the tt slot only. It must give ρ > 1e−6 on at least
  one resonant torus. If not, the test is blind and V19 is VOID.

## Target and verdict
**Target:** the MN β-derivative, at all 4 resonant tori.

**Verdict:**
- **OBSTRUCTED** (no first-order integral involving Q exists, at any valence): ρ > 1e−6 at **every** resonant torus,
  with both N, after all gates and controls pass. Even one torus suffices logically; all four strengthen it.
- **NOT OBSTRUCTED / INCONCLUSIVE:** ρ < 1e−15 at every torus. That would conflict with V17 and with §153, and would
  be reported as such.
- **MIXED:** report each torus as measured.

## What this does and does not establish
- **Logically,** a nonzero resonant coefficient on a single resonant torus rules out a smooth first-order integral F₀(J) +
  βF₁ near that torus, for any F₀ with k·∂F₀/∂J ≠ 0. That's the classical Poincaré argument, under the
  nondegeneracy that Kerr's frequency ratio actually varies across the family. V19 doesn't prove that nondegeneracy;
  it checks it numerically: Υ_r/Υ_θ changes with r_a near each torus.
- **Numerics:** the statement is high-precision numerical (40-digit quadrature and FFT), not interval-certified. An
  interval version could follow if the result is wanted at proof grade.
- **Not covered:**
  - second order in β;
  - the exact MN metric, which V10-MN covers to valence 10;
  - tori far from the chosen ones (but resonant tori are dense, and one obstruction suffices).

## Resources
1 core at nice 10. Memory under 2 GB, disk under 20 MB. The run stops itself if free disk falls below 5 GB.

## Amendment 1 (2026-11-17, before any F value is computed): which tori are feasible
A scan of Kerr's frequency ratio Υ_r/Υ_θ over r_a showed two registered targets are infeasible. Only the frequency
ratio was computed; no H₁, F or coefficient values.
- **(r_p = 4M, z_max = 0.5):** the ratio climbs from 0.37 at r_a = 6M to 0.62 at r_a = 40M. 1 : 2 is reachable,
  but 2 : 3 is not within r_a ≤ 40M.
- **(r_p = 6M, z_max = 0.3):** the ratio is ≥ 0.63. 2 : 3 is reachable, but 1 : 2 is not.

Replacement tori, picked by the same scan, with r_a set by tuning:
- **1 : 2:** (r_p, z_max) = (4M, 0.5) at r_a ≈ 10M, and (4.5M, 0.3) at r_a ≈ 7M.
- **2 : 3:** (6M, 0.3) at r_a ≈ 10M, and (5M, 0.5) at r_a ≈ 17M.

Nothing else changes: gates, controls, thresholds and verdict rules all stay as registered.

## Addendum 2 (2026-11-17, AFTER the registered run, which gave MIXED): a parity follow-up, registered before running
**Registered verdict: MIXED**, recorded as such in FINDINGS.md. The MN target was resonant-nonzero on both 2 : 3 tori
(ρ = 2.1e−5 and 6.4e−4) but zero (≈ 1e−41) on both 1 : 2 tori. The sabotage was the reverse: nonzero on the 1 : 2
tori, zero on the 2 : 3 tori.

**Hypothesis (post hoc, which is why it is tested here):** a parity selection rule.
- z(q_θ + π) = −z(q_θ). The MN quadrupole (and h) is reflection-symmetric under z → −z, so F contains only even k_θ.
- So F_(2,−1) vanishes on the 1 : 2 tori by symmetry, not because a first-order integral exists.
- The sabotage x·y is odd in y, so its F contains only odd k_θ, and F_(3,−2) vanishes.

**Predictions, frozen now. Same tori, same N = 64 and 128, same thresholds:**
- **P1:** MN F_(4,−2) on A_12 and B_12 gives ρ > 1e−6. That is the doubled resonant harmonic, which is still resonant.
- **P2:** MN odd-k_θ coefficients F_(1,1), F_(0,1) and F_(2,1) give ρ < 1e−30 on all four tori. Parity is exact.
- **P3:** the sabotage's even-k_θ coefficients F_(0,2) and F_(1,2) give ρ < 1e−30 on all four tori.
- **P4:** the integrable controls (dM, da, null) give F_(4,−2) with ρ < 1e−15 on A_12 and B_12. Multiples must vanish
  too.

**Reading:** if P1–P4 all hold, the MIXED result is explained by parity, and the MN quadrupole is obstructed on all
four resonant tori, each via its lowest parity-allowed resonant harmonic. That gets reported as "registered MIXED;
explained and resolved by a pre-stated addendum". Any failure is reported as is.
