# R7 — Pre-registration: is O4 a threshold artifact, or a real obstruction? (adopting the literature's instrument)

*Frozen 2026-07-26, before `code/r7_threshold.py` is written or run. Falsification v2+, Tier R — precision
hygiene on a banked finding, the same character as R4. Prescribed by [A2](../A2_wall_audit/FINDINGS.md)'s
taxonomy: M6's prior-art gate produced a **species-1 (precision/instrument) wall**, whose prescription is
"keep pushing — upgrade the instrument." R7 is that upgrade, run as a test rather than assumed.*

## Background — and the claim of ours that is on the line

**R2** found **O4**: a degree-6 polynomial **falsely emitted** on pendulum orbits (σ_min/σ_max = 2.7×10⁻⁷,
under our hand-set τ_rel = 10⁻⁶) by *approximating* the transcendental invariant, with no true polynomial
invariant in its span. tabula reproduced it independently at degree 8 (in-sample 9.9×10⁻⁷, crossing the same
line; held-out 5.6×10⁻⁶).

**M6's prior-art sweep asserted, today, that "O4 is not an obstruction we discovered — it is our fixed
τ_rel = 1e-6 being the wrong kind of threshold," and that a noise-calibrated cutoff would "dissolve it
rather than guard against it."** That assertion was made from reading the literature, **not from running
anything.** R7 tests it. If it fails, M6's FINDINGS is wrong on that point and gets amended.

## The three upgrades being adopted (from M6's sweep)

1. **Noise-calibrated cutoff** — Oellerich & Emelianenko ([arXiv:2403.04889](https://arxiv.org/abs/2403.04889),
   Cor. 4.2): `σ_cutoff = √(N·p) · ‖ε‖^{2/3}_max`, replacing a hand-set relative floor.
2. **Spectral-gap library selection** — choose the library maximising `δ = σ_{j−1} − σ_j` rather than by hand.
3. **Constancy-gate / diversity guard** — Ray 2026 ([arXiv:2603.20474](https://arxiv.org/abs/2603.20474));
   here realised as a **held-out score**: derive the null vector on training orbits, score it on orbits with
   different initial conditions.

## Frozen method decisions (made before seeing any number)

- **Noise estimate ε — measured, not guessed.** Our orbits are synthetic, so "noise" is *integrator error*.
  Build the design matrix twice, from a `dt` run and a sample-matched `dt/2` run, and take
  `ε = max |M_fine − M_coarse|` entrywise. This is a **direct measurement of the perturbation to the design
  matrix**, independent of the invariant under test — no circularity.
- **Column normalisation.** The design matrix is column-normalised (unit 2-norm after per-orbit centring)
  before SVD — standard SINDy practice, and *necessary here*: a degree-6 library has wildly larger column
  scales than a degree-2 one, so absolute σ's are otherwise incomparable across libraries. **Both normalised
  and unnormalised numbers are reported**; the normalised one is primary.
- **Held-out split.** 6 orbits → 4 train / 2 test, test orbits drawn from the same distribution but unseen.
  Score `‖M_test c‖ / ‖M_test‖` with `‖c‖ = 1`, `c` = right singular vector of the training σ_min.
- All orbits, systems and initial-condition ranges are **identical to R2's** (pendulum `x₀ ∈ [1.6, 2.8]`,
  `p₀ ∈ [−0.3, 0.3]`, Yoshida-4, dt = 0.01, n = 2000), so O4 is reproduced, not re-created.

## Frozen gates

- **R7a — regression (the upgrade must not break true positives).** Under the new criterion, the known-true
  cases must still **EMIT**: harmonic in poly(2) (R2: 4.6×10⁻¹⁵) and pendulum in poly(4)+cos (R2: 2.2×10⁻¹²).
  **A "fix" that rejects true invariants is not an upgrade** — if R7a fails, the upgrade is rejected outright
  and the remaining gates are void.
- **R7b — the O4 test (the decisive one).** The degree-6 polynomial on pendulum orbits must be **REJECTED**
  by the noise-calibrated cutoff.
- **R7c — spectral-gap library selection.** Among {poly2, poly4, poly6, poly4+cos} on pendulum orbits, the
  gap criterion `max(σ_{j−1} − σ_j)` must select **poly4+cos** (the library containing the true invariant).
- **R7d — the held-out guard, as an independent check.** Held-out scoring must separate true from false:
  poly4+cos stays near machine precision out-of-sample; poly6 degrades by ≥ 10×.

## Verdict rule (three-valued, and one branch overturns us)

- **postulate TRUE — "O4 was a threshold artifact"** iff R7a **and** R7b pass. M6's assertion stands; the
  noise-calibrated cutoff dissolves O4, and the guard is belt-and-braces.
- **postulate FALSE — "O4 is a real obstruction; M6 overstated"** iff R7a passes but **R7b fails**: the
  degree-6 arm survives noise calibration too. Then the threshold was *not* the defect, O4 is a genuine
  property of the method, and **M6's FINDINGS must be amended** to say so. This is a live and pre-registered
  outcome, not a fallback.
- **UNDECIDED(noise estimate)** iff ε is unstable — e.g. varies by orders of magnitude with `dt`, or comes
  out at round-off so the cutoff degenerates — leaving Cor. 4.2 inapplicable in a near-noiseless synthetic
  setting. Reported with the numbers that made it inapplicable.

## Honest scope

- **Zero novelty.** All three upgrades are other people's; R7 is adoption plus a test that the adoption
  works on our own known failure case. The only thing being decided is *which of our two stories about O4
  is right*.
- The noise estimate is specific to synthetic integrator error. On real noisy data ε is directly available
  and Cor. 4.2 applies as written; the ε-by-step-halving construction here is a **stand-in for a setting the
  formula was not designed for**, and that is stated as a limitation, not hidden.
- A single system (pendulum) and one false-positive arm. Passing R7 does not prove the criterion is
  universally safe — it proves it handles the one case that broke us.
- Bridge-solo; reuses R2's own code and orbit setup; numpy only.
