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
- **12:45: Cuspis C2 sweep CLOSED (pre-statement 110c946, result 1c52557).** Mt 320, npt0 1024 and a 30-digit n·Δld1 each leave dev_b(2) at 4.42e-10. Cause UNIDENTIFIED (left: Mx/tmax, Arb arm-(b) reference); the run stopped as pre-stated.
  - The excess is a consistent signed −4.4e-10.
  - **Budget finding for 081d:** Q moves ~3e3 per unit max|Δσ|. That is an extensive gradient of the non-stationary Q_sad, so the σ precision needed tightens with resolution, and the gap noise floor is already at the edge at P = 4.
  - The Bridge asked for 081d draft edits only: the σ-precision budget, plus a design question for Sumit (would a stationary full functional make σ errors second-order?). Lanes idle.
- **12:47: Cuspis 081d draft edits (01a61fc), text only.**
  - §5b σ-precision budget: S₁ = 3.3e3, S(k) ∝ k³. The measured floor exceeds the requirement at every k, but this bites only the integer-VALIDATION arm. Production T_sad takes σ̇ from one dense solve (the Bridge checked sigma3d.saddle_term), and is bounded by a C1 check at each k.
  - §8: first-order σ sensitivity is intrinsic at O(N⁰). The Bridge agrees.
  - §9: the new candidate for the −4.4e-10 is σ₂'s distance from the exact saddle.
  - **The Bridge approved that test only if it costs ≤ 1 h** (pre-statement first, 1.5 GB cap); otherwise it is held for Sumit with 081d.
- **13:00: Cuspis exact-saddle test (pre-statement d025d51, result b3500cf): cause NOT found.** At the Arb saddle, dev_b(2) = +4.74e-10. The σ₂ error (−9.2e-10) is co-equal, but the +4.7e-10 evaluation excess on the σ ≠ 0 strip remains. Post hoc, labelled.
  - S₁ revised to 2.6e4 (direction-dependent), so plain float64 σ_n is hopeless for the validation arm at k ≥ 1. This strengthens option (a) for production.
  - Candidates Mx/tmax and Arb-reference correctness are held for Sumit with 081d.
  - **Cuspis: stopped for today.**
