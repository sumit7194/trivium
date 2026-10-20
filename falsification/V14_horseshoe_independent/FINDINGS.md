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

## B1 rigour fix: Q0 PASS, **Q1 FAILS on the rigorous pipeline** (results/b1_note.md, b1_q0.json, b1_q1.json, b1_validation.json)
- **A second, larger gap was found in the pre-B1 pipeline.** `validated_integ` (TaylorModels 0.13.1) drops the
  polynomial terms above orderQ in the initial-box variables and never bounds them.
  - On x′ = x², with its exact solution, the true value misses the enclosure by up to 3.8e12× the stored remainder,
    scaling as r³ (verified).
  - The Float64 rounding gap is also real: a 256-bit reference fell outside the old enclosures at 145 of 1299 step
    ends, by up to 66× the remainder.
  - **So the pre-B1 Q0 and Q1 "CERTIFIED" decisions were never rigorous.** They are hereby downgraded to
    "non-rigorous agreement".
- **B1 used `validated_integ3`** (same pinned package), which is validated per step in interval arithmetic. It bounds
  the truncated terms, uses exactly representable time steps and verified QR, and has midrad = false. No upgrade,
  no tuning. One package defect (undefined `t0` at validated_integ3.jl:467, hit only when no step length validates)
  is caught, and that piece fails closed.
  - Validation: 4113 of 4113 step-end samples on Q0's 5 points lie inside, smallest relative margin 0.0106; Q1 spot
    check 52 of 52 inside.
- **Q0 (rigorous): PASS**, 5 of 5 (widths 3e−13 to 4e−12).
- **Q1 (rigorous): FAIL as registered.**
  - The base t-sets come from r1_generic_*.spec (equal to the old boxes); the section is confirmed.
  - **The 4 example coverings and W2 M′⟹N are UNDECIDED,** where the gate requires CERTIFIED. So are W1 N⟹N, W2 N⟹N,
    W3 N⟹M and W3 N⟹N, which were certified before B1.
  - W1, W2 and W3 are still REJECTED.
  - **There is no contradiction anywhere:** no covering is certified by one pipeline and rejected by the other.
  - **Causes (method limits):**
    - a few support images (10–18 of 4096 at level 3, plus one N edge piece) fail the QR validation. For M⟹N and
      the N-source coverings, these are the only obstruction.
    - for M⟹M and W2 M′⟹N the enclosures are much wider, so the strong form of (a) is lost: max |s| bound 1.18 and
      1.71.
  - That the missing column pivoting in QR causes the widening is a guess (unverified).
- **Status under the prereg wording:** V14's S6 replay is "UNDECIDED (method limit)" until a further amendment
  qualifies it on Rössler. Quantum's own R1 (CAPD) is unaffected.
- **Possible upstream issue:** validated_integ's truncation behaviour, if its documentation claims rigour. To be
  checked against the TaylorModels docs before any report; the user decides.
- Runtime: Q1 8.1 h + 8.3 h on 2 processes, ≤ 1.3 GB each.
- **Upstream status, checked 2026-10-18:** TaylorModels.jl issue #207 (open, 2026-10-01, LongQianQL),
  "validated_integ2 incorrect enclosure", reports the same x′ = x² unsound enclosure for validated_integ2. The
  maintainer (lbenet) replied that he is aware of failures "also in validated_integ" and is working on a fix.
  - **So the gap is already known upstream. We will not open a duplicate.** A comment adding our validated_integ
    (v1) reproducer is optional, and the user's call.
  - The package presents these routines as "validated integration of ODEs", and the README says "guaranteed error
    bounds".
  - **Risk flag for B1/B2:** validated_integ3 is not named in #207, and passes our tests (4113 of 4113 inside against
    256-bit references, 52 of 52 on Q1). But its rigour rests on reading the source plus those tests, while the
    maintainer acknowledges defects in sibling routines.
  - V14 certificates on validated_integ3 are therefore labelled "subject to the open upstream defects in sibling
    routines", until the fix lands or validated_integ3 is independently confirmed.

