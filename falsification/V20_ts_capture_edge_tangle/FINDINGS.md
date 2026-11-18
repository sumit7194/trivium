# V20 FINDINGS: blind replication of ansatz §154 (TS δ=2 capture-edge tangle)

*Sealed 2026-11-18, before any ansatz §154 number was read. Seal: results/V20_SEALED.json (sha256 in the commit
message). Pre-registration: PREREGISTRATION.md (90e79e4), with amendments 1 (7d8f068) and 2 (6674ad6).*

## Verdicts
| stage | verdict |
|---|---|
| Registered (s0 ∈ {1e−7, 1e−8}, after the amendment-1 bug fix) | **VOID**: gate B6 failed (homoclinic index relabelled 5 to 6; θ and Ω spread 17% against < 5%). The ratio to the Kerr floor (~100–200) was also below 1e3. |
| Amendment 2 (s0 ∈ {1e−5, 1e−6}, B6′ by the homoclinic point), registered after the VOID and before running | **TRANSVERSE (replicated)** |

The original VOID stays on record. Amendment 2 is a new verdict under a design fixed after the first one failed: it
is not a blind first attempt.

## Level and gates
- **Level:** TS δ=2, p = 4/5, E = 97/100, L = +41/8 (retrograde, σ = 1). The Kerr partners are at L = +2.55380
  (the bridge's V12) and +2.550268 (ansatz's).
- **B0** (y-reflection symmetry, exact) passes for ts45, kerr45 and ts35.
- **B1** (reversor) ≤ 1e−11.
- **B2** passes in every run: closure ≤ 2e−12, |p_x*| ≤ 6e−15, |det DP − 1| ≤ 1.1e−11, hyperbolic.
- **B3:** Kerr x* equals the analytic retrograde unstable spherical orbit (r_sph − m) to ~1e−12 at both partners.
- **B4:** the new code path reproduces the bridge's sealed V16 result (TS p = 3/5) to 0.08% in both Ω and θ.
- **TS fixed point:** the only symmetric fixed point on [2, 30], hyperbolic. It lies below the bridge's V12 inner
  transition (~9.98), consistent with ansatz's qualitative remark.

## Amendment-2 numbers (outward branch, first symmetric homoclinic point)
| | θ | Ω (Lazutkin) | homoclinic point x_h |
|---|---|---|---|
| TS, 4 variants | 1.1237e−2 … 1.1247e−2 (spread 0.09%) | −2.7677e−6 … −2.7701e−6 (spread 0.09%) | identical to 1e−10 |
| Kerr, 8 runs (floor) | max 2.11e−7 | max \|Ω\| 9.7e−11, random sign | 28.4134 / 28.4162 |
| Ratio TS / floor | 5.3e4 | 2.9e4 | needed > 1e3 |

- **Diagnosis confirmed:** the floor scales with the iterate count. Kerr θ is ~5e−5 at n = 5, ~2e−7 at n = 4, ~3e−8
  at n = 3, and 1.6e−8 at s0 = 1e−4.
- **Linearisation check (s0 = 1e−4, not a gate):** TS θ = 1.12376e−2 and Ω = −2.7682e−6 at the same x_h. This agrees.
  The branch-label heuristic mislabelled the branch at this s0, but the homoclinic point is the same.

## Claim and scope
- **Numerical, not rigorous:** at this (E, L), the unstable spherical-type orbit of TS δ=2 has a transverse symmetric
  homoclinic point, so by Smale–Birkhoff there is a horseshoe and hence a chaotic saddle at this level.
- Independent code from ansatz: float64 DOP853 with variational equations against DD GBS with finite differences, and
  a different fixed-point method.
- One level only. The link to the §150 window is not checked. Not interval-certified.

## Process record
- One bug (the amendment-1 linear-zone filter) was found and fixed before any TS splitting value existed.
- The registered run was VOID, and was not rescued.
- The verdict word TRANSVERSE was known in advance, so the verdict itself is not blind. The numbers are blind (no
  ansatz value has been read).
- Blind comparison with ansatz: pending. Tolerances are as registered (x* 1e−7, λ_u 1e−5, n exact, x_h 1e−6, θ 2%).
  The index n is reported per s0, since amendment 2 showed that n depends on where the fundamental segment sits.

Environment: Python 3.14.5 (/Users/sumit/Github/conjecture_machine/.venv), numpy 2.4.6, scipy 1.18.0, sympy 1.14.0,
numba 0.65.1, Accelerate BLAS, macOS 27.2.

## Blind comparison with ansatz §154 (recorded after the V20 seal 8b7eb6f; ansatz values received by message, its embargo lift 43cde03)
Ansatz: R2 (DD, tol 1e−28), δ = 1e−12. V20: float64, the four amendment-2 variants.

| quantity | ansatz | V20 (worst variant) | relative difference | tolerance | result |
|---|---|---|---|---|---|
| x* | 9.804559168202628 | 9.8045591682 | ≤ 8.5e−15 | 1e−7 | **AGREE** |
| λ_u | 38.387723771736 | 38.38772377 | ≤ 6.9e−13 | 1e−5 | **AGREE** |
| x_h | 56.861080125941 | 56.8610801259 | ≤ 4.2e−13 | 1e−6 | **AGREE** |
| θ | 0.011237603095 | 1.1237e−2 … 1.1247e−2 | 1.9e−5 … 8.1e−4 | 2% | **AGREE** |
| n | 8 (δ 1e−12), 7 (δ 1e−11) | 4 (s0 1e−5, 1e−6) | not comparable as registered | exact | **n/a** (see below) |

- **The index n:** as amendment 2 found, n depends on where the seed segment sits, and ansatz's δ differs from V20's
  s0, so "n exact" can't be applied literally. This is recorded as not applicable, not as a pass. The seed-independent
  quantity is s_h·λⁿ, the distance along the unit unstable eigenvector that maps onto the homoclinic point. It is
  38.25054 in V20 (all four variants) and 38.25058 for ansatz at both δ, a 1e−6 relative agreement.
- Ansatz's p_x is the canonical momentum in the ts2:4/5 chart, with σ = 1 and m = 2/p. That is the same exact chart as
  the bridge's ts45 (the V10 loader of the same sealed component files).
- Kerr floor: ansatz 9.7e−14 (DD) against V20's 2e−7 (float64). Both are ≥ 4 orders below the TS θ.
- **Reading:** two independent codes (DD GBS with finite differences, against float64 DOP853 with variational
  equations) agree on every comparable quantity, θ included, to ≤ 0.08%. The comparison is one-way blind: V20 was
  sealed before ansatz's numbers were read. The result is a transverse symmetric homoclinic point at this level,
  numerical and not rigorous, with the scope as stated above.
