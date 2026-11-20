# TS capture edge: computer-assisted proof recipe (merged with B-5). Draft v1, Bridge (Opus 5.5), 2026-11-20

**Goal.** Turn Fable's conditional reduction (fable_work/ts_capture_edge/L3_ANALYTIC.md, Lemma L3′, reviewed in
V24/REVIEW_LOGIC.md) into a theorem:

> For TS δ=2 (ts45: p = 4/5, q = 3/5) at E = 97/100, L = 41/8, every survive/plunge switch on the symmetry line ℓ
> between x* and x_h lies on W^s(γ), the stable manifold of the brake orbit γ. In particular the capture edge
> accumulates in a Cantor set at x*.

**Division of labour.** quantum builds and runs the certificates in CAPD/Arb under its proof guard. The Bridge
supplies the exact inequalities and the float previews, and reviews each certificate against this file.

**Independence rule (kept).** TS outputs go to the Bridge only, not to tabula or others.
- **Storage (decided 2026-11-20, Bridge, option b).** Certificate code is committed to quantum. Certificate OUTPUTS go
  to quantum's gitignored qsim/scratch/ and are sent to the Bridge, because the quantum repo is public.
- **Note:** TheBridge repo is also public, and V20/V24 float values (λ, x_h, …) are already in its history. The
  tabula blind therefore rests on tabula not reading other repos. This is flagged to Sumit; it is not new exposure.

## v1.1 changes (quantum's review, 2026-11-20)
1. **Preregistration per certificate.** C-N, C-I3, C-L and C-T each get their own prereg before code, with pass rules
   and a control; use a Kerr-type or known-hyperbolic toy where one exists.
2. **Codegen gates.**
   - (i) K_flat ≡ geodesic H at random rational points, by quantum's own sympy route; V24 is the comparison only.
   - (ii) The interval enclosure contains exact rational evaluations of the field.
   - (iii) Section transversality: p_v < 0 is certified at every Σ crossing used. Time is flat-plane fictitious time
     (K = 0), not proper time.
3. **The brake point.** BOTH momenta vanish there, so the g″ formula is 0/0 (my v1 wording, "p_v → 0, reparametrise",
   was incomplete).
   - Fix: γ is even in t about the brake time. So u is analytic in v near v_b if V_v(brake) ≠ 0.
   - g′ → V_u/V_v there, and g″ comes from the t⁴ jet coefficients.
   - Certify V_v ≠ 0 at the brake point. This also gives the transversality of the shooting event (dp_v/dt = −V_v).
4. **C-L gap.** U is not a graph over x near its fold. So compare U(s) with R(U)(s′) by the signed distance along a
   certified transversal, in arc parameters.
5. **Wording corrected.** What makes C-L work is that FORWARD iteration contracts deviations transverse to W^u.
   Area preservation alone does not give that; it gives it together with the tangential growth.
6. **C-I1/I2 under Arb (quantum).** Implemented from the statements in V24/PREREGISTRATION.md, not from the Bridge
   code, for independence.

## 0. Fixed data (every certificate must state these)
- **Metric:** the Bridge TS2 metric, V11 loader, ts45. σ = 1 (prolate units).
- **Energy level:** E = 97/100, L = 41/8, μ = 1, exact rationals.
- **Flat-plane form (exact, V24 R1):** x = cosh u, y = cos v, K = ½(p_u² + p_v²) + V(u, v) = 0, with V = ½F(W + 1) and
  F = g_xx(x² − 1).
- **Section Σ:** v = π/2, p_v < 0, coordinates (x, p_x). P = first return to Σ. This is V20's map; the float
  implementation is falsification/V20_ts_capture_edge_tangle/code/v20.py.
- **Reversor:** R: (x, p_x) ↦ (x, −p_x), with P∘R = R∘P⁻¹. ℓ = Fix(R) = {p_x = 0}. S = R(U), where U is the branch
  of W^u_out from z* to h.
- **Float reference values:**
  - z* = (9.8045591682, 0), λ = 38.3877;
  - brake point (x, y) = (9.854404, 0.857154);
  - x_h ≈ 56.859;
  - W^u crosses S 4 times per fundamental domain (V24 C1′).

