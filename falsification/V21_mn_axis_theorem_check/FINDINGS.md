# V21 FINDINGS: independent check of Fable's MN axis theorem (DESIGN.md, Quantum-personal)

*2026-11-18. Pre-registration: PREREGISTRATION.md (2f7cfdc) and amendment 1 (f16d352, before any C3 number). The
code is the Bridge's own (the V9 MN transcription), with nothing from quantum or Fable.*

## Results
| Check | What | Result |
|---|---|---|
| C1 | V9's MN f at y = 1 vs Fable's Lemma 3, f0 = W(r² − 2Mr + a²)/(r² + a²W²); and ω(y = 1) = 0 | **PASS**: max relative difference 4.4e−40 and \|ω\| ≤ 3.7e−40 at p1 and p2, over 9 points, real and complex |
| C2 | V9's exact θ-linearised axial normal form r(x) vs −(3/16)(P_x/P)² (Lemmas 1 + 2) | **PASS**: ≤ 5.7e−35 relative on all 6 (p, E, μ²) rows. The general axis NVE holds exactly for MN |
| C3a′ | Static MN, one turning point of the σ-lattice: trace | 7e−13 … 2.5e−9 (zero to the integrator floor) at every j. **PASS** on the substantive ≤ 2e−2 |
| C3b′ | Two consecutive turning points: \|tr\| → 4 + 2cosh(π√3) = 234.768921740 | Deviation −1.66e−1, −1.94e−3, −1.97e−5, −1.97e−7 at j = 10, 10², 10³, 10⁴: ~1/j², much faster than the O(x) I registered. It reaches the rtol floor (~1e−8) at j ≥ 10⁵. Quadratic fit T∞ = 234.7689195 (−9e−9 relative) for β = 1/5, (E, μ²) = (1, 4), and the same for β = −1/3, (1, 9). Determinant 1; rtol 1e−12 vs 1e−13 agree to ≤ 8e−8. Sign of the trace: negative (v-normalisation), matching Fable's tr h = −(c² + 2) |
| C3c | Commutator trace of two overlapping pairs (informational) | not computed |

## Registered verdict: **VOID**, on V21's own clause
Amendment 1's clause C3b′(i) ("deviation decreases monotonically in |x| over the last four j") and C3a′'s "decreasing
in x" both fail literally, and both fail only because the values sit at the integrator floor (j ≥ 10⁵ for C3b; every j
for C3a). This is a mis-specification in V21 (a clause that a precision floor can break). It is not a property of the
claim, and by the registered definition that makes the outcome VOID. Clauses (ii) and (iii), and every substantive
number, pass by 6–8 orders of magnitude beyond their tolerances.

## Reading (informal; not a re-graded verdict)
- Fable's axis equation and MN axis formula are confirmed exactly by independent code (C1, C2).
- The sharp static prediction of the density argument, 234.768921740, is reproduced to 1e−8 at two parameter rows,
  for both signs of β and two energies, with single turning points giving trace 0.
- This supports Lemmas 1–3 and the static-case convergence (Lemma 6), together with the explicit pair of Lemma 4(e).
- It does NOT check:
  - the rotating-case model (six singular points);
  - Lemmas 4(a)–(d) and 5 in general;
  - Morales–Ramis's applicability at the accumulating singularity;
  - the class-of-integrals question.
  Those remain for the Opus review and quantum's certified C3.

Environment: Python 3.14.5 (conjecture_machine .venv), numpy 2.4.6, scipy 1.18.0, sympy 1.14.0, mpmath 1.3.0, macOS 27.2.
