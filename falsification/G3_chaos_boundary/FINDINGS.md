# G3 — Findings: the scan completed. The instrument did not.

*Overnight run finished 2026-08-16 (9/9 δ, ~14 h across four sessions and three mains cuts); gates frozen in
[PREREGISTRATION.md](PREREGISTRATION.md) and its ADDENDUM before code. Supersedes the 2026-07-26
UNDECIDED(search) attempt, whose diagnosis is preserved in §"History" below.*

## Result in one line

**By the frozen rule, G3 is KILLED as stated** — δ = 1.02, 1.05 and 1.5 are proven non-integrable yet show
no detectable chaos, so δ\* > 1. **But the deliverable the pre-registration actually named — "the boundary
and how the signal scales on the way down" — is NOT supported by this run**, because the detector's drift
conjunct carries no measurable information and its escape conjunct has no counting statistics. The
scientific content is a **negative instrument result**, and it is worth more than the kill.

## The single number that decides it

Ranked by max ÷ median drift, the statistic the fire rule uses:

```
3678   δ=1.2    fired=2
2980   δ=1.0    fired=0     <== INTEGRABLE CONTROL — Schwarzschild, TRUE drift is exactly 0
2699   δ=1.7    fired=3
1656   δ=1.02   fired=0
1639   δ=1.3    fired=4
 988   δ=2.0    fired=2
 747   δ=1.1    fired=1
 511   δ=1.05   fired=0
 455   δ=1.5    fired=0
```

**Eight of nine δ sit at or below the integrable control.** Only δ=1.2 exceeds it, and by 23%.

ZV at δ=1 *is* Schwarzschild. Its true frequency drift is not small — it is **zero**. Everything the
instrument reads there is its own noise, and on this statistic that noise outranks six of the eight
deformed spacetimes, including three that fired. **No null model, no fired/silent labels and no
methodology are required to read that table**, which is why it is the headline.

## The gate table

| gate | result | supported? |
|---|---|---|
| **G3a** — integrable control (δ=1.0) must not fire | **PASS** — fired 0, clean 50, distinct drift values 50 | **weakly — see below** |
| **G3b** — reproduce §106's δ=2 layer | **PASS** — fired 2 at x₀ = 8.03693, 8.04093 | yes |
| **G3c** — the δ boundary | reported δ\* = **1.1**; fired at [1.1, 1.2, 1.3, 1.7, 2.0], silent at [1.02, 1.05, 1.5] | **NO** |
| **G3d** — species classification | reported; the run's own prediction is **falsified** | **NO** |

### G3a passes, and the ADDENDUM's fix was still not enough

The ADDENDUM's change 4 was written precisely to stop a conjunctive gate passing vacuously: G3a now also
requires the drift estimator to be **non-degenerate** on the control (≥5 distinct values). It is —
50 distinct values from 50 orbits. **The gate still fails to catch the defect**, because non-degeneracy is
not discrimination. At δ=1.0 the drift conjunct **clears its own firing threshold by ≈993×** (2980 ÷ 3),
and the control passes only because the *escape* conjunct is silent — which is exactly how run 2 passed.

**A conjunctive gate certifies nothing unless each conjunct is shown to DISCRIMINATE on the control, not
merely to be alive on it.** That is the strengthened form of the lesson, and it cost two runs to learn.

## The drift conjunct carries no measurable information

Four independent tests, on 498 recovered per-orbit records across the five settled, mutually matched δ
(2 bands, ~100 orbits each):

1. **Pass fraction is flat.** Fraction of orbits clearing `drift ≥ 3 × median`:

   | δ | 1.7 | 1.5 | 1.3 | 1.2 | 1.1 | 1.05 | 1.02 |
   |---|---|---|---|---|---|---|---|
   | pass | 39.6% | **39.4%** | **37.0%** | 42.9% | 42.0% | 35.0% | 35.6% |

   **35–43% everywhere**, and it does not order with firing — the silent δ=1.5 passes *more* orbits than
   the loudest δ=1.3. A 3×-median cut on a heavy-tailed sample passes ~40% by construction.

2. **Two-sample KS, firing vs silent.** Ten pairs, Bonferroni α = 0.005. **Smallest p = 0.039 — not one
   pair separates.** The sharpest available contrast, δ=1.3 (4 fired) vs δ=1.5 (0 fired), gives **p = 0.503**.

