# S2 — Findings: the rest-buzz instrument reads a CURVED hidden manifold — the S³ tower is n(n+2), degeneracy (n+1)²

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier S — **rung 1 of the mathematical ladder** in [KK_EXTENSION_NOTES.md](../../KK_EXTENSION_NOTES.md).
Legs S (5D, one hidden loop) and U (6D hidden T² + axion) built the rest-buzz instrument on **flat** hidden
spaces. S2 asks whether it was a flat-space coincidence or a **method**.*

## Result in one line

**SURVIVES.** The instrument — unmodified in method — reads the curved tower. Measured buzz frequencies land
on `√(n(n+2))` to **0.42% worst-case** (0.02% in the ℓ≥1 sectors), every predicted level is present, the
levels are **ℓ-independent** for ℓ ≤ n and **absent** for ℓ > n, so the degeneracy count
`Σ_{ℓ=0}^{n}(2ℓ+1) = (n+1)²` is **measured, not asserted**. And the control bites: the S³ level **n=3
(m²=15) cannot be produced by any unit-radius flat T³** — 15 is not a sum of three squares.

## The gates

| gate | check | result |
|---|---|---|
| **S2a** | measured buzz = √(n(n+2)), n=1..6, ℓ=0..3 | worst rel. error **0.42%** (tol 1.5%); **no missing levels** — **PASS** |
| **S2b** | ℓ-independence (≤1%), n≥ℓ cutoff, count=(n+1)² | spread **0.34–0.41%**; cutoff holds; counts 4/9/16/25/36/49 — **PASS** |
| **S2c** | can a flat unit T³ make these levels? | **n=3 (m²=15): NO** — no three-square representation exists (exhaustive search) |
| **S2d** | buzz vs dense diagonalization of the same H | **0.055%** — consistent (instrument validation only, *not* a second route) |
| **A1 guard** | FD must be O(h²)-inexact | **0** levels matching to <1e-12 ✅ (no too-clean smell) |

### The measured tower

| n | √(n(n+2)) | ℓ=0 | ℓ=1 | ℓ=2 | ℓ=3 |
|---|---|---|---|---|---|
| 1 | 1.73205 | 1.7248 (0.42%) | 1.7311 (0.06%) | — | — |
| 2 | 2.82843 | 2.8169 (0.41%) | 2.8284 (0.00%) | 2.8285 (0.00%) | — |
| 3 | 3.87298 | 3.8598 (0.34%) | 3.8736 (0.02%) | 3.8737 (0.02%) | 3.8738 (0.02%) |
| 4 | 4.89898 | 4.8808 (0.37%) | 4.8978 (0.02%) | 4.8979 (0.02%) | 4.8981 (0.02%) |
| 5 | 5.91608 | 5.8959 (0.34%) | 5.9157 (0.01%) | 5.9159 (0.00%) | 5.9160 (0.00%) |
| 6 | 6.92820 | 6.9032 (0.36%) | 6.9276 (0.01%) | 6.9280 (0.00%) | 6.9284 (0.00%) |

The ℓ=0 column carries a **uniform ~0.36% bias** while ℓ≥1 sits at ~0.02%. That is not a physical breaking
of the degeneracy: ℓ=0 has no centrifugal barrier `ℓ(ℓ+1)/sin²χ`, so its modes reach the grid endpoints and
feel the discrete boundary placement (effective domain `π+h` rather than `π`) — an O(h) boundary effect that
the ℓ≥1 sectors are shielded from. The bias is *level-independent*, which is the signature of a boundary
artifact rather than a spectrum error. ℓ=0 also cleanly returns the **n=0 zero mode at m ≈ 0** — the
massless 4D field, present but not a rung of the massive tower.

## S2c — the curved/flat discriminator (the finding worth keeping)

| n | m²=n(n+2) | 3-square rep | flat unit T³? | r₃ (flat degen) | S³ degen (n+1)² |
|---|---|---|---|---|---|
| 1 | 3 | (1,1,1) | yes | 8 | 4 |
| 2 | 8 | (0,2,2) | yes | 12 | 9 |
| **3** | **15** | **NONE EXISTS** | **NO** | **0** | **16** |
| 4 | 24 | (2,2,4) | yes | 24 | 25 |
| 5 | 35 | (1,3,5) | yes | 48 | 36 |
| 6 | 48 | (4,4,4) | yes | 8 | 49 |

