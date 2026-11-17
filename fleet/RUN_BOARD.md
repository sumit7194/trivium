# Fleet run board (resource ledger)

The bridge allocates compute slots. Status only, never results. Update this on every launch and finish.

**Box:** 10 cores, 16 GB, disk ~8.2 GB free (2026-11-17). The fleet cap is 8 cores. The other 2 are for the system
and Sumit's SPHEREx detector session, which has priority. New disk is limited to 1 GB per job, with a stop-at-5-GB-free guard.
Large downloads wait for a disk cleanup.

## 2026-11-17: Sumit's go on all proposed items (macOS 27.2 regression: bridge, tabula, ansatz and Cuspis identical; DeepStrain and Quantum pending)

| Sister | Item | Slot | State |
|---|---|---|---|
| ansatz | True-fractal test (TS capture edge), after its preregistration | 2 cores, <1 GB, ~8 h | cleared, not launched |
| ansatz | Write-up of §150–§152; rank-3/4 design | none / slot request later | go |
| tabula | Tangle-seeded chaos check, after its preregistration | 2 cores, <2 GB, ~3 h | cleared (sent 2026-11-17 after its restart) |
| tabula | p = 4/5 high-precision probe (30 min), then full run by request | 1 core | queued |
| quantum | Regression, then wrapping test | 3 cores, ~1.5 GB | cleared after regression |
| quantum | G3 reference worker (~4 GB each) | 1 worker later | queued until the box is lighter |
| deepstrain | Regression; METRICS errata (bridge verifies independently); sGB note; time-slide literature check | 1 core, light | go |
| deepstrain | Benchmark build + 6–8 GB download | needs disk | WAITS for cleanup |
| cuspis | Upper-bound literature sweep; lower-bound firming | no compute | go |
| spherex | Planetes fake-mover run (Sumit's, priority): 1 Python worker + local helper | 1–2 cores, <1 GB, ~170 MB disk total | running until ~23:15, then ~30 min of scoring on 1 core |

Committed in core use when everything cleared is running: 2 + 2 + 3 + ~1 = 8.
