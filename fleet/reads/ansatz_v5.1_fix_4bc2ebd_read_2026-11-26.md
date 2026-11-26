# Bridge non-author read: ansatz v5.1 fix 4bc2ebd (after T1 on 7f96efc FAILED)

2026-11-26 · read of `git diff b64a43c 4bc2ebd -- scripts/_nve_route1_segment_v5.py scripts/_nve_route1_t1_compare.py`,
plus the P2 seal amendment. Compared against v4's prove at the same commit.

**Verdict: APPROVED. Go ahead with install → tests51 → P3. P2 on v4 is accepted.**

- The restored K-point z-control is line-for-line v4's: the same dq_list_v4(st, kc, arb(0), lau_c, laud_c), dyson_sum and gauge
  calls, the same pt tuple and the same log line. The only difference is the S4. prefix. It sits where v4 has it, after
  the reference walks and before the rows, so the cumulative STATS go through the same passes in the same order. F1's
  asserts also run on the control's steps, which changes only F1_COUNT, a v5-only field.
- norder=S4.NORD and point_constants use v4's own expression. Field order in the JSON does not matter, because T1 compares dicts.
- T1_MJSON: v5 may add only code/code_env/code_files (top level) and coverage/code/f1 (rows and chosen). env, version and
  every sec are dropped on both sides, and everything else must be equal. It was shown to fail on the 7f96efc outputs.
  That closes the gap that let the rows-only T1 miss norder and point_constants.
- What T1 did: it caught a real omission in a version described as "v4 + checks". That is the test working as designed.
  No bound, M, n, gauge or ratio value differed.
- P2 amendment: the seal had made running on v5 conditional on T1 passing, so moving P2 to v4 follows a branch the
  seal already set out. It is not a post-hoc change. Predictions are unchanged, and the F1 row is correctly marked
  not applicable. Record item: put P2's launch time, from its log, next to 4bc2ebd (18:17:15) and the manifest 68486b9 (18:18:20) in T_TESTS.md,
  so the record shows the amendment came before any P2 computation.
