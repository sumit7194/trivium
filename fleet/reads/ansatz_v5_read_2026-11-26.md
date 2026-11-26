# Non-author read: ansatz route-(i) v5 (43a2de1, scripts/_nve_route1_segment_v5.py). Bridge, 2026-11-26

**Reader:** the Bridge (Claude Opus, personal account). Not an author of v2, v3, v4 or v5. **Verdict: APPROVED for tests T1–T4,
with one addition (A1 below).** No compute was run for this read.

## What was checked
1. **The mathematics is untouched.** v5 is a wrapper: it imports proto, v2, v3 and v4 and patches functions at module
   level. `git diff c2dd39c 43a2de1` over the four imported files is EMPTY, so v4's mathematics is byte-for-byte the
   reviewed code.
2. **F1, the branch assert.**
   - `one_minus_kphi` uses φ = (21u² − 18u + 1)/(10(3u − 1)²) with u = z²/A², identical to proto line 123. It is also
     algebraically equal to the ω-form at line 55 (x = a²ω² = 1/u).
   - `assert v.real > 0` on an arb is true only when certified.
   - The patch reaches every expansion point:
     - v2's `safe_step` looks up the global `step` at call time (line 833), and it is the only caller (line 279);
     - v4's `series_from_init` is called by bare name (line 192).
   - AssertionError is not swallowed: v2 catches only RuntimeError (line 834); v4 catches ValueError/ZeroDivisionError
     (line 136) and RuntimeError (line 182).
3. **F2, the code hash.**
   - It covers proto, v2, v3, v4 and v5. The read checked the local-import closure: none of them imports any other
     project module, so the hash covers all project code that runs.
   - It is used in every key and file name: the dq checkpoint via `ck_key`, rows, nodes, the proof JSON and the
     verdict.
   - A foreign record raises AssertionError, which stops the run and is never reused.
4. **F3, coverage.**
   - The verdict asserts steps > 0, bounds = steps, ksub = KSUB², and pairs = steps·KSUB² for each loop, from counts
     taken during proving.
   - A proof truncated mid-loop would fail these.
   - v2's `boxes == expected_boxes` now gets real numbers.
   - Limit: both sides come from the proof JSON, so F3 checks internal completeness, not a separate recount. That is
     adequate, because the JSON is written only at the end of `prove()`.

## Addition required before production (A1)
- The hash keys project code only. The arithmetic also depends on python-flint/Arb (and Python). With runs moving to
  the Air, a different library version could reuse a checkpoint written by another build.
- Required: put `python-flint` and the Python version in the key (or record them in every record and refuse
  mismatches).
- T1 (v5 reproduces v4's rows exactly) on the same machine remains the primary equivalence test.
