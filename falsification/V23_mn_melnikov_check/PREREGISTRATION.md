# V23: independent recomputation of the MN Melnikov potential (Fable's mn_melnikov), pre-registration

*2026-11-20 ~12:45 IST, written before any V23 code. Sumit: "take them one at a time … don't rush".*

**Target.** `/Users/sumit/Github/fable_work/mn_melnikov/` (Fable 5.2 subagent, 2026-11-20; unreviewed). It claims that
for MN's quadrupole along Kerr's inclined homoclinic orbit, the Melnikov potential L(ψ₀) has a nonzero second
harmonic, so its zeros are simple: transverse homoclinic orbits and a horseshoe for small β ≠ 0, and no real-analytic
integral.

**Disclosure.** I read SETUP.md and MELNIKOV.md, including the claimed values:
- base point (M, a, r_u, z_m) = (5, 3, 16, 1/2): L₂ = −4.774821e−5 and D = L(0) − L(π/2) = −1.909928e−4;
- the Kerr controls give ≤ 1e−15;
- table rows at other (r_u, z_m), including (5, 3, 3.2M = 16, 0.8): L₂ = −8.021137e−4.

So this is a check of stated numbers, not a blind measurement.

**Independence.** Everything below is the Bridge's own code:
- the metric and its β-derivative come from V17's `g0_and_h` (with the 'M' and 'a' kinds for the controls);
- the shell momenta come from V19 (`quad_form`, F = Σ·H₁, as in V19);
- the homoclinic orbit and the θ-motion are the Bridge's own constructions (below), not Fable's `mnlib.py` or its
  Jacobi-cd formula.

## Method (Fourier form, as the claim's MELNIKOV §2 states it, but independently implemented)
1. **Level.** Solve R(r_u) = R′(r_u) = 0 and Z(z_m) = 0 for (E, L, Q) with mpmath (BL, μ = 1, +a), with R''(r_u) > 0
   (unstable). r_t and r₄ come from R/(r − r_u)², and κ = √(R''(r_u)/2).
   - Homoclinic: r_h(λ) = r_u + 2AB/((B − A) + (A + B) cosh κλ), with A = r_t − r_u and B = r_u − r₄.
   - **Gate H1:** (dr_h/dλ)² = R(r_h) to ≤ 1e−10 relative at 20 values of λ.
2. **θ in Mino time.**
   - z = z_m cos χ, with dλ/dχ = 1/√(a²(1−E²)(z₊² − z_m² cos²χ)) and z₊² = Q/(a²(1−E²)z_m²).
   - Υ_θ = π/λ(π), and ψ(χ) = Υ_θ λ(χ), computed by trapezoid-cumulative integration on N_χ points, checked spectrally
     at 2N_χ.
   - **Gate H2:** Z(z) ≥ 0 and the shell holds.
3. **v₂(r)** = (1/2π)∫₀^{2π} F(r, z(χ)) e^{−2iψ(χ)} (dψ/dχ) dχ, with F(r, z) = Σ·½G₁^{ab}p_a p_b. Here p_t = −E,
   p_φ = L, p_x² = k²R/Δ² and p_y² = Z/(1 − z²)²; G₁ = −G₀hG₀ (the V19 construction).
   - **Gate H3:** the mass shell |H₀ + ½| ≤ 1e−12 at every point used.
4. **L₂** = ∫_{−T}^{T} [v₂(r_h(λ)) − v₂(r_u)] cos(2Υ_θλ) dλ, by the trapezoid rule, with T = 40/κ.
   - **Gate H4:** halving the λ-step and doubling N_χ change L₂ by ≤ 1e−6 relative; T → 1.5T changes it by ≤ 1e−8
     absolute.
   - Also computed: L₀ (n = 0) and D ≈ 4(L₂ + L₆ + …), with L₄ and L₆ computed to check that they're small.