## Quantum HH-PRIMARY SEALED (received 2026-10-18; hashes only, nothing opened)
- Commit quantum ca819cf, with 26 result files in qsim/capd/horseshoe_results/: hh1_*, hh1a_*, hh1b_*, including W-AZ1/W-AZ2
  and the exact checks.
  - Hash examples: hh1_M0M0 989de158…84a6, hh1_W_AZ1_swap 002c896f…e627, hh1b_M3M4_c1c.pre_restart 15fbab29…3a85.
  - The full list is in the bridge transcript of 2026-10-18.
- Both readings of the post-hoc B13 budget change are in HH_PRIMARY_OUTCOME.md (ca819cf).
- **The bridge has NOT opened any of these.** V14 Q2's HH decisions must be committed first. That needs V14 to
  re-qualify on Rössler (B3, running).

## B3 (threaded): Q1 Rössler re-qualification on the RIGOROUS pipeline — PASS (results/b3t_q1.json; julia/b3t_*.jl)
- Pipeline: validated_integ3 (interval-validated steps, truncation bounded, midrad = false), orderQ 2, adaptive
  bisection of failing pieces (depth ≤ 6, ≤ 2¹⁶ leaves). 2 processes × 4 threads; the thread-safety test gave
  bitwise-identical output. Finished 2026-10-18 ~22:00.
- **Gate PASS:**
  - all 4 example coverings (M⟹M, M⟹N, N⟹M, N⟹N) are CERTIFIED: every leaf of (a) and (b), 4362–5335 leaves,
    refinement depth ≤ 2;
  - W1, W2 and W3's required rejections are REJECTED (certified (b) failures, both orientations);
  - **W2 M′⟹N is CERTIFIED** (5531 leaves, depth 2).
  - Also certified, as before: W1 N⟹N, W2 N⟹N, W3 N⟹M, W3 N⟹N.
- **0 contradictions with B1.** The decisions now coincide with the pre-B1 (non-rigorous) Q1 decisions.
- **Status:** V14 is qualified on Rössler with a rigorous pipeline. It is subject to the open upstream defects in
  TaylorModels' sibling routines (#207), as flagged.
- **Next gate:** Q2 (HH, blind). Its decisions are committed before reading quantum's sealed HH JSONs (ca819cf).
  Not started (the user said no new work today).

## Quantum HH-SECONDARY SEALED (received 2026-10-19; hashes only, nothing opened)
- Commit quantum 5a21dde. Files hh2_N0N0, N0N3, N3N4, N4N5, N5N6, N6N0, N6N3, exact_checks and summary
  (sha256 in the bridge transcript; e.g. hh2_N0N0 356cb5c2…dc5a, hh2_summary 68602610…dc5a…).
  - The outcome file HH_SECONDARY_OUTCOME.md stays unopened until V14 Q2's decisions are committed.

## Q2 (HH, blind) progress, 2026-10-19 13:10
- **CERTIFIED at the registered depth 6:** M0⟹M0 (6074 leaves), M0⟹M1 (15144), M2⟹M3 (7261; AZ special M3 sides),
  M4⟹M0 (4626), M4⟹M1 (5283).
- **W-AZ1 and W-AZ2: REJECTED** (certified (b) failures on M2′⟹M3).
- **M3⟹M4:**
  - UNDECIDED at the registered depth 6 (q2_hh_B.json);
  - **CERTIFIED after the disclosed post-hoc escalation Q2-R1** (q2_hh_D.json): 27053 leaves, max depth 8, i.e. 2
    levels beyond the registered 6, well within the escalation cap of 12.
