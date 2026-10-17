# V15 FINDINGS: the Manko–Novikov equatorial ring singularity

Pre-registration: PREREGISTRATION.md (bf73ce2). Four independent Opus agents (Q1–Q4), plus the verifier (V) after them.
Status: Q1–Q4 are in; V (adversarial verifier) is running.

## Q1: existence map — PASS (all registered checks)
- **Equatorial reduction (verified, sympy plus 50-digit numerics).**
  - On y = 0: P₁ = 0, P₂ = −1/2, and a(x,0) = −b(x,0) identically.
  - B(x,0) = (x+1−(x−1)b²)², and A(x,0) = −(x+1−(x−1)b²)((x+1)b²−(x−1)). So A = 0 wherever B = 0.
- **Closed form.** With s = arcoth x, κ = √(1−χ²) and β = q/κ³, B = 0 on the equator ⇔
  **β (cosh s − 1)² (cosh s + 2) = s + artanh κ.** The ratio LHS/RHS is strictly monotone in s, so:
  - **exactly one equatorial ring for every q > 0 and every χ ∈ (0, 1);**
  - none for q ≤ 0 (Kerr, q = 0, has none: negative control PASS).
  - Bridge spot-check of the closed form at the V13 roots: residual 2.8e−12 (C0) and −8.0e−12 (F5-R), consistent with
    the 12 printed digits.
- **Registered roots.** C0 1.929828258521150 (Δ 1.2e−12); F5-R 1.921922587916760 (Δ 3.2e−12); (0.6, 0.1024)
  1.075962201195 (Δ 1.2e−9). No other root at any of the three. PASS (≤ 1e−9, ≤ 1e−9, ≤ 1e−6).
- **R < 0.5 boundary.** The ring is at R < 0.5 iff q < q*(χ) = (1−χ²)^{3/2}[asinh 2 + artanh√(1−χ²)]/(2(1+√5)).
  At χ = 0.9, q* = 0.0245. Confirmed on a 103 × 401 grid with 0 mismatches.
- **Off the equator.**
  - q > 0: no zeros (numeric scan plus edge asymptotics; partially verified, not a proof).
  - q < 0: exactly one ±y pair of off-equator B = A = 0 rings for every χ. Verified on the unreduced B at 60 digits.
    Example: χ 0.9, q −1 gives x ≈ 1.69, y ≈ 0.80.
  - Direct minimisation of B finds exactly one zero at each of 8 test points.
  - The q < 0 rings do not affect V13 (all its points have q > 0), but the V13 domain discussion should mention them.

