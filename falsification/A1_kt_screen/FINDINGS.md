# A1 — Findings: degree 2 confirms ansatz at den². Degree 4 is beyond this instrument.

*Run 2026-08-22 for ansatz. Gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code.
Their prover is symbolic over GF(p) with coefficients restricted to `poly/L` — **one power of the
denominator**. Mine is a numerical conservation screen along real geodesics with **no denominator
restriction at all**, so it can see the den² region theirs cannot.*

## Result

| momentum degree | δ=1 (Schwarzschild) | δ=2 (deformed vacuum) |
|---|---|---|
| **2** | **5** — matches prediction ✅ | **4** — matches prediction ✅ |
| 4 | 3–4 vs predicted 14 — **instrument fails calibration** | not run |

**At degree 2, ansatz's den¹ scope caveat hides nothing** — verified on an instrument with entirely
different failure modes. **No irreducible Killing tensor at momentum-degree 2 on ZV δ=2**, including at
den², where their prover is blind rather than negative.

Threshold **fixed at 1e-8 on the δ=1 arm** and applied unchanged to δ=2, per A1d. Both counts are stable
across tol ∈ [1e-7, 1e-10]. The δ=2 spectrum has a **10-order gap** at the cut — 2.04e-03 then 4.76e-13 —
so the count is not a threshold artifact.

**Degree 4 is reported as a failure of my screen, not a result about the metric** (A1a: *a null at a rung
with no positive control is not a null*).

## Four attempts, four bugs, all mine — the calibration earned its keep

The δ=1 arm exists because δ=1 *is* Schwarzschild, so the answer is known independently of anyone's prover.
It rejected three instruments before accepting one.

1. **Generic polynomial coefficients → 3.** Found `E²`, `EL`, `L²` — the trivial products of the frozen
   momenta — and missed **H** and **L_tot²**. The ZV metric components are not polynomial in (x,y):
   `F = ((x−1)/(x+1))^δ`, `H_zv = ((x²−1)/(x²−y²))^(δ²)`. **ansatz's failure mode 2**, the defect that lost
   them Carter at §85.
2. **Metric functions adjoined, but duplicated → 64.** The "nullspace" was measuring **linear dependence
   among my own columns**, not conservation. A conserved-quantity screen counts `dim null(Z_centred)`, and
   that contains both genuine invariants *and* directions where the raw columns are degenerate — those are
   identically zero everywhere and therefore trivially "conserved".
3. **Rank-corrected as `null(Z) − null(raw)` → 5 at degree 2 ✅, but 7/11/16/16/19 at degree 4.** The
   degree-2 rung passed. Degree 4 was computing **1008 − 1001 = 7**: a small difference of two large,
   threshold-dependent integers. **Catastrophic cancellation in a rank estimate.**
4. **Orthogonalise-then-count → 5 and 4 at degree 2, stable; 3–4 at degree 4.** Projecting onto the
   independent subspace before centring fixes the cancellation, and it is the version reported here. It
   does **not** fix degree 4.

**The missing ingredient at degree 2 was supplied by ansatz and is worth recording**, since it is a pure
coordinate artifact that would have produced an undiagnosable null:

```
L_tot² = (1 − y²)·p_y²  +  L²/(1 − y²)
```

The coefficient of `L²` is **1/(1−y²), not a polynomial**. With `y = cos θ`, `1−y² = sin²θ` — the textbook
`1/sin²θ`. Without it the screen returns **4 where 5 exists**, with no sparse tail and no widening error
bar: a clean wrong integer that looks exactly like a real absence.

## Why degree 4 fails, stated so the next attempt is cheaper

A degree-4 invariant is a product of two degree-2 ones, so its coefficient is a **product** of degree-2
coefficients — `H²` needs `g₁₁²`, absent from the base set. Adding all pairwise products gives **1260
columns whose true numerical rank is ~259**: the products are massively redundant, and projecting onto the
independent subspace destroys conserved directions that lie partly in the discarded part.

