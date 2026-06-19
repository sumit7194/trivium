# Move F — Pre-registration: curvature or boundary? (isolating the driver of the bulk/edge effect)

*Frozen 2026-06-19. Sharpens Move E: our hyperbolic disk had BOTH curvature and a boundary, so we
never separated them. This 2×2 does.*

## The question

> Move E found a bulk/edge boundary: learned recovery of an exact distance degrades toward the
> "edge", and it appeared in curved spaces but not flat ones. But the hyperbolic disk confounds
> two things — it is **curved** AND it has a **boundary**. Is the effect driven by curvature, by
> the boundary, or by their combination?

## The 2×2 (same recovery harness in each)

|  | **boundary** | **no boundary** |
|---|---|---|
| **curved** | hyperbolic disk (Poincaré) | **sphere S²** (compact) |
| **flat** | flat disk (hard edge) | flat torus (periodic) |

In each space: sample points, give a net the **noisy extrinsic embedding coordinates** (noise
scaled to each space's coordinate spread), have it recover the **exact intrinsic geodesic distance
to a fixed reference**, and measure the relative recovery error in the **bulk** (mid-range
distance) vs the **edge** (far end of the distance range). Report edge/bulk.

- **hyperbolic** (curved −, boundary): `d_H(0,z) = 2·arctanh(r)`, sensitivity → ∞ at the boundary.
- **sphere** (curved +, NO boundary): `d_S(N,z) = arccos(z₃)`, bounded but sensitivity → ∞ at the
  poles/cut-locus.
- **flat disk** (flat, boundary): `d_E(0,z) = r`, sensitivity = 1 everywhere; boundary at `r=R`.
- **flat torus** (flat, NO boundary): toroidal distance; sensitivity = 1, periodic, no edge.

## Predictions (frozen)

- **H-curvature (the hypothesis):** the effect is driven by CURVATURE, not the boundary —
  - hyperbolic edge/bulk **> 1.5**, sphere edge/bulk **> 1.5** (curvature, with or without boundary);
  - flat disk edge/bulk **≤ 1.3**, flat torus edge/bulk **≤ 1.3** (flat, with or without boundary).
- **H-boundary (the alternative):** if instead flat-disk shows the effect (> 1.5) and the sphere
  does NOT (≤ 1.3), the driver is the BOUNDARY, not curvature — and Move E's "curvature" framing
  would be **corrected**.
- **Decision:** the cell that separates them is the **sphere** (curved, no boundary). If it shows
  the effect → curvature. The flat disk (flat, boundary) is the other discriminant: if it does NOT
  → boundary alone is insufficient.

## What outcomes mean (decided before running)

- **curved cells YES, flat cells NO** → it is curvature; Move E sharpened (the boundary was
  incidental). The mechanism: a curved space's exact distance has diverging sensitivity at the edge
  of its range; a flat one does not.
- **bounded cells YES, unbounded NO** → it is the boundary; Move E corrected to "boundary effect."
- **only hyperbolic YES** → it is the *combination* (curvature + a conformal boundary, i.e. metric
  divergence) — which is exactly what a black-hole horizon / AdS boundary is, a GR-relevant sharpening.

## Honest scope
Four toy geometries, one recovery harness; a clean isolation test, not a universal claim. The
"edge" is the far end of each distance range; noise is scaled per space for fair comparison.

## Deliverables
- `code/curvature_vs_boundary.py` — the four spaces + the shared recovery harness.
- `code/plot_cvb.py` — the 2×2 edge/bulk figure.
- `FINDINGS.md` — the 2×2 result and which of H-curvature / H-boundary / combination it supports.
