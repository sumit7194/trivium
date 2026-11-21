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

---
## Addendum B (2026-11-21 ~11:30): Neon T21 Theorem 1 on its lacunary example
**VERDICT V27-B: FAIL as registered**, on B1 only, from a defect in the Bridge's harness. B2-B5 PASS.
Environment: CPython 3.14.5 (conjecture_machine/.venv), numpy/scipy as in ENVIRONMENT/bridge_env.json, DOP853 rtol 1e-12.

| Clause | Result | Registered |
|---|---|---|
| B1 counts and simplicity | winding 3.000000; Newton returned NaN | **FAIL** (harness) |
| B2 eta | max\|eta\| = 0.060467 (2^14 grid identical) < 1/15; Neon 0.06045 | PASS |
| B3 trace | tr = -1869.186881 (Neon -1869.187); \|tr\| > 27 | PASS |
| B4 det | \|det - 1\| = 3.2e-9 | PASS |
| B5 D-infinity step | winding(v+ v-) = 1.00000, so the winding of Y is 2, as the proof states | PASS |

**Cause of the B1 fail.** The harness computed f0' as f0 * sum 1/(z - c_k). The registered Newton start points
2, 16 and 512 are exact zeros of f0, so the formula gives 0 * inf = NaN. No pre-run control exercised that code path.

**Labelled post-run diagnostic B1′ (not the verdict).** It uses a division-free derivative
(code/v27_B_postdiag.py, results/v27_B_postdiag.txt). It finds three distinct, simple a-points inside the circle:
0.5487, 17.497 and 511.954, with |f0'| = 0.53, 0.51 and 15.3. Together with the registered winding of 3, this
accounts for the count.

**Reading.** On Neon's own example, every quantity Theorem 1's proof uses checks out:
- the hypotheses (m = 3, N + P = 3, eta < 1/15);
- the multiplier, about 1869, far above the proof's floor of 28;
- the exact winding 2 in the D-infinity step.
Together with the Bridge's hand re-derivation of the proof steps (neon_work/onlykerr/T21_summary.md), Theorem 1
looks right. It still needs a second reader before it is cited. Theorem 2 (all slow-growth entire functions) is
only a sketch from Neon and has NOT been checked here.
