# Leg U — Pre-registration: the 6D KK tower and its axion (a two-loop projection, gated against ansatz §112/§113)

*Frozen 2026-07-03, before `code/kk6_tower.py` is written or run. This is the **6D sequel to leg S**:
leg S joined the 5D single-loop tower `m_n = n/R` across four repos; here the bridge builds its **own**
two-hidden-loop (T²) projection simulator and asks two things ansatz has just **proven symbolically** but
no repo has shown numerically — (U1) does the two-loop tower carry the **sum-of-two-squares degeneracy**
`m = √(n₁²+n₂²)/R`, and (U2) does turning on the **twist χ** (ansatz §113's axion) **split** that
degeneracy exactly as the SL(2,ℝ)/SO(2) coset metric demands? Read-only from ansatz; the bridge writes all
of its own code. Explicitly NOT a claim about real particle physics or our universe (per quantum's
`PLAN_projections.md`); it is a cross-repo triangulation of a proven structure (U3).*

## The proven anchor (ansatz, read-only)

- **§112** (`112_kk6_two_fields.py`, commit `d43640d`): 6D KK on T² with **diagonal** fibre
  `ds²₆ = g₄ + Φ₁²(dw¹+A¹)² + Φ₂²(dw²+A²)²` — internal metric `M = diag(Φ₁², Φ₂²)`, machine-derived
  dictionary (all leftover zero). The fibres cross-couple; the off-diagonal fibre equation is the
  twist-sourcing constraint `R₆(w₁,w₂) = ¼Φ₁²Φ₂² F₁·F₂ = 0` — two parallel fields DEMAND a dynamical twist.
- **§113** (`113_kk6_twisted.py`, commit `5dd18e0`): turn the off-diagonal modulus χ(r) on —
  `M = [[Φ₁², χ],[χ, Φ₂²]]`, `det M = Φ₁²Φ₂² − χ²`. Machine-proven: χ is a **propagating 4D scalar**
  whose source is `F₁·F₂`, with kinetic normalization `1/det M` — the **SL(2,ℝ)/SO(2) axion-dilaton coset
  metric**. So (Φ₁,Φ₂,χ) are the T² moduli and **χ is the axion**.

## The physics the bridge tests (its own instrument)

A massless wave on `1 visible dimension × a hidden T²` with internal metric `M`. A mode winding
`(n₁,n₂) ∈ ℤ²` around the two hidden loops projects, in the visible dimension, to a particle of mass
```
    m²(n₁,n₂) = (M⁻¹)^{ab} n_a n_b .
```
- **Diagonal** `M = diag(Φ₁²,Φ₂²)`, square torus `Φ₁=Φ₂=1` (so `R=1`):
  `m² = n₁² + n₂²` → `m = √(n₁²+n₂²)` — the **r₂ (sum-of-two-squares) tower**.
- **Twisted** `M = [[1,χ],[χ,1]]`, `det M = 1−χ²`:
  `m²(n₁,n₂) = (n₁² − 2χ n₁n₂ + n₂²)/(1−χ²)`. The cross-term `−2χ n₁n₂` **lifts** every degeneracy with
  `n₁n₂ ≠ 0` and leaves every one with `n₁n₂ = 0` untouched.

The bridge measures `m` as the **rest-buzz frequency**: a zero-visible-momentum packet in winding sector
`(n₁,n₂)` oscillates in time at ω = `m(n₁,n₂)` (the same rest-buzz quantum used for the 5D tower). The
internal metric enters only through a **finite-difference Laplace–Beltrami operator on the hidden torus**
`∇²_hidden = (M⁻¹)^{ab} ∂_a∂_b` (the twist appears as the genuine cross-derivative term
`2(M⁻¹)^{12} ∂_{y₁}∂_{y₂}`); the buzz frequency is **measured from the time series**, never injected.

## Frozen numbers (Φ₁=Φ₂=1; twisted run uses χ = 0.3, so det M = 0.91)

| sector (n₁,n₂) | continuum m, χ=0 | continuum m, χ=0.3 | role |
|---|---|---|---|
| (1,0) & (0,1) | 1.00000 | **1.04828** (both) | control: n₁n₂=0 → **no split** under χ |
| (1,1) | 1.41421 | **1.24035** | axion channel (n₁n₂=+1) |
| (1,−1) | 1.41421 | **1.69031** | axion channel (n₁n₂=−1) |
| (2,0) & (0,2) | 2.00000 | 2.09657 | higher shell, control |
| (2,1) & (1,2) | 2.23607 | — | shell N²=5 (diagonal degeneracy check) |

`Δ(m²)` between (1,−1) and (1,1) at χ=0.3: predicted `4χ/(1−χ²) = 1.2/0.91 = 1.31868` (m-split 0.44996).

## Frozen gates

- **U1 — the diagonal two-loop tower + degeneracy.** With χ=0, the measured rest-buzz for each sector
  reproduces `m = √(n₁²+n₂²)` within **TOL = 2%** (the finite-difference instrument floor; quantum's 5D
  single-loop demo hit 0.2–0.7%, we allow margin for the 2D grid), AND the within-shell degeneracy holds:
  `|m(1,0)−m(0,1)|` and `|m(1,1)−m(1,−1)|` are each **< 1% of m** (they should be identical up to grid
  anisotropy). PASS = the bridge's independent instrument reproduces ansatz §112's diagonal-M spectrum.
- **U2 — the axion splits the degeneracy (the headline).** With χ=0.3:
  1. **Split present, correct sign & size:** measured `m(1,1)` and `m(1,−1)` match the twisted-M
     predictions (1.24035, 1.69031) within **TOL = 2%**, i.e. the (1,±1) pair splits with `m(1,−1) >
     m(1,1)` and `Δ(m²)` matches `4χ/(1−χ²)` within TOL.
  2. **Control holds (placebo):** the `n₁n₂=0` pair (1,0),(0,1) does **NOT** split — `|m(1,0)−m(0,1)| <
     1% of m` — even though both shift to 1.04828.
  PASS = the twist is measurably an axion coupling: present with the coset-metric magnitude in the
  `n₁n₂≠0` channel, absent in the `n₁n₂=0` channel. FAIL = split wrong/absent, or the control also splits
  (would indicate a grid artifact, not the axion).
- **U3 — honest framing (fixed in advance).** This is a **flat-torus KK spectrum** — textbook physics
  (Kaluza 1921 / Klein 1926). The bridge's contribution is the **cross-repo triangulation**: an independent
  numeric instrument reproduces ansatz §112's machine-proven diagonal-M spectrum *and* exhibits §113's
  axion (the twist χ) as a **measurable degeneracy-splitting**, extending quantum's 5D single-loop demo and
  leg S's tower to **6D with its full moduli space**. It is **not** a claim that our universe has extra
  dimensions, and the buzz-vs-formula agreement is a self-consistency of two implementations of the same
  geometry (the FD Laplacian vs the closed-form coset metric), not an independent measurement of nature.
