# G3 — third-party predictions, filed BEFORE δ=1.02 landed

*New file, purely additive. [PREREGISTRATION.md](PREREGISTRATION.md) and its ADDENDUM are **unmodified** —
the frozen gates G3a–G3d are untouched by anything here. This records predictions made by sister sessions
about a result that had not yet been computed, so they can be scored rather than rationalised.*

## Ordering evidence — why this file is genuinely pre-data

Recorded **2026-08-15T23:37:23Z**, while `g3_overnight.py` (PID 52691, 25 min elapsed) was mid-run on
δ=1.02, in stage 2.

- `results/overnight.log` is **137 lines** and contains **zero** lines matching `^    1.02 |` — the δ=1.02
  result row has not been written.
- `results/g3_overnight.json` md5 = `55211f605c86727e025104c77b0d5d70`; its `scan` key holds 8 δ, and
  `1.02` is still under `partial`, not `scan`.

Anyone can check the run's own log ordering against this file's commit.

## ① quantum's prediction (relayed via the repo-context session)

> **δ=1.02's escape conjunct will be SILENT, and that is physics, not artifact.** δ=1.02 and δ=1.05 sit
> adjacent to the integrable point; near-integrable ⇒ KAM tori almost entirely intact ⇒ the chaotic layer is
> exponentially thin in the perturbation ⇒ escapes rare-to-absent. Quiet there is the predicted behaviour.

**Falsification condition, in their words:** *"If δ=1.02 FIRES while 1.05 is silent, my reasoning is wrong
and you should discount this whole section."*

**Consequence if correct:** δ=1.05's silence is what near-integrability looks like, so it should not be
grouped with δ=1.5 as one phenomenon. The anomaly list shrinks to **δ=1.5 alone**, and "non-monotonic
boundary" must be restated as **"one interior silent point."**

**Bridge note, also pre-data:** this prediction is *weakly* stated in one respect — δ=1.05 and δ=1.02 are
already known to be silent-so-far, and PREREGISTRATION §"structural reason" itself predicts the layer must
shrink to zero width as δ→1⁺ by continuity. So a silent δ=1.02 confirms something the pre-registration
already expected. The prediction's real content is the **grouping claim** (1.05 ≠ 1.5), not the silence.
Scored on that basis.

## ② The absolute-scale observation (accepted, and it does not depend on δ=1.02)

**ZV at δ=1 IS Schwarzschild, which is integrable — its true frequency drift is exactly zero.** Therefore
everything the instrument reads at δ=1.0 is *its own noise floor*, in absolute units:

| δ | max drift | ÷ control | note |
|---|---|---|---|
| **1.00** | 8.685e-03 | **1.00** | control — TRUE drift is 0, so this is pure instrument noise |
| 1.05 | 6.073e-03 | **0.70** | **below the noise** |
| 1.10 | 7.190e-03 | **0.83** | **below the noise** |
| 1.50 | 1.329e-02 | 1.53 | |
| 2.00 | 2.859e-02 | 3.29 | |
| 1.20 | 5.981e-02 | 6.89 | |
| 1.30 | 8.596e-02 | 9.90 | |
| 1.70 | 1.252e-01 | 14.42 | |

**This is stronger than any fired/silent analysis because it does not use the labels at all.**

**And it is understated.** The control ran **50** clean orbits against ~100 for every treatment δ. `max` is
an order statistic, so E[max] grows with N: the control's noise is measured from *half* the sample and is
therefore **biased low**. Matched, the control's noise floor would rise, pushing more δ under it.

## ③ Correction to the bridge's own KS result (accepted)

The bridge ran two-sample KS on log10 drift across the five settled matched δ, grouped by fired count, and
found no pair separating (smallest p = 0.039 over 10 pairs, Bonferroni α = 0.005).

**The relayed caveat is correct and is accepted:** fired count *is* escape count, which this same analysis
showed has no counting statistics (0–4 escapes per ~100 orbits). **Testing drift against a noise label
cannot separate, even for a perfect detector.** So that result establishes *drift does not predict escape* —
it does **not** establish *drift carries no chaos information*. The comparison that would settle it is
against the integrable control, whose per-orbit data was lost (see below). FINDINGS must state it the
narrower way.

