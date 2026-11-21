# Digest: "Only Kerr among two-centre data". What the symmetry axis says about hidden integrals of geodesic motion

*Status: a draft digest, the first under fleet/PROCESS_DIGEST_FIRST.md. For an outside relativist or dynamicist.*
*Provenance and tools: argument drafted by Claude Fable 5.2 (2026-11-19/20, Sumit's personal account); reviewed and
checked by the Bridge (Claude Opus 5.5); first-order classification re-derived by ansatz-machine (Claude Opus).
Human direction: Sumit Pal. Checks: falsification/V25_only_kerr_checks; ansatz §158.*

## 1. Why it matters
- **Kerr (with Schwarzschild as its static case) is the only known asymptotically flat vacuum black hole whose
  geodesics are integrable.** Its fourth constant,
  the Carter constant, comes from a hidden symmetry (a Killing tensor). Every "bumpy" deformation people have
  studied numerically (Manko–Novikov, Zipoy–Voorhees, Tomimatsu–Sato) shows chaos somewhere.
- **The folklore is that integrability singles out Kerr.** That folklore is what makes "look for chaos in extreme-
  mass-ratio inspirals" a test of the Kerr hypothesis for LISA. Markakis (MNRAS 441, 2974 (2014)) states it as a
  conjecture: a stationary axisymmetric vacuum spacetime is integrable iff it is Kerr. He proves only a Newtonian,
  polynomial-integral analogue. We found no theorem of this kind in the relativistic setting (section 11).
  Killing-tensor work covers only integrals polynomial in momenta, and only for named metrics or static classes.
- **What this result adds.** A proof covering a large class:
  - rational axis data whose real part has at least two distinct poles;
  - an arbitrary rational twist;
  - integrals of any functional form, provided they are meromorphic near the complexified axis geodesics.
  In that class, integrability forces Kerr (Kerr–NUT without asymptotic flatness). Two families are covered
  automatically: every "static twin" (Kerr's mass profile without its rotation) and every two-rod-type solution.

## 2. The result, stated carefully
Assume the following:
- a stationary axisymmetric vacuum metric, regular on an outer segment of the axis;
- axis Ernst data e(z) = f0(z) + i c0(z), rational, asymptotically flat;
- f0 has at least two distinct poles;
- timelike axis geodesics with L = 0, over an open interval of energies.

**Conclusion.** If the geodesic flow has a complete set of first integrals that are meromorphic on a complex
neighbourhood of the (punctured) complexified axis geodesic, then the metric is Kerr.

**Not claimed** (the boundary matters as much as the result):
- **"Kerr is the only integrable one."** Two single-centre classes are not touched:
  - Schwarzschild's f0 with any twist;
  - a double pole, as in Zipoy–Voorhees δ = 2 and its twisted relatives.
  At this order the axis gives no condition there, for structural reasons.
- **Integrals that are real-analytic outside the horizon but do not continue meromorphically into the complex axis.**
  For Kerr-type data that complex region includes the ring points z = ±ia. A physicist's "nice integral" need not
  continue there. This is the physical-meaning caveat (section 6).
- **Non-rational axis data.** A one-parameter family of non-rational twists on Kerr's f0 passes every test used here.

## 3. How you could have found it (the motivated route)
1. **Where to look.** A stationary axisymmetric vacuum solution is fixed by its Ernst potential on the axis, e(z). A
   test that reads only e(z) could therefore classify all solutions at once. The axis geodesic exists in every such
   spacetime and is explicit. So use it as the particular solution in Morales–Ramis theory:
   - integrability implies that the differential Galois group of the variational equations along that orbit has a
     commutative identity component;
   - this holds at every order (Morales–Ramis–Simó).
2. **First order sees only the mass profile.** The normal variational equation along the axis is
   v″ + (3/16)(P′/P)² v = 0, with P = E² − μ²f0. It depends on f0 = Re e alone.
   - Its singular points are the zeros and poles of P.
   - Kovacic's algorithm only needs to count them: solvable iff s + 2h ≤ 4 (s simple points, h heavy ones).
   - For rational f0 this is deg f0 ≤ 2. Every axis profile more complicated than "two centres" is out, rotating
     Tomimatsu–Sato δ = 2 included.
   - ansatz re-derived this independently: confirmed at generic energy, with one wording fix ("generic E").
3. **The obstacle: the twist is invisible at first order.** Kerr's f0 with no rotation (the "static twin") passes.
   So does Kerr's f0 with any other rotation profile. The first-order test cannot tell them apart.
4. **The key observation: the twist enters first at third order, and only as (c0″)².**
   - Expanding the metric near the axis, the twist appears in the ρ⁴ coefficient of the L = 0 potential.
   - The third-order Galois condition becomes a residue condition on five explicit differentials.
5. **The trick that makes it computable: subtract a known integrable reference.**
   - Every f0 with two simple poles is the f0 of a (possibly complexified) Kerr–NUT solution. That solution is
     integrable, so all its residues vanish.
   - For any other twist with the same f0, the residue therefore comes only from the difference
     [(c0″)² − (c_ref″)²] D³.
   - The hard twist-free part never has to be computed.
6. **Two local lemmas finish it.**
   - **Lemma P (at a pole of f0).** The principal parts with zero residue form a single line. This forces the twist's
     residues to satisfy r² = −m², i.e. c0 = ±c_KerrNUT.
   - **Lemma X (away from the poles of f0).** A twist pole anywhere else always leaves a nonzero residue for some
     energy. The proof continues to the energy at which a turning point reaches the twist pole, where the residue
     blows up.
     - **The critical case**, where two turning points merge, was closed this week. There the blow-up coefficient is
       a Taylor coefficient of e^{c′ arsinh ξ}. It vanishes only for integer c′, and an exact identity forces
       c′² = −w²/2 ∈ {−2, −8}.

## 4. The key idea in one paragraph
The symmetry axis is a single orbit that every stationary axisymmetric spacetime has, and the whole spacetime is
coded in data along it. At first order that orbit sees only the mass profile, and it allows at most two "centres".
The rotation is invisible until third order. There it must cancel, residue by residue, against what Kerr's own
rotation would produce. Only Kerr's rotation (or its mirror image) cancels exactly.

## 5. Why this target (choice reasoning)
- **Alternatives considered:**
  - more numerical chaos surveys: many exist; they give evidence, not proofs, and they work one solution at a time;
  - Killing-tensor classifications: geometric, but blind to non-polynomial integrals;
  - a second particular solution (for example equatorial circular orbits), as Maciejewski–Przybylska–Stachowiak did
    for Zipoy–Voorhees δ = 2 (cited from memory; to check). That works one family at a time.
- **Why the axis.** It is the one orbit that exists universally, is explicit, and is parametrised by finite data. That
  turns "all solutions" into "all rational functions of a given degree".
- **What made it doable.** The Ernst axis-data parametrisation, Morales–Ramis–Simó, and the reference-subtraction
  trick (section 3, step 5).

## 6. The physical-meaning check
- **"Meromorphic near the complexified axis orbit" is the precise class of integrals excluded.**
  - It includes the Carter constant, and every integral polynomial or rational in momenta with analytic coefficients.
  - It does not obviously include an integral that is smooth outside the horizon but singular at complex points of
    the axis (z = ±ia for Kerr-type data).
  - For the physics question (chaos in inspirals), real-analytic integrals on the physical region are what matter. The
    gap between the two classes is a real caveat, not a technicality.
- **Only L = 0 is used.** The L ≠ 0 sector is not needed for the obstruction. It might add conditions that remove the
  non-rational family (open).
- **Asymptotic flatness** is used only to drop the NUT charge.

## 7. What is checked, and how
| ingredient | check |
|---|---|
| twist enters only as (c0″)² at ρ⁴ | V25 P1: two derivations, exact Kerr to 1e−52 |
| reference residues vanish (Kerr, Kerr–NUT, complexified) | V25 P2: true geodesics, own code |
| closed-form residue at a pole of f0 | V25 P3: 13/13 cases (after fixing our own derivative-factor bug; first run VOID) |
| Lemma P identity and null space | V25 P4: exact; null space is the predicted line to pole order 12 |
| two-rod example obstructed | V25 P5 |
| single-centre cases NOT obstructed at third order | V25 P6 (as Fable said) |
| first-order classification (deg ≤ 2) | ansatz §158, independent Kovacic count |
| Lemma X, critical case | V25 addendum B: exact identity; scaling at rate σ; integer-exception control |
| logic, step by step | V25 REVIEW_LOGIC (sound given ingredients) |

## 8. What we learned, including surprises and mistakes
- **Fable's own first version overclaimed.** On 11-19, Fable's first-order note said the axis leaves "Kerr–NUT and a
  small degree-2 family". That forgot the twist is free at first order. Fable corrected it itself the same day, and
  the correction is what led to third order.
- **The closed-form residue is better grounded than the draft said.** It follows from the reference's integrability
  plus Lemma P, not only from numerical matches.
- **Our own errors:**
  - a wrong derivative factor voided the first numerical run;
  - a Richardson-extrapolation floor was too high;
  - a pass rule was applied below the arithmetic floor.
  Each one is recorded and fixed under a labelled amendment.

## 9. Open (what would make it "only Kerr")
1. **Single-centre data** (Schwarzschild's f0 with twist; Zipoy–Voorhees δ = 2 type). This needs a different orbit or
   fifth order. It is the hardest part, and the real wall.
2. **The non-rational family** on Kerr's f0: try the L ≠ 0 sector, or fifth order.
3. **Non-rational axis data in general.**
4. Small items:
   - the pole-at-infinity variant of Lemma X (a sketch);
   - writing out that κω_i(E) is non-constant;
   - a full-text read of Brink III/IV and of the Morales–Ramis literature beyond MPS 2013 (first-pass literature
     check done, section 11).

## 10. Talk test (can we explain it?)
We can explain every step above, Fable's included.

**Outreach status.** Ready for outreach, with the first-pass literature check done (section 11). The framing is:
- a partial proof of Markakis's conjecture;
- in the class of meromorphic integrals near the complexified axis;
- for rational two-centre axis data.

Before sending:
- read Brink III/IV in full, since they are the closest in setting;
- ask an expert in the Morales–Ramis school whether anything unpublished or obscure overlaps.

## 11. Prior work (first-pass literature check, Bridge, 2026-11-20)
**Method.**
- Web searches.
- A full-text or abstract read of the closest papers; the depth is stated per item.
- INSPIRE citation lists of the four nearest works:
  - MPS 2013: 10 citing papers;
  - Markakis 2014: 14;
  - Brink IV: 15;
  - Vollmer 2017: 4.

None of those citing papers is a differential-Galois classification of stationary axisymmetric vacuum spacetimes
along the axis.

| work | what it proves | class of integrals | relation |
|---|---|---|---|
| Markakis, MNRAS 441 (2014), arXiv:1202.5228 (intro read; rest from summary) | Newtonian: quadratic constants exist only for one family; no quartic ones for vacuum potentials. Relativistic: "integrable iff Kerr", as a **conjecture** | polynomial in momenta | **Anticipates our statement as a conjecture.** Ours is a partial proof in a different integral class |
| Brink, Spacetime Encodings I–IV, PRD 78 (2008), 81 (2010); arXiv:0911.1589, 0911.1595 (abstracts only) | Killing tensors in SAV from the Ernst potential; type-D quadratic case; a suggested algebraic test for quartic Killing tensors | polynomial, of order 2 and 4 | Closest in setting (Ernst data). A test, not a classification. **Read in full before outreach** |
| Vollmer, J. Geom. Phys. 115 (2017), arXiv:1602.08968; PRD 92 (2015), arXiv:1506.06926 (abstracts) | No nontrivial Killing tensors up to valence 7, 9 and 11 for TS, the C-metric and ZV; valence 3 reducible in the static Weyl class | polynomial, bounded valence | Complementary (named metrics) |
| Kokkinos, arXiv:2608.22523 (2026; partly read) | No irreducible rank-2 Killing tensor in the static Weyl class | quadratic | Complementary (static) |
| Maciejewski–Przybylska–Stachowiak, PRD 88 (2013), arXiv:1302.4234 (read earlier, fleet LITERATURE.md) | ZV δ = 2 non-integrable via equatorial orbits, first-order Kovacic | meromorphic | Same method on one metric. Our class (ii) needs this kind of second orbit |
| arXiv:1111.4690, 1206.0660 (titles only) | no 6th-degree integral for ZV; non-integrability of ZV | polynomial / numerical | Complementary |
| arXiv:gr-qc/0701065 (snippet only) | numerically, TS δ = 2 geodesics "appear integrable" | numerical | **Conflicts** with the fleet's TS δ = 2 obstructions (first-order axis count: deg f0 = 4; the V20 tangle). Worth a footnote |

**Reading.** As far as this check reaches:
- the result is new as a theorem;
- its target statement was anticipated as a conjecture (Markakis);
- its setting was anticipated by Brink's Ernst/Killing-tensor programme (polynomial integrals only).

**Not exhaustive:**
- no full-text read of Brink;
- the Morales–Ramis community's own work (Maciejewski, Przybylska, Combot, Morales-Ruiz) was searched only through
  citations of MPS 2013.


**Addendum (2026-11-21, novelty search; see digests/NOVELTY_SEARCH_2026-11-21.md).**
- New prior art: Kokkinos 2026, "Killing tensors of Weyl's class" (arXiv:2608.22523). It shows that no
  two-Killing-vector member of Weyl's class admits an irreducible rank-2 Killing tensor. That is a different
  integral class from ours (meromorphic).
- Dolan 2019 (read at source) calls a differential-Galois proof for Curzon–Chazy open.
- We found no prior "only Kerr" geodesic-integrability theorem, and no prior integrability use of the lower-axis
  relation.

## 12. Update (2026-11-20, late evening): single-centre data closed via the LOWER axis
- **The idea** (Fable 5.2, one-off run; checked by the Bridge in V26). An asymptotically flat solution has a second
  outer axis segment. There the axis data are 1/e_+:
  - Meinel–Neugebauer, CQG 12 (1995) 2045, eq. (35), read in the original;
  - the Bridge's own parity proof, and its own Ernst series to order 10.
- **What the lower axis shows.**
  - A twisted single-centre profile has f0^- of degree ≥ 4. It is obstructed at FIRST order (V26 N-count; an
    adversarial search found no counterexample).
  - Static double-pole data look two-centre from below and are obstructed at THIRD order (V26 B6).
  - The far lower axis is automatically regular for asymptotically flat data without NUT (V26 addendum B).
- **Resulting statement.** Among asymptotically flat stationary axisymmetric vacuum metrics with rational axis data,
  integrals meromorphic near BOTH outer axis families force Kerr, Schwarzschild or static ZV δ = 2. ZV δ = 2 is
  non-integrable by MPS 2013, through an equatorial orbit. So, with that citation, **Kerr (and Schwarzschild) is the
  only one in this class.**
- Sections 2 and 9 above are superseded on this point. What remains open:
  - non-rational axis data (including the "invisible" family; Fable has numerical first-order evidence from below);
  - the physical-meaning caveat on the class of integrals (section 6).

## 13. Update (2026-11-21 12:46): what changed on 2026-11-21 (all claims checked as listed; Gemini "Neon" outputs are UNVERIFIED until a fleet check, which is cited)
**Provenance.** Several steps below were first produced by Google's Gemini 3 ("Neon") on Sumit's accounts and then
checked independently by the Bridge or a sister session. Outreach must say so plainly: name which steps came from
which tool and how each was checked.

### 13.1 The remaining Only-Kerr lemmas and the single-centre case
- **Lemmas X-infinity and G3** (Neon T6): checked exactly at their cores (V25 addendum C).
- **The single-centre case from scratch** (Neon T3 + T9: lower-axis trick plus classification): matches V26 (V26-E,
  degree counts; the ZV delta = 2 control).

### 13.2 The "invisible" non-rational family is now covered
This is Kerr's f0 with a branched twist, (c0'')^2 = (8/(5a^6(u^2+1)^6)) B(u^2, k). It passes the third-order test.
- **First-order non-integrability** (Neon T8 for one spin, T11 for every spin a in (0, 1)):
  - Bridge exact checks V26-F/G;
  - ansatz's independent 50-digit monodromy V26-H, agreeing to ~1e-11 at three energies;
  - k = 4 is not an exception (ansatz).
- **The allowed parameter range k < 30/7 for every spin** (Neon T14, the U_a separation): the Bridge re-implemented
  the interval certificate independently (V26-J, 449 boxes, PASS).
- **The "G1 gap" found by ansatz's second reading** (zeros of P must also stay in Re z > a): closed by Neon T19.
  Independent Bridge certificate V26-K:
  - exact E-elimination (sympy);
  - four interval certificates (one after a labelled fix to the Bridge's own enclosure; the registered FAIL is kept
    on record);
  - an end-to-end winding of exactly 2 at 28 parameter points.
- **Exceptional parameters (ansatz gap B):** the theorem holds for all k in (-infinity, 30/7) except a discrete,
  possibly empty set K*(a). At spin 0.6, K* is empty on [-10.5, 4.05] by a 50-digit argument-principle count
  (registered; PASS).
  - Caveats: floating point, not interval; one spin; nothing below -10.5; first-order lower-axis NVE only.
  - One energy per k suffices for Morales-Ramis, so the single spin, not the single energy, is the limitation.

### 13.3 Non-rational axis data in general (K5): much narrowed, not closed
- **Curzon-Chazy** (f0 = e^{-2M/z}): the axis NVE reduces to a hypergeometric equation, giving SL2 at every energy
  (Neon T16; Bridge exact check V27-A). We found no prior differential-Galois proof: Dolan 2019 calls one open, and
  Georgiev 2019 uses a different route.
- **Theorem 1, the annulus winding-number obstruction** (Neon T21): a circle with |m| >= 2, N + P >= 3 and a small
  eta forces SL2.
  - Bridge hand re-derivation plus V27-B on Neon's example (B2-B5 PASS; B1 registered FAIL from a Bridge harness
    bug, with a labelled diagnostic).
- **Theorem 2:** every transcendental entire f0 of order 0 with log n(r) = o(sqrt(log r)) gives SL2 (Neon T21/T22).
  It includes all functions of finite logarithmic order.
- **An independent referee pass** (Neon T24, a separate session): both theorems TRUE, with five minor repairs. One
  real numeric slip: e^{3pi alpha_2/2} = 27.9988, not "> 28"; "> 27" suffices, and the Bridge confirmed the value. A
  corrected write-up is in progress (Neon T28).
- **Residual open class:** transcendental meromorphic data that is "balanced" (|m| <= 1 on all large circles)
  without a small-tail rational approximant of degree >= 3, and fast-growing entire data with no degree >= 3
  rescaling limit and no Theorem 1 circle.

### 13.4 Literature (Bridge novelty search, digests/NOVELTY_SEARCH_2026-11-21.md)
- We found no prior work on:
  - the axis-NVE route for Curzon-Chazy;
  - the lower-axis use for integrability;
  - an "only Kerr" theorem for meromorphic integrals.
- New prior art to cite: Kokkinos 2026 (arXiv:2608.22523), which rules out irreducible rank-2 Killing tensors. That
  is a different, polynomial-integral statement.
- **Still to do before sending** (section 10): a full read of Brink III/IV, and the question to a Morales-Ramis expert.

### 13.5 Current statement, for outreach
Among asymptotically flat stationary axisymmetric vacuum metrics, geodesic integrability by integrals meromorphic near
both outer axis families forces Kerr or Schwarzschild in either of two settings:
- rational axis data (ZV delta = 2 excluded via MPS 2013);
- Kerr's own mass profile with the invisible branched-twist family, except possibly a discrete set of k for each spin
  (none found where tested).

Open, stated plainly:
- non-rational axis data in general (narrowed to the residual class above);
- the physical-meaning caveat on the class of integrals (section 6);
- a certified (interval) version of the exceptional-k count.
