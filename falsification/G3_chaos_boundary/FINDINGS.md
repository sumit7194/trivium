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

Integers between 0 and 4, out of ~100 orbits each. At a true rate equal to the largest observed (4/100),
Poisson gives **P(observe 0) = 1.8%** and **P(≤1) = 9.2%**. δ=1.1 (1 escape) versus δ=1.5 (0) is not a
distinguishable difference, and even 4-vs-0 is ~2σ on a single uncorrected comparison across eight δ.

**δ\* = 1.1 rests on one orbit escaping at δ=1.1 and none at δ=1.05.** That is not a boundary; it is a
coin landing once.

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

**A residual excess above pure-estimator noise does exist and is unexplained.** Null max/median at matched
n, 2000 replicates: median ~208, 95th ~407, max 750–1001. Every δ **including the control** exceeds it
(δ=1.0: 2980, p < 0.001). Candidates, none yet tested: non-uniform section sampling (crossings are uniform
in index, not time, which the synthetic did not model); RK4 phase error over ~1.2M steps; and the control's
n=50 conditioning. **The synthetic assumes uniform sampling, so ~200 is a lower bound on true noise.**

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

1. **Replace the drift estimator.** The floor is peak-estimation variance; the fix is a proper
   frequency-analysis method (NAFF/Laskar) or far longer records — not a better integrator.
2. **Re-run the control at n ≈ 100** to match the ladder. δ=1.0 is the only δ at n=50, and every
   absolute-scale statement leans on that row.
3. **RK4 step-size sweep — on δ=1.0 for the drift excess, and on the escapes.** Energy and phase are
   different failure modes; `drift()` measures phase, and the h⁴ energy scaling above says nothing about
   it. Truncation-driven excess should fall ~16× per halving. **Sweep the escaping orbits too**: escape is
   the only discriminating conjunct, it is decided in the plunge where energy error reaches 1.7e-3, and if
   an orbit's escape verdict changes with h then `n_fired` is a step-size artifact.
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