## ④ Open, and NOT accepted without checking

- **tabula's 1e6× calibration** (`132_zv_gamma_metric.py:161-163`) is a threshold on **C-drift**, a different
  quantity from this item's **frequency drift**. Transferring a numerical threshold between two different
  metrics is the same error already caught once this round (dividing ratios that have different
  denominators). The *qualitative* warning — that a fixed absolute threshold mislabels weakly-perturbed KAM
  orbits — stands and is worth heeding; the **number 1e6× does not transfer** until someone shows the two
  drifts are commensurate. `[asserted, unverified]` per **L10**.
- **quantum's finite-difference-Christoffel mechanism** names `geodesic_chaos.py` at h=1e-4. **G3 does not
  import that module.** `g3_overnight.py` imports only `_zv_invariant.metric` and
  `poincare.{_rk4, p_on_shell, H_value}`. The mechanism may still be right, but it must be demonstrated in
  *this* code path before it explains δ=1.0's noise. `[asserted, unverified]`.

## ⑤ Data loss, disclosed

`main()` rebuilds its state dict and carries forward only `scan` and `partial` — it never copies
`orbits_archive` (`code/g3_overnight.py:281-286`). Resuming the run on 2026-08-15 therefore dropped the
per-orbit archive.

- **Recovered** from git HEAD: 498 orbits for δ=1.7/1.5/1.3/1.2/1.1.
- **Lost:** δ=1.05's 100 orbits (uncommitted working-tree only). Summary row survives.
- **Already lost on an earlier run:** δ=1.0 and δ=2.0 per-orbit data.

The δ=1.0 loss is the expensive one: it is exactly the null distribution ③ says is needed, and the row ②
depends on. This is the same vacuous-carry-forward species the item has produced twice before.

## Scoring — completed 2026-08-16, δ=1.02 landed

δ=1.02 result row: `1.02 | [4.00808, 9.84386] | 101 clean | floor 1.08e-05 | max drift 1.78e-02 |
101 distinct | esc? False | fired 0 [2291.0s]`.

### quantum's prediction: **CONFIRMED — and it carries little weight**

δ=1.02's escape conjunct was **silent** (0 escapes, 0 fired). The falsification condition — *"if δ=1.02
FIRES while 1.05 is silent"* — was **not** triggered. Scored honestly, three discounts apply, two of them
stated in this file before the data:

1. **The pre-registration already predicted it.** PREREGISTRATION's own continuity argument says the layer
   must shrink to zero width as δ→1⁺. Silence at δ=1.02 confirms what the frozen document expected.
2. **The statistic has no power to detect the alternative.** Escape counts across the ladder are
   0,0,0,1,2,4,0,3,2 per ~100 orbits. **Superseding the Poisson estimate first used here** (P(0) = 1.8%
   at a true rate of 4/100), the correct instrument is an exact test on the actual counts, and it is
   harsher: **δ=1.3 (4/100) vs δ=1.5 (0/99) gives Fisher exact p = 0.121** — the conjunct cannot separate
   the ladder's own extremes, and all six exact binomial intervals overlap. δ=1.1 (1 escape) versus
   δ=1.02 (0) is far weaker still. **A prediction of "silence" cannot be informative when the instrument
   cannot separate 0 from 1** — and detecting even a halving of the escape rate would need ~1141 orbits
   per arm against the ~100 run. See [FINDINGS.md](FINDINGS.md) for the full power table.
3. **The grouping claim — its actual content, per the pre-data note above — is contradicted.** If δ=1.05
   and δ=1.02 are quiet *because* near-integrability makes the layer exponentially thin, drift should also
   be smallest there. It is not. **δ=1.02, the δ closest to integrable, has max drift 1.78e-02 — larger
   than δ=1.05 (6.1e-03), δ=1.1 (7.2e-03) and δ=1.5 (1.33e-02), and 2.05× the integrable control.**

**Verdict: prediction confirmed, hypothesis not supported.**

### G3d's own pre-registered prediction: **FALSIFIED**

