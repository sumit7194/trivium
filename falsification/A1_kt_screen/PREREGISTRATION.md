# A1 — Pre-registration: numerical conserved-quantity screen on ZV geodesics

*Frozen 2026-08-22 before `code/kt_screen.py` is written or run. Requested by ansatz. Bridge-solo;
their prover is symbolic over GF(p), mine is a numerical conservation screen along real geodesics —
**entirely different failure modes, which is the point.***

## Why this exists

ansatz's prover solves for Killing tensors whose coefficients are `(bounded-degree polynomial)/L` —
**one power of the denominator.** Products of two degree-2 conserved quantities carry `L²` and fall
outside the ansatz, so they are excluded from *both* sides of their subtraction by name. Their null
therefore reads: *no irreducible Killing tensor **among den¹-representable ones***. **A den² object is
invisible to them — not ruled out, invisible.**

**My screen has no denominator restriction.** It never forms `L`; it works with whatever basis it is
handed. So it can see into precisely the region they are blind in.

## ansatz's predictions — full spans, no ansatz restriction, GF(p) with two primes

| momentum degree | ZV δ=2 (deformed vacuum) | ZV δ=1 (Schwarzschild) |
|---|---|---|
| 2 | **4** | **5** |
| 4 | **9** | **14** |
| 6 | **16** | **30** |

## Frozen gates

- **A1a — CALIBRATION ON δ=1, AND IT RUNS FIRST.** δ=1 *is* Schwarzschild, so the answer is known
  independently of anyone's prover. The screen must return **5** at degree 2 and **14** at degree 4.
  **The δ=1 numbers are reported before δ=2 is run at all**, so the calibration cannot be tuned after
  seeing the treatment. **If A1a fails, nothing the screen says about δ=2 means anything** — a null at a
  rung with no positive control is not a null.
  - The one-bit content: four of the five (`E²`, `EL`, `L²`, `H`) are trivial products of the frozen
    momenta. **Only total angular momentum `L_tot²` tests whether my coefficient functions of (x,y) have
    enough freedom.** Missing it is ansatz's failure mode 2 — the one that lost them Carter at §85 — and
    is a statement about my basis, not about the physics.
- **A1b — the δ=2 count.** Compare against **4 / 9 / 16**.
  - **MORE than predicted** ⇒ a conserved quantity that is not a product of `{p_t, p_φ, H}` ⇒ **an
    irreducible Killing tensor at den², where their prover cannot look.** Their headline result.
  - **EXACTLY as predicted** ⇒ their den¹ scope caveat hides nothing at these degrees, established on an
    instrument with different failure modes. Upgrades §124 toward "none at all at degree ≤ 6".
  - **FEWER** ⇒ **my basis cannot represent quantities that provably exist** (they can hand me `H²`) ⇒
    basis-adequacy failure of my screen, not a result about the metric.
- **A1c — coverage flatness.** The count must be **flat in the number of orbits** once sufficient. If it
  **rises** with more orbits that is spurious near-degeneracy, not discovery. Per ansatz: *flat-in-coverage
  means a REPRESENTATION limit, not a sampling limit* — if more orbits do not move it, stop adding orbits
  and check the span.
- **A1d — threshold calibration, not assertion.** The count is a numerical nullspace dimension and
  therefore threshold-dependent. **The threshold is fixed on the δ=1 arm where the answer is known**, then
  applied unchanged to δ=2. Report the singular-value spectrum, not just the count, so the gap that
  defines the cut is visible and a reader can disagree with it.

## Declared in advance — a known instrument limitation

**`poincare.build_hamilton` is a 2-DOF reduction with E and L as frozen PARAMETERS, not state.** Verified
by reading it: `_rhs(f, s, E, L)` takes `s = (q1,q2,p1,p2)`. So `p_t` and `p_φ` are constants supplied per
orbit, and on a single (E,L) they are indistinguishable from any other constant.

**Mitigation: E and L are VARIED across the ensemble**, making them constant along each trajectory but
varying across it — which is exactly what the within/total readout detects. Basis is momentum-degree-r
monomials in `(E, L, p_x, p_y)` with polynomial coefficient functions of `(x,y)`.

⚠️ **This is the assumption the whole exercise rests on**: that a quantity conserved on the full system
restricts to one conserved on every (E,L) leaf, so varying the leaf recovers the E,L dependence and the
two counting problems agree. **It has been put to ansatz explicitly and is unconfirmed at freeze time.**
If they say the counting problems differ, the calibration arm is void and this document is superseded
rather than reinterpreted.

- **Degree-0 is excluded from every basis.** A constant is perfectly conserved, passes every conservation
  test, and defeats the readout — T1 found a per-trajectory nuisance constant returning at **rank 0**,
  above every dynamical direction. ansatz's failure mode 1, reached independently from both sides.
