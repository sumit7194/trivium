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
