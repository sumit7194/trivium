# Move F — Findings: curvature or boundary? (an honest correction to Move E)

*Run 2026-06-19. Predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before running.
This leg **corrects** Move E's "curvature-driven" framing — and the correction is sharper and more
GR-relevant.*

## Result in one line

The bulk/edge effect needs **neither curvature alone nor a boundary alone** — only the **hyperbolic
disk**, the one space whose **metric diverges at the edge (a conformal boundary)**, shows it. The
sphere (curved, compact, no boundary) shows nothing; the flat disk (a hard boundary, finite metric)
shows nothing. So the driver is a **conformal / horizon-like boundary where the metric blows up** —
exactly what a black-hole horizon is — not curvature in general.

## The 2×2

| space | curvature | boundary | metric at edge | edge/bulk | effect |
|---|---|---|---|---|---|
| **hyperbolic** | curved (−) | yes | **diverges** (`d→∞`) | **3.81×** | ✅ |
| **sphere S²** | curved (+) | no | bounded (`d≤π`) | 0.49× | ✗ |
| **flat disk** | flat | yes | finite (`d=r`) | 0.78× | ✗ |
| **flat torus** | flat | no | finite | 0.51× | ✗ |

Only the hyperbolic cell fires. The absolute errors confirm it is real, not a relative-error
artifact: hyperbolic recovery error grows ~8× from bulk to edge (small coordinate noise → large
distance error, because `d d_H/dr = 2/(1−r²) → ∞`), while the sphere's absolute error is uniform
(its bounded metric is recoverable everywhere). See `results/legF_curvature_vs_boundary.png`.

## What this corrects, and why it's better

Move E concluded the bulk/edge boundary "tracks curvature." **Move F shows that was imprecise.**
The discriminating feature is not curvature (the sphere is curved and shows nothing) nor a boundary
(the flat disk has one and shows nothing) — it is the **metric diverging at a conformal boundary**.
Hyperbolic space is the only one of the four whose intrinsic distance is *unbounded*: its ideal
boundary at `|z|→1` is where the Poincaré metric blows up. That is precisely the structure of:
- a **black-hole horizon** (proper distance / tortoise coordinate diverges; the exponential
  near-horizon redshift — the same hyperbolic throat),
- an **AdS conformal boundary**,
- the **light-ring / QNM edge** of Move B (the near-horizon geometry).

So the honest, sharpened statement is: **a learned representation recovers an exact structure in the
bulk and loses it at a conformal boundary where the metric diverges.** This is a *better* connection
to GR than "curvature," because the GR "edge" (the horizon) is exactly a metric-divergence boundary,
not generic curvature.

## Verdict on the frozen predictions

- **H-curvature (curved cells fire, flat stay quiet): FALSE.** The sphere (curved, no boundary) did
  *not* fire (0.49×). Curvature alone is insufficient.
- **H-boundary (bounded cells fire): FALSE.** The flat disk (boundary) did *not* fire (0.78×). A
  boundary alone is insufficient.
- **The pre-registered "combination" outcome holds, sharpened:** only hyperbolic (curved *with a
  conformal boundary where the metric diverges*) fires. The mechanism is **metric divergence at a
  conformal boundary**, the GR-relevant reading.

## Honest limits and scope of the correction

- **This sharpens the bulk/edge-*recovery* finding specifically** (Move E test B, distance recovery
  from coordinates). The broader "edges" across the bridge (the algebraically-special Weyl edge of
  Move C, the integrability boundary of Move D) are *different* edge mechanisms — Move F does not
  claim they all reduce to metric divergence. The through-line "learned recovers the bulk, exact
  owns the edge" survives; the specific *cause* of the distance-recovery edge is now pinned to a
  conformal boundary.
- **Four toy geometries.** A hemisphere (positive curvature *with* a finite-metric boundary) would
  further confirm it is the divergence and not curvature+boundary generically; predicted: no effect.
- **No new physics or ML.** The contribution is an honest isolation that corrects and deepens the
  Move E claim.

## Artifacts
- `code/curvature_vs_boundary.py` — the four geometries + the shared recovery harness.
- `code/plot_cvb.py` — the 2×2 figure.
- `results/curvature_vs_boundary.json`, `legF_curvature_vs_boundary.png`.
