# V17: pre-registration. An independent first-order check: which Kerr Killing tensors survive the Manko–Novikov quadrupole deformation?

*2026-11-17, evening IST. Written and committed BEFORE any V17 code exists or runs. Sumit's go: 2026-11-17.*

## The claim under test (ansatz §153, sealed e85f7f4, data/jet/SEAL_153.sha256)

Kerr is deformed to first order by the Manko–Novikov (MN) quadrupole parameter β: g = g_Kerr + β h + O(β²). ansatz
reports that only the trivial tensors survive at every valence 1–6:
- the trivial ones are p_t^a p_φ^b H^c, giving the floor 2, 4, 6, 9, 12, 16;
- Carter, Carter² and Carter³ all die at first order.

**What the bridge knows of ansatz's run:** the headline numbers above; that its method is a "box-free first-order jet
test" with S = B − B₀ on the pair (F₀, F₁); that its controls reproduced its published §141 ladder (d1: 4/10/21,
d3: 4/9/17); and its input check (dg/dβ against a 60-digit finite difference). The bridge has **not** read §153, its
code, its MN file, its points or its parameter values. This check is therefore independent, but **not blind**.

## Method: the bridge's own

**Metric.** The bridge's own MN transcription (V9 `v9_nve.mn_functions`), gated against quantum's fields in V8/V9 and used
in V10-MN. Here β is a sympy symbol:
- g₀ = g at β = 0, which is Kerr;
- h = ∂g/∂β at β = 0, taken symbolically by sympy.
The inverse-metric perturbation is G₁ = −G₀ h G₀, in blocks: the (t, φ) 2×2 block, and the xx and yy entries separately.

**Jets.** The bridge's own V10 machinery:
- truncated bivariate power series over GF(q);
- √ handled at points where the base is a rational square (no exp survives at β = 0);
- the Poisson-bracket jet operator `build(G, r, N)`. It is linear in G, so E(G₀ + βG₁) = E₀ + βE₁.

**Two formulations, computed side by side; they must agree.**
- **(A) Explicit Kerr basis plus solvability.** The Kerr Killing tensors at valence r are spanned by
  p_t^i p_φ^j H₀^k K^l with i + j + 2k + 2l = r. Here K is Carter's tensor, written out explicitly below.
  - For each basis element F₀,ᵢ, compute bᵢ = E₁·jet(F₀,ᵢ), the jet of {H₁, F₀,ᵢ}.
  - A combination Σcᵢ F₀,ᵢ extends to first order iff E₀ k₁ = −Σcᵢ bᵢ is solvable at jet level.
  - So S_A = n_basis − (rank[E₀ | b₁ … bₙ] − rank E₀).
- **(B) Joint kernel.** S_B = nullity([[E₀, 0], [E₁, E₀]]) − nullity(E₀). This is the dimension of the projection
  of the joint jet kernel onto the F₀ jets.

**Carter's tensor in MN's (x, y) chart at β = 0:**
- coordinates: r = M + k x, y = cos θ, k = √(M² − a²);
- K = (1 − y²) p_y² + (a(1 − y²) p_t + p_φ)² / (1 − y²) − 2a² y² H₀.

The sign convention of a in V9 is fixed by gate C0: both signs are tried, and exactly one must pass.

**Points and parameters.**
- Points: P_A = (3/2, 1/3), with R₀ = 7/6; P_B = (2, −1/4), with R₀ = 7/4.
- Parameters (M, a): p1 = (5, 3), k = 4; p2 = (13, 5), k = 12.
- Primes: q₁ = 2³¹ − 1 and q₂ = 2³¹ − 19.
- Valence r = 1–6 (Kerr counts 2, 5, 8, 14, 20, 30; floor 2, 4, 6, 9, 12, 16).
- Jet order: N = r + 1, escalating to r + 2 and then r + 3 while S > floor.

## Controls, run first; any failure means STOP

- **C0, the Kerr gate (exact).** At both points, both parameter sets and both primes:
  - E₀·jet(F) = 0 identically for F = p_t, p_φ, H₀ and K;
  - the basis jets are independent, with rank equal to the Kerr count at every valence 1–6;
  - nullity(E₀) ≥ the Kerr count.
- **C1, survival can be seen.** Deformations inside the Kerr family must give S = the Kerr count at every valence
  (all tensors survive): h = ∂g/∂M and h = ∂g/∂a at β = 0, at fixed (x, y).
- **C1b, a null deformation.** G₁ = −L_ξ G₀ with ξ = (x y² + x²/3) ∂_x + (x y) ∂_y must give S = the Kerr count.
- **C2, death can be seen.** G₁ = x·y in the tt slot only, zero elsewhere (non-separable). It must give S < the Kerr
  count at valence 2; the prediction is the floor. If S stays at the Kerr count, the method is blind and V17 is
  VOID.
- **Internal checks, at every run:**
  - S_A = S_B, otherwise STOP;
  - S ≥ floor, because the trivial tensors always extend; a value below the floor means a BUG and STOP;
  - the two primes must agree, otherwise report both and treat the case as unresolved.

## Target and verdict

**Target:** the MN β-derivative, for both parameter sets, both points and both primes, at valence 1–6.

**Verdict:**
- **CONFIRMED** (agrees with §153) if S = floor at every valence 1–6, for every parameter set, point and prime, at
  some N ≤ r + 3.
- **NOT CONFIRMED / INCONCLUSIVE** at a valence where S > floor at N = r + 3. A jet bound above the floor does not
  prove that a tensor survives.
- **DISAGREES** if a control-passing run finds survivors beyond the floor that persist to N = r + 3 at both points and
  both primes. Report it, don't adjust.

## What this does and does not establish

- **Death at jet level is a necessary-condition failure.** No smooth first-order extension K₁ exists near the point.
  That holds over Q, given the modular-rank caveat:
  - over GF(q), rank E₀ can drop. A drop could wrongly show a death, but never wrongly show a survival;
  - two primes plus the control behaviour make that unlikely, but this is not a proof;
  - the grade is "exact modular arithmetic, two primes".
- **Not covered:**
  - the pole-order ladder (partial survival at higher powers of Carter); the bridge has no independent partial-survival
    control;
  - second order in β;
  - the exact (non-perturbative) MN question, which V10-MN already covered to valence 10.
- **A second method** (resonance / Poincaré obstruction on resonant Kerr tori) is deferred: it runs only if V17 agrees.

## Resources

1 core at nice 10. RSS guard 3 GB. Under 50 MB of disk. The run stops itself if free disk falls below 5 GB.
