# V25 review: the logic of Fable's "only Kerr" draft (THEOREM_DRAFT, VE_DERIVATION §4–§5, DEGREE2_FAMILIES §2–§5). Bridge, Opus 5.5, 2026-11-20

This file covers the arguments only. The numerical claims are tested separately (V25 FINDINGS: P1 done; P2–P6
registered in addendum A).

## Verdict: Theorem 1 / Claim A / Claim B are SOUND as deductions from their stated ingredients, on every step I re-did by hand.
The Corollary depends on an inherited first-order result (I10) that is not re-derived anywhere. "Only Kerr" in full is
not claimed, and the draft says so correctly.

## Steps re-derived by hand

1. **"All residues vanish ⟺ Q = (d_u² − w²κ²)B with B rational in z"** (used in Lemma P).
   - If all residues of Q e^{wκu}du vanish, then ∫ = R e^{wκu} with R meromorphic on the curve. Write R = A + yC with
     A, C rational in z. Then (d_u + wκ)R = Q.
   - The y-odd part gives A′ + wκC = 0.
   - The y-even part gives Q = −(1/(wκ))(y²A″ + ½(y²)′A′ − w²κ²A) = −(1/(wκ))(d_u² − w²κ²)A, because
     d_u²A = y²A″ + ½(y²)′A′.
   - So B = −A/(wκ) is rational. **Correct.**
2. **Lemma P** (given the three-term identity, which is to be checked in P4(i)).
   - The coefficient of v^k in (d_u² − w²κ²)Σβ_k v^k is m1(k−1)(k−½)β_{k−1} + ε̃θ_kβ_k − m2(k+1)(k+½)β_{k+1}. At k = 1
     the β₀ term drops out, so that equation is a constraint: the residue condition at z1.
   - **Weight 2** (θ_1 = 0): −3m2β_2 = q_1.
   - **Weight 4** (θ_1 = −3, θ_2 = 0): −3ε̃β_1 − 3m2β_2 = q_1.
   - **Solving down.** Solving from the top pole order m, each step adds one factor of ε̃. So β_2 has ε̃-degree m − 3,
     with a nonzero leading coefficient: θ_k = k² − 1 ≠ 0 for k ≥ 2 when w = 2.
   - **Bound on m.** For E-independent q_1, the weight-2 condition holding on a set of E with a limit point forces
     m ≤ 3.
   - **m = 3.** β_2 = q_3/(5m1) gives q_1 = −(3m2/(5m1))q_3. Then weight 4 gives β_1 = 2q_2/(3m1) and
     −2ε̃q_2/m1 + [the weight-2 condition] = 0, hence q_2 = 0.
   - **m = 2.** The same algebra forces q_2 = q_1 = 0.
   - So the admissible principal parts form one line, spanned by v³ − (3m2/(5m1))v. **Correct.**
3. **Claim A pole counting.**
   - **Pole order.** A pole of order n in c0 gives (c0″)²D³ a pole of order 2n + 1 at z1. That is 3 for n = 1 and ≥ 5
     for n ≥ 2, which is excluded.
   - **Simple poles.** With residues r1, r2 and v = (z − z2)/(z − z1): z − z1 = δ/(v − 1) and D = δ²v/(v − 1)². So
     (c0″)²D³ = 4(r1²v³ + 2r1r2 + r2²v⁻³), and Q = 4(r1² + m1²)v³ + const + 4(r2² + m2²)v⁻³.
   - **Conclusion.** The v¹ coefficient is 0, so Lemma P forces q_3 = 0, i.e. r1² = −m1². **Correct** (reproduced
     exactly).
4. **The closed form (I7) is better grounded than the draft says.**
   - The twist-free residue at z1 equals minus the reference-twist residue whenever the (complexified) Kerr–NUT
     reference is integrable with integrals meromorphic near its punctured axis curve.
   - The reference-twist residue is a Lemma-P computation on 4r²v³.
   - So I7 follows from the reference's integrability plus Lemma P, not only from "five numerical matches". The
     numerical cancellation (≤ 7e−29 in four data sets) is then a consistency check of that integrability hypothesis.
5. **The direction of the Galois argument actually used.**
   - Every obstruction claim needs only: monodromy ⊂ differential Galois group, plus the closure of ⟨torus element of
     infinite order, nonzero translation⟩ ⊇ G_a ⋊ G_m, which is connected and non-commutative.
   - That direction does not need the "Galois group = Zariski closure of monodromy" (Fuchsian/Schlesinger) half. That
     half is needed only for the "not excluded" statements (families C and D), which are negative claims anyway.
   - **Fuchsian character.** I checked it at the punctures over the poles of f0. Δ = f0·D is analytic and nonzero at
     z1, and the local parameter is s = u − u_P. So the first-order solutions are analytic in s, and the third-order
     integrands are meromorphic in s. The punctures are regular singular. Fine.
6. **Reduction R ⊂ full VE_3 (I2).** Sound.
   - The L = 0 one-parameter family through Γ exists.
   - Expressing the perturbed orbit as a graph over z inverts z(τ, ε) algebraically in the jets already in the field.
   - Quotients of algebraic groups map G° onto (G/N)°.
   - Also, at L = 0 solving H = −μ²/2 for p_z is exact algebra: p_z² = 2U − p². So system R with the full U IS the
     full L = 0 geodesic flow. P2 uses that.

## Gaps (carried into the Fable / proof-recipe list)

- **G1. I10, the inherited first-order classification (deg f0 ≤ 2).** The Corollary ("Kerr is the only one among
  data whose real part has ≥ 2 distinct poles") needs it to exclude deg f0 ≥ 3. It is hand-derived in an older note,
  with only the TS δ=2 instance checked (V22). **Status: open.** It needs an independent derivation, or a checked
  Kovacic count.
- **G2. Lemma X, critical case** (a twist pole p with f0′(p) = 0). This is used in Claim A to exclude twist poles away
  from the centres. The generic case is sound as an argument; the critical case is a two-line sketch.
- **G3. I12: non-constancy of κω_i(E).** It is minor, and easy in practice: κ² is affine in E² and the periods vary.
  But it is not written.
- **G4. Lemma P's three-term identity.** It is a CAS identity; checking it is P4(i).
- **G5. Single-centre data (families C and D).** This is the real wall for "only Kerr". At third order the axis
  monodromy is structurally commutative there. A fifth-order computation or a second particular solution would be
  needed. This is research, not a check.
- **G6. The invisible non-rational family.** It passes the L = 0 third-order test. It may be excluded by the L-sector
  (c0′ is multivalued), at fifth order, or by another orbit. **Open.**
- **G7. Meaning of (H-integrals).** The integrals must be meromorphic near the complexified axis curve, including near
  the complex ring points z = ±ia. A real-analytic integral on the physical exterior that does not continue there is
  not excluded. This is correctly stated in the draft; it should be kept in any write-up.

## What is established, if P2–P6 pass
- **Theorem 1:** a full proof modulo G2–G4, the MRRS theorem (literature) and the L = 0 reduction (sound).
- **Theorem 2 / Corollary:** additionally modulo G1.
