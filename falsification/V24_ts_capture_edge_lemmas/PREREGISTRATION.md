# V24: independent check of Fable's capture-edge lemmas (fable_work/ts_capture_edge/L3_ANALYTIC.md), pre-registration

*2026-11-20 ~14:30 IST, written before any V24 code. Sumit: review the three Fable results one at a time.*

**Target.** Fable 5.2's claims (unreviewed):
- (R) the reduced L = 0-sector geodesic problem at TS δ=2, p = 4/5, E = 97/100, L = 41/8 is a particle in a flat (u, v)
  plane with potential V = ½F(W + 1), where x = cosh u, y = cos v and F = g_xx(x² − 1);
- (I1) on Hill's region {V ≤ 0} with 1.5 ≤ x ≤ 9.49: ∂V/∂x > 0;
- (I2) on {V ≤ 0} with 9.3 ≤ x ≤ 77.1: ∂V/∂(y²) > 0.

Fable says both inequalities were CHECKED by interval arithmetic, with no undecided boxes.

**Disclosure.** I read L3_ANALYTIC.md §0–§6, but none of Fable's check scripts or outputs.

**Independence.** The Bridge's own TS2 metric (V11 loader, ts45), sympy and mpmath interval arithmetic (mp.iv). Nothing
from Fable's checks/.

## Checks
- **R1 (exact).** With F := g_xx(x² − 1), verify symbolically:
  - g_xx(x² − 1) = g_yy(1 − y²) (the conformal-flat condition);
  - H = ½[g^xx p_x² + g^yy p_y² + W] equals F⁻¹·[½(p_u² + p_v²) + ½F(W + 1)] − ½, with p_u = p_x √(x² − 1) and
    p_v = −p_y √(1 − y²).

  sympy must cancel the difference to 0.
- **I1 (interval).** Write s = y². On the box [1.5, 9.49] × [0, 1] in (x, s), recursively bisect. A box is DECIDED if
  either the enclosure of W + 1 is > 0 (outside Hill's region), or the enclosure of ∂V/∂x is > 0. Depth limit 24.
  - **PASS:** 0 undecided boxes.
  - Report the box count and the minimum lower bound of ∂V/∂x on decided Hill boxes.
- **I2 (interval).** The same on [9.3, 77.1] × [0, 1], with ∂V/∂s.
- **Negative controls** (they must FAIL, i.e. leave undecided or violating boxes, to show the checker can see a
  failure):
  - I1 extended to x ≤ 9.6 (Fable says it fails beyond 9.4995);
  - I2 with the sign requirement reversed (∂V/∂s < 0).
  - **Measured BEFORE fixing anything:** I run the I1-extended control first and record its count. That's allowed by
    the control-floor rule, and it is not the target.

## Verdicts
- **CONFIRMED:** R1 exact, I1 and I2 with 0 undecided, and both negative controls show failures.
- **FALSIFIED:** an inequality has a box where the enclosure proves the wrong sign.
- **INCONCLUSIVE:** undecided boxes remain at the depth limit with no proven violation.
- **VOID:** a negative control shows no failure (the checker can't see failures).

**Not covered:** I3 (needs a validated γ), Lemmas G, Q, E, L3′, the hole lemma, and the lobe conditions T, C1 and C2.
Those come next, separately.

Resources: 1 core, nice 10, a footprint watcher at 1.5 GB.

## Registered results and Amendment A1 (POST-RESULT, implementation only)
- **R1: PASS (exact).** The conformal condition and the Hamiltonian identity both cancel to 0.
- **I1: PASS.** 2067 boxes, 0 undecided, 0 violations, 1.0 s.
- **NEG-I1 (extended to 9.6): FIRES.** 1230 boxes with a proven wrong sign near x ≈ 9.599, consistent with Fable's ridge at
  9.4995.
- **NEG-I2 (reversed): FIRES** (39742 proven violations).
- **I2: INCONCLUSIVE** as registered: 11165 undecided and 0 violations. Every undecided box sits at s ∈ [0.99988, 1],
  i.e. against the AXIS (y² → 1).
  - **Diagnosis:** the denominators of V and ∂V/∂s carry factors (s − 1) and (s − 1)². On a box touching s = 1 those
    straddle 0 in interval arithmetic, so the sign test can never decide, whatever the depth.
  - This is an implementation limitation of V24, not a property of V.
- **A1 (implementation only; no tolerance, domain or rule changes):** before the interval sign test, divide every
  denominator by its known factors (s − 1)^k, (x² − s)^k and (x − 1)^k(x + 1)^k, and multiply the sign by the exact,
  known sign of each removed factor on the domain (x > 1 ≥ s): (s − 1)^k has sign (−1)^k, and the others are positive.
  - Rerun I1, I2 and both negative controls. The registered I2 INCONCLUSIVE stays on record.
