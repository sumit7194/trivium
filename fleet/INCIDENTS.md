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
