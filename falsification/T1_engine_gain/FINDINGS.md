# T1 — Findings: the gain is FLAT along α. §94's contrast is not a sensitivity gradient.

*Run 2026-08-21 for tabula (SpaceTime / curvature). Gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md)
before code. Independent implementation from tabula's written spec; **their code was not read**, which is
the property they said they could not manufacture for themselves.*

## Result in one line

**T1b = FLAT.** Gain varies at most **1.74×** across α ∈ {0,1,2,3,4}, under the frozen 3× bar, **with no
ordering on the {0,1,3}-vs-{2,4} split.** ⇒ **§94's emit/certify contrast is not explained by a sensitivity
gradient along α.** The certificate survives on this axis.

## The gates

| gate | result |
|---|---|
| **T1a** — plant recovered at the integrable points | **PASS** — overlap 0.998–1.000 at every α |
| **T1b** — gain flatness (decisive) | **FLAT** — max/min ≤ 1.74×, no {2,4} gradient |
| **T1c** — detection threshold vs α | **FLAT** — same threshold at every α |
| **T1d** — confound check | ⚠️ **the plant ranks FIRST** — see below |

## T1b — the numbers

gain = (plant's true within/total ratio) / (ratio the readout recovers), out-of-sample on held-out
**trajectories**. Faithful = 1.00.

| ε | true ratio | α=0 | α=1 | α=2 | α=3 | α=4 | max/min |
|---|---|---|---|---|---|---|---|
| 1e-4 | 1.0e-08 | 1.085 | 1.659 | **1.199** | 1.550 | **1.027** | 1.62× |
| 1e-3 | 1.0e-06 | 0.899 | 1.058 | **0.937** | 1.561 | **0.912** | 1.74× |
| 1e-2 | 1.0e-04 | 0.628 | — | **0.873** | 0.731 | **0.504** | 1.73× |

**No gradient in the feared direction.** At ε=1e-4 the certified points α=2,4 are the *most* faithful in
the set (1.199, 1.027 against 1.659 and 1.550 at the islands). At ε=1e-2, α=4 is worst (0.504) but α=2 is
**best** (0.873) — scatter, not a gradient. If sensitivity degraded at the certified points, α=2 and α=4
would move together. They do not.

## T1c — detection threshold does not move with α

Max overlap on the plant (≥0.9 = recovered):

| ε | α=0 | α=1 | α=2 | α=3 | α=4 |
|---|---|---|---|---|---|
| 0 | 1.000 | 0.998 | 1.000 | 1.000 | 1.000 |
| 1e-3 | 0.995 | 0.990 | 0.999 | 1.000 | 1.000 |
| 1e-2 | 0.985 | **0.724** | 0.981 | 0.977 | 0.947 |
| 1e-1 | 0.066 | 0.017 | 0.095 | 0.391 | 0.093 |

Threshold sits between ε=1e-2 and 1e-1 at **every** α. The one early failure is **α=1 — an integrable
island, not a certified point.** If anything the islands are marginally weaker, which is the opposite of
the hypothesis.

## ⚠️ T1d — the readout ranks a meaningless constant FIRST

The plant is a **per-trajectory constant with no dynamical meaning whatsoever**. It comes back at
**rank 0** at α = 0, 2, 3, 4 (rank 1 at α=1) — i.e. **above every dynamical direction**, at ratios of
1e-26 to 1e-27.

**This independently reproduces tabula's own confound-planting result**, on a readout built from their
spec by someone who had not read their code. It says the readout as specified **cannot distinguish a
genuine conserved quantity of the dynamics from a per-realization constant** — both are "conserved along
each trajectory, varying across the ensemble," and nothing in the within/total criterion separates them.

That is not a defect this measurement introduces; it is the structural property that makes tabula's C4
clause necessary (*the candidate must be a function of the dynamical state*). **T1's flat-gain result is
therefore a statement about the readout's generic sensitivity, not specifically about its sensitivity to
dynamical invariants** — see the caveats.

## Honest scope — what this does NOT establish

- **The plant is dynamics-independent by construction.** A gain gradient that affected only *dynamical*
  features would not show up here. This measures whether the readout's generic sensitivity varies with α;
  it does not measure whether its sensitivity *to dynamical invariants specifically* varies with α.
  **That is the sharper question and this run does not answer it.** Answering it needs a plant that is a
  genuine function of the state and conserved by the α-dynamics — which is the same object §94 is looking
  for, so it may be circular in the same way tabula showed my Candidate-B offer was.
- **My readout is not tabula's.** T1a shows mine works; it does not show mine is theirs. If their
  implementation differs structurally, its gain profile could differ. Disagreement between us would be
  informative and none has surfaced — but "no disagreement" is weak evidence next to "independently
  reproduced."
- **Shell integrity is mildly α-dependent**: median |ΔH|/H runs 6.04e-4, 6.08e-4, 7.70e-4, 8.85e-4,
  9.90e-4 for α = 0…4 — a systematic **1.6× rise with α**. Small, but it is a real α-gradient in the
  substrate. It should not touch a dynamics-independent plant, and the flat gain is consistent with that,
  but a *dynamical* plant would sit on top of it.
- **α=1 returns small negative ratios** (−1.7e-19, −9.1e-17), a conditioning artifact of the generalized
  eigenproblem at machine precision. They are zeros; reported rather than clipped.
- Pinned shell E₀ = 8 — deliberately, per the pre-registration, because **that is the configuration the
  certificate runs in.** tabula advised varying E₀; the synthetic plant carries its own across-ensemble
  variance, so it is detectable without that, and varying E₀ would have measured a different setup's gain.

## Inputs & artifacts

`code/t1_gain.py` · `results/t1_gain.json`. 70 trajectories per α, velocity-Verlet, dt=0.02, 2500 steps,
150 burned, train/test split over trajectories. Requested by tabula; bridge-solo.