## Controls (same code)
- **C1, Kerr-to-Kerr:** h = ∂g/∂M and h = ∂g/∂a give |L₂| ≤ 1e−12 (float64 floor with margin), at the base point.
- **C2, positive:** a deliberately non-Kerr toy, h = V17's sabotage (an x·y entry in tt only), must give |L₂| ≫ 1e−12.
  Its parity is odd in y, so use n = 1 for it: the test is |L₁| > 1e−8.

## Verdicts
- **REPRODUCED:** H1–H4 and C1–C2 pass, and V23's L₂ at the base point agrees with Fable's −4.774821e−5 to ≤ 1e−4
  relative (and is nonzero by > 1e6 × the C1 floor). Also the (z_m = 0.8) row −8.021137e−4, to ≤ 1e−4.
- **DISAGREE:** any gate and control pass, but an L₂ differs beyond 1e−4. Investigate; never average.
- **VOID:** a gate or control fails. **No monotonicity clauses; controls checked against what they can produce**
  (lesson of V21/V22): Kerr deformations give exactly 0 in theory (W^u = W^s), and the sabotage has no symmetry
  forcing its n = 1 harmonic to vanish.

**Not covered:** certification (interval bounds on L₂ ≠ 0, which is the next step: quantum's Arb, or the Bridge's
mpmath iv), the theorem's analytic steps (to the Opus review), the explicit β₀, and the static limit.

Resources: 1 core, nice 10, a footprint watcher at 1.5 GB, minutes.

## Addendum A (2026-11-20, after V23 REPRODUCED; before any bracket-form code): close review item (i)
- **Check B:** compute M(ψ₀) = ∫{K_r, K₁} dλ DIRECTLY along the homoclinic orbit, at the base point, for the MN
  perturbation.
  - The bracket is taken in (x, p_x), with p_x = k Δ⁻¹ dr_h/dλ (signed), using the full phase-space K₁ = Σ·½G₁^{ab}p_a p_b.
  - ∂_x K₁ is by central differences at fixed momenta; p_y² = Z/(1 − z²)²; z(ψ₀ + Υ_θλ) comes from the V23 θ-table,
    inverted.
- **Compare** with Υ_θ L′(ψ₀) from V23's harmonics: L′ = −4L₂ sin 2ψ₀ − 8L₄ sin 4ψ₀.
- **PASS:** relative agreement ≤ 1e−4 at ψ₀ = π/4 and π/8, and |M(0)| ≤ 1e−3 × |M(π/4)| (the parity zero). The Kerr
  control ∂/∂M must give |M(π/4)| ≤ 1e−10.

### Addendum A, registered result: FAIL on the Kerr-control clause. Amendment A2 (POST-FAILURE, diagnosed)
- **Registered run** (Nchi 4096, finite-difference step hx = 1e−6):
  - MN bracket vs Υ_θL′: 2.867240e−3 vs 2.867237e−3 at π/4 (1.0e−6 rel), and 2.027487e−3 vs 2.027507e−3 at π/8
    (9.6e−6 rel). Both PASS.
  - M(0) = −1.7e−9. PASS.
  - **Kerr ∂/∂M control: 3.0e−8 > 1e−10. FAIL.** So addendum A as registered is a FAIL on its control clause.
- **Diagnosis** (a scan, results seen):
  - The control does not move with the θ-table resolution: 3.02e−8, 2.99e−8 and 3.06e−8 at Nchi 4096, 16384 and 65536.
  - It falls with the finite-difference step: −1.3e−9 at hx = 1e−5, and 5.5e−11 at hx = 1e−4.
  - So it is ROUND-OFF in the central difference ∂_x K₁ at hx = 1e−6 (K₁ is O(1–10) for h = ∂g/∂M). It is not physics
    and not interpolation.
  - The tolerance 1e−10 was set without checking this method's floor. That is another control-clause mis-specification
    of mine (see the memory note "control-clause checks").
- **A2:** rerun with hx = 1e−4 and Nchi 16384, keeping every tolerance. PASS requires the same clauses as addendum A. The
  registered FAIL stays on record.