PREREGISTRATION G3d predicted species-1 (precision), with the evidence being *"max-drift declining smoothly
toward the floor as δ → 1, rather than vanishing abruptly,"* and noted that a non-smooth pattern *"would be
a genuine surprise."* Observed, ordered by δ:

| δ | 1.0 | 1.02 | 1.05 | 1.1 | 1.2 | 1.3 | 1.5 | 1.7 | 2.0 |
|---|---|---|---|---|---|---|---|---|---|
| max drift | 0.0087 | **0.0178** | 0.0061 | 0.0072 | 0.0598 | 0.0860 | 0.0133 | 0.1252 | 0.0286 |

Not a smooth decline in either direction. **The prediction is falsified.** But the reading proposed here is
*not* that the surprise is physical — see below.

### The line that survives every objection raised this round

Ranked by max/median, the statistic the fire rule actually uses:

```
3678  δ=1.2   fired=2
2980  δ=1.0   fired=0   <== INTEGRABLE CONTROL, true drift exactly 0
2699  δ=1.7   fired=3
1656  δ=1.02  fired=0
1639  δ=1.3   fired=4
 988  δ=2.0   fired=2
 747  δ=1.1   fired=1
 511  δ=1.05  fired=0
 455  δ=1.5   fired=0
```

**Eight of nine δ sit at or below the integrable control.** Only δ=1.2 exceeds it, by 23%. δ=1.0 is
Schwarzschild; its true frequency drift is exactly zero. No null model, no fired/silent labels, and no
methodology is required to read that table.

### Supporting results from this round

- **Drift carries no information about the physics.** Two-sample KS across the five settled matched δ:
  smallest p = 0.039 over 10 pairs (Bonferroni α = 0.005) — no pair separates; δ=1.3 (4 fired) vs δ=1.5
  (0 fired) gives p = 0.503. Regrouped against the *physical* knob |δ−1| to remove the noise-label
  objection: Spearman ρ = +0.089 over 498 pooled orbits (<1% of variance), Kruskal–Wallis p = 0.265.
- **The per-δ "floor" is estimator variance, not dynamics.** `drift()` fed synthetic quasiperiodic series
  with *true drift identically zero* — no metric, no integrator, no force — returns median 4.9e-06 against
  the run's δ=1.0 floor of 2.9e-06. Reproduced within a factor of 2 with no dynamics at all.
- **There is a residual excess above pure-estimator noise.** Null max/median at matched n: median ~208,
  95th ~407, max ~750–1001 over 2000 replicates. Every δ *including the control* exceeds it. Source not
  identified; the synthetic assumes uniform sampling, so ~200 is a lower bound.
- **The A1 integration guard is inert. 0 rejections out of 599 orbits** (dH range 1.67e-13 … 2.16e-12,
  guard 1e-4 — 4.6×10⁷ margin). It has never rejected anything and certifies nothing. Fourth instance of
  the vacuous-gate family in this item, after run 1's dead drift conjunct, run 2's zero-orbit control, and
  run 2's jointly-silent conjunction.
- **Drift correlates with |ΔH| (pooled ρ = +0.552, p = 4e-41) but the proposed mechanism fails**: max |ΔH|
  is 2.16e-12, seven orders below the guard; drift vs distance-to-separatrix gives ρ = +0.007, p = 0.87;
  and the loudest orbit in the ladder has *below-median* |ΔH|.

### Data loss, recurred

The `orbits_archive` carry-forward bug (`code/g3_overnight.py:281-286`) fired again on this run. The
completed file now archives **δ=1.02 only**; δ=1.7/1.5/1.3/1.2/1.1 were dropped a second time. Those 498
orbits are recoverable from git HEAD and were re-banked before the run; **δ=1.05's 100 orbits remain lost.**

### What this does not decide

G3a and G3b are recorded as the run reports them (control did not fire; §106's δ=2 layer reproduced at
x₀ = 8.03693, 8.04093). **The G3c boundary δ\* = 1.1 and the G3d species classification are not supported
by this evidence**, because the drift conjunct is uninformative and the escape conjunct has no counting
statistics. Gates remain decided by [PREREGISTRATION.md](PREREGISTRATION.md); this file records what the
numbers will and will not carry.
