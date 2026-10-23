# V16 FINDINGS (sealed 2026-10-23, before reading tabula's §199b)

Setup: TS δ=2 at p = 3/5 (ts35) and Kerr (kerr35, same a/M, δ = 1 chart) at E = 0.94, prograde, ε = −0.01
(L = −l_sep·(1+ε)). Section y = 0 upward, (x, p_x) with p_x the canonical momentum. Variational tangents; Newton fixed
point via the symmetric bracket. Sealed file: results/V16_SEALED.json (sha256 below, in the commit message).

| | l_sep | h | closure (G1) | R0 | λ_u | n | z_h (apex) | θ | Ω (Lazutkin) |
|---|---|---|---|---|---|---|---|---|---|
| TS2 (rtol 1e-12, s0 1e-7) | 9.11087 | 0.016335 | 4.6e-14 | 6.2e-12 | 51.38 | 4 | x = 37.824 | 7.537e-4 | 1.790e-7 |
| TS2 (1e-13, 1e-7) | | | | | | 4 | 37.824 | 7.542e-4 | 1.791e-7 |
| TS2 (1e-12, 1e-8) | | | | | | 5 | 37.824 (p_x residual 7e-8) | 6.40e-4 | 1.52e-7 |
| TS2 (1e-13, 1e-8) | | | | | | 5 | 37.824 | 7.533e-4 | 1.789e-7 |
| Kerr (1e-12, 1e-7) | 4.42970 | 0.021444 | 7.7e-14 | 2.4e-12 | 46.60 | 4 | x = 19.499 | 2.5e-8 | −1.3e-11 |

- Gates: G1 and R0 pass everywhere. G2 (variant spread < 20%): 15% (the (1e-12, 1e-8) variant is low and has a
  homoclinic-point residual of 7e-8 in p_x, a refinement-tolerance artefact; the other three agree to 0.1%).
- **Ω (Lazutkin homoclinic invariant), TS2: ≈ 1.79e-7, about 1e4 × the Kerr value (1.3e-11)** ⇒ transversal splitting
  (invariant-certified, numerical), per the registered rule (> 10× Kerr, spread < 20%). Ω is the blind quantity.
- **θ replication: DISAGREE as registered.** V16 θ = 7.54e-4 vs tabula's 2.50e-3 at the same level (h = 1.63e-2
  matches tabula's 1.6e-2). That is a factor ~3.3. θ is coordinate-dependent (it depends on how p_x is scaled), so the
  first hypothesis to check with tabula is the momentum coordinate (the canonical p_x vs a velocity such as dx/dτ)
  and the tangent normalisation. To be investigated, never averaged.
- The lobe area was not computed (registered as "if reached").
