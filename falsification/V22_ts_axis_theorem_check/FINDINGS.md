# V22 FINDINGS: independent check of Fable's TS δ=2 axis theorem (THEOREM_TS.md)

*2026-11-20. Pre-registration 536313a. The code is the Bridge's own (the V10/V11 TS2 loader, kerr_ts_chart), with
nothing from quantum or Fable.*

## Results
| check | result |
|---|---|
| **T1** axial NVE ≡ −(3/16)(P_x/P)² (exact, sympy) | **PASS** for ts45, ts35 and kerr45: the difference cancels to 0 identically, for symbolic E and μ² |
| **T2** configuration (exact roots with multiplicity) | **PASS**. T-a and T-b: 8 simple. T-c: 7 finite simple plus 1 at infinity. T-d (λ = 8/3): 2 double zeros plus 4 simple poles. λ = √2: 8 simple |
| **T4f(a)** single simple points | **PASS**: \|tr\| ≤ 1.3e−9 at every simple point (TS T-a and T-d; Kerr; ZV) |
| **T4f(b)** T-d double zeros | **PASS**: tr = −85.0314572039 at both, matching −2cosh(π√2) = −85.03145720… to ~1e−11 |
| **T4f(c)** non-commuting loxodromic pair | **PASS**: TS T-a 378 pairs, TS T-d 66 pairs, with \|tr[G,H] − 2\| up to 1e18 |
| **Control: Kerr** (4 simple) | **PASS**: singles ≈ 0; 0 non-commuting loxodromic pairs; max \|tr[G,H] − 2\| = 5.2e−7 ≤ 1e−6 (all commute) |
| **Control: ZV δ=2** (2 simple plus a double pole) | Double pole trace −85.0314572038 ✓; singles ≈ 0 ✓; **0** non-commuting loxodromic pairs ✓. **BUT** the literal registered clause "no non-commuting pair" FAILS (max \|tr[G,H] − 2\| = 7.2e3) |

## Registered verdict: **VOID**, on my own mis-specified ZV control clause
- ZV's axis group is of dihedral type (Kimura's dihedral row): a solvable group that still contains non-commuting
  elements (diagonal against antidiagonal).
- So "no non-commuting pair" was the wrong control. The right one, matching the L6 criterion used for TS, is "no
  non-commuting pair of LOXODROMIC elements", and that passes (0 pairs).
- By the registered rule ("VOID: a control fails"), the outcome is VOID. This is the same kind of self-inflicted
  mis-specification as V21's.

## Reading (informal)
- Independent code confirms Fable's TS axis equation exactly (T1).
- It confirms the configuration at every registered energy, including the special double-zero energy and the point
  at infinity (T2).
- It finds a numerically non-abelian (loxodromic, non-commuting) monodromy at both a generic and the special energy.
- It shows the expected solvable-type behaviour for Kerr (everything commutes) and for ZV (no loxodromic
  non-commuting pair).
- **Consistent with Theorem TS. Not checked:** the Kovacic case analysis as a proof, and certification. Those go to
  quantum's certified tools and a fresh review.

## Process record (honest)
- **The first T4f run stalled for 12 h.** Root cause: sympy nroots splits a numerical DOUBLE root into two points
  ~1e−8 apart, and the dedupe threshold (1e−9) missed it. That made a microscopic loop between them. Fixed (1e−5).
- **An earlier run leaked to 13 GB** (solve_ivp step history). It stopped ansatz's run; see fleet/INCIDENTS.md. Fixed
  with t_eval=[t1].
- **The ZV run failed in nroots** (a double pole). Rerun with exact sympy roots (v22_zv.py).
- None of these changed a tolerance or a test after seeing results.

Environment: Python 3.14.5 (conjecture_machine .venv), numpy 2.4.6, scipy 1.18.0, sympy 1.14.0, macOS 27.2.
