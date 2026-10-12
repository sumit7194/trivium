# V8 — Findings: quantum's Tomimatsu–Sato δ=2 obstruction, checked by a second session

*Run 2026-09-24. Pre-registration `9365bc4`; post-failure amendment V8′ `78f2646`. Non-blind (see the
pre-registration). The bridge imports nothing from quantum. The metric is ansatz's data.*

## Verdict

| Step | Result |
|---|---|
| V8 as registered | **REFUSED**: the ZV positive control failed, because a count-only route is underpowered on ZV. The TS rows were seen in the same pass (a procedural slip, disclosed) |
| **V8′ (post-failure), controls** | **all behave.** ZV δ=2 → OBSTRUCTION on all 3 rows. Kerr → no log point, so not obstructed, on all 3 rows. Two poisons (log point present, but case 1 true by construction) → NOT OBSTRUCTION, with P found at degrees 2 and 3 |
| **V8′, TS δ=2, 6 rows** | **OBSTRUCTION on every row: CONFIRMED** |
| V8a, vacuum and evenness | **PASS.** The metric is even in y. R_ab = 0 exactly at 3 fresh random rational points for each (p, q). A 3% bump of g_xx gives |R| ≈ 0.07–0.10, so the check can fire |

## What the bridge derived, with its own code (`code/v8_nve.py`)

**Set-up.** H = ½ g^{ab} p_a p_b with p_T = −E, p_φ = L and mass shell −μ². Γ is the equatorial solution y = 0,
p_y = 0. The normal variational equation in (δy, δp_y), with x as the independent variable, is put in normal form
z″ = r(x) z with r ∈ ℚ(x). The rows are (E, L, μ²) ∈ {(1,0,4), (1,0,9), (1,1,4)} at (p, q) = (3/5, 4/5) and
(4/5, 3/5), with σ = 1.

**Structure found on every TS row, identical to quantum's ξ₁ report:**
- **x = 0:** a double pole with b = 3/4. The exponents are −½ and 3/2, so N = 2. The bridge's own Frobenius
  recursion finds a nonzero logarithmic term. That makes it a **log point**.
- **The ring quartic:** 9x⁴ + 30x³ − 30x − 25 at p = 3/5, i.e. 25(p²x⁴ + 2px³ − 2px − 1), and
  16x⁴ + 40x³ − 40x − 25 at p = 4/5. A double pole with b = −3/16 at every root (checked exactly by polynomial
  remainder), so the exponents are ¼ and ¾.
- **A turning-point sextic:** the coefficients depend on the row. A double pole with b = −3/16, exponents ¼ and ¾.
- **Infinity:** r has order 4 there, so α∞ ∈ {0, 1}.

**Kovacic.**
- The log point puts a non-trivial unipotent into the local monodromy, which excludes cases 2 and 3.
- For case 1, the smallest possible Σα_c is −½ + 4·¼ + 6·¼ = 2, which is greater than the largest α∞ = 1. So no
  exponent choice gives d ∈ ℤ≥0. Case 1 fails **on the count alone**: zero candidates, and no polynomial solve is
  needed.
- That leaves case 4, so G = SL(2, ℂ) and G⁰ is not abelian: the Morales–Ramis obstruction.

**So the TS verdict rests on four things:** the NVE derivation, the exact local exponents, the log term at x = 0,
and a count. The ZV and Kerr controls validate the derivation pipeline and the log detection on known answers.
The poisons validate that the case-1 solver can return "P found", which matters for ZV but not for TS, whose
count admits no candidate at all.

## Instrument log

1. **Procedural slip.** The first script computed the control rows and the TS rows in one pass, so the TS output was
   seen before the (failed) control verdict was applied. Disclosed in the addendum. V8′ gates properly: controls
   first, then an exit if any fails.
