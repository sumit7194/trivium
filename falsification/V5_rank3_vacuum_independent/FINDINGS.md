# V5 — FINDINGS: the fleet's rank-3 vacuum object checks out, by a route independent of ansatz

**Verdict: the rank-3 Killing tensor F on the 4D Lorentzian vacuum pp-wave (`high_rank_killing` EXP-002,
`9384d7f`) is IRREDUCIBLE IN THE POLYNOMIAL SENSE — confirmed by bridge code that imports nothing from any
sibling.** One gate failed as registered and was re-run under a stronger, post-failure instrument. That is
recorded, not smoothed over.

| gate | result | control |
|---|---|---|
| V5a signature (1,3) | **PASS** — one negative eigenvalue | — |
| V5b Ricci-flat | **PASS** — R_ab ≡ 0 symbolically | poison-b (non-harmonic g_tt) is non-flat ✓ |
| V5c {H,F} = 0 | **PASS** — symbolically | poison-c (one sign flipped) gives a nonzero bracket ✓ |
| V5d pure part ≠ 0 | **PASS** — F at p_t=p_s=0 = (p_ξ²+p_η²)(ηp_ξ−ξp_η)/(32ρ²) | — |
| V5e dim K1 = 2, 1st-order jet count | **FAILED as registered** — upper bound 6 | ∂_t, ∂_s in kernel ✓ · flat space → 10 ✓ |
| V5e′ dim K1 = 2, 2nd-order jet count *(post-failure)* | **PASS** — upper bound 2, lower bound 2 | ∂_t, ∂_s in kernel ✓ · flat space → 10 ✓ |

**The argument.** Rank 3 splits only as 1+2 or 1+1+1, so every reducible rank-3 Killing tensor carries a
rank-1 factor. With K1 = span{∂_t, ∂_s} (V5e′), every reducible tensor vanishes at p_t = p_s = 0. F does not
(V5d). So F is not in the span of reducible tensors.

## The V5e failure, and a defect in this repo's own pre-registration

The first-order count returned 6 — an upper bound that isn't tight on a pp-wave, whose curvature is null
and highly degenerate. The kill condition I had frozen said "more than 2 kills the argument," which
**confused "the bound isn't tight" with "the claim is false."** The verdict stayed FAILED. The stronger
count was registered as a new check, **labelled post-failure, before it ran** — the same standard the
bridge held quantum to on 2026-09-23 (A4 §8j). It passed, and it is graded as weaker evidence than a
first-time pass.

## Scope — what this does and does not establish

- **Established:** polynomial irreducibility, vacuum, (1,3) signature, conservation — by an independent route.
- **One relayed input:** the metric and F were taken from `high_rank_killing` WRITEUP §2. Everything else
  was re-derived. Had they been mis-transcribed, this check would be of a *different* object — but a
  different object that is still a Lorentzian vacuum with a conserved, polynomially irreducible rank-3
  tensor, so the kind of claim R-1 needs survives regardless.
- **Not re-checked:** functional dependence, the 5D companion, the KK reading, and the "exactly one
  irreducible direction" count (ansatz-scoped, per its author).
- **Still AI checking AI.** An independent code route is not a human expert. This object is the fleet's
  best candidate for an outside reader (FLEET_PLAN H-5).

## What it changes

The bridge's **B-1 (scored ~3%) was already done**, 18 days before it was listed, in the polynomial sense.
G-3 is killed by construction *inside the fleet*. The open moonshot becomes the **functionally independent**
version (H-2).
