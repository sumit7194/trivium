# V12: pre-registration of the bridge's independent reproduction of the TS δ=2 fractal-basin exponent α

*2026-10-11. Written and committed BEFORE any V12 code exists.*

**Target.** ansatz's claim that at matched distance from each system's own separatrix:
- the survive/plunge boundary of TS δ=2 is fractal, with uncertainty exponent α ≈ 0.05–0.16;
- Kerr's boundary is smooth, with α ≈ 1.05.

**Source.** The method spec comes from ansatz's text message of 2026-10-11: definitions only, no code, no per-orbit
data.

**What is known in advance.** The headline ranges are known, as is ansatz's L_sep at each level. The per-level α
values and CIs are not, and ansatz is asked to hold them until V12's numbers are sealed.

## What is shared with ansatz (needed for comparability), and what is the bridge's own
| | Shared (from the spec) | Bridge's own |
|---|---|---|
| Physics | reduced 2-DOF H = ½[g^xx p_x² + g^yy p_y² + W], μ² = 1, p_t = −E, p_φ = L | metric transcription (V10 loader for TS; `kerr_ts_chart.py` for Kerr), compact symbolic build (V11) |
| Levels | TS (p, E, L) of L1, L2, L3 | L_sep by **bisection to 1e−10** (not a 0.01 m grid); hence its own ε_sep and its own Kerr partner L |
| ICs | y = 0, p_x = 0, p_y > 0 from the mass shell; perturb x0 | window procedure, sample size, seeds |
| Outcomes | SURVIVE (N crossings or τ = 5e6), PLUNGE (x < 1.5), ESCAPE (x > 2000 or \|y\| > 0.999999) | integrator: **numba-compiled DOP853** with terminal events; validated against scipy DOP853 |
| Estimator | uncertainty fraction f(ε) (Grebogi–McDonald–Ott–Yorke) | primary α fit by **binomial maximum likelihood**; ansatz's WLS is reported only as secondary |

## Levels (TS values from the spec; Kerr partners computed by the bridge)
- **L1:** TS p = 4/5, E = 0.97, L = +5.125 (σ = 1, m = 2/p = 5/2)
- **L2:** TS p = 4/5, E = 0.97, L = +5.875
- **L3:** TS p = 3/5, E = 0.95, L = −16/3

For each level:
- **L_sep(TS):** the infimum of |L| (at fixed E and fixed sense) for which the equatorial allowed set
  {x : W(x, 0) ≤ −1} contains a closed interval touching neither x_in nor x = 400.
  - x_in = x_ring + 0.01 for TS; x_in = 1.0005 for Kerr.
  - Found by bisection on |L| to 1e−10, with the closed interval detected by sign changes of W + 1 on a fine grid,
    refined by root-finding.
- **ε_sep = (|L| − L_sep)/L_sep.**
- **Kerr partner:** p equal to TS's, same E, and |L_K| = L_sep,K·(1 + ε_sep,TS).
  - **Sense** is matched PHYSICALLY: sign(L·J) is equal in TS and in Kerr.
  - The J sign is read from each chart's asymptotic g_tφ, not assumed from chart conventions.

## Gates (all must pass before any α target runs)
- **G1, Kerr L_sep against the analytic answer.**
  - On Kerr, the pocket first appears at the stable equatorial circular orbit of energy E.
  - The bridge's numerical L_sep,K must equal the Bardeen–Press–Teukolsky circular-orbit L at E_circ(r) = E
    (stable branch, r_BL = x + m) to a relative 1e−8, at p = 4/5 and p = 3/5, for the sense used.
