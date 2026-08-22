# G3 item 0 — The boundary is NOT SUPPORTED, and the FINDINGS headline is WITHDRAWN

*Run 2026-08-22, ~3.5 h. Gates frozen in [PREREG_BOUNDARY.md](PREREG_BOUNDARY.md) before code, including
the two-arm control commitment made before either arm reported.*

## B1 — the decisive test

| δ | escapes | rate | exact 95% CI |
|---|---|---|---|
| 1.3 | **2/312** | 0.0064 | [0.0008, 0.0230] |
| 1.5 | **3/317** | 0.0095 | [0.0020, 0.0274] |

> **Fisher exact p = 1.0000 → BOUNDARY NOT SUPPORTED.**

The frozen rule: *p ≥ 0.05 ⇒ not supported, and at this n that is a genuine null, not an underpowered
one — δ\* = 1.1 should be withdrawn outright rather than left standing as "unsupported."*

**And the direction reversed.** The previous run had δ=1.3 at 4/100 and δ=1.5 at 0/99 — the contrast the
whole boundary rested on. At ~3× the orbits the *silent* δ has the **higher** rate. That is what pure
counting noise looks like when you give it room: not a shrinking effect, a sign flip.

**δ\* = 1.1 is dead.** It rested on one orbit escaping at δ=1.1 and none at δ=1.05, and the same statistic
at 3× the sample cannot distinguish the ladder's own extremes at any threshold whatsoever.

## B3 — drift is still uninformative, now at triple the sample

| estimator | KS p, δ=1.3 vs δ=1.5 |
|---|---|
| FFT | **0.9944** |
| NAFF | **0.8840** |

This was the pre-registered danger: *a null at low n and a signal at high n is what an underpowered test
looks like, and I should not be able to dismiss that by having asserted it earlier.* Tripling n moved it
from p=0.503 to p=0.994. **The drift conjunct carries no information, and that now survives its own
power check.**

## B4 — the A1 guard is inert, confirmed

`dH` range **1.945e-13 … 1.035e-12** against `DH_MAX = 1e-4`. **0 rejections of 629 orbits**, worst orbit
~10⁸ below threshold. Identical verdict to the original run at 599 orbits.

## ⚠️ THE FINDINGS HEADLINE IS WITHDRAWN

[FINDINGS.md](FINDINGS.md) leads with: *"eight of nine δ sit at or below the integrable control."* That
rested on the control's max/median of **2980**, measured at **n=50** — the only δ in the ladder not run
at ~100.

Re-measured properly, both arms:

| control arm | n | median drift | max | **max/median** |
|---|---|---|---|---|
| A — matched orbit count | 320 | 7.743e-06 | 9.714e-03 | **1254** |
| B — matched x₀ spacing | 160 | 7.020e-06 | 8.691e-03 | **1238** |
| *original* | *50* | *2.915e-06* | *8.685e-03* | ***2980*** |

**The original control was inflated ~2.4× by small-sample bias in the median.** Against the corrected
value, only **4 of 8** deformed δ sit at or below it:

```
ABOVE control:     δ=1.02 (1656)   δ=1.2 (3678)   δ=1.3 (1639)   δ=1.7 (2699)
at/below control:  δ=1.05 (511)    δ=1.1 (747)    δ=1.5 (455)    δ=2.0 (988)
```

**The two arms agree exactly — 4 above, 4 below in both.** So the frozen commitment is satisfied in its
letter: the arms did not disagree, and the result is a fact about the spacetimes rather than about my
matching choice. **But they agree that the headline is false**, which is an outcome the pre-registration
did not anticipate: it planned for arms disagreeing, not for both arms refuting.

**This is exactly the defect ansatz and quantum flagged hours before it was measured** — the control was
structurally unmatched (one separatrix band against two, n=50 against ~100, smallest median in the run by
3.3×) and I had recorded that as a caveat rather than as something to fix. It was fixable, and fixing it
falsified the headline.

## What survives, and it is most of the substance

The headline was the *rhetorically* strongest claim, not the load-bearing one. Untouched:

- **The drift conjunct carries no information** — pass fraction flat at 35–43% across every δ, KS
  separating no pair at n≈100 *or* n≈315, Spearman ρ=+0.089 against the physical knob.
- **Drift values are not comparable across δ** — gain varies 2.157× with fractional bin offset, and
  longer records do not fix it (16× data, flat to 0.04–1.3% at fixed offsets).
- **The A1 guard is inert** — 0 of 629.
- **The escape conjunct has no counting statistics** — and B1 now demonstrates that directly rather than
  by power calculation.
- **§106's δ=2 layer reproduces** — the one solid positive in the item.

## Two methodological failures this run exposed, both mine

**① A pre-registration that enumerates how a result could be AMBIGUOUS is not the same as one that states
how it could be WRONG.** The frozen commitment was: *the headline must hold under matched-n AND
matched-spacing; withdrawn if the arms disagree.* Both arms agreed — 4 above, 4 below, exactly — **and
they agreed the headline was false.** The commitment was satisfied in its letter and the finding died
anyway, because the outcome that occurred had no rule attached to it. Enumerating more ways to be
*undecided* never produces the clause you needed. *(Named by tabula.)*

**② A caveat is where you put the thing you have decided not to act on.** [FINDINGS.md](FINDINGS.md)
records the control as structurally unmatched — one separatrix band against two, n=50 against ~100,
smallest median in the run by 3.3× — and lists "re-run the control at n ≈ 100" as forward-look item 2.
**ansatz and quantum both flagged it hours before it was measured.** It sat as an honest note while the
headline built on it stood, and fixing it took one afternoon and falsified the claim.

> The record was honest and the behaviour was unchanged. **Writing it down feels like handling it.**

That is the same move as burying an exclusion in smaller words at the bottom, and it is worth more as a
warning than the boundary result is as a finding: *this item spent two runs establishing that an
unmatched control invalidates a comparison, while its own unmatched control sat in a caveat.*

## The item's verdict, restated

**G3 is KILLED as stated** (δ=1.02, 1.05, 1.5 are non-integrable and silent). **The boundary δ\* = 1.1 is
WITHDRAWN, not merely unsupported.** The scientific content is a negative instrument result: a detector
whose drift conjunct carries no information and whose escape conjunct cannot separate its own extremes at
3× the sample, guarded by a gate that has never once fired.

---

## Reproducing every number above

```bash
python code/gate_boundary.py
```

16 assertions over the banked JSONs — the B1 counts, the Fisher p, both KS p-values, the guard's
0/629, and the control re-measurement at 1254/1238 that withdrew the FINDINGS headline. Artifact:
[results/gate_boundary.log](results/gate_boundary.log).

This gate was written **after the fact**, prompted by quantum's audit question — *for every number in a
docstring or writeup, can the committed code produce it?* Until 2026-08-22 the answer here was **no**.
The scans were on disk from the start; the summary statistics quoted from them were computed in
`python -c` one-liners and existed only in this file. A withdrawal that a reader cannot re-derive from
the repo is worse than an unreproducible claim: the retraction itself becomes something to take on
trust.
