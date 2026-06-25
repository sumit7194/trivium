# Leg Q — Findings: legibility ⟺ KY-integrability (A10, the well-posed revival)

*Run 2026-06-26 (A10). Closes the loop SISTER_REQUESTS.md opened: A10 was retired as ill-posed
("geometrizes ⟺ universal ∧ conservative as an exact proof" — not a metric theorem), and reframed as a
*testable* question — **does a learned geometry become legible iff the metric is KY-integrable?** tabula
answered its half (§127); this leg joins tabula's `legible` column to leg O's `KY-integrable` column and
tests the equivalence across the catalog. Both source artifacts are consumed READ-ONLY.*

## Result in one line

Across the catalog, **a learned geometry is legible iff the metric admits a Killing tensor** — tabula's
neural legibility instrument EMITS the verified hidden invariant (Carter constant) for exactly the metrics
that leg O's symbolic Killing–Yano survey finds integrable, and CERTIFIES "no invariant" for exactly the
ones it finds non-integrable. **7/7 metrics agree on the joint set; Matthews φ = 1.0** (perfect
separation), with **two independent non-integrable cases**. Two deliberately-independent repos — a *neural*
probe on observed geodesics (tabula) and a *symbolic* KY algebra on the exact metric (leg O) — reach the
identical integrability verdict metric by metric. A10 is un-retired in its well-posed form, and **confirmed**.

## The join (tabula `legible` vs leg O `KY-integrable`)

| metric | leg O: KY-integrable (symbolic) | tabula: legible (neural) | agree |
|---|---|---|---|
| Kerr | yes | yes | ✅ |
| Kerr–Newman | yes | yes | ✅ |
| Kerr–de Sitter | yes | yes | ✅ |
| Taub–NUT | yes | yes | ✅ |
| bumpy (quadrupole) | **no** | **no** | ✅ |
| **Zipoy–Voorhees δ=1** (Schwarzschild) | yes | yes | ✅ |
| **Zipoy–Voorhees δ=2** (γ-metric) | **no** | **no** | ✅ |

Contingency on the joint set: integrable&legible = 5, non-integrable&non-legible = 2, false-legible = 0,
missed = 0 → **φ (Matthews) = 1.0**. tabula reports ~26 orders of magnitude separating "emit" (engine
held-out variance ~1e-28 on the integrable metrics) from "certify" (~1e-2 on the bumpy ones) — the
legibility split is not marginal, it is categorical.

**Update (2026-06-26) — Zipoy–Voorhees closes the loop, both repos independently.** After leg O added the
exact ZV γ-metric to its symbolic KY survey (δ=1 → KY tensor, δ=2 → none), tabula ran §132: it built the
*real* ZV geodesic Hamiltonian in prolate-spheroidal coords and applied its emit-or-certify legibility
instrument, deriving the exact separation constant `C = (1−y²)p_y² + L²/(1−y²)` to look for. It **EMITS C for
δ=1** (Schwarzschild: conserved to 1.1e-23 = integration precision, cosine-to-C = 1.000) and **CERTIFIES no
invariant for δ=2** (C-drift 8.0e-6 = **7×10¹⁷×** the integrable floor; 3e-4 in the strong-chaos region). So
the legible ⟺ integrable equivalence now holds on a **second, independent non-integrable spacetime** — a
*different deformation* (exact static vacuum γ-metric vs the axisymmetric bump) in *different coordinates*
(prolate x,y vs Boyer–Lindquist r,u) — verified by both the neural (tabula §132) and symbolic (leg O
`survey_zv`) routes. The §9 claim is no longer resting on a single bump.

**Single-repo metrics (consistency check, same rule):**
- *leg O only* — **Schwarzschild**: KY-integrable = yes (tabula did not run a legibility datum for it; the
  KY survey's gate metric).
- *tabula only* — **bumpy-strong**: legible = no, tabula-integrable = no → **consistent** with
  legible ⟺ integrable on tabula's own labels.

So a *union* view spans 9 metrics, every one consistent with the equivalence; **7 are directly
cross-validated** across both repos (Kerr, KN, KdS, Taub–NUT, bumpy, ZV δ=1, ZV δ=2), with two of them
(bumpy, ZV δ=2) *independent* non-integrable cases.

## What this establishes (and what it does not)

- **It is the cross-validated form of THE_BRIDGE §9's "geometrizes ⟺ conservative."** The directional claim
  (Move E) is now a metric-by-metric equivalence checked by two *methodologically independent* instruments:
  tabula learns a geometry from observed geodesics and asks whether a distillation head can emit a verified
  conserved quantity; leg O asks the exact metric, symbolically, whether a Killing–Yano tensor exists. They
  agree everywhere. That agreement — neural-empirical ↔ symbolic-exact — is exactly the bridge's thesis.
- **It localizes the boundary at integrability, not at "Kerr-ness."** Taub–NUT (a *non*-Kerr vacuum) is both
  legible and KY-integrable; the bumpy deformation is neither. So the learnability/legibility transition
  tracks the *hidden symmetry*, not proximity to Kerr — consistent with leg O (Taub–NUT carries Kerr's
  rank-2 structure) and leg J (the bump has no Killing tensor of degree ≤4).

## Honest limits (per §7)

- **tabula's toy is a faithful Stäckel-separable, Kerr-like geodesic model** (tabula's own scope note):
  Kerr–de Sitter is modeled as a *separable cosmological deformation* (the full rational-Carter KdS lives in
  tabula script 97), and Taub–NUT via the NUT gravitomagnetic shift L → L − 2n cosθ (web-verified:
  Kerr–Taub–NUT shares Kerr's 2nd-rank Killing tensor). The equivalence is demonstrated on this catalog, not
  proven for all spacetimes.
- **"Certify" tests for the absence of an *exact low-degree* invariant, not literal chaos** (the KAM caveat:
  a crude approximate invariant can linger under bounded confinement). This matches leg J precisely — the
  bump is *formally* non-integrable (no KY tensor of degree ≤4) and *near*-integrable (no chaos found), and
  the legibility instrument keys on the formal non-existence, which is the right target.
- **Not fully orthogonal in spirit.** Both instruments ultimately probe the same underlying fact (does a
  Killing tensor exist). The independence is *methodological* — a learned neural probe vs symbolic algebra,
  in two separate repos — not logical. The value is that two very different computational routes to the same
  question never disagree, on 5 metrics spanning charge, cosmological constant, and NUT charge.

## Inputs (read-only) & artifacts

- tabula §127 — `/Users/sumit/Github/SpaceTime/curvature/results/127_integrability_legibility.json`
  (`legible` per metric) + `notes/A10_for_bridge.md`.
- tabula §132 — `/Users/sumit/Github/SpaceTime/curvature/results/132_zv_gamma_metric.json` (ZV γ-metric
  legibility on real geodesics; δ=1 emits C, δ=2 certifies none).
- leg O — `legO_catalog_survey/results/survey_catalog.json` + `survey_zv.json` (`ky_dim` per metric, incl. ZV).
- `code/geometrizes_integrability.py` — normalizes metric names across the repos, joins the columns (incl.
  the ZV extension), builds the 2×2 contingency, reports φ. `results/geometrizes_integrability.json`.