3. **Against the physical knob, not the noise label.** Grouping by fired count tests drift against a
   quantity that is itself noise, so the test was repeated against |δ−1|: pooled Spearman **ρ = +0.089**
   over 498 orbits (<1% of variance), Kruskal–Wallis across the five distributions **p = 0.265**.
   Drift fails to track the perturbation strength either.

4. **Median drift tracks δ, not chaos**: −5.017 (1 fired), −4.792 (2), −4.284 (4), −4.534 (0), −4.334 (3).

## The escape conjunct has no counting statistics

Because drift is uninformative, `n_fired` is determined **entirely by escape**. The escape counts are:

```
δ:      1.02  1.05  1.1  1.2  1.3  1.5  1.7  2.0
escapes:   0     0    1    2    4    0    3    2
```

Integers between 0 and 4, out of ~100 orbits each. As binomial proportions with exact 95% intervals:

| δ | 1.3 | 1.7 | 1.2 | 1.1 | 1.5 | 1.05 |
|---|---|---|---|---|---|---|
| escapes | 4/100 | 3/101 | 2/98 | 1/100 | 0/99 | 0/100 |
| 95% CI | [.011, .099] | [.006, .084] | [.003, .072] | [.000, .055] | [.000, .037] | [.000, .036] |

**Every interval overlaps every other.** And the decisive test — the loudest δ against the silent one,
the sharpest contrast the ladder contains:

> **δ=1.3 (4/100) vs δ=1.5 (0/99): Fisher exact p = 0.121.**

**The only discriminating conjunct in the detector cannot distinguish its own extremes at p < 0.05.**
Every other pairwise contrast is weaker still. **δ\* = 1.1 rests on one orbit escaping at δ=1.1 and none
at δ=1.05** — a difference whose interval spans nearly the whole observed range. That is not a boundary.

The sample size required to do better, at 80% power and α = 0.05, against the ~100 orbits per δ actually
run:

| effect to detect | orbits per arm needed |
|---|---|
| 4% → 2% (escape rate halves) | **1141** |
| 4% → 1% (quarters) | **424** |
| 4% → ~0 (total loss) | **191** |

**The escape conjunct is underpowered by roughly an order of magnitude for anything short of total
signal loss.** This bounds every claim in the item that depends on `n_fired`, which is all of them.

## G3d's own pre-registered prediction is falsified — and δ=1.02 is why

G3d predicted species-1 (precision), evidenced by *"max-drift declining smoothly toward the floor as
δ → 1"*, and named a non-smooth result *"a genuine surprise."* Observed:

| δ | 1.0 | 1.02 | 1.05 | 1.1 | 1.2 | 1.3 | 1.5 | 1.7 | 2.0 |
|---|---|---|---|---|---|---|---|---|---|
| max drift | 0.0087 | **0.0178** | 0.0061 | 0.0072 | 0.0598 | 0.0860 | 0.0133 | 0.1252 | 0.0286 |

**δ=1.02 — the δ closest to integrable — is the fourth-loudest in the ladder**, larger than δ=1.05,
δ=1.1 and δ=1.5, and **2.05× the integrable control**. The pre-registration's continuity argument requires
the signal to shrink to zero as δ→1⁺. It does not. The prediction is falsified, and the surprise is the
instrument, not the physics.

## Where the floor actually comes from

`drift()` was fed **synthetic quasiperiodic series with true drift identically zero** — constant
frequencies, no metric, no integrator, no force of any kind:

| case (N=200) | median | 90th pct | max of 400 |
|---|---|---|---|
| 3 incommensurate tones | **4.9e-06** | 9.2e-05 | 1.8e-03 |
| run's δ=1.0 floor (median) | **2.9e-06** | — | — |

**The per-δ "floor" is reproduced to within a factor of 2 with no dynamics at all.** It is FFT
peak-estimation sampling variance between two 100-point halves. **No integrator change, symplectic method,
or extended precision touches it.**

**A residual excess above pure-estimator noise does exist**, but ⚠️ **the null percentiles first quoted
here were not robust and are withdrawn.** They were `median ~208, 95th ~407, max 750–1001`. That null drew
`f0 ~ U(0.08, 0.30)` with tones at `f0·{1, √2, π/2}`, putting the top tone at up to **0.471 against a
Nyquist of 0.5** — so the widest draws were aliasing. The null's max/median is highly sensitive to that
arbitrary choice:

