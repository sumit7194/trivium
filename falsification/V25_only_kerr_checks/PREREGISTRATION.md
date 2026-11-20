# V25: independent checks of Fable's "only Kerr" draft (fable_work/only_kerr/), part 1: Fable's P1 (near-axis series), pre-registration

*2026-11-20, written before any V25 code. Sumit: review the three Fable results one at a time.*

**Target.** VE_DERIVATION.md §2. Near a regular axis, F1 = f e^{−2γ} and F2 = 1/f − fω²/ρ² satisfy:
- F1₂ = −f0″/4 + f0′²/(2f0) and F2₂ = (f0 f0″ − f0′²)/(4f0³), both twist-free;
- F1₄ = F1₄^static(f0) − (c0″)²/(64 f0) and F2₄ = F2₄^static(f0) − (c0″)²/(64 f0³).

That is, the twist enters only at ρ⁴, and only as (c0″)². Fable tested it on Kerr (exact) and a static metric. The
twisting non-Kerr case (TS δ=2) is untested; that is its own proposed check P1.

**Disclosure.** I read VE_DERIVATION.md §0–§3, THEOREM_DRAFT.md §1–§3 and CHECKS_PROPOSED.md, but none of Fable's check
code or outputs. I do NOT use Fable's F1₄^static.

**Independence.**
- **F1₄^static and F2₄^static:** I derive them myself in sympy from the static Weyl equations. ψ is axisymmetric
  harmonic, ψ = Σ a_n(z)ρ^{2n} with a₀ = ½ ln f0; γ_ρ = ρ(ψ_ρ² − ψ_z²) with γ(0) = 0; F1 = e^{2ψ−2γ}; F2 = e^{−2ψ}.
- **TS:** the Bridge's own TS2 metric (V11 loader, ts45, σ = k = 1), converted to Weyl form:
  - f = −g_TT and ω = −g_Tφ/g_TT;
  - e^{2γ} = f g_xx(x² − 1)/(x² − y²);
  - (x, y) from (ρ, z) by R± = √(ρ² + (z ± 1)²), x = (R₊ + R₋)/2, y = (R₊ − R₋)/2.
- **Axis data f0(z) and c0(z):** from the TS Ernst potential at y = 1 (the form verified in outreach/PROBLEM; f0 checked
  equal to −g_TT(x, 1)), with c0 = Im of the Ernst E on the axis.

## Check (mpmath, 50 digits)
- **Coefficients.** At z ∈ {2.5, 4, 7} (real outer axis, z = x), extract the ρ², ρ⁴ coefficients of F1 and F2 by a
  degree-6 polynomial fit in ρ² over ρ ∈ [1e−3, 1e−2] (12 points).
  - **Gate:** the fit is stable. Coefficients from two point sets (12 and 16 points) agree to ≤ 1e−20 relative.
- **PASS (TS):**
  - F1₂ and F2₂ match the formulas to ≤ 1e−15 relative.
  - (F1₄ − F1₄^static(f0)) / (−(c0″)²/(64 f0)) = 1 ± 1e−12, and the same for F2 with f0³.
- **Controls:**
  - **Kerr** (kerr45, p = 4/5; the same pipeline, twisting): must also pass. That's the must-pass.
  - **Static Weyl** (ZV δ=2, c0 = 0): F1₄ = F1₄^static to ≤ 1e−15. A must-pass with zero twist.
  - **Must-fail:** replace c0″ by 1.1·c0″ in the TS prediction. The ratio must then be off by ~21%, which shows the
    check is sensitive.

## Verdicts
- **CONFIRMED:** the gate, TS, Kerr and ZV all pass.
- **FALSIFIED:** TS fails beyond tolerance while the controls pass. In particular, a ρ⁴ difference not proportional
  to (c0″)².
- **VOID:** the gate or a must-pass control fails.

**Not covered here:** P2–P6 (return maps; residues; Lemma P; the two-rod example; ZV and Schwarzschild), the Galois
step, and the inherited first-order classification.

---

## Addendum A (2026-11-20, before any P2–P6 code): Fable's checks P2–P6, Bridge constructions only

**Disclosure.**
- I have now read CHECKS_PROPOSED, DEGREE2_FAMILIES, KERR_CONTROL and VE_DERIVATION in full.
- I have NOT read any of Fable's check code or outputs (checks/*.py, *.out), and I will not.
- The predictions below are Fable's, copied from CHECKS_PROPOSED.

