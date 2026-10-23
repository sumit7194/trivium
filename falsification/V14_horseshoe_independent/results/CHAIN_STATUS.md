# V14 chain status (Q2-U, then Q3-S)
- 2026-10-21 21:59:07 chain (re)started, pid 75014, git 5087ad1
- 2026-10-21 21:59:07 START U -> results/q2u.log
  julia pid 75020
- 2026-10-22 11:00:16 END U rc=0
    2026-10-21T22:16:07.087  DONE AZ: M0 => M0  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 0
    2026-10-21T22:52:10.766  DONE AZ: M0 => M1  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 2
    2026-10-22T08:48:50.336  DONE AZ: M1 => M2  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 68
    2026-10-22T09:09:03.233  DONE AZ: M2 => M3  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 2
    2026-10-22T10:45:19.261  DONE AZ: M3 => M4  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 23
    2026-10-22T10:55:32.936  DONE AZ: M4 => M0  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 0
    2026-10-22T10:59:02.322  DONE AZ: M4 => M1  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 0
    2026-10-22T10:59:46.648  DONE W1: M2 => M3  REJECTED  (certified failure of (b) (both orientations refuted))  fallback images 1
    2026-10-22T10:59:48.666  DONE W2: M2 => M3  REJECTED  (certified failure of (b) (both orientations refuted))  fallback images 0
- 2026-10-22 11:00:16 START S -> results/q3s.log
  julia pid 78817
- 2026-10-22 18:38:53 END S rc=0
    2026-10-22T11:21:55.206  DONE S: N0 => N0  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 2
    2026-10-22T12:23:57.816  DONE S: N0 => N3  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 5
    2026-10-22T17:43:32.796  DONE S: N3 => N4  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 57
    2026-10-22T18:19:52.280  DONE S: N4 => N5  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 8
    2026-10-22T18:28:52.803  DONE S: N5 => N6  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 1
    2026-10-22T18:38:48.928  DONE S: N6 => N0  CERTIFIED  (B2 refinement: every leaf of (a) and (b) certified)  fallback images 1
    2026-10-22T18:38:48.944  DONE S: N6 => N3  REJECTED  (certified failure of (b) (both orientations refuted))  fallback images 0
- 2026-10-22 18:38:53 chain finished