2. **A solver bug that would have voided V8′.** The first V8′ run parsed each factor with a plain `Symbol('x')`
   instead of the NVE's real x. So every factor degree came out 0 and θ came out 0, and its "ZV OBSTRUCTION" was
   meaningless. It was caught because the candidate counts looked wrong: 16 candidates on a TS row whose count
   admits none. Fixed, with an assertion that the degrees sum correctly, and re-run. The results above are the
   re-run. **Without the poison controls, a solver that never finds P would have passed every other control.**
   So the poisons were added (post-hoc, labelled) and both behave.
3. Two trivial script errors (an import split and an int-vs-sympy zero). Fixed, with no effect on any verdict.

## Scope, which travels with the verdict

- Meromorphic first integrals only, in a complex neighbourhood of the equatorial Γ.
- Only at the six tested (p, q; E, L, μ²).
- On ansatz's supplied metric. Its vacuum property is now re-checked by the bridge at 3 fresh points per (p, q),
  still pointwise and not a symbolic proof.
- It says nothing about how much chaos there is, or about other particular solutions.
- It is AI checking AI: quantum and the bridge derived the same thing with separate code, non-blind. **No human has
  checked it.**
- Prior art is preliminary: the citers of the ZV proof (INSPIRE recid 1219938, 10 records, matching its
  citation count) and a TS title query show no Morales–Ramis proof for TS. A full sweep hasn't been done.

## Net

**Two independent derivations (quantum's tool and the bridge's V8′) agree that TS δ=2 is not meromorphically
integrable near its equatorial geodesics at the tested parameters.** Each one reached this after a post-failure
amendment. This agrees with ansatz's sealed expectation and with tabula's numerical rung, which found nothing up
to rank 4. It is a candidate result for an outside reader. A full prior-art sweep comes first.

## Open tension, recorded 2026-09-26 (post-hoc, not a verdict)

tabula's rank-6 run was **REFUSED in all four arms** under its gate R1, so it issues no verdict. But in the one arm
where TS was read (p = 4/5 shared arm, far field, even r6 d4), it saw **one TS direction at Kerr's
exact-conservation level** (2e-23 to 8e-26) on all three shells, 1e8× better than at rank 4. Two readings:
- (a) a far-field formal-series approximant, which would be consistent with the obstruction;
- (b) a genuine polynomial invariant of rank ≤ 6, which would be in tension with the Morales–Ramis obstruction at
  P2 = (4/5, 3/5).

Two caveats:
- Vollmer 2016's no-Killing-tensor theorem (valence ≤ 7) is at p = 3/5, **not** the p = 4/5 of this arm, so it does
  not settle (b) here.
- The Morales–Ramis result covers meromorphic integrals near the equatorial Γ at its own (E, L, μ²) levels.
  tabula's far-field shells are different levels.

**The decisive test is pre-registered separately** (tabula: strong-field, d = 6, where K³ is representable, so Kerr
resolves). The TS direction's coefficient vector is exported to the bridge only. Until that lands, the TS grade
stays as above, and this tension is carried with it.

**Correction (same day, from tabula):** the far-field direction is at **p = 3/5, q = 4/5**, not p = 4/5. So it is
**Vollmer's parameter point.** Vollmer 2016's rigorous theorem (no additional Killing tensor of valence ≤ 7, in
involution with the trivial ones) excludes reading (b) *as a Killing tensor*. What remains possible is:
- (a) an approximant, favoured; or
- a shell-restricted (fixed-energy) integral, which Vollmer's theorem does not cover.

tabula's standardised weights point the same way. 54–85% of the weight is at momentum degree 0 (a Carter-like
core), falling off with degree, spread over 60–83 terms. The strong-field d = 6 run (tabula `ef25326`) decides.
**tabula has not been told about Vollmer**, to keep its run blind to TS literature.

**Resolution of the tension (post-hoc, 2026-09-26).** tabula's strong-field d = 6 run (`ef25326`) is
**INCONCLUSIVE** under its frozen rule at both parameter points. Kerr's controls are green, and R1 resolves by
~1e19. Post-hoc, the TS direction's conservation relative to Kerr's Carter **degrades toward the source**:
5e2 → 5e4 → 2e7 at p = 3/5, and the deepest shell is also the worst at p = 4/5. Kerr's Carter holds at 1e-24 to 1e-23
on every strong-field shell.

