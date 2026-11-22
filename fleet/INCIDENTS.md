# Fleet incidents (shared-Mac operations)

## 2026-10-11 05:57: the bridge killed two of quantum's pool workers
**Cause.** The bridge ran `pkill -f "multiprocessing.spawn"` to clean up its own failed spawn-test workers. The
pattern also matched quantum's plan-A V23 Pool workers (PIDs 28384, 28385; parent `chl_planA_V23.py`, running 8 h).

**Effect.**
- V23 hung: the respawned workers sat idle and imap never returned the lost tasks.
- The 2 in-flight jobs were lost: the last two V3 nodes (t = 1.37, q = 32.9, sets B and C), about 2 h each.
- 96/98 results were safe in V23's checkpoint.

**Cost.** About 4 core-hours, plus about 2 h of wall-clock delay to plan A. No result was permanently lost.

**Recovery.** Quantum killed its own V23 by explicit PID and relaunched it from the checkpoint, rerunning only the 2
lost jobs. The Lean batch was unaffected (fork-mode workers).

**Rule adopted.** Kill only explicit PIDs verified as your own (parent chain or cwd). Never kill by pattern on the
shared box.

## 2026-10-11: a system numerical-library defect (under responsible disclosure)
Tabula root-caused its §195 crash series to a defect in a vendor numerical library. It has been reported to the vendor
through its security channel by the user.

Details are withheld from all public repos until the vendor resolves the issue or states it is not a security issue,
per the user's direction. They are kept in local, uncommitted notes.
- Fleet impact: each sister audited its own code locally. The bridge's paper code, ansatz, deepstrain and quantum are
  unaffected. Tabula moved to an alternative library build.
- Results are not affected.

## 2026-11-19 09:55 — the Bridge's own V22 check pushed swap to 3.5 GB and stopped ansatz's v3 run
- **Cause:** V22's float monodromy code called scipy solve_ivp without t_eval=[], so it stored every accepted step. The same leak Quantum found and fixed on 11-18 (02391fb). It ran 1 h 50 min and reached 13 GB compressed.
- **Effect:** ansatz's v3 window guard fired correctly (swap > 2 GB with pressure 2, sustained 1,035 s) and stopped it at 09:55. Checkpoint 793a4c9; nothing lost.
- **Fix:** Bridge stopped PID 30460 (verified own) at 09:57. Swap fell and pressure returned to 1. t_eval=[] added to v22.py. V22 reruns only under a footprint cap.
- **Lesson:** the Bridge ran a job without its own footprint guard while asking every sister to have one. From now on every Bridge compute job runs under a footprint cap (ulimit or a watcher), the same rule as the sisters'.

## 2026-11-20 — Bridge: footprint_watch.sh guarded the wrong process (no harm)
- **What.** Jobs launched as `timeout … python …` were watched by PID of the `timeout` wrapper (~1 MB), not the
  python child. So the memory cap was silently inactive for those runs (V24 C1/C1′ diagnostics, ~130 MB, harmless).
- **Fix.** tools/footprint_watch.sh now sums memory over the PID and all its descendants, and TERMs the whole tree.
  It was re-attached to the running job; committed 0f9809a.
- **Lesson.** A guard must be tested against the actual process tree it protects. Check `pgrep -P` once after
  attaching.

## 2026-11-21 ~17:5x: Cuspis P1 pre-check memory overrun (contained)
- **What:** the P1 pre-check went to 3.3 GB RSS + 1.1 GB compressed (4.4 GB) against a declared ≤ 2 GB peak. Its own watchdog (2 GB cap) killed it within ~18 s. System free memory afterwards was 53%.
- **Cause:** the memory model missed the FFT-convolution copies (stacked arrays, FFT/IFFT outputs, Python lists of full matrices) at W = 6.
- **Effect on others:** none. Quantum's A3 (PID 40882) is alive. tabula's §213 first launch did crash at about the same time, but from its OWN KeyError (amendment-1 control print vs control dict; peak 362 MB); its guard log shows free memory at 67–68% throughout. Fixed in 22fd2b7 and relaunched at 17:58, before any result was printed.
- **Fix:** preallocated arrays plus a row-blocked FFT convolution; the peak is to be MEASURED on a short dry run under a 1.5 GB cap before anything is declared.
- **Lesson:** declare peaks from a measured dry run, not from a model. A watchdog set at the declared peak is what made this harmless.
- **Disk (checked 17:59):** 11 GB free on /. Quantum's A3 has a < 5 GB disk stop; its lines are expected to write < 2 GB in total. Candidate for freeing space, with Sumit's OK only: quantum b15_g6.json (931 MB, old, gitignored).

## 2026-11-21 evening: Cuspis's third memory overshoot (contained)
- The P1 σ probe at W = 2, r = 6, N_y = 96 reached 2.74 GB, and the watchdog killed it at its 2.2 GB cap. The earlier
  "~1.8 GB at r = 6" declaration was not computed from the measured scaling.
- Fix: every declaration now comes from the MEASURED law, ≈ 0.89 GB × (N_y/16) × (N₂D/720)², then a 1-minute measured
  dry run. Declared now: W = 2, r = 6 ≈ 2.0 GB and W = 3, r = 4 ≈ 2.1 GB, staggered.
- Pattern: this is the third overshoot from modelled rather than measured peaks today. The watchdog at the cap made
  each one harmless.

## 2026-11-21 ~21:3x: Cuspis EXP-081b, P = 12 worker over its memory envelope (contained)
- The watchdog stopped W2 P12 at 2.25 GB tree footprint (1.90 resident + 0.35 compressed) against the 2.2 GB cap; the
  registered estimate was ~1.4 GB. No R value was computed or seen. It resumes from the worker checkpoint (48 of 53
  nodes done) with the cap raised to 3.2 GB; the box was ~62% free. The killed run is kept on record.
- Pattern: the FOURTH modelled-vs-measured memory miss on this line today. Compressed memory grows over long runs, so a
  short dry run under-reads the peak. Lesson: dry runs must last long enough to reach steady compressed growth, or the
  declared peak should carry a ×1.5 margin.
- **06:35:** ansatz's Prop. 2 control script ran away to 10 GB with no RSS guard and caused pressure kills in two other sisters' runs. The Bridge's request didn't specify a memory bound; it should have.