| assumed f₀ range | top tone | null max/median |
|---|---|---|
| U(0.08, 0.30) — *as published* | up to 0.471 | **315** |
| U(0.08, 0.20) | up to 0.314 | 98 |
| U(0.12, 0.18) — run-like | up to 0.283 | **18** |

**A 17× spread driven entirely by a parameter never matched to the data.** The qualitative conclusion
survives — δ=1.0's observed 2980 exceeds every variant, and narrowing toward run-like frequencies makes
the excess *larger*, not smaller — but **no specific null percentile should be quoted from this synthetic**,
and the p-values derived from it are withdrawn. Self-caught; the criticism that a floor measured on a case
that does not resemble the run is a floor for a different instrument is the same one this document levels
at the original FFT-bin null, one level up.

**The correct null must be computed at the orbits' actual observed frequencies.** That was impossible from
the banked records, which store no series — it is the reason forward-look item 4 exists, and the E2/E3 run
(see [PREREG_ESTIMATOR.md](PREREG_ESTIMATOR.md)) persists series specifically so it becomes possible.

Candidates for the excess, none yet tested: non-uniform section sampling (crossings are uniform in index,
not time, which the synthetic does not model); RK4 phase error over ~1.2M steps; the control's n=50
conditioning; and **frequency-dependent estimator gain** (below).

## The A1 integration guard is inert

```
A1 guard rejections: 0 of 599 orbits
dH range: 1.672e-13 .. 2.158e-12        DH_MAX = 1e-4
worst orbit sits 4.6e+07 x below the threshold
```

**The guard has never rejected anything.** It is cited in the pre-registration as the discipline keeping
integration artifacts out of the result; on this run it kept nothing out, because nothing came within seven
orders of magnitude of it.

**Two hypotheses were tested and one is settled.** Energy is *not* algebraically constructed:
`p_on_shell` is called exactly once, for the initial condition, and the loop is pure `_rk4`. Confirmed
behaviourally by a direct single-orbit h-sweep, worst |dH/H| = 1.045e-03 → 6.817e-05 → 5.933e-06 →
3.729e-07 at h = 0.04 → 0.005, i.e. **15.3×, 11.5×, 15.9× per halving — clean h⁴**. A projected quantity
would not scale with h.

**RESOLVED, and not as first suspected.** The seven-order gap between a directly-integrated orbit
(6.8e-05 at h=0.02) and the banked records (~1e-12) suggested that evaluating H only at section crossings
(`if prev < 0.0 <= s[1]`) was sampling a bounded-oscillatory error at a privileged phase. **That hypothesis
is falsified.** Measuring the same orbits both ways — at crossings, and at every step:

| δ | x₀ | crossings reached | dH at crossings | dH at every step | ratio |
|---|---|---|---|---|---|
| 1.3 | 6.0000 | **200** | 1.459e-13 | 1.767e-13 | **1.2×** |
| 1.3 | 9.0000 | **200** | 8.438e-15 | 1.066e-14 | **1.3×** |
| 1.7 | 10.0000 | **200** | 3.131e-14 | 3.597e-14 | **1.1×** |
| 2.0 | 8.0369 | **200** | 7.547e-13 | 8.635e-13 | **1.1×** |
| 1.3 | 5.1704 | 197 | 8.464e-13 | 5.302e-05 | 6.3e+07× |
| 1.1 | 4.3419 | 22 | 1.541e-13 | 6.604e-06 | 4.3e+07× |
| 1.0 | 9.6667 | 5 | 1.099e-13 | 1.685e-06 | 1.5e+07× |
| 1.7 | 6.8212 | 15 | 1.024e-13 | **1.663e-03** | 1.6e+10× |

**For every orbit that completes its record, crossing-sampling is faithful — ratio 1.1–1.3×.** There is no
phase artifact, and the recorded ~1e-12 is real for the recorded portion. The enormous ratios belong
exclusively to orbits that **terminate early**, and the mechanism is already documented in the code: during
the terminal plunge, fixed-step RK4 loses energy catastrophically, and there are no further crossings, so
the crossing-sampled maximum never sees it.

