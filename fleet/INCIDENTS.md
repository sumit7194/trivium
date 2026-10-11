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
