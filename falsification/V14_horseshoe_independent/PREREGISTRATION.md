# V14: pre-registration of the bridge's independent replay of the chaos-proof covering relations (quantum S6)

*2026-10-16. Written before any V14 covering code exists. Quantum's R1 (Rössler) has PASSED (ce66e54), and the
bridge knows its decisions. Quantum's HH-PRIMARY is running, and the bridge has not seen its results.*

## Role
Quantum's phase-2 pre-registration (S6) requires a second implementation of every covering relation that the
horseshoe claim rests on. CAPD/MPFR is quantum's engine. V14 uses **TaylorModels.jl 0.13.1** (Julia 1.13.2,
IntervalArithmetic 1.0.12 with Float64 intervals; pinned in `julia/Manifest.toml`). It shares no code and no
arithmetic library with CAPD or MPFR.

## What V14 computes
For a t-set ("h-set") pair (M, N) and a map P (a Poincaré return, or its iterate):
- The checks of AZ 2001 Def. 2, as used in quantum's T0/B8:
  - **(b)** the image of M's left edge lies in N's left side, and the image of M's right edge lies in N's right side
    (or the reverse, with the orientation recorded);
  - **(a)** the image of M's whole support misses {|u| ≤ 1, |s| ≥ 1} in N's frame. The strong form |s| < 1 is
    recorded as data.
- The Poincaré map is built by the bridge from the validated flowpipe:
  - for each Taylor-model step, the section function is bounded over the step;
  - the crossing time is enclosed by interval root-isolation on the step's time polynomial, plus its remainder;
  - transversality (the section gradient · field excludes 0) is certified on the crossing enclosure, else that piece
    FAILS closed;
  - the image is the flowpipe evaluated on the crossing-time enclosure.
- Edges and supports are subdivided by a fixed, pre-stated ladder (8, 32, 128 pieces per edge; 4×4, 16×16, 64×64 boxes
  per support). The first level at which every piece certifies is recorded. An exhausted ladder is UNDECIDED.
- Energy-level systems (HH, Kerr, MN) need the S9 analogue: the eliminated momentum is enclosed from H = E on the
  correct branch, and every crossing enclosure must contain H = E.

## Gates (in order; each must pass before the next)
- **Q0, flowpipe sanity:**
  - the harmonic oscillator over 2π contains its exact image (done: `julia/smoke.jl`);
  - Rössler's validated flow, at 5 points, contains a high-precision (mpmath, 50-digit) non-rigorous reference at
    T = 5.
- **Q1, Rössler qualification on quantum's exact specs** (`qsim/capd/horseshoe_results/r1_*.spec`, read as inputs):
  - reproduce the 4 example coverings as CERTIFIED;
  - reproduce W1, W2 and W3 as REJECTED (certified failure, or UNDECIDED at the top of the ladder, recorded as which).
  - W2's M′⟹N must certify (quantum notes this is a genuine covering).
- **Q2, HH qualification:** the 7 (5.1) coverings on AZ 2001's published M0–M4 as CERTIFIED, and W-AZ1/W-AZ2 as
  REJECTED. Run only after quantum's HH-PRIMARY result is sealed (commit + sha256) and sent. V14's HH decisions are
  committed before the bridge reads quantum's HH JSONs.
- **Q3, MN replay (after A-K20):** every covering in quantum's MN claim.

## Comparison rule (matching quantum's MR cross-path rule)
- **FAIL** = opposite CERTIFIED decisions on any check. A FAIL is investigated, never averaged; the claim waits until
  it is resolved.
- **UNDECIDED** on one side is not a disagreement. It is reported as "overlap only".
- Margins (how far inside a side each edge image lies) are compared as data, not as a gate.

## Wording
On success, the claim's S6 line reads: "an independent implementation (TaylorModels.jl, Float64 intervals) certifies
the same covering relations". If V14 cannot certify the MN coverings within its ladder, the line reads "S6 replay
UNDECIDED (method limit)", and the fallback (CAPD in Weyl coordinates, representation-independent only) is invoked by
quantum's registered rule.

## Budget and environment
- At most 2 cores at nice 10, and no wall-clock stop rule.
- Julia and package versions are pinned; each result JSON records them.

