# V22: independent check of Fable's TS δ=2 axis theorem (THEOREM_TS.md), pre-registration

*2026-11-19 ~08:10 IST, written before any V22 code. Sumit's go: "yes to all 3".*

**Target.** `/Users/sumit/Github/fable_work/axis_integrability_classification/THEOREM_TS.md` (Fable 5.2,
Quantum-personal, 2026-11-19 ~01:15; HAND, unreviewed). It claims that TS δ=2 has no additional first integral that
is meromorphic near the complexified axis orbit (L = 0), at every E ≠ 0 and μ ≠ 0. Mechanism: the axis NVE has 8
simple singular points generically (4 simple + 2 double at E²/μ² = 1 + 1/|q|), and that fails every Kovacic case.

**Disclosure.** I have read THEOREM_TS.md §0–§5, including its float expectations: single traces < 1e−9, −85.031457 at
the double zeros, and a non-commuting loxodromic pair at T-a.

**Independence.** I use the Bridge's own TS2 transcription (the V10/V11 loader of ansatz's sealed component files)
and the Bridge's own Kerr-in-TS-chart, with my own axial-NVE derivation. Nothing comes from quantum or from Fable's
check scripts.

## Checks (any FAIL stops the run and is reported)
- **T1, Lemmas 1–2 for TS (exact).** The θ-linearised axial normal form r(x) of the reduced L = 0 Hamiltonian
  H = ½(g^xx p_x² + g^θθ p_θ² + g^tt E²), y = cos θ, must equal −(3/16)(P_x/P)², with P = E² − μ² f0 and
  f0 = −g_TT(x, 1).
  - The identity is checked with sympy (cancel to 0) at ts45 and ts35 for symbolic E, with μ² = 1.
  - If sympy cannot finish within 10 min: mpmath at 40 digits at 8 points, real and complex, rows T-a..T-d, with
    relative difference ≤ 1e−25.
- **T2, configuration (exact).** At p = 4/5 rows T-a (λ = 8/15), T-b (2), T-c (1) and T-d (8/3), count the zeros and
  poles of P with multiplicities (sympy factor or roots), including the point at infinity.
  - Expected: 8 simple (T-a, T-b, T-c with one at infinity), and 4 simple + 2 double (T-d).
  - Also a generic irrational check: λ = √2 gives 8 simple.
- **T4f, monodromy (float, NOT certified).** Integrate the normal form y'' = r y with scipy DOP853 complex at rtol
  1e−12 (checked against 1e−13), around circles in the x-plane.
  - (a) Around each simple point: |tr| ≤ 1e−8.
  - (b) T-d, around each double zero: tr = −2cosh(π√2) = −85.0314572… to ≤ 1e−7 relative.
  - (c) Non-commutation at T-a: from a common base point, take loops around two adjacent pairs of simple points,
    giving G and H. Both must be loxodromic (|tr| > 2 + 1e−6), with |tr[G,H] − 2| > 1e−3.
- **Controls, same code.**
  - Kerr (kerr45, same E and μ²), 4 simple points: |tr| ≤ 1e−8 around each. For every pair of pair-loops G and H,
    |tr[G,H] − 2| ≤ 1e−6, i.e. they commute: the virtually abelian case. It must NOT show non-commutation.
  - ZV δ=2 axis (q = 0): f0 rational of low degree, configuration per NOTES (1 heavy double pole); no non-commuting
    pair.

## Verdicts
- **CONSISTENT:** T1, T2, T4f(a,b,c) and both controls pass. That would mean the axis equation, the configuration and
  a numerical non-abelian monodromy are independently confirmed. NOT covered: the Kovacic case analysis as a proof,
  every special energy, and certification (Quantum's tools); those go to the review and a certified run.
- **FALSIFIED:** any test fails beyond its tolerance while its controls pass.
- **VOID:** a control fails, or a numerical problem in V22 itself. **No monotonicity clauses (lesson of V21).**

Resources: 1 core, nice 10, minutes.
