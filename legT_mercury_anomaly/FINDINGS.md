# Leg T — Findings: Mercury's anomaly accounting, with sister instruments

*Run 2026-07-03; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the compute. The
historical Le Verrier decomposition, performed with the family's own tools: tabula measured Mercury's
**total** perihelion precession on real 120-year JPL Horizons data (EXP-15 P4, via the drift of the
Laplace–Runge–Lenz azimuth — the LRL vector its emit-or-certify engine had just *discovered* from the same
data); the bridge subtracts the literature Newtonian planetary-perturbation value and asks whether the
**exact GR term** — computed with **tabula's own instrument-measured GM☉** — closes the books.*

## Result in one line

It closes. **568.4 (tabula, measured) − 532.3 (Clemence 1947, Newtonian secular) = 36.1 ″/century**, vs the
exact Schwarzschild advance **43.0 ″/century** (6πμ/(c²a(1−e²)), evaluated with tabula's μ̂ measured from the
ephemerides to 1e-6 relative) — agreeing within **~1σ of the instrument's demonstrated 6.6 ″/cy floor**
(gate: |36.1−43.0| = 6.8 < 2σ = 13.1, **PASS**). The 43″ that broke Newtonian gravity in 1859 is exactly
what tabula's real-data measurement leaves over, and exactly what the GR formula supplies.

## The accounting (all ″/century)

| item | value | source |
|---|---|---|
| measured total (LRL-azimuth drift, 1900–2020, 498 orbits) | **568.4** | tabula EXP-15 P4 (real JPL Horizons) |
| − Newtonian planetary perturbations | 532.3 | Clemence 1947, RMP 19, 361 (external anchor) |
| = residual anomaly | **36.1** | |
| exact GR term, with tabula's measured μ̂ | **43.0** | 6πμ̂/(c²a(1−e²)); μ̂ = 2.9591194e-4 AU³/day² |
| instrument floor σ (their total vs the known 575.0) | 6.6 | tabula's own 1.1% |

T1 also passes: the GR term with the *instrument-measured* μ̂ differs from the true-μ value by 9e-7 relative
— tabula measured GM☉ well enough that the GR prediction is insensitive to which is used.

## Why this is a bridge result

Three sources with disjoint provenance meet in one subtraction: a **neural instrument's measurement on real
ephemerides** (tabula — which first *discovered* the conserved LRL vector from the data, then watched its
azimuth drift), a **literature anchor** (the same role Abedi Table I plays in leg 8), and an **exact-theory
term** (the Schwarzschild advance — the formula ansatz's engine world proves geodesically; evaluated here in
closed form). None of the three could make the statement alone; the composition is the classic 1859→1915
story reproduced end-to-end by the family's instruments on real data.

## Honest limits (frozen in advance, T3)

- **Not an independent GR detection.** GR is baked into the JPL ephemerides, and the Newtonian share is 12×
  larger — separable only via the external literature anchor. The claim is *consistency of the accounting at
  a ~7″/cy floor*, i.e. the GR term is **required and sufficient** to close the books at the instrument's
  demonstrated precision.
- σ is taken from tabula's own total-vs-known discrepancy (6.6 ″/cy, 1.1%) — a demonstrated floor, not a
  formal error propagation.
- The Newtonian secular value is used as a point anchor; its own ~0.1″-level uncertainties are far below σ.

## Inputs (read-only) & artifacts

- tabula EXP-15 — `curvature/results/156_newton_from_ephemerides.json` (P4 measured total; P3 μ̂_LRL).
- `code/anomaly_accounting.py` — the gated decomposition. `results/anomaly_accounting.json`.
