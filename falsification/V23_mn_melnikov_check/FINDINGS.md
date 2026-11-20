# V23 FINDINGS: the MN Melnikov second harmonic, independently recomputed. **REPRODUCED**

*2026-11-20. Pre-registration 103424e (before any code). The code is the Bridge's own: V17 g0_and_h for the metric and
the β-, M- and a-derivatives; its own homoclinic solution; its own spectral θ-motion in Mino time. Nothing from
Fable's mnlib.py.*

| | V23 | Fable (mn_melnikov) | tolerance | result |
|---|---|---|---|---|
| Level (E, L, Q, r_t, r₄, κ) at (5, 3, 16, 1/2) | 0.935281504567998718539…, 12.97253203560728069…, 56.37733827951502…, 47.50817742630806…, 0.33309351987706…, 7.86302299764606978… | the same to every printed digit | — | agree |
| **L₂, base** | **−4.774821150e−5** (N_χ 256 and 512; λ-step halved; T = 40/κ and 60/κ all identical to 10 digits) | −4.774821e−5 | 1e−4 rel | **AGREE** |
| L₀ | 7.150033063 | 7.150033 | — | agree |
| L₄ | −5.3127e−10 (so 2L₄ = −1.06e−9) | "−1.06e−09 cos 4ψ" | — | agree |
| L₂ at z_m = 0.8 (E = 0.9772515…) | −8.021137217e−4 | −8.021137e−4 | 1e−4 rel | **AGREE** |
| **C1 Kerr controls** (∂/∂M, ∂/∂a), L₂ | 5.8e−16, −2.4e−16, −5.6e−16, 9.6e−17 | ≤ 1.2e−15 | ≤ 1e−12 | **PASS** |
| **C2 sabotage** (x·y in tt): L₁ | 210.19 (its L₂ ≈ 1e−15, the parity rule) | — | > 1e−8 | **PASS** |
| Gates | H1 (dr_h/dλ)² = R to 6.8e−15; shell ≤ 2.1e−15; H4 convergence exact to 10 digits | | | PASS |

**Verdict: REPRODUCED.** The MN quadrupole's Melnikov potential along Kerr's inclined homoclinic orbit has a nonzero
second harmonic. It is 11 orders of magnitude above the Kerr-to-Kerr floor, and the result is insensitive to every
numerical parameter.
- D = L(0) − L(π/2) ≈ 4L₂ = −1.9099e−4.
- M(ψ₀) = −4Υ_θL₂ sin 2ψ₀ + … , with simple zeros at 0, π/2, π and 3π/2.

**Still open (not covered by V23):**
1. **Interval certification of L₂ ≠ 0.** Floats can't prove it, although a margin of 1e11 over the floor makes an
   error implausible. Route: an Arb or mpmath-iv quadrature with a rigorous truncation tail bound (the integrand
   decays like e^{−κλ}) and a rigorous error term for the periodic trapezoid in χ.
2. **The theorem's analytic steps** (Robinson's theorem applied to the Mino-time Hamiltonian; the reduction; the
   real-analytic-integral conclusion): for the Opus review.
3. **The explicit β₀,** the static limit a = 0, and retrograde orbits.

Environment: Python 3.14.5 (conjecture_machine .venv), numpy 2.4.6, sympy 1.14.0, mpmath 1.3.0, macOS 27.2.

## Addendum A: bracket form M = ∫{K_r, K₁} dλ, directly (review item (i))
- **Registered run: FAIL** on the Kerr control (3.0e−8 against 1e−10). Diagnosed as round-off in the finite-difference
  step hx = 1e−6; it is not physics. The MN comparisons already agreed to 1e−6 and 1e−5.
- **A2 (post-failure, diagnosed, all tolerances kept):** hx = 1e−4, Nchi = 16384. **PASS**:
  - bracket vs Υ_θL′: 2.8672369681e−3 vs 2.8672372214e−3 at π/4 (8.8e−8 rel), and 2.0275063903e−3 vs
    2.0275066876e−3 at π/8 (1.5e−7 rel);
  - M(0) = 1.8e−11;
  - Kerr ∂/∂M 5.5e−11 and ∂/∂a 1.3e−11 (≤ 1e−10).
- **Review item (i) is CLOSED:** the Melnikov function equals Υ_θ L′(ψ₀), checked by a second implementation of the
  bracket integral.
- Items (ii) (Robinson at source) and (iii) (interval certification) remain open.