**Common machinery (own code).**
- **R-full.** At L = 0 the geodesic flow on H = −μ²/2 is exactly system R. The independent variable is z; the
  variables are (ρ, p); p_z = √(2U(ρ², z) − p²); dρ/dz = p/p_z; dp/dz = ∂_ρU/p_z; U = (E²F2 − μ²)/(2F1).
  - F1 and F2 come from an EXACT metric, continued complexly with R_i = (z − b_i)√(1 + ρ²/(z − b_i)²) (principal
    root).
  - p_z is continued from q0 = y/Δ by p_z = q0√(1 + (2(U − U0) − p²)/q0²).
- **R-trunc.** The same, but with U built from F1 and F2 through ρ⁴:
  - my own static-Weyl series (V25 P1, sympy), plus the twist terms −(c0″)²/(64f0) and −(c0″)²/(64f0³) confirmed
    in P1;
  - U is then re-expanded through ρ⁴.
  - It needs only f0 and (c0″)². Fable's h_4 formula is NOT used.
- **Loop.** z = z_c + r e^{iθ}, θ ∈ [0, 4π]: twice around a puncture that is a branch point of y² = ND, and once
  around an unbranched one.
  - Integration: solve_ivp DOP853, rtol 1e−13, t_eval = [end].
  - y and u (du = dz/y) are integrated along the loop.
  - u − u_P is obtained from a radial segment in t = √(z − z1).
- **Basis.** X± = e^{±κ(u − u_P)}(√Δ, (Δ′y/(2Δ) ± κ)/√Δ), with κ² from the two-pole formula.
  - Self-check before use: X± satisfy VE_1 (dρ/ds = p, dp/ds = 2U₂ρ, ds = Δdu) to ≤ 1e−10 at 5 points.
- **Return map.** Start at ε(c₊X₊ + c₋X₋) and read the end point in the X± basis.
  - A(ε) = (c_end − c)/ε², at ε ∈ {0.02, 0.01, 0.005}.
  - A = Richardson (4A(ε/2) − A(ε))/3, using both pairs.
- **FLOOR FIRST (control-clause rule).** Measured before any verdict, for every case:
  - the linear return map's deviation from I (ε = 1e−7 run, divided by ε);
  - |A(r₁) − A(r₂)| for two loop radii;
  - |A from (0.02, 0.01)| − |A from (0.01, 0.005)|.
  - floor = the max of these. "Zero" means |A| ≤ 100·floor. "Matches" means |A − pred| ≤ max(100·floor, 1e−6|pred|).
  - A case with floor > 1e−4 is VOID.