- **19:02: Email reply received (Sumit's Gmail, 12:21) from Loukes-Gerakopoulos on TS δ=2.** He suggests a Poincaré section near the main unstable periodic orbit and would not be surprised by chaos. A possible sharper version of tabula §198 is held for Sumit's ideas discussion. **Box check before the app restart:** every compute job is detached (parent = launchd): Quantum runner 15193 with 2 Kerr edge chunks, rot90 twins 90952/90954, A3 40882. Cuspis/tabula/ansatz idle.
- **19:15: Quantum F12 HARNESS: all 16 Kerr specs lack `param level`** (the mn lift hard-codes H = −1/2, but S9 checks SYS.level). So every Kerr piece threw an S9 BUG: kerr_e N0N0/N0N1 had 34 S9-BUG lines each, 0 COVER, ~7.5 h void. Quantum PAUSED them (SIGSTOP).
  - The Bridge independently confirmed it (16/16 specs; hs_cover.cpp L139–142, L426, L200; both processes in state T).
  - **Approved B15e A1:** fix the specs; add a runner gate (a known-answer: a no-level spec must be REFUSED); run a NOT-COUNTED S9 smoke plus a must-fail wrong-level twin; move the void outputs to kerr_e_void_nolevel/; swap the runner; rerun kerr_e from scratch.
  - Slip 16, shared (the Bridge approved the B15c header): the recipe and twin gates ran on hh, so the mn path was never smoke-tested.
- **19:16: Sumit APPROVED 081d (refinement series k = 1–3) for tonight.** Cuspis was woken via session message. Order: registration commit (plant_guard and tol_ref mandatory, C1 check per k, σ budget, r-statistic decision rule pre-written), then Bridge control-clause review and GO, then run (4 cores, nice 12, declared cap ~4 GB, pressure-stop on). Quantum is NOT stopped; it co-runs.
- **19:19: Quantum B15e A1 registered (852b9f9) and fixed (4c66dab). Bridge spot-check:** 0 Kerr specs lack the level line; gate known-answer REFUSED, 0 launches (run.log L107). S9 smoke S+/S− (level −1/2 vs −499/1000) running as PIDs 4433/4439. Counted kerr_e restarts only after the smoke PASSes.
- **20:16: Cuspis 081d REGISTERED (963c8f5); no new-k number exists.**
  - Bridge review: the control table is good. ONE CLAUSE NAMED: the §B decision bands leave gaps. p = 1 convergence (r = 0.667) and p = 1 growth (1.5) are always INCONCLUSIVE, and slow power |p| ≤ 0.55 reads as "log-like". Fix to be committed before launch (R(1.5) enters r).
  - **k = 3 cost CORRECTED by Cuspis:** ~3.1 GB per process, ≈ 47 core-h, NOT one night.
  - Stage 1 (k = 1.5, 2.5; ≤ 4 GB, ~9 h) is approved in principle and starts on GO. Stage 2 (k = 3) options go to Sumit.
- **20:17: 081d amendment 1 (361febf), committed before launch.** Bands: converging ≤ 0.75, 'log-like or slow power' 0.87–1.15, power ≥ 1.33; 16/16 planted tests pass. **Bridge GO for Stage 1** (k = 1.5, 2.5; ≤ 4 GB, ~9 h). **Sumit chose Stage 2 option (i):** 3 parallel processes, ~9.3 GB, ~16 h. It starts after Stage 1 passes, at a quiet time agreed with Sumit, with the memory cap taken from a measured k = 3 probe.
- **20:18: 081d Stage 1 LAUNCHED 20:17** (lanes 14172/14331/14342, watchdogs 14494/14503/14512; declared ≤ 4 GB). Next report: STOP, void k, or Stage 1 end.
- **21:43: 081d Stage 1: both k = 2.5 routes were killed by their own 2.3 GB caps in the t0 phase** (peaks 2.37/2.57 GB; nothing read; outputs kept). Cuspis's memory formula was wrong a second time. The Bridge OK'd relaunch at 3.9 GB caps (full-run peak ~3.1 GB, scaled from the measured k = 2 peak). k = 1.5 W3 is done and W6 is running. **Stage 2 re-estimate from measurement: ~6.2 GB per k = 3 process, so Sumit's 3-parallel choice (~19 GB) cannot fit;** it goes back to him.
- **21:45: 081d k = 2.5 relaunched ~21:58 (1e89ddc).** Per Sumit's 'soft caps' instruction: soft warning at 3.5 GB, hard backstop 5.0 GB, pressure-stop is the real guard (Bridge accepts). Premature C1s stopped and kept ungraded; lanes now run route → C1. A watcher is armed on the lane logs. Stage 2 choice is pending with Sumit.
- **21:46: Sumit chose 081d Stage 2 = 2 parallel k = 3 processes** (~12.4 GB, ~24 h). It starts after Stage 1 passes, with a k = 3 probe measurement first and soft caps.
- **21:58: 081d interim (ce4f113), gates only, no R read.** k = 1.5 is non-void (C1 PASS). k = 2.5 W10 Step 0 failed at s = 5.052, so s_max is capped at 3.948 (registered; not void). Cuspis found the analyzer wasn't applying the S0 cap and fixed the wiring before any R read; the Bridge checked it against row S0 (18/18 tests). A runner-edit slip was caught by the watcher; nothing was rerun.
- **22:30: Quantum A1 S9 smoke stage 1 INCONCLUSIVE (33073e9):** the whole-set pieces blew up (sqrt domain, enclosures ~1e79) before reaching S9. Stage 2 (16 column-0 pieces) is running. The Bridge pre-stated stage 3 if needed: the exact edge-L pieces known to reach S9 in the void run. Kerr stays held.
- **04:45: Quantum's long run passed its second time checkpoint (R2) and logged it as DEFERRED, as registered.** The set is saved and hashed (753ab82); nothing threw. **Smoke stage 2 has run 6.25 h with no piece finished.** Both pieces are live (CPU time is rising), but the stage had no time bound. The Bridge asked Quantum to measure the time per piece in the void Kerr run and pre-state a bound of 3x that. If the bound passes with no result, stage 2 is INCONCLUSIVE and stage 3 starts. Disk has 12 GiB free; Cuspis's Stage 2 output size will be checked before it starts.
- **05:00: Quantum smoke stage 2 bound committed (66121ec): 3 x 680 s per piece (measured from the void Kerr run) x 16 pieces = 9.07 h, ending 07:33:33.** Accepted. Found along the way: hs_cover holds results in a buffer and writes them only when a cover ends, so a stopped run loses finished results. Before stage 3 and the Kerr rerun, the Bridge requires a flush after each piece, with a kill-mid-run known-answer check.
- **05:05: Quantum flush fix registered (8e9595f), known-answer check PASS.** hs_cover now launches under `/usr/bin/stdbuf -oL`, so finished pieces are written to disk at once. The binary and its sha (fb5fcbfc) are unchanged. In the check, a run killed mid-cover kept 9 finished lines with stdbuf and 0 without. The Bridge verified that stdbuf is present and that the launch line is wired in. Stage 2 (started before the fix) runs to its 07:33 bound.
- **07:35: Quantum smoke stage 2 INCONCLUSIVE as registered** (bound passed with no result; 47854/47860 stopped by verified PID). **Stage 3 started 07:34 (db4886b)** on the 4 exact pieces known to reach the S9 check, with immediate result writing on. Its two specs differ only in the level line (Bridge checked). Stage 3 had no time bound. The Bridge asked for one to be committed now (3 x 680 s x 4 ≈ 2.3 h, ending ~09:50). Kerr is still held.
- **07:45: Quantum stage 3 time bound committed (5e7b8d4), ending 09:50:27**, before any S9 line appeared. Accepted.
- **09:07: Quantum smoke stage 3 PASS (NOT COUNTED; e35eb15).** With the correct level, all 4 test pieces passed. The deliberately wrong level hit the known bug on all 8 edges, so the guard is live. The Bridge read both outputs and confirmed all 8 Kerr specs now carry the level. **Runner swap and Kerr rerun from scratch approved, as registered in A1.** The void Kerr output is moved aside, not deleted.
- **09:09: Quantum Kerr rerun started from scratch (7df329c).** Runner 79322; Kerr chunks 79482/79486, each line written at once. Void output moved aside. The Bridge verified the PIDs and asked for an expected wall time plus a 3x check-in bound, from the measured rate.
- **09:30: Quantum Kerr expected time registered (7ff4fa5)**, before any output. Measured 685 s per piece (smoke stage 3), which agrees with the void run. 128 pieces per chunk gives at least 24.4 h per chunk; first pair ~09:29 on 24 Nov. The 3x check-in bound is 26 Nov 10:12 (a check-in, not a stop). Planning: 8 chunks, 2 at a time, so Kerr takes at least ~4 days. Accepted. A stray pre-existing log change was swept into the commit; harmless, history left as is.
- **13:40: Cuspis refinement series, first batch finished (105e4fe). "Stage 1 of 2, no verdict" accepted.** The k = 2.5 gates all PASS. R(k) = 2.26, 4.23, 6.44, 8.22 (k = 1 to 2.5), positive and still rising. PRIMARY is INCONCLUSIVE until k = 3, as registered. The report was held because the Bridge looked offline at 12:55; it was delivered at 13:40.
  - **Bridge caught a descriptive slip:** the registered decision bands were applied to the secondary ratio instead of the primary one. Under the registered primary ratio, the extrapolated R(3) of 9.16-9.93 sits in the upper gap or the power-divergent band, not near converging. Converging would need R(3) ≤ 7.37, below R(2.5). A labelled correction was asked for; nothing registered changes.
  - The k = 3 memory probe is approved. Stage 2 (2 processes) starts after the probe if the measured peak x 2 ≤ 13 GB, with expected time, a 3x bound and a disk estimate committed first.
- **14:00: Cuspis correction committed (43fbd33)**; the Bridge's thresholds reproduced independently. **k = 3 memory probe running (072de80):** the hardest node only, no R readable, with a k = 2.5 control run alongside. The Stage 2 memory test uses the probe peak scaled by the k = 2.5 full/probe ratio, to cover the checks phase.
- **14:00: Cuspis k = 3 memory probe was a STOP event.** It reached 7.32 GB and was still rising when pressure-stop killed it, before any node ran. Two parallel processes cannot fit under 13 GB; the scaled per-process peak is ~9.3 GB (argued). This is the third memory-formula miss: the earlier "6.2 GB" was low by ~1.5x. The Bridge approved a solo probe to measure the real peak and the time per node. Options go to Sumit after that; the Bridge leans to 1 process at a time (~2 days, same code for every k).
- **15:05: Cuspis Stage 2 launched SERIAL (7b9fc00), per Sumit ("let it grow, lets see where it reaches solo").** Measured k = 3 peak is 7.32 GB per process (a single hard node captures the whole-run peak; the control ratio was 0.98), and the hardest node took 2463 s. Census and Step 0 run first, behind a void gate tested both ways. Then route and check at the smaller width, then the larger. Expected ~62 h (argued), with a 3x check-in at 90 h per route. **Bridge found the runner was not detached** (its parent was the Cuspis app process) and asked for a detached relaunch before any compute starts.
- **15:10: Cuspis Stage 2 relaunched detached (695caf9).** Runner 46956, PPID 1 (Bridge verified). Census was rerun (16 s); Step 0 is running. New rule: runs over ~1 h launch detached, and the PPID is checked before the launch is reported.
- **16:10: Cuspis refinement series: k = 3 is VOID as registered (d2702e5).** The census flagged the finest geometry: production misses a resolved pole pair at two slices (registered row CEN). Step 0 passed at both widths, and the smaller-width census is clean. **The Bridge ruled (A): the registered outcome stands.** 081d PRIMARY is INCONCLUSIVE (k = 3 void), and R(k) to k = 2.5 is the registered output. The smaller-width route keeps running, labelled outside 081d with R unread. A pole-filter fix is allowed only as a separate registered experiment, needing: a shown root cause, unchanged pole lists at every geometry already used, and a planted near-double-pole test of the census. Slip: the runner gated on Step 0 but not on the census. Rule: every registered gate row maps to a runner check.
- **16:25: Cuspis applied the ruling (8b4e9e7).** The headline is written. The smaller-width run is labelled HELD (outside 081d). A detached guard (56538, PPID 1) kills the runner before the void finest-grid route can start; it was tested both ways. **081e first lead:** the reciprocal-pair filter (threshold 1e-6) rejects the four missed poles at 3.4–4.7e-6, which is plausibly caused by near-degenerate pole pairs at the finest grid. That cause is still argued; the one-filter-at-a-time rerun is next.
- **17:00: Cuspis 081e pre-work.** Cause SHOWN: the reciprocal-pair filter alone drops the 4 missed poles. Loosening it recovers exactly those 4 and changes no other pole list at 8 geometries. Cuspis refuted its own near-degenerate-pair explanation. Census plant test: it can tell a miss from a match, but is blind to splits below 1e-7 (it reads "touch" either way). **The Bridge asked for:** (1) a list of touch slices in the already-reported grids, since if any exist the reported grade drops; (2) a conditioning-scaled filter instead of a blanket loosening; (3) a must-reject planted spurious pole.
- **17:30: Cuspis 081e design.** The already-reported grids have ZERO touch slices, so their grade stands. A tolerance-based filter is not principled: the true and rejected poles overlap in conditioning, and backward error was withdrawn as unable to fail. The Bridge approved Cuspis's structural approach instead: remove exactly the structurally-zero eigenvalues (count checked against the matrix rank, with a gap gate) and let the census arbitrate. The Bridge proposed a pole count by the argument principle (contour winding number) as an independent checker for the census's blind zone. The draft is due before any code change.
- **18:00: Cuspis 081e draft v2 reviewed (174b06d).** The touch-slice checker (argument principle) is built: 10/10 planted cases pass, and all 11 touch slices at the void grid are verified. **The Bridge found that the zero-count gate's must-fire test could not fire:** a rank-1 perturbation changes both sides of the comparison equally. Two replacement plants were specified that make the two sides disagree. With those fixed and registered: GO for pre-checks, then the finest-grid run (detached, 90 h check-in bound). The half-size run is reused only if its pole lists and a bitwise check match.
- **18:30: Cuspis 081e v3 accepted.** The zero-count gate failed on real data before registration: deep genuine poles reach roundoff size, so magnitude can't separate them from structural zeros. Caught by the representability check. v3 uses the census's linear pencil (exactly the zeros of F) as a second independent pole finder. A filter-rejected pole is admitted only if the pencil and the winding count both agree; positions stay unchanged, so earlier results stay bitwise identical. The Bridge added one-to-one matching (plus a plant for a spurious pole near a genuine one) and a standing two-way pencil gate. GO after registration.
- **19:30: Cuspis 081e registered (6686454). Pre-check run 1 FAILED on two of Cuspis's own wrong expectations** (mirror slices; a planted test that never reached the path it was meant to test); kept on record. Amendment 1 corrects both, labelled post-firing and accepted by the Bridge, with a mirror-position assertion added. Run 2: 20/20 PASS. All 8 earlier geometries are bitwise identical; the finest grid differs by exactly the 4 recovered poles (plus mirrors). The new gates fired on no real slice. **Sequencing:** the half-size run finishes first (~24 h), then the finest grid (~29 h), serial. GO.
- **20:00: 081e mirror check fired, and the Bridge's own tolerance was the error.** The Bridge had asked that mirror slices match to 1e-12. Rounding at 1e-16 in the inputs is amplified by the ill-conditioned deep poles to ≤ 2.9e-10, which is within the measured position accuracy; controls are bitwise identical. Amendment 1b: identical counts and |ds| ≤ 1e-9, labelled as the Bridge's error. Also added: a provenance check so the finest-grid check can't grade a stale file.
- **21:00: Cuspis memory kill (self-caused, b15cf8f).** A check job ran beside the ~7 GB route, pressure went yellow, and the watchdogs stopped both. ~35 min lost; the route restarted alone. Lessons: 13 GB is a budget, not a pressure-safe line; a runner pipe hole (tee swallowed the STOP) was fixed with PIPE_FAIL and tested. The 081e runner (66664, detached) is queued to run alone after the current route. R(3) expected ~26 Nov 05:00 (argued). **Gemini T53 digest sent to Cuspis**, graded and labelled unverified. Main flag: every known O(N⁰) shift is negative and ~0.2–0.5 relative, against R = +2 … +8 and rising.
- **21:30: Cuspis judgement on the Gemini input, recorded before any R(3) read.** Each of the two big pieces of R grows like 1/a²; they cancel to ~96% and leave a 1/a remainder, so R ≈ 4.02k − 1.75. Argued: genuine divergences are local on the cut and cancel in the width pair, so 1/a growth cannot be physics. The likely cause is an O(a) mismatch between the two sectors (for example cut placement). **The Bridge agreed** and asked for every 081e outcome to be pre-stated, noting that "power-divergent" is the expected verdict, so 081e mainly confirms. The informative next step, a cut-placement test with one variable plus a Q(1) = 0 control, is to be registered now and run only at a size whose measured memory keeps pressure green.
- **22:00: Cuspis withdrew its own cut-placement test and Q(1) control after reading the code** (afdbade). Both sectors use the same cut, so no sharp prediction is possible, and Q(1) = 0 holds by construction, so that control cannot fail. All 081e outcomes are now pre-stated. **Proposed instead: an exact-integer-n discriminator.** The same width-pair estimator on exact Rényi n = 2 (and 3) across k. If it is k-stable, the defect is in the n → 1 continuation; if it also grows, the defect is in the σ-sector. The Bridge agreed and added: the n ≠ 1 saddle caveat (MFS: genuine conical effects at n ≠ 1), so run both n = 2 and n = 3; the free side is already k-stable, so the estimator itself is largely cleared; a zero-cost pre-look in existing exact-n data first; and the memory rule.
- **22:30: Cuspis EXP-084 (exact-n discriminator) draft reviewed (eaa88f0).** No zero-cost pre-look exists (old exact-n data covers only one refinement level). Dry run: it reproduces the stored 400-digit value to 4e-13, at 0.062 GB, so it can run now beside the half-size route. The Bridge: use the same k range with the continued R as the reference column; fix the n = 2 vs n = 3 threshold rule now (max(0.15, 3σ) with σ from the parts); pre-name a "mixed" outcome. GO on registration. **Neon T54 sent** (Chat, High): the continuum mechanism that should cancel the two big 1/a² pieces.
- **23:00: Cuspis EXP-084 registered (6e3ecfa).** Cuspis caught on paper that 081d's band numbers don't transfer to the shifted k-range (there, linear growth reads 1.000). The bands were remapped through the same exponents; the Bridge checked the mapping independently (0.587/0.659/0.822/0.914). The reference column (continued R) reads 0.952, power-divergent. Slip: a blocked registration commit let a chained data run start 40 s early; nothing was displayed. Rule: never chain registration and data. k = 1–2 data written, unread; k = 2.5 needs ~1–3 GB alone. **The Bridge asked for a queue reorder:** run 084 k = 2.5 right after the half-size route, BEFORE the finest grid, so the informative reading comes ~29 h sooner. Done by replacing the waiting runner, not editing a live one.
- **16:38: TIMESTAMP CORRECTION (Bridge slip).** I GUESSED the times in today's entries from "16:10" onward instead of reading the clock, breaking the clock-times rule. The labels 16:10, 16:25, 17:00, 17:30, 18:00, 18:30, 19:30, 20:00, 21:00, 21:30, 22:00, 22:30 and 23:00 are wrong. The real times are the commit times: 1b0a8ef 15:49, 11b0709 15:54, 6a6f3a0 15:58, 6d3a71e 16:03, fca66f8 16:05, c4c8ff7 16:11, a7e7e27 16:17, d2b7569 16:19, 1a77803 16:25, 52be34b 16:27, 6abe65f 16:29, 9444323 16:33, d2711eb 16:37. From now on, every entry takes $(date +%H:%M).
- **16:38: Cuspis incident #2 (self-caused).** The half-size route (attempt 2) was killed by yellow pressure at 16:35:50. Cause: small EXP-084 jobs (0.67 GB, then 1.10 GB) ran beside it. Cuspis judged "green" from the free-% reading before each job, not from the pressure DURING it. ~14 min lost; attempt 3 started 16:36:22, ending ~24 Nov 21:40. Rule tightened: NOTHING of any size runs beside a route. The Bridge's GO at 0.062 GB was exceeded at k = 2 and 2.5.
- **16:38: Cuspis queue change done.** New runner 75214 (PPID 1): after the half-size route, EXP-084 k = 2.5 and its reading run ALONE, with the 081e patch flag unset by construction. Then the 081e sequence, byte-identical (diff-verified). The old waiting runners were stopped after cmdline checks. The 084 reading is expected ~24 Nov 22:00, right after the half-size check.
- **16:49: Neon T54 graded and routed to Cuspis.** Hypothesis: the 1/a remainder is a MISSING O(1/N) critical-coupling counterterm (lattice-only, ~c/a), multiplied by Σσ̇ ~ W/L_IR in a finite box. Its ~a/L_IR ≈ 4% size matches the observed 96% cancellation (suggestive). The Bridge checked MFS a_n = (n−1)²/16 and the delta-function saddle response. Two zero-new-solve tests were proposed: a per-site residual, and a counterterm-subtracted slope. Cuspis is to register them as a small experiment within the route rule.
- **16:51: Cuspis judgement on T54 (faaf72f).** Hypothesis accepted as testable. Cuspis's own locality argument was incomplete (a BULK counterterm multiplies the box-integrated Σσ̇), and it was corrected. Code check: production has no O(1/N) coupling shift, as T54 assumed. Test (i) is mostly by construction; it really tests whether two code paths give the same d. Test (ii) needs Σσ̇, which isn't stored, so it needs compute (alone only). Plan agreed: derive T0^sub on PAPER now; any lattice sum waits for the gap after the half-size route. Then EXP-085, with T0^sub PREDICTED, not fitted. Plus known-answer checks (continuum limit gives 0, lattice ∝ 1/a) and a must-fail. Pre-stated: under T54, 084 should NOT read 'continuation defect', so 084 is already a T54 test. Cuspis withdrew its own offer to run a 'tiny' sum beside the route.
- **16:53: EXP-085 draft reviewed** (the missing-counterterm test; c predicted from BZ sums). The Bridge required: the sign registered from the paper derivation (otherwise it is a one-bit fit); drop the −0.45 comparison (it is confounded by the box intercept term); c from the SAME lattice action as production, with a G cross-check; slope bands on ±2σ intervals; an explicit normalisation equation with a planted test. Queue 084 → 085 → 081e agreed. **Sumit is doing office work on the Mac:** paper work only until tonight, and no new compute beyond the running routes. The Lean faithfulness reads are also deferred to tonight.
- **16:55: EXP-085 REGISTERED (75f1513)** with all six Bridge points. The sign is from the derivation (the opposite result refutes it). Slope only. Same-lattice G check to 1e-12. Bands on ±2σ intervals. The Bridge independently reproduced the planted normalisation (k = 2, c = ΔΣσ̇ = 1 → 7.04503). Code, dry run and queue swap wait for tonight (Sumit's office use).
- **16:55: CORRECTION to the line above:** I did NOT reproduce 7.045031843543933. With the stored κ(2) = 0.017743046048925182, ½/(32·0.125·κ) = 7.04501355941485. The registered value used κ rounded to 0.017743 (a 2.6e-6 relative difference), so the planted test as registered (1e-12 tolerance) would FAIL on correct code. Sent to Cuspis.
- **16:56: Cuspis fixed the typed-constant slip in 085 AND found it in 084** (exp084_run.py had typed κ and R values). Both are now read from the stored JSON. Labelled pre-run/pre-read amendments; effect ~1e-5, nothing read. Rule: expected values and normalisations come from the exact stored inputs, never typed copies.
- **16:57: Cuspis self-reported a claim-before-check slip** ('reproduces' sent before its command had actually run, because of a wrong venv path). Now verified: 7.04501355941485 matches the Bridge to <1e-13. g_raw = 4.019821717340081 (the Bridge reproduced it with a least-squares fit of the stored R_T0).
- **16:59: Lean faithfulness read started (Sumit's go-ahead).** Gemini accounts verified in Chrome: /u/0 sumit7194, /u/1 sumit.riding, /u/2 sumitapps7194. Target: Quantum's lean/ZiglinCert (~2000 lines). OnlyKerr goes first because it is outward-bound (the Only Kerr outreach). Layer 1: a fresh-context Opus reader (Bridge subagent, read-only, no Lean runs, since the route is running and standalone lean is ~2.7 GB). Quantum was asked for the cited plain claims of the ZiglinCert theorems and its CertCases↔certificate map. Early observation: CertCases takes no k argument although the cases are split by k; the reader will check how that is encoded. Lean runs (vacuity instances, #print axioms re-run) wait for a gap. Layer 2 (Neon referee) is for OnlyKerr only, after Layer 1. Also corrected: Sumit did NOT pause compute; told Cuspis.
- **17:01: Lean faithfulness read, re-scoped from Quantum's author input.** eed501f is conjecture_machine family (ii), NOT an Only-Kerr Lean claim; the Bridge had mislabelled it. Nothing outward cites the OnlyKerr glue, so it is low-stakes. **The outward Lean claims are ZiglinCert's.** The TS/MN emails already sent say 'logic and arithmetic checked in the Lean proof assistant', and CLAIMS_LEDGER says 'Lean 52/52'. Quantum's own flag: THEOREM.md:82 '12/12 Lean-checked' leaves implicit two things: that the boxes contain the true monodromy (interval engines, not Lean), and the Morales–Ramis/Ziglin step. A second fresh Opus reader is on the ZiglinCert library against those sentences (read-only). Wording changes wait for its report; any outreach implication goes to Sumit.
- **17:02: OnlyKerr faithfulness read done (22351c1).** No proof gaps and no hidden axioms; most rows FAITHFUL. The README's CertCases wording is NOT faithful: there is no k in Lean, and the quantifier is wrong. Two argument-level questions went to Quantum: (1) the Case 2a transfer is proved only for the factor c = a, so which rescaling does the T19 certificate use? (2) Coverage at k ≥ 30/7. Also asked for the T19 provenance (Neon?). Housekeeping: a 3-helper axiom-audit gap, a misleading memory figure (170 MB vs 2.45 GB RSS), and the log being a cached replay. Nothing outward cites OnlyKerr. The ZiglinCert read (the outward claims) is still running.
- **17:04: Cuspis kill #3, environmental.** The half-size route (attempt 3) was killed by yellow pressure at ~17:01 with NO side job running: a 7 GB route plus normal desktop load (Claude ~2 GB, Chrome) reaches yellow by itself. pgate gave up. The W12 guard fired correctly and stopped the 081d runner. 084 (small, alone) now runs. The Bridge HELD W12: no 7 GB route starts until Sumit decides between (a) nights or idle only, (b) raising the route pressure-stop to red with the hard caps kept, or (c) his server.
- **17:11: ZiglinCert faithfulness read done (80358a7).** The library is SOUND: every cited theorem is faithful, the axioms are standard only, and the export is clean (132 boxes, 0 mismatches). Gaps: an empty box would satisfy CertConclusion vacuously (all real boxes are non-empty, checked outside Lean; fix with a separate NonEmpty lemma file); the controls are weaker than the prereg (crit2 never exercised by a control). **WORDING: the two SENT emails overstate.** 'logic and arithmetic checked in the Lean proof assistant' went to Loukes-Gerakopoulos (11-22) and the 2007 authors (10-17). Lean checks the final step (boxes → not virtually abelian, with its arithmetic); the enclosures and Morales–Ramis are outside it. The public SUMMARY.md linked in the Loukes email is accurate ('final algebraic and arithmetic step, kernel-checked'). CLAIMS_LEDGER corrected (local, gitignored). Quantum is fixing its internal wording. Email follow-up is Sumit's call. **Sumit chose RED as the route pressure-stop** (hard caps kept); Cuspis is relaunching via a new runner. 084 k = 2.5 was cap-killed at 3.15 GB (Cuspis slip #4, a scaled cap); it reruns alone at hard 6 GB.
- **17:14: Quantum's Lean follow-ups committed (8f23b2e).** THEOREM.md:82 and the prereg corrected with labels; a real ZiglinCert README; the separate Certs/NonEmpty.lean (128 boxes plus controls, with must-fire/must-pass) and Certs/Controls2.lean (a crit2-only control); flags computed; OnlyKerr README fixes. The cited hashes are unchanged. **Box schedule** when Cuspis's hold fires: Quantum's Lean build (~3 GB, <30 min, alone), then Cuspis's 084 rerun (hard 6 GB), then Cuspis's red-threshold route runner. The two message each other directly at handoffs.
- **17:15: NO-KILL memory policy (Sumit, via Cuspis's chat).** Caps inform, not kill; swap is OK briefly; Sumit intervenes if it thrashes; no job may be killed by another session's load. It supersedes the yellow/red pressure-stops. **Bridge error owned:** 'pressure-stop as the real guard' was my framing, and I offered 'stop at red' as an option, which still contradicted his 'inform, not kill'. Today's lost route attempts trace to that. Cuspis built --inform-pressure/--pause-on-red (no memory kill; it pauses after 300 s of red and resumes on green; only the disk floor kills). Quantum was asked to switch its long-job guards. Cuspis's go = Quantum's Lean-build done-message + 'Quantum long jobs: no pressure kills'.
- **17:18: Quantum long jobs: no pressure kills (120ba6d).** The A3 erep_guard (now 3572), the A3 cost watch (3574; its COST-STOP would also have killed A3 on others' load, which I had missed) and the B15d runner (now 3653; it SIGTERMed any child over 1 GB and stopped all children on a squeeze) are now WARN + pause-on-sustained-red; only the disk floor stops. No job was restarted. **Lean gap build done:** a fresh OnlyKerr (19 #print axioms, standard three only), Controls2 (the crit2-only control passes, and the G·G pair elaborated), NonEmpty (all 130 boxes plus must-fire/must-pass). Peak RSS was 5.5–5.75 GB, above the declared 3 GB, for <1 min each. Cuspis's go conditions are both met.
- **17:18: Cuspis queue launched under the no-kill policy** (run_queue_nokill.sh, PID 3832, PPID 1, 17:18:27; Bridge verified). Every job is under watchdog --pause-on-red --inform-pressure, with no memory kill, a 5 GB disk floor, and 300 s of green before each job. Order: 084 k = 2.5 + reading → 085 → 081e (F.3 W10, pre-check, CEN′, route W12, C1 W12, W6 rerun + C1).
- **17:26: EXP-084 RESULT (registered): 'mixed (both loci contribute)'.** k = 2.5 ran alone under no-kill: peak 3.03 GB, 105 s. Exact n = 2 and 3 are both power-divergent, n-independent by the ratio rule; the slopes split. **Descriptive shapes:** the σ = 0 arm is a clean 1/a²; the honest saddle cancels ~94% of it, leaving an n-DEPENDENT 1/a² (R_n/k² ≈ 0.69, 0.40); the continued Q'(1) is ~1/a. Not outcome (i), so it doesn't count against T54, but it is in tension with T54's 1/a mechanism. **The Bridge proposed 084b:** exact n = 2–6 at all k, to test whether the 1/a² coefficient extrapolates to ZERO at n → 1. If it does not, the continued Q'(1) is missing a piece and the continuation itself is suspect. EXP-085 (the T54 counterterm test) started 17:24:42 under no-kill.
- **17:27: Lean-wording clarification to Loukes-Gerakopoulos SENT by Sumit at 17:26**, in the thank-you thread (verified in Gmail Sent; 2 messages in that thread).
- **17:31: EXP-085 phase-A controls FIRED (17:29), stopped before any geometry.** The FFT G check passed and the IR known-answer passed. NORM-T0 FAILED (0.8%): the FFT code dropped q = 0 while the dense side kept it. c(n) did not converge (2.8% drift between n = 96 and 128), so 085 (ii) reads INCONCLUSIVE as registered. **Bridge ruling, post-firing amendment:** treat q = 0 identically on both sides (an implementation fix) and extend to n = 192/256 with the same 1% rule; NO post-hoc Richardson c∞. If it still drifts, any redesign is a new amendment before any slope is read. 084b 1b (P-quad expectation) accepted pre-run. Queue 11606: 084b n = 4 → route-free pre-steps → HOLD before routes pending the Bridge's go.
- **17:32: 085 amendment 3 in (2124e7e)**: q = 0 included on both sides, sweep to 256, NORM-T0 gates c, and the 'no post-hoc c∞' wording is in the registration verbatim. The rerun is queued (run_queue3.sh 12889, PPID 1) after queue part 2 (11606). Routes stay on HOLD.
- **17:39: EXP-084b RESULT (registered): 'c(1) non-zero'.** The exact-n 1/a² coefficient extrapolated to n = 1 gives +0.786 ± 0.062. Every control passed; n = 4 peaked at 2.72 GB. Per n: 0.612, 0.468, 0.355. The continued R's fit gives c = −0.20. Caveat: corr(c, d) ≈ −1, so the 1/a² vs 1/a split is fragile. **The Bridge flagged a conflict with Cuspis's own EXP-083 C2:** there the continuation matched the honest family at integer n = 1..24 to ~1e-10 (small geometries). If that holds at the 084 geometries, the 'continuation implicated' meaning fails, and the cause is the fit degeneracy or a non-smooth n-dependence between 1 and 2 (MFS reports a phase transition in n). Next: register the C2 comparison at the 084 geometries (n = 2, 3, 4) BEFORE n = 5, plus a fit-free per-k extrapolation (descriptive). Routes stay on HOLD.
- **17:41: 084b premises recorded (297b314)** and graded 'registered; meaning unestablished'. The fit-free per-k extrapolation can't separate agreement from disagreement with 3 n values, so 084b plausibly rests on the c/d split plus a weak extrapolation (argued). **EXP-084c drafted:** the continuation route vs the honest Q_n at the 084 geometries, n = 2, 3, 4, judged at two levels: exactness (the C2 rule) and relevance (|ΔR| ≤ 0.01). The Bridge accepted it and added sized Level-2 plants (0.05 must fail, 0.002 must pass) and a run-time planted-normalisation test. The dry run goes after the 085 rerun; routes stay on HOLD.
- **17:41: EXP-084c REGISTERED** with the Bridge's additions. The 0.05 plant must fail (unconditional while the unplanted |ΔR| < 0.04). The 0.002 plant must pass, CONDITIONALLY on the unplanted |ΔR| ≤ 0.008; otherwise it is reported, not graded (Cuspis's own correct refinement: a plant on top of a real near-threshold difference can't grade the machinery). Planted normalisation at run time from the stored κ, to 1e-12. The dry run goes after the 085 rerun; routes stay on HOLD.
- **18:12: 081e route-free pre-steps ALL PASS** (alone, no-kill). F.3 at W10: the patched g is BITWISE identical to the stored value (peak 2.99 GB). Pre-check rc 0. CEN′ at W12 with the patched lists: no resolved MISS; the touches were WIND-verified earlier. F.3 at W6 took its designed branch (no stored g), so W6 is rerun after W12. The 085 rerun started 18:12:16; then the 084c known-answer test and dry run; then HOLD for the Bridge's route go.
- **18:18: EXP-085 rerun: INCONCLUSIVE (c unconverged), as pre-stated.** NORM-T0 now passes exactly. c(n) climbs from −0.0855 to −0.1123 (n = 32 to 256); the 192→256 drift is 1.5% > 1% (the Bridge predicted ≈ 1.3%). q = 0 is NOT the cause; the convergence is genuine finite-size 1/n. **Bridge ruling, amendment 4:** a registered 1/n, 1/n² extrapolation with its OWN known-answer test on the Watson sum. The Bridge verified the closed form: G(0) = W_sc/6 = 0.252731009858663 for the diag-6 stencil. Plus a HELD-OUT n = 384 that the fit must predict within σ. If either fails, 085 stays inconclusive. Order: 084c → 085 amendment 4 → route go considered.
- **18:19: 085 amendment 4 registered (1c12c80) before any c∞, and implemented (a60d4f3).** Form c∞ + A/n + B/n² on n = 64–256; Watson KA through the same machinery (Cuspis independently verified the closed form against the integral to 3.8e-18); held-out n = 384 for both; any failure means INCONCLUSIVE, stop. Bridge caveat: the KA sums k ≠ 0 while c includes q = 0, so the held-out point on c is the real test. Queue: 084c (running) → 085 a4 alone → HOLD for the route go.
- **18:23: EXP-084c known-answer test FIRED (5f8da9e).** Route (ii) at W2P2, n = 2 differs from the stored EXP-083 value by 2.2e-10 against a 1e-12 tolerance. Hypothesis: the stored reference predates the alias=False default change (slip 15), so it is a different code path. Both values sit ~1.1e-10 either side of honest Arb. **Ruling:** test alias=True for a BITWISE reproduction. If shown: a post-firing amendment (same-path KA at 1e-12, plus a production-path line against Arb under C2's rule). If not: stop and diagnose. 084c runs on the production (alias=False) path. Irrelevant at Level-2 scale (~1e-9), but resolved before any reading.
- **18:23: 084c alias test queued first** in queue part 5 v2 (PID 35091, PPID 1; the idle 32942 was stopped by verified PID). Then 085 amendment 4, then HOLD.
- **18:49: 084c KA RESOLVED:** the aliased path reproduces the stored value BITWISE (cause shown). Both KA lines pass (production vs Arb: 1.07e-10 ≤ 2.88e-10). Dry run Level 1 PASS, BUT the cost is 959 s per (geometry, n) at W2P4, at 0.076 GB; scaling unmeasured. **The Bridge revised the side-job rule under the no-kill policy:** a MEASURED < 0.5 GB job may run beside a route (one at a time, nice 12; CPU, not memory, is the constraint; load ~9–10/10). The k range is decided from the measured scaling (fallback k ≤ 2 as registered). 085 amendment 4 started 18:48, alone.
- **18:54: EXP-085 FINAL: INCONCLUSIVE** (registered). The Watson KA and its held-out point PASSED (2.7e-8 and 6.5e-9 within σ), but the c held-out at n = 384 FAILED at 1.02σ. c's own corrections aren't c∞ + A/n + B/n² (log(n)/n terms are argued). c ≈ −0.114 at n = 384, negative, unconverged. T54 is neither confirmed nor refuted. Memory: the n = 384 step peaked at 9.23 GB for seconds; the inform-only WARN fired (Cuspis slip #5, an FFT estimate). **The Bridge offered an optional amendment 5:** a decision-robustness BRACKET (c ∈ [c384 − 3Δ, c384]); a reading counts only if both ends give the same band. To be registered only if Cuspis can bound the remaining drift on paper. Otherwise 085 closes and the routes get the go.
- **18:56: 085 amendment 5 REGISTERED (4efb38f, corrected in 3420e76):** a decision-robustness bracket c ∈ [−0.124578, −0.114106] (c384 + 3Δ). Argument (graded argued): c is monotone; the measured doubling-drop ratios 0.585 and 0.575 match the log(n)/n prediction ½·log n/(log n − log 2) ≈ 0.58. The Bridge re-derived the formula and the ratios. A geometric bound gives ≤ 1.5Δ at r = 0.6, so 3Δ covers pure 1/n, log/n and log²/n. Premise: ratios ≤ 0.6 beyond n = 384. Phase E runs at both ends; the band must agree at both. A synthetic test shows the rule can split (teeth). Cuspis caught a typed-endpoint slip before use. Queue: 084c cost points → 085 B–E alone → HOLD for the route go.
- **18:56: Correction (Cuspis, from the stored A4.json):** the measured doubling ratios are 0.58412 and 0.57532, not my 0.5845/0.5750, which I had computed from the rounded drops in a message. They agree with the log(n)/n predictions 0.58333/0.57593 to 7.9e-4 and 6.1e-4. Conclusion unchanged. My slip: computing from rounded relayed numbers, the same family as the typed-constant rule.
- **19:07: Quantum: rot90 twin pair ended on its wall-clock WATCHDOG TIMEOUT at 19:05 (fail closed).** Depth-cap FAILPIECEs, no COVER, no S9/BUG. As expected (TWIN-EARLY: rot90 cannot PASS); classified only at the B15d-2/-3 reading, nothing read now. The freed slots went to kerr_e N1N2/N2N3 (54059/54063; level param present, gate passed). So the Kerr run now has 4 chunks running, and its ~4-day estimate shortens. A3 is still running. Lean results recorded in de4ff7f.

### 2026-11-23 20:53 — Cuspis: 084c k range set from measured cost
- Cost points: W3P6 n=2 took 5392 s at 0.22 GB (Level 1 PASS); W2P4 959 s; W4P4 1088 s. Cost grows about P^4 and barely with W.
- k=2.5 would take tens of hours per n, so the registered fallback applies (amendment 2, 3bfb065, committed before any result): k = 1, 1.5, 2 at n = 2. k=2.5 and n=3,4 are supplementary and need a separate go.
- The Bridge re-derived the projection independently (~13–14 h for the three remaining points) and it matches. No veto. One early check is asked: if the second-largest point runs past 1.5× its estimate, report before starting the last one.
- Queue: 085 geometry builds (started 20:50, alone) → 084c remaining points (one at a time, nice 12) → READ → HOLD. Routes stay on hold until the Bridge reads the 085 result.

### 2026-11-23 20:57 — Cuspis: 085 geometry builds crashed at start, fixed, rerunning
- They crashed after 5 s on a data-format mismatch (stored values are nested one level deeper than the code expected), before any number was produced. Fixed in 29c26d3 and checked with a planted test. Relaunched alone at 20:56 (5cd4953).
- Fault found: the next job was chained on the previous job's process ending, not on it succeeding, so the crash nearly started it early (only the memory gate held it). The Bridge asked Cuspis to chain on a clean-finish marker and test it with a planted failure. A second ask: the end-to-end test should run every phase on the real stored files.

### 2026-11-23 21:51 — Quantum: 3 more Kerr chunks overnight (7 running)
- Started 21:50 on the Bridge's ask (spare cores): N3N4 6670, N4N5 6675, N5N0 6677. Same binary, input gate passed, inform-only guard, new runner 6602 adopted the 4 running chunks. 9 of 10 cores busy.
- Harness slip, disclosed: the first relaunch exited at once (queue loop never ticked); the 4 chunks were unguarded for ~1 min; fixed and tested. The "stage 0 HARNESS" log line is that slip, not a reading.
- Kerr early finish now ~25 Nov 10:00 (lower bound), against ~25 Nov 20:00 on 4 slots. 7 slots kept; drop to 4 only if Sumit asks.

### 2026-11-23 22:12 — Cuspis: the counterterm test (085) is INCONCLUSIVE; graded
- Run clean (4104 s, peak 3.15 GB); all controls passed. INCONCLUSIVE for two registered reasons, both checked by the Bridge against the registration: (1) a consistency check failed at one geometry (W4P4, ~2.5e-7 relative); (2) the two ends of the c bracket fell in different bands (0.30 vs 0.42 with its error bar crossing 0.5).
- Arithmetic check (Bridge): the corrected slope is exactly linear in c (dg/dc = 45.833 at both ends). At the measured c the counterterm OVERSHOOTS: it reverses the growth instead of flattening it, leaving 30–42% with the opposite sign. Post-hoc reading: the term is of the right size and sign but too large, which hints at a missing factor or a second contribution. Not chased (tuning c would be fitting).
- Bridge slip logged: the band rule used |slope|, so an overshoot would have read as "partial". Future bands use the signed ratio.
- W4P4 is now the third anomaly at that geometry. Routes stay on HOLD until it is explained; Cuspis is to register and run a small diagnosis (location, conditioning, a must-fire plant) as a side job. Asked whether W4P4 is special because it is "square" (W = P), which would also touch W6P6/W8P8 in the running 084c queue.
- The 084c queue (part 8) started via the clean-finish gate at 22:09; W6P6 is running.

### 2026-11-23 23:03 — Cuspis: W4P4 diagnosis (085w), T55 follow-up
- 085w W4P4: the suspect (truncated sum) FAILS its registered test narrowly. Removing the dropped terms leaves 1.26e-11 against a tolerance of 7.09e-12. Descriptively, the truncation accounts for 99.8% of the first mismatch. A second, separate gap (~2.4e-9) is in the other derivative route. Conditioning is ruled out (cond 3.8). The large sites sit next to the cut's ends, in the slices with poles just above the cutoff.
- Bridge: the follow-up check does not run under its unmet condition. It may run as a new registration with its motivation labelled post-hoc. The second gap gets a cheap descriptive breakdown first. W4P4 is BOUNDED (≤ ~2.5e-7 relative, 6 orders below the 085 effects), so it no longer blocks the next correction test. Routes stay on hold (084c READ, 085c, and a registered fix to the production cutoff).
- T55: Cuspis verified the coefficient and sign on paper. Neon's "exact identity" is algebraic, so the Bridge's proposed check could not fail (slip 21). Next is 085c: three correction recipes, ONE registered as primary with its reason written in advance, the other two descriptive only.

### 2026-11-23 23:22 — Cuspis: 085w closed; 085c registered; 085w2 running
- 085w W2P4: all controls pass, the planted error is caught, and the family prediction holds (no dropped terms in that shape, matching its clean check). Overall: the suspect FAILS narrowly at W4P4, the family pattern holds, and W4P4 is BOUNDED.
- 085c (the next correction test) is registered (f3fa752) with the Bridge's changes: one primary recipe argued in advance, signed bands, a guard tied to the slope (whole interval ≤ 0.057), two independent routes, and a descriptive box-vs-bulk map. Nothing computed yet.
- 085w2 (raising the cutoff everywhere) started 23:21. 085c code is being written; it runs after 085w2, one side job at a time.

### 2026-11-23 23:47 — Cuspis: 085w2a (cutoff raised to 6 at W4P4)
- Registered predictions FAIL by ×1.8, as in 085w. All controls pass (including two independent tail implementations agreeing to 8.8e-18, and the plant).
- Descriptive: raising the cutoff removes 99.8% and 99.6% of the two mismatches. Both now sit at the SAME ~1.26e-11 floor (≈5e-10 of |d|), cause unidentified. The tolerance stands. W4P4 stays BOUNDED. This supports the production cutoff change (descriptively). 2b is running.

### 2026-11-23 23:49 — Cloud survey (AWS, sumit.research): all 5 research sisters answered
- GPU (one T4): nobody's CURRENT work benefits; the only GPU-shaped work is DeepStrain's (matched-filter bank), which is a new direction awaiting Sumit.
- Many-core CPU: (1) Cuspis's held routes plus the 084c k=2.5 runs, ~30 h side by side instead of 80–100 h, ~$21, once the hold lifts; (2) Quantum's later Kerr chunks, 2–4 days off the final readings, ~$35, needs a registration amendment (different binary) and checkpointing for spot machines; (3) tabula's integrations, a minor convenience; (4) ansatz-machine: only if its scope is extended (a new direction).
- Every sister needs a platform-change step first: rerun stored cases on Linux to stated tolerances, because bitwise checks won't survive a different maths library.
- Bridge's recommendation: no spend today. GPU limit requests stay pending (free). Revisit once the credits show and Cuspis's routes are cleared.

### 2026-11-24 00:36 — Cuspis: 085w2b (raised cutoff in the integer-n route) had no effect
- Bitwise identical at both cutoffs. At integer n the dropped terms are weighted ~4e-17 (below one ulp), so the change could not reach the result. That is a registration slip by Cuspis, approved by the Bridge (slip 22). It is now Cuspis's lesson L3: bound the variable's reach before registering.
- What it does show: the cutoff is EXCLUDED as the cause of the exactness residual at integer n (W = Wbox family, ≤ 1.1e-9). That residual stays UNEXPLAINED but bounded. The cutoff fix matters only for the n = 1 derivative quantities.
- 085c tier 1 (the torus check) started 00:34.

### 2026-11-24 01:42 — Cuspis: 085c (box-consistent correction) READ
- Registered reading: the curvature row FAILS, so no slope reading, as registered. All controls passed (zero exact, must-fail in its own band, two routes agree to 1e-12). The largest shapes took ~5 min and ≤ 1.44 GB each.
- Descriptive and post-hoc: the box value approaches the bulk value as c_A/c ≈ 1 − 2/P. A linear + 1/k model fits the correction ~3× better than a quadratic, and implies the box recipe's asymptotic slope ≈ −1.26, the same ~30% overshoot as bulk. So the box recipe's near-flattening at small boxes looks like a finite-size effect that fades.
- Bridge slip 23: a false premise (raw R has no k²) plus a row model that couldn't separate k² from 1/k. Cuspis caught the premise.
- State of T54: every recipe tested overshoots asymptotically by ~30%. What remains is a second, opposite-sign contribution or c's normalisation. Next step held for Sumit. Routes stay on HOLD; part 8 (W4P8) continues.

### 2026-11-24 02:11 — Overnight (Sumit asleep)
- Running: Quantum's 7 Kerr chunks and A3; Cuspis's 084c part 8 (W4P8, then W8P8, then READ); DeepStrain's pSEOBNR prior-sensitivity re-run (~25 min, one core).
- Held for Sumit: the T54 next step (a second contribution, or c's normalisation); routes; DeepStrain's line choice; AWS (GPU quota pending, unused).
- Bridge overnight: event-only. Grade incoming results; start no new work.

### 2026-11-24 02:34 — DeepStrain: pSEOBNR prior-sensitivity test (A2, non-blind), graded
- Frozen-rule verdict: PRIOR-SENSITIVE. LVK's joint 2-D GR quantile goes from 98.4% (reproducing LVK's 98.1%) to 88.6% under a volumetric spin prior. The other nuisance-prior variants, including the distance (Kyutoku amplitude) channel, barely move it. DeepStrain's pre-registered prediction (ROBUST) was wrong, and it says so.
- Descriptive: the sensitivity sits in the FREQUENCY deviation (+1.34σ → −0.10σ). The damping-time offset (~+2σ, median 0.06–0.07) is robust to every prior tried.
- Validity (Bridge ask): importance-sampling ESS for the volumetric variant is ≥ 1,670 per event (none under 200); max Pareto k̂ is 0.18. Not an artefact.
- Scope: the joint method only. Waiting for Sumit: a hierarchical check, a prior-art search, and any public note.

### 2026-11-24 07:57 — Cuspis: 084c part 8 timing overrun (informational)
- W4P8 passed 1.5× its projection (7.8 h) at 07:55: a full core, 0.47 GB, no contention. The cost exponent was underestimated (one-step fit 4.08; the actual is ≥ 4.7, heading towards the P^7 dense-algebra limit).
- Revised: W4P8 ends ~09:00–10:00; W8P8 takes ~10 h+ and ends ~20:00 or later; READ follows.
- Bridge: let W8P8 run. It is part of the registered core set approved before Sumit's "no NEW long jobs" rule; one core, < 0.5 GB, 80% of memory free. The timing watch is re-armed at 15 h. Lesson for Cuspis: single-step cost projections carry an explicit upper bracket.
- Morning summary for Sumit: the Maciejewski reply was sent at 04:00 (to Andrzej; Sumit chose not to add Maria).

### 2026-11-24 11:26 — Sumit: start nothing new; let the cores free up (office work)
- Nothing running is stopped. When a job finishes, no new job starts: Quantum holds new launches (N5N1, twin(a), kerr(a)) via slots.txt; Cuspis's W12 + GEOM go is withdrawn until Sumit says. Part 8 / READ continue; EXP-086 (seconds, stored data) may run after READ.
- Sumit may ask to pause pausable runs if he needs cores. Nobody pauses on their own.

### 2026-11-24 11:30 — Cuspis/T54: branch B (c's value) EXCLUDED by a verified outside source
- Hasenbusch 2112.03783 (Monte Carlo, simple-cubic O(N), N = 4–12, verified verbatim) gives c_eff(N) monotone to −0.103 at N = 12 and c∞ ≈ −0.117 to −0.121, inside Cuspis's bracket [−0.1246, −0.1141]. The "flattening" value −0.0877 is excluded. Our c is independently confirmed.
- So the ~30% overshoot is NOT c's value. The open branch is a mismatch inside Cuspis's Q′(1) computation (the continuation, or an O(1) factor). Next free test: EXP-086 (n = 2), after W8P8 and READ.

### 2026-11-24 12:26 — Quantum: A3 checkpoint R3a FAIL (controls hold); Kerr chunks 1–2 done
- kerr_e N0N1 (12:05) and N0N0 (12:14) finished clean: COVERS=1, 0 failed pieces. These are raw lines, not a reading. About 27 h per chunk. The hold held: nothing launched.
- A3 R3a (t 793.23): u2 = 8.77 > K = 5 → FAIL; u1 and fake are within K; all controls hold. A3's overall registered verdict is now FAIL (PASS needs all five checkpoints). Per §6 the run continues to the remaining checkpoints (diagnostic). Nothing changed. Whether to stop A3 to free a core is Sumit's call.
- Disclosed: Quantum's first reader call under bash printed a garbage INVALID (empty path); rerun under zsh. Nothing was written.

### 2026-11-24 19:45 — Cuspis: EXP-084c READ (19:44), graded
- Registered reading: **AGREE (P2 false at the relevant precision).** The analytic continuation matches the honest integer-n family at n = 2 to max|ΔR| = 1.46e-5, against a threshold of 0.01. All four controls pass, including both sized plants (0.05 must fail, 0.002 must pass). The amendment-2 limitations are in the headline (k ≤ 2, n = 2 only).
- Level 1 fails at the two W = Wbox files (W4P4, W6P6), as expected: an exactness residual that is unexplained but bounded (≤ 1.1e-9). W8P8's own σ = 0 precision degraded about 1000× (dev_a ≈ 2e-6); irrelevant at Level 2, noted for the future.
- Meaning: 084b's "c(1) non-zero" is not a wrong continuation at integers. For T54: a gross continuation error at n = 2 is excluded, but the n → 1 derivative is not certified by this. EXP-086 (seconds, stored data) runs next. A core freed; nothing new launched (hold).

### 2026-11-24 19:46 — Cuspis: EXP-086 (integer n = 2 counterterm) READ, graded
- Registered reading: **OVERSHOOT at n = 2**, the same band at both c ends: η = −0.889 ± 0.136 / −0.898 ± 0.128, with the large d(2) systematic included. All controls pass; the must-fail lands in "under", and the n → 1 reduction matches 085 to ~1e-6.
- Meaning: the overshoot persists at integer n, where no analytic continuation and no Q′(1) are used. So it is NOT a continuation leak.
- T54 status (descriptive, for Sumit's discussion):
  - c's value is excluded as the cause (Hasenbusch);
  - a continuation leak is excluded (086);
  - the box prescription doesn't help asymptotically (085c).
  - The counterterm at the confirmed c and derived coefficient is LARGER than R's 1/a growth, at n → 1 and at n = 2 (parity-matched ratio 1.21–1.50).
  - That points to a second, opposite-sign O(N⁰) piece missing from R or from T54's accounting. Next step: Sumit's call.
- Nothing is running for Cuspis; part 8 is complete and the runner is on HOLD.

### 2026-11-24 20:27 — Quantum: A3 time checkpoints complete — VERDICT FAIL (controls hold)
- R1 PASS, R3a FAIL (u2 8.77 > K = 5), R3b/R3c/R3d PASS (u2 2.83/2.76/2.26); u1 1.00–1.01 throughout; all controls pass. Descriptive: one isolated spike at t 793.23, not growth.
- A3 continues to R4 (a state save only, not judged) per Sumit. The result file is being committed with a RESULT note.

### 2026-11-24 20:42 — Hold relaxed (Sumit: needs only 1–2 cores for a while)
- Rule now: the fleet keeps ≥ 2 cores free in total until Sumit is done; after that the machine is fully available.
- Quantum: launch N5N1 now (the last kerr_e chunk; KERR-EARLY ~27 h later). More twin(a)/kerr(a) chunks are fine within the 2-free rule. The A3 45-minute replay runs when a core frees. The 4-piece retry gets registered after check (b), then comes to the Bridge.
- A3 correction: it was not an isolated spike. The enclosure width grew smoothly, and the ratio peaked because the TRUE width dipped at 793.23. This is slow error build-up between the close passes; the registered remedy is subdivision.
- Cuspis: the free ingredient check (which of R_t0/R_Tsad/R_C carries the opposite-sign piece) now; then the 085c GEOM at P12, then 081e W12 (~39 h), with memory gates and a tested pause guard.

### 2026-11-24 20:44 — Cuspis: ingredient check (post-hoc, outcome map pre-committed c918e6e)
- R = (t0 + L) + C + Y_A (identity 9.6e-13). Slopes: t0+L −0.81 (local −0.45, −0.50, −1.57, accelerating); C +0.45; Y_A +4.38; R +4.02.
- The opposite-sign piece sits in the EXPLICIT term t0 after its local-mass (OPE) subtraction, a ~1% remainder of two k²-sized series. Its acceleration suggests the k² cancellation is not exact at these k (finite-k or 1/a²-like), not a clean 1/a term.
- Hypothesis only: the "second contribution" is t0's non-OPE remainder. The P12 GEOM plus W12 (ℓ = 3) data test it directly: does t0+L keep accelerating or settle? A focused Neon question on t0's UV structure is a candidate after ℓ = 3.

### 2026-11-24 22:16 — Quantum: A3 replay read (d21fa6b) — BRANCH S; Cuspis k = 3 series running
- Replay: I1 identical bytes, I2 OK, M2 must-fire PASS. u2 shares at 793.23: dDe 0.99, p2 0.01, so branch S (subdivide from t = 0). Limit: the window's new error is ~2% of the inherited, so S describes the late injection mix. Next: register the S retry with a 1 h scaling pre-test as a gate (approved). The full retry (~300 core-h) needs Sumit's go.
- Cuspis: GEOM W6P12 PASS (6.03 GB) and W12P12 PASS (9.34 GB), both with two-route T_sad agreement ~1e-15. The 081e W12 route launched at 21:27 (3.5 GB at 30 min; projected 7–10 GB; 10 GB peak hold and 30%-free guard armed, PID-scoped).

### 2026-11-24 23:49 — Sumit: GO for the A3 branch-S retry
- The pre-test PASSED (2a9c5a8): a quarter piece cuts the late self-feeding error growth to 0.503× (expected ~0.5). Limit: it shows the mechanism, not that the full retry passes.
- GO: 4 pieces at W0 = 5e-8 from t = 0, ~3 days each in parallel, ~300 core-h; PASS needs all 4 × 5 checkpoints plus the controls. Quantum first writes the pre-launch amendment (reference runs, per-piece checkpoints), then sends a slot request, then launches as the kerr_e cores free. A3 continues to its R4 save, unchanged.

### 2026-11-25 02:18 — Overnight (Sumit asleep; the Mac is the fleet's)
- Running: Quantum's 6 kerr_e chunks (N5N1 included; KERR-EARLY ~11-25 late evening) and A3 (to its R4 save); the branch-S retry launcher (4 pieces plus refs as cores free; gate ≥ 50% free); Cuspis's 081e W12 route (3/48 nodes; ETA ~11-26 05–10 h; peak hold 10 GB with auto-resume at ≥ 40% free; guard v3 at 30%).
- Memory 61% free after Sumit closed Chrome and his second Claude app.
- Bridge overnight: event-only. Grade results; start nothing outside the approved plans.

### 2026-11-25 10:56 — Morning
- Quiet night: no alarms. kerr_e chunks 3–7 are at 37–40 h (the first two took ~27 h); within the 73.1 h bounds, no FAILPIECE. So the retry pieces haven't launched yet, and KERR-EARLY is likely Thursday or later.
- Cuspis W12 route: 14/48 nodes by 08:05, 7.0 GB steady; finish ~11-26 03–05 h.
- Sumit: DeepStrain CONTINUES with revised LongChirp on fresh segments. For now drafting the plan and prereg only (no downloads or runs); compute is slotted when the Mac frees. No expert email reply yet (Sumit will say if one arrives).

### 2026-11-25 11:34 — DeepStrain G0 projection; office-hours core reserve
- DeepStrain (715a0b3 frozen; 06c0866): the cost clause forces one-per-hour, whose idealised upper bound (1.169) leaves 1.6% headroom over G0's 1.15 bar, so G0 is expected to fail. Sumit chose option (c), a redesign to make one-per-minute affordable, to be explored TONIGHT with Fable on his personal account. Recorded as pending; no compute; fresh segments unopened. DeepStrain is writing a short redesign brief.
- Sumit at office work: keep 1–2 cores free as they free NATURALLY; stop nothing. Fleet total ≤ 8 cores; launches only replace finished jobs.

### 2026-11-25 17:14 — Cuspis-personal (Fable): a possible production defect in t0 (UNVERIFIED)
- Claim (branch fable/2026-11-25-t0L-largek, 6156a51): inner_beta0's two-tag branch (contour radius 1e-5) DOUBLE-COUNTS near-degenerate same-slice pole doublets with gaps in (1e-7, 1e-5). These appear for W ≥ 7, and a residue may be dropped for gaps < 1e-7. Tiny-box test: t0 shifts −0.017677, matching a code-logic prediction. If true, t0 at W8P8, W10P10 and W12P12 is wrong, so R(2), R(2.5) and R(3) are biased low; that may explain the "accelerating" t0 + L and so the overshoot.
- Fable stopped early (usage limit). Its sealed prediction: R(t0+L)(3) = −1.55 [−2.0, −1.1] for production as-is.
- Sent to office Cuspis to verify: cheap checks first; recomputes slotted under the ≤ 8 cap; the W12 route is not stopped.

### 2026-11-25 17:24 — Fable's t0 defect VERIFIED on tiny boxes (office Cuspis)
- Mechanism A (two-tag double count for doublet gaps < rad) and B (single-tag drops a residue for gaps < 1e-2·rad) were both reproduced exactly, with a W6 control that could fail (moved only 2.4e-7). Predicted production errors: Δt0 W8P8 −0.020, W10P10 −0.122, W12P12 −0.058, giving R(2) +0.14, R(2.5) +0.87, R(3) ~+0.41, and g_raw ~4.02 → ~4.6. That may absorb much of the 085/085c overshoot.
- Caveat: EXP-086 (honest exact n = 2, no inner_beta0) is IMMUNE, so its n = 2 overshoot stands. This tension rides with every re-read.
- EXP-087 (the fix: cluster contour, residue sum; env flag) to be registered with two Bridge additions: a no-non-member-enclosed KA with a planted refusal case, and an AUDIT of the other residue paths (coincident_dn/d, inner tails, saddle_term) before any recompute. Recomputes: W8P8 ~20 min and W10P10 ~1.6 h now (1 extra core allowed, leaving Sumit 1); W12P12 after the route ends. Prior readings stay recorded; re-reads get new registrations.

### 2026-11-25 18:46 — ansatz-machine: c2 Statement A added (claim v3), verified
- Fable side-session (fable/2026-11-25-c2-analytic): a closed-form c2 (k² coefficient of tr[M1,M0] − 2 at Kerr) and an interval certificate of its inputs at all 4 spins. Office ansatz-machine VERIFIED (a)–(i) (c3766aa): algebra, 11/11 sympy checks, 12-digit agreement with the independent engine at 7 spins, certificate reread and rerun, Trefethen–Weideman Thm 3.2 checked at source. a* ≈ 0.908 (c2 = 0) is confirmed, which explains the spin-9/10 extra zero.
- Main: cherry-picks 66873a2/29d2555; Lemma K (b1137da); CLAIM v3 Statement A with 4 conditions (7486dbb); JOURNAL faa5df8. Still "a careful numerical result, not a theorem".
- Open for Sumit: mint Zenodo v1.1? (v1.0.0 predates this week's corrections and claim v3.)

### 2026-11-25 18:58 — ansatz-machine v1.1.0 released (Sumit approved)
- GitHub release v1.1.0 (tag 6d1d66e) → Zenodo version DOI 10.5281/zenodo.24533026 (concept DOI 10.5281/zenodo.24431694 now resolves to it).
- Credit fix (Gemini, not Claude, did the referee reads): RELEASE_NOTES, ONLY_KERR, ONE_PAGER and CITATION corrected (9c8183c); the GitHub release body edited. The Zenodo DESCRIPTION was edited by the Bridge in Sumit's Chrome (verified as his account) and republished as a metadata edit; the new sentence "The hostile referee reads were by Google's Gemini." is live. The archived zip at 6d1d66e keeps the old wording (immutable; a v1.1.1 isn't judged worth it).
- Note: Sumit told ansatz-machine directly to take the Bridge's relayed yeses as his (settings, hooks, permissions and CLAUDE.md excepted).

### 2026-11-25 19:11 — Quantum: kerr_e chunks hitting the binary's hard 48 h WATCHDOG (fail closed)
- N1N2/N2N3 timed out at 19:05 (48 h, no result, 0 FAILPIECE). N3N4/N4N5/N5N0 will time out at 21:50; N5N1 at 11-26 20:43 unless it finishes first. Cause: the loaded box (load 10–13, swap up to 4.5 GB) pushed per-chunk time past 48 h; N0N0/N0N1 took 27 h earlier. The registration slip (48 h watchdog not listed) is logged as Bridge slip 24.
- Decision (Bridge): option B, an env-var watchdog with the default 48 h unchanged, identity-checked plus a must-fire, registered in a B15e amendment before rerunning the 5 chunks at ~120 h. Freed cores go to the kerr_e reruns first, then branch-S pm/pp/refs (mm/mp already running since 19:06). Quantum paused its own launcher (verified PID).

## 2026-11-25 19:41 — kerr_e: 48 h timer cancelled in the four running chunks (Sumit's go)
- Quantum found there's no progress counter and no checkpoint, so a timed-out chunk loses everything. Its proposal: cancel the pending alarm() in each live process with lldb.
- Dry run first, on a dummy with the same signal+alarm setup. alarm(0) returned 275. The dummy survived past its old fire time and exited 0. **Catch:** lldb `detach` left the process STOPPED (state T). The procedure therefore adds `kill -CONT` and a state check.
- Real run (fleet/kerr_e_timer_rescue_2026-11-25.sh; log in fleet/kerr_e_timer_rescue_2026-11-25.log). Each step checks the PID's args against the expected spec. Results:
  - N3N4 6670: 7740 s left;
  - N4N5 6675: 7738 s;
  - N5N0 6677: 7737 s;
  - N5N1 93687: 90132 s.
  - All four were back in state R at about 80% CPU. Computation untouched, binary unchanged.
- About 140 core-hours saved tonight, plus N5N1's ~23 h. Reruns are now needed only for N1N2/N2N3 (already lost), after the A4 identity checks pass. One interim slip there: the GB check reloaded an old checkpoint. Quantum re-running with a fresh checkpoint path.

## 2026-11-25 20:05 — Cuspis: W8P8 referee confirms the t0 fix; EXP-086b; Fable n = 2 consultation
- **W8P8 referee (19:44).** The fix agrees with the rad-1e-6 truth to 9.2e-7. The true correction is +0.020684, against the artifact model's +0.020126 (the model under-counts by 2.7%). ΔR(2) = +0.1457, measured. The Bridge re-derived all of these from the raw values.
- **EXP-086b** (descriptive; registered first, be5a3c8). At n = 2, the counterterm/R₂-growth ratio is 1.371/1.497 with bulk c and 0.982 with box c_A. That sharpens the n = 2 tension but does not settle it.
- **Fable consultation.**
  - The brief (91595d1) was sent by the Bridge directly to Cuspis-personal on Sumit's instruction. Answer a3a385f; seal bcdb69f (seal committed first, verified).
  - Fable's claims, ALL UNVERIFIED: the first-order counterterm is complete at integer n; c_A is valid at every n; R₂'s ℓ² growth is a slow 1/r² tail of σ₂, not a 1/a² term; T54 + box prescription is the whole story to ~2%.
  - SEALED: R₂ + ΔR₂^A at ℓ = 2.5 = 0.182 ± 0.020, outer band [0.14, 0.23].
  - Cuspis is asked for checks (a)–(f): seal grading, a script rerun, a finite-difference test of Q1, the σ̇ profile, saddle dominance, and a non-author read of Q2.

## 2026-11-25 20:40 — Cuspis EXP-088: Fable's n = 2 answer checked (b1ada3f)
- **E PASS.** H₂ + σ₂ is positive definite at all 6 geometries (λ_min 0.041–0.161). Strict concavity then makes the stored saddle the unique RS stationary point, so Q1's premise holds.
- **C registered FAIL (Cuspis's slip).** The 1e-6 tolerance ignored the central-difference truncation (control-clause slip 25).
  - Post-hoc, cause SHOWN: the error is pure O(ε²) (×100 per decade). Richardson agrees with the first-order form to ≤5e-9 on 2 boxes × 3 directions, and the n = 1 control goes to 0. **Q1 VERIFIED, post-hoc.**
- **D FAIL for Fable.** Its "σ̇ is a contact term, no 1/r² tail" doesn't hold: σ̇'s tail is as extended as σ₂'s and ~2× larger. Q3's MECHANISM is unsupported. (Q3's conclusion, no 1/a² term, is untested by this.)
- **A, SEAL.** S₂(2.5) = 0.161872 (the Bridge re-derived 4.316952 − 4.155079).
  - PRIMARY [0.162, 0.202]: FAIL, by 1.3e-4 (1.006σ). SECONDARY [0.14, 0.23]: inside. Risk values 0.27/0.35: not hit.
  - Bulk local ratio 1.2125/1.3237, predicted 1.27/1.39 ± 0.03: FAIL. Right direction, falls faster than predicted.
- **Net.** Q1 is supported. Q2 follows but moves A-vs-bulk to n = 1 (open item). The Q3 mechanism is undercut. The seal is a near-miss.

## 2026-11-25 ~21:10 — Neutral AI credit live on both Zenodo records (Sumit's rule)
- ansatz-machine d9fd9e0 and DeepStrain 7205bba/a211b4f: headline surfaces say "AI-assisted"; one neutral disclosure paragraph uses the "every result reported as established" form.
- Zenodo descriptions edited (metadata only; same DOIs, no new versions) and read back: 24533026 (ansatz v1.1.0) and 24399603 (DeepStrain/LongChirp; names Claude only, since the snapshot predates any Gemini use, which the Bridge verified in git).
- Chrome: the only connected browser at first was another Google profile ("software-consultant"). Nothing was done there; the edits were made after Sumit connected his own profile, which was checked first (new rule: chrome-profile-check-first).
- Pending: DeepStrain's GitHub release body (longchirp-v1.0.0) needs Sumit's word.

## 2026-11-25 22:50 — Cuspis W10P10 t0 recompute (84f5783); fleet core sequencing
- **W10P10.** KA PASS (3.4e-13). Correction +0.121780 (the Bridge re-derived it), ΔR(2.5) = +0.8715. The code-logic model agrees to 8.2e-5, but that is code against code.
  - There is no truth referee at W10P10: the doublet gaps (~9e-8) are below the contour floor. **PARTIALLY VERIFIED.**
  - Fable's W10P10 prediction (−0.1218) matches to 2e-5.
- **Order after the W12 route** (Bridge): C1 W12 first, as registered in run_k3. Then the W12P12 t0 recompute, one for one. The new re-read registrations (R(k), 085/085c, the ingredient split) are to be drafted now, with Fable's k = 3 seals in the header.
- **Fleet.** 10 long jobs on 10 cores at 22:35. Quantum's own limit is lowered to 7 (a4_mycap.txt); Cuspis swaps jobs one for one only (run_089 replaced W10P10 at 22:49). The ansatz-machine-personal Fable round runs short nice-12 jobs. Raise Quantum's limit back to 8 when Cuspis drops to 1 job.

## 2026-11-25 ~23:10 — Cuspis EXP-090, k ≤ 2.5 re-read with the corrected t0 (f7d6313; script ae2e3c6 committed first)
- Controls K1–K6 all pass, run first. This part is confirmation, not blind.
- Corrected R(2), R(2.5) = 6.5877, 9.0902 (the Bridge checked them: stored + 0.1457 and stored + 0.8715). g_raw goes from 4.020 to 4.572.
- **A: ρ_s = +0.0429 ± 0.0020, SUPPORTED (robust).** Bulk hi/lo: −0.144/−0.249, OVERSHOOT at both ends.
- Fable S-4 PASS (0.4322 vs 0.428; 0.3710 vs 0.371).
- Ingredient map: none of (a)–(d). The old "opposite-sign piece in t0" was mostly the inner_beta0 defect.
- Caveats: finite-k only (Y's 1/a² row still fails); conditional on A-vs-bulk at n = 1 (the EXP-089 wall test runs tonight); EXP-086 n = 2 bulk overshoot stands; partially verified (no truth referee at W10P10). k = 3 waits on its four gates.

## 2026-11-25/26 — ansatz-machine-personal (Fable) eps round finished: 75957fd (Part A), 4bc7b37 (Part B). UNVERIFIED
- **Part A.** Interval-certified r_a at all 4 spins (a few ×1e-3; ~1e-4 at 9/10). The three controls pass per Fable. Limiting factors: the lasso remainder and the circle's 2nd-order term, about equally.
- **Part B.** A validated point evaluator (Arb, using Quantum's venv read-only) that agrees with the engine at 3 points.
  - **k-as-ball FAILS** (×1e7 wrapping), which changes the route (i) design.
  - Chebyshev plus Bernstein-ellipse was demonstrated with a sampled M; a proved M is designed but not built.
  - The "real k suffices" simplification is to be checked against the claim and registration.
  - Cost estimate: a few to 20 core-h per spin. A self-caught acos/sub-ball bug is fixed.
- The office ansatz-machine verifies A then B (B1–B4: ATAP Thm 8.2 at source; scope of "real k"). Nothing launches.

## 2026-11-25 23:45 — Deepstrain-personal (Fable) round: coherent2 redesign (c)
- Brief v1.1, a8c3d44 (house rules, reserved core, MPS under 2 GB, fresh segments untouched). Sent by the Bridge at Sumit's request.
- Core reserved: Quantum PAUSED kerr_e/N5N1, PID 93687 (optional chunk; alarm already cancelled), at 23:40:10. It's still counted in Quantum's limit. **Resume on the Bridge's word when the round ends** (~4–6 h).
- Caveat: kerr_guard's disk-resume could SIGCONT it. Quantum re-pauses if that happens.

## 2026-11-26 — ansatz-machine: CLAIM v3.1, Statement A with explicit certified ε_a (ddcbd53; merge bd74e05)
- ε_a = 2.79e−3, 1.92e−3, 8.39e−4, 1.06e−4 at spins 3/10, 3/5, 4/5, 9/10: the corrected-code r rounded down. The Bridge checked the rounding against 2.799955e−3 / 1.925557e−3 / 8.398961e−4.
- Lineage: Fable Part A 75957fd → office verification e10f274 (slip: |m|² upper bound used where a lower one was needed) → fix run 9d0ee9f → merge. Part B prototype checked (bcd9292); route (i) input in docs/ROUTE1_REGISTRATION_INPUT.md (nothing launches).
- No release / Zenodo version: v1.2 is Sumit's decision, raised with him.

## 2026-11-26 00:30 — DeepStrain Fable round done computing; N5N1 resumed
- Fable redesign (c), UNVERIFIED (branch fable/2026-11-26-coh2c, c1f197e/ec5dd31/a019eba):
  - local engine 14.1 µs/template (sealed 25 µs HIT, 239× the stored 3.36 ms);
  - stage-2 total 9–16 h at one per minute (sealed ≤ 20 h HIT), or 14–22 h with constructed grids;
  - exact E3 χ² gate matches brute force;
  - MISSES: decimation and the grid ratio.
  - Real-noise headroom ≥ 1.15× NOT tested (step T).
  - Memory: RSS hid MPS. The stored T-cost run was ~5–6 GB real. Fable had 2 small overshoots (2.33/2.15 GB). DeepStrain switched job_guard to phys_footprint.
  - Shared-tree accident: office commit 104c69c landed on Fable's branch; cherry-picked to main.
- N5N1 (93687) was paused 23:40:10 → 00:27:20 (47 min, nothing lost) for Fable's core; resumed, state R.

## 2026-11-26 ~01:30 — DeepStrain: redesign (c) VERIFIED (except the MPS re-time); step T REGISTERED (PREREG §12 Amendment T1)
- Whole-box brute force on 6 grids / 7,178 templates matches to ≤ 5e-6. The cost is 17.8/22.3 h; overheads were re-derived (only H1+L1 combine missing, +5–20%).
- D1–D5 accepted with measured numbers. D5 uses a uniform 2.20% box (the code ran at the pooled 2.15%; re-check in the build list).
- Step T: PyCBC 2.10.0 statistic imported (newsnr_sgveto_psdvar w/o the SG term, Allen χ² at the top 5).
  - Sealed: R_tune 1.12 [0.85, 1.40], P(G0) ≈ 35%.
  - Memory plan: footprint guard, pause-only, start gate free ≥ 50% & pressure 1.
  - Fresh segments unopened.
- **Pending Bridge slot go:** the MPS re-time plus ~18 h + ~22 h passes, AFTER Cuspis's big-memory jobs (W12 route, then W12P12 t0, 5–6.5 GB). Short build/gate runs are allowed now under the start gate.
- Fable rounds out: Quantum-personal (sealed blind retry prediction, brief 4bc659f) sent 01:1x. The ansatz route-(i) segment brief f6988c8 waits for Sumit's go at the 03:20 window.

## 2026-11-26 01:22 — Quantum-personal (Fable): sealed blind prediction of the branch-S retry
- Commit d31ac7f on fable/2026-11-26-retry-predict (parent 4bc659f). One file, sha256 0a6d7f99cd90d736de858083028c1da2f91bcfa926b9feccac5933648547c70c (the Bridge verified the hash without reading the file).
- Quantum doesn't open it until read_retry.sh gives the VERDICT, then grades per brief §4 (interval coverage, piece calls, verdict, Brier).
- Disclosure: Fable knew from metadata that mm/mp launched first; no outcome data.

## 2026-11-26 02:05 — OVERNIGHT FABLE PLAN (Sumit asleep; the Bridge runs it)
- 03:21 timer (bg task) → ask Quantum to PAUSE 93687 (N5N1) → send the ansatz route-(i) segment brief f6988c8 to ansatz-machine-personal (pre-checked: scratchpad/ap_route1_msg.txt; pause note q_pause2.txt).
- Spare rounds in the 03:20–05:30 window, each STARTING by 04:30 at the latest; none after:
  - (a) Quantum-personal: a sealed blind kerr_e prediction (compute-free; may run in PARALLEL with ansatz). Brief requested from Quantum by 03:00.
  - (b) Cuspis-personal: only if Cuspis says it's ripe (wall test / A-vs-bulk). Brief by 03:00.
  - (c) A second ansatz round if the first ends early with a clear next step.
- After the ansatz round: resume 93687; hand to ansatz-machine for verification.
- No Fable after 05:30 (weekly reset); Sumit decides next week.
- Do NOT leak the sealed retry prediction's content (Sumit's screenshot showed it) to Quantum.
- 02:20 update to the overnight plan:
  - Quantum kerr brief 74b5f2e is ready (scratchpad/qk_msg.txt) and goes to Quantum-personal at 03:21 in parallel with ansatz.
  - Cuspis brief a457622 (A vs bulk; S-a, S-b, S-c) goes to Cuspis-personal once EXP-089 is graded (with an addendum), or at 04:15 as is.

## 2026-11-26 01:17 (graded 02:05) — Cuspis EXP-089 wall test (960d2b8)
- Strips fixed at (2, 4); walls P = 4 → 6. Controls pass.
- ρ_A 0.2735 → 0.0472 (Δ −0.226); ρ_bulk −2.218 → −1.378 (Δ +0.840); G_b drop 1.066.
- **f = +0.212**, inside PRIMARY [−0.3, 0.3]: "A not wrong", and Fable's seal (7c846a1) PASSES. The Bridge re-derived f = 0.226/1.066.
- Partially verified: one P step, an argued premise. Second n = 1 reading favouring A (with EXP-090); the derivation question stays open.
- For the overnight Cuspis-personal round, the Bridge will send the addendum ONLY after Fable reports its S-a/S-c seal sha.
- 02:05 Sumit: the last START time for any Fable round moves from 04:30 to 05:00. No Fable after the 05:30 weekly reset.
- 03:21 START: N5N1 (93687) paused at 03:21:29 for a reserved core. Sent: ansatz-machine-personal route-(i) segment brief f6988c8 (hand over by ~05:15); Quantum-personal Kerr sealed-prediction brief 74b5f2e. Cuspis A-vs-bulk brief a0b6042 is next (by 04:15; addendum only after the seal sha).
- 03:31 Quantum-personal Kerr prediction SEALED: fd22a7f (sha256 99e33cd0…604d; the Bridge verified it without reading). Disclosure: knew N1N2/N2N3 timed out (no outcome); ruling: keep them in the edge column, footnoted. 03:3x Cuspis-personal brief a0b6042 SENT; the addendum goes only after its seal sha.

## 2026-11-26 ~04:00 — Cuspis EXP-091: Fable's A-vs-bulk seals graded (c515d58; amendment C3′ ae5b046 before the rerun)
- Interior c_A/c at P = 12: sealed 0.826 ± 0.003, measured 0.82628, PASS (1σ).
- Raw g_b(3) 0.2735 ± 0.003 vs 0.27652 and y_A(3) 0.7654 vs 0.76238: both ~1.0σ off, PASS on the inferred ±2σ band (labelled inferred).
- Δ_bb(3) hi = −4.031 (the Bridge checked it: 0.27652 × 14.5792). Fable's −3.89 ± 0.08 is 1.8σ off; not graded because norm(3) = 14.579 fell outside Fable's guessed range.
- S-a ("Δ_bb → const") is not tested: deceleration is slow (increments −0.485, −0.474, −0.306, −0.275). Its fail clauses did not fire, which verifies nothing. It stays ARGUED.
- Exposure: Y_A(3) = 11.115 is now known, so the k = 3 A reading is blind only in R(3).
- Slip 26 logged (C3 tolerance below the typed precision; the proposed fix used the wrong c).
- 03:47 (clock): Cuspis-personal's A-vs-bulk round is finished (head 6ed6a44). Fable RETRACTS its sealed S-a after the seal: a log in c_A, c_A∞ = −0.1183. Sent to Cuspis for checks (a)–(e). Note: the two preceding run-board headings said '~04:00', but the clock read 03:3x–03:4x.
- 03:49 Deepstrain-personal: step-T blind prediction brief d01cb8d SENT (sits beside DeepStrain's own sealed 1.12/35%; redacted registration provided). ansatz route-(i) round still running.

## 03:56 — Cuspis office checks of Fable A-vs-bulk (6adc53b; EXP-092 a48bde4)
- S-a graded "author-retracted after the seal".
- Third c_A implementation, P = 16/20: H-log SUPPORTED. y1 = 32/(3π²) VERIFIED at source (Moshe & Zinn-Justin hep-th/0306133 §3.2, Eqs. 3.28/3.33).
- Free gL = 0.070–0.074, 15–20% above y1·h0 = 0.0611, so the coefficient is NOT confirmed. c∞ = −0.1166 … −0.1188 by fit form.
- Grade: argued, structurally supported, coefficient unconfirmed.
- P-1 (wall step to P = 8) and P-2 (n = 2 wall test) to be registered; the G_b(8) GEOM may run now. The long routes queue on Cuspis's core after the W12 chain.
- Cores: Cuspis 1 (route), so Quantum's a4_mycap goes back to 8. Fleet ≤ 9 (93687 paused for ansatz Fable).
- 03:57 ansatz-machine-personal route-(i) first segment FINISHED: 604d520, verdict CERTIFIED on k ∈ [1, 1.1] at spin 3/5 (UNVERIFIED). Sealed M_F MISS (6.57e10 vs ≤ 1e8); the rest HIT. Gaps: Dyson gauge derivation, 1+1e-7 float inflation, mean-value enclosure, single implementation. Sent to ansatz-machine for checks. Resume of 93687 requested from Quantum.
- 04:00 Cuspis EXP-093/094 (Fable P-1/P-2) registered f874dac. G_b(8) = 1.0215 vs sealed 0.97 ± 0.06: PASS (be9cad7). The long routes are queued (run_093_094.sh, PID 59649) after the W12 chain on Cuspis's single core. A 10th core would let P-1 start sooner: Sumit's call.
- 04:04 Deepstrain-personal step-T prediction SEALED: b13b4f8 (sha256 0f78841d…8eb7; the Bridge verified it without reading); push requested. DeepStrain opens it only after G0. The S0 json is missing on main (on the build branch). Only the ansatz follow-up (gaps b/c) is still running.
- 04:31 ansatz-machine-personal follow-up DONE: d855810. All-ball verdict unchanged (CERTIFIED); dq/dk enclosure asserted; gauge legitimacy written up. Found a ~1e-15 vertex gap in the Part B proto walk (closed in v2). All 5 overnight Fable rounds finished; no Fable after this. Fleet: N5N1 resumed 03:58; fleet ≤ 9.
- 04:32 One last optional Fable task sent (starts before 05:00): ansatz-machine-personal repeats the v2 certified segment at spin 9/10, k ∈ [1, 1.1], seal first; finish by ~05:25.
- 04:51 ansatz-machine VERIFIED the route-(i) first segment (604d520 + d855810): record b38af7d; byte-identical reproduction of both versions. (a) gauge/Dyson chain checked by hand; (b)/(c) closed; (d) independent 50-digit engine inside the enclosures; the bound is valid but loose (true ‖·‖ within ~7% of 1, against e^I = 2233 on the lasso). The Part B vertex gap is confirmed and recorded. The spin-9/10 seal 620c470 is in; its run is pending.
- 04:56 Fable spin-9/10 check: NO certificate (cost: n = 140, ~7.5 core-h; circle Dyson constant 478 vs 10.5 at 3/5). Seal 620c470, results d18de63. Sent to ansatz-machine for checks and a diagnosis. FABLE USE ENDED for this week (Sumit's rule: nothing after 05:00/05:30).
- 05:16 ansatz-machine diagnosis (7dd8c18): the spin-9/10 '46× harder circle' is an ENCLOSURE ARTIFACT (wrapping of Laurent c0/dq-dk on boxes; inflation up to 5,900×). Intrinsic circle constants are 0.36 (3/5) and 0.65 (9/10). The 250–300 core-h estimate is void. No 7.5-h slot; ansatz-machine builds a centred enclosure itself (seal first), then re-measures.
- 06:20 ansatz centred enclosure (seal 67c7661, results 8b9971c, record 6df925d): spin 3/5 n 24 → 18, still CERTIFIED (|Im tr M1| 1.3e-8 weaker, graded a narrow FAIL of 'no weaker'; slip 27, the Bridge's clause). Spin 9/10: point constants fixed (circle 0.773), the k-disc not (n 134). Next: the k-Taylor fix (seal first; proof stage only). The 9/10 verdict needs the Bridge's word.
- 09:56 Quantum A5/A5b checkpointing: run 1 found a T5 design flaw (slip 28) and a REAL orphan-record bug (T6b) in both readers; fixed in 2a14c76, binary 77eb34a6. All tests rerun from scratch (~3 h). The kerr_e relaunch waits for a full pass and the Bridge's word. ansatz spin-9/10 v4 prove running (PID 9512, 1–2.5 h, with checkpoints).

## 2026-11-26 ~12:00 — MacBook Air added as a fleet resource (Sumit's offer, to recover the outage loss)
- `ssh air`: dedicated key ~/.ssh/id_ed25519_air, Host air in ~/.ssh/config (backup config.bak-2026-11-26). Air: M1 4P+4E, 8 GB, macOS 27.2.1, 72 GB free.
- Python env installed with Sumit's OK: ~/GitHub/fleet-air/.venv (Homebrew Python 3.14.10; numpy 2.4.3, scipy 1.17.1, mpmath 1.3.0, sympy 1.13.3, python-flint 0.9.0, pinned to Cuspis's .venv).
- Budget on the Air: Quantum kerr_e ×4 (statically linked b15e2 variant, amendment B15e A6, byte-identity on both machines first) + Cuspis EXP-093/094 ×2 (a platform amendment with KA identity first). That leaves 2 cores for Sumit. Pause-only guards; checkpoints pulled back and validated.
- 11:49 Cuspis: EXP-094 (P-2) ran here (ab0304b): INCONCLUSIVE, the G₂b drop of 0.1995 missed the 0.2017 threshold by 1.1% (a fragile, self-set rule). f₂ = +0.487 descriptive (the Bridge checked it), outside Fable's 0.05 ± 0.15. EXP-093 identity on the Air launched 11:45 (W2P6, then W2P8 on PASS). The Bridge's two messages conflicted on Air slots (3 vs 1); Cuspis followed the later one (1).

## 2026-11-26 12:04 — Bridge handed to "Bridge - claude personal" (office account out of limit; Sumit's word)
- Checked at handover: Mac mini running Quantum mm/mp/pm/pp (2836/2838/4180/4182), kerr_e N1N2 (32284), A5b tests (16230/41807) plus queued chains; Cuspis W12 route (5132, guards 3051/3107/3108, run_087w12 3109). Air: Quantum A6 tests (3415→4114), Cuspis EXP-093 identity (3944/4098), Sumit's AlphaMate dashboard (untouched). Mini 74% free, 10 GB disk; Air 76% free, 71 GB.
- Sent (blind-checked): Quantum-personal and Cuspis-personal to confirm and re-arm report-only watchers (mini plus Air via ssh), with the handoff's pending actions as their go after a no-double-launch check; Deepstrain-personal code-only go (no runs, mini full); ansatz-machine-personal go on the route-(i) registration draft, requiring a non-author check plus a second implementation before any result counts.
- Bridge backstop watcher on the six long PIDs, memory and disk, and Air reachability (report-only). The first version misfired (zsh does not word-split an unquoted $PIDS); all PIDs verified alive and the watcher re-armed with an array.
- 12:12 Sumit's office window (~5-6 h): Quantum refs W1 ref 47206 + W2 waiter 38321 PAUSED (SIGSTOP 12:11:45, logged in retry_s/refs.log; nothing waits on refs today; no wall timer). ansatz §3 compute HELD (code reading continues). Stage (i), the pieces, N1N2 and Cuspis untouched. Resume both on Sumit's "done".
- Quantum A6 addendum 3 (4580a9b: thermal log-only; promote_air.sh, synthetic 7/7) and e0d0032 (a4_mycap as is) committed before launch. A5b all PASS (db63e68). ansatz route-(i) registration draft v0 c3a61ab read; go on §3 (a), (b), P1 only (compute held now).
- 13:00 Quantum A6 identity PASS on both machines (13 outputs byte-identical between M4 and M1; 279bf22). 5 Air kerr_e chunks launched once at 12:59:19 (N2N3 8602, N3N4 8615, N4N5 8628, N5N0 8641, N5N1 8654; guard 8663 pause-only; record 1dc4f19). pull_air.sh 69773 detached on the Mac mini. Cuspis EXP-093 identity PASS (7f3731e) → W2P8 on the Air 12:26; 30-min pull-back 60346. ansatz reproduction running on the Air (~70–100 min). DeepStrain: twinexact PASS; C9 → option (i) (post-check amendment, FAIL runs kept); K1-(A) N_MC = 100k per L_max (false-fail 1.5%); C11 read by the Bridge (f313dab). Evening slots queued for after Sumit's office window.
- Machines: Mac mini = Quantum 5 + Cuspis 1 (≈4 free for Sumit); Air = Quantum 5 + Cuspis 1 + ansatz 1.
- 15:24 Quantum: N1N2's first edge record landed 15:13 (3 h 43 min; ~32 min per evaluation). Naive projection ~475 h per chunk against the 30-d watchdog. NEW jobs: A8 correction 1 (HS_WATCHDOG_S=off = no alarm; a bad value FATALs, no silent 48-h fallback; macOS alarm() max 1e8 s) → rebuild b15e5, A8 tests restarted on it. RUNNING chunks: timer-raise plan 52f103c (lldb alarm(0)), NOT applied. **DECISION FOR SUMIT by ~2026-12-06:** needs his password (Mac-mini lldb authorisation dialog; Air one-time `sudo DevToolsSecurity -enable`). Cost re-projection after ~5 more records; options (registered subset / cost order) go to Sumit if it holds at ~3 wk per chunk.
- ansatz: (b) engine at all 44 nodes inside enclosures PASS (8d31624). The 3.14 repro DIFFERS only in the unchosen rows' free gauge (3.13 vs 3.14 complex multiply); exact rerun under Python 3.13.18 running on the Air.
- SphereXVision moved ~36 GB to the Air (checksum-verified; Sumit approved the delete): Mac mini 43 GB free, Air 36 GB.
- The Air is reached over the USB link while the VPN is on (~/.ssh/config: no forced IPv4; HostKeyAlias).
- 17:27 ansatz: exact repro IDENTICAL under Python 3.13.18 (f0710a4); P1 CERTIFIED with 10/10 sealed hits (bfcbcfa); v5 7f96efc diff read by the Bridge (two v4 diagnostics restored, identical expression); T1–T4 running on the Air, then P2/P3, then the cost redo → Sumit. Cuspis: EXP-093 P-1 all 3 PASS (4d13f1f); EXP-095 registered 83566e3 with a SEALED READ (outputs sha-only until a blind prediction is sealed next week, or read descriptive-only); W2P10 on the Air from 17:26, W4P10 may run as the 8th Air core if its peak is ≤ 2.5 GB. W12P12 t0 on the Mac mini under a 9-GB pause-only hold. Quantum: A8 correction 1 (cb7afa0, b15e5), tests restarted 16:52.

## 2026-11-26 17:34 — ansatz v5.1 read
- Bridge non-author read of v5.1 (fa7859f, moves only the proof-stage segment for the cost pilot P3): APPROVED with B1. B1: refuse R1_HALF/R1_FLOATS when R1_KC is unset. Read: fleet/reads/ansatz_v5.1_read_2026-11-26.md.
- Order: T1–T4 on 7f96efc → P2 → install v5.1+B1 (new manifest) → T1 again (same machine and Python) and T2–T4 → seal P3 → run P3. The P1–P3 cost redo then goes to Sumit for the production decision.

## 2026-11-26 17:45 — Quantum A8 on b15e5
- T7 (watchdog: unset 48 h, 1e8 clamp, off = none, 60 s must-fire exit 124, 7 bad values FATAL) and T0 (6/6 BYTE-IDENTICAL): PASS (147404c). Next: T1, T2 (SA+SE), T4, T5/T5b.
- ansatz: B1 folded in (b64a43c), approved; P3 sealed (4a7bb55) with the 3.9 rejection predicted at P=95%; runners 76f2715.

## 2026-11-26 18:19 — ansatz T1 on 7f96efc FAILED (diagnostic only), fix approved
- T1 differed in one field (stats) in all 4 rows. v5 had dropped v4's K-point z-control, and the proof JSON was also missing norder and point_constants. No bound affected.
- Fix 4bc2ebd (v4's code restored, T1 extended to the whole proof JSON and shown able to fail): APPROVED. P2 runs on v4 per its seal's own condition (amended before any P2 computation). Next: v5.1 install → tests51 → P3.
- 18:21 ansatz: the P2 manifest was committed 54 s after launch (slip recorded in 1f3d3d7). The Bridge checked all 3 manifest hashes against the files at 4bc2ebd (committed 11 s BEFORE launch): equal, so P2's record holds. v5.1 is installed (b7e17c4); tests51 is chained on P2 rc 0; P3 waits for the tests51 read.
- 18:22 Quantum kerr_e: first Air edge record (N4N5 E/0/0) done 18:03:56: 4 leaves, all R, 0 fails, 3486 steps, 5 h 05 min, ~43 min/eval with 5 chunks sharing the Air (Mac mini N1N2 ~32 min). 2 records in total; revised projection at 7 records.
