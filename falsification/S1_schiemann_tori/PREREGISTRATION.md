# S1 — Pre-registration: flat 4-tori are NOT spectrally determined (the KK-tower punchline of the drums arc)

*Frozen 2026-07-24, before `code/schiemann.py` is written or run. Falsification v2, Tier S — bred from the
K2/K5 drums arc. The postulate under attack: **"a KK compactification's mass tower determines the hidden
torus."** In 2D it does (V3 SURVIVED: flat 2-tori are spectrally determined). This attack builds an explicit
**4-dimensional** counterexample: two non-isometric flat 4-tori with identical Laplace spectra — hence
identical KK mass towers — so the tower cannot determine the hidden T⁴, even in principle.*

## Source (primary; leg-W discipline)

Cerviño & Hein, "The Conway–Sloane tetralattice pairs are non-isometric," arXiv:0910.2127. The explicit
integer instance is **Schiemann's example, parameters (a,b,c,d) = (1,7,13,19)** (their Remark 1). Original
results: Milnor 1964 (16D), Conway–Sloane 1992 (the 4-parameter family), Schiemann 1990 (the integer
quaternary forms). The lattice generators are transcribed **verbatim** from the paper (p.4); the theta
agreement is **self-validating** — a wrong transcription makes the two theta series disagree, so S1a
passing certifies both the transcription and the isospectrality.

## The construction (verbatim, p.4)

Basis B carries inner product `diag(a,b,c,d) = diag(1,7,13,19)`. Generators (columns, B-coords):
```
l0 = (−1, 3, −1, 1)      l1 = (1, −1, −1, 3)      l2 = (−1, −1, 1, 3)      l3 = (−1, 1, −1, 3)
L1 = span{ l0, l1, 3·l2, 3·l3 }        L2 = span{ l0, 3·l1, l2, 3·l3 }
```
Gram matrices in the generator basis: `G1 = M1ᵀ D M1`, `G2 = M2ᵀ D M2`, `D = diag(1,7,13,19)`,
`M1 = [l0 | l1 | 3l2 | 3l3]`, `M2 = [l0 | 3l1 | l2 | 3l3]` — exact integer 4×4 symmetric positive-definite.
A lattice vector has n-coords `n ∈ ℤ⁴`; square-norm `nᵀGn`; inner product of two `pᵀGq`.

## Frozen gates (all exact integer arithmetic; no floating point in the verdicts)

- **S1a — isospectral (same theta series).** The representation numbers (count of lattice vectors of each
  square-norm) of L1 and L2 agree for **every** norm up to N_max = 400, **and** `det G1 = det G2` (a
  necessary consistency check + a transcription guard). PASS = same tower. Expected PASS (proven theorem).
- **S1b — non-isometric (exact witness).** The **degree-2 Siegel theta** must differ: enumerating ordered
  pairs of lattice vectors up to a norm bound B2 and bucketing each by its 2×2 Gram data
  `(‖u‖², ‖v‖², u·v)`, there exists a bucket whose multiplicity differs between L1 and L2. An isometry is a
  bijection preserving all pairwise Gram data, so **a single differing bucket proves non-isometry
  rigorously.** PASS = non-isometric. If no differing bucket up to B2, report **UNDECIDED(bound)** honestly
  and raise B2 (Cerviño–Hein prove the degree-2 invariant Θ₁,₁ differs, so a difference must exist).
- **S1c — the KK punchline (framing, not a gated numeric claim).** A flat torus `ℝ⁴/Λ` has Laplace spectrum
  `{4π²‖v‖² : v ∈ Λ*}`; so **representation-equivalent lattices (S1a) ⟺ Laplace-isospectral dual tori**. The
  tori `T_i = ℝ⁴/L_i*` therefore have **identical Laplace spectra = identical KK mass towers**, yet are
  **non-isometric (S1b)** — the mass tower cannot determine the hidden T⁴. Dimension boundary, now complete:
  **audible in dim ≤ 3** (V3 + Schiemann's positive theorem) · **deaf from dim ≥ 4** (this pair, and
  Milnor's 16D). What could still tell them apart is **eigenfunction-level data** — exactly route 5's
  channel (K5: recordings carry eigenfunction overlaps, not just the spectrum).

## Honest scope

- Pure lattice theory (Milnor / Conway–Sloane / Schiemann / Cerviño–Hein). **Zero novelty claimed** — a
  worked, exact verification on the family's own instrument, closing the K2/K5 arc in the actual KK setting
  (flat tori, no boundary — a genuine compactification analogy, not merely a 2D membrane).
- The gated claims (S1a, S1b) are pure lattice facts, airtight in exact arithmetic. S1c is the physics
  reading, stated with its dual-lattice correspondence explicit.
- Bridge-solo: exact Python integer arithmetic, no sister, no external run-time dependency beyond the
  one-time literature pull (done, from the primary PDF read directly).
