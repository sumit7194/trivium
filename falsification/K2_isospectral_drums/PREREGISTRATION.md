# K2 — Pre-registration: the mass tower does NOT determine the hidden geometry

*Frozen 2026-07-23, before `code/k2_drums.py` is written or run (the construction was scouted in a scratchpad
to set honest thresholds; the production script re-derives everything under the gates). Ledger item K2
(Tier K — expected kill; a sharpening shot whose value is the worked demonstration on our own instrument).*

## The postulate under attack (Ledger K2)

> **"The KK mass tower determines the hidden geometry"** — "you can hear the shape of the hidden drum."

This is Kac's 1966 question ("Can one hear the shape of a drum?"), answered **NO** by Gordon–Webb–Wolpert
(1992): two non-congruent planar domains with identical Dirichlet spectra. **Expected KILL.** The value is a
worked demonstration of spectral non-uniqueness *on the family's own FD instrument*, and the setup for the
drums arc (K5 — can a net distinguish them from projections? · M4 — does any coupling break the degeneracy?)
and for its honest converse (V3 — 2D flat tori *are* determined by their spectrum).

## The construction (frozen)

Each drum is **7 congruent right-isosceles triangles** (legs 1, hypotenuse √2) glued two different ways —
the Gordon–Webb–Wolpert pair, in the vertex form used by Cleve Moler's transplantation exposition:

- **Drum 1 outline:** (0,0),(0,1),(2,3),(2,2),(3,2),(2,1),(1,1),(1,0)
- **Drum 2 outline:** (1,0),(0,1),(0,2),(2,2),(2,3),(3,2),(2,1),(1,1)

Both have area 7/2. The 7 triangles per drum are listed explicitly in the code.

**Why the discrete result is exact, not approximate:** the transplantation proof (an eigenfunction on one
drum is assembled from rotated/reflected triangular pieces of the other) is a *combinatorial* bijection, so
it applies verbatim to the finite-difference operator at **any** grid size. The two FD Laplacians are
therefore expected to be isospectral to **machine precision**, not merely to discretisation error.

## Method (frozen)

- **Grid:** offset cell centres at ((i+½)h, (j+½)h), h = 1/n — the offset guarantees no grid point ever lands
  on a triangle edge, so the interior test is unambiguous.
- **Interior test:** a point is in the drum iff it is strictly inside one of the 7 triangles (barycentric).
- **Operator:** the standard 5-point Dirichlet Laplacian on interior points (exterior neighbours contribute
  0), scaled by 1/h². Lowest **20** eigenvalues via sparse shift-invert.
- **Grid-alignment guard (frozen):** the comparison is only run at resolutions where the two drums yield the
  **same interior-point count N₁ = N₂**. Resolutions failing this (scouting found **n = 24** does: 1988 vs
  1981) are *reported and excluded* — the offset grid is not transplantation-compatible there, which is a
  property of the grid, not of the drums. Production resolutions: **n ∈ {16, 32, 64}**.

## Frozen gates

- **K2a — the KILL (primary): same tower.** At every aligned resolution, the lowest 20 Dirichlet eigenvalues
  of the two drums agree to **max |Δλ|/λ̄ < 1e-8**. → **KILLED**: identical spectrum, different geometry ⇒ the
  tower does not determine the shape. → SURVIVES if any eigenvalue differs by more than 1e-3 relative.

- **K2b — different geometry (non-congruence).** The two drums must genuinely differ:
  (i) they share **area** (7/2) and **perimeter** — a required consistency check, since these are the leading
  heat-trace coefficients and *must* agree for isospectral domains; and
  (ii) they are **not congruent**, proved by exhaustive search over all 8 symmetries of the square
  (4 rotations × reflection) plus translation: no element of the dihedral group maps drum 2's vertex set onto
  drum 1's. A finite, exact check — not a numerical one.

- **K2c — exactness (the transplantation signature).** The agreement is at machine precision and does **not
  degrade with resolution**: max |Δλ|/λ̄ ≤ 1e-10 at n = 16, 32 and 64 alike. An FD *approximation* would show
  error shrinking as O(h²); a *combinatorially exact* isospectrality shows resolution-independent
  machine-precision agreement. This distinguishes the two and is the sharper claim.

## Honest limits (fixed in advance)

- **This is a known theorem** (Gordon–Webb–Wolpert 1992; Kac 1966), not a discovery. Zero novelty is claimed.
  The payout is Tier-K's stated one: a worked demonstration of spectral non-uniqueness on our own instrument,
  which the drums arc (K5, M4) and the converse (V3) then build on.
- 2D Dirichlet drums are an *analogy* for a KK mass tower, not a KK reduction: the postulate is killed in the
  precise sense that "spectrum ⇏ geometry" for a Laplacian eigenvalue problem. Any claim about literal
  extra-dimensional geometry would need the actual KK setting — not claimed here.

## Anchors (read-only)

Kac 1966 ("Can one hear the shape of a drum?") · Gordon–Webb–Wolpert 1992 (Inventiones 110, 1–22) ·
Cleve Moler, "Can One Hear the Shape of a Drum? Part 3, Transplantation" (MathWorks, 2012) ·
Driscoll 1997 ("Eigenmodes of isospectral drums", SIAM Review). Interpreter: conjecture_machine `.venv`
(numpy 2.4.6, scipy 1.18.0).
