# V26 findings: Fable's single-centre result via the lower axis (Bridge, 2026-11-20 evening)
Environment: Python 3.14.5 (conjecture_machine .venv), sympy 1.14.0, mpmath 1.3.0; macOS 27.0.1 arm64.
Bridge code only (code/). Fable's scripts were not run or reused.

## L-src: PASS (read in the original PDF)
Meinel & Neugebauer, "Asymptotically flat solutions to the Ernst equation with reflection symmetry", CQG 12 (1995)
2045, arXiv:gr-qc/0302114 (5 pages, read in full).
- Section III integrates the Ernst linear problem along both outer axis parts. It assumes only asymptotic flatness
  and regularity for ζ > ζ₊ and ζ < ζ₋; reflection symmetry is NOT used there.
- Eq. (35): f^(u)(ζ) = (1 + G(ζ))/F(ζ) and f^(l)(ζ) = F(ζ)/(1 + G(ζ)), with one pair of analytic functions F(K),
  G(K) (Eqs. 32–36; their analyticity is stated in Section IV).
- **Hence f^(l)(ζ) = 1/f^(u)(ζ),** with f^(u) continued analytically. That is rule (L).
- Their headline result (reflection symmetry ⟺ f^(u)(ζ) conj f^(u)(−ζ) = 1) is the symmetric special case.

## L-proof (Bridge, by hand): an independent parity argument
**Hypotheses.**
- Asymptotic flatness: ξ → 0, where ξ = (1 − e)/(1 + e).
- ξ is real-analytic for r > R on a full neighbourhood of both outer axis segments, so
  ξ = Σ_{n≥0} r^{−(n+1)} F_n(u) with u = cos θ and each F_n regular on [−1, 1].

**Ernst equation in ξ:** (ξ ξ̄ − 1) Δξ = 2 ξ̄ (∇ξ)².

**Order r^{−(n+3)}.** The equation reads L_n F_n = S_n, where L_n F = ((1 − u²)F′)′ + n(n+1)F.
- S_n is a sum of products F_a F̄_b (terms in F_c), with a + b + c = n − 2.
- ∇ contributes ∂_r, which keeps the angular parity, and the term (1 − u²)∂_u·∂_u, which takes two u-derivatives
  and so also keeps the product parity.
- So if F_k(−u) = (−1)^k F_k(u) for k < n, then S_n has parity (−1)^n.

**Induction.**
- L_n commutes with u → −u.
- Split F_n into its parity-(−1)^n part and its opposite part G. Then L_n G = 0.
- The solutions of L_n G = 0 regular at u = ±1 are multiples of P_n, which has parity (−1)^n (Q_n is log-singular at
  ±1). So G = 0.
- The base case n = 0 gives L₀F₀ = 0, so F₀ is constant.

**Lower axis** (u = −1, z = −r):
ξ_l(z) = Σ (−z)^{−(n+1)} (−1)^n F_n(1) = −Σ F_n(1) z^{−(n+1)} = −ξ_u(z). **QED.**

**What both proofs need.** Asymptotic flatness, and a REGULAR lower axis segment. The series form also needs
convergence for large r. That is standard for analytic asymptotically flat solutions, but it is an assumption here.

## L-num (own code, code/v26_L.py): PASS to order 10
Ernst equation for (ξ, η = ξ̄ as an independent field) solved order by order with exact Gaussian rationals, from random
upper-axis moments. At every order, the polynomial F_n of degree ≤ n exists and is unique given F_n(1); this confirms
the series form.
- **Result.** For 3 complex seeds and 1 real (static) seed, F_n(−1) = (−1)^n F_n(1) holds exactly at every order
  n = 0..10, i.e. ξ_l = −ξ_u.
- **Wrong guesses fail** for every seed: the mirror guess e_-(z) = e_+(−z) and the guess e_- = conj(e_+).

## Exact controls (code/v26_exact.py): PASS
Rule L holds identically in closed form for:
- Schwarzschild (ξ = x);
- Kerr (ξ = px + iqy);
- Kerr–NUT (e^{iα}(px + iqy), not reflection-symmetric);
- Tomimatsu–Sato δ = 2.

The mirror guess e_-(z) = e_+(−z) fails for Kerr, Kerr–NUT and TS. It holds for Schwarzschild only because ξ_u is odd
there.

## N-count (code/v26_N.py): PASS
For e = 1 − 2/z + i b/z² (b = 1/2, 1, 3):
- f0^- has degree 4. P = E² − f0^- has 8 simple singular points (4 simple poles + 4 simple zeros), so s + 2h = 8 > 4.
- **Control** c0 = b/z (Kerr–NUT-type): degree 2, s + 2h = 4.

## N-search (adversarial): PASS (no counterexample)
**Random scan.** 6000 trials over classes D (f0 = 1 − 2/z), C (double pole) and f0 = 1. Twists had denominators of
degree 1–4, with roots placed at the centre, at f0's zero, at random rationals, or as irreducible quadratics.
Numerators were sometimes forced to vanish at f0's zero.
- Asymptotically flat twists (c0 = O(z⁻²)): minimum deg f0^- = 4 in all three classes. 0 hits with deg ≤ 2.
- **Must-find control (non-flat twists):** 700 hits with deg 2, all of Kerr–NUT type (c0 = b/z in class D, and
  c0 = b/(z − s) for f0 = 1). The search finds the known exceptions.

**Symbolic families, with resultant-forced cancellations:**
- generic degree 4–8;
- after any one parameter cancellation, the minimum is 4;
- the one exception is class C with c0 = a/z², which reaches degree 3, but only at q = ±i a, i.e. complex data, not a
  real metric. Even there, degree 3 is still obstructed at first order.

## Verdict so far
- **(L) CONFIRMED:** source read in full, own proof, own series code exact to order 10, exact closed-form controls.
- **(N) CONFIRMED** on every tested family, with no counterexample.
- **Consequence.** Twisted rational single-centre data, seen from a regular lower axis, have f0^- of degree ≥ 4. The
  first-order classification (deg ≤ 2 ⟺ solvable, at generic E; ansatz §158) then obstructs them.

**Still unchecked by the Bridge:**
- the static class-C third-order step (Fable's t4; the Bridge's B6);
- an end-to-end exact metric (B1);
- certified lower-axis monodromy (B3);
- the first-order classification itself.

**The physical caveat is now sharper.** The corollary needs BOTH outer axis segments regular, and integrals
meromorphic near BOTH axis families. A twisted single-centre solution may carry a singular lower axis (a string).
If so, it falls outside the hypotheses rather than being excluded. That needs stating explicitly in any write-up.
