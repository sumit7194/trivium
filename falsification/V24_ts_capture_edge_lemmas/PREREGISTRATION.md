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
