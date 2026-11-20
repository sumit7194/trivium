# V23 review: the analytic steps of Fable's THEOREM_DRAFT (mn_melnikov). Bridge, Opus 5.5, 2026-11-20

Scope: `fable_work/mn_melnikov/THEOREM_DRAFT.md` §2–§4 (Theorem A, Theorem A′, Corollary B) together with SETUP.md §1–§4.
The numbers are in V23 FINDINGS (REPRODUCED). This file covers the logic only.

## Verdict: SOUND IN STRUCTURE, with three things to close before the theorem can be stated as proved

**Checked and agreed:**
1. **The Mino-time reduction is legitimate.** K_β = Σ_Kerr(H_β + ½) is analytic near cl(Γ₀) under (K4). On {K_β = 0} its
   flow is a time change of the geodesic flow on H = −½, and the physical level stays at K = 0 for every β. At β = 0,
   K₀ = K_r + K_θ is an exact product.
   - This is Robinson's setting: a 4-dimensional reduced phase space; (A1) with F = K_r; (A2) with γ₀ the unstable
     spherical orbit and Γ₀ the shared separatrix component.
   - The periodic orbit continues into {K_β = 0}, because a hyperbolic periodic orbit of a Hamiltonian lies in a
     one-parameter family indexed by energy.
