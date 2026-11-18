# V21: independent check of Fable's claimed axis theorem for Manko–Novikov (pre-registration)

*2026-11-18 ~21:30 IST, written before any V21 code exists or runs. Sumit's go: "after your check independently..."*

**Target.** `/Users/sumit/Github/fable_work/mn_general_theorem/DESIGN.md` (Fable 5.2 in the Quantum-personal session; not
registered, not reviewed). It claims Theorem 1: for every β ≠ 0, every α, E ≠ 0 and μ ≠ 0, the axis NVE has a
non-solvable Galois identity component.

**Disclosure.** I read DESIGN.md §1–§7 before writing this. Its predicted numbers (234.769; −5.04e7; trace 0 at a single
turning point) are known to me, so these checks are tests of a stated prediction, not blind measurements.

**Independence.** Everything uses the Bridge's own MN transcription (V9 `v9_nve.py`: `mn_functions`, `axial_r`), which
imports nothing from quantum or from Fable's text. It was checked against ansatz's package in October.

## Checks (in order; any FAIL stops the run and is reported)
- **C1, Lemma 3 (MN on the axis), exact and numeric.**
  - At p1 = (5, 3, 1/5) and p2 = (13, 5, −1/3), V9's f at y = 1 must equal
    `f0 = W (r² − 2Mr + a²)/(r² + a²W²)`, with W = exp(2β/x³), r = kx + M, k = √(M² − a²).
  - Symbolic simplification first. If that is inconclusive: mpmath at 40 digits at ≥ 8 points, real x ∈ (1.2, 30) and
    complex x with |x| ∈ (0.3, 1), with relative difference ≤ 1e−30.
  - Also, ω at y = 1 must be 0 to the same tolerance.
- **C2, Lemmas 1 + 2 combined.** V9's axial normal-form coefficient r(x) (z'' = r z, independent variable x, from the
  exact θ-linearisation) must equal `−(3/16)(P_x/P)²`, with P = E² − μ² f0(x).
  - Two normal forms in the same independent variable that are gauge-equivalent have identical coefficients, so
    equality is the test.
  - Run at p1 and p2 with (E, μ²) ∈ {(1, 4), (1, 9), (0.97, 1)}, at the same ≥ 8 points, at 40 digits, with relative
    difference ≤ 1e−25.
- **C3, the sharp prediction (Lemmas 4 and 6, static case).** α = 0, so f0 = W(x − 1)/(x + 1) (the a = 0 case of (3),
  once C1 confirms (3)).
  - Integrate equation (2), written in σ = 2β/x³ (equation (4): v_σσ + (4/(3σ)) v_σ + (3/16)(d ln P/dσ)² v = 0), around
    closed σ-loops near the turning-point lattice σ_j = ln(E²/μ²) + iπ(2j + 1).
  - (a) A circle around ONE σ_j (radius π/2): |trace| ≤ 1e−6 asymptotically (a reflection, trace 0). Report j = 5,
    10, 20, 40.
  - (b) A circle around TWO consecutive σ_j, σ_{j+1} (centre the midpoint, radius 1.5π): |trace| → 4 + 2cosh(π√3)
    = 234.7690…
  - **PASS for (b):** at j = 5, 10, 20, 40, 80 the deviation |tr| − 234.769 decreases monotonically (O(1/j) expected).
    Its Richardson extrapolation lies within 0.5% of 234.769, and so does the j = 80 value within 2%.
  - Two parameter rows: (β, E, μ²) = (1/5, 1, 4) and (−1/3, 1, 9). β < 0 uses its own branch of x = (2β/σ)^{1/3};
    the result must be the same.
  - Integration: scipy DOP853 complex, rtol 1e−12, with the result checked against rtol 1e−13 (traces must agree to
    1e−6 relative).
  - The sign of the trace depends on the normalisation; |tr| is the registered quantity, and the sign is reported.
- **C3c (informational, not a gate):** the commutator trace of two overlapping pairs, compared with −5.04e7.

## Verdicts
- **CONSISTENT:** C1, C2 and C3(a, b) all pass. That means the axis equation, MN's axis formula and the sharp static
  prediction of the density argument are confirmed by independent code. It does NOT prove Lemmas 4–6 in the rotating
  case, Morales–Ramis's applicability, or the class-of-integrals question; those remain for the Opus review and for
  quantum's certified C3.
- **FALSIFIED:** any check fails beyond its tolerance, reported as is, and the route goes back to the Fable session.
- **VOID:** a numerical or gate problem in V21 itself.

Resources: 1 core, nice 10, minutes.