By exhaustive integer search (Legendre's `4^a(8b+7)` criterion **verified, not invoked**), **15 is not a sum
of three squares** — so the S³ level n=3 is a mass no unit-radius flat T³ can produce. The instrument is
reading *curvature*, not re-deriving a flat tower in disguise. The degeneracies separate the two even more
sharply: S³ gives the perfect squares `(n+1)² = 4,9,16,25,36,49` while the flat count `r₃` is erratic
(8, 12, 0, 24, 48, 8) — it even *drops* from 48 to 8 between consecutive levels.

**Honest bound on this control:** a *general* flat T³ has continuously tunable radii, so it can be made to
hit any single mass. The statement proved here is about the **unit-radius** T³ — the direct analogue of leg
U's unit T² — and, more robustly, about the **shape of the whole tower**: `n(n+2)` with quadratic degeneracy
growth is not the shape any flat torus produces. This connects S2 to the Tier-S spectral arc (S1's
isospectral 4-tori, K2's drums): here the tower *does* distinguish the geometry, because the two candidates
are curved-vs-flat rather than an isospectral pair.

## Two instrument catches (the discipline log)

Both first runs **failed**, and both failures were mine, not the postulate's — the R4 lesson again (the wall
was the wrong instrument). Logged, not hidden:

1. **Random-probe chi-square nulls.** The overlap `a(t) = Σ_k c_k² cos(ω_k t)` weights mode k by `c_k²` —
   a **1-dof chi-square** for a single random probe, hence near zero with appreciable probability. Levels
   n=3,7,8,9 vanished from the ℓ=1 sector while ℓ=2,3 showed them fine, and the matcher silently paired n=3
   with the n=4 peak, reporting a fake "26.5% error." **Fix:** average the power spectrum over 8 independent
   probes (the weight concentrates on its mean — changes weights, never frequencies), and report an absent
   level as **MISSING** rather than mismatching it to its neighbour. *A level cannot exist in one ℓ-sector
   and not another — that impossibility is what exposed the bug.*
2. **A negative eigenvalue disguised as silence.** The ℓ=0 sector returned **no peaks at all**. Cause: FD
   boundary placement puts the lowest eigenvalue of `H` just *below* 1 (≈0.993), so the pre-registered
   evolution `ü = −(H−1)u` gave that mode a small **negative** stiffness — exponential growth at rate ≈0.08,
   i.e. **e³² over T=400**, burying every real peak ~10¹⁴ below the leading ramp. ℓ≥1 was immune because its
   lowest eigenvalue is `(ℓ+1)² ≥ 4`. **Fix:** evolve `ü = −Hu` (positive definite, unconditionally stable)
   and convert with the substitution's own algebra `m² = ω² − 1`, which is stated in the frozen
   pre-registration. **This is a method-detail change, not a gate change** — all tolerances (1.5% / 1.0% /
   3%) stand exactly as frozen, and it is recorded here as a deviation rather than quietly absorbed.

Family pattern, now six deep: R2 constant-column, R3 exponent-window, R4 grid-vs-root-find, S2 ×2. Every one
was a *silent* failure mode — a wall that looked like a result. Feeds **G7** (walls are instrument-relative).

## What this does and does not establish

- **Establishes:** the rest-buzz instrument is a **method**, not a flat-space artifact. It reads any hidden
  manifold whose Laplacian is computable — legs S/U's generality claim survives its first curved test, and
  rung 1 of the (A) ladder is climbed with all of the leg-S/U discipline intact (frequencies measured from a
  time series, nothing injected; a real control; an A1 too-clean guard).
- **Does not establish anything new about physics.** `n(n+2)` is the textbook Laplace spectrum of S³
  (equivalently the SU(2) Casimir `4j(j+1)`, `n=2j`) with degeneracy `(n+1)²`. **Zero novelty is claimed.**
  The falsifiable content was entirely our instrument's reach.
- **Says nothing about our universe.** This is (A)-sense richness in `KK_EXTENSION_NOTES.md`'s terms. The
  (B) cliff — evidence at ~10¹⁶ GeV, and ~10⁵⁰⁰ consistent compactifications with no selector — is untouched
  and uncrossable by this or any simulation here. Richer and more consistent never upgrades to true.
- **S2d is not a second route.** Diagonalizing the same `H` validates that we *read the time series
  correctly*; it is the same physics input, so it earns no independence credit.

## Inputs & artifacts

`code/s2_s3_tower.py` (staggered-grid 1D reduction, multi-probe leapfrog rest-buzz, exhaustive three-square
search) · `results/s2_s3_tower.json`. Reduction: `ψ = R(χ)Y_ℓm`, `R = u/sinχ` ⇒
`H u = −u'' + ℓ(ℓ+1)/sin²χ · u = (λ+1)u`, N=300, ℓ=0..3, T=400, 8 probes. Bridge-solo; own code; read-only
from sisters; pure numpy. Extends [legS_kk_tower](../../legS_kk_tower) and
[legU_kk6_tower](../../legU_kk6_tower) from flat to curved hidden space.
