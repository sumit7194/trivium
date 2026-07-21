# Leg Y — Pre-registration: CK adjudication of the bridge's own catalog (auditing leg Q's independence assumption)

*Frozen 2026-07-21, before `code/ck_adjudicate.py` is written or run. **A falsification-flavoured
self-check of the bridge's strongest result.** Leg Q claims "legible ⟺ KY-integrable, **8/8**, Matthews
φ = 1.0", and rests on an assumption never tested: that its eight catalog entries are **eight genuinely
different spacetimes**. Two metrics can look entirely different on paper and be the same spacetime in
different coordinates — the costume problem. Until now the family had no decision procedure. ansatz has
just built one (`scripts/ck.py`, §116–§118) and it *already* found a costume: ZV δ=1 in prolate spheroidal
coordinates is byte-identically Schwarzschild. This leg points that instrument at our own count.*

**No preferred outcome.** All three verdicts below are pre-registered as equally acceptable and reported
identically. A downward correction to our own headline is a *result*, not a loss; the number is either
true or it is not.

## The catalog under audit (leg Q's joint set, verbatim)

| # | entry | leg Q verdict | construction |
|---|---|---|---|
| 1 | Kerr | integrable | leg O `delta_metric(A, r²−2r+A²)` |
| 2 | Kerr–Newman | integrable | `delta_metric(A, r²−2r+A²+¼)` |
| 3 | Kerr–de Sitter | integrable | leg O catalog |
| 4 | Taub–NUT | integrable | leg O catalog (non-Kerr, integrable) |
| 5 | **bumpy ε=0.35** | **non-integrable** | `delta_metric(A, …, bump)` — **rotating** Kerr-form deformation |
| 6 | ZV δ=1 | integrable | leg O `zv_geometry(1)` — prolate spheroidal; *known* = Schwarzschild |
| 7 | **ZV δ=2 (γ-metric)** | **non-integrable** | `zv_geometry(2)` — **static** |
| 8 | **Manko–Novikov q=0.5** | **non-integrable** | rotating Geroch–Hansen quadrupole |

Note (established before running, not a result): entries 5 and 7 cannot coincide — 5 is stationary-rotating
(spin A ≠ 0), 7 is static. Different Killing structure. **The genuinely exposed pair is 5 vs 8** — *both*
rotating quadrupole deformations of Kerr, which leg Q counts as two of its "three independent
non-integrable classes."

## Frozen gates

- **Y0 — instrument cross-check (must pass for the rest to mean anything).** The bridge's *own* ZV δ=1
  geometry (leg O's `zv_geometry(1)`, our construction, prolate spheroidal) fed to ansatz's CK must return
  **EQUIVALENT** to Schwarzschild in standard coordinates — independently reproducing ansatz §116's headline
  through a *different metric construction*. FAIL ⇒ stop; the instrument is not doing what we think on our
  inputs, and no downstream verdict is trustworthy.
- **Y1 — the integrable entries are distinct.** All pairs among {Kerr, Kerr–Newman, Kerr–de Sitter,
  Taub–NUT, ZV δ=1} return **INEQUIVALENT** (expected: they differ in matter content / Λ / NUT charge, which
  §117's order-0 Ricci–Segre invariants separate without any frame fixing). Any **EQUIVALENT** here is a
  duplicate in leg Q's count. Any **UNDECIDED** is reported as such, not counted as either.
- **Y2 — the three "independent non-integrable classes" (the claim at risk).** Pairs among
  {bumpy ε=0.35, ZV δ=2, MN q=0.5}, with the 5-vs-8 pair as the sharp case. Pre-registered outcomes, all
  equally acceptable:
  1. **all INEQUIVALENT** ⇒ leg Q's "three independent classes" is upgraded from *assumed* to **proven**;
  2. **any EQUIVALENT** ⇒ leg Q's independent-class count **corrects downward** (three → two), and leg Q's
     FINDINGS is amended the same day with the correction stated in its headline, not a footnote;
  3. **UNDECIDED** ⇒ reported as an instrument wall (see below), and leg Q's claim reverts to explicitly
     *assumed*, with the assumption named in its FINDINGS.
- **Y3 — the expected wall, pre-registered as a legitimate outcome.** ansatz's own scope notes: types D and
  I decided; II/III and order-1 null-rotation isotropy → UNDECIDED; type-I exponents need rationalizing;
  and "anything genuinely two-variable (r *and* θ, serious rotation) blows up the algebra engine"
  (their killed 7.5 h runs; Kasner u=3 unfinished at 25 min). Entries 5 and 8 are exactly that regime, so
  **UNDECIDED on the sharp pair is the most likely single outcome** and is *not* a failure of this leg — it
  is a measurement of the instrument's reach, and the family's recurring
  *walls-are-instrument-relative* theme in its symbolic-algebra edition.
  Budget: **600 s per CK signature**, timeouts recorded as UNDECIDED(wall) and distinguished in the results
  JSON from UNDECIDED(procedure).

## Method & scope

- ansatz `scripts/ck.py` + `gr_engine.Geometry` are used **read-only**, via ansatz's own venv (precedent:
  leg J used `poincare.box_dimension`; leg X used their mpmath). All bridge code lives in TheBridge.
- Metric constructions are the **bridge's own** (leg O's `survey_catalog.py` / `survey_zv.py` forms), not
  copied from ansatz's CK batteries — so Y0 is a genuine cross-construction check, not a replay.
- Rigour direction, stated in advance: a **differing** invariant/certificate is a rigorous INEQUIVALENT;
  **matching** ones are necessary-but-not-sufficient unless CK's isotropy/functional-relation recursion
  terminates. Verdicts are reported with which of the two they are.
- Out of scope: literature novelty; whether tabula's legibility toy model faithfully represents each metric
  (leg Q's own scope note stands); the KY/legibility verdicts themselves — this leg audits **only** the
  independence of the entries, i.e. the denominator of "8/8".

---

## AMENDMENT (2026-07-21, **post-hoc — written AFTER seeing the v1 wall**, before `ricci_route.py` runs)

**Disclosure:** this amendment was made *after* observing that 6 of 8 CK signatures exceeded the 600 s
budget (Y1 10/10 undecided, Y2 undecided). It is therefore not a blind pre-registration and is labelled as
such wherever its results are reported.

**Y1b — the cheap sound route.** ansatz §117 established that `tr((R^a_b)^k)`, k=1..4, are **order-0 and
frame-independent** — they need no tetrad, no canonicalization, and no ∇C, so they escape the
expression-swell wall that stopped the full procedure. §117 also fixes the logic: *differing invariants are
a rigorous INEQUIVALENT; matching ones are necessary but not sufficient.*

Gate, one direction only:
- pairs whose order-0 Ricci invariant vector / Segre type **differ** ⇒ **rigorously INEQUIVALENT**
  (counts as decided, and is proof-strength);
- pairs that **match** ⇒ **INCONCLUSIVE by this route** (explicitly *not* evidence of equivalence — the
  vacuum entries all have R_ab = 0 and will match trivially);
- the sharp pair (bumpy vs MN) is untouched by this route, since both are vacuum-type deformations.

This can only *increase* the decided fraction of Y1; it cannot rescue Y2, and no matching result from it
will be reported as support for distinctness.
