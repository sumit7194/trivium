# V26: independent check of Fable's single-centre result (lower-axis route). Bridge, 2026-11-20 evening, before any code
**Claim under test** (fable_work/only_kerr_single_centre/REPORT.md):
- **(L)** On an asymptotically flat solution, the axis data below the source are e_-(z) = 1/e_+(z). Equivalently
  ξ_-(z) = −ξ_+(z), with ξ = (1 − e)/(1 + e) and e_+ continued analytically in z.
- **(N)** Rational, asymptotically flat, single-centre data (f0 with one pole, simple or double, or f0 ≡ 1) with
  c0 ≢ 0 give deg f0^- ≥ 4, where f0^- = f0/(f0² + c0²).
- Hence first-order obstruction on the lower axis.

The Bridge works only from the claim statements. Fable's scripts are NOT run or reused.

## Checks
**L-src.** Read Meinel–Neugebauer, CQG 12 (1995) 2045 (arXiv:gr-qc/0302114) in the original PDF, and quote the
relation they state between the two axis potentials.
- PASS if it states (L), or something equivalent to it, under stated hypotheses.

**L-proof (by hand, Bridge).** A parity induction on ξ = Σ r^{−(n+1)} F_n(cos θ).
- Show F_n(−u) = (−1)^n F_n(u), using:
  - the Ernst equation for ξ;
  - regularity of F_n on [−1, 1] (both axes regular);
  - the kernel of the order-n Legendre operator.
- Write it out in FINDINGS. It must identify every hypothesis used.

**L-num (own code).**
- **Method.** Solve the Ernst equation for ξ order by order in 1/r (sympy, exact rationals), from random complex
  upper-axis moments, to order 10. Use 3 random seeds and 1 seed with real moments (the static control).
- **PASS** if ξ(θ = π) = −ξ_+ exactly, at every order.
- **Must-fail.** At the same orders, the "mirror guess" e_-(z) = e_+(−z) and the guess e_- = conj(e_+(z)) must both
  be violated for a twisted, non-reflection-symmetric seed.
- **Exact controls (closed form, no series):**
  - Kerr–NUT with ξ = e^{iα}(px + iqy);
  - Tomimatsu–Sato δ = 2 from the V11 loader's Ernst potential (if available), or the standard α/β form;
  - Schwarzschild in Weyl coordinates.
  - Compare the actual axis values at y = ±1 with the rule.

**N-count.** For e = 1 − 2M/z + i b/z² (M = 1; b ∈ {1/2, 1, 3}): compute f0^- exactly, factor it, and list the
poles and zeros of P = E² − μ² f0^- at a generic E.
- **Expected:** 4 simple poles + 4 simple zeros (s + 2h = 8 > 4).
- **Control:** c0 = b/z (Kerr–NUT-type) gives s + 2h ≤ 4.

**N-search (adversarial).** Search for asymptotically flat rational e with single-centre f0 and c0 ≢ 0 such that
deg f0^- ≤ 2.
- **Families:**
  - e = (polynomial of degree d)/(polynomial of degree d), d ≤ 3, with the pole structure of f0 forced to one
    real point;
  - symbolic parametrisation for d ≤ 2;
  - random rational-parameter scans for d = 3.
- **PASS** (= supports N) if none is found.
- **Must-find control:** dropping asymptotic flatness, the search must find the Kerr–NUT-type twist in class D.

## Verdict
(L) and (N) are CONFIRMED if L-src, L-proof and L-num pass, and N-count and N-search pass.

**Not covered here:**
- B1 (an exact twisted single-centre metric off the axis);
- B3/B7 (certified lower-axis monodromy);
- the first-order classification, which is inherited from ansatz §158.

## Addendum A (2026-11-20, late evening, before code): B6, static double-pole data seen from below
**Claim.** Static class C, f0 = (z² − 2Mz + q)/z² with q ≠ 0 and q ≠ M² (distinct zeros). Seen from below,
f0^- = 1/f0 = z²/(z² − 2Mz + q) = 1 − m1/(z − z1) − m2/(z − z2), where:
- z1, z2 are the roots of z² − 2Mz + q;
- m1 = −z1²/(z1 − z2) and m2 = −z2²/(z2 − z1), both ≠ 0;
- c0^- = 0.

This is two-centre data with zero twist. Theorem 1 (V25) then obstructs it at third order: closed form
F = 1 + r1²/m1² = 1.

**Check.** Bridge V25 code (v25_rmap.py return map on the truncated system R; V25 P3 machinery), applied to f0^-:
- **(i)** real roots: M = 1, q = 3/4 (z = 3/2, 1/2), at E = 0.8 and 0.6;
- **(ii)** complex roots: M = 1, q = 5/4 (z = 1 ± i/2), at E = 0.8 and 0.6.
- **PASS:** the cubic return-map coefficients A match the closed form with F = 1, by the V25 P3 rule (error
  ≤ max(100·floor, 1e−6·scale)), and are nonzero, with no VOID.

**Controls**
- **Cancellation control:** the same f0^- with the complexified reference twist (c0 = c_ref) must give A ≈ 0 (F = 0).
- **Exact check:** ZV δ = 2 (q = M²) from below has a double pole (f0^- = z²/(z − M)²). So it is not two-centre and
  stays undecided, as claimed.

## Addendum B (2026-11-20, late evening, before code): item 2 (regularity of the lower outer axis), instead of a full exact metric
**Why the change.**
- B1's first aim (does the lower-axis value equal 1/e_+?) is now settled by L-src, L-proof and L-num. The series IS
  the solution off the axis near infinity.
- What remains open is the physical caveat: is the lower outer axis regular, with no Misner string and no conical
  defect, for asymptotically flat twisted data?

**Argument (by hand, to check).** In Weyl–Papapetrou form, ∂_θ ω = r² sin θ ∂_r χ / f², where χ = Im e. So the jump of
ω between the two outer axis segments, along a large semicircle, tends to −2 × (the 1/r coefficient of χ), i.e. to
the NUT parameter. With c0 = O(z⁻²) there is no jump. ω is constant along each regular axis segment, so both are
zero. γ → 0 at infinity on both segments likewise.

**Check (own series code, v26_L solver).** Take e_+ = 1 − 2/z + i b/z² (b = 1), to order 10, and compute
Δω(R) = ∫₀^π R² sin θ ∂_r χ / f² dθ at R = 20, 40, 80.
- **PASS:** |Δω| decreases like R^{−1} or faster, towards 0.
- **Must-fail control:** add a NUT term (+ i n/z, n = 1/2). Δω must tend to −2n·(sign convention), i.e. a nonzero
  limit, within 1e−2 at R = 80.
