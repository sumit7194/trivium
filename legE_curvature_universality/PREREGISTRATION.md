# Move E — Pre-registration: do the bridge's meta-findings survive outside GR?

*Frozen 2026-06-19, before any probe is trained. Discipline: THE_BRIDGE.md §2, §6 (the
cross-domain / curvature-atlas lens). The most ambitious leg: it tests whether two findings that
look like facts about black holes are really facts about **learned-vs-exact structure on a curved
space**.*

## The claim under test

The bridge produced two meta-findings about where a *learned* representation meets an *exact*
structure:
1. **The legibility gap** (Move C, leg 2): an exact quantity can be *present* in observations yet
   *not linearly legible* — only nonlinearly recoverable.
2. **The bulk/edge boundary** (Moves C, D): a learned representation recovers the exact structure
   *in the bulk* but fails *at a sharp edge*, which only the exact construction owns.

> **Hypothesis:** these are not GR-specific. If they track *curvature* — appearing wherever a
> learned representation meets an exact **curved** structure, and **vanishing in a flat control** —
> then they are facts about learned-vs-exact structure, not about black holes. We test this in two
> non-GR curved domains from tabula's own curvature atlas (the neural ring S¹, the hyperbolic
> hierarchy), each against its flat control.

## Test A — the legibility gap vs curvature (S¹ vs a flat line)

- **Curved (S¹, tabula `90_neural_ring`).** A hidden heading `θ ∈ S¹`; `N` neurons with von Mises
  tuning `a_i = exp(κ·cos(θ−φ_i))` + noise. The exact structure is the manifold coordinate `θ`.
  Recover `θ` from the population activity: **linear (Ridge)** vs **nonlinear (kNN/MLP)**, circular
  R² (residual wrapped to [−π,π]).
- **Flat control (a line).** A hidden `x ∈ [0,L]`; `N` neurons with Gaussian tuning
  `a_i = exp(−(x−c_i)²/2σ²)` + noise. Recover `x`: linear vs nonlinear, R².

The von Mises ring is the same encoding on a *closed/curved* latent; the Gaussian line is the
*flat/open* control.

## Test B — the bulk/edge boundary vs curvature (hyperbolic vs Euclidean)

- **Curved (hyperbolic, tabula `89_hierarchy_hyperbolic`).** Points `z` in the Poincaré disk at
  radii `r = |z| ∈ [0, 0.95]`; the exact structure is the hyperbolic distance to the origin
  `d_H(0,z) = 2·arctanh(r)`, which **diverges as r→1**. The net sees the (flat) Euclidean
  coordinates with fixed observation noise and learns `d_H`. Measure relative recovery error vs
  radius: **bulk** (r<0.5) vs **edge** (r>0.85).
- **Flat control (Euclidean).** Same points; the exact structure is `d_E(0,z)=r` (no divergence).
  Learn `d_E` from noisy coordinates; relative error vs radius.

Fixed-precision observations make the curved edge ill-conditioned (`d d_H/dr = 2/(1−r²) → ∞`); the
flat structure has no such edge.

## Predictions (frozen)

- **A1 (curved S¹): legibility gap PRESENT.** nonlinear − linear circular-R² for `θ` > **0.3**.
- **A2 (flat line): legibility gap ABSENT.** nonlinear − linear R² for `x` < **0.1**.
- **B1 (curved hyperbolic): bulk/edge boundary PRESENT.** edge relative error ≥ **3×** bulk error.
- **B2 (flat Euclidean): bulk/edge boundary ABSENT.** edge error ≤ **1.5×** bulk error.
- **Headline (the claim).** Both meta-findings reproduce in the curved domains (A1, B1) and vanish
  in the flat controls (A2, B2) → they track *curvature*, not GR: facts about learned-vs-exact
  structure on a curved space.

## Agreement criterion (frozen)

The leg **supports the bigger reading** iff A1∧A2∧B1∧B2 all hold — the boundaries appear with
curvature and disappear without it, in domains that have nothing to do with black holes. Any cell
failing is a finding (e.g. if the flat control *also* shows the gap, the effect is not curvature).

## Honest scope (per §7)

- **A demonstration, not a proof of universality.** Two curved domains + two flat controls support
  the reading "these are about curved learned-vs-exact structure." They do not prove it holds for
  *all* such structures. The claim is "survives the first out-of-GR tests, with controls," not
  "universal law."
- **Tabula's own atlas rows.** S¹ (`90`) and hyperbolic (`89`) are tabula's curvature-atlas
  domains, so this is a genuine cross-domain test, not a contrived one. The flat controls are the
  matched no-curvature cases.
- **No new physics, and no new ML.** Circular variables needing nonlinear decode, and hyperbolic
  distance diverging at the ideal boundary, are both known. The contribution is showing the
  bridge's two boundaries are *the same phenomenon* in GR and in these non-GR curved spaces.

## Deliverables
- `code/curvature_universality.py` — both tests + flat controls (self-contained, tabula venv).
- `code/plot_universality.py` — the gap-vs-curvature and edge-vs-curvature figure.
- `FINDINGS.md` — the 2×2 table (curved/flat × legibility/bulk-edge), the verdict, honest limits.