### P2. The Kerr control and the static twin with TRUE geodesics (R-full)
- **Data.** Prolate units σ = 1. M = 5/4, a = 3/4 (Fable's M = 1, a = 3/5). Puncture z1 = −M + ia. E = 4/5 and also
  E = 7/10; μ = 1.
- **(a) Kerr.** The V11 kerr45 metric.
- **(b) The static twin.** Own implementation of the Weyl formula in CHECKS_PROPOSED P2, with b shifted to prolate z
  (b = (1, −1, −M + ia, −M − ia), ε = (+1, +1, −1, −1)).
  - **Validated first:** its ρ² and ρ⁴ coefficients equal my own static series to ≤ 1e−12.
  - **Validated first:** the Weyl equation γ_z = 2ρψ_ρψ_z holds at 3 real points (finite difference, ≤ 1e−8).
- **Predictions.**
  - Kerr: A = (0, 0), from either start.
  - Twin: from (1, 0), A = (−π/2, π); from (0, 1), A = (π, −π/2). Both independent of E.
- **Must-pass cross-check.** R-trunc on the twin's (f0, c0 = 0) gives the same A as R-full (within the floor).

### P3. The closed-form residue swept (R-trunc, Fable's coordinates)
- **Prediction** for start (1, 0) at puncture z1: A = (−3πi m2 F/(5δ), 6πi m2 F/(5δ)), with δ = z1 − z2 and
  F = 1 + r1²/m1².
- **Sets:**
  - Kerr M = 1, a = 3/5, E = 4/5, twist λ c_ref with λ ∈ {0, ½, 1, 3/2}, so F = 1 − λ²;
  - the same at E = 7/10 (λ = 0);
  - Kerr M = 1, a = 4/5, E = 13/10 (unbound, λ = 0);
  - Kerr–NUT-type z1,2 = ±i/2, m1 = 1 − 0.4i, m2 = conj, E = 7/10, with λ ∈ {0, 0.7};
  - real poles z1 = 1, z2 = −½, m1 = ¾, m2 = ½, E = 3/5, with c0 = 0 (F = 1), with c0 = ½/(z − 1) − ½/(z + ½)
    (F = 13/9), and with the complexified reference twist (F = 0).
- **Falsified if** any value disagrees, or if a twist with r1 ≠ ±i m1 gives zero.

### P4. Lemma P
- **(i)** The three-term identity for (d_u² − w²κ²)v^k: exact sympy, for general symbols (k symbolic, w ∈ {2, 4}).
- **(ii)** Own residues from local series. With t = √(z − z1), du = 2dt/g(t) and g = √(N(z)(z − z2)), compute the
  residue of (z − z1)^{−k} e^{wκu} du for k ≤ 12, w ∈ {2, 4}, at 20 energies, for the Kerr-type, Kerr–NUT-type and
  real-pole parameters (mpmath, 60 digits).
  - Find the null space of the E-independent principal parts, by SVD with a gap ≥ 1e20.
  - **Prediction:** dimension 1, spanned by the principal part of v³ − (3m2/(5m1))v.
- **(iii)** R-trunc return maps for Kerr's f0 (M = 1, a = 3/5, E = 4/5) with (c0″)² = (c_K″)² + Q/D³.
  - **Prediction:** Q1 = (1/3)[v³ + v⁻³ − (3/5)(v + v⁻¹) − 4/5] gives (0, 0), and Q2 = (1/3)(v³ + v⁻³) gives
    (−π/24, π/12).

### P5. A real two-rod-type example (R-full)
- **Data.** The static Weyl solution with f0 = 1 − (3/4)/(z − 1) − (1/2)/(z + 1/2), built as in P2 with real b. Loop
  around z1 = 1, E = 3/5.
- **Prediction:** A = (−0.6283i, 1.2566i), i.e. −3πi m2/(5δ) and its partner.
- The twisted version and the reference control are in P3 (R-trunc).

### P6. The negative claims (R-full on ZV δ = 2; R-trunc on Schwarzschild's f0)
- **(a) ZV δ = 2** (the V11 zv metric; f0 = ((z − 1)/(z + 1))²).
  - **Prediction:** around the point over z = 1 (the zero of f0) and around a large circle (the point at infinity),
    the linear return map is I and the cubic part is zero, in (ρ, p) coordinates. Sheet: the one with y continued
    from the start.
  - **Secondary, not verdict-bearing:** the multipliers of the linear map around the double pole vs e^{±√2π}.
- **(b) f0 = 1 − 2/z**, with c0 = b/(z − p) − b/(z + p), b = 0.3, p = 3.
  - **Prediction:** the linear return maps around z = 0 and z = ±p are I. No torus, so cubic terms then commute
    automatically through ε³. So (b) tests only the linear parts. The cubic parts are recorded.

### Verdicts
- **P2:** Kerr zero AND twin matches → CONFIRMED. Kerr nonzero → FALSIFIED (criterion or reduction wrong). Twin
  zero → FALSIFIED (no obstruction). Twin nonzero but a different value → value FALSIFIED, obstruction CONFIRMED.
- **P3–P6:** per item, the same logic.
- A failed self-check or validation → VOID for that item.

### Addendum A, first P3/P4(iii) run, and amendment A1 (POST-RESULT; written after seeing the run)
**Result as registered.** P3 and P4(iii) are VOID as run, for two reasons.
- **(a) The VE_1 self-check failed** (relative error ~1). Cause: a coding error in the CHECK. I used d/ds = Δy d/dz;
  the correct form is (y/Δ) d/dz, since ds = Δ du and du = dz/y.
- **(b) 6 of the 13 cases have floor > 1e−4.** It is dominated by the Richardson difference (the residual ε⁴ term,
  1e−4 to 3e−4). The radius difference is ≤ 2e−5 and the linear deviation ≤ 7e−11.
- **For the record (not a verdict):** every case agreed with its prediction to ≤ 1.7e−5. Both zero-controls (λ = 1
  Kerr; the complexified reference) gave ≤ 4e−9. Q1 gave ≤ 7e−7 and Q2 matched (−π/24, π/12).

**Amendment A1.**
1. **Self-check corrected and widened.** X± must satisfy VE_1 with d/ds = (y/Δ)d/dz to ≤ 1e−8 (central difference)
   at 5 points on the loop: θ = 0, 0.8π, 1.6π, 2.4π, 3.2π. y and u there come from the ρ = p = 0 flow.
2. **Two-level Richardson.** Use ε ∈ {0.02, 0.01, 0.005, 0.0025}. Level 1: R = (4A(ε/2) − A(ε))/3. Level 2:
   RR = (16R(ε/2) − R(ε))/15. The estimate is RR from (0.01, 0.005, 0.0025); rich_diff = |RR₀ − RR₁|.
3. **Unchanged:** the floor definition (max of the radius difference, rich_diff and the linear deviation), the
   100× rule, VOID if floor > 1e−4, all predictions, all data, and all radii.

### P2/P5/P6 first run, and amendment A2 (POST-RESULT; written after seeing the P6 run)
- **P2 and P5 ran as registered (amendment A1 machinery).** All match; see FINDINGS.
- **P6 as run:**
  - **ZV around z = 1: VOID.** The cubic floor is 3.3e−3. The linear deviation from I is 1.9e−9.
  - **ZV around infinity:** identity, as predicted.
  - **Double pole (secondary):** the integration failed. The linear growth e^{√2π} ≈ 85 at ε = 0.02 pushes ρ past the
    radius of the √ continuation.
- **Diagnosis (ε scan at r = 0.3).** A(ε) grows like 1/ε²: 1e−6 at ε = 0.02, 1e−3 at ε = 0.00125. That is
  integration noise of ~1e−9 near the rod end (q0 is large there) divided by ε². It is not a cubic term.
- **Amendment A2 (for the ZV z = 1 loop only):** radii (0.4, 0.6); ε ∈ {0.08, 0.04, 0.02, 0.01}, which keeps
  ρ/|z − 1| ≤ 0.2; rtol 1e−14. Otherwise unchanged (two-level Richardson, the floor rule, VOID if floor > 1e−4).
- **Double pole (secondary, not verdict-bearing):** linear map only, from the ε = 1e−7 runs.
- **Schwarzschild-f0 loops:** run as registered.

### Amendment A2 result and amendment A3 (POST-RESULT)
- **A2, ZV around z = 1: VOID** (floor 9e3).
  - An ε scan shows the ε = 0.08 runs are garbage (A ~ 1e5). ρ leaves the domain of the √ continuation.
  - For ε ≤ 0.04, A = 0 to ≤ 1e−6 at both radii. My A2 choice of ε = 0.08 was wrong.
- **A3 (for this loop only):** ε ∈ {0.04, 0.02, 0.01, 0.005}. Radii (0.4, 0.6) and rtol 1e−14, as in A2. Everything
  else is unchanged.
- **The other P6 items are final as run under A2:**
  - ZV around infinity: identity.
  - Double pole, secondary: multipliers 85.019695 and 0.011762 vs e^{±√2π}.
  - Schwarzschild f0 + dipole: linear identity at z = 0 and ±3. (b) is verdict-bearing on the linear parts only, as
    registered.

## Addendum B (2026-11-20 evening, before code): gap G2, Lemma X in the critical case (a twist pole at a critical point of f0)
**The Bridge's argument (by hand; written up in REVIEW_LOGIC after the checks).**
- **The residue.** At a point over p, with D(p) ≠ 0 and Q = Σ_{k≤m} A_k (z − p)^{−k}, the residue is
  e^{wκu_p} R(E), where R = Σ_k A_k h_{k−1} and h_j are the Taylor coefficients at p of h = e^{wκ(u−u_p)}/y.
- **Algebraic continuation.** R is algebraic in E. So if it vanishes on an interval it vanishes identically, and
  it can be continued to ε := E² − E*² → 0, where E*² = μ² f0(p).
- **Write** φ = E² − μ² f0 (so y = D√φ) and a = μ² f0″(p)/2.
- **Critical case** (f0′(p) = 0). Then f0″(p) ≠ 0, because f0 − f0(p) has a double zero and degree ≤ 2. Scale
  t = z − p = σξ with σ² = −ε/a. Then σh(p + σξ) → M(ξ) uniformly on |ξ| ≤ ½, where
  - M(ξ) = e^{c′ arsinh ξ}/(D_p √(−a) √(1 + ξ²)), with c′ = wκ(E*)/(D_p √(−a));
  - so h_j σ^{j+1} → M_j, and R ~ A_m σ^{−m} M_{m−1}.
  - M is proportional to d/dξ e^{c′ arsinh ξ}. Its Taylor coefficients satisfy T_{n+2} = (c′² − n²)T_n/((n+1)(n+2)), so
    they vanish only if c′ is a real integer.
  - **Claimed identity:** κ²(E*) = μ² f0″(p) D(p)²/4. That gives c′² = −w²/2 ∉ {0, 1, 4, ...}. So R is unbounded and
    G2 closes.
- **Generic case** (f0′(p) ≠ 0). The same scaling with t = (ε/φ′)ξ gives M ∝ (1 + ξ)^{−1/2}, and R ~ ε^{1/2−m}.

**B1 (exact, sympy).**
- **(a)** For f0 = 1 − m1/(z − z1) − m2/(z − z2), with D = (z − z1)(z − z2) and Fable's κ², the difference
  κ²(E*) − μ² f0″(p)D(p)²/4 reduces to 0 modulo the numerator of f0′(p). Use polynomial remainder in p with symbolic
  m1, m2, z1, z2, μ.
- **(b)** The same for the double pole: f0 = Δ/(z − z1)² with Δ monic quadratic, and κ² = μ²Δ(z1)/2.
- **(c)** The resultant in p of num(f0′) and num(f0″) is not identically 0 (the critical point is nondegenerate).
- **PASS:** all three.

**B2 (numerical, mpmath, 60 digits; power-series arithmetic for h at p).**
- **Data.** Kerr-type f0 (M = 1, a = 3/5, μ = 1; poles ±ia) and a real two-pole f0 (z1 = 1, z2 = −1, m1 = 3/10,
  m2 = 1/2). At one critical point p of each, take w ∈ {2, 4}, m ∈ {1, ..., 6} and ε ∈ {10^{−2}, ..., 10^{−10}}.
- **Quantity.** dev(ε) = |h_{m−1} σ^m / M_{m−1} − 1|.
- **PASS:** for every (case, w, m), dev ≤ 1e−3 at ε = 1e−10, and dev is non-increasing over the last four ε.

**Controls**
- **Generic.** At a non-critical p (0.3 + 0.2i, both cases): the local slope of log|h_{m−1}| against log ε, between
  the two smallest ε, is −(m − ½) ± 0.05.
- **Must-show-vanishing.** Replace κ by κ_int, chosen so that c′ = 1. The model then predicts M_2 = M_4 = 0, so
  |h_{m−1}σ^m| ≤ 1e−2 at ε = 1e−10 for m = 3 and m = 5, while m = 2 stays O(1). This shows the check can see the
  integer exception.

**Not claimed.** The pole at z = ∞ and family C's other uses of Lemma X; this addendum covers only the critical-point
case at finite p.

## Addendum C (2026-11-21 ~02:30, before code): checking Gemini Neon's proofs of Lemma X-∞ and Lemma G3 (output UNVERIFIED; /Users/sumit/Github/neon_work/onlykerr/)
**C1 (exact, sympy).** For f0 = 1 − m1/(z − z1) − m2/(z − z2), D = (z − z1)(z − z2), N = E²D − μ²Δ and P4 = N·D, with
X = (E² − μ²)(z1 − z2) − μ²(m1 − m2) and S = X²/(μ⁴m1m2), the claim is:
- I = (z1 − z2)²(X² + 3μ⁴m1m2)/12;
- J = −(z1 − z2)³X(2X² + 9μ⁴m1m2)/432;
- I³ − 27J² = μ⁸m1²m2²(z1 − z2)⁶(X² + 4μ⁴m1m2)/256;
- j = 256(S + 3)³/(S + 4).

Classical binary-quartic invariants, with symbolic parameters. **PASS:** all four differences simplify to 0.

**C2 (numerical, mpmath, 50 digits; exact series in t = 1/z).** Lemma X-∞, case M = (m1 + m2)/2 ≠ 0. With
Q = z^m + z^{m−1}, ε = E² − μ², the claim is
R(ε) = Res_{t=0}[Q(1/t) e^{wκs(t)} (ds/dt) dt] ~ ∓(−1/2 choose m−1)(2Mμ²)^{m−1} ε^{−m+1/2}.
- Cases: Kerr-type (m1 = m2 = 1, z1,2 = ±0.6i) and asymmetric (m1 = 3/4, m2 = 1/2, z1,2 = 1, −1/2); m = 1..4;
  w = 2; ε = 1e−4, 1e−6, 1e−8.
- **PASS:** |ratio − 1| ≤ 1e−2 at ε = 1e−8 in every case, decreasing as ε → 0.
- **Must-fail control:** m = 0 (Q regular at ∞) gives a residue of 0 to 1e−40.

**C3.** Lemma X-∞, case M = 0 (m2 = −m1). The claimed leading coefficient is A·(polynomial in α), with α² = −w²/2.
Check the ratio to the claim at m = 1..4 (w = 2).
- **Must-fail control:** imaginary w = i√2, giving α = ±1. Then the leading coefficient must vanish at m = 3: the
  scaled residue is ≤ 1e−2 relative to the w = 2 value.

The I2 argument is reviewed by reading only. No code.
