# K2 — Findings: the mass tower does NOT determine the hidden geometry

> ## ⚠️ CORRECTION (2026-07-24) — the first version of this result was wrong in its *mechanism*
>
> **Bug found by tabula, confirmed and fixed by the bridge.** The original discretisation used the **same
> grid offset in x and y**. Every grid point lying on an internal diagonal (x±y ∈ ℤ) is then interior to no
> triangle, and the strict in-triangle test dropped it. Those dropped lines acted as walls: **each drum was
> disconnected into 3 congruent pieces (sizes 360/360/120 at n=16), identical between the two drums**, so the
> two discrete Laplacians were *one matrix relabelled*. The celebrated "identical to ~10⁻¹⁵, **resolution-
> independent**" was therefore a **triviality, not transplantation**, and K5 was untestable on it.
>
> **Retracted:** the K2c claim of resolution-independent *exact* discrete isospectrality, and the inference
> that it demonstrated the combinatorial transplantation.
> **Stands:** the verdict **KILLED** — but now on the continuum GWW theorem plus a *converging* numerical
> demonstration, which is what an honest generic FD grid can show.
> **Fixed:** distinct offsets (0.5, 0.25) so no grid point can lie on any edge, plus a **connectivity
> assertion** in `laplacian()` as a regression guard.

*Run 2026-07-23, corrected 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item K2
(Tier K — expected kill). **Verdict: KILLED** — on the continuum GWW theorem plus a convergent numerical
demonstration. Sets up the drums arc (K5, M4) and its honest converse (V3).*

## Result in one line

The two Gordon–Webb–Wolpert drums — non-congruent planar domains built from the same 7 right-isosceles
triangles glued differently — have Dirichlet spectra that **converge to each other as the grid refines**
(6.87×10⁻² at n=16 → 1.47×10⁻² at n=96, order ≈ h⁰·⁹⁷, staircase-boundary limited), consistent with their
**exact continuum isospectrality** (GWW 1992). You cannot hear the shape of the drum.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **K2a** (KILL) | spectra converge with resolution | **6.87e-2 → 4.10e-2 → 2.17e-2 → 1.47e-2** (n=16/32/64/96), monotone, ×4.7 | **K2 KILLED** |
| **K2b** | genuinely different shapes | area 3.5=3.5, perimeter 10.242641=10.242641; **not congruent** | **PASS** (unaffected by the bug) |
| **K2c** | ~~exactness, resolution-independent~~ → convergence order | ≈ h⁰·⁹⁷ | **RETRACTED and replaced** |

## The spectra (n = 96, lowest 6, corrected grid)

```
drum 1:   9.9589  14.3057  20.3627  25.7480  28.5078  36.3606
drum 2:   9.9760  14.4334  20.4261  25.8671  28.5795  36.4575
```

Close but not identical — the residual is discretisation error, and it **shrinks monotonically** with
resolution (6.87e-2 → 1.47e-2 from n=16 to n=96, ≈ h⁰·⁹⁷), converging toward the exact continuum
isospectrality. The interior-point counts differ slightly between drums (32304 vs 32208 at n=96), as they
should for a generic grid sampling two different domains.

## Why K2b matters (and why "same perimeter" is a feature, not a coincidence)

Isospectral domains **must** share the leading heat-trace coefficients — area (c₀) and perimeter (c₁) — so
finding area 3.5 = 3.5 and perimeter 10.242641 = 10.242641 is a *required consistency check*, not evidence of
sameness. The shapes are nonetheless genuinely different: an **exhaustive, exact** search over all 8
symmetries of the square (4 rotations × reflection) combined with translation finds **no** isometry mapping
one vertex set onto the other. Two different shapes, one spectrum.

## What the corrected demonstration does and does not show (K2c)

The GWW drums are isospectral **exactly, in the continuum** — that is the theorem, and it is not in question.
What a *generic* finite-difference grid can show is **convergence to it**: the discrete spectra approach each
other as h → 0, here at order ≈ h⁰·⁹⁷ (first order, as expected when a staircase grid approximates a domain
with diagonal boundaries). That is an honest numerical corroboration of the theorem.

What it does **not** show — and what the retracted claim wrongly asserted — is *exact discrete*
isospectrality. Transplantation is indeed a combinatorial bijection, but it only transfers to a discrete
operator on a grid the transplantation actually maps to itself. A generic offset grid is **not**
transplantation-compatible, so exact discrete agreement should not be expected, and when the first run
appeared to show it at ~10⁻¹⁵ *resolution-independently*, that was the tell-tale of an artifact rather than a
triumph. Building a genuinely transplantation-compatible discretisation is a well-posed and interesting
follow-up; it was **not** achieved here.

## Honest limits (frozen in advance)

- **This is a known theorem** — Kac's 1966 question, answered negatively by Gordon–Webb–Wolpert (1992).
  **Zero novelty is claimed.** The payout is Tier-K's stated one: a worked demonstration of spectral
  non-uniqueness on the family's own FD instrument, with an exact non-congruence proof attached.
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
