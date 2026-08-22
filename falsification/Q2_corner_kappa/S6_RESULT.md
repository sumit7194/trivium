# s=6: the corner spread falls FASTER than s⁻², and the drift is ~10× the noise

**The rung that was recorded as permanently out of reach this afternoon.** It ran in 15.5 minutes on a
box we had both computed could not hold it. The refusal was tested and wrong; see
[PEAK_MEASUREMENT.md](PEAK_MEASUREMENT.md).

## The measurement

    s=6  L=960  m·L=1.60  l=24…120     four regulators, 990/1126/891/887 s

    s=6 floor=1e-14 3p: area 36.2213%   CORNER 0.02902%
    s=6 floor=1e-09 3p: area 36.2208%   CORNER 0.02891%

## What it answers

quantum's single open question was whether the s⁻² constant's **1.3% scatter over s=3,4,5** was noise or
drift. s=6 was the point that would settle it, and it was written off as unreachable.

| s | corner spread % | s²·spread |
|---|---|---|
| 1 | 1.68650 | 1.68650 |
| 2 | 0.25000 | 1.00000 |
| 3 | 0.12000 | **1.08000** |
| 4 | 0.06762 | **1.08192** |
| 5 | 0.04274 | **1.06850** |
| 6 | 0.02902 | **1.04472** |

*(s=1,2 quantum's; s≥3 this study. Provenance flagged because three of the five numbers in their
published sequence are mine — see their README.)*

**The constant is not constant. It falls monotonically from s=4 on**, and the scatter nearly triples when
s=6 is added:

    over s=3,4,5     1.0685 … 1.0819    1.25%
    over s=3,4,5,6   1.0447 … 1.0819    3.48%

**Local exponents:**

    s 3->4    s^-1.994
    s 4->5    s^-2.056
    s 5->6    s^-2.123        the deviation from -2 GROWS with s
    global    s^-2.048

## Is it above the noise?

The clip band — the difference between the two eigenvalue floors — gives a per-point error estimate:
**0.12% at s=5, 0.38% at s=6.** The constant moves **3.4%**. **The drift is roughly 10× the numerical
noise.** It is not scatter.

## What this does and does not establish

**Does:** the corner spread falls faster than s⁻², the deviation is monotone in s, and it exceeds the
numerical noise by an order of magnitude. quantum's 1.3% was the visible part of a trend, not error.

**Does not:** identify what the true law is. `s^-2.048` global is a fitted exponent over four points and
carries every caveat this repo learned today — hold-out unvalidated at this range, and a fitted exponent
absorbs whatever the model omits. **Four points cannot distinguish a slightly different power from s⁻²
plus a subleading correction**, and those have different meanings for universality.

**And it does not clear the open systematic.** The zero-mode non-common residual is **22–41% of the
regulator signal** at every resolution measured (quantum, s=1,2,3), unmeasured at s=6 until the deletion
pass runs. **A 3.4% drift sits well inside a systematic of that size.** The drift is real against
*numerical* noise; whether it is real against the *zero-mode* contamination is exactly what the deletion
pass is for, and that number does not exist yet.

**Treat this as: the s⁻² law is not exact, by an amount that numerical noise cannot explain and the known
systematic can.**
