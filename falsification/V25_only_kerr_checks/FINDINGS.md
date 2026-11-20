# V25 FINDINGS, part 1 (Fable's check P1): near-axis series. **CONFIRMED**

*2026-11-20. Pre-registration 1ac330d. One implementation fix before any result existed: the first run crashed in the
Vandermonde solve (an ill-conditioned matrix), so the fit was rescaled by t/1e−4. No result was seen before the fix.*

The Bridge's own TS2/Kerr/ZV metrics, its own static-Weyl ρ⁴ series (sympy), and mpmath at 50 digits; z ∈ {2.5, 4, 7}.

| | TS δ=2 (twisting) | Kerr (twisting) | ZV δ=2 (static) |
|---|---|---|---|
| Gate (12- vs 16-point fit) | ≤ 1.4e−24 | ≤ 1e−24 | ≤ 1.4e−24 |
| F1₂, F2₂ vs the twist-free formulas (relative) | ≤ 1.7e−29 | ≤ 1e−29 | ≤ 1.7e−29 |
| (F1₄ − F1₄^static) / (−(c0″)²/(64f0)) | **1.0000000000** (all 3 z) | **1.0** | — (difference ≤ 1.3e−26; twist 0) |
| (F2₄ − F2₄^static) / (−(c0″)²/(64f0³)) | **1.0** | **1.0** | — (≤ 2.6e−24) |
| Must-fail (1.1·c0″) | 0.8264 = 1/1.21: fires | | |

- The static ρ² formulas also match the claimed ones symbolically (difference 0).
- **Verdict: CONFIRMED.** The twist enters the near-axis Hamiltonian at ρ⁴ only, and exactly as −(c0″)²/(64f0)
  (F1) and −(c0″)²/(64f0³) (F2). That now holds on a twisting non-Kerr exact solution (TS δ=2) as well as on Kerr, with
  a static-Weyl ρ⁴ part derived independently.

**Still open (P2–P6 and the rest):**
- the third-order return maps on full metrics (P2: Kerr zero, static twin (−π/2, π));
- the residue sweep (P3); Lemma P and the invisible family (P4); the two-rod example (P5); ZV and Schwarzschild (P6);
- the Galois step;
- the inherited first-order classification.