## Disclosure (2026-10-16): partial unblinding on HH
While answering a process question, quantum told the bridge one qualitative fact about its first HH pass: on coarse
16×16 boxes, condition (b) passes and condition (a) fails, for 4 of the 7 coverings. The bridge has seen no numbers
and no per-covering decisions. V14's HH run is unaffected: it uses its own pre-stated subdivision ladder, and its
decisions are committed before the bridge reads quantum's JSONs. Quantum's registered HH run is its first pass. The
adaptive pass is a disclosed post-hoc escalation (quantum 5d77bee; an earlier message gave the hash "b2d1c1a" before the commit existed).
- **Second partial unblinding (2026-10-16):** a quantum status message reported that 1 of 7 adaptive HH coverings
  (M0⇒M0) was certified at that point. V14's HH decisions are unaffected (own ladder, committed before reading
  quantum's JSONs); disclosed here.
- **Complete list of HH information the bridge has received** (quantum's own inventory, 2026-10-16):
  1. the first-pass qualitative picture ("(b) passing and (a) failing on coarse boxes"; disclosed above; also in
     quantum's prereg commit 5d77bee);
  2. the adaptive-pass M0⇒M0 certified, at 305 leaves;
  3. the first-pass settings (16×16 support boxes, 64 pieces per edge).
  Nothing else: no other covering outcome, no W result, no margins.
  4. (Added at quantum's own disclosure.) Quantum's prereg note d64dc56 says the adaptive W-AZ re-runs were stopped
     because they would bisect to the 2¹⁶ cap, and that the registered first pass "already settles" W-AZ1 and W-AZ2.
     That is a qualitative statement about the W outcome; treat it as known.
  5. (2026-10-17 evening, a quantum status message.) The two HH coverings still running after the reboot (they are
     being rerun under quantum's B13) "likely" have a persistently failing box, and quantum offers this as the reason
     for their long runtimes. It is quantum's speculation, but it is qualitative information about two coverings;
     treat it as known.
     - The bridge has NOT read B13 or any of quantum's HH JSONs.
     - Five HH coverings are sealed at quantum 914e99f. The bridge has not received their hashes or outcomes.
     - V14's HH decisions stay on V14's own pre-stated ladder, committed before reading quantum's JSONs.

## Amendment B1 (2026-10-18 overnight, after Q1 and BEFORE Q2/Q3): close the Float64 rounding gap
- **The gap:** `validated_integ` does the polynomial coefficient arithmetic in Float64, and those rounding errors
  are not in the remainder. So V14's enclosures are not fully rigorous.
- **Fix, in order of preference:**
  1. Run TaylorModels with Interval{Float64} polynomial coefficients, if the package supports it end to end. Every
     coefficient operation is then enclosed.
  2. Otherwise, add an a-posteriori rounding bound to each step's remainder. Bound: (number of coefficient
     operations) × (max |coefficient|) × eps(Float64) × a safety factor of 4, derived and stated per step.
     Validate it by comparing against a BigFloat (256-bit) re-run of the same steps on Q0's Rössler points: the
     bound must contain the Float64-vs-BigFloat difference.
- **Re-qualification:** with the fix, rerun Q0 (5/5 containment) and Q1 (the same 4 CERTIFIED, W1–W3 REJECTED,
  W2 M′⟹N CERTIFIED). Either a different decision, or an UNDECIDED, is reported as such.
- Q2 (HH) and Q3 (MN) use only the fixed pipeline.
- The S6 wording stays conditional on B1 passing.

## Amendment B2 (2026-10-18, after B1's Q1 FAIL and BEFORE any further covering run): re-qualify on Rössler
- **Why:** on the rigorous pipeline (B1, validated_integ3), Q1's required certifications came out UNDECIDED. The
  causes are a few QR-validation failures per support, and wider enclosures that break the strong form of (a) on
  M⟹M and W2 M′⟹N.
- **Changes, all pre-stated here (the integrator and its rigour are unchanged):**
  1. **Adaptive refinement of failed pieces.** Any support box or edge piece that fails validation or a check is
     bisected (in its longer side, in the t-set's (u, s) chart), recursively to depth ≤ 6 below the level-3 ladder,
     with a cap of 2¹⁶ leaves per covering. A covering is CERTIFIED only if every leaf certifies.
  2. **Higher Taylor order in the box variables:** orderQ 3 (from 2), with orderT unchanged. This is a single
     pre-stated setting, not a sweep.
  3. **Pivoted QR**, only if available in the pinned package. Otherwise this item is dropped and recorded.
- **Gate (unchanged from Q1):** the 4 example coverings CERTIFIED; W1, W2 and W3 REJECTED; W2 M′⟹N CERTIFIED.
  - Any certified-vs-rejected contradiction with B1 or with quantum is a FAIL to investigate.
  - If B2 still leaves required certifications UNDECIDED, V14 stays "UNDECIDED (method limit)". The next option (a
    different validated integrator) would then need its own amendment.
- **Budget:** ≤ 2 processes at nice 10, ≤ 3 GB, and disk checks before running.

## Amendment B3 (2026-10-18 afternoon, after B2 was stopped with NO verdict, before any B3 run)
- **Why:** B2 (orderQ 3 plus adaptive refinement) was too slow: about 10 s per P² image, with level 3 unfinished
  after 7 h. It was stopped at the user's restart (logs committed, 2bc189e) and has no outcome. B1's data shows the
  obstruction is local: QR-validation failures on 10–18 of 4096 level-3 pieces, plus a wider (a) bound for M⟹M and
  W2 M′⟹N. Local refinement at B1's cost should reach it.
- **Change:** B2's adaptive refinement (bisect failing pieces in the (u, s) chart along the longer side; depth ≤ 6
  below level 3; ≤ 2¹⁶ leaves; CERTIFIED only if every leaf certifies) is applied at **orderQ 2**, B1's setting.
  - The B2 code is reused with only the order constant changed (julia/b3_*.jl, a mechanical copy of b2_*.jl; the
    diff is recorded).
  - The integrator (validated_integ3, midrad = false), the ladder and the gate are unchanged.
- **Gate (unchanged):** the 4 examples CERTIFIED, W1–W3 REJECTED, W2 M′⟹N CERTIFIED. A contradiction with B1 is a
  FAIL.
  - If B3 still leaves required certifications UNDECIDED, V14 stays "UNDECIDED (method limit)".
  - The next option would be a different validated integrator, under its own amendment.
- **Budget:** 2 processes at nice 10, ≤ 3 GB total, a disk check first. It runs in the bridge's own session (no
  sub-agent).
- **Risk flag kept:** results on validated_integ3 are "subject to the open upstream defects in sibling routines"
  (TaylorModels.jl #207).
- **B3 implementation note (2026-10-18 ~17:45), on the user's request to use the idle cores:** B3 is restarted as
  julia/b3t_q1_cover.jl. It is b3_q1_cover.jl plus a threaded prefetch of the P² images: the same images, computed
  in parallel, behind a cache lock.
  - Method, settings, ladder, refinement and gate are unchanged.
  - Thread-safety test (julia/b3t_threadtest.jl; results/b3t_threadtest.log): 16 rectangles, serial vs 4 threads,
    give bitwise-identical enclosures (all 16 ok), at 3.7× speed.
  - The serial B3 run (3.5 h, no verdict) was stopped; its logs are kept.
  - Output: results/b3t_q1_{N,M}.json, 2 processes × 4 threads.

## Q2 launch note (2026-10-18 ~22:50, before any Q2 decision exists; nothing of quantum's HH results has been read)
- Q2 runs on the B3t pipeline qualified by Q1 (27a89b7). Code: julia/q2_hh_poincare.jl and julia/q2_hh_cover.jl, a
  mechanical adaptation of b3t.
- Inputs: quantum's hh1_*.spec files only (t-sets, AZ M3 special sides, covers). No JSON, outcome or adaptive-pass
  spec (hh1a/hh1b) was read.
- System: H = (px² + py²)/2 + (x² + y²)/2 + x²y − y³/3; Θ1 = {x = 0, ẋ > 0, H = 1/6}; P1; coordinates (y, p_y).
  - px is lifted from the energy on the positive branch, with the radicand certified > 0 (else the piece fails
    closed).
  - S9: H on every image enclosure must contain 1/6.
- t-sets are parallelograms: each source piece's axis-aligned hull is integrated (conservative).
- AZ special M3 sides: as in the spec semantics. For special targets no certified (a)-violation is claimed.
- Smoke test: 3 points against RK4 references, all contained. Quick test at level 1: runs, coarse pieces undecided
  (expected).
- Ladder and refinement as in Q1/B2. Gate as registered: the 7 (5.1) coverings CERTIFIED; W-AZ1 and W-AZ2 REJECTED
  under the Q1 merge rule. Runs as 2 processes × 4 threads.
- **Q2 speed-up (2026-10-19 ~10:40; mechanical, no change of method):** refinement now prefetches each batch of
  child pieces in parallel (`refine!(…; pre = …)`), with the same breadth-first order, leaves and decisions. The
  pending AZ M2⟹M3 covering runs as its own group "C" (6 threads), while group A finishes M1⟹M2 serially. W1/W2 are
  already REJECTED via M2′⟹M3 (group B), so the W M1⟹M2 lines are not needed for the gate.
- **Blinding disclosure:** quantum's seal file names (hh1b_M1M2_*, hh1b_M3M4_*) reveal which two coverings needed its
  re-split, consistent with disclosure item 5. That was seen before any V14 Q2 decision on those coverings, and
  V14's procedure is fixed regardless.

## Amendment Q2-R1 (2026-10-19 ~11:00, after M3⟹M4 came out UNDECIDED at the registered depth 6, before any rerun)
- **Registered result kept:** M3⟹M4 is UNDECIDED at depth 6 (q2_hh_B.json). (b) is all certified; (a) has a failing
  leaf at depth 6.
- **Diagnosis (labelled post hoc):**
  - The failing leaf's rigorous image is computed (ok); it is not an integration failure. Its envelope is too wide:
    U ∈ [−1.18, −0.94], S ∈ [−1.0016, −0.52].
  - A NON-rigorous float probe of 81 points in the leaf gives true margins of ≈ 0.07 (in U) and ≈ 0.23 (in S): the
    true image clears the forbidden zone.
  - So the envelope is ~2–3× too fat in linear size, which ≈ 3–4 more bisections should fix.
- **Escalation, M3⟹M4 only:** MAXDEPTH 12 (6 levels beyond registered; a leaf can reach 1/4096 of a level-3 piece's
  area), leaf cap 2¹⁸. Same pipeline, ladder and checks, with parallel refinement.
- **Stop rule:**
  - CERTIFIED if every leaf passes;
  - REJECTED if a certified violation appears;
  - otherwise UNDECIDED at depth 12 / cap. Then report "limit of this method", with the leaf.
- **Reporting:** a CERTIFIED here is reported as "certified after a disclosed post-hoc depth escalation", alongside
  the registered depth-6 UNDECIDED.

## Amendment Q2-R2 (2026-10-19 ~19:45, after M1⟹M2 came out UNDECIDED at the registered settings, before any rerun)
- **Registered result kept:** M1⟹M2 is UNDECIDED at depth 6 / leaf cap 2¹⁶ (q2_hh_E.json). (b) is certified
  (orientation −1). For (a), 2977 of 4096 level-3 boxes fail; the leaf cap was hit with 34487 pieces queued; no
  certified violation.
- **Diagnosis (labelled post hoc; q2_m1m2_diag.jl, q2_m1m2_probe.jl):**
  - Every level-3 rigorous image is computed (0 integration failures). The failures are all "ambiguous": the
    enclosures are wide, median U width 6.0 and S width 13.1 in M2's frame. Each box's image is a thin, tilted,
    stretched curve, and its axis-aligned hull is fat.
  - A NON-rigorous float probe (17 × 17 RK4 grid points per failing box, 2977 boxes) finds no point inside
    F = {|u| ≤ 1, |s| ≥ 1}. The minimum distance-type margin max(1 − |s|, |u| − 1) is 0.160, with median 0.946.
  - Disclosure: a first version of the probe used a wrong margin (|u| − 1 if |u| > 1, else 1 − |s|), which
    understated margins near |u| = 1; it was corrected before this amendment, and both files record the fix.
  - Estimate, assuming enclosures shrink linearly: boxes need 3–7 bisections below level 3 (581, 1329, 767, 273
    and 27 boxes at 3, 4, 5, 6 and 7). The pessimistic leaf count is 2.7 × 10⁶; the real count should be far lower,
    because children with larger margins pass early.
- **Escalation, M1⟹M2 only (group "F"):** MAXDEPTH 10 (4 levels beyond the registered 6; 3 beyond the estimated
  worst case), leaf cap 2²⁰. Same pipeline, ladder, checks and parallel refinement as Q2-R1; 5 threads. Group A keeps
  running as the serial identity check of the registered run. (The stop message's text still reads "leaf cap 2^16
  reached"; that is fixed wording, and the cap in force is the env value recorded in the JSON.)
- **Stop rule:**
  - CERTIFIED if every leaf passes;
  - REJECTED if a certified violation appears;
  - otherwise UNDECIDED at depth 10 / cap 2²⁰, reported as the limit of this enclosure method.
  - A possible next step is a method change (evaluating u and s on the Taylor-model polynomial instead of the
    axis-aligned hull). That would need its own amendment and validation; it is not part of Q2-R2.
- **Reporting:** a CERTIFIED here is reported as "certified after a disclosed post-hoc depth/cap escalation (Q2-R2)",
  alongside the registered UNDECIDED.

## Amendment Q2-R3 (2026-10-20 ~11:30, after Q2-R2 ended with one leaf whose image fails to integrate; before applying)
- **Registered results kept:** M1⟹M2 is UNDECIDED at the registered settings (q2_hh_E.json) and UNDECIDED under
  Q2-R2 (q2_hh_F.json, "failing leaf at depth 10").
- **Facts from q2_hh_F.json:**
  - (b) is certified (orientation −1).
  - For (a), the refinement queue was EMPTY when the single remaining leaf L hit depth 10. L is chart
    u ∈ [−631/1024, −315/512], s ∈ [887/1024, 111/128].
  - So every other piece of the (a) refinement is a leaf that passed (miss_F certified).
- **Diagnosis (post hoc; q2_m1m2_leaf.jl, q2_fb_explore.jl):**
  - L's image is not computed at the registered orderT 16: validated_integ3 stops at t = 4.63 ("QR preconditioning
    could not be verified"). A float probe gives a margin of 0.26.
  - With the SAME validated_integ3 (orderQ 2, midrad false, same abstol and maxsteps), orderT 12, 14, 18 and 20
    all integrate L, and each image satisfies miss_F. orderT 24 hits a package FieldError, which is irrelevant.
  - Disclosure: the fallback list below was chosen AFTER seeing this. That cannot bias the result: every enclosure
    validated_integ3 returns is rigorous at any orderT, so using any successful one is sound.
- **Rule (Q2-R3):** if the registered integration (orderT 16) of a piece fails (image not ok), retry with orderT 14,
  then orderT 18; use the first ok image. Everything else is unchanged: section logic (q2_fallback.jl generates
  `poincare1_fb` textually from q2_hh_poincare.jl with only the integrator call swapped), status logic, miss_F and
  violates_a. Pieces whose primary image is ok are never re-integrated.
- **Validation, done BEFORE L counts (q2_r3.jl):** on 200 pieces drawn reproducibly from the level-3 grid
  (seeded; every 20th of the 4096 boxes, then the first 200 of the 2977 non-pass boxes in list order, up to 200 in
  total), whose primary images are ok:
  - (V1) each fallback image (orderT 14 and 18) must INTERSECT the primary image in (y, p_y); disjoint enclosures
    of the same set would mean a bug;
  - (V2) every float RK4 point of a 3 × 3 grid in the piece must lie inside every computed enclosure, primary and
    both fallbacks.
  - Any V1/V2 failure voids Q2-R3.
- **Application:** with validation passed, evaluate L under the rule.
  - If its image passes miss_F, the Q2-R2 leaves together with L form a complete cover of M1 by certified pieces,
    and M1⟹M2 is CERTIFIED.
  - If L's image is ok but ambiguous, refine L's subtree under the rule to depth 12 (cap 2¹²).
  - A certified violation → REJECTED. Otherwise UNDECIDED.
- **Reporting:** a CERTIFIED here is reported as "certified after disclosed post-hoc escalations Q2-R2 (depth/cap)
  and Q2-R3 (integrator-order fallback for one leaf)", alongside the registered UNDECIDED.

## Amendment Q2-U and Q3-S (2026-10-21, registered BEFORE either run; for the unattended run while the user travels)
Both use ONE fixed setting, chosen now and applied identically to every covering:
- the Q2 pipeline unchanged (validated_integ3, orderQ 2, orderT 16, midrad false; the same ladder; the same (a)/(b)
  logic, miss_F and violates_a);
- refinement to MAXDEPTH 10, leaf cap 2²⁰ (the Q2-R2 values);
- the Q2-R3 rule everywhere: a piece whose orderT-16 image fails is retried with orderT 14, then 18, using the first
  ok image. The validation of that rule (V1/V2, 200 pieces, 0 failures) is in q2_hh_R3.json;
- the image cache is cleared between coverings with different source sets (memory bound only; it never changes an
  image).
Driver: julia/q2u_main.jl; chain: julia/run_chain_2026-10-21.sh.

**Q2-U, the uniform re-run of the AZ (5.1) coverings plus the wrong-set controls.**
- Coverings: the 7 AZ (5.1) coverings, plus W-AZ1 and W-AZ2 on M2′⟹M3. Spec files: quantum's hh1_*.spec (the same
  sha256 as Q2).
- **Gate:** PASS iff all 7 AZ coverings are CERTIFIED AND W-AZ1 and W-AZ2 are both REJECTED. Anything else is
  reported as it falls.
- Purpose: to replace "certified, two of them after post-hoc escalations" by "certified under one setting fixed in
  advance". Q2's registered results and escalations stay on record unchanged. Q2-U is a new run, not a revision.
- Disclosure: the setting was chosen AFTER Q2/Q2-R1/R2/R3 showed what M1⟹M2 and M3⟹M4 need. So Q2-U certifies under
  a fixed setting, but it is not blind to the difficulty.

**Q3-S, an independent replay of quantum's HH-SECONDARY (NOT blind).**
- Coverings: quantum's B14 constructor sets N0, N3–N6 (hh2_*.spec at quantum 5a21dde, whose sha256s were already
  verified against the seals): N0⟹N0, N0⟹N3, N3⟹N4, N4⟹N5, N5⟹N6, N6⟹N0 (required) and N6⟹N3 (optional).
- **Disclosure:** quantum's outcome is already known to the bridge: the 6 required coverings certified, and N6⟹N3 a
  certified orientation failure. So this is a cross-implementation REPLAY, not a blind test.
- Expected agreement: 6 CERTIFIED, plus N6⟹N3 REJECTED (or UNDECIDED, which counts as "overlap only").
- Comparison rule as in Q2: FAIL = opposite certified decisions.
- The sets are general parallelograms; each piece is integrated as its axis-aligned hull, which is conservative (as
  for the AZ sets).

**Running:**
- One Julia process at a time, 6 threads, nice 5, heap hint 8 GB. A watchdog kills it only if RSS > 11 GB (own PID
  only), and the chain then moves on.
- Q2-U runs first, then Q3-S.
- Results: results/q2u_*.json and results/q3s_*.json, written after each covering. Status: results/CHAIN_STATUS.md.
- **Addendum (2026-10-21, before launch): checkpoint/resume, at the user's request.** The user asked that a long power
  loss cost at most a few hours, and that nothing live in tmp folders.
  - q2u_main.jl overrides refine! with an identical breadth-first refinement that saves its full state every hour
    to results/ckpt_q2u/ (queue from head on, leaves, maxd, nnew; keyed by covering and phase) and resumes from it.
  - Finished coverings in q2u_all.json / q3s_all.json are skipped on relaunch. The chain appends to its logs and
    status file and has a pid lock.
  - **Test (julia/test_resume_2026-10-21.sh):** AZ M0⟹M0 run uninterrupted vs kill -9'd after its first checkpoint
    and relaunched. Both CERTIFIED, 6074 leaves, max depth 2; ALL fields identical except timings; 0 leftover
    checkpoints. The decision logic is unchanged.
