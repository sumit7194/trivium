# V11 — Pre-registration: the bridge's independent reproduction of chaos candidates (ansatz's TS δ=2 chaos study)

*2026-10-10. Written and committed BEFORE any V11 code runs. Conventions come from ansatz's text message (y0 = 0,
p_x0 = 0, p_y0 > 0 from the mass shell, μ² = 1, up-crossings of y = 0, affine time = proper time, S_ex and fd as
defined there). The bridge has not read ansatz's code.*

## The bridge's own implementation (`code/v11_chaos.py`)
- **Metric:** the bridge's own transcription. ZV δ=2 comes from V8's `zv()`, TS from ansatz's sealed component files
  via V8's loader, and Kerr from V10's Boyer–Lindquist form.
- **Equations:** H = ½[g^xx p_x² + g^yy p_y² + W] with W = g^tt E² − 2g^tφ E L + g^φφ L². The vector field and its
  **exact Jacobian** come from sympy symbolic differentiation (ansatz uses central differences).
- **Integrator:** scipy **DOP853** (ansatz uses Dormand–Prince 5(4)), with exact section events at y = 0, direction +1.
- **Tangent vector:** v0 = (1, 0.7, −0.4, 0.3)/‖·‖, evolved by the exact variational equations. It is renormalised
  every Δτ = 10.
- **Detector:** S_ex = Σ ln‖v‖ − ln τ_last, with chaos declared at S_ex ≥ 10.
- **Frequency drift:** fd per the stated recipe (halves, Hanning window, rfft, parabolic peak), threshold 0.0115, used
  only when n ≥ 100.
- **Stops:** 300 crossings, τ = 5e6, plunge x < 1.5, or escape x > 2000.
- **Tolerances:** rtol 1e−11 and 1e−13. A classification counts only if both tolerances agree.

## Validation gate (ZV δ=2, E = 0.95), which must pass before any TS candidate is examined
| Orbit | Expected |
|---|---|
| L = 2.9, x0 = 7.56263 | CHAOTIC (S_ex ≥ 10 at both tolerances) |
| L = 3.0, x0 = 7.57274 | CHAOTIC |
| L = 3.0, x0 = 7.62 | REGULAR (S_ex < 10, fd < 0.0115 at both tolerances) |

The comparison is on classifications, not identical numbers, because layer orbits are sticky and depend on the exact
realisation. **If any orbit is misclassified, STOP and diagnose; the detector is not tuned on these orbits.**

## Use
Each TS candidate ansatz reports gets reproduced at both tolerances.
- **REPRODUCED:** CHAOTIC at both.
- **NOT REPRODUCED:** REGULAR at both.
- **INCONCLUSIVE:** the two tolerances disagree.

## Addendum 1 (before any Kerr replay): Kerr in ansatz's chart, a Carter diagnostic, and the truncated score
- **Kerr in the TS chart:** `kerr45` (p = 4/5) and `kerr35` (p = 3/5), built from the δ = 1 Ernst potential with the
  same conventions (`code/kerr_ts_chart.py`). The twist equations are satisfied exactly, and R_ab = 0 exactly at 3
  rational points.
- **Carter diagnostic:** Q = (1−y²)p_y² + y²(a²(1−E²) + L²/(1−y²)), with a = q/p, recorded as the maximum relative
  deviation along the orbit while x ≥ 1.5. A conserved Q together with a "chaotic" score marks a detector false positive.
- **Truncated score:** classification now uses S_ex truncated at the last section crossing, the same rule as ansatz's
  amendment 4. Untruncated S_ex is still reported. The ZV gate is re-checked under the truncated score before any Kerr
  replay.

## Addendum 2 (before any TS replay): a geometric diagnostic, the classification rule, and a speed-up
**Why.** S_ex is unspecific near the separatrix, since regular Kerr orbits reach 11–62 (ansatz). And fd is
realisation-sensitive: the bridge's own 1e−13 realisations of the ZV layer orbits gave fd 0.0006 and 0.002.

**Two geometric diagnostics** on the section points (x, p_x), standardised by their std, at n ≥ 100:
- **R (Fourier roughness):** the RMS residual of a K = 12 Fourier fit of radius against angle about the centroid,
  divided by the RMS deviation of the radius about its mean.
