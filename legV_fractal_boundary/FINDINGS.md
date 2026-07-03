# Leg V — Findings: the bridge's box-dimension instrument, transferred from GR orbits to quantum's detector wall

*Run 2026-07-03; gates V1/V2/V3 frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before a line was
written. A **cross-domain instrument transfer** in the shape of leg R: the bridge's box-counting dimension
— built to separate regular GR orbits (D≈1) from chaotic ones (D→2), validated on Hénon–Heiles and the
di-hole in leg J, mirroring ansatz's `poincare.box_dimension` — is pointed at **quantum's QM detector-wall
experiment**. Quantum sent a double-slit interference pattern onto a wall with three absorbing masks along
y (uniform, periodic, a level-3 **Cantor set** at matched 8/27 coverage) and concluded, via JS-divergence
and fringe-correlation, that the boundary geometry co-decides where clicks land but "nothing
fractal-specific" is manufactured. The bridge adds the axis quantum never used — **fractal dimension** —
and confirms that verdict quantitatively. Read-only from quantum (Cantor geometry reconstructed
analytically; the wave sim **reimplemented** in the bridge's own code, not imported).*

## Result in one line

The bridge's GR-born box-dim estimator, applied cold to a quantum-mechanics experiment, recovers the Cantor
boundary's **exact fractal dimension** `D = log2/log3 = 0.6309` and the solid wall's `D = 1.0` (V1);
**separates** the Cantor wall from the periodic wall at *identical* 8/27 coverage — a dimensional axis
quantum's JS-divergence could not name (V2); and an **independent reimplementation** of quantum's wave sim
reproduces its gating and fringe-integrity numbers *to two decimals* while showing the Cantor detection
support **inherits** the boundary's sub-integer dimension rather than manufacturing an integer one (V3).

## V1 — the instrument reads dimension correctly in a new domain

| object | measured D | expected |
|---|---|---|
| analytic Cantor set (grids 3,9,27,81; counts 2,4,8,16) | **0.6309** | log2/log3 = 0.63093 |
| uniform (solid) wall | **1.0000** | 1.0 |

The same `log N(G) / log G` slope the bridge runs on Poincaré sections recovers the exact fractal dimension
of quantum's Cantor boundary — validated independent of its GR origin.

## V2 — the dimensional discriminator quantum did not use

At the matched coverage (8/27 ≈ 0.296) quantum built specifically to isolate geometry from coverage, the
bridge's box-dim over the self-similar band (grids 3,9,27; cell 108→36→12 ≥ the 12-cell finest segment):

| wall | D | local per-octave slopes | slope std |
|---|---|---|---|
| **cantor** | **0.6309** | [0.631, 0.631] | **0.000** (scale-invariant) |
| **periodic** | 0.7325 | [1.000, 0.465] | 0.268 (drifts) |

The fitted-D separation (0.102) is real but modest; the **crisp** signature is scale-invariance — the
Cantor wall has a *constant* log-log slope across octaves (the definition of a fractal), while the periodic
wall's slope drifts from 1.0 (resolving solid intervals) to 0.47 (coarse gaps). Two walls quantum could
only tell apart by *how much* their click distributions differ (JS-divergence) are here told apart by *what
kind of set they are* — an independent, complementary axis.

## V3 — the QM cross-check: gating reproduced, dimension inherited not manufactured

An independent reimplementation of quantum's 2-D Schrödinger double-slit + detector-wall sim (480×324, 9000
steps) reproduces quantum's own numbers:

| quantity | bridge (this leg) | quantum (`fractal_boundary.py`) |
|---|---|---|
| JS-divergence vs uniform, periodic | 0.342 | 0.34 |
| JS-divergence vs uniform, cantor | 0.438 | 0.44 |
| corr(detected, incident×mask): uniform / periodic / cantor | 0.966 / 0.858 / 0.917 | 0.97 / 0.86–0.92 |

Two deliberately-separate codebases agree on the QM experiment to two decimals — a reproduction cross-check
in its own right. Then the new axis: the **Cantor detection support** has `D = 0.6309` — the mask's
dimension, *not* blurred up toward 1.0 by the dynamics. This makes quantum's qualitative "gated, not
fractal-manufactured" verdict quantitative: the wave **inherits** the boundary's fractal dimension and adds
none of its own.

## Honest limits (frozen in advance, V3 framing)

- **The detection support is a subset of the mask by construction** (clicks occur only in absorbing cells),
  so `D(detection) ≤ D(mask)` structurally; the *content* of V3 is (a) the two-decimal independent
  reproduction of quantum's gating/integrity, and (b) that the dynamics do **not** blur the support up
  toward D=1 — the sub-integer dimension survives.
- **Lattice sim, numerical diffraction.** The de Broglie wavelength `λ = 2π/k₀ ≈ 6.3` cells is comparable
  to the 12-cell finest Cantor segment, so the quantum probe images the fractal boundary only down to ~λ —
  a resolution floor. This is the QM instance of the bridge's recurring **"walls are instrument-relative"**
  theme (leg R; Phase-5 note): a fractal is resolved only above the probing instrument's scale. Framing,
  not a separately-gated measurement here.
- **Not a claim about continuum QM, real detectors, or extra dimensions** (per quantum's
  `PLAN_projections.md`). The result is a cross-repo triangulation of a proven boundary-gating effect with a
  quantitative dimension.

## Inputs (read-only) & artifacts

- quantum `qsim/fractal_boundary.py` + `PLAN_projections.md` — the experiment and its verdict (reconstructed
  + reimplemented, not imported).
- ansatz `scripts/poincare.py::box_dimension` — the estimator leg V mirrors in 1-D (also used in leg J).
- `code/fractal_boundary_dim.py` — the bridge's instrument + reimplemented sim + gates.
  `results/fractal_boundary_dim.json`.
