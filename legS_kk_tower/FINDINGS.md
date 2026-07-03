# Leg S — Findings: the Kaluza–Klein mass tower — one number, four repos, four independent routes

*Run 2026-07-03. The bridge's first FOUR-repo cross-validation, and the leg that formally welcomes the
**quantum** project (a local QM-foundations lab, `/Users/sumit/Github/quantum`) as the 4th sister. Its
flagship idea — "mass = hidden-dimension momentum" (a massless 5D field on a circle of radius R appears in
4D as a tower of massive fields, m_n = n/R) — was pursued independently in three sibling repos; nobody had
joined the numbers. All inputs read-only.*

## Result in one line

The KK tower **m_n/m_1 = n** holds across **four deliberately-independent routes in four repos** — a
machine-**proven** reduction (ansatz §111: 5D vacuum ⇔ 4D Einstein–Maxwell–dilaton, every dictionary
coefficient derived symbolically, the planted "frozen-scalar" trap caught), **direct numerics** (quantum
`kk_projection.py`: max err **0.22%**), an **independent reimplementation** (tabula §157 FDTD: **0.66%**;
cross-implementation agreement with quantum **0.44%**), and a **neural net that discovers the tower from
visible projections alone** (tabula §157 learned ladder: **1.44%**, latent→n isotonic R² = 0.99996, the
n=0 massless mode correctly learned ≈ 0). Gate PASS.

## The join (`code/kk_tower_join.py`)

| n | exact | quantum ω_n (direct) | tabula FDTD ω_n (indep. impl.) | tabula LEARNED m_n (from projections) |
|---|---|---|---|---|
| 1 | 1 | 1.0022 | 1.0066 | 1.0078 |
| 2 | 2 | 2.0031 | 2.0027 | 1.9920 |
| 3 | 3 | 3.0027 | 2.9989 | 2.9567 |
| 0 | 0 | — | — | **0.0550** (massless mode ≈ 0 ✓) |

Group velocities (quantum vs exact Klein–Gordon at the same kick): 0.999/1.000 · 0.703/0.707 · 0.445/0.447
— the projection doesn't just buzz at the right rest frequency, it *travels* like the massive field it
projects to.

## Why this is a bridge result and not a summary

- **The four routes fail differently.** A symbolic-derivation error (route 1), a discretization artifact
  (routes 2–3), and a representation-learning artifact (route 4) have no common failure mode; their
  agreement on one dimensionless ladder is the cross-validation. Routes 2 and 3 are separate codebases
  (agreement 0.44%) — implementation independence, the same standard leg Q applied.
- **The theorem anchor is load-bearing.** ansatz §111 turns m_n = n/R from a modeling assumption into the
  mode-expansion consequence of a *proven* reduction — including the honesty trap (the quantum project
  deliberately planted "5D vacuum = gravity + EM with the scalar frozen"; the machine extracted the F²=0
  obstruction and rejected it). The numeric towers then test the *consequence* against three instruments.
- **The learned route is the §9-thesis case.** tabula's K=1 bottleneck saw only visible projections — no
  hidden coordinate — and discovered the integer winding and its mass ladder. That is "discover the hidden
  structure from observations, then verify against the exact theory," the bridge's founding pattern, now
  running through a hidden *dimension* rather than a hidden *invariant*.

## Honest limits

- The exact tower here is the flat-space KK toy (2D massless wave on a strip, R=1) — the pedagogical core
  of the idea, not the full curved §111 geometry; the theorem and the numerics meet at the mode-expansion
  level, not as a single end-to-end computation.
- quantum's numbers are read from its recorded, verified run (`qsim/PLAN_projections.md` Route A) — the
  bridge did not rerun its simulation (the project is local-only and not git-tracked; its numbers were
  already independently replicated by tabula's separate FDTD, which is the stronger check anyway).
- The learned ladder's 1.44% (and n=0 at 0.055) is representation noise, not physics — tabula's own scope.

## Inputs (read-only) & artifacts

- ansatz §111 — `conjecture_machine/scripts/111_kaluza_klein.py` + RESULTS.md (the proven dictionary).
- quantum — `qsim/kk_projection.py` numbers as recorded in `qsim/PLAN_projections.md` (Route A).
- tabula §157 — `curvature/results/157_kk_mass_discovery.json` (G0 FDTD replication + K1/K2 learned tower).
- `code/kk_tower_join.py` — the gated four-route join. `results/kk_tower_join.json`.
