# S1 — Findings: flat 4-tori are NOT spectrally determined (KILLED, exact)

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier S — the KK-tower punchline of the K2/K5 drums arc, lifted from 2D membranes to real compactification
geometry (flat 4-tori, no boundary). Pure exact integer arithmetic. Source: Cerviño–Hein arXiv:0910.2127,
Schiemann's instance (a,b,c,d)=(1,7,13,19).*

## Result in one line

**Two non-isometric flat 4-tori have identical Laplace spectra — hence identical KK mass towers.** The
Schiemann/Conway–Sloane lattices L₁, L₂ (index-9 sublattices, D = diag(1,7,13,19)) share their theta series
**exactly** across all 14 occupied shells to norm 400 (det = 35 852 544 for both) — **S1a PASS** — while
their degree-2 Siegel theta **differs**, first at bucket (‖u‖²,‖v‖²,u·v) = **(48, 96, −24)**: L₁ has **0**
such ordered pairs, L₂ has **4** — **S1b PASS**, a rigorous non-isometry witness. **The KK mass tower does
not determine the hidden T⁴ in dimension ≥ 4.**

## The gates

| gate | check | result |
|---|---|---|
| S1a | theta(L₁) = theta(L₂) for every norm ≤ 400, and det G₁ = det G₂ | **PASS** — 0 mismatches / 14 shells; det 35852544 both |
| S1b | degree-2 Siegel theta differs (a differing 2×2-Gram bucket) | **PASS** — bucket (48,96,−24): 0 vs 4 (3049 differing buckets total) |

The Gram matrices (exact, from the verbatim generators):
```
G1 = [[96,48,72,276],[48,192,492,528],[72,492,1728,1368],[276,528,1368,1728]]
G2 = [[96,144,24,276],[144,1728,492,1584],[24,492,192,456],[276,1584,456,1728]]
```
Minimal norm 48 (both, multiplicity 2); the towers agree shell-by-shell, but the *relationship* between the
norm-48 and norm-96 vectors differs — L₂ has four ordered (48,96)-pairs at inner product −24, L₁ none. That
single bucket is enough: an isometry is a bijection preserving all pairwise inner products, so a differing
degree-2 Siegel coefficient proves non-isometry **exactly**, not numerically.

## leg-W / leg-Z discipline

The generators were transcribed from the primary PDF (Cerviño–Hein p.4), the exact failure mode from leg W.
Two guards held: (a) **self-validation** — a mis-transcribed generator would break S1a (the towers would
disagree); they agree across all 14 shells, certifying the transcription *and* the isospectrality at once;
(b) **det G₁ = det G₂** as an independent consistency check (isospectral lattices share determinant), and it
holds. No transcription error survived.

## S1c — the KK punchline (framing, precise)

A flat torus ℝⁿ/Λ has Laplace spectrum `{4π²‖v‖² : v ∈ Λ*}` (dual lattice). So **representation-equivalent
lattices ⟺ Laplace-isospectral dual tori.** S1a makes L₁, L₂ representation-equivalent ⇒ the tori
`T_i = ℝ⁴/L_i*` have **identical Laplace spectra**; S1b makes L₁, L₂ non-isometric ⇒ (duality preserves
isometry classes) `T₁, T₂` are **non-isometric**. Identical KK tower, different hidden torus — verified.

**The dimension boundary, now complete on the family's own instruments:**
- **Audible in dim ≤ 3** — flat 2-tori are spectrally determined (our **V3 SURVIVED**; Schiemann's positive
  theorem covers dim ≤ 3).
- **Deaf from dim ≥ 4** — this pair (and Milnor's 16D E₈⊕E₈ vs D₁₆⁺).
- **What could still tell them apart:** eigenfunction-level data, not the spectrum — exactly **route 5's
  channel**, and the content of **K5** (a recording carries eigenfunction overlaps, which distinguished the
  isospectral drums while the eigenvalue tower sat at chance).

This closes the K2 → K5 → S1 arc: *same spectrum, different geometry (K2/S1); the geometry is recoverable
only from data richer than the spectrum (K5/route 5).*

## Honest scope

Pure lattice theory — Milnor 1964, Conway–Sloane 1992, Schiemann 1990, Cerviño–Hein 2009. **Zero novelty
claimed**; the payout is an exact, self-validating verification on the bridge's instrument and the
arc-closing statement in the genuine KK setting. The gated claims (S1a, S1b) are airtight in exact integer
arithmetic; S1c is the physics reading with its dual-lattice correspondence stated explicitly. Not a claim
about our universe's compactification (which no instrument can reach — see `KK_EXTENSION_NOTES.md`).

## Inputs & artifacts

Cerviño–Hein, "The Conway–Sloane tetralattice pairs are non-isometric," arXiv:0910.2127 (read directly from
the PDF). · `code/schiemann.py` (exact Python integer arithmetic) · `results/schiemann.json`.
