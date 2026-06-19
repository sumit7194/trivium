# Move E — Findings: do the bridge's meta-findings survive outside GR?

*Run 2026-06-19. Predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any probe.
The most ambitious leg — and an honest, qualified yes.*

## Result in one line

Both of the bridge's meta-findings reproduce in **non-GR curved spaces** (tabula's atlas domains —
the neural ring S¹ and the hyperbolic disk) and **vanish in matched flat controls** — so they are
facts about **learned-vs-exact structure on a curved space**, not about black holes. The
**bulk/edge boundary** is the robustly curvature-driven one (it *scales* monotonically with
curvature); the **legibility gap** is real and curvature-specific (16× the flat control) but
modest in size. The frozen *aggressive* effect-size thresholds were not all met; the directional
contrast and the scaling are the honest signal.

## The 2×2 (curved vs flat × the two meta-findings)

| meta-finding | curved domain | flat control | verdict |
|---|---|---|---|
| **Legibility gap** (Move C / leg 2) | S¹ ring: gap = **0.127** | line: gap = **0.008** | curvature-specific (**16×**), but modest |
| **Bulk/edge boundary** (Moves C, D) | hyperbolic: edge/bulk **2.32×** (at r_max→1) | Euclidean: **~0.5×** (flat) | curvature-driven, **scales** |

**The bulk/edge scaling (the strong result).** As the sampling reaches toward the curved edge, the
hyperbolic recovery degrades monotonically while the flat control stays flat:

| edge proximity r_max | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|
| hyperbolic edge/bulk | 0.78 | 0.95 | 1.26 | **2.32** |
| Euclidean (flat) | 0.47 | 0.43 | 0.45 | 0.55 |

The exact structure's edge (where the Poincaré metric `d d_H/dr = 2/(1−r²) → ∞`) is exactly where
the learned recovery fails — and the closer to it, the worse, monotonically. The flat space has no
such edge and the learned recovery is uniform. This is the same shape as Move D (the exact Carter
tensor dies at the deformation edge) and Move C (the Weyl invariant fails at the algebraically-
special edge) — now in a space with no black hole in it.

## What survived, and what is honest about it

- **The directional claim holds in both tests.** Each effect appears in the curved domain and is
  absent (legibility) or reversed (bulk/edge) in the flat control. The legibility gap is 16× larger
  on the circle than the line; the edge penalty is present on the disk and absent on the plane.
- **The bulk/edge boundary scales with curvature.** The edge/bulk error ratio grows 0.78 → 2.32 as
  the ideal boundary is approached, while the flat control is invariant. A scaling law, not a
  single contrast, is the strongest evidence the boundary is curvature-driven.
- **The legibility gap is real but modest, and *topological*.** It is 16× the flat control but only
  0.13 in absolute size, because a von Mises population code is largely linearly decodable — the
  non-legible part lives in the **coordinate seam** (the chart's edge). The κ-sweep makes this
  explicit: the gap *shrinks* as the bump sharpens (0.17 → 0.04 from κ=1→16), so it is driven by the
  closed *topology*, not the tuning width. (A nice through-line: the legibility gap lives at the
  edge of the coordinate chart — the two meta-findings may be one finding about edges.)
- **The frozen aggressive thresholds were not all met** (A1 gap>0.3, B1 edge≥3× at base params),
  reported honestly. A2 (flat no gap) and B2 (flat no edge) held; the curved effects are
  directionally clear and, for bulk/edge, cleanly scaling — but smaller than the steep thresholds
  guessed before any data.

## The bigger reading (appropriately qualified)

This is the leg with real headroom, and it delivers a **qualified** version of the big claim: the
bridge's two boundaries are **not about black holes** — they appear wherever a learned
representation meets an exact **curved** structure (a neural population's ring, a hierarchy's
hyperbolic disk) and disappear when the structure is flat. The bulk/edge boundary in particular is
a curvature-scaling phenomenon. So "a learned representation recovers an exact structure in the
bulk but loses it at the curved edge" is a statement about **curvature and learning**, of which the
GR results (Moves C, D) are one instance. The honest caveat: this is a **demonstration across two
curved domains with controls**, not a proof of universality, and the legibility-gap half is modest.

## Honest limits

- **Demonstration, not proof.** Two curved domains + two flat controls; the claim is "survives the
  first out-of-GR tests, with controls and a scaling law for bulk/edge," not "universal."
- **Frozen thresholds missed.** A1/B1 not met at base parameters; reported, not hidden. The
  directional + scaling evidence is what carries the conclusion.
- **Legibility gap is small.** It is curvature/topology-specific but modest; population codes are
  mostly linearly legible, with the gap at the seam. The bulk/edge boundary is the stronger half.
- **No new physics or ML.** Circular variables needing nonlinear decode and hyperbolic distance
  diverging at the boundary are both known; the contribution is showing the bridge's two GR
  boundaries are the *same phenomenon* in these non-GR curved spaces.

## Artifacts
- `code/curvature_universality.py` — both tests + flat controls + the κ and r_max curvature sweeps.
- `code/plot_universality.py` — the gap-vs-curvature and edge-scaling figure.
- `results/curvature_universality.json`, `legE_curvature_universality.png`.
