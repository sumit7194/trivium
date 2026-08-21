# T1 — Pre-registration: is tabula's C5 readout equally sensitive along the α axis?

*Frozen 2026-08-21 before `code/t1_gain.py` is written or run. Requested by tabula (SpaceTime /
curvature) after the bridge's L15 point landed on their suite. Bridge-solo; independent implementation,
tabula's code not read.*

## The question

tabula's §94 certifies on the quartic Hamiltonian

    H = ½(pₓ² + p_y²) + ¼(x⁴ + y⁴) + (α/2)x²y²

integrable at α = 0, 1, 3; certified at α = 2, 4. The pass reads *"engine emits at the islands, silent
at 2 and 4."* **That is a cross-parameter claim validated on the floor.** Floor is statistical error and
averages down as 1/√N; **gain variation along the α axis is systematic and never averages down.** So a
sensitivity gradient in α would wear the costume of physics and the floor check cannot tell the difference.

**Measure the gain directly: plant a conserved quantity of known amplitude at each α and ask what the
readout recovers.**

## One deliberate departure from tabula's spec, stated up front

tabula warned that with the shell pinned, any quantity with no across-ensemble variance scores
within/total ≈ 1 however perfectly conserved, making the threshold unfailable — and advised varying E₀.
**This build keeps the shell PINNED at E₀ = 8 and plants anyway.** The synthetic plant carries its own
across-ensemble variance by construction (a per-trajectory constant drawn at random), so it is detectable
regardless of whether E₀ varies. That matters because **the pinned shell is the configuration §94's
certificate actually runs in**, and it is that configuration's sensitivity which is in question. Varying
E₀ would measure the gain of a different setup than the one being certified. *Both are run; pinned is
the primary.*

## Frozen gates

- **T1a — the plant must be recovered at all at the integrable points.** At α ∈ {0, 1, 3} the readout must
  return a direction with |overlap| ≥ 0.9 on the planted feature for a near-perfectly-conserved plant
  (ε = 0). If it cannot find a plant that is exactly conserved by construction, the instrument is broken
  and every later gate is void. **Positive control; nothing below counts without it.**
- **T1b — GAIN FLATNESS, the decisive gate.** Define gain = (plant's true within/total ratio) /
  (ratio the readout recovers for the plant direction), out-of-sample on held-out trajectories. Compute at
  each α ∈ {0,1,2,3,4} for each ε ∈ {0, 1e-4, 1e-3, 1e-2, 1e-1}.
  - **FLAT** iff max/min gain across α is **< 3×** at every ε. ⇒ §94's emit/certify contrast is physics.
  - **DEGRADED** iff gain at α ∈ {2,4} is systematically worse than at α ∈ {0,1,3} beyond 3×.
    ⇒ §94's pass measured sensitivity, not integrability, and the certificate needs re-scoping.
  - **UNDECIDED** iff the spread exceeds 3× without ordering on the {0,1,3} vs {2,4} split — real
    variation, but not the gradient the hypothesis names.
- **T1c — detection threshold.** Report the smallest ε at which the plant is still recovered
  (|overlap| ≥ 0.9), per α. A sensitivity gradient shows here as a threshold that moves with α, and this
  is independent of T1b's ratio arithmetic.
- **T1d — the confound check tabula's own method demands.** The plant is a per-trajectory nuisance
  constant with **no dynamical meaning**. If the readout ranks it *above* genuine dynamical structure, that
  reproduces tabula's own confound result rather than measuring gain — report the plant's rank among
  recovered directions, and treat a plant that always wins as a warning about the readout, not a success.

## Declared in advance

- **I have tabula's numbers** (pinned: 1.1e-10 / 4.9e-19 / 2.3e-10 at α=0/1/3, 1.9e-04 / 1.8e-03 at
  α=2/4; varied: 3.7e-11 / 1.4e-24 / 9.0e-10 / 7.1e-11 / 3.1e-09 against floors 3.6e-07…1.0e-06).
  **Reproducing them is not a goal and disagreement is a live, valuable outcome** — that is the whole
  reason an outside session was asked. My readout is built from their written spec, not their code.
- **Integrator: velocity-Verlet** (symplectic; the quartic potential is separable). Energy conservation
  reported per α — an ensemble whose energy drifts is not a fixed shell and would void the comparison.
- Ensemble per tabula: ~70 bounded trajectories, dt = 0.02, 2500 steps, first 150 discarded.
  Train/test split over **trajectories**, never over time samples within a trajectory.
- **Live outcomes:** (a) flat ⇒ §94 survives on this axis; (b) degraded ⇒ §94 re-scoped;
  (c) T1a fails ⇒ my readout is not theirs and the exercise says nothing about their suite.
