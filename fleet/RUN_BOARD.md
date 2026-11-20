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
