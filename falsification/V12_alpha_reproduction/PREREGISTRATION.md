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

## Addendum 1 (2026-10-11, before any gate value was compared): G1 pointed at the wrong circular orbit
**What happened.** The first `v12_lsep.py` run stopped on its own monotonicity assertion. A scan of the closed-pocket
predicate on the grid showed it is NOT monotone in |L|: at TS 4/5, E = 0.97 it is True only for |L|/m ∈ [4.19, 4.48].

**Physics, now stated correctly.** At fixed E < 1, as |L| grows:
- a closed pocket first appears when the barrier top reaches W = −1. That is the **unstable** circular orbit of energy
  E, which is the separatrix.
- the pocket disappears when its floor rises through −1. That is the **stable** circular orbit of energy E.

The original G1 text named the stable orbit; that was wrong. The L_sep definition itself ("smallest |L| with a closed
interval") is unchanged and matches the spec.

**Changes:**
- **L_sep** = the lower edge, by bisection between the last False and the first True grid point. Monotonicity is no
  longer asserted.
- **G1 (corrected):** on Kerr, the lower edge must equal the BPT **unstable**-branch L at E (r_mb < r < r_isco) to a
  relative 1e−8, for the physical sense.
- **G1b (new, same tolerance):** the upper edge, found by its own bisection, must equal the BPT **stable**-branch L.
  This is a second analytic check on the same code.
- No gate value had been compared to BPT, ansatz or anything else when this was written. The only output seen was the
  predicate's True/False pattern on the TS 4/5 grid.

## Addendum 2 (2026-10-11, post-failure, synthetic data only, before any real orbit): G4 was mis-calibrated
**G4 as pre-registered FAILED** (`results/v12_G4.json`, seed 4, K = 2000):

| Case | Hits | α̂ (MLE) | CI | Band | Result |
|---|---|---|---|---|---|
| smooth | 399/156/49/23/8 | 0.871 | [0.78, 0.98] | [0.95, 1.05] | FAIL |
| Cantor | — | 0.285 | — | 0.369 ± 0.05 | FAIL |
| random | — | 0.0025 | — | [−0.05, 0.05] | PASS |

**Root cause: the gate, not the estimator.**
1. **Sampling spread was ignored.** Across 20 seeds (K = 2000, w = 0.03) the smooth α̂ has mean 0.987 and sd 0.041.
   Its bootstrap CI covers 1 in 20/20. A single-draw band of ±0.05 fails about 25% of the time by design; seed 4 is
   about a 3σ low draw.
2. **The target ignored finite-range bias of the TRUTH.**
   - The exact Cantor f(ε), from a deterministic 2·10⁶-point grid, has slope 0.322 over the pre-registered
     ε ∈ [3e−5, 3e−3] (ε/w ∈ [1e−3, 1e−1]).
   - Its local slopes are 0.236, 0.320, 0.343, 0.373. The asymptotic 0.369 is reached only at smaller ε/w
     (0.363 over ε = w·3^−k, k = 3–11).
   - So over this range, the quantity the estimator measures is an **effective exponent**, and 0.369 was the wrong
     target.

**Consequence for the real study (stated before any real data).** V12's α, like ansatz's, is an effective exponent
over [3e−5, 3e−3], not an asymptotic dimension. Single-level α̂ carries a sampling sd of about 0.04 near α ≈ 1. The Kerr
band [0.85, 1.15] is about ±3.5σ and is kept.

**G4′ (replaces G4).** 20 seeds per synthetic case (K = 2000, w = 0.03, the same ε set). The population target α_pop
is the binomial-likelihood fit to the exact f(ε) from the dense grid, over the ε with ≥ 10 expected hits.
- smooth: |mean α̂ − α_pop| ≤ 0.03, and CI coverage of α_pop ≥ 17/20;
- Cantor: the same two criteria;
- random: |mean α̂| ≤ 0.03.
The failing seed-4 run stays on record.

## Addendum 3 (2026-10-11, post-failure, synthetic only): G4′ failed on Cantor CI coverage; decision rule written BEFORE measuring
**G4′ result** (`results/v12_G4p.json`):

| Case | Mean α̂ | α_pop | sd | Coverage | Result |
|---|---|---|---|---|---|
| smooth | 0.993 | 1 | 0.046 | 20/20 | PASS |
| Cantor | 0.310 | 0.305 | 0.013 | **16/20** (needed ≥ 17) | **FAIL** |
| random | 0.0013 | — | — | — | PASS |

The bias criterion passed for Cantor; only coverage failed. 16/20 has probability about 0.016 under exact 95%
coverage, so the percentile bootstrap may under-cover on fractal boundaries.

**Rule, fixed before the 200-seed measurement:**
- Measure coverage of α_pop over 200 seeds (600–799) for smooth and Cantor.
- If both are ≥ 90%: keep the percentile bootstrap, report the measured coverages next to every V12 CI, and treat G4′
  as passed on bias plus measured coverage.
- If either is < 90%: switch the primary CI to a bootstrap-t (studentized; inner bootstrap 100) and re-run this
  200-seed check on the new interval. The new interval must reach ≥ 90% on both before any real run.

**Why this doesn't touch the verdicts.** The primary verdict thresholds (TS CI upper end < 0.5; Kerr CI ∋ 1) are
unchanged. Kerr's smooth-case coverage is the relevant one for the Kerr criterion, and that was 20/20.

**Addendum 3 outcome** (`results/v12_G4p_coverage200.json`, seeds 600–799):
- smooth: coverage 192/200 = **96%**; mean α̂ 0.999, sd 0.053.
- Cantor: coverage 186/200 = **93%**; mean α̂ 0.304 against α_pop 0.305, sd 0.011.

Both are ≥ 90%, so under the rule above the percentile bootstrap is kept and **G4′ PASSES**. Every V12 CI will be
reported with these measured coverages (smooth 96%, fractal 93%).

## Addendum 4 (2026-10-11): scheduling only
V12 runs before tabula's §195 G0 rerun, with tabula's agreement. Tabula is first debugging a segfault in its own smoke
test and expects no G0 launch within 45 min. The numba integrator makes V12 roughly 30–45 min on 6 workers. No science
change.

## Addendum 5 (2026-10-11, before any α data): Kerr-chart regularity bug and window design flaw, both found in the window scan
**What the window scan showed** (`windows` mode; outcomes only, no ε sampling, no α):

**(a) The bridge's own Kerr chart is numerically singular at the ergosurface.**
- Kerr 3/5 had 12/400 CAPPED starts. Every one stalled while crossing the ergosurface f = −g_tt = 0, which at p = 3/5
  lies at x = 5/3 on the equator, outside the plunge cut 1.5.
  - scipy also needed 2.15 M steps to reach τ = 0.79, so this is not specific to the numba integrator.
- **Cause:** `kerr_ts_chart.py` builds g_φφ = −fω² + ρ²/f and g_tφ = fω with ω ∝ 1/A (A = the numerator of f), so
  terms that are singular individually cancel. Measured against 50-digit evaluation, the relative error of the float
  g_φφ is 5e−9 at Δx = 1e−4, 2.5e−5 at 1e−6, and 1.2 at 1e−8.
- **The TS component files are regular:** ≤ 5e−16 down to Δx = 1e−12 at both p, on the equator and at y = 0.5.
- Kerr 4/5 never meets its ergosurface before plunging: it sits at x = 1.25 on the equator, and f > 0 at x ≥ 1.5 for
  all y. So only Kerr 3/5 is affected.
- **Fix:** V12 uses `sp.factor(sp.cancel(·))` of every Kerr component. V11's code is left untouched as a sealed run;
  its Kerr 3/5 results are flagged for a re-check.
- **New gate G0r:** for all 4 charts, every component evaluated in floats must match a 50-digit evaluation to a
  relative 1e−12 at Δx = 1e−2 … 1e−12 from the ergosurface (equator and y = 0.5). G1 and G2 are re-run on the
  regularised Kerr chart.

**(b) The pre-registered window spans both boundaries.** Every system's start interval reads PLUNGE | SURVIVE | PLUNGE.
For example, TS L1: plunge on [1.5, 9.98], survive on [9.98, 56.7], plunge beyond. The hull of all changes therefore
has |W| ≈ 24–48. With K = 2000, a smooth boundary would give < 1 hit at ε = 3e−3, so every Kerr fit would come out
INSUFFICIENT. That is a design error.

**Replacement, the spec's choice, with the bridge's own parameters:**
- PRIMARY = the **inner** transition (the status change at smallest x0).
- Stage 2: 400 x0 uniform on [x_a − 3Δ, x_b + 3Δ], where x_a and x_b are the coarse points bracketing the inner change
  and Δ is the coarse step.
- W = the hull of the stage-2 changes ± 3 dense steps, widened symmetrically to ≥ 0.03.
- SECONDARY = the outer transition, treated identically. It is reported, but kept out of the verdict.

Nothing else changes.

## Addendum 6 (2026-10-11, written while G3 is running, after seeing 2 of its 300 rows): G3 is ill-posed on chaotic orbits
**Seen so far:** 2 TS L1 rows where numba says SURVIVE and scipy says PLUNGE (x0 = 9.900835…, 9.912877…). Probed with
the numba integrator alone, both orbits' outcomes change with tolerance:
- rtol 1e−10, 1e−12, 1e−13 → PLUNGE, after 124–197 crossings;
- rtol 1e−11, 1e−14 → SURVIVE.

These are long chaotic transients. Their outcome depends on perturbations at the integration-error level, so no two
correct integrators must agree on them. "≥ 99% identical outcomes" is therefore not a valid integrator test on TS
windows.

**G3′ (replaces G3; fixed before the remaining G3 rows are read):**
- **Kerr systems (s1, s5):** unchanged. ≥ 99% identical outcomes, and survivors' first 20 section x agree to 1e−7.
- **TS systems (s0, s4):**
  - (i) every numba/scipy outcome disagreement must be **realisation-sensitive**, meaning the numba outcome is not
    invariant across rtol ∈ {1e−11, 1e−12, 1e−13, 1e−14};
  - (ii) among orbits that ARE invariant across those tolerances, ≥ 99% identical outcomes;
  - (iii) the **first** section crossing must agree to 1e−8 for every orbit with ≥ 1 crossing in both, since
    divergence has not had time to grow by then;
  - (iv) on survivors that are invariant across tolerances, the first-20 dx is reported; it is not gated, because
    chaotic orbits legitimately diverge.
- **Reported quantity:** the realisation-sensitive fraction r of each TS window, as a by-product. It feeds the
  interpretation, not the primary fit. The primary fit is unchanged.

**Interpretive note, stated now.** An orbit whose outcome flips under integration-error perturbations is a point
where the outcome is sensitive at every resolvable scale. In f(ε) such points count as uncertain at every ε, as they
should for chaotic dynamics. E1's rule for excluding noise-dominated ε stays as pre-registered.
