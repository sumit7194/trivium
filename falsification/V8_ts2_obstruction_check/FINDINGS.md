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
