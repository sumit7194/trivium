# V27 findings

## A (2026-11-21, early morning): Neon T16 exact claims. **Registered verdict FAIL, from a Bridge control-design slip; every Neon claim PASSES exactly**
Code: code/v27_A.py. Outputs: results/v27_A.txt; results/v27_A_postdiag.txt (labelled post-result).

**A1 PASS.**
- Curzon f0 = e^{−2M/z} with w = −2M/z gives eʷ exactly.
- With x = eʷ the NVE becomes v_xx + v_x/x + (3/16)(x − ã)⁻²v = 0.
- Exponents: {1/4, 3/4} at ã and ±i√3/4 at ∞.

**A2 PASS (the claims).**
- The parameterisation is valid: trace 0, det 1, tr(M0M_ã) = τ.
- tr h1 = −2 − τ², tr h2 = −2 − 4τ², and tr[h1, h2] − 2 = −4τ⁶, all identically in u.
- So Neon's analytic proof that Curzon–Chazy has a Zariski-dense axis NVE group (SL2) at every E is confirmed at
  the level of the group computation.

**A2 registered control: FAIL, the Bridge's design error.**
- The control was "diagonal M0 must give tr[h1, h2] = 2". That is wrong: a diagonal M0 together with a general
  trace-0 M_ã is not in D∞. The computed residual is ∝ u²(λ² − 1)⁶(…).
- The correct control also needs M_ã antidiagonal (u = 0). Post-result, labelled: then tr[h1, h2] − 2 = 0, as
  required.
- This is the Bridge's third control-clause slip tonight (V26-E1 labelling, V26-G2 tolerance, V27-A2 control).
- **Mechanism adopted, following Cuspis:** from now on every Bridge prereg must-fail is run once as a pre-check
  before registration, with a recorded control table.

**A3 PASS.**
- Neon's single-energy D∞ example (f0 = 1 − e^{z/√3}cot(z/2), Y = sin z) and reducible example
  (P = sin(√3 z)/cosh z) satisfy their identities to ≤ 1.2e−30.
- The control (√3 replaced by 1.7) leaves a residual of 0.0275, so it fires.
- So single-energy growth arguments cannot settle Class A, as Neon says.

**Not machine-checked:**
- the Rescaling Persistence theorem (Theorem 3), and its use of isotopy and analyticity in a outside S(f0);
- the corollaries.

**Literature:** whether the axis-geodesic proof for Curzon–Chazy is new relative to Georgiev 2019 (an equatorial
equilibrium plus a period-function argument) is still to check.
