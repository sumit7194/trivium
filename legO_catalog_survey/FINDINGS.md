# Leg O — Findings: the Killing-tensor search as a catalog SURVEY instrument (B4)

*Run 2026-06-24 (backlog B4). Phase 1 built a symbolic Killing–Yano existence search for single metrics
(leg J). This turns it into a reusable INSTRUMENT — one uniform search run across the ansatz metric
catalog, classifying which spacetimes admit a (Carter-type, KY-origin) hidden symmetry. Uses gr_engine
read-only.*

## Result in one line

A single symbolic Killing–Yano search, applied uniformly, correctly classifies the whole catalog: it
recovers the Carter-type hidden symmetry on every integrable metric — **including the genuinely non-Kerr
Taub–NUT** — and reads **NONE** for the bumpy metric (leg J). The discover→verify machinery is now a
reusable instrument, not a one-off.

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