**That is the intended behaviour, and the fix that produced it was correct** — the previous version
evaluated dH on the final mid-plunge state and therefore rejected *exactly* the escaping orbits it existed
to certify. But it has a consequence that was not previously stated:

> **The A1 guard certifies the bound, recorded portion of an orbit and is structurally silent about the
> escape itself** — and escape is the *only* discriminating conjunct in the fire criterion. One of the four
> terminating orbits sampled here integrates its escape at |dH/H| = **1.663e-03, some 17× above the guard
> threshold** the run reports it as passing.

So the guard is inert in two senses: it has rejected nothing (0/599), and it cannot in principle speak to
the quantity that decides `n_fired`. **No claim that "the integration is clean on energy" is made in this
document.** Energy conservation on the recorded arc is established; the accuracy of the escape
determination is not, and is the natural target of the step-size sweep in item 3 below.

*Caveat: the terminating orbits sampled here are the bisected separatrix edges, i.e. marginal by
construction, so the ratios above are not a random sample of the ladder.*

## The estimator's gain depends on frequency — so drift is not comparable across δ

*Added 2026-08-16 from the estimator replacement work, gated in
[PREREG_ESTIMATOR.md](PREREG_ESTIMATOR.md). This is the sharpest instrument result in the item.*

A NAFF-style estimator (continuous maximisation of the Hanning-windowed Fourier amplitude) was built and
gated. **E1 failed as frozen** — its drift floor came out *worse* (1.22e-05 vs 5.17e-06) where the gate
required 10× better. Diagnosing that failure produced the finding.

**NAFF's frequency estimate is 100–10,000× more accurate** than the FFT peak (single tone: 1.98e-07 vs
1.88e-03; three tones: 1.21e-05 vs 1.77e-03) and it *still* scores worse on drift. The reason is the
statistic: `drift = |f₁−f₂|/max(f₁,f₂)`, and the FFT peak's error is a **systematic bias set by the
fractional bin offset**, near-identical in both halves and therefore **cancelling in the difference**.
The incumbent's floor sits 340× below its own frequency error. **The incumbent's floor is low because it
is biased, not because it is accurate — a half-split difference statistic rewards a biased estimator over
an accurate one.**

**Then the response was measured for the first time** (every earlier number in this item is a *noise*
measurement). Injecting known drifts into series whose halves are generated at known distinct frequencies,
with fractional bin offset controlled:

| | FFT gain | NAFF gain |
|---|---|---|
| on-bin | 0.755 | 1.000 |
| quarter-bin | 0.924 | 1.004 |
| **half-bin** | **1.592** | 0.991 |
| three-quarter | 0.895 | 0.993 |
| **spread over 32 offsets** | **0.839** | **0.025** |

> **The incumbent's gain varies by 2.1× with where an orbit's frequency sits in the bin grid.** Two orbits
> with identical true drift and different absolute frequencies do not report the same drift. Different δ
> means different orbital frequencies, means different bin offsets, means different gain — **so drift
> values are not comparable across the ladder, and δ-structure can be manufactured with no physics in it
> at all.** The distortion is worst at low true drift, which is where the ladder lives.

**This is a fifth candidate explanation for δ-dependent structure**, requiring neither chaos, resonance,
integration error, nor sampling geometry. *(Mechanism predicted by quantum before the test, with a stated
falsification condition — FFT gain flat and unity — which did not occur and was not close.)*

**Note the incumbent still wins on SNR**: 0.909/5.167e-06 = 175,840 against NAFF's 1.000/1.219e-05 =
82,032, a factor 2.1. **SNR is the wrong figure of merit here.** It ranks detectors for *is there a signal,
at one setting*; every G3 claim is a **comparison across δ**, for which the operative property is **gain
stability along the comparison axis**. The structural reason, and it is decisive: **the floor contributes
statistical error, which averages down as 1/√N; gain variation contributes systematic error along the
comparison axis, which does not average down at any N.** Setting them equal gives a crossover true-drift of
`0.59·d = 5.167e-06` → **d ≈ 8.8e-06 — below every drift value in the ladder.** At d = 1e-03 systematics
beat statistics by ~110× in a *single* measurement.

