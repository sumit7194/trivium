# V16: independent replication of the TS δ=2 separatrix splitting (tabula §199), and the Lazutkin invariant
Registered 2026-10-23, before any V16 computation.

## Disclosure
- tabula's §199 values were already received by message: p = 3/5, ε = −0.01, θ = 2.50e-3 ± 3.4e-5 (and the other
  levels). So the θ replication is NOT blind.
- The Lazutkin homoclinic invariant (and, if reached, the lobe area) IS blind: tabula's §199b numbers will not be read
  before V16's are sealed (committed with sha256 sent).
- Definitions taken from tabula's prereg: TS δ=2 at p = 3/5 (q = 4/5), timelike (H = −1/2), E = 0.94, prograde,
  L = −l_sep·(1+ε) with ε = −0.01, where l_sep is the |L| at which the equatorial saddle of the effective potential
  lies exactly on the shell. Section Σ = {y = 0, p_y > 0}, coordinates (x, p_x).

## Independent implementation
- Field: the bridge's own TS2 transcription (V10/V8 loader, the ts35 = t1o2 component files), via V11's compact build
  (exact symbolic Jacobian, numba).
- Kerr control: the same mass and spin in the TS chart (V11 kerr_ts, p = 3/5, q = 4/5), at the same ε relative to
  ITS OWN l_sep.
- Tangents from the VARIATIONAL equations (exact Jacobian), not finite differences. That is a different method from
  §199.
- Fixed point by Newton on P(z) = z with DP from the variational solution. Manifold tracking by iterating a
  fundamental segment of W^u (pocket branch). The primary symmetric homoclinic point is the first p_x = 0 crossing
  at x > x*, refined by bisection in the segment parameter.

## Gates (all must pass, else the result is void)
- R0: the reversor S(x, p_x) = (x, −p_x) satisfies S∘P∘S∘P = id to ≤ 1e-9 at 5 test points.
- G1: Lyapunov fixed point closure |P(z*) − z*| ≤ 1e-10.
- G2: variant stability: rtol 1e-12 vs 1e-13, and fundamental-segment start s0 ∈ {1e-7, 1e-8}. Spread of θ < 20%.

## Measures and verdicts
- θ = the angle between t_u and S·t_u in (x, p_x) at the primary homoclinic point (coordinate-dependent; for
  comparison with §199).
- Ω = Lazutkin's homoclinic invariant: ω(t_u, t_s) with the tangents transported from the fixed-point eigenvectors,
  normalised by ω(e_u, e_s) = 1 and e_s ∝ S·e_u, where ω = dx ∧ dp_x on Σ. In closed form,
  Ω = (t_ux·t_up)/(e_ux·e_up), with t_u = λ⁻ⁿ·DPⁿ·e_u transported. Kerr must give |Ω| at the numerical floor.
- **Replication verdict for θ (TS2):** REPLICATED if |θ_V16 − 2.50e-3| ≤ 3σ_combined + 10%; else DISAGREE, reported
  and investigated, never averaged.
- **Ω:** reported with its variant spread and the Kerr value. "Transversal (invariant-certified, numerical)" if
  |Ω_TS| > 10 × |Ω_Kerr| and the spread < 20%.