- **G2, agreement with ansatz's grid values.** The grid value over-states the true threshold by less than one step, so
  0 ≤ L_sep,ansatz − L_sep,bridge < 0.01 m + 1e−9 must hold for:
  - TS 4/5 (+): 10.475;
  - Kerr 4/5: 5.2125;
  - TS 3/5 (−): 9.2667 (that is, 139/15 to the spec's precision; tolerance 1e−4 on that rounding);
  - Kerr 3/5: 4.500.
  - A failure here is diagnosed before running. It does not void the run, because the bridge's exact L_sep is the
    better-defined quantity. Any disagreement is reported.
- **G3, the integrator.**
  - 300 orbits (4 systems × 75 x0 drawn in the windows) through the numba DOP853 and through scipy DOP853, both at
    rtol 1e−11.
  - The outcome class must be identical for ≥ 99%.
  - On survivors, the first 20 section x-values must agree to 1e−7.
- **G4, the fitter**, on synthetic outcome functions with K = 2000:
  - a smooth single boundary must give α ∈ [0.95, 1.05];
  - the middle-thirds Cantor boundary must give α = 1 − ln2/ln3 = 0.369 ± 0.05;
  - outcomes that are i.i.d. random at every x0 must give α ∈ [−0.05, 0.05].
- **G5, conservation.** |2H + 1| < 1e−8 at the end of every SURVIVE orbit. On a 200-orbit Kerr sample, the Carter
  relative drift (V11 `carter()`) must be < 1e−9.

## Primary runs: the 3 matched pairs (6 systems)
- **Window.**
  - 400 x0 uniform across the allowed equatorial interval [max(x_in, 1.5), x_outer turning point] at N = 300.
  - W = the hull of all status-change midpoints, ± 3 grid steps.
  - Then widen symmetrically to |W| ≥ 10·ε_max = 0.03. This is ansatz's saturation lesson, adopted from the start.
- **Sample.** K = 2000 x0 uniform in W (numpy default_rng seeds 12000 + system index). The design is nested: each x0
  is integrated with x0 ± ε for ε ∈ {3e−3, 1e−3, 3e−4, 1e−4, 3e−5}.
- **Settings.** N = 300 crossings, rtol 1e−11.
- **Uncertain** at ε: outcome(x0 − ε) ≠ outcome(x0) or outcome(x0 + ε) ≠ outcome(x0). f(ε) = #uncertain / K_valid.
  Step-capped or forbidden starts are excluded and counted.
- **Primary estimator.** Binomial maximum likelihood for log f = c + α log ε over all ε with ≥ 10 hits; at least 3
  such ε, else INSUFFICIENT.
  - 95% CI: nonparametric bootstrap over x0 (1000 resamples, percentiles 2.5/97.5).
  - Secondary: the weighted least squares in the spec.

**Verdict per pair:**
- **VOID (INCONCLUSIVE)** unless Kerr α̂ ∈ [0.85, 1.15] with its CI containing 1.
- **CONTRAST REPRODUCED** if TS's CI upper end is < 0.5 and the TS and Kerr CIs are disjoint.
- **NOT REPRODUCED** if TS α̂ ≥ 0.85 with a CI containing 1, i.e. TS looks smooth like Kerr.
- **INCONCLUSIVE** otherwise.

**Overall:** REPRODUCED if at least 2 of the 3 pairs give CONTRAST REPRODUCED and none gives NOT REPRODUCED.

**Numeric agreement (secondary).** After V12 is sealed, ansatz's per-level α and CIs are compared. They AGREE if the
CIs overlap. A disagreement with both contrasts reproduced is reported as a quantitative discrepancy, not as a failure
of the claim.

## Pre-registered extensions (run after the primaries; they answer ansatz's open questions)
**E1, depth and horizon (L1 pair only):**
- ε extended by {1e−5, 3e−6, 1e−6}, at both N = 300 and N = 600, with rtol 1e−13 throughout E1. One tolerance is used
  per fit.
- **Realisation-sensitivity rule:** the fraction r of x0 whose base outcome differs between rtol 1e−11 and 1e−13 is
  measured. Any ε with f(ε) < 3r is excluded as noise-dominated.
- **Interpretation, fixed in advance.** At any finite N the outcome map is piecewise smooth, so f must eventually
  cross over to α → 1 below some ε_c(N) ~ e^{−λT}.
  - A genuine fractal boundary predicts ε_c(600) < ε_c(300), with the flat region extending further at the longer
    horizon.
  - A finite-time artefact predicts ε_c independent of N.
  - If no crossover appears down to 1e−6 at either N, the result reads "flat to 1e−6". That is consistent with a fat
    fractal or a positive-measure chaotic layer, and it will not be over-interpreted.

**E2, perturbation direction (L1 pair):**
- Perturb p_x0 instead of x0. p_x0 = ±ε, with p_y re-solved from the mass shell; same windowed x0 and same ε set.
- The contrast must hold in this direction too. If it does not, that is reported as a limitation of the primary
  result.

## Resources and scheduling
- Starts only after tabula's §195 G0 rerun completes, per the user's sequential preference. Gates G1, G2 and G4 are
  CPU-light and may run before then.
- Up to 6 worker processes when the 5-minute load is < 8. Memory is small (< 0.5 GB per worker).
- Per-orbit checkpointing, so an interruption loses nothing.
- No human has checked this pre-registration.
