# Leg O — Findings: the Killing-tensor search as a catalog SURVEY instrument (B4)

*Run 2026-06-24 (backlog B4). Phase 1 built a symbolic Killing–Yano existence search for single metrics
(leg J). This turns it into a reusable INSTRUMENT — one uniform search run across the ansatz metric
catalog, classifying which spacetimes admit a (Carter-type, KY-origin) hidden symmetry. Uses gr_engine
read-only.*

## Result in one line

A single symbolic Killing–Yano search, applied uniformly, correctly classifies the whole catalog: it
recovers the Carter-type hidden symmetry on every integrable metric — **including the genuinely non-Kerr
Taub–NUT** — and reads **NONE** for the bumpy metric (leg J). The discover→verify machinery is now a
reusable instrument, not a one-off. **Extended (2026-06-26):** the same search, run in *prolate-spheroidal*
coordinates on the exact **Zipoy–Voorhees γ-metric**, recovers Schwarzschild's KY (δ=1, gate) and reads
**NONE** for the deformed γ-metric (δ=2) — a *second*, literature-standard non-integrable spacetime, in
*different coordinates*, so the instrument keys on integrability itself, not on one bump or one chart.

## The survey (degree-≤4 KY 2-form search, exact rational linear algebra)

| metric | KY 2-forms (deg ≤4) | hidden symmetry? |
|---|---|---|
| Schwarzschild | 1 | YES (integrable) |
| **Kerr** (gate) | **1** | YES — gate ✅ |
| Kerr–Newman | 1 | YES |
| Kerr–de Sitter | 1 | YES |
| **Taub–NUT** | **1** | YES — *non-Kerr* integrable ✓ |
| bumpy ε=0.35 | **0** | NO (leg J) |

- **Gate passes:** Kerr recovers its unique Killing–Yano tensor.
- **The instrument is not Kerr-specific:** Taub–NUT — a structurally different stationary-axisymmetric
  metric (a NUT charge gives `g_tφ ∝ cosθ`, no relation to Kerr's rotation) — is correctly found
  KY-integrable. So the search keys on the genuine hidden symmetry, not Kerr-shaped coincidences.
- **The non-integrable case reads NONE:** the bumpy metric (leg J's deformation) has no KY tensor,
  reproduced here in the uniform survey.

## Update (2026-06-26) — Zipoy–Voorhees γ-metric: a second non-integrable confirmation, in a second chart

The catalog above is all Boyer–Lindquist (r, u=cosθ) with a *single* non-integrable example (the bumpy
metric). To test that the instrument flags **integrability itself** — not a quirk of one bump or one
coordinate system — we added the **Zipoy–Voorhees (γ-) metric** (ansatz `zipoy_voorhees.py`): an *exact*
static vacuum with a tunable Geroch–Hansen quadrupole, δ=1 ≡ Schwarzschild, δ≠1 genuinely non-integrable (a
documented chaotic testbed, Lukes-Gerakopoulos 2010). It is naturally written in *prolate-spheroidal* (x, y),
so the same KY-nullspace search was run with monomials in (x, y). For integer δ the metric is rational, so
the exact-rational linear algebra carries over; δ=2 is the clean deformed case.

| metric | coords | KY 2-forms (deg ≤4) | hidden symmetry? |
|---|---|---|---|
| **ZV δ=1** (Schwarzschild) | prolate (x,y) | **1** | YES — gate ✅ |
| **ZV δ=2** (γ-metric) | prolate (x,y) | **0** | NO (non-integrable) |

- **Gate passes in the new chart:** Schwarzschild's KY tensor is recovered from the prolate-coordinate
  metric — the search is not tied to Boyer–Lindquist.
- **A second non-integrable case reads NONE:** the δ=2 γ-metric — a *different* deformation from leg J's
  bump (an exact vacuum naked singularity vs. an axisymmetric quadrupole bump), and a literature-standard
  chaotic spacetime — admits no degree-≤4 KY tensor. So the instrument's NONE is about integrability, not
  about one specific bump. (This also predicts, via leg Q's legible ⟺ KY-integrable, that a learned ZV-δ=2
  geometry would be *non-legible* — a clean future tabula cross-check.)

**Update (2026-06-26/07-02) — both halves of the prediction landed.** (i) tabula ran the legibility probe on
real ZV geodesics (§132): δ=1 emits the separation constant exactly, **δ=2 is non-legible** — the predicted
cross-check, confirmed (leg Q, now 8/8). (ii) ansatz **exhibited ZV δ=2's actual chaos** (§106, using the
frequency-drift detector the bridge built for leg J): the razor-thin stochastic layer at the plunge
separatrix — layer x0=7.545 (drift 0.0266, escapes after 210 crossings) vs the eternal island chain at
~1e-4, a 267× split 0.012 apart in x0, both chaos signatures (frequency wander + finite lifetime). So this
row's "NO hidden symmetry" is now backed at **all three levels: symbolic** (this survey: no KY tensor),
**neural** (tabula: non-legible), and **dynamical** (ansatz: chaos exhibited) — the strongest-validated
non-integrable entry in the catalog.

## What it buys

One symbolic search now **classifies any catalog metric** as KY-integrable or not — turning leg J's
single-metric proof into a reusable instrument with a clean reference table. The integrable rows
reproduce textbook integrability (calibration, not new physics); the value is the *uniform instrument* and
the non-Kerr (Taub–NUT) generalization test.

## Honest limits
- **Degree ≤4, KY-origin.** The search rules in/out a Killing–Yano 2-form of polynomial degree ≤4. A
  higher-degree KY tensor, or a rank-2 Killing tensor *not* of KY origin, would be missed — those need the
  numeric rank-2 / rank-4 SVD search (leg J's `numeric_killing_search.py` / `numeric_quartic_search.py`),
  which can be added to the survey per metric (at the cost of orbit sampling).
- All integrable rows are known results; this is an instrument/calibration demonstration, not a discovery.

## Artifacts
- `code/survey_catalog.py` — the catalog metrics (Schwarzschild, Kerr, KN, KdS, Taub–NUT, bumpy) in
  rational u=cosθ coords + the uniform KY survey. `results/survey_catalog.json`.
- `code/survey_zv.py` — the Zipoy–Voorhees γ-metric (ansatz `zipoy_voorhees.py`) in prolate-spheroidal
  (x,y); same KY search, Schwarzschild-gated (δ=1), δ=2 reads NONE. `results/survey_zv.json`.