⇒ **E1 was gated on the wrong property twice over**: on noise alone (which selects for deafness — an
estimator returning zero has a perfect floor), and then on SNR (which would have chosen the distorting
instrument). **Gate an instrument on the property the claim depends on.** A high-SNR instrument with
parameter-dependent gain is *more* dangerous than a noisy one for cross-parameter work, because it
produces confident, reproducible, wrong structure.

## What is and is not established

**Established.** §106's δ=2 layer reproduces at x₀ = 8.03693 and 8.04093 (G3b). Two orbits, both
signatures, 988× above their own floor — that regression is the one solid positive in this item, and it
held across the whole rerun. Separately: **the drift conjunct is uninformative; the escape conjunct is
underpowered; the A1 guard is inert; and the estimator's noise floor is set by FFT peak variance.**

**Not established.** **δ\* = 1.1 is not supported.** Neither is any statement about the shape of the
boundary, its monotonicity, or the scaling of the signal — the quantity in which "scaling" would be
measured does not vary with the physics. Earlier working notes in this campaign described the boundary as
**"non-monotonic"**; that phrasing asserts more than the data carries and is **withdrawn**. Whether ZV
metrics near δ=1 have a thin chaotic layer remains **open**, exactly as before this run.

## What a real attempt needs, in priority order

0. **MORE ORBITS — and this is the cheapest route to a conclusive item, ahead of every instrument fix.**
   Two power questions were previously conflated here. The **step-size** question (does h shift the escape
   *fraction*?) is brutal: ~1141 orbits/arm for a halving. The **boundary** question (is 4/100 different
   from 0/99?) is far easier — at **n ≈ 200–300 per δ** one expects ~8 vs 0, **p ≈ 0.007**. So 2–3× the
   current orbit count, on existing machinery, would settle whether the boundary exists at all. **If it
   does not survive that, the estimator and integrator work are moot; if it does, both become worth doing
   on an effect known to be real.** *(Sequencing contributed by quantum.)*

   ⚠️ **But it must run through the corrected estimator, not before it** — and that is structural, not a
   preference. More orbits shrink only the *statistical* error; the gain variation documented above is
   *systematic* along the very axis being compared and does not average down at any N. **Running 200–300
   orbits per δ on the FFT statistic would deliver a beautifully significant measurement of a quantity
   whose gain varies 2.1× across the comparison axis — worse than doing nothing, because an underpowered
   null is honest and reads as inconclusive, while a well-powered distorted result is confident,
   reproducible, and gets believed.**

1. **Replace the drift estimator — for gain stability, not for floor.** NAFF's gain is flat to 2.5% where
   the incumbent's varies 2.1×; its floor is *worse* and its SNR is 2.1× worse, and neither of those is the
   property a cross-δ claim depends on. Do **not** re-gate this on floor or on SNR.
2. **Re-run the control at n ≈ 100** to match the ladder. δ=1.0 is the only δ at n=50, and every
   absolute-scale statement leans on that row. **And recompute the synthetic null at the orbits' actual
   observed frequencies** — the published null was sensitive to an assumed frequency range by 17× and its
   percentiles are withdrawn.
3. **RK4 step-size sweep on δ=1.0, for the drift excess.** Energy and phase are different failure modes;
   `drift()` measures phase, and the h⁴ energy scaling above says nothing about it. Truncation-driven
   excess should fall ~16× per halving.

   **And on the escapes — but judged on the ensemble fraction, never on individual verdicts.** Escape is
   the only discriminating conjunct and it is decided in the plunge, where energy error reaches 1.7e-3.
   ⚠️ **Near a separatrix the escape basin boundary is generically fractal, so individual orbits flipping
   verdict under a change of h is EXPECTED at any step size — that is the dynamics, not a defect.**
   Judging on flips would condemn a working detector. The statistic is the escape *fraction* at h vs h/2
   with binomial errors: stable fraction ⇒ `n_fired` is sound despite flips; systematically moving
   fraction ⇒ artifact. **Note from the power table above that at ~100 orbits per arm this test can only
   resolve near-total signal loss**, so it must be run at ≫100 orbits or reported as inconclusive.
   *(Fractal-basin correction and the fraction statistic contributed by quantum, relayed 2026-08-16;
   it corrects an earlier draft of this item that proposed the individual-flip criterion.)*

