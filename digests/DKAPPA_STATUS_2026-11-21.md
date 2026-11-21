# δκ (Cuspis): where the number stands, 2026-11-21 (digest)

*Written by the Bridge from Cuspis's experiment records (corner_function repo) and Neon outputs (neon_work/dkappa,
outside the repo). Cuspis owns this line. Neon outputs are UNVERIFIED except where Cuspis's grade is cited.*

## The question, and why it matters
In the large-N O(N) model at criticality in D = 3, the entanglement entropy of a strip of width w has a universal
term −κ·L/w. At leading order in N it is N times the free-scalar value, κ_free = 0.0396481. The O(N⁰) correction δκ
comes from the σ (Hubbard–Stratonovich) sector. Its value, and above all its sign relative to the registered threshold
(δκ/κ_free compared with −0.450), says whether the interacting fixed point carries more or less "strip
entanglement" than free fields predict. It is a clean, universal, computable number that tests how entanglement
behaves in an interacting CFT. Nobody has computed it before, as far as the line's searches show.

## What was settled on 2026-11-21
1. **The continuation to n → 1 (the replica limit).** The fleet needs Q′(1) for Q(n) = log det B_n − n·log det B₁.
   - T36 (Neon) proposed splitting the inner sum. Cuspis FALSIFIED it with a pure-gauge toy whose exact answer is 0;
     T36 gave 0.904 + iπ.
   - T40 (Neon) kept the inner summand unsplit, so the gauge phases cancel (α-type 0). Cuspis's checks then
     VERIFIED it on a stand-in lattice: held-out exact-base fits to 1e-67, and Q′(1) = −1.38691 ± 2e-4 against
     T40's −1.38687.
   - Along the way Cuspis and the Bridge both wrongly trusted a Newton-series minimum (−1.4207). The remainder holds
     confluent n·aⁿ terms that are not completely monotone, so the series dips and then recovers. Neon T40b diagnosed
     it, and both of us retracted. Lesson recorded: exact-base fits with held-out validation are the referee.
2. **Growth bounds (Neon T40c/T40d).** At transverse momentum q = 0 the two-edge problem separates exactly under the
   bipolar map ζ = ln(z/(z−w)), which gives a polynomial bound. For q > 0 it is NOT closed: the precise obstruction is
   that q²Ω² is not H₀-bounded. Numerics stay bounded.
3. **The lattice engine (Cuspis EXP-081).**
   - EXP-081a: the first engine omitted the saddle term. Its "universal" ratio grew with the box, which is impossible,
     and that signature exposed the omission. Fixed with engine-path controls, including a saddle-off regression.
   - Edge geometries are numerically unusable at large imaginary twist (e^{2π Im α} conditioning).
   - EXP-081b replaces them with a STRIP PAIR (W = 2 and 4) in the same box. The free-side box systematic is
     measured at ±4%. A 40-digit referee (N2′, own poles) PASSES. Production is running; no R value has been seen.
4. **The infinite-volume route (Neon T46/T46b).**
   - A Chebyshev-Galerkin boundary-integral method gives κ_free in exact infinite volume to 5e-4, in seconds and with
     < 50 MB (Cuspis reproduced this).
   - The saddle term is resolved there (d·r → −1/32 reproduced by Cuspis).
   - A discretisation inconsistency spoils s ≳ 1.
   - The first prototype, δκ/κ_free ≈ −0.2 ± 0.5, is NOT converged and partly not reproducible from the code
     delivered. Cuspis graded it partial. T46c asks for one consistent discrete operator, free-side ratio convergence
     and the complete code.

## Target-choice reasoning
The lattice route gives a first sign estimate with a measured uncertainty (±10–20% expected). It is limited by the
box: brute force cannot reach the continuum on this Mac, and only partly on a cloud machine. The infinite-volume route
is the precision route. Running both lets each check the other. A quiet-night r = 8 point was approved by Sumit, but it
waits until EXP-081b passes.

## Physical-meaning check
- Everything rests on the anchored-residue continuation now verified on a toy. That it is the right continuation for
  the full 3D bubble rests on the growth bound (q > 0 is still open).
- The −1/32 saddle cancellation is checked through the engine code path, not only analytically.

## Process notes from this line
- Controls must exercise the production code path. An analytic identity is not a control of the code.
- A planted control must come from the structural class that can actually occur (confluent, not only monotone).
- Referees must be independent of what they check: own poles, never seeded by production.
- EXP-081 has had several amendments (a, b, N1′, N1″, N1‴, N2′), all registered before any R was seen. The final
  write-up must tabulate them.

## Update 2026-11-22: EXP-081b verdict
- **INCONCLUSIVE as registered** (Cuspis 62ab26f; the Bridge checked it against the analyzer output).
  - The only cause is the width nuisance σ_W = 30. Its W = 8 geometry failed the reliability rule at its first
    checkpoint, so that number measures a truncated calculation, not the nuisance.
  - Every W = 2/4 geometry is reliable to s = 6. Controls K, N2′, N_y and s-quad pass; N4 (s_cut) fails at 1.6e-4.
  - One production bug (the pole-merge tolerance) was found by the N_y control and fixed. The verdict is unchanged.
- **Descriptive only (σ_W left out, which the registration forbids):** R∞ = 2.41 ± 0.29, i.e. positive. It must not
  be quoted.
  - It is surprising next to the negative O(N⁰) corrections of C_T (−0.45) and F, and against the T46 prototype.
  - The W = 2 strip is narrow, so a lattice term that does not cancel is a live suspect.
- **Next:** EXP-081c, a new registration (081b stays on the record), re-measures σ_W with numerics that pass the
  reliability rule. It may merge with the P = 16 night run.

- **Later, 2026-11-22: a deeper check.**
  - Cuspis showed (EXP-082) that a continuation can match every integer-n value and still have the wrong n → 1 slope.
  - The lattice engine's σ-side continuation, including the saddle term, has never been compared with honest
    integer-n data.
  - EXP-083 does that at small P. If it disagrees, the +2.4 is suspended, whatever σ_W turns out to be.

## Open
- The δκ sign: EXP-081c (σ_W re-measured) and the infinite-volume route (T46d) as the independent check.
- T46c: a consistent discretisation, then a converged infinite-volume value.
- The growth bound for q > 0.
- The r = 8 night run (on hold).