- **D (nearest-neighbour dimension):** D = ln 2 / ln(d½/d₁), where d₁ and d½ are the median nearest-neighbour distances
  for all points and for the first half. D ≈ 1 for a curve and ≈ 2 for an area.

**Calibration on controls only:**
- regular: the ZV torus at 7.62, the flagged Kerr orbit (kerr45, E = 0.97, L = 1.25, x0 = 4.44855), and matched Kerr
  orbits;
- chaotic: the ZV layer orbits at L = 2.9 and L = 3.0.

The diagnostic used is whichever of R and D separates every regular control from every chaotic one with the larger
log-margin. Its threshold is the geometric mean of the closest regular and chaotic values. If neither separates the
controls, it is reported, and V11's TS verdicts rest on S_ex and fd only, as INCONCLUSIVE unless all agree.

**Classification for TS replays:** the chosen geometric diagnostic is primary, and it must agree at both tolerances.
S_ex, fd and (for Kerr) the Carter deviation are all reported alongside.

**Speed-up:** F and J are lambdified jointly with shared common-subexpression elimination. The arithmetic is unchanged.

## Addendum 3 (after the ZV calibration runs, before any TS replay): a late-escape criterion and neighbourhood ensembles
**What the ZV calibration showed.** The same layer orbits give different realisations under tiny arithmetic changes. The
joint-CSE build changes the rounding.
- L = 2.9 at 1e−13: no plunge in 300 crossings, R 0.002, fd 1e−4, S_trunc 9.6. Looks regular.
- L = 2.9 at 1e−11: plunges at 186, R 0.044.
- L = 3.0: R 0.0015 and 0.58 at the two tolerances.

**Consequence.** Single-orbit classification of sticky layer orbits is realisation-dependent. That is inherent to thin
chaotic layers, not a bug. **D (the nearest-neighbour dimension) is broken for quasi-periodic orderings** (it gives 50
on the torus) and is DROPPED.

**Added criteria, physically grounded, for the TS replays:**
1. **Late escape (primary).** In an integrable system a bound orbit lies on an invariant torus with fixed radial turning
   points. One that completes ≥ 50 section crossings can never later plunge, except through integration error across
   an unstable manifold. So an orbit counts as NON-REGULAR if it plunges after ≥ 50 crossings at BOTH tolerances, with
   |2H+1| < 1e−9 at its last crossing. For Kerr, this is backed by the Carter deviation check.
2. **Neighbourhood ensemble.** For each TS orbit a)–g), integrate 8 neighbours at x0 ± {0.001, 0.002, 0.004, 0.008}, at
   rtol 1e−13, plus the same 9 initial-condition offsets on the matched Kerr level, i.e. the same E and L/m with x0 at
   the same relative position in its survive window. Record the fraction that is NON-REGULAR (late escape, or R above the
   addendum-2 threshold if R separates the controls).
   - **CONFIRMED (bridge):** the TS fraction ≥ 3/9 and the Kerr fraction = 0 at that level.
   - **NOT CONFIRMED:** the TS fraction is 0.
   - **INCONCLUSIVE:** anything else.
3. **Single-orbit S_ex, fd and R** at both tolerances are still reported for comparison with ansatz.

## Addendum 4 (ensembles running, NO ensemble result yet seen): the scoring is replaced, the premise was wrong
**Correction, raised by ansatz before any data.** Addendum 3's premise ("a bound orbit with ≥ 50 crossings can never
later plunge") is false near the separatrix. In an integrable system, plunge-or-not is fixed at t = 0, but an orbit
just on the plunge side zoom-whirls near the unstable spherical orbit. That costs ~log(1/δ) of time per approach, with
polar oscillations, so it can make 50+ crossings and then plunge with Carter exactly conserved. Late escape is
therefore NOT a non-integrability signature by itself.

**Replacement primary criterion: escape-basin structure across each 9-member ensemble.** The data are unchanged; only
the scoring changes.

Order the members by x0. Record each outcome as S (survives 300 crossings) or P(n) (plunges after n crossings).
- **Integrable expectation:** at most ONE S/P status change within ±0.008. On the P side, n is monotone, increasing
  toward the boundary (≈ −log|x0 − x_b|).
- **Chaotic (fractal basin) expectation:** S and P interleave (≥ 2 status changes), and/or n is non-monotone on a P run.

Scores:
- T = the number of S/P status changes;
- V = the number of monotonicity violations of n along each P run (oriented toward the adjacent S block, or toward the
  larger n if there is no S block).

