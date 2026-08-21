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