## Q2: curvature singularity — singularity CONFIRMED; the strict per-side slope criterion FAILS on one side (reported as registered)
- **Analytic, partially verified:**
  - B = |A₊|², A = Re(A₋Ā₊) and Ernst ℰ = e^{2ψ}A₋/A₊. ℰ satisfies the Ernst equation to ~1e−99.
  - On the equator A₋ = −2(1+a²) ≠ 0, so ℰ and f have simple poles at the ring.
  - The Ernst equation forces the pole to be holomorphic in W = (ρ−ρ₀)+iz. Predicted |∂_yA₊/∂ₓA₊| = R_s matches to
    25 digits.
  - The leading local metric is a vacuum pp-wave (all invariants vanish), so naive power counting is wrong.
  - ASSUMED, not derived: the first correction behaves as in Kerr. That gives
    K ≈ 48 cos 6θ_W / (ρ₀²Λ²|W|⁶), i.e. **K ∝ d⁻⁶ in coordinate distance (proper distance s ∝ d², so ∝ s⁻³)**, with
    12 nodal directions.
  - The coefficient law is checked numerically at 4 rings (C0, F5-R, (0.6, 0.1024), Kerr's ring): K·δ⁶ matches to
    3.5e−7. The ring is asymptotically type D.
- **Numerical route, new and independent of v13_kretschmann:**
  - 2+2 block-Riemann formulation with exact sympy derivatives, mpmath at 100 digits (a 150-digit repeat agrees to
    77 digits).
  - Kerr control: matches the closed form to ≥ 98 digits at 3 points. Negative control (C0, x 5, y 0.3):
    K = 0.08357926…, finite and smooth.
  - **Ricci:** R_abR^ab / K ≤ 7e−160 at the ring points (vacuum holds to working precision).
- **Registered criteria:**
  - Agreement with V13 at C0, d = 1e−3: **PASS** (Δ 1.2e−12 and 9.9e−14). All 16 V13 values agree to ≤ 1.4e−10.
  - Exponent vs fitted slope (d 1e−2…1e−5) within ±0.1:
    - x > x_s: −5.930 (C0), −5.929 (F5-R): pass.
    - **x < x_s: −6.128 (C0), −6.121 (F5-R): FAIL by ~0.03 beyond the band.**
    - Off-axis rays: x = x_s, ±y −6.049; diagonal (+,+) −5.967; **diagonal (−,+) −6.310 (outside the band).**
  - **Bridge reading:** the prereg says "both sides" without saying pooled or per side. We take the STRICTER, per-side
    reading, because choosing the lenient one after seeing the data would be tuning. **Criterion: FAIL as registered.**
  - **Cause (post hoc, labelled as such):** the d = 1e−2 point is pre-asymptotic. On the inner side K is still
    negative there. The local slopes over the last decade are −6.004, −5.996, −6.002, −5.998 and −6.00001 on every ray.
  - So the exponent −6 is supported by the local slopes and the analytic coefficient match. The registered fit window
    was simply too wide.
  - This does not change the verdict that the ring is a curvature singularity. K grows without bound on every ray, by
    ~6 orders of magnitude per decade in d.
- **Caveat carried to V:** Q2 and V13 share the V9 transcription. Their agreement checks the curvature codes, not the
  transcription.
  - Ricci-flatness cannot settle the GLM Eq. 3h "−2" ambiguity: moving the −2 outside the sum multiplies e^{2γ} by
    e^{8β}, which is still vacuum but has a conical axis.
  - So V must decide (iii) by **axis regularity** (e^{2γ} = 1 on the axis, elementary flatness) and an independent
    transcription source. Ricci alone is not enough. This sharpens the prereg's test (iii).

## Q3: geometry at the ring (verified at C0 and F5-R; generic structure verified symbolically)
- **Local forms at C0:**
  - A ≈ −118.8 δx − 1121 y² (linear in δx);
  - B ≈ 204.8 δx² + 557.9 y² (positive-definite; ≈ 788 d² in Weyl coordinates);
  - the numerator N of g_φφ: N(x_s, 0) = 0, N ≈ 1126 δx + 1778 y².
- **Pole, not zero:** f = e^{2ψ}A/B ∝ 1/d. ω tends to a finite nonzero limit (11.02 at C0; 11.04 M at F5-R), so
  g_φφ ≈ −ω² f ∝ 1/d.
  - g_φφ → +∞ from the outside (ergoregion side) and −∞ from the inside (CTC side), and stays finite along the
    vertical tangent.
  - What vanishes is ρ²/f, the norm of ∂_φ + ω∂_t. This is the same structure as Kerr's ring, and the code
    reproduces Kerr's g_φφ to 1e−45.
- **Generic triple meeting (symbolic):** on the equator, with F = (x−1)a² − (x+1):
  - A, C and Q are each divisible by F, and B = F², so A = C = Q = N = 0 at every ring, for every (χ, q).
  - The ergosurface and the g_φφ = 0 curve both pass vertically through the ring and are tangent to each other.
  - The construction fails only if λ = 1 − 3β/R_s³ = 0 or ω_ring = 0.
  - The sector ordering (CTC-only inside, ergo-only outside, a thin lens with both) is verified at C0 and F5-R only.
- **CTC region at C0** (partially verified): bounded, with ρ < ρ_s = 0.71945 and |z| ≤ 0.91976. The ring is its
  outermost point. Three lobes: one equatorial, and a mirror pair touching the horizon rod. Whether the lobes are
  disjoint, and the structure near x = 1, are unverified.

Files: code/v15_q{1,2,3}_*.py; results/v15_q1_existence.json, v15_q1_map.svg, v15_q2_curvature.json,
v15_q2_analytic.md, v15_q3_geometry.{json,md}, v15_q3_c0*.png/svg. Env: the conjecture_machine venv (Python 3.14.5,
sympy 1.14.0, mpmath 1.3.0, numpy 2.4.6), as recorded in each JSON.

## Q4: literature (results/v15_q4_literature.md, screening record results/v15_q4_screen.json)
- **Verdict: no paper we could legitimately read identifies a curvature singularity off the horizon in MN.**
  - Full text read closely [verified]: Gair–Li–Mandel 2008; Brink 2008; Lukes-Gerakopoulos–Apostolatos–Contopoulos
    2010; Contopoulos et al. 2011 and 2012; Lukes-Gerakopoulos & Contopoulos 2013; Bambi & Barausse 2011; Bambi &
    Lukes-Gerakopoulos 2013; Johannsen 2013; Destounis & Kokkotas 2021; Staelens et al. 2023; Wang–Chen–Jing 2018;
    Dey et al. 2022; the Yunes Living Reviews article; the Geyer 2013 thesis; four Manko-group papers.
  - Keyword screen of full text [partially verified]: 284 further papers. 40 non-arXiv works were checked on metadata
    or abstract only. Text inside figures cannot be screened.
- **Brink 2008 Fig. 10 ("No singularities outside")** [verified on the rendered page]: a label inside a cartoon,
  making a family-wide claim with no parameter point or computation behind it. Brink's Fig. 6 parameters work out to
  χ 0.9, q 0.95, the same as C0.
- **Not read:** MN 1992 (CQG 9, 2477; the IOP page is behind a captcha, not circumvented, and it is closed access
  elsewhere); Castejon-Amenedo & Manko 1990; Manko 1990 (CQG 7 L209); Manko et al. 1998.
  - **So "not identified in MN 1992" is UNVERIFIED.** Johannsen 2013 cites MN 1992 only for "naked singularity".
- **Closest precedents** [verified]:
  - Kodama & Hikida 2003 (Tomimatsu–Sato δ=2): Ψ₂ ∝ B⁻³ at the equatorial B = 0 point where the inner ergo-boundary
    meets the equator, with g_φφ having a pole there. This is the same structure as Q2/Q3.
  - Manko 2011 (arXiv:1110.6564): a vacuum ring singularity sits where the stationary-limit surface touches the
    CTC-region boundary. This is the Q3 geometry, but it has not been applied to MN by anyone.
- **Unrecognised traces at ρ ≈ 0.72** [our inference; unverified]: GLM's touching point of the CTC and bound regions;
  the E- and L-independent inner boundary of allowed motion in Contopoulos et al. 2011/2012; the deep
  effective-potential hole in Lukes-Gerakopoulos et al. 2010; Geyer's g_φφ blob.
- **For the Manko email:** the honest framing is "we could not find this in the literature we could read, and we
  could not read MN 1992, so we're asking whether it is already known". It is not "new".
