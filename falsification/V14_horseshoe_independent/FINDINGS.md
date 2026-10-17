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

## Q1: Rössler qualification on quantum's specs — PASS as registered (results/q1_rossler.json; julia/q1_*.jl)
- **Read only the five r1_*.spec files** (ex_coneM, ex_coneN, W1_swap, W2_rot90, W3_shrink). No quantum JSONs were
  read. A·A⁻¹ = I was checked exactly for every t-set.
- **Example coverings:** M⟹M, M⟹N, N⟹M and N⟹N under P² are all **CERTIFIED**, at ladder level 2.
  - Condition (b) passes at level 1. Condition (a) passes at level 2, and the strong form |s| < 1 holds everywhere
    (max |s| 0.44–0.88).
  - Orientations: +1, +1, −1, −1. Smallest edge margin 0.106 u-units (0.058 in y).
  - Return times 11.3–12.2. Transversality is certified (min ẋ = 4.1 on the crossing enclosures).
- **Wrong-coverings (each REJECTED as a certified (b) failure at level 1, both orientations refuted; none UNDECIDED):**
  - W1: M⟹M, M⟹N and N⟹M rejected.
  - W2: M′⟹M′ and N⟹M′ rejected. **M′⟹N CERTIFIED**, as the prereg requires (orientation −1, margins 0.723 and
    3.54).
  - W3: M⟹M and M⟹N rejected. N⟹M is certified; shrinking the target along u makes it easier, so this is genuine.
- **Q1 PASS** (all 4 examples CERTIFIED; W1/W2/W3 REJECTED; W2 M′⟹N CERTIFIED).
- **Caveats:**
  1. **The section is an assumption.** The specs don't state it; {x = 0, ẋ > 0} in (y, z) was used, as in
     Zgliczyński 1997 and CAPD's example. Quantum has been asked to confirm (a spec question, not an outcome).
  2. **RIGOUR GAP (important):** TaylorModels `validated_integ` does the Taylor-polynomial arithmetic in plain
     Float64 and does not add those rounding errors to the remainder. Q0 has the same gap.
     - The decisions here are safe numerically: the smallest margin is ~1e10 × the rounding error, and a non-rigorous
       spot check put 120 of 120 sample images inside the enclosures.
     - **But as built, V14 is NOT a fully rigorous implementation.** "Certified" here means certified up to
       unaccounted Float64 rounding in the polynomial arithmetic.
     - This must be fixed before V14's certificates can stand in for S6. Amendment B1 below is registered before
       Q2/Q3.
- Runtime ~26 min × 2 processes; ~1.1 GB per process.
- **Update (quantum's spec answer; no outcomes received):**
  - The section is CONFIRMED: x = 0 crossed from x < 0 to x > 0, coordinates (y, z), P². The field matches
    q1_poincare.jl.
  - The base coverings in quantum's run are specified in r1_generic_{MM,MN,NM,NN}.spec. Q1 took M and N from the
    ex_cone specs (which are cone-condition checks), but their boxes are exactly the r1_generic M and N (same centres,
    U and S). So the Q1 base result applies to the same coverings.
  - The B1 re-qualification reads r1_generic_*.spec directly and asserts the equality.