## 1. The certificates

### C-N: the hyperbolic block at z* (hypothesis N)
- **Output:**
  - an interval box Z ∋ z* with z* unique in Z (Krawczyk on P(z) − z, using the C¹ enclosure [DP] on Z);
  - a block N ⊃ Z with coordinates (ξ, η) and cone conditions from [DP] on N (expansion of ξ-cones, contraction of
    η-cones);
  - explicit enclosures of W^u_loc and W^s_loc as graphs η = w_u(ξ) and ξ = w_s(η), with Lipschitz bounds;
  - D ∩ N = {ξ > 0, η > 0} (D's corner at z*), and the line x = x* through the complementary quadrants.
- **Float preview:** λ = 38.388; the linear relation x − x* = 0.998(ξ + η) (Fable c03).
- **Status:** feasible (quantum, HH-primary pattern), after the TS codegen.

### C-I3: the gate inequality, reformulated (Bridge suggestion, from today's sample)
- **Validated γ.** γ is a brake orbit, so validate it as the unique zero of the shooting function
  s(x₀) = p_u at the first p_v = 0 event.
  - Interval Newton in the single unknown x₀, using a C¹ enclosure of the flow from (u₀ = arcosh x₀, v = π/2,
    p_u = 0, p_v = −√(−2V)).
  - The output is a C² enclosure of the configuration curve u = g(v), v ∈ [v_b, π/2], with g′ = p_u/p_v and
    g″ = (−p_v V_u + p_u V_v)/p_v³.
  - Near the brake point p_v → 0. Reparametrise there by time, or use the local brake expansion.
- **Leaves.** g_τ = u₁ + τ(g − u₁), u₁ = arcosh 9.3, τ ∈ [0, 1].
  C(τ, v) = −V_u + g_τ′V_v + 2V g_τ″/(1 + g_τ′²), evaluated at (g_τ(v), v).
- **Certify ∂C/∂τ > 0 on [0, 1] × [v_b, π/2] ∩ Hill.** Then C(1, v) ≡ 0 holds exactly, because γ is an orbit, and
  C(τ) = −∫_τ¹ ∂C < 0 for τ < 1.
  - This avoids the degeneracy at τ → 1 that a direct "C < 0" bisection would hit.
  - The exploratory float sample (300 v × 201 τ) gives **min ∂C/∂τ = +0.632, at τ = 1 on the equator.** It is the
    same margin as Fable's C/(1 − τ), as it must be.
- **The sliver beyond the brake latitude (v < v_b).** Leaves are continued as u = const (g′ = g″ = 0), so C = −V_u.
  - **Certify V_u > 0** on Hill ∩ {u₁ ≤ u ≤ u_b, v ≤ v_b}. This is an explicit rational inequality: I1-type, no γ
    needed. The Bridge can do it with the V24 interval code.
  - **Corner condition at v = v_b.** γ's slope there is g′ ≈ −0.006 (float), so the corner between the curved leaf
    and its straight continuation is small. Lemma G needs the corner to be "convex inward". To do: state it exactly
    and check it. **This is an open logic item, Bridge.**
  - **Exploratory float geometry (2026-11-20; planning, not a test).**
    - Below v_b, the Hill region inside γ is a thin CAP, ending within 1e−3 in v. Its u-range is [u₁, ≤ u_b].
    - In the cap, min V_u = 0.999 and max |V_v| = 163.5.
    - Straight continuation (g′ = 0) gives C = −V_u ≤ −0.999, but has a corner.
    - C¹ slope-matched linear continuation has no corner, but max C = −0.0010 over 6e6 samples: too thin.
    - **Design choice to make:** a continuation with g″ > 0 (the 2Vg″ term is ≤ 0 in Hill), or the straight one plus
      a corner lemma. Bridge to decide and register before checking.
  - **DECIDED (V24 addendum D, PASS on a sample).** Use the C¹ linear continuation. Fable's straight continuation has
    the wrong corner sign (REVIEW_LOGIC addendum).
    - On the cap: C < 0 (max −0.0096 over 592k points), with −C ≥ 52·r, where r = distance to the brake point.
    - **Certificate:** interval C < 0 on the cap minus a disc of radius ρ₀ around the brake point, plus a jet lemma
      inside the disc. The jet lemma uses quantum's brake-point jets and needs V_v(brake) ≠ 0 (already certified
      for #4).
- **Status:** feasible. Parallel with C-N, independent.

### C-L: one validated curve (F-b′, U1, C1, C2)
- **Representation (agreed with quantum).** Do NOT box-enclose W^u pointwise; λ^8 wrapping would kill it.
  - Take a parametrised local unstable segment from C-N: a fundamental domain {(ξ, w_u(ξ)): ξ ∈ [ξ₀, λξ₀]}.
  - Propagate it as C¹ sets (Lohner; zonotope/doubleton where the wrapping test says so), split into short
    parameter pieces.
  - Area preservation means transverse errors do not grow. Only the injected integration error and the wrapping
    matter.
- **Conditions to certify, all 1D along the arc parameter s:**
  - **(U1/F-b′)** Up to h, the curve stays above ℓ (p_x > 0) and is a graph over x. Float min p_x on the interior
    = 6.0e−5.
  - **(C1)** For every piece of the outside arcs, the next 6 images return and miss cl(D). D's boundary is U ∪ S,
    with S = R(U), so this is a comparison of the curve with its own mirror image.
  - **(C2)** P^{j₀} of each outside arc lands in N ∩ {ξ ≤ 0, η > 0}, with j₀ = 2 (Fable).
- **Near the crossings the gap → 0 by definition, so precision there is not the issue.** Split each outside arc into:
  - **core pieces**, where the certified gap |p_x| − U(x) is bounded away from 0. Float: the gap is ≥ 1e−7 except
    within ~1% of the arc length of a crossing;
  - **end pieces** at each crossing, where the derivative of the signed gap along s has a certified sign. That gives
    a unique simple zero, which is T.
- **Float dry run first (quantum's suggestion):** the injected error per return and the width growth per piece. The
  Bridge can provide its float U, S and crossing parameters (V24 C1′ JSON).
- **Status:** feasible if formulated right; the heaviest item. 128-bit MPFR plus zonotopes is likely needed.

### C-T: transversality at the primary points
- **At h ∈ ℓ = Fix(R):** S = R(U), so the tangents at h are v = (a, b) and Rv = (a, −b). The crossing is transverse
  iff a ≠ 0 and b ≠ 0, i.e. U's tangent at h is neither along nor perpendicular to ℓ. This is one C¹ enclosure of
  U's tangent at h.
- **At the other crossings** (m, and the two further crossings found in V24): a certified sign change of the gap
  with a nonzero derivative (from C-L end pieces).
- **Open question (Bridge, cheap):** are the 4 crossings per fundamental domain symmetric points on Fix(R) and
  Fix(P∘R)? Their spacing is exactly a quarter period in log s (V24). If so, every crossing is a symmetric homoclinic
  point, and each T reduces to the h-type check.
- **Status:** feasible once C-L exists.

### C-I1/I2 (already interval-checked by the Bridge, V24)
- To call them proved, rerun them under an audited interval library: quantum's Arb, or mpmath.iv cross-checked
  against Arb. Cheap.

## 2. Order (agreed with quantum's reply)
1. TS codegen into CAPD, with its gates (quantum, 1–2 days).
2. C-N.
3. C-I3, in parallel with C-N. The sliver inequality and the corner condition are on the Bridge side now.
4. A float dry run of C-L.
5. C-L certified.
6. C-T.
7. The Bridge assembles the theorem and checks each certificate's output against §1.

## 3. Where Opus might get stuck (for the later Fable discussion)
- **The corner condition at the brake latitude** for Lemma G (logic). Probably easy; to do today.
- **Wrapping in C-L.** If zonotopes at 128 bits are not enough for 8 returns near the fold of W^u, a
  parameterisation-method W^u_loc with a high-order validated remainder may be needed. That is engineering, not
  insight.
- **No step here currently looks like it needs Fable's kind of help.** The reduction is done. What remains is
  validated numerics, plus one small logic item.