That is the signature of a formal-series approximant, not of an exact invariant. Together with Vollmer 2016 at
p = 3/5 and the Morales–Ramis obstruction, **the tension is resolved in favour of the approximant reading.** This is
not a verdict of tabula's rung, whose own grades stay REFUSED / INCONCLUSIVE; it is the bridge's reading of all
the evidence. No further runs.

## V8-mono: quantum's TS δ=2 v2 monodromy certificates, reproduced by the bridge (2026-10-05, pre-registration committed 01:41)

**All 6 rows REPRODUCED.** Every gate passes on every row:
- provenance ≤ 6.5e−42;
- Abel ≤ 5.5e−10;
- convergence ≤ 6.6e−9.

Agreement with quantum's v2 midpoints is ≤ 2.9e−9 relative on all three invariants.

| Row | Point, (E, L, μ²) | tr[g,h], bridge |
|---|---|---|
| 0 | P1, (1,0,4) | 1.582859621 − 75.61779771i |
| 1 | P1, (1,0,9) | −2.336288614 + 6.5727524i |
| 2 | P1, (1,1,4) | 33.57839164 − 50.74493873i |
| 3 | P2, (1,0,4) | −49.07593352 + 101.8276866i |
| 4 | P2, (1,0,9) | −0.9817397367 (Im ~1e−9, i.e. numerically 0) |
| 5 | P2, (1,1,4) | −92.11550054 + 20.63826164i |

**What this closes.** The TS monodromy, which V8 recorded as *uncorroborated*, is now reproduced numerically by a
second code. The equations come from the bridge's own V8 derivation on ansatz's Ernst- and twist-checked metric.
Combined with quantum's v2 + v1 certificates, the TS δ=2 obstruction now has two routes:
- certified monodromy, by two quantum engines, reproduced by the bridge;
- the Kovacic/log-point argument of quantum 2b′ and bridge V8′.

**Instrument log.** The first attempt simplified p_t and q_t symbolically with `sp.cancel`. Memory ran away to
~8 GB, and the process was killed by hand (01:41–01:51) while ansatz's rank-6 job and quantum's jobs were running on
the 16 GiB box. The fix composes the x-coefficients numerically. Every run now sits under a self-kill guard at 2 GB,
and the process peaked at 0.12 GB. The runaway overlapped ansatz's watchdog stop at 01:50:34, which was disclosed to
ansatz. **Lesson: the bridge's own runs need a memory guard whenever the box is committed.**

Results: `results/v8_ts_monodromy.json`.

## V8-mono on quantum's bound-orbit levels (item 1), 2026-10-10

| Row | (p, E, L, μ²) | DOP853 (complex128) | HP (mpmath Taylor, 30/40 digits) |
|---|---|---|---|
| C1 | (4/5, 47/50, −39/5, 1), Dubeibe's level | INCONCLUSIVE (convergence 2.2e−7) | **REPRODUCED** |
| C2 | (3/5, 47/50, −52/5, 1) | REPRODUCED (3.0e−8) | **REPRODUCED** |
| C3 | (4/5, 19/20, −773/100, 1) | INCONCLUSIVE | **REPRODUCED** |
| C4 | (4/5, 97/100, −201/25, 1) | INCONCLUSIVE | **REPRODUCED** |
| C5 | (4/5, 97/100, 1051/100, 1) | REPRODUCED (2.4e−10) | **REPRODUCED** |
| C6 | (3/5, 19/20, −93/10, 1) | INCONCLUSIVE (Abel 1.8e−7) | **REPRODUCED** |
| C7 | (3/5, 97/100, −48/5, 1) | INCONCLUSIVE (Abel 1.5e−7) | **REPRODUCED** |
| C8 | (3/5, 97/100, 287/20, 1) | REPRODUCED (7.6e−11) | **REPRODUCED** |

