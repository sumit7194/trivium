# Move I — Findings: the edges are TWO kinds (recovery/resolution vs physical)

*Run 2026-06-20. A pre-registered prediction (I1) was **falsified**, and chasing why gave the correct,
richer taxonomy — and reconciled Moves F/G/H. Reported as it happened.*

## Result in one line

The bridge's "edges" are **not one mechanism**. There are two genuinely different kinds:
**recovery/resolution edges** (the exact structure *exists*; the exact closed-form owns it with zero
error, while finite-resolution learning fails at the diverging gradient, and noisy input defeats even
the exact form) and **physical edges** (the exact structure *ceases to exist*; nothing owns it because
there is nothing there). My prediction that the divergence edge would simply *vanish* at perfect
observation was **wrong** — it is resolution-limited, not purely noise — and that correction is the
finding.

## I1 — FALSIFIED as stated, and what it taught

Prediction: the F/H divergence-recovery edge would vanish (edge/bulk ≤ 1.3) at σ→0. **It did not:**
edge/bulk = **5.69× at σ=0** (and is *larger* at σ=0 than at σ=1e-2, because at σ=0 the bulk error is
tiny). So the edge is **not** purely observation noise (Move H's reading was incomplete). Chasing it:

| at σ=0, N = | 4k | 16k | 64k | 256k | exact closed-form |
|---|---|---|---|---|---|
| edge/bulk | 6.96× | 7.26× | 4.87× | 3.80× | **0 (no edge)** |

The edge **shrinks with data** (slowly) and the **exact closed-form `d=2·arctanh(r)` has zero error
everywhere**. So it is a **resolution/precision** edge: the diverging gradient makes the structure hard
to *resolve* by finite-resolution learning (you need ever more data near the boundary), while the exact
computation gets it for free. **The exact closed-form owns this edge; learning fails it.**

## I2 — held: D is a physical edge

On **clean** geodesics (the perfect-observation limit), the approximate-invariant var-ratio is the
integration-noise floor at ε=0 (2.6e-18) but rises to **1.3e-2 by ε=0.08** — **5×10¹⁵× the floor** —
and keeps climbing. This is not observation: the deformed torus *genuinely admits no low-degree
invariant* for ε>0. The structure is **gone**, and the exact oracle correctly reports its absence.

## The taxonomy (the result), and how it reconciles F/G/H

Two kinds of edge, and the difference is whether the exact structure **exists**:

| | exact structure | exact closed-form (exact input) | learning (finite resolution) | noisy input |
|---|---|---|---|---|
| **recovery/resolution edge** (F/H, C) | exists | **owns it** (0 error) | fails (diverging gradient / vanishing signal) | defeats even the exact form (Move H) |
| **physical edge** (D) | absent (ε>0) | finds nothing (correct) | finds nothing (correct) | — |

This reconciles the earlier moves into one coherent statement:
- **"Exact owns the edge" is TRUE for recovery edges with exact input** (Move I: the closed-form is
  exact everywhere; learning fails at the diverging gradient). Moves A, B are this case — ansatz
  computes from the exact metric, no resolution/noise limit.
- **Move H's "neither owns the edge" was specifically the NOISY-input case** — correct there: noisy
  position defeats even the exact closed-form. It does not generalize to exact input.
- **Physical edges (D) are a different thing entirely** — the structure is gone; "owns" doesn't apply.

So Move H slightly *over-generalized* ("noisy-recovery → exact doesn't own the edge"); Move I restores
the exact-input case and adds the precise taxonomy. The honest synthesis is now three statements (next
section).

## The synthesis, in its final honest form

1. **Recovery/resolution edges** (where the metric/distance diverges or a signal vanishes — F/H/C):
   the exact structure exists; the **exact closed-form owns the edge**, finite-resolution learning
   fails there (shrinking only slowly with data), and **observation noise defeats even the exact form**.
2. **Physical edges** (where the exact structure genuinely changes — D's integrability loss): the
   structure is **absent** for ε>0; no method recovers what is not there.
3. **Direct-exact tasks** (A, B): no recovery, no resolution/noise limit — exact is precise everywhere.

## Honest limits
- Two cases tested decisively (F/H, D); C classified by argument (vanishing-signal recovery edge).
- The F/H resolution edge shrinks slowly with data (3.8× at 256k); "vanishes only in the
  infinite-data + exact-input limit", not at any finite budget — reported, not rounded to "vanishes".
- The taxonomy is a property of these phenomena; whether *every* edge in physics falls into exactly
  these two kinds is not claimed.

## Artifacts
- `code/edge_taxonomy.py` — the F/H noise sweep + the D noise-floor analysis (+ the inline data-size
  sweep that diagnosed I1).
- `results/edge_taxonomy.json`.
