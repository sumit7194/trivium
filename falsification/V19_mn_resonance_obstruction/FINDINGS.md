# V19: findings. A Poincaré resonance obstruction for the MN quadrupole at first order

*2026-11-17. Pre-registration 7beb2d0, with amendment 1 (293f250: replacement tori, before any F value) and
addendum 2 (83746 launch; registered in the commit before running). Seal: results/V19_SEAL.sha256. One crashed
attempt is kept as results/v19_driver_attempt0_divzero.log: the sign gate divided by a zero norm, a bug in the gate
only, fixed before any coefficient existed.*

## The registered run: verdict MIXED (as registered)
- **Gates:**
  - The mass shell holds to ≤ 9e−41 at every grid point. One BL sign of a, (+a), passes; the other sign's resonance
    could not be tuned.
  - Resonance tuning is ≤ 6e−41.
  - N = 64 and N = 128 agree.
- **Controls:**
  - ∂M, ∂a and null: ρ ≤ 4e−41 on all four tori, so the integrable and gauge deformations show no obstruction. ✓
  - Sabotage, x·y in tt: ρ = 0.31 and 0.069 on the 1 : 2 tori, and ≈ 1e−42 on the 2 : 3 tori. The test can see an
    obstruction. ✓
- **Target, MN ∂/∂β, lowest resonant harmonic:**

| Torus | Resonance, k | ρ |
|---|---|---|
| A_12 | 1 : 2, (2, −1) | 1.2e−41 |
| B_12 | 1 : 2, (2, −1) | 5.8e−43 |
| C_23 | 2 : 3, (3, −2) | **2.11e−5** |
| D_23 | 2 : 3, (3, −2) | **6.41e−4** |

The registered rule needed every torus above 1e−6 for "OBSTRUCTED", so the registered verdict is **MIXED**.

## Addendum 2: the parity follow-up, predictions frozen before running
**Hypothesis.** The MN quadrupole is reflection-symmetric under z → −z, so F contains only even k_θ, and the (2, −1)
harmonic vanishes by symmetry. The sabotage x·y is odd, so it contains only odd k_θ.

| Prediction | Result |
|---|---|
| P2: MN odd-k_θ coefficients, (1,1), (0,1), (2,1), all tori, ρ < 1e−30 | **holds**: ≤ 5e−41 |
| P3: sabotage even-k_θ coefficients, (0,2), (1,2), all tori, ρ < 1e−30 | **holds**: ≤ 6e−41 |
| P4: integrable controls at (4, −2) on A_12 and B_12, ρ < 1e−15 | **holds**: ≤ 1.4e−40 |
| P1: MN at the doubled resonant harmonic (4, −2), ρ > 1e−6 | **A_12 holds: 2.42e−5. B_12 FAILS the threshold: ρ = 2.84e−7** |

**About B_12:** its ρ is identical at N = 64 and N = 128 and lies 33 orders of magnitude above every control's noise
floor. It is unmistakably nonzero, but below the 1e−6 line that was fixed in advance, so under the rules it doesn't
count as an obstruction. It's reported as "nonzero, below the registered threshold".

**Parity is confirmed exactly** (P2, P3). The MIXED pattern was a symmetry selection rule, not a sign of
integrability.

## Overall reading
Under the registered thresholds, the MN quadrupole deformation is resonantly obstructed on **3 of the 4** Kerr tori:
- C_23 and D_23 in the registered run;
- A_12 via the pre-registered addendum.

The fourth, B_12, shows a clearly nonzero but sub-threshold coefficient.

By Poincaré's argument, **one** obstructed resonant torus already rules out any smooth first-order integral
F₀ + βF₁ with F₀ depending on Carter's Q near that torus. That covers every valence and non-polynomial integrals too.

**Consistency:**
- V17: jet-level, valence ≤ 6, the floor;
- ansatz §153: the same;
- V10-MN: the exact MN has nothing to valence 10;
- MN is known to be chaotic.

V19 extends the first-order statement beyond any fixed valence, by a completely different (global, dynamical) method.

## Grade and limits
- **High-precision numerics** (40-digit quadrature and FFT, two grids, controls at ~1e−41). Not interval-certified.
- **The nondegeneracy assumption** (the frequency ratio varies across the family) is checked numerically by the r_a
  scan, not proved.
- **The verdict wording is registered MIXED**, with the explanation and the 3-of-4 resolution coming from a disclosed,
  pre-stated addendum after seeing the MIXED result. Not covered: second order in β, and tori far from these four.