**HP method** (pre-registered addendum, code `v8_hp.py`):
- p(x) and q(x) are reduced exactly to rational functions (degree ≤ 12).
- Taylor-series transport in t, with exact coefficient series at each centre.
- Convergence between (dps 30, K 60) and (dps 40, K 80) is ≤ 1e−22 on every row.

**Validation.** The validation rows (row 0, C2, C5, C8) come out at ~1e−16. That's the precision floor of the
double-precision targets the bridge stored, not the method's. Against the 25-digit strings quantum sent, C3's
tr[g,h] = 0.63414386438599461988417340… and C6's 1.29013464239116070983647387… agree to every digit quantum sent
(25 for C3, 24 for C6).

**The real-hyperbolic rows** (C1, C3, C4, C6, C7): tr[g,h] and tr²/det(h) come out real to |Im| ~ 1e−30 to 1e−35,
confirming quantum's "decided by the real part" reading:
- tr[g,h] ∈ (0, 2);
- tr²/det(h) ~ 1e4.

**So all 8 bound-orbit certificates, including Dubeibe's own level, are independently reproduced.**

**Instrument lesson.** Complex128 DOP853 runs out of digits on loops whose monodromy is real-hyperbolic of order 1e4.
There the commutator trace in (0, 2) comes from heavy cancellation. HP transport is the right tool there, and
tuning tolerances is not.

**Environment (back-filled 2026-10-11, per the fleet reproducibility policy):** CPython 3.14.5,
`/Users/sumit/Github/conjecture_machine/.venv`; numpy 2.4.6 (Accelerate), scipy 1.18.0, sympy 1.14.0, mpmath 1.3.0,
numba 0.65.1; macOS 26.5 arm64. Pinned in `ENVIRONMENT/` (bridge_env.json, bridge_requirements.lock). Assumed
unchanged since the run; the venv was not upgraded in between.

## Exact equation identity with quantum (2026-10-11), for the CAPD third replay
The bridge exported its own exact NVE coefficients (TS: `code/v8_export_capd.py`; MN: `code/v9_export_capd.py` and
`code/v9_export_capd_axial.py`; exports in `export_capd/`), each self-checked against its original unreduced
expressions at 40 digits (≤ 3.2e−27; most ≤ 1e−31).

Quantum's gate found the bridge's p and q to be **identical rational functions** to its own:
- P·Q′ − P′·Q ≡ 0 exactly, with the E_k = exp(w_k) as independent symbols;
- covering **all 14 TS rows** (0–5, C1–C8) and **all 6 MN equatorial rows** (quantum qsim/capd/replay_gate_ts.json,
  replay_gate_mneq_0.json, replay_gate_mneq_1_2_3_4_5.json @ 4afe971);
