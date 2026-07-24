# S3 — Findings: identical mass towers, different vertices — postulate SUPPORTED, but my frozen gate was unreachable

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier S — the item that **unifies the drums arc in field-theory language**: K2 (KILLED — isospectral drums,
the tower does not determine the geometry) + K5 (KILLED — a net separates them anyway, because *a recording
is the spectrum weighted by eigenfunction overlaps*), stated as one KK compactification.*

## Verdict in one line

**UNDECIDED (gate mis-specified) — with the postulate SUPPORTED and KILLED definitively excluded.** The two
compactifications have **identical mass towers** (δ_spec → 0 monotonically) and **genuinely different cubic
couplings** (δ_coup → a nonzero limit of **+2.14%**, against a congruent-mirror null that extrapolates to
**+0.007%**, i.e. zero). But **one of my three frozen conditions — `δ_coup > 10·δ_spec` — was unreachable by
construction**, and I do not get to retroactively declare a pass. The result is recorded at the honest bar.

## The setting

A massless scalar on `ℝ^{1,3} × D` with Dirichlet walls, `D` a GWW drum. With `Φ(x,y) = Σ_k φ_k(x) ψ_k(y)`
and `−Δ_D ψ_k = λ_k ψ_k`:

> **masses `m_k² = λ_k`** — an eigen**value** quantity ⇒ *identical* for the pair (GWW)
> **vertices `g_{ijk} = ∫_D ψ_i ψ_j ψ_k`** — an eigen**function** quantity ⇒ *different*

Observable: `G(M) = Σ_{i,j,k ≤ M} g_{ijk}²`, the squared Frobenius norm of the truncated cubic coupling
tensor — invariant under eigenvector sign flips *and* within-multiplet rotations. `M = 8` at every
resolution, placed at a genuine spectral gap by the frozen rule.

## The data

| n | cells | δ_spec (tower) | δ_coup **GWW** | δ_coup **null** (mirror) | GWW/null |
|---|---|---|---|---|---|
| 16 | 904 / 888 | 5.236% | 0.090% | 2.388% | 0.04× |
| 32 | 3600 / 3568 | 2.657% | 1.014% | 1.229% | 0.82× |
| 48 | 8088 / 8040 | 1.779% | 1.388% | 0.825% | 1.68× |
| 64 | 14368 / 14304 | 1.336% | 1.575% | 0.621% | 2.54× |
| 96 | 32304 / 32208 | 0.892% | 1.762% | 0.414% | 4.25× |
| **128** | 57408 / 57280 | **0.670%** | **1.856%** | **0.311%** | **5.97×** |
| **h→0** | — | → 0 | **+2.137%** | **+0.007%** | → ∞ |

Three monotone trends, in opposite directions, is the whole result:

- **δ_spec falls** (5.24% → 0.67%, monotone) — the drums *are* isospectral. K2 reproduced inside the KK
  setting. **S3a PASS.**
- **The null's δ_coup falls**, and falls as a clean `∝ h`: `δ_coup·n = 39.3, 39.6, 39.7, 39.8, 39.8` across
  n=32…128 — pure discretisation error, extrapolating to **+0.007%**. A congruent copy has the same
  couplings, as it must. **S3c PASS** (0.311% < 1.856%/5 = 0.371%).
- **The GWW δ_coup RISES** (0.09% → 1.86%) and plateaus, extrapolating to **+2.14%**. It is converging *to a
  nonzero value*, which is precisely what a physical difference looks like against a vanishing artifact.

That the null extrapolates to 0.007% — three orders below the GWW limit — is the instrument certifying
itself. **A1 too-clean guard: no ~exact agreements; K2's connectivity assertion inherited and never fired.**

## Why the verdict is not "TRUE" — my error, stated plainly

S3b had two conditions. The second (**δ_coup persists, does not converge away**) **passes decisively**. The
first (**δ_coup > 10·δ_spec**) **fails**: 2.8× at n=128.

It fails because I chose it badly at freeze time. It compares a quantity converging **to zero** (δ_spec, an
artifact measure) against one converging **to ~2%** (δ_coup, the signal), so the ratio can only grow as fast
as `1/δ_spec`. And K2 had *already documented* that δ_spec is staircase-boundary limited to `≈h^0.97` — the
drums' 45° edges cannot be resolved by a square grid better than O(h). Reaching 10× therefore needs
`δ_spec < 0.19%`, i.e. **n ≈ 450** (a ~1350² grid, ~700k cells) — not reachable with this dense FD, and
knowable as unreachable *before* I froze it, from K2's own findings. That is a pre-registration error, not a
result, and it is recorded as one.