- **M1⟹M2: UNDECIDED at the registered settings** (q2_hh_E.json, 2026-10-19 18:51; the parallel-refinement rerun):
  - (b) certified, orientation −1, at level 3.
  - (a): 2977 of 4096 level-3 boxes fail. Refinement hit the leaf cap 2¹⁶ at depth 6, with 34487 pieces still queued.
  - No certified violation of (a).
  - So the limit hit is the leaf cap (the amount of work), not the depth.
  - Group A (serial, same computation) is still running; it is kept as an identity check of the parallel refinement.
  - Post-hoc diagnosis: 0 image failures at level 3; fat hulls (median U width 6.0, S width 13.1). Float margin
    ≥ 0.16 over all 2977 boxes. Hence Q2-R2.
  - Group A (serial) finished: AZ M1⟹M2 is identical to group E (UNDECIDED, 65536 leaves, depth 6), so the identity
    check of the parallel refinement passes. Its AZ M2⟹M3 is CERTIFIED with 7261 leaves, identical to group C.
- **M1⟹M2 under Q2-R2 (q2_hh_F.json, 2026-10-20 04:55): UNDECIDED, "failing leaf at depth 10"**, 131251 leaves.
  - Every other piece passed: the queue was empty when the one remaining leaf hit depth 10.
  - That leaf (chart u ∈ [−631/1024, −315/512], s ∈ [887/1024, 111/128]) is NOT an enclosure-width problem. Its
    rigorous image fails to compute at all: "integration_stopped_at_t=4.63" (validated_integ3's step validation /
    QR preconditioning gave up, with t1 ≈ 8.76).
  - A float probe of that leaf gives u ∈ [1.109, 1.118] and s ∈ [−0.744, −0.736], a margin of 0.26: comfortably
    outside F.
  - So the one remaining obstacle is an integrator failure at a single tiny box, not a sign that the covering fails.
    Any fix (e.g. a fallback integration for failed leaves only) needs its own pre-registered amendment and
    validation.
- **M1⟹M2 under Q2-R3 (q2_hh_R3.json, 2026-10-20 10:52): CERTIFIED** after disclosed post-hoc escalations Q2-R2
  (depth 10 / cap 2²⁰) and Q2-R3 (integrator-order fallback).
  - Validation of the fallback, done before L counted: 200 pieces checked, V1 failures 0 (every orderT-14/18
    enclosure meets the orderT-16 one), V2 failures 0 (every float grid point lies inside every enclosure).
  - Leaf L under the rule: orderT 14, U ∈ [1.031, 1.197], S ∈ [−0.930, −0.551], so miss_F holds. With the Q2-R2
    leaves, M1 is covered by certified pieces.

## Q2 decisions — COMPLETE (2026-10-20), committed before opening quantum's sealed HH results
| AZ covering (5.1) | decision | how |
|---|---|---|
| M0⟹M0 | CERTIFIED | registered depth 6 (6074 leaves) |
| M0⟹M1 | CERTIFIED | registered depth 6 (15144 leaves) |
| M1⟹M2 | CERTIFIED* | *registered UNDECIDED (leaf cap); certified after disclosed post-hoc Q2-R2 + Q2-R3 |
| M2⟹M3 | CERTIFIED | registered depth 6 (7261 leaves; AZ special M3 sides; group A identical) |
| M3⟹M4 | CERTIFIED* | *registered UNDECIDED (depth 6); certified after disclosed post-hoc Q2-R1 (depth 8) |
| M4⟹M0 | CERTIFIED | registered depth 6 (4626 leaves) |
| M4⟹M1 | CERTIFIED | registered depth 6 (5283 leaves) |
| W-AZ1, W-AZ2 (wrong sets) | REJECTED | certified (b) failures on M2′⟹M3 |

- **Gate Q2 as registered:** NOT passed at the registered settings (2 of 7 UNDECIDED).
- **With the disclosed escalations:** all 7 coverings are CERTIFIED and both wrong-set controls REJECTED.
  - So, independently of quantum, the AZ M-chain coverings M0⟹M0⟹M1⟹M2⟹M3⟹M4⟹{M0, M1} hold for P1 at h = 1/6,
    under our TaylorModels pipeline. This is the transcription of AZ's sets in quantum's spec files.
  - Reporting must say "certified after disclosed post-hoc escalations" for M1⟹M2 and M3⟹M4.