2. **Convergence.** dK_r = 0 on γ₀, so the Melnikov integral is absolutely convergent (Robinson's Remark 3.10).
3. **Symmetry.** Evenness of L follows from the reversors (R₁) and from r_h(−λ) = r_h(λ), z(−ψ) = z(ψ). The even-harmonic
   rule matches V19 and is confirmed numerically in V23 (odd harmonics ≈ 0 for MN; even ones ≈ 0 for the y-odd
   sabotage).
   - Lemma S (symmetric homoclinic orbits persist) holds by the transversality of Fix R_i to W^u₀ within the level.
     The argument is standard.
4. **Step 6 (Moser's argument).** It is correct as written: λ-lemma accumulation plus the identity theorem for
   s^m g(u, s). It gives exclusion on any connected open U ⊃ γ_β ∪ Γ_β, in the real exterior. No complexification is
   used.
5. **Theorem A′'s finite-branch argument.** Correct.
   - Near p, the zero set of a nonconstant real-analytic F − F(p) in the 2D section is a finite union of analytic
     half-branches ending at p (Łojasiewicz).
   - A W^u arc through Pⁿ(q) cannot lie on the W^s_loc branch. If it did, W^u and W^s would coincide near Pⁿ(q),
     hence everywhere by analytic continuation, contradicting (N′).
   - So some other branch meets W^s_loc at points accumulating at p, and must equal it. Contradiction.
   - Note that it needs (N′) only, not transversality. That makes "D ≠ 0 ⟹ no real-analytic integral near the tangle"
     the cleanest certified target: one number, sign-definite.
6. **Corollary B.** The (E, L, μ) rescaling and the descent of F to the reduced level are fine. The uniform β₀ comes
   from the implicit function theorem at a nondegenerate zero. Fine.

**To close (none is a known gap; all three are "not yet verified by a second party"):**
- **(i) The bracket form.** That M = ∫{K_r, K₁} dλ = Υ_θ L′(ψ₀) was checked numerically by Fable alone (its c2). V23 only
  recomputed L. A second implementation of the bracket integral at a few ψ₀ would close it. (The boundary-term
  argument in MELNIKOV §1 reads correctly: equal Mino phases at both ends.)
- **(ii) Robinson 1996's exact hypotheses and conclusions** (Theorems 3.3–3.5, Remark 3.10) were read only by Fable. Someone
  should read pp. 1–6 at source and check (A1), (A2), the smoothness class, and the sign convention.
- **(iii) Certification of the one number.** L₂ ≠ 0 (equivalently D ≠ 0 for Theorem A′, and L″(0) ≠ 0 for Theorem A)
  with interval arithmetic. The margin is 1e11 over the Kerr floor, so this is a formality, but it is the formality
  that makes it a theorem.

**Wording for any write-up (until (i)–(iii) close):** "for small nonzero quadrupole β, the Manko–Novikov geodesic flow
has transverse homoclinic orbits near Kerr's inclined zoom-whirl orbits, and admits no real-analytic first integral
(commuting with p_t and p_φ) on any region containing that tangle. This is conditional on one numerically computed,
not yet interval-certified, Melnikov coefficient (independently reproduced, V23)". β₀ is not explicit, so β = 1/5 and
β = −1/3 are NOT covered.

## Item (ii) CLOSED (2026-11-20): Robinson 1996 read at source (pp. 1–7; file ~/Downloads/mel.pdf, downloaded with Sumit's OK)
- **Setting:** an autonomous H^ε = H₀ + εH₁ + O(ε²) on a 4-dimensional phase space, with:
  - (A1) X₀ completely integrable with a second independent integral F;
  - (A2) a hyperbolic periodic orbit γ₀ with Γ₀ = comp[W^u(γ₀) \ γ₀] = comp[W^s(γ₀) \ γ₀], two-dimensional.
- **M is defined inside the perturbed energy surface (H^ε)⁻¹(h₀), h₀ = H₀(γ₀),** as ∂_ε[F∘ζ^u − F∘ζ^s]. That matches the
  draft's use: the physical level K = 0 is fixed for all β.
- **Thm 3.3:** a nondegenerate zero of M(·, h₀) on Γ₀ gives a transverse homoclinic orbit for small ε ≠ 0. The proof
  cites the implicit function theorem and ref. [10].
- **Thm 3.4:** M = lim ∫_{−T*}^{T} (DF·Y) dt, with the end times chosen so that the limit points coincide (conditional
  convergence in general).
- **Remark 3.10:** if DF ≡ 0 on γ₀, the integral is an ordinary improper integral from −∞ to ∞. That holds here:
  dK_r = 0 at (r_u, 0).
- **Thm 3.5:** differentiation under the integral sign, given absolute convergence. **Remark 3.6:** any coordinates are
  allowed.
- **Conclusion:** the draft's use of Robinson (A1)–(A2), Thms 3.3–3.5 and Rem. 3.10 is accurate. The sign convention
  (u minus s) matters only for the sign of the splitting, not for the existence of a nondegenerate zero.

Only item (iii) is still open: interval certification (assigned to quantum's Arb tools).

## Item (iii), stage 1: CERTIFIED (quantum, d338e00, qsim/mn_melnikov/RESULT.md; 2026-11-20 16:05)
- **L₂ = [−4.77482114974644e−5 ± 6.81e−20],** Cauchy tail (≤ 4.0e−30) included. It EXCLUDES 0.
  - The midpoint agrees with V23 to 5.3e−11 relative.
- **Gates:**
  - Krawczyk radius 1.6e−35, containing V23;
  - parity L₁ contains 0;
  - Kerr controls (∂M, ∂a) contain 0, at ≤ 4.2e−23;
  - the sabotage L₁ = 210.18566494 excludes 0;
  - G5 run as written after a disclosed post-run finding: 10 points, 5 of them complex, worst 1.5e−38.
- **Consequence: Theorem A′ is no longer conditional on a numerical coefficient.** For small nonzero quadrupole β,
  the MN geodesic flow has no real-analytic first integral (commuting with p_t, p_φ) on any region containing the
  zoom-whirl tangle.
  - It now rests on: the certified L₂; Robinson's theorem (read at source); and the reviewed argument.
- **Still open:**
  - stage 2, L″(0) ≠ 0 with the higher-harmonic bound (T3), for Theorem A (transversality and horseshoe);
  - an explicit β₀. β = 1/5 and −1/3 are still NOT covered.

## Item (iii), stage 2: in progress (quantum; S2-A1 cabccc9; 2026-11-20 evening)
- **L₄ = [−5.31274262510e−10 ± 7.4e−22]** (Arb, gates included). V23's floats: N_χ 256 gives −5.3127361e−10
  (1.2e−6 relative off) and N_χ 512 gives −5.3127390e−10 (6.8e−7 off). So V23 converges towards the certified value,
  inside the registered 1e−6 rule. No FINDING.
- **Must-fail holomorphy controls PASS** (both INVALID-POINT):
  - (σ, τ) = (0.17, 0.6) fails at Re λ 0.050, Im λ 0.170, near the r_h pole;
  - (0.07, 1.35) fails at Im χ −1.316, where z_m cosh τ = 1.
- **Amendment S2-A2 (pre-count; labelled as after L₄ and after the debug runs at the off-grid point (0.02, 0.1)).**
  - **Why.** Plain interval evaluation of the integrand has a dependency factor of ~5000, from quadrupole cancellations.
    So the registered box rule for C is infeasible.
  - **New route.** C ≤ √(2 I2h/κ) by Cauchy–Schwarz with weight sech(κλ). The integrand of I2h is |G|² cosh(κλ), with
    |G|² = G(w)G(w̄) holomorphic. It is enclosed with nested acb.integral on [0, 2] × [0, π], plus an analytic tail.
    The Bridge checked the constant and the tail by hand.
  - Grid, b, tube, gates, pass rule and controls are unchanged. T3 is monotone in C, so any rigorous C̄ ≥ C keeps the
    pass rule rigorous.
  - **Bridge conditions (approved with these):**
    1. the second factor is evaluated at (λ − iσ, χ + iτ), never as conj(·);
    2. branch-checking (analytic) evaluation everywhere in the integrand, whatever flag is passed in;
    3. a real-analyticity gate, G(w̄) ∋ conj G(w), at random tube points;
    4. a known-value control of the nested-integral mechanism, with a pole 0.02 off the λ segment.
  - **Debug only (not counted).** At (0.02, 0.1): C ≈ 9.1, T3 ≈ 24, so it does not close there, as expected with
    q = 0.45. At the far corner it closes if C < ~880.
