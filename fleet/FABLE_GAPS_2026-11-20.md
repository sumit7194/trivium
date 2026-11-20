# Gaps and blockers in this morning's three Fable results: a running list for the later "Fable or Opus?" discussion

*Bridge, started 2026-11-20 afternoon, updated as checks finish. Sumit asked for this. It is not a promise that Fable
will be used. Each gap is marked:*
- **OPUS-OK**: routine, or already in hand (the Bridge or quantum can do it on Opus);
- **OPUS-TRY**: real work, but worth trying on Opus first;
- **HARD**: a research step where we may get stuck; a candidate for Fable if Opus stalls.

## 1. MN Melnikov (physical-class non-integrability for Manko–Novikov)
- **State.** Reproduced (V23); logic reviewed (sound); Robinson's theorem read at source. Everything rests on one
  number: certification is quantum's Arb run (relaunched 13:33 after its own nan bug; ~2.5 h).
- **M1. Certify L₂ ≠ 0 (Theorem A′) and L″(0) ≠ 0 with a bound on the higher harmonics (Theorem A).** OPUS-OK
  (running).
- **M2. β₀ is not explicit.** The theorem covers only "small enough" quadrupole β. The physical-looking values
  β = 1/5 and β = −1/3 are NOT covered. Fixing this needs either:
  - an explicit β₀ (a quantitative implicit-function bound: OPUS-TRY, heavy interval work); or
  - Fable's route C (CERTIFY.md): certify, at one given β, the 2×2 scattering matrix near the equatorial homoclinic
    loop. That is a CAPD-type computation: OPUS-TRY. It shares tooling with the capture-edge recipe below.
- **M3. Wording discipline.** Until M1 closes, it is "conditional on one numerically computed coefficient". Nothing
  to do but keep it.

## 2. TS capture edge (capture-edge reduction for TS δ=2)
- **State.**
  - Every input has been checked independently. Exact or interval: R, I1, I2. Sample: I3, and the lobe conditions
    C1/C2 (V24 C1′, today).
  - The lemma logic is reviewed (sound).
  - The theorem is still conditional on validated versions of these.
- **C1. A validated γ enclosure plus I3 in interval arithmetic, including the sliver beyond the brake latitude.**
  - The sliver is the one region I could not check even as a sample.
  - OPUS-TRY: a validated ODE enclosure (Taylor model or CAPD-style) of one orbit, then interval bisection of an
    explicit C[g].
- **C1b (found this afternoon). Lemma G has a gap at the brake latitude.**
  - Fable continues the leaves as straight lines below v_b. That creates an upward kink in τ, which allows exactly
    the turning-back that Lemma G must exclude.
  - Fix: slope-matched leaves, plus a small local lemma at the brake point, where the margin → 0 by continuity.
  - OPUS-TRY (Bridge). Details in V24/REVIEW_LOGIC.md, addendum.
  - **Update.** The fix was checked on a sample (V24 addendum D, PASS): C < 0 on the whole cap, vanishing only
    linearly at the brake point. What remains is the interval version plus a jet lemma, which is engineering.
- **C2. Hypothesis N: interval-Newton fixed point and cone conditions at z*.** OPUS-OK (standard; quantum has
  Krawczyk).
- **Plan of record with quantum:** recipes/TS_CAPTURE_EDGE_PROOF_RECIPE.md v1.1.
- **C3. Validated lobe conditions T, C1, C2.** W^u followed for ~8 returns.
  - The W^u–S gap falls to ~1e−7 near the crossings, so the enclosures must be tighter than that.
  - OPUS-TRY. This is the heaviest numerical item, the core of a CAPD-type proof.
- **C4. Rigorous transversality at h.** OPUS-TRY (the same machinery as C3).
- **C5 (new today). Observation to understand.** Today's W^u crosses S 4 times per fundamental domain, exactly a quarter period
  apart. Is it a symmetry? It affects how many lobes a proof must handle. OPUS-OK to investigate.
- **Merge with B-5 (the CAPD chaos-proof moonshot).** C2–C4 are exactly B-5's steps. This is the "proof recipe" to try
  writing on Opus after the reviews.

## 3. "Only Kerr" (third-order axis obstruction)
- **State.**
  - Logic reviewed (V25 REVIEW_LOGIC.md: Theorem 1 sound given its ingredients).
  - P1 confirmed: the twist enters only as (c0″)² at ρ⁴.
  - P3 confirmed: closed-form residue, 13/13 cases, own truncated system.
  - P4 confirmed: the identity is exact; the null space is exactly the predicted line to pole order 12; the invisible
    family is zero, the non-admissible case is not.
  - P2 confirmed (exact Kerr gives zero; exact static twin gives (−π/2, π)).
  - P5 confirmed (exact two-rod).
  - P6 confirmed as tested (ZV and Schwarzschild-f0: no third-order axis obstruction, as Fable said).
  - So Theorem 1 ("only Kerr among two-centre data") stands, modulo K1/K2 and the literature theorem.
- **K1. I10: the inherited first-order classification (deg f0 ≤ 2).** The Corollary needs it. Only a hand derivation
  exists, and only one instance is checked. OPUS-TRY: re-derive the Kovacic count independently and test a degree-3
  example.
  - **Assigned 2026-11-20 to ansatz** (Sumit offered its help): an independent re-derivation of the Kovacic count, plus a
    computational check on degree-2 controls and degree-3 examples, including the merged-zero edge case.
  - **DONE** (ansatz §158, 5f14db2). The classification is CONFIRMED at generic E; the necessary direction is ~95%.
    New edge case: three merging zeros can be solvable at special E, so the wording must be "generic E". K1 is
    essentially closed for the Corollary.
- **K2. Lemma X, critical case** (a twist pole at a critical point of f0). OPUS-TRY: a careful asymptotic argument.
- **K3. Single-centre data** (Schwarzschild's f0 with any twist; ZV δ=2 and its twisted relatives). HARD.
  - This is the real wall between "only Kerr among two-centre data" and "only Kerr".
  - Here the axis orbit gives commuting monodromy at third order for structural reasons.
  - Routes: fifth-order axis equations (only for twist poles away from the centre); a second particular solution
    (equatorial orbits, as was done for ZV); or a non-monodromy obstruction.
  - This is the most natural Fable target among the three.
- **K4. The invisible non-rational family** (Kerr's f0, branched twist, passes the third-order test at every energy).
  It might be killed by the L ≠ 0 sector, by fifth order, or by another orbit. HARD-ish. OPUS-TRY on the L-sector
  first.
- **K5. Non-rational axis data in general** (first order for arbitrary analytic f0). HARD (open research).

## Where Fable would add the most (Bridge's view, to discuss)
1. **K3** (single-centre data). It is genuinely creative, and nothing on our side is close.
2. **M2 via route C or explicit β₀**, if the Opus attempt at the CAPD tooling stalls.
3. **The capture-edge proof recipe (C1–C4) is mostly engineering.** Opus first; Fable only for a specific stuck
   step.