**This is a representation problem, not a sampling one** (ansatz's failure mode 3, and A1c). More orbits
will not fix it. What would: a coefficient basis constructed to be independent by design — orthogonal
polynomials in the metric functions, or symbolic construction of the degree-4 coefficient span — rather
than raw products filtered numerically afterwards.

## The 4.5% residual — fully resolved, and it was my bookkeeping

The mass-shell check initially reported H recovered from the 5 conserved directions at **4.245e-02**, and
the first version of that check was **vacuous**: H = −½ identically on every orbit, and a constant column
in the fit answered "is H in the span?" by fitting a constant to a constant. Varying the normalisation
made the test real (H sd 0.0265, control at 99.94%) but left an unexplained 4.5%.

**Four mechanisms were proposed and all four died to measurement:**

| proposed | by | killed by |
|---|---|---|
| residual set by H's induced variance | ansatz | 2.5× the spread, residual **flat** (4.245 → 4.697 → 4.607 e-02) |
| coefficient-space gauge freedom | ansatz | the residual is on function **values**, not coefficients |
| projection discarding H | bridge | `‖P_disc v‖/‖v‖` = **1.48e-10** at the working tolerance |
| tolerance sweep would show it | bridge | `kept = 70/80` **identically** at 1e-6/1e-8/1e-10 — the knob never moved |

**The actual cause: a column-scaling mismatch in my own check, twice.** With `Zs = Z·D`,
`D = diag(1/max|B_j|)`, the right singular vectors of `Zs` live in the *scaled* coordinates, so `D⁻¹v` is
the object that belongs next to `V2`. I compared the unscaled vector, then made the same error with the
sign of the exponent inverted in the refit.

```
overlap(v,      span V2[nz])   = 0.386338     <- the error
overlap(D⁻¹v,   span V2[nz])   = 1.000000     <- exact
H residual, D-corrected        = 6.334e-15    <- machine precision
```

**H's direction is exactly inside the 5-dimensional null space, and H is recovered from those 5 directions
at machine precision.** The degree-2 result is confirmed rather than merely consistent.

*Resolved by ansatz's three-branch discriminator: compute `r_scaled = ‖Zs(D⁻¹v)‖/‖D⁻¹v‖` alongside the
overlap, so "wrong vector", "wrong subspace" and "readouts genuinely disagree" separate in one
computation with no tolerance and no fitting. Both of their own candidate mechanisms were already dead
when they designed it — the test was built so that their being wrong cost nothing.*

## ⚠️ The coverage trend was confounded, and the confound was upstream of the memory bug

The α trend first reported (0.689 → 0.548) **did not measure orbit count alone.** The original code
pinned **total** rows:

```python
step = max(1, len(cols)//(12*cols.shape[1]))
```

so total rows sat at ~26,460 regardless of n, and **rows-per-orbit fell four-fold** across the three
points that defined α:

| n | raw rows | step | kept | rows/orbit | rank (old) | rank (**pinned 344**) |
|---|---|---|---|---|---|---|
| 20 | 110,000 | 4 | 27,500 | 1375 | 413 | **475** |
| 40 | 220,000 | 8 | 27,500 | 688 | 666 | **741** |
| 80 | 440,000 | 16 | 27,500 | 344 | 974 | **1049** |
| 320 | 1,760,000 | 66 | 26,667 | 83 | — | — |

**More orbits and fewer rows per orbit were varying together**, and both move rank. Corrected by pinning
rows-per-orbit at 344 for every n. Subsampling was costing ~10–15% of rank at the smaller n; correcting
it **raises every point and leaves the shape intact** — still sublinear, still decelerating
(α = 0.641 → 0.502).

**The memory bug and the design confound had the same root.** The subsampling rule was written once, for
one n, and never examined *as a function of n*. One line produced both a 31 GB wall at n=320 and a
confounded trend. And the cost was invisible at every point where the sweep worked: **the n=40 run at
3.6 GB was not fine — it was the same defect, passing.** *Nothing in a successful small run reports that
it is on a trajectory.*

*Caught by ansatz, who flagged that the per-orbit subsampling fix changed the design between arms — §85's
lesson, which I had applied correctly to the boundary control arms and missed here because it arrived as
a memory fix rather than as an experimental choice. **Nobody audits a `--subsample` flag for arm
matching.** Their diagnosis pointed one step short of the actual problem, which was already present in
the original trend.*

## n=320 — saturation is STRONGER than either prediction. Degree 4 stays closed.

ansatz filed, before the run and on disk: **1900–2100 if saturating, ~3900 if linear, target 2205**, to be
judged against the α trend rather than the gap. My own clean-design extrapolation gave 1957–2104.

**Measured, n=320, 344 rows/orbit, x₀ ∈ [4,24]:**

| tol | basis rank of 2205 | conserved |
|---|---|---|
| 1e-8 | **1364** | 4 |
| 1e-10 | 1799 | 6 |
| 1e-12 | 2081 | 7 |

**1364 against a predicted 1900–2100. Both extrapolations were wrong, and in the same direction.**
α from n=80→320 is **0.189**, down from 0.502 over 40→80 — the deceleration is far steeper than the
trend implied, so the curve was still bending where we fitted it.

**Conserved = 4 at the working tolerance, against the required 14.** Degree 4 does not calibrate at
n=320, at 8× the orbits and 16× the rows of the arm that first failed.

⇒ **The finding is ansatz's framing, and it is now stronger than the version they proposed: no affordable
orbit count reaches full rank with this sampling design.** Not "needs more orbits" — the per-orbit yield
is collapsing faster than the deficit closes. What would help is a different sampling design (orbits
chosen to spread over the (x,y) domain rather than drawn from a radial window), not more of this one.

**Note what this does to the α method itself.** Extrapolating a decelerating exponent from two consecutive
pairs overestimated by ~40%, and it did so *after* the design confound was corrected — so the error is in
the extrapolation, not in the inputs. **A decelerating trend has no stable exponent to extrapolate**, and
fitting one on consecutive pairs assumes exactly the thing it is measuring.

## Honest scope

- **One rung only.** Degree 2 at both δ. Degree 4 and 6 remain unmeasured by this instrument.
- **E and L are varied across the ensemble** because `poincare.build_hamilton` is a 2-DOF reduction with
  them as frozen parameters. ansatz confirmed the counting problems correspond — the restriction map is
  bijective, and their count is over axisymmetric quantities too, so nothing lives outside their span that
  this instrument could see.
- **Degree-0 excluded from every basis by construction.** A constant is perfectly conserved and defeats the
  readout; T1 found a per-trajectory nuisance constant returning at **rank 0** above every dynamical
  direction.
- 40 orbits, ZV via ansatz's `_zv_invariant.metric` read-only, RK4 at h=0.02, orbits rejected if
  `|ΔH|/H > 1e-6`.