**The correct gate is the one S3c already implements:** compare `δ_coup(GWW)` against `δ_coup(null)` — the
*same* observable computed by the *same* machinery on a congruent pair, so the discretisation error cancels
in the comparison instead of being estimated by a different quantity with a different convergence rate.
Apples to apples. By that gate the postulate passes at n≥96 and passes overwhelmingly in the h→0 limit
(2.137% vs 0.007%).

**Re-registered for a future S3′** (frozen here, not run): drop the `10·δ_spec` condition; require
(i) `δ_coup(GWW) > 5·δ_coup(null)` at the two finest grids, and (ii) the h→0 linear extrapolations to
separate — GWW bounded away from zero, null consistent with zero. Both already hold; running S3′ would be
re-reading data I have, so **the honest label for what was actually pre-registered stays UNDECIDED**, and
S3′ is left as a genuinely fresh future gate rather than a same-day relabel.

## What is nonetheless established

**KILLED is definitively excluded.** The pre-registration's kill condition was "δ_coup shrinks with
resolution like δ_spec does, i.e. the couplings agree too." δ_coup does the *opposite* — it grows
monotonically to a nonzero plateau while the null shrinks to zero. There is no reading of this data in which
the two compactifications are locally indistinguishable at cubic order.

So the physics content of the drums arc closes as intended, at the strength the data support:

> Two Kaluza–Klein compactifications on the GWW drums give 4D field theories whose **particles have exactly
> the same masses** and whose **cubic vertices differ by ~2%**. The mass tower cannot tell them apart; a
> scattering amplitude can.

This is K5's mechanism — *identical eigenvalues, different eigenfunctions; a projection samples the
eigenfunctions* — restated as a field-theory observable, and K2's kill given its physical consequence: what
the spectrum loses, the interactions retain.

## Honest scope

- **A toy compactification.** A Dirichlet drum is not a smooth closed internal manifold and a free scalar
  with a `Φ³` vertex is not a realistic KK theory. The reduction is exact *as stated*; nothing here is a
  claim about real extra dimensions. The (B) cliff of `KK_EXTENSION_NOTES.md` is untouched.
- **Zero novelty.** Isospectral-but-not-isometric domains having different eigenfunctions is the content of
  GWW / Sunada transplantation; KK couplings being eigenfunction overlap integrals is textbook dimensional
  reduction. The bridge's contribution is **the join** — K2's and K5's kills as one falsifiable field-theory
  sentence — plus the convergence control that separates a physical difference from discretisation error,
  which is the part that is easy to overclaim.
- **The ~2.14% figure is instrument-specific**, not a universal constant: it is `G(8)`'s relative difference
  for this drum pair with this normalization and this truncation. The robust statement is *nonzero vs zero*,
  not the number.
- Inherits K2's **corrected** build — distinct grid offsets and the connectivity assertion, from the bug
  tabula caught (equal offsets disconnected each drum into 3 congruent pieces, making the two discrete
  operators one matrix relabelled). S3d re-checks it every run.

## The discipline log

- **A verdict-logic bug, caught before it was believed.** The first version of the verdict mapping had an
  `else` branch that printed **"KILLED — the couplings agree too"** for exactly this gate combination
  (S3a ✅, S3b ❌, S3c ✅) — a label flatly contradicted by the same run's numbers. Fixed to branch on the
  actual kill condition (`not persists`). *A verdict string is a claim and must be derived from the
  condition it names, not from falling off the end of an if-chain.*
- **The first run stopped at n≤64** and read UNDECIDED(numerics) with the null (0.62%) too close to the GWW
  gap (1.58%). Extending to n=96,128 — an instrument improvement, no gate touched — separated them. The
  trends were already visible at n≤64 (null falling, GWW rising) but were **not** treated as sufficient.

Family pattern, now seven deep: R2 constant-column · R3 exponent-window · R4 grid-vs-root-find · S2 ×2 ·
S3 ×2. Feeds **G7** (walls are instrument-relative) — and S3 adds a new species: *the wall was my own
pre-registered threshold*, not the instrument.

## Inputs & artifacts

`code/s3_drum_kk.py` (KK reduction, cubic overlap tensor, congruence null, h→0 extrapolation) ·
`results/s3_drum_kk.json`. Imports the bridge's own [K2 build](../K2_isospectral_drums/code/k2_drums.py).
Closes the arc with [K2](../K2_isospectral_drums) (same tower) and [K5](../K5_drum_learnability) (locals
leak); companion to [S1](../S1_schiemann_tori) (flat 4-tori not spectrally determined) and
[S2](../S2_s3_tower) (the instrument reads curved hidden spaces). Bridge-solo; numpy/scipy.
