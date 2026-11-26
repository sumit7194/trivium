# Bridge non-author read: ansatz route (i) v5.1 (fa7859f, branch personal/2026-11-26-route1-check)

2026-11-26 · read of `git diff 7f96efc fa7859f -- scripts/_nve_route1_segment_v5.py`, plus a check of every place in
v2–v4 that names the segment ([1, 1.1], "21/20", SEG, seg_centres, FLOATS).

**Verdict: APPROVED for the T1–T4 rerun and P3, with one fix (B1) before install.**

What was checked:
- R1_KC unset: SEG, seg_centres, floats file, floats key "21/20", BASE, checkpoint, rows, M and log names are all as in v5.
  The CODE hash changes (it covers the file), so v5.1 needs new T1–T4. ansatz already proposed that.
- R1_KC set: only the proof stage moves. v5's prove() reads V.seg_centres(1), V.SEG and KREF itself. v4's dq checkpoint key
  starts with V.SEG (v4 line 54), so moved-segment keys cannot match default keys, and the KTAG file names keep them apart.
  The v2/v3/v4 functions that still hard-code "21/20" (v2 prove/nodes, v3 prove, v4 prove) are not on the v5 prove path.
  verdict() refuses a moved segment. Its v2 nodes/verdict still state [1, 1.1], so that refusal is correct.
- Rationals are parsed exactly with fmpq, so decimals are refused by int(). The assert covers half > 0 and kc − half > 0.
  A missing floats key raises KeyError, which also refuses.
- LIMZ depends only on the spin, so P3 at large k_c may reject rows at the Laurent-ratio limit (the k_c = 3.9 crossing).
  That is a valid result about the top of region A, not a failure of v5.1.

B1 (fix before install, folded into the same v5.1 hash): fail closed when the segment variables are half-set.
If R1_KC is unset, assert that R1_HALF and R1_FLOATS are also unset. Today a typo such as R1_KCC=2 R1_HALF=1/20
silently proves the DEFAULT segment and resumes the default checkpoint and rows files under the same code hash.

Order approved as ansatz proposed:
1. Finish T1–T4 on 7f96efc.
2. Run P2.
3. Install v5.1 + B1 with a new manifest.
4. Rerun T1 (v5.1 default rows vs v4 rows, same machine AND same Python), then T2–T4.
5. Seal P3, then run it.