3b. **A narrow, well-aimed integrator fix — escape segment only.** The both-ways measurement above locates
   the energy failure precisely: fine on the bound arc (1.1–1.3×), blowing up in the terminal plunge. That
   is the known failure mode of fixed-step methods — the orbit accelerates, the natural timescale
   collapses, and constant h stops resolving it. The indicated cure is **adaptive stepping or a
   time-transformed / regularised scheme through the plunge** (the Wu–Deng–Pan time-transformation
   literature, `[asserted, unverified]` per **L10**), **not** extended precision and **not** symplectic
   integration for its own sake — neither touches this. This is a much smaller build than a general
   integrator and it is aimed at the only conjunct that discriminates.
4. **Persist crossing times** so non-uniform sampling geometry can be tested — the most likely explanation
   for the residual excess, and untestable from the current records.
5. **Report escaping *fraction* over a fixed phase-space volume**, not a binary per-orbit outcome. Near a
   separatrix the basin boundary is generically fractal, so a single orbit's outcome is not stable; an
   ensemble fraction is.
6. **Then, and only then, the resonance hypothesis** — that chaos onset is non-monotonic in δ via low-order
   resonances. It is the best physical explanation on offer, but rotation number is estimated by the same
   machinery currently under suspicion, so it would inherit the problem. Its pre-registered two-stage form
   and falsification conditions are in [PREDICTIONS_ROUND12.md](PREDICTIONS_ROUND12.md).

## Honest scope

- **Zero novelty in the physics.** ZV non-integrability is ansatz §97/§98; the δ=2 layer is §106 and
  Lukes-Gerakopoulos PRD **86**, 044013, `[asserted, unverified]` on our side per **L10**.
- **The kill is uninteresting on its own and was pre-registered as such** — δ=1 is Schwarzschild, so a
  boundary must exist by continuity. The pre-registration named the boundary and the scaling as the
  deliverable, and this run does not deliver them.
- **This is a statement about our instrument at this resolution, not about the spacetimes.** By
  [A2's taxonomy](../A2_wall_audit/FINDINGS.md) it is **species-1 (precision)** with a *named* crossing
  point: the estimator, not the compute budget.
- **Data loss.** `main()` carries forward only `scan` and `partial`, never `orbits_archive`
  (`code/g3_overnight.py:281-286`), so both resumes dropped the per-orbit archive. 498 orbits for
  δ=1.7/1.5/1.3/1.2/1.1 were recovered from git HEAD; **δ=1.05's 100 orbits are lost**; δ=1.0 and δ=2.0
  per-orbit data were lost on an earlier run. **The δ=1.0 loss is the expensive one** — it is the null
  distribution every argument here would otherwise be tested against.
- Bridge-solo; imports ansatz read-only (`_zv_invariant`, `poincare`); ansatz unmodified. Analysis in this
  document beyond the run's own output was performed on recovered per-orbit records and on synthetic
  series, with no change to the scan or its gates.

## History — the 2026-07-26 attempt

The first run returned **UNDECIDED(search)**: `drift()` was FFT-bin-quantized to 2/N = 0.0333, above the
0.027 signal being hunted, so every δ returned an identical 6.67e-2. The ADDENDUM upgraded the estimator to
parabolic sub-bin interpolation, moved the hunt to the plunge separatrix, and raised the budget to §106's
(N=200, x₀ step 0.002). **That upgrade worked** — the quantization is gone and δ=2.0 now reproduces. It
replaced a floor set by the bin grid with a floor set by peak-estimation variance, which is better but is
still a floor, and is still above the physics at seven of nine δ.

Three bugs found and fixed across the runs, all of the same species — *a silent failure returning a
plausible number*: exactly-planar orbits from an inverted `p_x = 0` condition; `find_separatrix` returning
a grid edge without bisecting; and the A1 guard evaluated on the final mid-plunge state, which rejected
**exactly the escaping orbits it existed to certify**.

## Inputs & artifacts

`code/g3_overnight.py` · `results/g3_overnight.json` · `results/overnight.log` ·
[PREDICTIONS_ROUND12.md](PREDICTIONS_ROUND12.md). Attacks **G3** (v1 ledger, Tier G): **KILLED as stated,
boundary UNMEASURED.**
