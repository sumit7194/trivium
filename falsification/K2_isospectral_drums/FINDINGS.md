# K2 — Findings: the mass tower does NOT determine the hidden geometry

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item K2
(Tier K — expected kill). **Verdict: KILLED**, and the agreement is stronger than "numerically close": it is
**combinatorially exact**. Sets up the drums arc (K5, M4) and its honest converse (V3).*

## Result in one line

The two Gordon–Webb–Wolpert drums — non-congruent planar domains built from the same 7 right-isosceles
triangles glued differently — have **identical Dirichlet spectra to ~10⁻¹⁵ (machine precision)**, and the
agreement is **resolution-independent** across n = 16, 32, 64, proving the discrete isospectrality is exact
(transplantation) rather than a finite-difference coincidence. You cannot hear the shape of the drum.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **K2a** (KILL) | lowest 20 Dirichlet eigenvalues agree, rel < 1e-8 | **3.3e-15 / 7.1e-15 / 4.7e-15** at n=16/32/64 | **K2 KILLED** |
| **K2b** | genuinely different shapes | area 3.5=3.5, perimeter 10.242641=10.242641; **not congruent** | **PASS** |
| **K2c** | exactness: rel ≤ 1e-10, resolution-independent | flat at ~1e-15 (no O(h²) decay) | **PASS** — transplantation, not FD error |

## The spectra (n = 64, lowest 8)

```
drum 1:  18.938837  18.938837  30.143464  30.143464  47.809646  48.799368  48.799368  58.233891
drum 2:  18.938837  18.938837  30.143464  30.143464  47.809646  48.799368  48.799368  58.233891
```

Identical digit for digit, including the doubly-degenerate pairs. Interior point counts also match exactly
(N₁ = N₂ = 14112 at n=64).

## Why K2b matters (and why "same perimeter" is a feature, not a coincidence)

Isospectral domains **must** share the leading heat-trace coefficients — area (c₀) and perimeter (c₁) — so
finding area 3.5 = 3.5 and perimeter 10.242641 = 10.242641 is a *required consistency check*, not evidence of
sameness. The shapes are nonetheless genuinely different: an **exhaustive, exact** search over all 8
symmetries of the square (4 rotations × reflection) combined with translation finds **no** isometry mapping
one vertex set onto the other. Two different shapes, one spectrum.

## Why the agreement is exact, not approximate (K2c — the sharper claim)

The transplantation proof (an eigenfunction on one drum is reassembled from rotated/reflected triangular
pieces of the other) is a **combinatorial bijection**, so it applies verbatim to the finite-difference
operator at *any* grid size. The signature: a mere FD approximation would show error decaying like O(h²) as
the grid refines, whereas the measured error is **flat at ~10⁻¹⁵ across n = 16, 32, 64** — i.e. it is solver
round-off, independent of resolution. That is the fingerprint of exact isospectrality.

**Grid-alignment guard (fired as pre-registered).** At **n = 24** the two drums give *different* interior
point counts (1988 vs 1981) and are not isospectral on that grid. This was frozen in advance as an exclusion:
the offset cell-centre grid is not transplantation-compatible at that resolution — a property of the **grid**,
not of the drums. Reported rather than hidden; the aligned resolutions (16, 32, 64) all agree at machine
precision.

## Honest limits (frozen in advance)

- **This is a known theorem** — Kac's 1966 question, answered negatively by Gordon–Webb–Wolpert (1992).
  **Zero novelty is claimed.** The payout is Tier-K's stated one: a worked demonstration of spectral
  non-uniqueness on the family's own FD instrument, with the exactness sharpened and an exact non-congruence
  proof attached.
- 2D Dirichlet drums are an **analogy** for a KK mass tower, not a KK reduction. What is killed precisely is
  "spectrum ⇒ geometry" for a Laplacian eigenvalue problem. A claim about literal extra-dimensional geometry
  would require the actual KK setting and is **not** made here.
- **What this sets up:** K5 (can a net trained on projections distinguish the drums? — i.e. do
  eigen*functions* leak information the eigen*values* do not?), M4 (does coupling a second field break the
  degeneracy?), and V3 (the honest converse: 2D flat tori *are* determined by their spectrum).

## Inputs (read-only) & artifacts

Kac 1966 · Gordon–Webb–Wolpert 1992 (Inventiones 110, 1–22) · Cleve Moler, "Can One Hear the Shape of a Drum?
Part 3, Transplantation" (MathWorks 2012) · Driscoll 1997 (SIAM Review). `code/k2_drums.py` ·
`results/k2_drums.json`. Interpreter: conjecture_machine `.venv` (numpy 2.4.6, scipy 1.18.0).
