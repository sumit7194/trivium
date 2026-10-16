# V14 findings (bridge, TaylorModels.jl replay)

## Q0: flowpipe sanity — PASS (2026-10-16), after one diagnosed fix
- **Q0a.** The harmonic oscillator over 2π contains its exact image (`julia/smoke.jl`).
- **Q0b.** Rössler (a = 5.7, b = c = 0.2), validated flow to T = 5 from 5 points, against a 50-digit mpmath reference
  (`code_q0_ref.py`; cross-checked at 70 digits to 25 digits). **5/5 contain the reference.** Enclosure widths are
  5e−13 to 6e−12 after widening. Result: `results/q0_rossler.json`.
- **Diagnosis of the first attempts** (recorded, not hidden):
  1. Parameters given as Float64 constants: 3 of 5 missed by ~1e−14. Fixed by carrying a and b as constant extra
     states, with interval boxes enclosing the exact decimals.
  2. Still 2 of 5 missed. `julia/q0_diag.jl` showed that the package's own flowpipe boxes contained the reference in
     EVERY case, but the step's Taylor model evaluated at δt = T − t_n did not, by up to 0.49 enclosure widths.
     Evaluating in full interval arithmetic (`rig_eval`) did not change this.
  3. `julia/q0_timeprobe.jl` widened δt by ±ε, and containment returned at ε = 1e−15 for one case and 1e−14 for the
     other.
- **Conclusion:** the step-start time labels t_n are Float64 sums that drift from the true elapsed time by ~n ulps.
  The state enclosures are rigorous as sets.
- **Rule adopted** (`julia/v14_rigor.jl`): every time offset is widened by ε_n = 4·n·eps(T_max), and all Taylor-model
  evaluations go through `rig_eval`, which is interval arithmetic throughout.
- **Why the rule is sufficient:** Poincaré-map images of autonomous flows don't depend on time labels. Return-time
  enclosures carry the widening.
- Environment: Julia 1.13.2, TaylorModels 0.13.1, TaylorIntegration 0.18.19, IntervalArithmetic 1.0.12 (pinned
  Manifest).
