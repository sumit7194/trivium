# Move C — Findings: the coordinate-free invariant cross-measure

*Run 2026-06-19. Metrics, observation construction, probe ladder, and predictions frozen in
[PREREGISTRATION.md](PREREGISTRATION.md) before any probe was trained. A **mixed result**,
reported honestly: the legibility half succeeds cleanly, the fine-discrimination half does not.*

## Result in one line

Ansatz's **coordinate-free Weyl invariant is present in the frame-randomized tidal field** and a
capable net recovers its **magnitude** (MLP R² = 0.96) — but **not linearly** (linear R² = 0.02),
the legibility gap the leg set out to find. Where it stops: the net does **not** robustly recover
the **fine structure** — the exact Petrov O/D boundary (best 0.75, not >0.95) and the rank-ordering
across three decades (Spearman 0.56) — which is precisely where ansatz's *exact* coordinate-free
construction is irreplaceable.

## The numbers

Tidal field `E_ij = R_{0i0j}` computed from each exact metric (Schwarzschild/de Sitter gated to
machine precision), **rotated by a random SO(3) frame** at every sample, probed against ansatz's
exact labels. Split by metric instance (anti-leakage).

| | linear (Ridge) | nonlinear (kNN) | nonlinear (MLP) | invariant-feature ceiling |
|---|---|---|---|---|
| **Weyl magnitude recovery, R²** | **0.02** | 0.68 | **0.96** | 0.999 |
| **Petrov O/D, accuracy** (threshold the recovered invariant) | 0.46 | — | **0.63** | 0.75 |

Spearman(best-nonlinear, truth) = 0.56.

| prediction | result |
|---|---|
| **P1** — nonlinear R² > 0.9 | ✅ (MLP 0.96) |
| **P2** — legibility gap (nonlinear − linear) > 0.3 | ✅ (gap **0.94**) |
| **P3** — O/D accuracy > 0.95 | ❌ (best 0.75) |
| **P4** — Spearman > 0.9 | ❌ (0.56) |

## What this means (both halves honestly)

**The clean win — the legibility gap (P1, P2).** The coordinate-free Weyl magnitude `tr(Ẽ²)` is a
*quadratic, rotation-invariant* function of the tidal components. A **linear** probe on the
frame-randomized components cannot form it (R² = 0.02 — the random frame scrambles the linear
readout); a **nonlinear** net recovers it (MLP R² = 0.96), and the invariant-feature ceiling
confirms it is fully there (0.999). This is exactly the leg-2 legibility lens applied to a
*deductive* invariant: ansatz's coordinate-free quantity is **information-present but not linearly
legible** from the frame-dependent observation, and learning the rotation-invariant structure is
what unlocks it. The de Sitter case sharpens it — de Sitter has large curvature (Kretschmann ≠ 0)
but **zero Weyl** (conformally flat), so the net cannot cheat off curvature magnitude; it must
isolate the traceless Weyl part, and the MLP does.

**The honest limit — the fine Petrov boundary (P3, P4).** The recovery is good *in the large* but
not *at the edge*. The Weyl magnitude spans three decades (a weakly-curved black hole far from its
horizon has `tr(Ẽ²) → 0`, approaching de Sitter's exact zero), and R² is dominated by the large
values — so the net nails the scale (R² 0.96) while mis-ranking the small ones (Spearman 0.56) and
failing to cleanly separate near-conformally-flat type-D from type-O (O/D accuracy 0.75, even from
the near-perfect-regression ceiling). The exact Petrov classification lives in that small-Weyl
limit, and that is where the *inductive* oracle's learned representation runs out and the
*deductive* oracle's exact algebraic construction (§57 `petrov`, §76 `invariant_fingerprint`) is
the only thing that gets it right.

## The cross-measure verdict

A genuine, bounded cross-measure: the learned representation and the exact engine **agree on the
gross coordinate-free invariant** (a net recovers ansatz's Weyl magnitude from frame-randomized
observations, non-linearly), and **part ways at the algebraically-special boundary** (the exact
Petrov type, the conformally-flat edge), which only the exact construction resolves. That boundary
— where the approximate, learned invariant degrades and the exact one is required — is the same
shape of finding as Move D's hierarchy: the inductive oracle captures the structure until the
sharp edge, and the deductive oracle owns the edge.

## Honest limits

- **Mixed result, reported as such.** P1/P2 pass, P3/P4 fail; the leg does not fully meet its
  frozen success criterion. The legibility-gap result is the clean, robust finding; the
  fine-boundary failure is itself informative, not hidden.
- **O vs D, static observers.** Richer Petrov types (I, N) and the magnetic Weyl (frame-dragging)
  are out of scope; a non-spherical vacuum metric (Zipoy–Voorhees) would extend the class set.
- **Heavy-tailed target.** The Weyl magnitude's three-decade range is what splits R² (high) from
  Spearman (low); a fixed-SNR or log-scaled design would change the fine-recovery numbers but not
  the qualitative split (gross recovered, edge not).
- **No new physics.** Tidal fields, Petrov classification, and curvature invariants are textbook;
  the contribution is locating, through the project's own legibility lens, exactly where a learned
  representation recovers an exact coordinate-free invariant and where it cannot.

## Artifacts
- `code/tidal_observations.py` — ansatz side: numeric tidal tensor from each exact metric
  (gated), frame-randomized; ansatz exact Kretschmann / Weyl-magnitude / Petrov labels.
- `code/probe_invariants.py` — tabula side: the linear / nonlinear (kNN, MLP) / invariant-feature
  probe ladder; O/D via thresholding the recovered invariant.
- `code/plot_crossmeasure.py` — the legibility-ladder figure.
- `results/tidal_observations.json`, `probe_invariants.json`, `legC_invariant_crossmeasure.png`.
