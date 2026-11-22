# Fleet run board (resource ledger)

The bridge allocates compute slots. Status only, never results. Update this on every launch and finish.

**Box:** 10 cores, 16 GB, disk ~8.2 GB free (2026-11-17), ~17 GB after Sumit's cleanup at 20:20. The fleet cap is 8 cores. The other 2 are for the system
and Sumit's SPHEREx detector session, which has priority. New disk is limited to 1 GB per job, with a stop-at-5-GB-free guard.
Large downloads wait for a disk cleanup.

## 2026-11-17: Sumit's go on all proposed items (macOS 27.2 regression: ALL repos pass; DeepStrain torch passed 9d80a6b after a resumable re-fetch)

| Sister | Item | Slot | State |
|---|---|---|---|
| ansatz | True-fractal test (TS capture edge), after its preregistration | 2 cores, <1 GB, ~12–13 h (ETA revised) | RUNNING since ~20:00 (prereg 471f76c; self-stops on disk, memory or swap limits) |
| ansatz | Write-up of §150–§152 | none | in progress (d1c8031, 78bdbbb) |
| ansatz | Small-deformation Killing-tensor jet test (prereg 4d7a0c3) | 1 core, <1 GB, short bursts <1 h total, nice 15 | cleared |
| tabula | §200 tangle-seeded chaos check (zoom amendment b710291) | 2 cores, ~1.2 GB, <50 MB, ~3–4 h | RUNNING since 19:55 (process group 78266; write-up 5423fdb). Comparison with ansatz §150 is graded "independent code, not blind" (tabula declared qualitative exposure, numeric unsure) |
| tabula | p = 4/5 high-precision probe (30 min), then full run by request | 1 core | queued |
| quantum | macOS 27.2 regression: PASSED (0ef24f7); next, the wrapping test (harness + pass/fail reading first) | 3 cores, ~1.5 GB | slot request pending |
| quantum | G3 reference worker (~4 GB each) | 1 worker later | queued until the box is lighter |
| deepstrain | Regression; METRICS errata (bridge verifies independently); sGB note; time-slide literature check | 1 core, light | go |
| deepstrain | Benchmark build + 6–8 GB download | ≤8 GB download | cleared once disk is freed (17 GB), after its literature check, with notice to the bridge first |
| cuspis | Upper-bound literature sweep | no compute | DONE (898cfcf): no published cap mechanism |
| cuspis | Free-field lattice test of the wedge mutual-information statement (Sumit go), then write-up | 1 core, <2 GB, <200 MB | DONE (prereg 6785173, result 06ec09f): VOID as registered (control failed to plateau at 90°); 2.894 grade unchanged; slot released; short consolidation then stop |
| bridge | V17: independent first-order check of ansatz §153 (prereg aea5ffb, amendments 0e8de6b, 3e6557b) | 1 core, nice 10, <3 GB, <50 MB | DONE: CONFIRMED, agrees with §153 (floor at valence 1–6; controls 96/96) |
| spherex | Planetes fake-mover run (Sumit's, priority): 1 Python worker + local helper | 1–2 cores, <1 GB, ~170 MB disk total | running until ~23:15, then ~30 min of scoring on 1 core |

Committed in core use when everything cleared is running: ansatz 2 + tabula 2 + quantum 3 + cuspis 1 + deepstrain ~light = ~8.

## Overnight 2026-11-17/18 (Sumit's go ~23:50)
| Sister | Job | Slot |
|---|---|---|
| ansatz | True-fractal test, running | 2 cores, until ~8 AM |
| tabula | §200 DONE and sealed (bff2c9f, local); now the p=4/5 timing probe, then a pre-registered post-result fix round; full p=4/5 run by slot request | up to 3 cores |
| quantum | Wrapping test (after its harness and reading are committed) + ONE G3 reference worker | 3 + 1 cores, ~1.5 + ~4 GB |
| deepstrain | Public benchmark: charter first, checkpointed and pausable, downloads ≤ 8 GB; GWOSC retries for the torch regression | ≤ 2 cores, ≤ 4 GB |
| cuspis | One process (per Sumit), details pending | — |
| bridge | Idle: V17 and V19 done; V18 done | — |

Rules: nice ≥ 10; stop at 5 GB free disk, yellow memory pressure, or swap > 2 GB; nothing outward-facing.

### 2026-11-18 07:25 IST — ansatz saddle test
- The saddle test finished at 07:10 with no guard stop. The Kerr negative control FAILED, so the registered TS verdict is **VOID**.
- Cause: an R1 precision floor near Kerr's separatrix, where integration error decides which pass an orbit plunges on.
- The TS R1 data are sealed and stay unread (sha256 9876f3c9…, commit 02682bb).
- Rerun per addendum 2 (7c1e845), which carries its own verdict:
  - **Step 1:** Kerr at R2, ~2 h on 2 cores, nice 10. Granted.
  - **Step 2:** TS at R2, ~12–14 h on 2 cores. Granted only if the step 1 Kerr control passes; ansatz reports the outcome to the bridge first.
- Box at grant time: 72% memory free, 0.26 GB swap, 16 GB disk free.
- **08:33:** step 1 (Kerr at R2) FAILED its gate, so step 2 was not launched and the slot is released (ansatz 06844c5).
  - Post-hoc reading: the engine's precision floor (~1e-16) lies above the registered 1e-18 refinement.
  - Decision: not parked. Ansatz drafts a redesign proposal for Sumit (higher-precision engine, or a refinement floor calibrated on Kerr).
  - The TS embargo stays in place both ways.

### 2026-11-18 09:25 IST — tabula
- The §200 fix round is sealed (c5dd941, local; summary sha256 c40b0cd1…). Embargoed; no numbers.
- §201 (high-precision splitting at p = 4/5; pre-registration d883f03) is running on 1 core, nice 15, 600 MB cap, ≤ 24 h slot. PGID 75881, python PID 75884.
- The fix round's 2 cores are freed.
- Note: ansatz's redesign option C (homoclinic tangle) duplicates tabula §199b and the bridge's V16 replication. C is held; ansatz is checking whether its capture-edge level matches p = 3/5.

### 2026-11-18 13:02 IST — cuspis
- EXP-039 relaunched on Sumit's direct prompt (prereg fd4ee90, unchanged), restarting from V1.
- Watchdog PID 89651, nice 20. Caps: 2.5 GB memory, stops when free disk falls below 5 GB or memory pressure reaches warn. Expected peak 1.5–2 GB.
- Box at launch: pressure level 1, 72% free, 14 GB disk free.
- Also running: tabula §201 (PID 75884). Quantum's wrapping runner has finished, but no report yet.
- **13:10:** cuspis EXP-039 run 2 stopped at gate V3. Cause: double-precision noise in the EXP-038 reference at s = 6440.
  - Addendum A (dcdc7fd) adds V3′, which sums over the above-floor nodes only, plus a floor diagnostic. It is graded a post-failure amendment.
  - Run 3: watchdog PID 99122. Run 2 peaked at 1.31 GB.
- **14:01:** cuspis EXP-039 run 3 PASS: p = 1.590/1.591 against a predicted 1.60 ± 0.10. Peak 1.38 GB, no guard fired; Cuspis is now idle. Closes the EXP-038 Part C void (67987dd).
- **13:20–13:50:** bridge V20 (blind replication of ansatz §154), 1 core. The registered run was VOID; amendment 2 gives TRANSVERSE, and the blind comparison AGREES (edf46dd).
- **12:37:** DeepStrain benchmark fetch COMPLETE (64/64; in-script integrity checks OK; the GWOSC published size and stats check is still to do).
- **01:23 yellow, root cause:** DeepStrain's foreground injection golden test, run outside run.sh (no nice, no watchdog), about 1–1.5 GB on top of the fetcher. Lesson adopted by DeepStrain: all full-segment checks go through run.sh.
- **Granted:** DeepStrain oracle Y0, ~1 h on 2 cores at nice 15 via run.sh, after the GWOSC check.
- **Quantum wrapping test:** verdict WRAPPING (c22d325); all controls pass. Next step is a better enclosure design, registered with the bridge before any subdivision; nothing launched.
- **14:03:** Quantum G3 worker restarted (PID 57519, guard 57558; 5 GB cap, stops on yellow).
  - Overnight its footprint grew ~46 MB/min (0.09 → 1.47 GB over 30 min), a second contributor to 01:23.
  - Quantum reports the growth curve after ~30 min: leak, or task size.
- **14:32:** Quantum G3 worker stopped by its guard on yellow pressure.
  - Task #21 grows linearly (~61 MB/min) from a fresh start and has never completed in 3 attempts.
  - It stays STOPPED until Quantum finds whether this is a leak or a real peak, and sends a slot request.
  - At 14:34 the box showed 59% free, swap 0.26 GB.
- **14:35:** DeepStrain Y0 oracle done (e168e8d); GWOSC stats check passed (5ad8be8).
  - Peak was 3.53 GB, close to the 4 GB cap. Together with Quantum's G3 at ~1.9 GB it is the likely trigger of the 14:32 yellow.
  - DeepStrain will crop to signal windows before reuse. The Y1/Y2 memory probe (< 30 min) is OK.
- **Quantum G3 growth root-caused:** scipy solve_ivp was storing the dense step history (t_eval=None). The fix is t_eval=[], bit-identical on 8 tasks.
  - Approved: restart now, 1 core, nice 15, with G1_00_P deferred to last. The untested status −1 path is noted as a caveat.
- **14:55:** DeepStrain Y2 (CNN yardstick) GRANTED: ~1–1.5 h, 2 threads plus MPS, nice 15, measured peak ~2.4 GB.
  - Asked to report at both the new MLGWSC-style per-trigger tolerance (≤ 60 s) and a tight fixed one, scoring all yardsticks under the same rule.
- **15:21:** Quantum G3 fix confirmed (02391fb): footprint flat at 89 MB for 31 min. Worker PID 4371; G1_00_P deferred to last. Memory issue CLOSED.
- **15:25:** DeepStrain Y2 done (81fe09f), 31 min. The CNN reaches ~48 Mpc at 1/day against the oracle's 155 Mpc.
  - The real peak was 3.59 GB, against 2.2 GB declared; the source of the spike is not yet found.
  - The Y1 slot will be declared at 3.6 GB and scheduled with nothing else heavy alongside.
  - 1/month FAR is not reachable with 27.3 d of background; the plan is being corrected.
- **Cuspis moved to "Cuspis-personal"** (Sumit's second account; handover 3ed9b9a). The old Cuspis session no longer touches the tree.
  - EXP-040 (978b97c): continued in dimension D, the three anchor theories' κ/C_T cross at D ≈ 2.75 / 2.85 / 2.94. So the 13% band at D = 3 is "just past the crossings", not a general D = 3 law.
  - Partially verified (two implementations sharing the reduction route). Runs < 4 min, 0.25 GB.

### 2026-11-18 16:17 IST — Quantum moved to "Quantum-personal" (the old session is idle and off the tree)
- Fable 5.2 wrote the E-representation design (3dc0e3e). It is not registered; only offline float estimates exist (Z1 passes).
- Model attribution goes forward in commit messages; no history rewrite.
- G3 was stopped at 15:23 by system-wide pressure (its own footprint was flat at 89 MB). It is HELD until swap is below ~1 GB and DeepStrain's Y1 golden check is done.
- The status −1 path (19 of the 20 existing rows) is now checked bit-identical on 5 tasks.
- Box: swap 1.92 of 3 GB, 42% free. The second Claude app (personal account) adds about 1 GB of baseline.
- **DeepStrain → "Deepstrain-personal"** (same repo).
  - The Y1 dev golden rerun is running (PID 85036, ~20 min). The first pass was vacuous: templates were offset 5 s by pycbc's post-merger tail. Fixed in e6741cb, and the golden now requires loud recoveries.
  - The Y1 slot request comes from Deepstrain-personal.
- **Sumit's decision:** DeepStrain Y1 runs on the full 24 segments (~38 h). The slot goes to Deepstrain-personal after the golden passes.
- **Quantum-personal:** the E-representation prereg was AGREED (1496a30, 79fde97). Primary is Z-sym; ZG(256,128) is the timing-only fallback; B17 K = 5 is the existing rule.
  - Fable's "0 ∈ E not needed" was overruled by the Opus review; it is a real gate.
  - Implementation plus tests T1–T3 (light) are going ahead. The full run needs a slot after T3.
- **tabula → "Tabula-Geometrica-personal".**
  - §201 (PGID 75881) looks stuck: job 2 (TS2 ε = −0.01, dps 34) has run ~7 h against a ~10 min estimate. A suspected integrator loop; no result seen.
  - Not stopped. The new session diagnoses it before any stop or relaunch.
- **Cuspis-personal EXP-041** (EMI curve) done: ee21235.
- **16:40:** Quantum-personal Z-sym enclosure run GRANTED: 1 core, nice 10, < 250 MB, < 300 MB disk, ~39 h.
  - T1–T3 pass (9b9fdc6, bb7aa8e); amendment A1 (b9dac75); the timing-only decision is Z-sym.
  - Guard: disk stops at once; swap/pressure stops only if sustained 10 min. No auto-restart.
  - G3 still held until swap is under ~1 GB.
- **Fable task sent to ansatz-machine-personal:** is the capture edge the W^s of the §154 orbit? Reasoning first, then an Opus review and prereg.
- **16:45:** Quantum-personal Z-sym run STARTED (PID 37679, guard 37817; 96a65dd). T4 stop/resume is byte-identical.
  - Guard re-armed by the bridge: stop on swap > 2 GB AND pressure ≥ 2, or on level 4, each sustained 600 s. Disk < 5 GB and own footprint > 300 MB stop at once.
  - Reason: the kernel pressure level read 2 at 48% free.
- **20:20:** tabula §201-T blind theory prediction REGISTERED. Seals: d146f2c, e2332b4, 625a543 (note da5106c0…, json 773500a4…), hashes verified.
  - Theory by Fable 5.2; review and compute by Opus.
  - The registered per-level procedure failed its p = 3/5 validation. Variant B is post-hoc on p = 3/5 but blind to §201.
  - §201 was paused (SIGSTOP) 19:22–20:12 for the seal, and is now on job 12/12.
  - The embargo is NOT lifted (no ansatz verdict to compare).
- **20:17:** Quantum work back in the "Quantum" session (office account; Quantum-personal closed).
  - The Z-sym run is fast: t 176/292 after 3.5 h, 178 MB.
  - G3 RELEASED (swap 0.4 GB, 81% free): 1 core, nice 15, sustained-600-s guard.
- **Coordination:** sisters run on the office account with Opus; Fable only occasionally, on the personal account.
- **20:50:** sisters back on the office account. Acks and grants sent:
  - ansatz: edge-link prereg acked; build and run.
  - DeepStrain: Y1 full-24 slot granted; M11 public push held for Sumit.
  - tabula: told to hand over with Tabula-Geometrica-personal first (two sessions open on one repo).
  - Quantum G3 restarted 20:18 (PID 71097, guard 71169, 1 GB tree cap; 5db3a21).
- **tabula §201 DONE** (784e9d2): canonical splitting measured at all 3 levels; Kerr valid; 12/12 jobs OK.
  - §201-T grading (50c15b9): the splitting is polynomial/linear in h, not exponentially small (F1a passes).
  - Variant B passes F1a, F1b, F2, F3 and F4.
  - The per-level procedure fails F1b and F2 at ε = −0.03.
  - Numbers stay local and embargoed (available for a later bridge blind replication).
- **20:20:** DeepStrain Y1 noise LAUNCHED (PID 73724). The measured pace gives ~39 h for 24 segments, then fg ~6 h. Peak 2.5 GB RSS plus 3.1 GB MPS.
- **M11 public correction PUSHED** (4df3fc4): all 4 looks still UNINFORMATIVE after the +5-s shift. Out-of-domain CNN FARs not re-checked (stated in the addendum).
- **Fable task to Quantum-personal (Fable 5.2):** a general MN non-integrability theorem (routes: β-deformation/Galois semicontinuity, Poincaré–Kozlov from V19, an exponential-extension Galois argument, parameter-uniform certification).
  - Output goes to /Users/sumit/Github/fable_work/mn_general_theorem/ (outside repos); no commits. Opus review and registration follow; Quantum (office) imports.
- **20:52:** ansatz edge-link: engine gate PASS. The registered T-L3 is VOID (a Kerr must-fail control didn't fire); T-L3′ (a6274cb) passes its Kerr gate (b0fb9e3).
  - TS T-L3′ GRANTED: ~1 h, 1 core, nice 10. R1 only if a falsifying counter is non-zero.
- **~21:45: MN axis theorem (Fable DESIGN.md).**
  - Bridge V21 (30231db): C1/C2 PASS (1e-35..1e-40); static C3 reproduces −(4 + 2cosh π√3) to 1e-8. Registered VOID on V21's own floor-limited clause.
  - Quantum-personal (Opus) on worktree branch mn-axis-theorem: fresh-Opus review running. Certified C3/C0/L6 prereg AGREED with a vacuity guard; phase 1 at 1 core, nice 10.
- **21:50: MN axis-theorem certified phase 1 ALL PASS** (A1, c806979).
  - Q1–Q4 pass; T-exact holds on 22 loops; T-limit static −234.60 ± 1e-19.
  - T-L6 certified at all 4 rows, rotating p1 included.
  - Fresh Opus review (6811d2d): Theorem 1 STANDS WITH CORRECTIONS (localised class; real-analytic exterior integrals not covered).
  - Phase 2 (j = 100, 1000) GRANTED: ≤ 90 min, 1 core.
- **ansatz edge-link TS T-L3′: PASS** (4bdb161), graded a post-failure amendment, blind to TS. 67 min; slot released. Kerr T-BANDS cost is being measured next.
- **Cuspis-personal (Fable, then Opus):**
  - EXP-042A: no interacting-CFT κ exists in print; toy base rate for the clustering registered.
  - EXP-043: Einstein's κ/C_T curve is the Mellin transform of a profile with a sharp edge at t = π/(2e); all 4 registered predictions pass, so each curve pair crosses exactly once for D > 2.
  - Partially verified (lemma not read at source). Light compute.
- **ansatz edge-link: the registered T-SWITCH is VOID** (control failures, dd7dbdc). T-SWITCH′ controls pass (df66777).
  - TS T-BANDS plus T-SWITCH′ GRANTED: ~1.3 h, 1 core.
  - Grade: two post-failure amendments, blind to TS.
- **~22:30: MN axis theorem certified run PASS** (branch mn-axis-theorem, tip 7d5a2fa, 11 commits, not pushed).
  - T-exact holds on 66 loops; T-limit is 19.6/j² (matches V21); T-L6 certified at all 4 rows × 3 j.
  - Lean 12/12 (L6_gl2, standard axioms). Disclosed: Lean peaked at 2.8 GB, over the 2 GB per-task figure.
  - Revised THEOREM.md (Opus) states the localised class; real-analytic exterior integrals are not covered.
  - Merge into main is for office Quantum (regenerate Certs/All.lean).
  - Personal account near its weekly limit, so the next Fable task waits until Thursday.
- **~23:45: ansatz edge-link VERDICT NOT ESTABLISHED** (dc06b20, §155).
  - T-SWITCH′ found no certified strand pairs; T-BANDS certified none of its edges. T-L3′ (one-way gate) stands.
  - Post-hoc diagnosis: the bisection predicate was not owned by γ. A redesign proposal is next; nothing run.
- **Sumit's go:** ansatz edge-link redesign (a5daf8e). Steps: prereg first, then Kerr and must-fail controls, then TS. ~1 h, 1 core.
- **23:20:** ansatz edge-link v2 (prereg 60ccf93): registered controls VOID; v2′ (fde95e2) controls all PASS (187b233).
  - TS window run GRANTED overnight: ~3.5–4.5 h, 1 core, checkpointed.
- **23:36:** Quantum combined Lean build PASSED (3073219): 9028 jobs, rc 0, no "declaration uses sorry", peak ~1.05 GB. The MN axis-theorem certificates are now in the full Lean build.
- **~00:20 (11-19): Fable bounded task** (Quantum-personal, last ~4% of the other account): fable_work/axis_integrability_classification/NOTES.md, all HAND.
  - Claim: for rational axis f0, the axis NVE is solvable for all E iff deg f0 ≤ 2. Kerr passes; ZV δ=2 passes; rotating TS δ=2 FAILS (deg 4: 8 simple points, SL2 at generic E).
  - Bridge quick check: its own TS2 loader gives axis f0 of degree 4 (ts45, ts35); Kerr degree 2.
  - TODO (morning): pre-register a V22 check (numeric and certified monodromy of the TS axis NVE at generic E, plus the classification lemma), then review. This could give an analytic all-energy TS non-integrability theorem in the axis/meromorphic class.
- **~01:xx (11-19): Fable Parts A and B done** (fable_work/axis_integrability_classification/: THEOREM_TS.md, ONLY_KERR.md, LOG.md, checks/).
  - Part A, claimed: TS δ=2 is not meromorphically integrable on the axis orbit at every E ≠ 0 (8 simple points generically; 4 simple + 2 double at E²/μ² = 1 + 1/|q|). The general f0(p, q) is checked against the Bridge transcription.
  - Part B: the axis test is blind to the twist. A third-order VE sees it, but "only Kerr" remains a programme.
  - MORNING: pre-register Bridge V22 from THEOREM_TS.md section 5 (T-a..T-d), then a fresh-Opus review.
- **Overnight: ansatz edge-link v2′ VACUOUS** (73ac61a, §156). The vacuity guards failed (close passes to γ are rare), so no bisections ran.
  - The ownership-slope test is validated (Kerr separatrix ½, γ 1, artefacts 0).
  - New proposal (bisect on the 300-crossing fate, classify by slope) waits for Sumit. Nothing running.
- **08:35:** Quantum A2 pre-tests T1r and T4r PASS; REDO amendment and A2 REGISTERED (858234f).
  - main run at step 1460, maxE 1.2e-2, tracking the REDO-off blow-up.
  - main_redo launches once the main run's registered outcome is recorded.
- ansatz v3 TS window running (~3.2 h, Sumit's direct go).
- Bridge V22: T1 and T2 PASS (exact); T4f TS T-a non-commuting. Remaining T4f and controls rerunning (PID 30460).
- **Quantum Z-sym main run (REDO off): registered outcome FAIL** (22e5b70). THREW at step 1478, t 289.12, before the checkpoints; controls all held.
  - read_result.sh printed INVALID; the Bridge ruled the prereg text governs, so FAIL. Setup-mismatch caveat kept.
- G3 was guard-stopped 09:46 by the Bridge's V22 leak; restarted 10:27 (PID 56367).
- main_redo LAUNCHED 10:28 (PID 56446, 8c8d190), ~35–45 h; own-footprint cap raised to 500 MB in advance.
- **~13:30: ansatz edge-link v3: NOT ESTABLISHED** (609bc49, §157). The window switches are beyond pointwise resolution (long chaotic transients).
  - Chain net: the one-way gate holds; the ownership instrument is validated; the link is unresolved. §150 wording stands.
  - ansatz recommends closing the pointwise line. The Bridge suggests rethinking via a rigorous one-way-gate argument (see message to Sumit).
- **23:45:** Quantum G3 switched to 3 claim-based workers (PIDs 37214, 37246, 37279; guards 37219, 37251, 37291), 1 core each, nice 15, ~90 MB each.
  - Gates passed (485d857): bit-identical reruns, and a dummy-claim test.
  - 14 tasks remain; ETA ~6–10 h. G1_00_P misattribution fixed forward (6867aa0).
- **11-20 05:03: DeepStrain LongChirp benchmark COMPLETE** (e144731).
  - Y1 bank: 57.5 Mpc @1/day; Y2 CNN 48.4 Mpc (own var) or 25.5 (±1 s); Y0 oracle 155 Mpc.
  - Y1/Y2 ratio 1.19 [1.10, 1.29] @1/day.
  - Memory: y1fg peaked over its declaration (4.06 GB); the watchdog stopped it 3×. Root cause: a pycbc TaylorF2 per-length leak; fixed with short-lived children.
  - Release/DOI and the README need Sumit.
- **11-20 08:40:** Quantum B15 counted run LAUNCHED on Sumit's direct go (PID 78628, guard 78639, nice 10). Kerr control with the rust map, then the G6 auditor; < 2 h, < 1 GB. The G6 design was agreed by the Bridge with the red-flag near-miss change.
- Running alongside: Quantum main_redo (since 11-19 10:28).
- Bridge V22 done (f1eb2cf): every substantive test passes; registered VOID on the Bridge's own ZV clause.
- **11-20 13:00–14:05: Bridge V24 C1′ and V25 P2–P6** (each 1 core, nice 5–10, ≤ 130 MB; footprint_watch now guards
  the process tree). All DONE: V24 C1′ PASS (0f9809a); V25 P2–P6 CONFIRMED (1812a8a).
- **11-20 13:33: Quantum Melnikov stage-1 certification relaunched** after its own nan bug (0129c88; launcher 10918,
  guard 10928). Jobs: L2, L1, the ∂M and ∂a variants, the sabotage. ~2.5 h.
- **11-20 16:05: Quantum Melnikov stage 1 CERTIFIED-NONZERO** (d338e00). Theorem A′ is now unconditional (small β).
  Stage 2 (L4 + T3) is next, with its T3 design to be reviewed by the Bridge first.
- **11-20 afternoon: ansatz §158** (5f14db2): the axis first-order classification is confirmed at generic E (closes
  gap K1).
- **Bridge V24 addenda D and E:** brake-cap fix PASS; crossings symmetric (E2).
- **11-20 17:46: Quantum Melnikov stage 2 counted run LAUNCHED** (4d94bd4; launcher 92782, guard 92796 with a 1 GB
  cap; nice 10). L₄ is already certified (cabccc9). The C bound uses the Cauchy–Schwarz route S2-A2, with the Bridge's
  4 conditions. Order: known-value control, 2 must-fail points, then 16 grid points → T3.json. ETA ~04:00–05:00 on
  11-21. CERTIFIED-NONDEGENERATE if any counted point closes.
- **11-20 evening: DeepStrain LongChirp v1.0.0 PUBLISHED** (Sumit approved).
  - Tag longchirp-v1.0.0; DOI 10.5281/zenodo.24399603 (concept DOI 10.5281/zenodo.24399602).
  - Author "Independent researcher", with ORCID and an AI-use disclosure.
  - pycbc issue gwastro/pycbc#5554 filed.
  - Name collision on Zenodo with an unrelated "ZahraZali/DeepStrain" record (Sumit's call).
- **11-20 22:33: Quantum B15 counted run + G6 DONE** (85af9f0).
  - Step 2 is UNRESOLVED by the registered rule.
  - Post-result reading: all 147 accepts are robust at 1e-14 (81 with measured error, 66 extrapolated). The unresolved
    part is rejects and red flags only.
  - Estimates, not bounds. Steps 3-4 (rigorous coverings) come next, after Melnikov.
- **11-20 evening, other runs:**
  - tabula §202 (Adam→L-BFGS, CPU, ~01:15);
  - Cuspis EXP-044 (determinant route; G1 FAIL as registered, G1′ labelled);
  - DeepStrain real-background cascade (waiting for the box-free signal after tabula);
  - ansatz: a blind twin of V26 B8.
- **11-20 23:16: tabula §202 done** (aee869a, local only, because of the embargo). INCONCLUSIVE as registered (no arm
  reaches relL2 < 0.20).
  - Demonstrated: with L-BFGS the loss went down while the field error went up, on both seeds. That retires "the wall
    is compute".
  - Most likely, the frozen-set loss doesn't pin the solution. That is UNTESTED: n = 2, field error not tracked during
    training, and the loss weighting is a confound.
  - Any follow-up needs its own prereg and Sumit's go.

### 2026-11-21 02:44 IST: tabula §203 DONE
- 12/12 jobs exited 0; every gate passed.
- Registered verdict: 2, H-coll SUPPORTED (sealed 13469fc, local).
- The support is thin. The mechanism holds together in seed 1 only, seed 0 is a counterexample, and seed 2 does not
  replicate.
- Bridge asked for three things:
  - report the limitation in the same sentence as the verdict;
  - fix L-BFGS stall detection, with a must-fail control;
  - pre-register, but not run, the "loss pins the solution at a residual of about 1e-5" test, for the morning.
- The Mac stays quiet overnight: Gemini is using Chrome memory and DeepStrain is on hold.

### 2026-11-21 ~03:15 IST: tabula §204 full run GO
- The test starts training from the true solution. Estimated 1–1.3 h, peak ~0.9 GB.
- Gates: 50% free per job, abort below 35% free, 1.5 GB cap.
- The feasibility fit reached gate O (0.0199). The oracle is not reused.

### 2026-11-21 ~05:30 IST: Cuspis PAUSED at f70c92b (self-stop on slip rate)
- Four registration slips tonight; all were caught by controls and none changed a conclusion.
- New mechanism: every prereg carries a control table, and no must-fail is registered without a pre-check file.
- The stage-B spec is in report.md for a cold resume.
- Morning decision for Sumit: resume with Opus, or a compact Fable brief on the growth of Σ̃′ along Im α.

### 2026-11-21 04:19 IST: tabula §204 DONE
- Verdict 5 MIXED: PIN in 2/3 seeds.
- The POSITIVE CONTROL FAILED in 3/3, so the instrument cannot tell "stable" from "stuck".
- Secondary: frozen-set drift away from the truth, 3/3 (but Adam on fresh points drifts too).
- Descriptive: releases lower the IC/BC terms while the field leaves the reference.
- Bridge asked for a zero-training consistency check first: do the PINN loss and the FD reference define the same
  problem? Pre-register, then run.
- The box is free.

### 2026-11-21 ~04:55 IST: tabula §205 DONE; §206 GO
- §205 verdict INSTRUMENT FAIL: the relative clauses assumed small baselines (one of them was the Bridge's
  suggestion).
- Descriptive finding: the PINN loss and the FD reference agree on PDE and IC, and DISAGREE on the inner boundary
  data at r = 0.1. That comes from FD-600's truncation error near the origin: S-sized, about 20× the PINN BC level.
- §206 GO, pre-registered first: switch the BC/IC data source to FD-2400 (minimal change) and repeat the §204
  R-Adam release.

### 2026-11-21 05:08 IST: tabula §206 stopped by its own side guard (pressure level 2, 42% free); resumed ~05:35
- Cause: Chrome at about 5.9 GB (three Gemini sessions) plus the FD-2400 dense solve. tabula's job was not the cause.
- The resume is from the cache: the heavy solve is done and the remaining stages peak around 0.9 GB. Same gates.
- Lesson: with three Gemini Task sessions open, Chrome's footprint grows with page length. Close finished Gemini
  tabs before heavy local jobs.

### 2026-11-21 ~05:45 IST: tabula §206 stopped by its in-job watchdog (1,574 MB > 1.5 GB cap); launcher hole found and fixed
- watch_footprint.sh always exited 0, so every `|| stop` behind it was dead code (silent_nulls 75). Fixed in 0c49b80,
  with a known-fail test and an audit of every caller. §204 is unaffected: its asserts held.
- Protocol deviation: the oracle fits ran before B0. Bridge decision: refit after B0; keep the early fits set aside,
  labelled unused.
- Relaunch GO, after a deliberate cap-breach dummy job confirms the stop now works.

### 2026-11-21 06:12 IST: tabula §206 DONE, verdict 2: BC data did NOT drive the drift (UNCHANGED 3/3)
- The corrected loss scores the truth at L = 3.4e−7, at PINN level.
- Releases from the value-fit oracles still walk to 110–1000× higher-loss basins, about 0.1 away in field error.
- The oracles start about 1000× above the truth's loss (mostly IC misfit).
- §207 GO (prereg first): a representation test. Can hybrid oracles (value plus physics terms) sit near the truth
  at low loss? Then release from them.

### 2026-11-21 06:50 IST: tabula §207 DONE, verdict 1: REPRESENTATION LIMIT (scoped: upper bound, ladder not flattened)
- Near-truth hybrid points have loss 20–34× the truth's (gate 10×).
- Descriptive: they are 3–50× LOWER in loss and 6× closer to the truth than where the §206 releases ended. So the
  drift is a path effect, not the loss preferring a far solution (a reading, not registered).
- §208 GO (prereg first): release from the hybrid points with §206's exact settings, plus a descriptive arm at 10× lower lr.

### 2026-11-21 07:11 IST: tabula §208 DONE, verdict C MIXED (PIN 1/3)
- Descriptive, and informative: at lr/10 the loss falls, the held-out residual falls and IC/BC fall in all 3 seeds,
  yet the field drifts smoothly away from the truth (0.017 → 0.035–0.038). That is the §203-seed-0 pattern, now 3/3.
- Reading (not registered): there is a step-size walk PLUS a tilt (descent within this network moves away from the
  truth).
- §209 GO (prereg first): saturation, lr/10 over a 4× budget. §210 (capacity ladder) to be drafted; it runs after
  §209 with a go.

### 2026-11-21 07:38 IST: tabula §209 DONE, verdict 1: DRIFT SATURATES (3/3)
- At small lr the drift plateaus at +0.020 to +0.025 (about 5× the reference uncertainty) after about 6k steps,
  while the held-out residual keeps falling.
- Reading: a bounded offset to a nearby basin.
- §210 GO: a capacity ladder ("does the ~0.02 offset shrink with width?"). Cost probe first; flag the Bridge if over
  about 4 h.
- **~07:50, §210 cost probe.** Every rung fits the enforced footprint cap (≤ 1.12 GB). In-process maxrss reads up to
  1.86 GB at w256. Bridge decision: option A (full ladder, footprint cap, maxrss recorded), about 2.8 h. Running
  ~08:00–10:50.
- **~10:57, §210 relaunch-2 stopped by the side guard** (level 2, 48% free) during the first matched-step-size release.
  All 9 primary releases had finished. Cause: three Gemini Task tabs open in Chrome plus the w256 peak. The Bridge
  closed the Gemini tabs (67% free) and gave GO for (a). **Run 4 launched** (process group 22210, side guard on, 68%
  free): pre-check and eqcheck, then the 3 matched-step-size releases (2.5 GB cap), then the registered analysis.
  Gemini rule from now on: close each tab after sending its Task, and keep at most one open while heavy jobs run.
- **~11:50, Quantum Melnikov stage 2: still running.** PID 92792, up 17 h; 12 of 16 points COUNTED, none closing yet.
  The best column is tau = 0.6, where the deficit falls ~17x per +0.03 in sigma. An extrapolation (not a result)
  says sigma = 0.13 might close narrowly. New ETA ~17:00. If nothing closes, the verdict is OPEN; any amendment
  (larger LAM_I or the sigma range) is decided after the verdict, labelled.
- **~12:00, tabula §210 DONE** (edadf1a / 904a54d). Verdict C MIXED, per seed NONE / NONE / SHRINKS. Going from w64
  to w128 halves the offset (~0.02 to ~0.01) in every seed; w256 adds nothing, and depth helps about as much as width.
  Release step size was ruled out by the lr-match arm. tabula's floor prediction was wrong (0/3). Confound found:
  the w256 hybrids start less well fitted. **§211 GO:** w256 fitted to a matched start quality (registered
  criterion, budget cap), then the same release. If it still doesn't beat w128, the width thread parks with the
  statement "the offset saturates at ~0.01".
- **~12:10, Cuspis stage B/C** (77d489f). Lemma U (e) now reduces to the growth rate of C+(1/2+iy) alone: is it
  < 2pi? The Born rate is pi; the resolvent may add more. Every other factor grows polynomially (partially verified).
  The Bridge asked Cuspis to pre-register its own direct C+ rate measurement (controls: Born gives pi; a planted 2pi
  term is flagged), so that T20 becomes a cross-check rather than a blocker.
- **11:55 (real clock), V26-K DONE:** Neon T19's closing of the G1 gap is independently confirmed. K2 is FAIL as
  registered (a Bridge enclosure blow-up); amendment K2′ PASS; K0, K1, K3A, K3B, K4 (28/28) and K5 PASS. ansatz told.
  Only-Kerr pre-outreach still open: ansatz gap B, and T24 (the referee of the K5 theorems; not needed for Only Kerr
  itself).
- Timestamp note: the Bridge's "~" times from 11:40 to 12:35 in today's logs ran 20-40 min fast; the git commit times
  are the record.
- **Cuspis, CH05 Painleve route** (a5c8abd, pre-checks only, NOT registered because of a discrepancy).
  - The route gives a resummation ratio of O(1) on the line, so C+ would grow at pi and (e) would be log-free.
  - It agrees with T20-v0 at first order (0.08% at alpha = 0.1) but differs at higher orders (1.8% in C+ at
    alpha = 0.3).
  - One step is argued, not proven.
  - The Bridge gave GO for a third, direct method (2D same-tip coefficient at alpha = 0.3, <= 0.5%), with known-answer
    controls and a must-resolve control. T23 is still held from Cuspis.
- **tabula §211, launch 1 stopped** by the 1.5 GB fit cap (w256 seed-0 hybrid at 1,563 MB; ops log 4061d6d). The
  pre-check had passed in full. Bridge GO for a labelled operations amendment: w256 hybrid fits get the 2.5 GB cap;
  the rest is unchanged; resume skips the finished work. New cost estimate 4-10 h.
- **V28 SEAL (b93cb63).** The Bridge re-implemented T20-v0 and T23. At twist 0.3, Cuspis's CH05-route ratio 1.162
  matches T23's 1.16274, and Cuspis's T20-v0 1.141 matches the Bridge's 1.140946. So the CH05 route and T23 look like
  the SAME resummation.
  - Twists 0.2 and 0.4 stay sealed for a blind comparison.
  - T23's corrected first-order closed form follows from its legs (confirmed to 1e-14).
  - Cuspis was warned that "Born at u = 3" is contested, so not a must-pass. BIE referee GO; Neon to build a second
    BIE blind from Cuspis's spec.
- **ansatz gap B:** prereg 98b54e9; the registered run is going (PID 94001); controls C0, C3a/b, C1 and the guards
  pass.
- **tabula §211, launch 2:** running (group 24603), amendment 569bec1.
- **Cuspis:** the blind test MATCHED, so Cuspis moves to stage C (registered C+ growth along 1/2+iy via the CH05
  route). Neon T25 does the direct BIE referee; Cuspis builds its own BIE only if T25 is ambiguous.
- **12:10, δκ first-order normalisation, effectively settled.** At twist 1/2, Cuspis's symmetry-fixed absolute CH05
  values equal the Bridge's T23 implementation to 1e-7 (linear = (4/pi) x Born; resummed -0.00599707). Born is
  excluded there by 27%. T23 is released to Cuspis. Stage C proceeds; the T25 BIE stays as the direct referee at 0.3.
- **12:20, ansatz gap B PASS** (prereg 98b54e9, result e0bb4d0; post-hoc labelled finite-subgroup exclusion fdf16d5).
  K*(0.6) has no points in [-10.5, 4.05] (50-digit argument principle). The theorem stays "all k except a discrete set
  K*(spin)". Gap B is evidence, with caveats: floating point, one spin, nothing below -10.5, first-order lower-axis
  NVE. No further runs. **All Only-Kerr pre-outreach checks are now done.**
- **12:34 Cuspis EXP-066 (8e5f336):** T25 code read in full and rerun (identical). Shape test vs CH05: constant to 2-4e-5. NEW absolute cross-coefficient test: 12 slices to ~2e-4. Real-twist C+ VERIFIED (four routes). Line growth partially verified (y <= 5); the all-y bound is open (T26). Next: the Lemma U write-up.
- **12:37 HOLD (Sumit):** no new starts until Sumit has discussed ~/Downloads/FLEET_IDEAS_2026-11-21.md with the Bridge. Running: tabula §211 and Quantum Melnikov (monitor only). Cuspis holds (T26 check only); DeepStrain and ansatz idle; all Gemini accounts idle.
- **12:39 CLARIFIED (Sumit):** the hold is ONLY on NEW directions. Current threads continue, with Gemini: Only-Kerr finish, Cuspis delta-kappa, K5 write-up, MN Melnikov, §211, the existing drafts.
- **12:47 current-thread progress:**
  - **Cuspis:** Route A withdrawn (a two-branch-line flaw); SC is now primary. Gates adopted. Bridge GO to source
    reading, with three points (measure the "scaleless" saddle; a planted Abel-Plana failure; final-error wording).
  - **ansatz:** both drafts at v1 (a03e1da). The Bridge read the rank-3 note and its cover: five points; pre-send
    condition = a RESULTS entry for cg_recheck. The TS/MN paper is still to be read in place (embargo).
  - **ONLY_KERR digest:** section 13 added (today's results and provenance).
  - **Quantum:** the embargo flag was a false regex match; no change.
- **12:52 Cuspis:** delta-kappa step 2 (source reading, d6d2918): Petkou C_T 1/N = -40/(9pi^2); Sigma normalisation anchored to MZJ eta_1. T27 gap (I) VERIFIED (EXP-068); Cuspis's B(4) = 6.78e-2 withdrawn as a float artifact, and T27's 6.871e-2 stands. GO for step 3 (prereg first).
- **13:13 Cuspis EXP-070 (091b3db):** checked T30 numerically, plus Steps 2-3 by hand. The Bridge line-checked T26's contour-shift Bessel bound (an analytic chain, spot-checked to ratio 0.976). Remaining before VERIFIED: a second line-check of T30 Step 4 (asked of Cuspis). EXP-069 (complex-a BIE validation) is registered and running.
- **13:14 Lemma U (e) VERIFIED for all y** (Cuspis 66940fb): |C+(1/2+iy)| <= C(1+|y|)^2(1+ln(1+|y|))^3, from Neon T26+T27+T30, each step line-checked by Cuspis and the Bridge plus numerics. Still open on Lemma U: (a), (b), (d) and the family choice (argued); (c) partially verified; Sigma' all-y. EXP-069 running.
- **13:27 Lean pass requested** (Sumit; credential-independent trust): Quantum to build an Only-Kerr glue file. Contents: the E-elimination identity, the Curzon traces, the T19 case-split logic with the certificates as hypotheses, and optionally the K5 constants. Limit 2 cores / ~3 GB. DeepStrain asked what it had queued (GO if <= 2 cores / 2 GB). Box at that time: load ~4.7/10, 69% free.
- **13:35 Quantum Lean glue DONE** (a62e717): lean/ZiglinCert/OnlyKerr. 16 theorems, no sorry, standard axioms only:
  - the E-elimination identity;
  - the Curzon traces (with the inverses checked);
  - the T19 case-split glue down to G1 != 0, with the certificates as named hypotheses and rescaling lemmas;
  - the K5 constants (exp bound > 46).
  The README lists what is NOT checked. 2.66 GB RSS. ansatz told that the rank-3 cover is obsolete (the Galajinsky exchange was Oct 16-20).
- **14:02 Cuspis EXP-069 PASS** (8db9026): the complex-twist BIE is validated against two separate anchors (Fredholm E_pred at 5 points; CH05 shape to 0.07%); the planted 2% is caught at 7 sigma. The y = 2 point is the hardest (Im leak 5.5e-3). GO for step 4, K-free (registered; tolerance from a measured ladder; counting-factor must-fail; full SC code-path coverage).
- **14:12 Cuspis EXP-071 K-free:** KF1 PASS (kappa_free = 0.0396481); the counting must-fail fired; the secondary clause FAIL as registered (a rounding-interval slip vs CHL09). **Sumit chose option (i):** Tier 1 (the linear SC terms) plus a measured Tier-2 size estimate with a pre-registered decision rule, then back to Sumit.
- **14:24 Cuspis: option (i) is ill-posed** (the Tier-1/Tier-2 split is gauge-dependent; a toy shows exact cancellation; e4ffec0, 77f10d0). Earlier Z-factor and cut-reduction steps withdrawn. **Sumit chose (v) + (iv):** a Neon brief for a gauge-invariant, edge-localised representation (Cuspis writes it; it goes to /u/2 as T31), plus a write-up of what is settled.
- **14:46 tabula §211 launch 2 stopped** by the side guard at 14:45 (level 2). Cause: Cuspis's exp073 at ~1.9 GB plus the §211 job. Before the stop: all 3 seeds MATCHED; primary labels BEATS/BEATS/BEATS (outcome 1); the fit-budget control was done for seeds 0-1. GO to finish the seed-2 control and analyse (60% free). Cuspis asked to declare footprints and guard runs over 1 GB.
- **15:04 tabula §211 DONE** (8ca1708/fea1b35): verdict 1 (width helps at a matched start), qualifier 1b (not separable from fit budget). The w128 control at k = 2 drifts as little: the lever is fit budget via start quality, and drift is about the start distance (Pearson 0.94, post-hoc). **GO for §212:** one registered test of the drift-about-start law (start ~1e-3; falsifier: D stays ~3e-3), then the PINN chain parks. Cuspis given GO for EXP-073(b) (~3 GB step, guarded); tabula launches after it.
- **15:06 box schedule:** Cuspis's light EXP-073(b) steps now (<= 2.5 GB) -> Cuspis's 6 GB slot (two W=64/t=1 steps, one at a time, 7 GB cap) -> tabula §212 on the Bridge's 'go §212'. The cause was Cuspis's SuperLU workspace (3-4x the LU fill), not anticipated; its own cap fired.
- **15:13 Cuspis EXP-073(b) (3c3d395): INCONCLUSIVE as registered.** T31's free isospectrality is consistent at the few-percent level, not verified at 2% (slow, sign-changing W-convergence; rule-VIII slip noted). T31's own K1 miss is explained by its small box. The open question for delta-kappa is sigma-side well-posedness with the true 3D bubble: a design decision for Sumit. Cuspis holds. **go §212 given to tabula.**
- **15:34 Sumit delegated the delta-kappa next step to the Bridge.** Decision: theory first. Cuspis writes BRIEF_T35 (sigma-side well-posedness with the true 3D bubble: is I - K_sig identity plus trace class? If not, a minimal gauge-invariant fix) for Neon /u/2. A cheap registered Richardson (iii) on the free side if it stays under 1 GB. No W=128 and no sigma production code before T35 is checked. Gemini: T33 (/u/1) and T34 (/u/0) still running.
- **15:38 T35 sent (/u/2):** sigma-side well-posedness for the true 3D bubble (Cuspis's brief, verbatim; 8.1k characters arrived). All three accounts busy (T33, T34, T35). **Cuspis EXP-074 (iii):** free isospectrality of the leading eigenvalue VERIFIED at <= 0.4%, two routes x two twists x two t; lambda2 under-resolved; overall INCONCLUSIVE as registered, with no FAIL. **Sumit:** 'time is not a worry'; multi-week work is acceptable when warranted.
- **16:02:** T36 sent (/u/2): Cuspis's correct n -> 1 sector-continuation brief (7.9k characters arrived). T37 sent (/u/0): the consolidated K5 write-up. T33 DONE (/u/1): beta* = -0.206224720 +- 3e-9 and a homoclinic pitchfork window; consistent with Quantum's finding; forwarded to Quantum with the downloaded code. /u/1 free. **Quantum main_redo (E_REP A2) PASS** (7d56c34; reported ~11 h late because of a watcher hang). Next checkpoints to be planned with Quantum.
- **16:11 Quantum:** main_redo section-5 diagnostic done (a87eea3). GO for the continuous registered run R1-R4 (~62 h, 1 core; checkpoints at 295.9, 581.8 (deferred), 793-805 (second swing), and the return at 1018.7), after the Melnikov counted run ends. Amendment A3 to be drafted with stop conditions (harness error, guard, per-step cost > 2x).
- **16:15:** Quantum A3 (68b94bc) AGREED, now registered (5 time checkpoints judged; sections deferred; launch after the Melnikov verdict). Cuspis is checking T36 (E1-E6); the Bridge transcribed T36 verbatim to neon_work/dkappa/T36_full.md. Neon /u/2 asked for the T36 code and the straddle question (A).

### 17:24 updates (2026-11-21 evening)
- **Sumit: no cost constraint for the fleet** (he tracks the limits himself). Broadcast to all 5 research sisters. Still in force: no Fable, the box RAM guards, and the new-directions hold.
- **tabula §212** sealed (cdae910): C MIXED, non-discriminating. The PINN chain §202–§212 is PARKED.
- **tabula §213 GO** (C anomaly, queue item 1; prereg 271e0bb, amendment 1bd97c1): ~2 h, 1 core, cap 1.5 GB; first, one full-length integration to check how RSS scales.
  - FINDING: §191 M1/§191b and leg 6 used sub-polar-period arcs (window 6 units vs a 22–30 unit half-period). So "C varies 40.8× less" is a short-arc statement and must carry that qualifier.
- **Quantum B15c REGISTERED** (a126a6b): the Kerr negative control for steps 3–4 (T1 #4155, T2 the 80 measured accepts, T3 the 66 extrapolated; vacuous-pass guard; a discriminating HH-based planted reject). Runs after the Melnikov verdict and the A3 launch.
- **DeepStrain:** doc fixes 0ef19d0; idle (everything else is a new direction).
- **Cuspis:** a 120-digit honest Q(n) to n = 90, to split the P5 gap between the q = 0 and q ≠ 0 sectors; T40b is on Neon.
- **17:27 Quantum Melnikov stage 2: CERTIFIED-NONDEGENERATE** (77073c2). The counted point (σ, τ) = (0.13, 0.6) closes with margin +1.5242e-5 (T3 = 68% of |L2|); 15/16 points don't close (thin margin, disclosed). All gates and controls pass; Bridge spot-check of the margin arithmetic agrees. First order in β at (M, a, r_u, z_m) = (5, 3, 16, ½) only; nothing at fixed β or in the β* window.
- **17:27 Quantum A3 main_cont LAUNCHED** at 17:26 (PID 40882, nice 10, 197 MB). The 30-min EARLY-COST check is pending. B15c-1 (the orientation-fail clause) is agreed; the driver and scorer come next.
- **Cuspis:** P5 = −1.420722 WITHDRAWN (47e4aa9). The confluent-control extension fires. T40's −1.386872 is favoured, pending the 120-digit data and a held-out fixed-base fit.
- **17:38 ansatz §162 (10b77ad):** window [3.95, 30/7 − 1e−12] has NO exceptional k at spin 0.6, E 0.8 (argument-principle counts over 15 functions, zero zeros; Kerr imprimitive must-detect and truncated-series must-fail both fire). Combined with gap B and the §161 endpoint, K*(3/5) ∩ (0, 30/7] lies only in the open sliver (30/7 − 1e−12, 30/7), sampled non-VA. Scope: 50-digit floating point, first-order lower axis, one (spin, E). Suggested next: the same pipeline at more spins, plus the exact digest claim sentence.
- **18:12 Cuspis EXP-080 (3715907):** P1 pre-checks all pass. The free calibration shows the Dirichlet BOX dominates (κ_lat/κ_free = 0.32 → 0.92 for r = 2 → 32, ~1/r), not the spacing; a dense σ side at r = 8 needs ~7 GB. **Bridge decision: option 3.** A lean P1 now (W = 2–3, r = 2–6, the ratio estimator R(r), r = 6 held out, the 2σ sign rule, plus: validate the ratio premise, a (ln r)/r model-spread form, the free side as the planted control, a registered N_y tolerance). In parallel, a P2 matrix-free / edge-localised design, with a Neon brief to follow.
- **18:23 Sumit APPROVED a quiet-night r = 8 run for Cuspis's lean P1** (W = 2, N_y = 64; measured ~6.3 GB, cap 8 GB; ~8–18 h; one process). It is to be registered as an EXP-081 amendment BEFORE any EXP-081 result is seen; per-β checkpointing is added and tested first. Sumit picks the night and quits the Claude app for it. **PENDING: the night.**
- **18:24 Cuspis STOPPED EXP-081:** the engine omitted the saddle term (T_saddle), so it computed an incomplete, box-divergent quantity. The no-saddle values seen were R = −48.5 and −69.4 at r = 2 and 3, growing with the box. Root cause: P0's P2 cancellation was checked only analytically, never through the engine. Fix: EXP-081a adds the saddle term, registered before any saddle-included value, together with the r = 8 amendment. Bridge controls: normalisation; lattice P2 d·r → −1/32; a saddle-OFF regression reproducing −48.5/−69.4; G1 with the saddle at 0; the box trend reported as a diagnostic, not a criterion.
- **Night r = 8 run:** Sumit chose launch variant (b): no memory cap, a 2 GB disk floor only. It starts after the daytime EXP-081a production finishes (~00:00–01:00). **PENDING: Sumit picks the night.** Launch command in Cuspis 8021ab2 (run from corner_function/scripts).
- **18:39 Quantum B15c COMPLETE (73230b5):** B15 prediction NOT TESTED (no chain reached hs_cover; 147 candidates = 13 distinct refinement paths). Control 3 passed on the sealed hh_swap. FINDING: the B14 frames are numerically singular on Kerr (sin∠(U,S) down to 6e-11, i.e. W^u = W^s).
- **18:39 B15d approved** (3a2e55b), plus a required frame-recipe POSITIVE control on HH (the same (U, U⊥) recipe must still certify HH, or a Kerr CERTIFIED-FAIL counts only as soundness). Slot: 2 hs_cover now, 4 after Cuspis's production ends. On the r = 8 night, Quantum STOPS its hs_cover runs first (A3 may continue).
- **19:04 Only Kerr, T38 gaps 1d (the k = 30/7 endpoint) and 2a (G1⁰ = C*) are CLOSED by two independent routes:** ansatz §161/49ade38 and Neon T41. ansatz confirmed the κ² match algebraically: (μ²−E²)β² − μ²c/2, giving a²(1−E²) for Kerr. Remaining:
  - the sliver (30/7 − 1e-12, 30/7), with T48 running for an explicit δ0;
  - spin coverage, with ansatz running a = 0.3, 0.8, 0.9;
  - an E = 1.5 point for §161, queued with its own prereg;
  - the write-up items (MRS punctures, integrability-class framing, citations).
- **19:08 Cuspis EXP-081a HALTED, no verdict:**
  - (A) The watchdog killed it at W = 2, r = 6 (1.94 GB, memory accumulating across geometries).
  - (B) A precision defect: the edge-to-wall cut makes G^(½+is) grow like e^{2πs}, so the edge g(s) is numerically destroyed beyond s ≈ 2, and a spurious pole near s = 4 appears at r = 4. The edge-saddle R values seen are erratic (1.82, 3.62, −237, 21.5). Integer-n checks pass, because they never probe large Im α.
  - Next: EXP-081b (a pole cutoff, registered 𝒞 truncation with a reliability criterion, a fresh process per geometry). The Bridge added: analytic angle-scaling balancing, an extended-precision referee control at s = 2–4, and a sign decision only if the truncation variants agree.
  - **The night r = 8 run is postponed until EXP-081b passes.**
- **19:12 Cuspis EXP-081b redesign APPROVED:** a strip PAIR (W = 2 and 4) in the same box, so no edge configurations and short cuts only. The free-side box systematic is measured at ±4%. P = 4..12 with P = 12 held out; 40-digit referee; 𝒞 tail both ways; fresh process per geometry; ~1.4 GB peak. The night run becomes a P = 16 strip pair (~6 GB, to be re-measured and re-registered) and stays ON HOLD until EXP-081b passes.
- **21:03 tabula §213 (45084dd): INSTRUMENT FAIL (C0).** The Kerr control orbits got only 1–2 polar sign changes, because the half-period was estimated from short arcs. Descriptively, ρ_C ≈ 0.97/0.97/0.55, so C is "not orbit-constant" (no verdict). One fix round APPROVED at low priority (why it matters: it turns the C-anomaly question into a registered verdict cheaply). It uses a Kerr-only half-period pre-check for NSTEP, a must-fail short-orbit C0 check, nice ≥ 15, < 1 GB, and yields to the r = 8 night.
- **ansatz spin 0.3:** no exceptional k in (0, 30/7 − 1e-12]; endpoint non-VA. Spins 0.8 and 0.9 are running.
- **tabula §213 fix round LAUNCHED 21:26** (amendment 2, 0ffe859; PGID 48091, nice 20, 1 GB cap; ~10–15 h). **On the r = 8 night:** touch `/Users/sumit/Github/SpaceTime/curvature/results/213b_STOP` for a clean checkpoint and exit (≤ 5 min); relaunching resumes bit-identically.

### 2026-11-22 00:39 IST: Cuspis EXP-081b verdict INCONCLUSIVE (62ab26f); the Bridge's call
- **Result:** INCONCLUSIVE under both rules, as registered. The Bridge read report.md and the analyzer output, and the numbers match.
  - **Sole cause:** σ_W = 30.07. The W8P8 box8 geometry failed reliability at its first checkpoint (cum 2.0e-7 > 1e-7), so its 𝒞 term was dropped and R48 = 32.7. The nuisance was never actually measured.
  - **Passed:** K, N2′, N_y (after the bug fix) and s-quad. **Failed:** N4 (s_cut 1.6e-4 against ≤ 1e-6; no consequence was registered).
  - **Production bug** found by N_y: the pole-merge tolerance 1e-9 sat below the QEP accuracy. It is fixed (1e-7). A replay of every merge decision shows only W4P6c3 changed. The verdict is the same either way.
  - **Descriptive only:** R∞ = 2.41 ± 0.29 without σ_W. Never quote it as a result.
- **The Bridge's call:** 081b stays INCONCLUSIVE, with no amendment.
  - The nuisance is re-measured as a NEW registration, EXP-081c. It discloses the seen value, and σ_W enters whatever it is.
  - New numerics must first reproduce reliable geometries on the production path. If W8P8 fails again, the verdict is INCONCLUSIVE with no rescue.
  - Find N4's root cause first. Measure resources on a dry run.
  - Merge 081c with the P = 16 night-run redesign if they are the same computation. The draft comes to the Bridge before any compute.
- **Physical-meaning flag sent:** a positive correction of about +2.4 is surprising next to the negative ones for C_T (−0.45) and F (about −0.24), and against the T46 prototype (−0.2 ± 0.5). The 081c design must be able to see a narrow-strip lattice term.
- **Night r = 8 run:** still on hold, pending the 081c draft.
- **00:49: EXP-081c draft (Cuspis d50f6de) APPROVED with five edits.** The edits:
  - A: a planted must-fire decides whether the run is void. Woodbury's margin at W8 is only about 2×.
  - B: Step 0's high-precision reference is extended to every checkpoint node, plus one g-level comparison.
  - C: an N4c prediction check at ≤ 1e-4.
  - D: ρ ≤ 0.10 is labelled "resolution-stable under one doubling", not "continuum-ready". The Richardson value is reported as descriptive.
  - E: the λ argument for K's excess is regraded, since the sign of the free refinement shift is opposite.
  - **Prerequisites:**
    - N4 was a mis-specified tolerance; the true remainder is ΔR ≈ 2e-5.
    - 081b's W8 "N1 failure" measured both methods' errors.
    - Dry run: about 4 h in the daytime, < 1 GB.
  - **No merge with the night run.** 081c is a resolution test; the P = 16 run tests volume. The P = 16 night run stays on hold, since R(P) is flat for P = 8–12.
- **00:50: 081c edit B was swapped by agreement.**
  - **Why:** a 40-digit g-level arm at W8 would take about 8–13 days, so it isn't feasible.
  - **Replaced by:**
    - B2a: an independent H(α) build compared entrywise, written blind to the production code, with a must-fire that flips one twist link;
    - B2b: one refinement step vs two at the g level.
  - **Already confirmed:** A's planted must-fire arithmetic gives an impact of 1.02e-6, 10× the threshold.
  - **Next:** Cuspis registers and runs in the daytime.
- **00:53: EXP-081c REGISTERED (Cuspis 8fcfb84) and running in the daytime.**
  - Declared 1.1 GB peak, cap 1.5 GB, one job, nice 12.
  - The B2a arm is written by a blind sub-agent.
  - Step 0 is tiered by node.
  - Mirror slices are aliased; the positive controls must confirm the aliasing against 081b's un-aliased values.
  - Run order: Step 0 and B2a, then the positive controls, W2P8 b8, W8P8, and N4c.
- **00:58: 081c Step 0 STOPPED as registered (Cuspis be7f9cf).**
  - **Result:** one refinement step reaches only 2.7e-12 at s ≈ 1.97, against the 1e-12 tolerance. The residual code itself was verified to 2.6e-18.
  - **The Bridge OK'd an amendment:**
    - adaptive refinement (correction ≤ 1e-15, at most 8 steps), with a divergence guard;
    - the 40-digit reference stays the referee;
    - the STOP stays on record;
    - the amendment is committed before the rerun;
    - the report gives step counts and wall time.
  - No production quantity had been computed when this was decided.
- **01:06: ansatz spin 0.8 (8241c9b).**
  - **Registered verdict:** EXCEPTIONAL CANDIDATES, caused by a classifier design flaw. T1Γ = T1·TΓ identically (Fricke; M1Γ⁻¹ is a single-point loop).
  - **Post-hoc resolution (labelled):** at the common zero k* = 4.00816, the circle pair is Zariski-dense. The Bridge checked Z1–Z4 there (tr M0M1 = 3.90 + 3.19i ≠ 0). So there is no exceptional k at spin 0.8 (floating point).
  - **The Bridge asked for:**
    - the 0.9 resolution protocol committed before 0.9's counts are read;
    - the patched T48b sliver certificate run by ansatz itself at spins 0.3, 0.8 and 0.9, so the planned Gemini sliver task is dropped;
    - the floating-point qualifier carried for k*.
- **01:36: ansatz interval sliver certificates (835ead3, 91fe428).**
  - **Results:** PASS at spin 0.6 (δ0 1.33e-11, under S2), 0.8 (2.41e-10, under S3) and 0.9 (3.63e-10, under S3). FAIL at 0.3.
  - **The 0.3 failure is real:** the endpoint group is near-degenerate there (τ = −4.46e-10 by the 50-digit walker).
  - **The Bridge checked the S3 diff:** zeroing C3/C4 is unused by the VE1 certificate (other scope), and Z2 via Fricke τ on inflated traces is sound. S3 is labelled post-failure.
  - **The Bridge asked for:**
    - an S4 rescue of spin 0.3, registered first, with failure final;
    - τ's accuracy at 0.3;
    - |τ| vs spin, for the claim sentence ("weakens toward low spin?").
    - It also noted that τ being identical across pairs is automatic (ABC = I).
  - **S1** (the 0.9 resolution protocol) was committed before any 0.9 output.
- **01:44: Cuspis check (c) FAILED its own prescription (a5bf055).**
  - **The test:** a pure-gauge ε-family, where the exact answer is 0.
  - **Results:** the threshold code grows like 0.06·ln(1/ε), then jumps to 0. P1 + P2 gives 11–17, and 12.3 at the gauge point.
  - **Downgraded:** "T0 resolved" is now unverified, and sealed P3 is unsupported.
  - **The Bridge asked for:**
    - an honest integer-n Q(n; ε) reference NOW, by Cuspis itself, registered briefly with the prediction "integer Q(n) = O(ε²) ⇒ the continuation is at fault";
    - a code-level answer on whether sigma3d's σ-side continuation has an analogous near-confluence issue. If yes, an honest integer-n σ-side control is a missing control for 081b's +2.4.
  - T46e will be graded only against the integer-n reference.
- **01:50: Cuspis EXP-082 DONE (e09178d / 8d670e6), honest integer-n referee on the ε pure-gauge family.**
  - **Result, reading (ii):** the threshold continuation matches every integer but has the WRONG n → 1 slope (+0.4…0.9 against a true −0.3…−8e-5 that → 0).
  - **Cross-check:** two implementations agree on the integers to 9 digits.
  - **A run-1 must-pass fired on Cuspis's own double-gluing bug.** It was fixed, and run 1 is kept.
- **01:50: lattice question answered "partially yes".**
  - The production Strip3D σ continuation (QEP poles, s_cut, y-convolution, T_sad) has NEVER been checked against honest integer-n data.
  - So this is a missing control for 081b's +2.4.
- **EXP-083 draft APPROVED with five edits:**
  - referee bases independent of production poles (own solve and/or a base-free arm);
  - discriminating power stated (the tolerance must be < half the gap between R = 2.26 and R = −0.45 at P = 4, or the test is non-discriminating);
  - the saddle correspondence argued in writing;
  - a saddle-off must-fire;
  - s_cut 1.5 relabelled as a diagnostic.
  - Runs in parallel with 081c, < 1 GB.
  - **The lattice sign now waits on EXP-083 as well as σ_W.**
- **01:55: EXP-083 Tier-1 NON-DISCRIMINATING (423719f), so it goes to redesign, not a verdict.**
  - **What passed:** pure gauge, and the own-pole scan matches the QEP.
  - **The fits:** fixed bases + confluent terms are tight, but the base-free pencil differs by 0.29 at W4P4, above the 0.191 half-gap.
  - **Redesign OK'd with four edits:**
    - higher-confluence model variants, an interior held-out block, and n-range drift;
    - the P = 4 pencil as a diagnostic;
    - P = 2 completeness (≤ 1e-3) as a STOP gate;
    - a disclosure that the honest Q′ are known and the comparison has not been formed, so the tolerance is mechanical.
- **01:59: EXP-083 P = 2 gate STOPPED as registered (a9d6f8c).**
  - **Why:** the float64 pencil can't see the small bases, and the adequate fit models disagree at ~0.02.
  - **Also:** a watchdog kill at 1.90 GB against a < 1 GB estimate (resource slip, recorded).
  - **R2 approved:** high-precision honest data by the sector decomposition.
    - The Bridge directed Arb (python-flint acb_mat; libflint 24 is on the box) instead of mpmath, aiming to reach P = 4, i.e. 081b's own geometries.
    - The sector decomposition must be validated against the direct n-sheet Q(n).
    - Memory is measured by dry run.
    - Consequences made explicit: a P = 2-only pass is code validation only; any fail suspends the +2.4.
- **02:00: EXP-083 R2 REGISTERED (f5b9e71).** Blocker: python-flint is not installed (only the Homebrew C library libflint 3.6.0; the Bridge's '24' was the dylib soname). Cuspis needs Sumit's own word in its chat to pip-install it, and the Bridge has asked Sumit. Meanwhile: float64 decomposition validation and mpmath cost/RSS dry runs.
- **02:02: EXP-083 R2.** Edit 2 PASSES: the sector decomposition equals the direct n-sheet Q(n) to 5.5e-12, both arms. mpmath cost: P = 4 about 25 h, so not feasible. Even P = 2 needs n ≳ 30–45 at ~120 digits (~10 h on mpmath). python-flint is the enabling step; Sumit said yes in the Bridge chat and was asked to give his word in Cuspis's chat.
- **02:03: Sumit gave Cuspis his yes (in Cuspis's chat) for the pinned python-flint install.** EXP-083 R2 is unblocked.
- **02:06: python-flint 0.9.0 pinned (Cuspis ef07c0f).** Arb is 30–100× faster than mpmath. R2 amendments A1 and A2 were registered before any referee number: n ≤ 72 at P = 2, adequacy held-out ≤ 1e-40. P = 4 needs n ≳ 120, so it is infeasible: R2 is P = 2 code validation only (a pass does not validate +2.4; a fail suspends it). P = 2 is running: 4 jobs, ~1.2 h, < 0.2 GB.
- **02:26: ansatz S4 FAILED, final (e025bbf).**
  - **Spin 0.3:** the endpoint is interval-certified Zariski-dense, but δ0 = 7.4e-15 < 1e-12. So the sliver at 0.3 is certified only on (30/7 − 7.4e-15, 30/7].
  - **τ accuracy:** 6.6e-39.
  - **Obstruction vs spin:** τ = −(tr Y)² at all spins (Bridge re-checked); |tr Y| ∝ a^7–a^8, so the obstruction weakens fast toward low spin.
  - **Sign change of tr Y** between spins 0.8 and 0.9, outside the tested spins. The Bridge asked for the one-line reason for τ = −(tr Y)², and an optional registered check at a_c.
- **02:56: ansatz.**
  - **τ identity derived** (0d6e021): single-point loops have M² = −I, so τ(A, B) = −(tr M2M1M3)². The Bridge re-derived it.
  - **Spin 0.9, region A:** count(F) = 3 against the expected 2, so the registered verdict will be EXCEPTIONAL CANDIDATES. Region A was not covered by S1, so the resolution is post hoc.
  - **Plan:** locate the zero. Non-real means physically irrelevant. Real means the independent-pair Z1–Z4 check.
  - **The Bridge asked:** C1 status; whether F has a reflection symmetry (a parity argument); and, as a lesson, resolution protocols should cover all regions.
- **03:35: R3 VOID before registration (control rule c).**
  - **What happened:** the known-bad T46d continuation passes both the integer test and the growth test. Carlson is ill-conditioned for modes with r below the data precision (slope error ~ δ/r).
  - **T46g grading amended** (recorded here; Neon is mid-run): decisive only at ε ≤ 0.1 saddle-on. At ε = 1, nothing counts unless evaluated at ≥ 50 digits.
  - **The Bridge proposed R3′ (visibility-scoped, arm a, P = 2).** The lattice has no r → 0 accumulation, so the kept poles (r ≥ 6.5e-9) are visible to Arb integers at δ ~ 1e-12, with slope error bounded at ~2e-4.
    - Known-bads in the visible class: s_cut 1.5 and dd 1.
    - The sub-cut class is bounded by N4.
    - Cuspis is asked for any hidden small-r branch choice in sigma3d.
- **03:37: R3′ REGISTERED (Cuspis), with four holes fixed.**
  1. The δ/r bound is per mechanism, not adversarial.
  2. P = 2 makes s_cut a no-op, so P = 4 (081b's W2P4 and W4P4) was added, with Arb n ≤ 12.
  3. The route (ii) port must reach δ ≤ 1e-11, or the claim is scaled.
  4. A route (ii) ⇄ route_b FD link per geometry.
  - **Every threshold-keyed branch in sigma3d now has its own control:** the QEP filters, the cluster merge, the residue radius, the β0 merge, the s_max truncation, and dd = 1.
  - **Scope:** arm a only. **T_sad carries the +2.4's sign** (saddle-off R = −48.5), so a pass does NOT validate the +2.4.
  - Runs after the 081c posctl, one job at a time.
- **03:50: R3′ step 1:** the port converges at n = 2…6 (δ 1e-13 to 2e-10), but Q_cont(1) has a 3.6e-9 floor from production's QEP pole precision. The claim is scaled as registered: it covers modes with r ≳ 2e-6 (s ≲ 2.0), and kept poles at s ∈ (2, 3] join the internally controlled class. The chain (~15 h, < 1 GB, one job beside 081c) is running.
- **04:09: Quantum.**
  - **A3 checkpoint 1 (t = 295.89) PASS.**
  - **B15d twin is very slow:** failing (a)-pieces exhaust leaves at the depth cap, ~4 h per piece, so days per covering.
  - **The Bridge approved a labelled amendment:** run the (b) edges and orientation FIRST within the same 2 slots, then (a).
    - Merge rule with a positive control on an hh2-classified covering.
    - No cap changes; (a) checkpoints resumed.
  - **Slots stay 2:** load is 10.9 on 10 cores. 4 after tabula §213 finishes, if the load drops.
- **04:15: Quantum B15d-2 REGISTERED (7e81cf0).** The twin runs edges first. The merged-COVER rule has a positive control (byte-identical to GB), and a vacuous edge chunk is never classified alone. The old twin (a) PIDs are paused (SIGSTOP), keeping 4.5 h and 9 h of in-flight work in memory; runner PID 30241. Recipe stays unchunked; edges-first for Kerr is optional with its own amendment. **Restart note:** the paused pieces must reach a checkpoint before any Mac restart.
- **04:17: Quantum B15d-3 REGISTERED (356d4c9):** Kerr edges first (KERR-EARLY reading, then (a)). The runner now adopts live hs_cover children on start (restart-safe); runner PID 34523. No Mac restart is planned (Sumit: later, when quiet); the paused pieces stay paused until the twin (a) phase.
- **04:26: ansatz.**
  - **a_c REPRODUCED (34c6540):** 0.85844619879171725346309 vs T50's …067, so 22 digits agree. At a_c the circle pair passes Z1–Z4: Zariski dense (50-digit floating point). Two implementations.
  - **Spin 0.9 registered verdict:** EXCEPTIONAL CANDIDATES, only because count(F) = 3 in region A. Region B is clean, and the endpoint and sliver are non-VA.
  - **C1 passed,** so the extra zero is outside |k| < 0.3 (not a Kerr split). The post-hoc locator is running (~30 min), then the claim sentence.
- **04:30: Cuspis arm (b) built and registered (4ee07fe). C1 at P = 2 and 4 PASSES (fb91521).**
  - **Result:** production T_sad equals an independent FD of the continued replica saddle to ≤ 3e-9 relative (τ = 1e-6).
  - **All plants fire:** sign flip, off, σ̇/2, and the k-index patch (1e5–2e6 × τ).
  - **Grade:** verified for the T_sad ASSEMBLY (the 081a class) at small P. It shares the QEP poles and the Poisson kernel, so it is NOT a validation of the +2.4.
  - **Solver amendment:** stagnation stop below 1e-12.
  - **Queued after 07:30:** heavy C1 (12 geometries up to P12 and W8P8), C2, and the Arb P4 arm (b) at ~3 GB.
- **04:35: ansatz spin 0.9 RESOLVED post hoc (3f2e41a):** the extra zero of F is at k = 0.1101 + 0.3415i, non-real, so physically irrelevant. There is no reflection symmetry. §163 committed.
  - **CLAIM SENTENCE drafted.** The Bridge sent four edits:
    - put spin 0.9's post-hoc zero in the sentence;
    - make the energy scope exact (E = 1.5 checked at the endpoint at spin 0.6);
    - "in involution";
    - one δ0 source.
  - It will then be committed as its own reference file.
  - **Remaining before the talk test:** the MRS section (T49 plus check) and the citations at source.
- **04:35: Quantum B15d-2 merge control (MC) PASS (eb9d86a):** the split and merged line is byte-identical to the unchunked GB line (CERTIFIED). The 12 twin edge chunks started 04:35; TWIN-EARLY to follow.
- **04:36: ONLY KERR CLAIM REFERENCE TEXT COMMITTED** (conjecture_machine eed501f, data/nve/CLAIM_FAMILY_II.md). All four Bridge edits are in, with a per-number source table. ansatz is now checking the citations at source, then the MRS section.
- **04:40: ansatz MRS section v1 (bdbcc30, 83aa2f5) read by the Bridge.**
  - **Citations checked at source:**
    - MRS 2007 VERIFIED (open Γ is covered);
    - Casale 2009 is NOT supported for open Γ, so dropped;
    - Beig–Simon 1981 VERIFIED (1980 is not for analyticity);
    - FHP 1989 VERIFIED;
    - the Prop. 2 citations are pending.
  - **The Bridge checked** Prop. 1's proof and the u = 1 crossing.
  - **One required addition:** a lemma (citation checked at source) that the Galois identity component is invariant under the finite cover Γ_E and the algebraic v-gauge, linking u-plane Zariski density to the NVE's (G)⁰.
- **04:49: Only Kerr READY FOR THE TALK TEST.** The reference claim is in eed501f. The MRS section has Lemma C (5167814 + sources); the Bridge checked the gauge and the proof. Prop. 2 is citation-pending (labelled). ansatz is idle (the new-directions hold stands).
- **05:55: T51 graded by ansatz (d067545).** e₋ = 1/e₊ is general (a two-Curzon asymmetric counterexample to the objection). Claim v2 is status-first, with conventions stated and "not black holes". F = O(k²) at Kerr. Prior-art checks pending.
- **05:56: ansatz literature at source (cb53e40).** MN95 Eq. 35 and EMR06 Eqs. 56–58 state e₋ = 1/e₊ before reflection enters, so Neon's own sources refute its objection. Markakis 2014 (Newtonian; conjecture: an equatorially symmetric SAV spacetime is integrable iff Kerr) verified; Kruglikov–Matveev verified (context only); no redundancy. Next: the reflection-symmetry status of family (ii) (decides the Markakis framing), then the Prop. 2 citations.
- **06:10: ansatz:** family (ii) has NO equatorially symmetric member for k ≠ 0, at any spin or plane (8400249, exact symbolic; the twist forces a mass octupole ∝ k), so Markakis is cited as motivation, outside his class. In the record: ZV δ = 3 (symmetric, static) is obstructed at first order (§158). A Markakis-framing line is a projection, gated on §158's necessary-direction proof being in the write-up. The TS δ = 2 deg f0 check is requested.
- **06:12: ansatz:** TS δ = 2 has deg f0 = 4 (a11b0e4; symmetric, verified). The necessary direction is still ~95% in the record. The Bridge pointed ansatz to the written Kovacic case table in fable_work/axis_integrability_classification/NOTES.md §2 and THEOREM_TS.md, to be checked after the Prop. 2 citations (low priority). The Markakis line is gated on that.
- **06:21: ansatz.**
  - **Prop. 2:** uniqueness CHECKED (the recursion's indicial polynomial is 4f0k²). Convergence is cited via Baouendi–Goulaouic through a reduction ansatz wrote itself; the 1976 systems paper is paywalled. The Bridge approved writing our own majorant proof, with a Kerr off-axis sanity control.
  - **The necessary direction (deg f0 ≥ 3 implies SL₂ at generic E) is now CHECKED** (856e759; Kovacic cases 1–2 entry by entry, case 3 excluded independently). Sufficiency stays ~80–85%.
  - **The Markakis framing line is now usable,** with three caveats; it goes into CLAIM_FAMILY_II.md as a separate related result.
- **06:33: Quantum B15d TWIN-EARLY (2fcdeb1).** The swap variant PASSES (edge-fixed CERTIFIED-FAIL ×6). rot90 can't reach CERTIFIED-FAIL (b and orientation pass; a can't certify), so B15d will hold at "control not decided" and Kerr won't run under B15d. That is control-clause slip 12 (in memory). **Bridge:** slots to 4 now (tabula's §213 process has ended; load 6.5); B15d-4 runs the recipe first; Quantum drafts a B15e with a pre-checked twin negative control (not run; Sumit told).
- **06:34: tabula §213 fix round.** The guard killed it at 06:30 (system free 34% < 35%; the pressure came from outside its job). 8 of 9 parts are done; wide C restarts (~50 min, < 1 GB). Descriptive: C rho 0.99 / 0.975 / 0.55 at r0 = 5/7/9; A 0.99. Wide C can't change the label. **Bridge:** GO when free ≥ 40%, guards unchanged. Cuspis holds its ~3 GB run until tabula is done.
- **06:34: tabula's wide-C resume is armed.** It launches only at free ≥ 50% and pressure level 1, polling once a minute, giving up after 8 h; guards unchanged. Cuspis's ~3 GB run waits on tabula's done-message.
- **06:35: MEMORY INCIDENT ROOT CAUSE FOUND by the Bridge.** ansatz's scripts/_nve_prop2_majorant_control.py (PID 92265, started ~06:24, the Kerr sanity control the Bridge requested) grew to 10 GB (9.9 GB compressed); swap was 1.79 of 2 GB. That tripped tabula's §213 guard and Cuspis's watchdogs at 06:29–06:32. ansatz was asked to stop it by verified PID and redesign it to bounded memory with a guard. The Bridge did not kill it (not its own process).
- **06:36:** ansatz stopped 92262/92265 by its own handle. Memory has recovered (free 77%, swap 2.11 GB and draining). The bounded redesign (< 100 MB, 1.5 GB self-guard) is approved. The Bridge sent a wrong memory figure and corrected it; rule in memory.
- **06:37: ONLY KERR APPLICABILITY CHAIN COMPLETE.** Prop. 2 is closed by our own majorant proof (b30d5c3, peak 22 MB); the Kovacic original confirms case 3; the related-result line is in CLAIM_FAMILY_II. Ready for Sumit's outreach decision.
- **06:39: Quantum.** B15d-4 registered (2dc1926); runner PID 7337 on 4 slots; recipe first. The B15e draft (4eede41): the second candidate "stab" stopped at the S8 geometry gate (pre-check rule written first). **Bridge call:** a ONE-VARIANT twin (swap alone), registered openly; no new candidate (forking path, same mechanism). Kerr edge chunks first once RECIPE is logged.
- **06:42: Quantum B15e REGISTERED (c3b7c8f).** One-variant twin (swap); runner PID 15193 (Cuspis night: SIGTERM 15193). Queue: RECIPE line, then (if swap PASS) the Kerr edge chunks, then KERR-EARLY, then the interleaved (a) chunks; KERR is final only if every twin merge is clean, otherwise WITHHELD. Dry-run order verified.
- **06:49: Cuspis R3′ P = 2 graded (0b36206), partially verified.** Link 1e-6 PASS; all plants fire; deviation growth is the port's tail quadrature (tmax = 48/n gives ≤ 6e-11). The Bridge ruled the visibility bound uses the n = 2 δ (1.4e-4); the n = 1 floor 3.5e-8 is a separate un-amplified term (~1e-8). tabula's wide C resumed (~07:00). The Arb 3 GB run is held until tabula is done.
- **07:17: Zenodo GitHub archiving switched ON for sumit7194/ansatz-machine** (Sumit asked; done in Chrome). ansatz is updating CITATION.cff (Pal, Sumit + ORCID + abstract + Claude-role line), plus ONLY_KERR.md and ONE_PAGER.md. Then the Bridge creates the v1.0.0 GitHub release, which triggers the DOI. The email draft is in outreach/only_kerr/.
- **07:22: ansatz-machine v1.0.0 RELEASED** (gh, tag at f91aa2d). Zenodo DOI 10.5281/zenodo.24431695 (record checked: Pal, Sumit; description including the Claude-role line). The DOI is in the email draft.
- **07:26: Only Kerr email to Maciejewski cc Przybylska PREFILLED in Gmail** via a compose URL (no keystrokes in the compose window). Both addresses were verified by the Bridge on the official pages (staff page; institute conference page). Both links resolve (200). The compose tab is left open for Sumit to read and send himself.
- **07:28: Only Kerr email SENT by Sumit** (Maciejewski cc Przybylska). Wait; don't chase.
- **07:38: TS δ=2 expert email to Lukes-Gerakopoulos PREFILLED** in Gmail (draft v2 at outreach/paper_ts_mn/EMAIL_DRAFT_expert_v2.txt). The address gglukes@gmail.com was verified on his arXiv:2511.08057 and 2605.02084. The SUMMARY.md link resolves (200). No keystrokes; the tab is left open for Sumit.
- **07:40: TS reminder ADDED** (Sumit's calendar, all-day 10 Dec): 'TS δ=2: check for reply from Lukes-Gerakopoulos'. The TS email was SENT by Sumit.
- **07:41: tabula wide C never ran.** The launcher's ABSOLUTE swap gate (1.5 GB) held it while swap was stale (1.8–2.1 GB at 84% free); the side guard wrote STOP at launch before any compute. A waiter process-group bug was found and fixed. **Bridge:** switch to swap GROWTH > 0.5 GB over the launch baseline (gate and side guard alike); other guards unchanged; launch when free ≥ 50% and pressure level 1. Cuspis's 3 GB run goes after.
- **07:41: tabula wide C RUNNING** (launched 07:41:44, PGID 48757, ETA ~08:40). Swap baseline 1822.69 MB, trip at +512 MB. The amendment was committed before launch (2bf2c1d).
- **07:47: Cuspis 081c W8P8 done.**
  - **Registered verdict: INCONCLUSIVE.** The residue clause failed at 8.7e-7 against 1e-8, but the threshold sat inside the unrefined arm's known error (slip 13). Production residues are converged to 6e-26.
  - **Next (Bridge):** census, N4c and the analysis run now, and σ_W, ρ and Richardson are reported POST HOC with impact grading, labelled.
  - **Schedule:** C2 P = 2 and the Arb 3 GB run after tabula (~08:40). R3′ P = 4 ports ETA ~10:00–10:30. Heavy C1 ETA ~13:00–16:00 (a guess).
- **07:49: Sumit is going to sleep.** The ideas discussion is set for this afternoon or early evening. Until then the Bridge monitors and decides routine calls only; no new directions.
- **07:57: Cuspis 081c post hoc:** ρ = 1.86. R goes 2.65 → 6.44 under one doubling (resolution effect +3.79, box +0.009); R48 reproduced two ways; sign undecided even post hoc. So **+2.4 is not a continuum number.** The Bridge asked for a ρ decomposition by component and a log-vs-power check (existing data), and for a refinement series DRAFT (not run).
- **08:01: Cuspis decomposition (a3cdc26).** R is a near-cancellation t0 vs T_sad (each ~20× the net). It holds in P and breaks along the W pair under refinement (+3.79). Log vs power is undecidable from the current data. The 081d refinement-series DRAFT (k = 1–3; r-statistic; k = 3 ≈ 15 h wall on 4 cores) is held for Sumit's scheduling; the k = 1.5 cost re-measure is OK'd.
- **08:08: Cuspis 081d cost measured (6bdfc99), timing only.** k = 1.5 ≈ 0.9 core-h; k = 2.5 ≈ 11; k = 3 ≈ 35 core-h (~9 h on 4 cores, one night); k = 4 ≈ 250. Residues ~2 GB at k = 3 (low-rank still needed). Held for Sumit's scheduling.
- **08:30: tabula §213 fix round DONE** (wide C finished 08:29, peak 557 MB, no guard trip). Registered verdict: **V3 NOT ORBIT-CONSTANT at all three r0**; controls pass, must-fail trips. Result sha256 252d2132…be8db. Sealing and write-up next. Cuspis: GO for C2 P = 2 and the Arb P = 4 arm (b).
- **08:31: tabula §213b SEALED** (cca6f21) and written up (f16be6f). V3 is not orbit-constant, so the 'shift is a function of Q' hypothesis is refuted. Open: why C's two parts cancel (the post-hoc idea is not registered). Next items (KEEP2 plateau, screen retrofit) are held until Sumit's ideas discussion unless they were pre-registered.
- **09:08: Cuspis C1 COMPLETE (1a1b1ec).** All 16 geometries pass, including W8P8: production T_sad = an independent FD of the continued saddle, to 3e-10–5.9e-9 relative (τ 1e-6). All plants fire at ≥ 5e4 τ. One auxiliary-arm ceiling was raised (deviation recorded); the rerun reproduces run 1 exactly. **The T_sad ASSEMBLY is verified; the continuation and the +2.4 are NOT;** 081c's ρ points at the regularisation. Lanes: A ports W4P4; B C2 W4P2, then Arb.
- **09:21: Cuspis C2 P = 2 PASS (b0792ed).** First honest-data test of the continuation WITH the saddle: σ_n matches the honest saddle to ≤ 1.4e-12; the route-(ii) T_sad matches C1 (≤ 9.5e-7); plants fire. One marginal point (W4P2 n = 2, 9.9e-11 vs 1e-10). Partially verified (integers, P = 2). The Arb P = 4 arm (b) is done for n ≤ 6 (0.43 GB, 7× under the declaration; a safe-side miss). R3′ closes after the P = 4 grade and C2 P = 4 (~10:30+). The +2.4 is still not validated.
- **11:08: Cuspis arm (a) P = 4 graded (1068c51). Registered verdict: arm (a) UNVALIDATED.** The W2P4 "s_cut below a kept pole" plant used 1.5, but all of W2P4's poles sit at s ≤ 1.329, so that plant could not fire. The slip is shared: the Bridge reviewed that registration too, and it repeats slip 12's rule. Bridge ruling: the registered verdict is the headline. A labelled post-hoc supplement sits under it: the corrected plant (s_cut 1.3) fires, the links pass, and the integers agree for r ≳ 2e-6. r in (6.5e-9, 2e-6) is untested at P = 4. The "EXP-083 ends" clause is read as closing arm (a) only; C2 (arm b) is graded as registered. Mechanism requested: a pre-run assertion in the plant harness that each plant changes its input at every geometry. C2 W2P4 PASS (n ≤ 6, route 5.3e-7). C2 W4P4 running (~45 min). The +2.4 is untouched (081c ρ 1.86 governs).
- **11:44: Cuspis EXP-083 R3′ CLOSED (061d06c). Arm (b) is UNVALIDATED as registered:** C2 W4P4 n = 2 dev 4.32e-10 against tol 3.1e-10. Every other C2 point passes, the route T_sad checks pass (5.3e-7, 7.7e-7), and the plants fire.
  - **Cause (Bridge read the diag outputs):** the tolerance took dev_a from production's path. Arm (b) runs on strip_sigma, which reuses mirror-slice poles (8.6e-8 pole noise) and doubles the baseline (2.32e-10 vs 1.04e-10). That is slip 15, a slip-13 repeat.
  - Post hoc on its own path, labelled: everything passes.
  - strip_sigma appears only in exp083 scripts, so the 081b/c production values are unaffected.
  - **Close-out order:** arm (a) unvalidated (plant), arm (b) unvalidated (cross-path tolerance), C1 PASS 16/16.
  - **The +2.4 is still not validated** (081c ρ 1.86).
  - **Bridge asked for:** (1) a cheap labelled check, arm (b) n = 2 on the un-aliased path; (2) a tolerance-path guard in the harness, with the aliasing removed or made opt-in, before 081d.
  - Lanes idle. 081d held for Sumit.
- **11:52: Quantum B15d RECIPE-POSITIVE (bd27a4a, run.log 11:47:05). Bridge read all 7 .out files.**
  - The 6 required coverings are COVERS=1 with edges=yes, fail_a = fail_b = 0.
  - The optional N6N3 is CERTIFIED-FAIL: 24/25 b-edge fail pieces are certified, plus an orientation certified-fail.
  - The chain is [3,4,5,6].
  - **B15e twin gate PASS** (the swap variant: all 6 CERTIFIED-FAIL).
  - **Kerr edge chunks started 11:47:** kerr_e/N0N0 (54961) and N0N1 (54963). The rot90 slots (90952/90954, ~16.8 h) continue.
  - No Kerr covering result yet. Next: KERR-EARLY after all 8 edge chunks.
  - A3 (40882) is unaffected. The note "Cuspis night: SIGTERM 15193" stays a contingency only; no Cuspis night is scheduled.
- **12:02: Cuspis post-hoc check (1b8cf34): aliasing is NOT the whole cause.** On the unaliased path, dev_b(2) at W4P4 is 4.43e-10 (σ fixed) or 5.42e-10 (σ re-solved), against arm (a)'s 1.04e-10. That is 4.3–5.2×, above the registered 3×.
  - Cuspis WITHDREW its "passes on own path" reading (struck through, pointer kept). The headline is unchanged: arm (b) UNVALIDATED as registered. The cause is unidentified; s_cut, npt and aliasing are falsified. dev_b is σ-sensitive (a Δσ of 3e-14 moves it by 1e-10).
  - Slip-15 mechanisms are built and tested: alias=False is the default, and tools/tol_ref checks the reference path.
  - **Bridge approved a ~20 min one-variable post-hoc sweep** (Mt, npt0, n·Δld1), with a written pre-statement first, 1.5 GB cap, nice 12. It stops at "unidentified" if nothing explains the excess.
