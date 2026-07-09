# Leg U — Findings: the 6D KK tower and its axion, on the bridge's own two-loop simulator

*Run 2026-07-03; gates U1/U2/U3 frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before a line of the
simulator was written. The **6D sequel to leg S**: leg S joined the 5D single-loop tower `m_n = n/R` across
four repos; here the bridge builds its **own** massless-wave-on-a-hidden-T² projection simulator and tests
two things ansatz has just **proven symbolically** (§112, §113) but no repo had shown numerically — the
two-loop **degeneracy** and its **axion-splitting**. Both gates pass; read-only from ansatz, all code the
bridge's own.*

## Result in one line

The bridge's independent finite-difference instrument reproduces ansatz §112's diagonal-metric
**sum-of-two-squares tower** `m = √(n₁²+n₂²)` (U1, max buzz error **0.33%**, within-shell degeneracy exact
to 0.00%) — and when the **twist χ** is turned on (ansatz §113's axion), the degenerate `√2` level
**splits** into `m(1,1)=1.241` and `m(1,−1)=1.692` with `Δ(m²)` matching the SL(2,ℝ)/SO(2) coset-metric
prediction `4χ/(1−χ²)` to **0.25%**, while the built-in `n₁n₂=0` control (1,0)≡(0,1) does **not** split
(0.00%). The twist is a **measurable axion coupling**, exactly where §113 proved it lives.

## The two-loop tower (U1, χ=0) — measured buzz vs prediction

| sector | m measured | m = √(n₁²+n₂²) | err |
|---|---|---|---|
| (1,0), (0,1) | 1.00331 | 1.00000 | 0.33% |
| (1,1), (1,−1) | 1.41365 | 1.41421 | 0.04% |
| (2,0), (0,2) | 1.99498 | 2.00000 | 0.25% |
| (2,1), (1,2) | 2.23073 | 2.23607 | 0.24% |

Every winding sector's rest-buzz lands on the sum-of-two-squares tower; the r₂ within-shell degeneracies
((1,0)≡(0,1), (1,1)≡(1,−1), (2,1)≡(1,2)) hold to 0.00%. This is ansatz §112's proven diagonal-M spectrum
`m² = (M⁻¹)^{ab}n_a n_b` reproduced by a completely independent implementation of the geometry.

## The axion splits the degeneracy (U2, χ=0.3) — the headline

| sector | n₁n₂ | m measured | m predicted | what the twist does |
|---|---|---|---|---|
| (1,0), (0,1) | 0 | 1.05137 (both) | 1.04828 | **control: no split** (shifts only) |
| (1,1) | +1 | **1.24086** | 1.24035 | pulled **down** |
| (1,−1) | −1 | **1.69166** | 1.69031 | pushed **up** |
| (2,1), (1,2) | +2 | 2.04194 (both) | 2.04348 | shifted together (equal n₁n₂) |

`Δ(m²)` between (1,−1) and (1,1): measured **1.322** vs coset-metric prediction `4χ/(1−χ²)` = **1.319**
(0.25%). The mechanism is exactly §113's: the off-diagonal modulus χ enters the internal inverse-metric as
a cross-term `−2χ n₁n₂/(1−χ²)`, so the level shift is controlled by the **product** n₁n₂ — a Zeeman-like
lifting. The degenerate `√2` doublet splits by its sign of n₁n₂; the (2,1)/(1,2) pair (equal n₁n₂=+2) stays
degenerate; the (1,0)/(0,1) pair (n₁n₂=0) is untouched. The tower is now labeled by **both** `n₁²+n₂²`
**and** `n₁n₂` — the fingerprint of the twist.

## Why this is a bridge result

Three deliberately-independent realizations of one geometry agree:
- **ansatz §112/§113** — the machine *proved* the 6D T² reduction: the diagonal internal metric
  `M = diag(Φ₁²,Φ₂²)`, and that the off-diagonal twist χ is a propagating axion on SL(2,ℝ)/SO(2) sourced by
  `F₁·F₂` (symbolic, leftover-zero).
- **quantum** — showed the 5D *single*-loop projection `m_n = n/R` numerically (rest-buzz, leg S).
- **the bridge (this leg)** — extends that to the *two*-loop case with its own FD Laplace–Beltrami
  simulator, and turns §113's axion from a symbolic modulus into a **measured degeneracy-splitting** with
  the coset-metric magnitude.

It is the leg-S pattern (discover-then-verify, one number many routes) aimed one rung up the dimension
ladder — and the axion channel adds a genuine **control** (n₁n₂=0), so the split is demonstrably the
physics and not a grid artifact.

## Honest limits (frozen in advance, U3)

- **Flat-torus KK spectrum — textbook physics** (Kaluza 1921 / Klein 1926). The buzz-vs-formula agreement
  is a **self-consistency of two implementations** of the same geometry (FD Laplacian vs closed-form coset
  metric), not an independent measurement of nature.
- **Not a claim about real extra dimensions.** Per quantum's `PLAN_projections.md`, none of these routes
  test whether our universe is built this way; they make the speculation exact and show what it would
  explain (a mass tower, an axion) and cost (unseen towers).
- The instrument floor is the finite-difference dispersion (≲0.33% at grid 64², modes |n|≤2); the twist
  magnitude (χ=0.3) was chosen to give a large, unambiguous split well inside the positive-definite regime
  (det M = 0.91 > 0).

## Inputs (read-only) & artifacts

- ansatz §112 `scripts/112_kk6_two_fields.py` (`d43640d`) — diagonal-M dictionary & spectrum anchor.
- ansatz §113 `scripts/113_kk6_twisted.py` (`5dd18e0`) — the twist = axion on SL(2,ℝ)/SO(2).
- quantum `qsim/kk_projection.py` + `PLAN_projections.md` — the 5D single-loop precedent and the honest
  framing this leg adopts.
- `code/kk6_tower.py` — the bridge's own T² projection simulator + gates. `results/kk6_tower.json`.

---

## Update (2026-07-10) — the five-route join: PASS. Leg U is the family's strongest object.

Round-6 sister results landed and the join gates (frozen in the PREREGISTRATION ADDENDUM before
`code/five_route_join.py` ran) all pass:

| route | who | result | gate |
|---|---|---|---|
| 1. symbolic proof | ansatz §112/§113 | M-dictionary + χ = SL(2,ℝ)/SO(2) axion, leftover-zero | anchor |
| 2. FD simulator | bridge (this leg) | split 0.45080, Δ(m²) to 0.25% | U1/U2 ✅ |
| 3. blind direct numerics | quantum | 10/10 sectors ≤0.27%; split 0.44867 (0.29%); control 0 | J1 ✅ |
| 4. independent FDTD | tabula (158, S0) | Δm² vs 4χ/(1−χ²) corr 1.00000, err 0.25% | J2 ✅ |
| 5. neural discovery, blind | tabula (158) | K=3 latents (decode r ≈0.97 each; χ-family K=1 = the axion); Δm̂² corr 0.9997, med 1.44%; control 0.16% | J3 ✅ |

Cross-route: bridge vs quantum measured splits agree to **0.47%** (J4 ✅). And the deep half, tabula's own
gated geometry results (recorded, not re-derived): the net's moduli space is the **SL(2,ℤ) fundamental
domain** (modular T/S gauge certificate ≤0.22%) and its learned spectrum reproduces the **hyperbolic
SL(2,ℝ)/SO(2) metric** in the many-mode limit (cosine vs true-mass metric 0.9994) — *the moduli-space
geometry ansatz proved symbolically, discovered from projections alone*. tabula also flagged the honest
subtlety: "latent metric" is gauge-ill-posed; the canonical object is the behavioral sensitivity metric,
hyperbolic only in the e^{−βm²} many-mode limit — adopted as this leg's framing too.
One spectrum, one axion, five failure-mode-disjoint routes. `results/five_route_join.json`.
