# Leg V — Pre-registration: the bridge's box-dimension instrument, transferred from GR orbits to quantum's detector wall

*Frozen 2026-07-03, before `code/fractal_boundary_dim.py` is written or run. A **cross-domain instrument
transfer** in the shape of leg R: the bridge's **box-counting dimension** — built to tell regular GR orbits
(section ≈ 1-D curve, D≈1) from chaotic ones (section fills 2-D, D→2), validated there on Hénon–Heiles and
the di-hole (leg J) — is pointed at **quantum's QM detector-wall experiment** (`qsim/fractal_boundary.py`).
Quantum passed a double-slit interference pattern onto a detector wall with three absorbing masks along y
— uniform, periodic (8 evenly-spaced segments), and a level-3 **Cantor set** (8 segments, same 8/27
coverage as periodic) — and concluded, via JS-divergence and fringe-correlation, that boundary geometry
co-decides where clicks land but "nothing fractal-specific" is manufactured by the dynamics. The bridge
adds the axis quantum never used — **fractal dimension** — as a sharper, quantitative test of that exact
claim. Read-only from quantum (the bridge reconstructs the Cantor geometry analytically and
**reimplements** the wave sim in its own code; it does not import or modify quantum's files).*

## The instrument (faithful 1-D analog of ansatz `poincare.box_dimension`)

ansatz's box-dim normalizes a point set to its bounding box, counts occupied cells at grids `G`, and takes
the slope of `log N(G)` vs `log G`. Leg V uses the **1-D** version: for a set of occupied positions along
y (a mask's absorbing cells, or a detection pattern's support), normalize to [0,1], count occupied cells at
grid `G`, `D = slope(log N vs log G)`. Same estimator, one dimension.

**Certain anchor:** on the analytic Cantor set at grids `G = 3,9,27,81,243`, the occupied counts are
`N = 2,4,8,16,32`, so `D = log2/log3 = 0.63093` **exactly** — a hard, known target for validation.

## Frozen gates

- **V1 — the instrument reads dimension correctly in the new domain (certain).**
  - Analytic level-6 Cantor set, grids (3,9,27,81,243): measured `D` within **0.02** of `log2/log3 =
    0.63093`.
  - Uniform wall (all cells occupied): measured `D` within **0.02** of **1.00**.
  PASS = the bridge's GR-born box-dim estimator recovers the exact fractal dimension of quantum's Cantor
  boundary and the integer dimension of the solid wall — validated cross-domain, independent of its origin.
- **V2 — the dimensional discriminator quantum did not use.** At **identical coverage** (8/27 ≈ 0.296),
  the bridge's box-dim over the self-similar band (grids 3,9,27; cell sizes 108→36→12 ≥ the 12-cell finest
  segment) **separates** the Cantor wall from the periodic wall:
  `D(periodic) − D(cantor) > 0.10`, with `D(cantor) ≈ 0.63` and its **local log-log slopes scale-invariant**
  (std of the per-octave slopes < 0.05) while periodic's drift (larger std). PASS = fractal dimension is a
  discriminating axis where quantum's coverage-matched design left only JS-divergence; FAIL (they don't
  separate at accessible scales) is itself an honest instrument-resolution finding.
- **V3 — the QM cross-check: the detection pattern inherits the boundary's dimension, doesn't manufacture
  fractality.** The bridge **reimplements** quantum's 2-D Schrödinger double-slit + detector-wall sim (its
  own code, same geometry) and:
  1. **reproduces quantum's qualitative result independently** — the three walls gate differently
     (`JS(cantor,uniform) > 0.1` and `JS(periodic,uniform) > 0.1`) and the pattern is gated-not-shifted
     (`corr(detected, incident × mask) > 0.8` on live cells);
  2. the **Cantor detection support** carries the boundary's dimension, not an integer one manufactured by
     the dynamics: `D(cantor clicks support)` sits in the sub-integer band, **< 0.85** (tracking the mask's
     0.63, allowing for finite-wavelength blur), and is closer to the Cantor mask's D than to 1.0.
  PASS = quantum's "boundary gates, nothing fractal-specific added" is confirmed *quantitatively, in
  dimension*, by an independent reimplementation.
- **V3 framing (fixed in advance, honest limits).** This is a **lattice** wave simulation with numerical
  diffraction; the de Broglie wavelength (`λ = 2π/k₀ ≈ 6.3` cells) is comparable to the 12-cell finest
  Cantor segment, so the quantum probe can only **image the fractal boundary down to ~λ** — a resolution
  floor, the QM instance of the bridge's recurring **"walls are instrument-relative"** theme (leg R, Phase
  5). The result is a **cross-repo triangulation** (the bridge's GR box-dim instrument transferred to QM
  confirms quantum's boundary-gating with a quantitative dimension); it is **not** a claim about continuum
  QM, real detectors, or higher dimensions.

## Inputs (read-only) & method notes

- quantum `qsim/fractal_boundary.py` + `PLAN_projections.md` — the experiment specification and its verdict
  ("boundary structure co-decides detection statistics via ordinary wave mechanics; nothing
  fractal-specific"). The bridge reconstructs the mask geometry from the spec and reimplements the sim; it
  does **not** import quantum's module (which would execute and write into the source repo).
- ansatz `scripts/poincare.py::box_dimension` — the estimator leg V mirrors in 1-D.
- Wave-sim parameters mirror quantum's for a faithful reproduction: grid 480×324, dx=1, dt=0.2, k₀=1,
  det wall at x=430, level-3 Cantor (8 segments of 324/27=12 cells), periodic (8 segments, matched 8/27).