- the MN axial gate (VREPRO 0–3 = the bridge's V9 rows 6–9) is pending.

Two independently written derivations agree as exact identities, which is stronger than the earlier 50-digit numerical
agreement. Quantum's CAPD replay (MPFR, no Arb) integrates the BRIDGE's equations.

### CAPD third replay, results (quantum, MR_REPLAY.md)
- **TS row 0 (P1, E = 1, L = 0, μ² = 4): REPLAYED** (quantum 7e76def, 4.3 h).
  - Setup: CAPD/MPFR only (no Arb), the bridge's V8 fields, and the identical 16-gon loops.
  - Result: all three certificate conditions certainly hold. w_g and w_h lie outside [0, 4]; tr[g,h] =
    1.58285961940844 − 75.6177977170676i ≠ 2, with an enclosure width of 3.8e−24.
  - Cross-engine checks: it overlaps v2's w_g, w_h and tr_comm balls and v1's tr_comm, and every g and h matrix entry
    overlaps v2's exact Lean-export boxes.
- **TS row 2: REPLAYED** (quantum de7759e, 3.9 h). Every check is consistent: it overlaps v2's w_g, w_h and tr_comm,
  v1's tr_comm, and all of v2's exact G/H boxes. TS rows 0 and 2 are now third-replayed.
- **C1 (Dubeibe's far-field bound level; P2, E = 47/50, L = −39/5, μ² = 1): REPLAYED** under A2 (quantum ebf2b14,
  12.3 h). Every check is consistent: v2's w_g, w_h and tr_comm, v1's tr_comm, and v2's exact G/H boxes. The 2007
  paper's own level is therefore certified non-integrable by three engines on two independent arithmetic libraries
  (Arb ×2, MPFR).
- **C2: REPLAYED** (quantum, 10.9 h; every check consistent). That makes 5/24 replay rows: TS 0, 2, 3, C1 and C2. 0
  failures under A2.
- **C1 (Dubeibe's level), attempt 1: FAILED-CLOSED** on quantum's own 6 h watchdog, at 35/54 segments; its loops are
  based far out. Re-queued under amendment A2 (a 24 h watchdog, a resource-only change). The attempt-1 record is kept.
- **Amendments A5/A6 (quantum, 2026-10-12, registered before use):**
  - Local Taylor re-expansion on 32 exact dyadic sub-segments (MPFR intervals, shift gate, halving rule). It was
    introduced for the MN stall; see V9 FINDINGS.
  - Positive control: TS row 0 re-replayed under A5 matched the original path (overlapping tr[g,h]; 11 min vs 4.3 h).
  - A6 puts the unstarted TS rows on the A5 path. Already-REPLAYED rows are re-run under A5 as a cross-path record,
    and TS 4 and C3 run on both paths.
  - Rule: a cross-path non-overlap or verdict change is a FAIL to investigate.
- **TS row 1: REPLAYED** (A5 path, 12.7 min; every cross-engine check true; 0 halvings; tr[g,h] width 4.7e−8). Tally:
  6/24 (TS 0, 1, 2, 3, C1, C2), 0 failures.
- **TS row 5: REPLAYED** (A5 path, 22.8 min; every cross-engine check true; 0 halvings; tr[g,h] width 3.0e−9). Tally:
  7/24 (TS 0, 1, 2, 3, 5, C1, C2), 0 failures. TS row 4 is still running on both paths.
- **C4: REPLAYED** (A5 path, 28 min; every cross-engine check true; 0 halvings). Its max shifted-coefficient width is
  6.7e−11 absolute, larger because the C loops are based far out (|c| ~ 7, so coefficients scale like c^j). The gate
  and the v2 exact-box overlaps pass. Tally: 8/24 (TS 0, 1, 2, 3, 5, C1, C2, C4), 0 failures.
- **C5: REPLAYED** (A5 path, 26 min; every cross-engine check true; 0 halvings). Tally: 9/24 (TS 0, 1, 2, 3, 5, C1,
  C2, C4, C5), 0 failures.
- **Resource bug in quantum's per-loop layout (results unaffected).** The ONLY directive was placed after the loop
  data, so every per-loop process computed all loops (3× the CPU). The combine still takes loop n from process n, and
  every affected row passed the v2 exact-box overlaps. Fixed for rows started after this point; the fixed layout is
  validated by requiring bit-identical loop matrices for TS row 0.
- **Determinism check** (quantum qsim/capd/replay_results/determinism_check.txt). Covers the 5 rows affected by the
  layout bug: the A5 control, TS 1, TS 5, C4 and C5. Each of their 15 loops was computed independently by 3 separate
  processes. All 3 copies are bit-identical in every exact interval endpoint of all 8 matrix entries.
- **Layout fix validated:** TS row 0 through the fixed layout gives loop matrices bit-identical to the A5 control, on
  1 core in 667 s.
- **C6: NOT_REPLAYED** (undecided, not contradicted).
  - LOX_G and LOX_H are certain, but tr[g,h] ≠ 2 is undecided. The h loop has large monodromy (v2 w_h ≈ 22337); at
    prec 128 and tol 1e−25 the enclosure widths grow to w_h ~3.7e4 and tr[g,h] ~1e12.
  - Every cross-engine overlap is true (the enclosures contain v2's values), and w_g is tight.
  - Next step, by the registered escalation rule: the same A5 path at order 40, prec 256, tol 1e−40.
  - Tally: 9/24 REPLAYED, 1 NOT_REPLAYED pending escalation, 0 contradictions.
- **Amendment A7 (quantum), registered before any escalated result.** It applies to every NOT_REPLAYED row on the A5
  path, TS or MN:
  1. order 40, prec 256, tol 1e−40, SUBSEG 32;
  2. if still undecided, the same settings with SUBSEG 128 on all loops;
  3. then stop, and report the row as NOT_REPLAYED by CAPD (undecided, enclosures contain v1/v2), with no further
     tuning. The v1/v2 certificate stands.
  Contradictions are a FAIL to investigate, never something to escalate past. C6's loop copies are bit-identical
  (added to the determinism record).
- **C7: NOT_REPLAYED** on the A5 path at 128 bits (tr[g,h] undecided, width 6.7e3; every cross-engine overlap true).
  - Pattern: the C rows (P2 bound level) have far-out loop bases (|c| ~ 7). Their polynomial values are huge, so
    128 bits runs out. C1 and C2 passed on the original path at 256 bits.
  - Every NOT_REPLAYED A5 row goes through the A7 ladder mechanically.
  - Tally: 9/24 REPLAYED, 2 pending the ladder (C6, C7), 0 contradictions.
- **Cross-path FAIL made precise (quantum, registered before any cross-path result).** A FAIL is either
  non-overlapping enclosures of w_g, w_h or tr[g,h], or opposite CERTAIN decisions. An undecided run goes through the
  A7 ladder. A cross-path row still undecided after the ladder is listed as "overlap only (A5 undecided)".
- **A8 (quantum 7491a16), scheduling only:** C3 A5, the C1 secondary and the C1/C2 cross-path re-runs start at A7
  step-1 settings (prec 256). C8, already started at 128 bits, runs the normal ladder.
- **C8: REPLAYED** (A5 path at 128 bits, 9 min, fixed layout; every cross-engine check true; 0 halvings; tr[g,h]
  width 5e−6). Not every far-out C row exhausts 128 bits. Tally: 10/24 REPLAYED, 2 undecided pending the ladder (C6,
  C7), 0 contradictions.
- **TS row 4: REPLAYED** (A5 path, 7.8 min; every cross-engine check true; 0 halvings; tr[g,h] width 5.2e−9). The
  original-path run (>26 h) continues, and the cross-path comparison follows when it finishes. **All six TS plunging
  rows (0–5) are REPLAYED.** Tally: 11/24, 2 undecided pending the ladder (C6, C7), 0 contradictions.
- **C3: REPLAYED** (original path, 10.2 h; every cross-engine check true; tr[g,h] width 1.4e−15). Its A5 run (A8,
  starting at prec 256) completes the cross-path pair. Tally: 12/24 REPLAYED (TS 0–5, C1–C5, C8), 2 undecided pending
  the ladder (C6, C7), 0 contradictions.
- **C3 on the A5 path** (A8, prec 256): REPLAYED in 18.6 min (tr[g,h] width 4.5e−16).
- **Cross-path table** (quantum qsim/capd/replay_crosspath.py): exact overlap of w_g, w_h and tr[g,h] plus a verdict
  comparison. TS 0: AGREE. C3: AGREE. No FAIL.
- **A7 ladder** started for C6 and C7 in parallel (scheduling only). Tally: 12/24 REPLAYED, 2 in the ladder, 0
  contradictions.
- **TS 0 secondary (a homotopic 24-gon at 0.8r, same base and approach ray, A5 path): REPLAYED** in 4.7 min. All 24
  loop-matrix entries overlap both primaries, the original path and the A5 control (exact comparison; quantum
  qsim/capd/replay_secondary_check.json). The monodromy is unchanged on an independently discretised homotopic loop,
  which rules out a discretisation artefact shared by the engines.
- **C1 secondary (Dubeibe's level; homotopic 24-gon at 0.8r; A5 at prec 256): REPLAYED** in 15 min (tr[g,h] width
  2.9e−16). All 24 loop-matrix entries overlap the original-path primary's (exact). Both registered TS secondaries
  (TS 0 and C1) are done.
