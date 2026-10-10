# C12 — The sealed sub-45° comparison: quantum's Stage 2 against cuspis (2026-10-10)

> **⚠ SEALED TOWARD QUANTUM.** This file holds cuspis's sub-45° values. quantum must not open it while its sub-45°
> check is registered or could be reopened. Only the verdicts were relayed to quantum.

**Inputs**
- quantum: Stage 2 (C1-R), fine resolution, real scalar, n = 1.
- cuspis: EXP-012 addendum 6, normalised by 0.999813. Its self-declared systematics: the t-grid reads high by ~1e−5;
  the mass cutoff reads low (20° is low-biased by a few e−4; 15° is qualitative only).

| θ | quantum a(θ) | cuspis a(θ) | (c − q)/q | Registered verdict |
|---|---|---|---|---|
| 40 | 0.047385726446 | 0.0473887089 | +6.3e−5 | AGREES WITH DISCREPANCY TO EXPLAIN |
| 30 | 0.067563458860 | 0.0676018797 | +5.7e−4 | AGREES WITH DISCREPANCY TO EXPLAIN |
| 26.565 | 0.077782154314 | 0.0778869709 | +1.35e−3 | DISAGREES |
| 20 | 0.106223257350 | 0.1069789401 | +7.1e−3 | DISAGREES |
| 15 | 0.141997013743 | 0.1455041688 | +2.5e−2 | DISAGREES (cuspis's 15° is qualitative only) |

## Third reference: the published HHCWM16 series, computed by the bridge
The bridge summed the series itself, from quantum's own C1-R transcription of HHCWM16 Table 3, which was
transcription-checked against cuspis earlier. The two estimates are κ-tail (a lower estimate) and r₇-tail (an upper
estimate), both under the observed monotone r_p.

| θ | S₈ (rigorous lower bound, given positivity) | tight interval [S₈+κ-tail, S₈+r₇-tail] | quantum vs κ-estimate | cuspis vs κ-estimate |
|---|---|---|---|---|
| 40 | 0.046692 | [0.047386, 0.047388] | **+7.7e−7 (inside)** | +6.4e−5 |
| 30 | 0.064486 | [0.067593, 0.067605] | **−4.3e−4** | +1.35e−4 (inside) |
| 26.565 | 0.072654 | [0.077874, 0.077894] | **−1.2e−3** | +1.7e−4 (inside) |
| 20 | 0.092517 | [0.106970, 0.107025] | **−7.0e−3** | +8.4e−5 (inside) |
| 15 | 0.112667 | [0.145713, 0.145839] | **−2.5e−2** | −1.4e−3 (its known cutoff) |
| 90 | – | – | +3.9e−8 | – |

## Reading (post hoc and the bridge's own, not a registered verdict)
**quantum's instrument:**
- excellent at 40° and 90°;
- increasingly LOW below about 35°, and growing fast toward sharp angles (−4e−4, −1e−3, −7e−3, −2.5e−2);
- this pattern is typical of a truncation (mass cutoff, integration range or tail) that the coarse/fine resolution
  gate cannot see;
- it stays above the rigorous S₈ lower bound everywhere, so it doesn't violate the strict bound, only the
  series-plus-tail estimate.

**cuspis's values:**
- sit inside the tight series interval at 20–30° to ~1e−4;
- so its self-assessed systematic budgets were conservative.

**Caveats:**
- the κ/r₇ tail interval rests on the observed monotonicity of r_p;
- at 15–20° the series tail is a large fraction of the value (S₈ is 22% low at 15°), so the interval there is a model
  estimate, not a bound.

**To quantum:** only the verdicts, plus a suggestion that it self-check against the published series with its own
machinery, and audit its truncation parameters. No values.