- **Next:** ask quantum to lift the HH embargo, then compare under the cross-path rule.

## Cross-path comparison with quantum (2026-10-20, after the embargo was lifted on both sides)
- **Seal check first:** all 35 sealed quantum files (hh1_*, hh1a_*, hh1b_* at ca819cf; hh2_* at 5a21dde) match the
  sha256s in quantum's seal messages (0 mismatches). Only then were HH_PRIMARY_OUTCOME.md and HH_SECONDARY_OUTCOME.md
  read.
- **Comparison rule (registered):** FAIL = opposite certified decisions. **Verdict: AGREE, no FAIL.**

| AZ covering | V14 (TaylorModels.jl, Julia) | quantum (CAPD/MPFR 128, C++) | orientation V14 / q | return-time hull V14 / q |
|---|---|---|---|---|
| M0⟹M0 | CERTIFIED | certified | +1 / LR | [6.831, 7.560] / [6.848, 7.505] |
| M0⟹M1 | CERTIFIED | certified | +1 / LR | [6.831, 7.560] / [6.848, 7.505] |
| M1⟹M2 | CERTIFIED* (Q2-R2/R3) | certified* (hh1b, B13) | −1 / RL | [7.223, 9.214] / [7.244, 9.409] |
| M2⟹M3 | CERTIFIED | certified | +1 / LR | [6.137, 7.898] / [6.144, 7.930] |
| M3⟹M4 | CERTIFIED* (Q2-R1) | certified* (hh1b, B13) | −1 / RL | [7.517, 8.126] / [7.499, 8.188] |
| M4⟹M0 | CERTIFIED | certified | +1 / LR | [6.611, 7.614] / [6.622, 7.581] |
| M4⟹M1 | CERTIFIED | certified | +1 / LR | [6.611, 7.614] / [6.622, 7.581] |
| W-AZ1, W-AZ2 | REJECTED ((b) failures) | rejected ((b) failures) | — | — |

  (* = certified only after disclosed post-hoc escalation, on both sides.)
- **The striking part:**
  - Each pipeline, at its own registered settings, left exactly the same two coverings undecided: M1⟹M2 and
    M3⟹M4. V14 hit its depth 6 / cap 2¹⁶; quantum's first pass did not certify (a) on any covering, and under its
    original 48 core-hour budget it is PARTIAL 5/7 with the same two missing.
  - Both needed the most work on those two (V14: depth 10 plus fallback, and depth 8; quantum: depths 9 and 11,
    about 23 and 32 CPU-h).
  - The strong form |s| < 1 of (a) fails on all 7 in both pipelines (recorded as data).
- **Consistency checks:**
  - Orientations agree 7/7.
  - Every pair of return-time hulls intersects, as two rigorous enclosures of the same range must. The true range
    lies in each intersection; e.g. for M1⟹M2 it is within [7.244, 9.214].
- **Wording (agreed with quantum, 2026-10-20):** "Two independent rigorous implementations (CAPD/MPFR and
  TaylorModels.jl/Float64 intervals) reproduce the covering relations (5.1) of AZ 2001 Lemma 5 on AZ's published
  t-sets, with condition (a) certified on the whole support. In both, M1⟹M2 and M3⟹M4 needed a disclosed post-hoc
  escalation beyond the registered settings, and the CAPD run also exceeded its originally registered core-hour budget
  (B13)."
  - Wherever the V14 side is cited, attach: "subject to TaylorModels.jl #207 sibling-routine defects".
  - Say "reproduces (5.1)", never "reproduces their proof": (5.2)–(5.4) and their Lemma 3 are not redone.
- **Not replayed by V14:** quantum's HH-SECONDARY (own constructor sets; 6/6 required coverings certified, plastic
  number ρ, h_top ≥ 0.2812). That would need its own blind gate.
