# Route 5 — neural discovery of hidden structure (the inverse route)

*Discussion note, 2026-07-24. Referenced from `KK_EXTENSION_NOTES.md`. Updated same-day with the round-8
falsification results (G2, K5), which sharpened this route's scope considerably.*

## What makes route 5 different

Of the five routes to the KK tower (legs S/U), four solve the **forward** problem: given the hidden
geometry, compute the shadows (ansatz proves, quantum/bridge/tabula-FDTD simulate). Route 5 — tabula's
neural discovery — runs **backwards**: shown *only* projections, never the metric, it must reconstruct the
hidden structure. Inverse problems are categorically harder (many machines produce similar output), so a
working inverse method is a statement that the output *contained* the machine.

## What it discovered (leg U five-route join, tabula §158)

1. **That hidden structure exists, and how many knobs:** bottleneck sweep knees at **K=3** for the
   three-moduli family (held-out R² 0.9967 → 0.9998 → 0.9997) and **K=1** for the twist-only family.
   Dimension counting by compression — the neural cousin of the count-triangle.
2. **What the knobs mean (disentanglement, not guaranteed):** the latents decode to the physical moduli
   (Φ₁, Φ₂, χ) at **r ≈ 0.97 each** — the natural coordinates, not a tangled mixture.
3. **The geometry of the space of geometries:** the behavioral metric reproduces the **hyperbolic
   SL(2,ℝ)/SO(2)** moduli geometry (cosine 0.9994 vs truth) and the **SL(2,ℤ)** modular identification
   (≤0.22%) — the structure ansatz §113 proved, read off shadows.

## Why it is the most extensible route

It is a **method, not a calculation** — "is there hidden structure, how much, what, shaped how?" — and the
question runs on any hidden geometry. The forward routes need the answer known in advance to check against;
the inverse route is the only one that could, in principle, be pointed at data whose answer nobody knows.
(It is also the only route that would read *real* data, had we any at the relevant scale — see
`KK_EXTENSION_NOTES.md` for why we don't.)

## The sting: least trustworthy of the five, by construction

Its power and its danger are the same property: it proposes structure freely, so it can propose structure
that isn't there. Known instances, all caught by the family's own discipline:
- tabula's **gauge-ill-posedness self-catch**: "the latent metric is hyperbolic" is not well-defined
  (latents are defined only up to reparametrization); the honest object is the behavioral sensitivity
  metric, hyperbolic only in the many-mode limit.
- round 8's **trajectory-indexing bug** briefly made both G2 adversaries read illegible — caught because a
  machine answer contradicted an independently derived one.

**Rule:** route 5 never stands alone. It is the *discover* half of discover→verify; its reach equals the
verification walking behind it.

## Round-8 update — the scope of route 5 is now a measured thing

Two falsifications sharpened what this route actually reads:

- **G2 (KILLED):** legibility does **not** track KY-integrability (the old 8/8 was a proxy forced by the
  catalog's type-D-vacuum homogeneity). Corrected claim: **legible ⟺ the invariant is
  polynomial-representable in the probe's basis.** So route 5's reader has a *basis*, and what it can
  discover is bounded by that basis — a transcendental invariant (Candidate B) is invisible to it. The
  open sharpening (drafted round-9 ask): does a log-augmented basis make B legible? "Representable" is
  instrument-relative, like every wall the family has measured.
- **K5 (KILLED):** a net distinguishes **isospectral** drums (0.76 position-blind / 0.98 modal) while the
  eigenvalue tower sits at chance — *recordings carry eigenfunction overlaps, not just spectra*. So route 5
  reads strictly **more** than the spectrum: the inverse route's data channel is richer than the forward
  routes' headline observable. This is why it could in principle distinguish hidden geometries that the
  mass tower alone cannot (see the Schiemann/4-torus item in `FALSIFICATION_V2.md`).

## The frontier

Every route-5 discovery so far has been of a **known** answer — calibration, not discovery. The real test
is pointing it at hidden structure where the answer is *not* known, with ansatz positioned to verify or
refute what it proposes. Candidates live in `FALSIFICATION_V2.md` (Tier S). Until then, route 5's honest
status: a calibrated instrument of striking reach, whose failure modes are documented and whose scope
(basis-representability) is now itself a measured, falsifiable statement.
