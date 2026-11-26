# Bridge non-author read: ansatz route (i) v5.2 = v5.1 + C1 (fa2ba7a)

2026-11-26 · read of `git diff 4bc2ebd fa2ba7a -- scripts/_nve_route1_segment_v5.py`, row_for in full at fa2ba7a, and V.ser (v2:113).

**Verdict: APPROVED for T1–T5 on the Air (same machine and Python), with one small fix (B2) folded in before the manifest.**

- The Arb sizing of n is right. `nr = log(4·MF/((ρ−1)·TOL_F))/log ρ` in balls. `nr < NMAX+1` is True only when the whole ball is
  below 41, so a non-finite or straddling ball is rejected: fail closed. With nr < 41, the float path can't overflow
  (4·MF/((ρ−1)·TOL_F) < ρ^41 ≤ 6.5^41 ≈ 4e33).
- The second branch rejects n = 42 after parity (n_raw in (40, 41)). This changes behaviour against v5.1, which had no
  cap, but only for rows with n > 40, and it matches registration §5.4 (n > 40 → split). Admitted rows with n ≤ 40 are bit-identical. T1's
  default-segment rows have n ≤ 20, so T1 can't see the change; T5b/T5c cover it.
- Rejected rows: MF, I0 and I1 are serialised by V.ser = x.str(50), with no float. The message uses log10 in Arb (the smoke-test fix).
- **B2 (fold in before the manifest):** the rejected-row dict still computes `c0_per_k=float(I0 / R)` and
  `c1_per_k=float(I1 / R)`. python-flint's float(arb) raises OverflowError beyond the double range. In the P3 crash case,
  I0/R ≈ 1e8, so it's fine, but a worse blow-up of the dq sums would crash the fail-closed path again. Use a safe
  conversion there (e.g. None or the Arb string when |x| > 1e300 or the ball isn't finite). Admitted rows are
  untouched, so T1 is unaffected. Add T5d: a rejected row with a non-finite or > 1e308 I0 serialises.
- NMAX affects efficiency only. n steers the interpolation degree, and the error bound is recomputed in balls for the n used.
  The comment says so.

**Registration mismatch (TOL_F), not part of C1:** §5.3 says the error bound ≤ 1e-2·|F(k_c)| (relative); the code uses an
absolute TOL_F = 1e-3. This is about feasibility, not soundness: the verdict compares |F| against a ball error bound, so a
too-loose target makes certification FAIL, never pass wrongly. Near k ≈ 1 the absolute target is stricter
(1e-3 < 1e-2·0.27), so the certified segments b38af7d and c2dd39c are unaffected. In the dyadic small-k segments
(|F| 1e-7 to 1e-10) it would be useless. **Production follows §5.3 (relative):** implemented in the P4 build with its own
read and T-tests, as ansatz proposes.

Probe (a) result accepted (577bdcc): the derivative-bound stop for segment centres is in (3.7, 3.8), and it's spin-independent.
The cause is acb.sqrt's enclosure inflation (the ball for s reaches 0 though 1−kφ's ball contains neither 0 nor the cut). The misses are reported.
For C2: smaller arcs or a centred evaluation of φ; a branch-aware sqrt isn't needed below ~3.85.