Per orbit:
- **CONFIRMED (bridge):** TS has T ≥ 2 or V ≥ 2, AND the matched Kerr ensemble has T ≤ 1 and V = 0, with Carter
  conserved (max relative deviation < 1e−8) on every Kerr member.
- **NOT CONFIRMED:** TS has T ≤ 1 and V = 0.
- **INCONCLUSIVE:** anything else, including any Kerr member with T ≥ 2, V ≥ 1, or a Carter violation. That would mean
  the instrument fails its control.

**Also reported:** every member's n, status, H drift, R and fd, and, as ansatz asked, the Kerr crossing counts before
plunge. Late escape stays as a descriptive column only.
*Addendum 4 clarifications (still no ensemble result seen), from ansatz:*
1. V counts only STRICT reversals of n; equal neighbouring counts are not violations.
2. "S" means the member survived the 300-crossing budget, not that it survives forever. The budget is stated next to
   every T.

## Implementation note (2026-10-10 ~23:00, before ANY ensemble data existed)
The first ensemble launch made no progress. Evaluating the full symbolic F and J took ~3.4 ms per call, an 814k-character
expression with no effective CSE, and no orbit finished in ~2.7 h. A power cut also killed the very first launch.

**Replacement:** a compact build. Only A = g^xx, B = g^yy and W are generated, with their first and second derivatives,
CSE'd and numba-compiled; F and the exact J are then assembled analytically.

**Validated before use:**
- It agrees with the original build to ≤ 2.2e−11 relative, at 80 random points across ts45, ts35, zv and kerr45.
- The flagged Kerr orbit reproduces its calibration: regular, S_trunc 4.1, fd 1e−4, Carter 5.9e−13.

The mathematics, criteria and scoring are unchanged (addendum 4).

## Addendum 5 (2026-10-10 ~23:20, before ANY ensemble data existed): step cap
Diagnosis: a TS neighbour orbit (ts45, x0 − 0.05) stalls inside a single 10-τ chunk. It takes ever-smaller steps,
presumably near a TS singular region, and with no step limit it hangs. ansatz's design has a step cap for the same
reason.

**Rule:**
- An orbit integration is capped at 3,000,000 right-hand-side evaluations; on reaching the cap, status = "capped".
- A capped orbit is NEVER counted as S or P.
- In the basin score, capped members are excluded from the ordered S/P sequence, and they're reported.
- An ensemble with fewer than 6 non-capped members, on either the TS or the Kerr side, is INCONCLUSIVE.
- In quick classifications, "capped" is its own class, so it neither brackets nor matches a survive/plunge transition.

Everything else is unchanged.

## Addendum 6 (2026-10-11, POST-FAILURE, after the a–g ensemble results were seen): a bug fix restoring the registered plunge definition
**Root cause (diagnosed).** The registered plunge criterion is x < 1.5, but it was tested only at the END of each 10-τ
chunk.
- An orbit that crossed x = 1.5 mid-chunk kept falling toward the (x, y) → (1, ±1) corner, the pole of the central
  object, where momenta exceed 1e6.
- The integrator then crawled until the evaluation cap fired, giving status "capped".
- Example: TS ensemble d, x0 = 5.927068, really plunges after 3 crossings at τ ≈ 117.
- The same defect hid the Kerr plunges, so no Kerr survive/plunge transitions were found.

**Fix:**
- x = 1.5 (inward) and x = 2000 (outward) are now TERMINAL integrator events, so the definitions are unchanged and are
  now applied exactly when crossed.
- The evaluation cap becomes a PER-CHUNK stall guard: 2M evaluations within one 10-τ chunk gives status "stalled".
  It's excluded from S/P like "capped".

**Checks (before any rerun):**
- The TS d member now gives plunge, 3 crossings, |2H+1| 3e−13.
- The Kerr inner quick check now gives plunge.
- The flagged Kerr orbit is unchanged: 300 crossings, S_trunc 4.1, fd 1.1e−4, Carter 5.9e−13.
- The ZV torus is unchanged: S_trunc −4.0, fd 3.6e−6.

**The rerun of ensembles a–g under addenda 3–5 + 6 is labelled POST-FAILURE.** The scoring and verdict rule are
unchanged.

**Scheduling:** the rerun waits its turn (ansatz's p35w α rerun, then tabula §194, then this).
