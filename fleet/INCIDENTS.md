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

## 2026-10-11: Apple Accelerate dgeqrf heap overrun (root-caused by tabula, commit 59812ec)
**What.** Accelerate's LAPACK dgeqrf (QR) writes past the end of a heap block it allocates internally, for near-square
matrices of about 550–800 × 550–629.
- Minimal repro: `np.linalg.qr(rng.standard_normal((629, 629)), mode='r')` under Guard Malloc.
- Clean at n ≤ 500, at m ≥ 900, and on OpenBLAS.

**Effect.** Silent heap corruption. It usually lands in slack, so the failure is intermittent: about 1/4 of tabula's
§195 runs crashed, typically later in the GC.

**Fleet exposure.** Every Mac env here links Accelerate for numpy and scipy (3.12, 3.13, 3.14). Indirect users of
dgeqrf include lstsq (gelsd) and SVD on tall matrices.
- tabula: remedy is the OpenBLAS env (.venv314ob), validated under Guard Malloc; earlier Accelerate results are
  flagged for rerun.
- ansatz, quantum and deepstrain have been alerted to audit.
- Bridge paper code (V8–V12) is not exposed; older bridge legs are queued for audit (spawned task).

**Upstream.** A draft report (Apple Feedback, and possibly numpy) is pending; the user decides whether to send.
- **Correction (deepstrain, 2026-10-11):** Mac torch is NOT a safe workaround. torch 2.12.0 reports BLAS_INFO=accelerate
  and LAPACK_INFO=accelerate, so torch.linalg on Mac CPU also uses Accelerate. Clean alternatives are an OpenBLAS numpy
  env, Linux, or the phone (OpenBLAS + ACL).
- **Audit results:** ansatz CLEAN (no LAPACK in any verdict path); deepstrain CLEAN (all QR/lstsq ≤ 29 columns; commit
  9262e51); bridge paper code CLEAN. Quantum: pending. Tabula: remedied via OpenBLAS.
