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
