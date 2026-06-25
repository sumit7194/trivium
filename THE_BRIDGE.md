# The Bridge

*A cross-validation program for three deliberately-independent projects:*
**ansatz-machine** (exact symbolic+numeric GR engine) ×
**tabula-geometrica** (neural geometry-from-observation) ×
**deepstrain** (real LIGO-data black-hole searches).

*Design doc for a working session that has all three repos checked out. Written 2026-06-17, grounded in the latest commits of each.*

---

## 0. How to read this

This is a **map, not a script.** Do not execute it top-to-bottom. Pick the spine (§3), build the smallest honest version, let results redirect. Most of what's below is optional menu.

The whole document rests on one fact you must protect: **these three projects were built with independent roots on purpose** — no project's assumptions were allowed to leak into another, so that when two of them agree, the agreement is *evidence* and not an echo. This session is where they finally meet. Read §2 before doing anything; meeting them carelessly throws away the thing that makes meeting them worth it.

---

## 1. The three oracles — what each repo uniquely gives you

Think of these as **three different ways of knowing the same physics.** The bridge is interesting precisely because the three ways are independent.

| Project | Epistemology | What it produces | Trust profile |
|---|---|---|---|
| **ansatz-machine** | Deductive — *what the equations say* | Exact metrics (discovered + proved), exact invariants/moduli, hair-count (three-valued), energy-condition class, thermodynamics (S=A/4), Killing vectors, **exact observables** (shadow, ISCO, light-bending, redshift), stellar structure (TOV/Buchdahl/max-mass), exotic spacetimes. Now has a numeric (finite-difference) track too. | Exact where it returns an answer; honest "UNPROVEN" where it can't. The **ground-truth oracle.** |
| **tabula-geometrica** | Inductive — *what a net infers from raw observation* | The legibility law (amortized→legible, free→scrambled), the economy race (bit-cost of a force: gravity 0/EM 1), the geometrization criterion (**universal ∧ conservative**), bottleneck invariant-counting, "the horizon is a steerable linear feature," and the curvature atlas (the same lens on markets / hierarchies / neural populations). | Approximate, learned, **architecturally blind to metrics** (sees only observations). The **representation oracle.** |
| **deepstrain** | Empirical — *what nature actually emitted, through real noise* | No-hair test on real ringdowns (δ, 2.6× tighter than classical, GW250114 Kerr-consistent), echo search (~1.2× edge, on-source null), subsolar/PBH search. Strict ethos: sensitivity from injections, significance from measured background, pre-registration, nulls are results. | Real but noisy; dominated by the **sim→real domain gap**. The **measurement oracle.** |

---

## 2. The one discipline that makes this worth doing

**Independence is capital you have been accumulating. The bridge is where you spend it — so spend it cleanly.**

The failure mode is not merging the engines; it's subtle — once you can see two answers, it's tempting to nudge one toward the other (pick a bottleneck width *because* you know the exact moduli count; tune a threshold so δ lines up). That spends the capital for nothing and converts evidence back into circularity.

Rules for every comparison in this doc:

1. **Obtain each measurement blind** — without the other oracle's answer in view.
2. **Pre-register the prediction and the agreement criterion** before comparing. (What number do you expect? What counts as "agree"? Decide first.)
3. **Never tune one oracle to match another.** If they disagree, that's a result, not a bug to fix.
4. **Report principled disagreements as findings.** The most interesting outcomes here are the gaps (see §5, §6).

tabula's "raw observations only, never show it the metric" rule already gives you blindness *architecturally* for the ansatz↔tabula leg — lean on that rather than willpower.

---

## 3. The spine — "how many numbers is a black hole?"

There is exactly **one statement all three projects already address, independently.** Build this triangle first; everything else is extension.

- **ansatz** *proves* the metric is fixed by (M, J, Q) — structural no-hair, established across its ladder.
- **tabula** *counts* the irreducible numbers from observation — the economy race and bottleneck-saturation are literally "how many numbers does this object need."
- **deepstrain** *tests* it on reality — ringdown QNM spectroscopy asks whether tone #1 and tone #2 imply a *consistent* (M, spin); δ is the measured deviation; GW250114 came back Kerr-consistent.

**The minimal triangle (build this, nothing more, first):**

1. Pick one family ansatz can produce exactly: Schwarzschild → Kerr (the astrophysical case, 2 numbers) and RN/Kerr-Newman (charged, 3 numbers).
2. **ansatz** reports the exact moduli/hair count. (Pre-register: 2 for Kerr, 3 for KN.)
3. **tabula** infers the count from observations of that family (bottleneck saturation width), blind. Pre-register: expect it to match.
4. **deepstrain** already has the measured side for the astrophysical case (the no-hair δ). Note whether real data is consistent with the same count.

**What the outcomes mean** (decide these before running):
- *All three give 2* → a clean triangulation: theory, representation, and measurement concur on the dimensionality of a black hole. Strong, and rare to have all three in one place.
- *tabula < exact* → the net found compressibility the parameter count misses (MDL < moduli dimension) — a genuine information-theoretic finding, not a failure.
- *tabula > exact* → the net is wasting capacity / hasn't converged — a learnability diagnostic.
- *deepstrain disagrees with theory* → either astrophysical complication or a real no-hair deviation; the exact + learned legs help localize which.

---

## 4. Pairwise bridges — the menu

Each item: **question → concrete experiment → interface → what it validates → honest size.**

### 4A. ansatz ↔ tabula (exact vs learned)

- **Invariant-count cross-measure.** Does tabula's neural bottleneck-count equal ansatz's exact moduli/hair-count? *Interface:* observables (ansatz now emits shadow/ISCO/light-bending — tabula's native input; feed it those, never the metric). *Validates:* both tools at once. *Size:* methods; agreement is a real validation milestone, the MDL≠moduli gap is the interesting part.
- **Conjecture handoff (highest-leverage, both halves are finished this week).** tabula discovered "*a force geometrizes ⟺ it is universal ∧ conservative*" from trajectories. Hand it to ansatz's prover: energy conditions (36) for the source, a timelike Killing vector / conserved energy for the "conservative" half. *Validates:* turns a cheap neural pattern into an exact statement on the catalog. *Size:* the physics is essentially the equivalence principle + dissipation-isn't-geometric (known) — the value is the discovery→proof pipeline working end to end.
- **Shadow-edge fidelity score.** ansatz's exact b_crit = 3√3 ≈ 5.20 M vs tabula's learned photon map (~5.76 M, ~11% high). *Experiment:* sweep how deep into the strong field tabula's training data reaches, watch the shadow edge march toward 3√3. *Validates:* a quantitative **strong-field learning curve** — how well the net learns the region no observation-only net wants to learn. (First, measure b_crit from the net's *null geodesics*, not the brightness threshold, to separate metric error from renderer artifact.)
- **Exact solutions as clean training data for the legibility law.** Use ansatz's exactly-labeled families instead of toy sims to re-run the amortized-vs-free legibility experiments. *Validates:* the legibility law on the cleanest possible data.
- **Leg-3 regime prediction.** tabula's refined Leg 3 says structure restores legibility *only when the conserved quantity must be inferred through dynamics* (indirect observation). ansatz knows exactly which quantities are conserved and how they couple — so it can **predict per-system whether tabula is in the direct or indirect regime** before tabula runs. *Validates:* a falsifiable cross-engine test specific to the legibility law.

### 4B. tabula ↔ deepstrain (learned vs real) — the domain-gap bridge

This is the pair with the **biggest practical payoff**, because deepstrain's dominant pain is the sim→real domain gap (it parked the ringdown tone-count and capped the PBH learned models), and tabula's whole subject is *when learned codes survive a change in distribution.*

- **The legibility law as a sim→real diagnostic (the headline idea).** Reframe the domain gap as a legibility question: is deepstrain's learned ringdown-parameter code **amortized (encoder-inferred → should transfer) or free/stored (→ scrambles under shift)?** The legibility law predicts which representations survive sim→real. *Experiment:* probe the transfer-failing models with tabula's linear-vs-nonlinear probe ladder; check whether the codes that fail to transfer are exactly the ones the law says will scramble. *Validates:* a genuinely new framing for sim→real transfer in GW ML — and possibly a *fix* (force amortization where the model currently stores). *Size:* if it works, this is the most original thing in the whole bridge, because it's the rare case where the abstract law makes a concrete prediction about a real-data failure.
- **Horizon-feature transfer.** tabula found "the horizon is a steerable linear feature" in simulated data. Does that linear direction appear in / transfer to real ringdown representations? *Validates:* whether a learned strong-field feature is real-data-robust.
- **Bit-count / DOF on real ringdowns.** How many numbers does a *real* ringdown irreducibly need? The no-hair test already answers "consistent with 2." Cast it as a DOF count and compare to tabula's neural MDL on simulated ringdowns. *Feeds:* the §5 triple count.

### 4C. ansatz ↔ deepstrain (exact vs real)

- **Exact templates to shrink the gap at the source.** ansatz can emit exact QNM-relevant structure and exact observables; to the extent deepstrain's domain gap comes from *approximate* simulation templates, exact ground truth can narrow it. *Validates:* whether exactness helps where approximation hurt.
- **Exact echo structure for the echo search.** deepstrain searches for echoes (a signature of exotic near-horizon structure) and found on-source null. ansatz has exotic spacetimes (wormholes, etc.) and can compute their exact near-horizon/echo-relevant structure. *Experiment:* generate exact echo-producing metrics, derive the template structure, inform deepstrain's comb. *Validates:* an exotic-object template grounded in exact GR rather than phenomenology.
- **Proof ↔ test on no-hair.** The cleanest pairing: ansatz's *proved* no-hair statement vs deepstrain's *measured* δ. Same statement, two epistemologies. (Completes the spine with the exact leg.)

---

## 5. The full triangle — all three at once

- **The no-hair triangulation** (the spine of §3, completed): theory says 2, representation infers 2, measurement is consistent with 2. Three independent ways of knowing, concurring on the dimensionality of a black hole.
- **The strong-field frontier.** All three care about the same region — the light ring at r=3M. ansatz computes it *exactly*; tabula learns it *imperfectly* (the shadow-edge / QNM-frequency error); deepstrain *measures* it (ringdown frequencies are sourced from exactly there). Two new questions only the triangle can ask: (a) is tabula's strong-field weakness in the regime real ringdowns actually constrain? (b) can ansatz's exact strong-field structure be used to *target* tabula's training (a curriculum) and pull the shadow edge to 3√3?
- **The MDL ↔ moduli ↔ measured-DOF triangle.** Three counts of "numbers a black hole needs": neural MDL (tabula), exact moduli dimension (ansatz), measured effective DOF from real ringdowns (deepstrain). Build the table. *Where they agree* is triangulation; *where they part* is the content — MDL below moduli means hidden compressibility, measured below theory means real data can't resolve a DOF, theory below measured would be the interesting one.

---

## 6. New dimensions of thinking this unlocks

Approaches to deliberately rotate through (the "think like a biologist / economist" instinct, made concrete):

- **The triangulation lens (the meta-method).** Most researchers have one or two of {deductive, inductive, empirical}. You have all three, kept independent. A claim that survives all three is confirmed in a way that's genuinely hard to get. *This* is the asset — not any single experiment.
- **The information-theorist's lens.** Stop asking "is it Kerr?" and ask "how many bits is a black hole, measured three ways?" The §5 count triangle is this lens. It reframes no-hair as a statement about *irreducible information*, which travels further than the GR-specific framing.
- **The ML-theory lens.** Domain gap = legibility (§4B). This is the one place an abstract result (the legibility law) makes a falsifiable prediction about a concrete real-data failure. If it lands, it's portable to all of ML, not just GW.
- **The two-level ground-truth lens.** tabula can be validated against *exact* labels (ansatz: does it match the idealized theory?) and *real* labels (deepstrain: does it match noisy nature?). The gap between "matches theory" and "matches nature" *is* astrophysical reality minus idealization — a quantity neither project sees alone.
- **The falsifiability-pipeline lens.** neural hunch (cheap, suggestive) → symbolic proof (exact, certifying) → real-data test (falsifying). A conveyor that turns intuitions into theorems into measurements. The "universal ∧ conservative" criterion is the first item ready to ride it.
- **The cross-domain lens (tabula's curvature atlas).** The same curvature/legibility machinery now spans markets (flat connection), hierarchies (hyperbolic), neural populations (S¹). So any bridge result phrased as "*when is a learned geometry legible / transferable*" may generalize **beyond GR entirely** — the most ambitious read, worth holding even if not chasing.

---

## 7. Failure modes — what NOT to do

- **Scope creep (the dominant risk).** Three repos is a lot of rope. Do **not** wire all three at once. Build the §3 minimal triangle, or one §4 pair, then stop and look. A finished small thing beats a sprawling unfinished one.
- **Spending independence carelessly** (see §2). The single most expensive mistake, because it's invisible — you'd still get agreement, it just wouldn't mean anything.
- **Overclaiming novelty.** The physics under all of this is mature: no-hair, QNM spectroscopy, shadows, echoes, the equivalence principle — all textbook or established-active. The contribution is **methods + the unusual end-to-end ownership + cross-validation**, framed honestly. deepstrain's no-hair result is a fine independent re-analysis, not a new physics claim; LVK does the frontier version.
- **Measurement-vs-engine confusion** (the shadow-edge lesson, generalized). Always separate "the oracle is wrong" from "my readout of the oracle is wrong." Measure b_crit from geodesics, not brightness; read moduli from the equations, not a fit; etc.
- **Letting the bridge block the bankable.** Two genuinely-unclaimed results are sitting unwritten — the rotating-EdGB closed form, and the legibility-law amortization isolation. The bridge is more fun than writing; it shouldn't eat the write-ups, which pay off regardless of how the bridge goes.

---

## 8. Suggested first-session ordering

1. **Cheapest leg of the spine first.** ansatz exact moduli-count + tabula neural count on the *same* exact families (observables interface, §4A). Pre-register the expected count and the agreement criterion. One afternoon; tells you immediately whether the two oracles even speak the same language.
2. **The domain-gap diagnostic** (§4B, the legibility-law reframe). Highest practical payoff; touches deepstrain's real pain.
3. **Close the triangle** with deepstrain's measured δ (§3).
4. Then, if momentum: the conjecture handoff (§4A) and the strong-field curriculum (§5).

Match the projects' shared ethos throughout: pre-register → build → gate → document. All three repos already live by it; the bridge should too.

---

## 9. Open questions to carry in

- Do MDL, moduli dimension, and measured DOF all give the same count for a black hole? Where do they part, and why?
  **→ ANSWERED (leg K / A9):** they agree on the observable count (1, 2, 2) when the code is *nonlinear*
  (moduli, measured-δ, neural-knee, and Levina–Bickel intrinsic-dim all converge; dyonic≈RN confirms the
  Q²+P² degeneracy). They part only for a *linear* MDL, which overcounts via curvature (leg 7b / Move I).
- Does **amortization predict sim→real transfer** in GW data? (If yes: the most original result available here.)
  **→ CONCRETE SUPPORT (leg L / A1):** the no-hair NPE's per-parameter *legibility* (measured on simulation:
  M 0.86, χ 0.51, δ 0.09) predicts its real-data posterior precision (M tightest → δ widest, identical
  ranking). A cheap sim probe forecasts which parameters the real measurement pins down. Honest scope: 3
  params / 1 event, and the mechanism is shared Fisher information (not an amortization-gap-overfitting
  effect) — the cross-model version needs several NPEs deepstrain would train. Also (A6): δ is
  information-limited even in this richer model, corroborating leg 2.
  **→ FULL VERDICT (A1, deepstrain's 5 NPE variants):** the amortization *gap* does NOT predict transfer
  (corr +0.04≈0); transfer is negative for all variants (real under-coverage), set by the sim↔real *domain
  shift*, not amortization — refuting the hypothesis but corroborating leg 2. Within-model legibility→precision
  stands; cross-model amortization→transfer does not. (Weak test: 5 pts, noise-limited.)
- Is tabula's strong-field error in the regime real ringdowns actually constrain — i.e., does it *matter*?
- Does "geometrizes ⟺ universal ∧ conservative" survive an exact proof on the ansatz catalog?
- Does any bridge result, phrased as "when is a learned geometry legible/transferable," generalize to the curvature-atlas domains outside GR?

---

## 10. Roadmap

### 10.0 What changed (2026-06-19): the engines grew the two halves the bridge was missing

Two independent build sprints — no cross-contamination, the repos still do not import
each other — added exactly the two halves of an inductive→deductive **discovery pipeline**:

- **ansatz** gained ~21 callable oracles (§56–76). Bridge-critical, with verified I/O:
  - `wave_potential(f, ℓ, s)` and `eikonal_qnm(f)` — QNM / ringdown from a static lapse
    (eikonal/WKB; Schwarzschild exact, ~3% vs Leaver). *The QNM unlock leg 3 was waiting on.*
  - `is_killing_vector(geo, ξ)` (exact, symbolic) plus the Killing-tensor / Killing–Yano
    residual machinery (`killing_tensor_residual`, §58/§69) — it can **numerically certify an
    externally-proposed Carter-type invariant**.
  - `invariant_fingerprint(geo)` (Weyl I/J, Kretschmann) and `petrov(geo)` — coordinate-free
    exact ground truth for the inductive oracle.
  - Logic-verified GW oracles: ringdown template + parameter-free no-hair ratio (§72),
    inspiral chirp (§73), polarizations / mode-count (§74), area theorem (§75),
    Kerr thermodynamics / Hawking (§61/§70).
- **tabula** gained a **distillation head** (scripts 95–100): it now emits a discovered
  conserved quantity as a **coefficient vector in an interpretable basis** (reconstructable to
  a closed form), cross-validated against an independent chaos diagnostic (SALI). It caught the
  Kepler Laplace–Runge–Lenz vector (96) and the Kerr–de Sitter *rational* Carter constant
  (97, cosine 0.9999 to textbook), and can tell a separability-preserving deformation from an
  integrability-breaking one **as a data test** (99). The FNO upgrade (100) broke the
  field-learning architecture wall — an enabler for a later "propose a whole metric" route.

This makes the §4A **conjecture handoff** — historically our weakest, most-overclaimed leg —
buildable *for real*, and upgrades the spine's proposition-level ringdown link (leg 3) to a
numeric one.

**Two standing integrity rules for this phase:**
1. **Numeric, not symbolic.** Ansatz certifies a proposed Killing tensor by residual
   `∇₍ₐK_bc₎ < tol` at sampled points, not as a symbolic theorem. Word every result
   "numerically certified to tolerance," never "proved."
2. **Independence is enforced by data flow, exactly as in leg 1.** Ansatz is the blind
   geodesic *source*; only trajectory arrays cross to tabula; only the candidate invariant
   crosses back; neither repo imports the other. This is chosen deliberately over reusing
   tabula's own integrator — the slower path, but the only one where agreement means
   *evidence, not echo* (§2). Optimizing this leg for speed would discard its entire value.

### 10.1 Phase 1 — complete

The original five-option roadmap is done; each became a leg (see JOURNAL / per-leg FINDINGS):

| Option | Became | Outcome |
|---|---|---|
| A — phase-shift curvature | leg 7b | FFT-magnitude recovers the true dimension (standardized space) |
| B — rotating curriculum | leg 5b | mixed: helps retrograde, hurts prograde (train/test leakage flagged) |
| C — generalized handoff | leg 4 | 1+1D special case only — **superseded by Move A** |
| D — integrability fingerprint | leg 5c | dimension *counting* did **not** fingerprint integrability — **superseded by Move A** |
| E — exotic echo templates | leg 8b | on-source null; suggestive but underpowered (N=25) sensitivity reversal |

A through-line worth keeping: leg 5c showed that *counting the bottleneck dimension* fails to
detect a hidden symmetry; tabula's new *invariant distillation* (95–99) succeeds where the
count failed. Move A is built on the method that works.

### 10.2 Phase 2 — the discovery→verify era

Each move follows the §2 discipline: pre-register the prediction and the agreement criterion,
obtain each side blind, report disagreements as findings.

#### Move A — the hidden-symmetry discovery pipeline  *(✅ CLOSED 2026-06-19; supersedes legs 4 and 5c)*
**Outcome:** the pipeline closed end-to-end. All four rungs agreed (Kerr/KN/Kerr-dS EXISTS,
bumpy DESTROYED), EXISTS vs DESTROYED separated by 4+ orders of magnitude, and tabula recovered
the *exact* textbook Carter coefficients `(1, a², −a², 1)` blind (cosine 1.0000), certified by
ansatz. The rational-library sub-prediction did not land — Kerr-dS bound orbits require small Λ,
where the rational correction is sub-resolution (a real physical finding). →
[legA_symmetry_discovery/FINDINGS.md](legA_symmetry_discovery/FINDINGS.md). Original plan below.
- **Question.** Can the inductive oracle *discover* a spacetime's hidden conserved quantity
  from trajectories alone, and the deductive oracle independently *certify* it from the metric
  — agreeing on which spacetimes have one and which do not?
- **Who does what.** Ansatz integrates geodesics from its exact metric and writes **only
  trajectory arrays** (the leg-1 blindness boundary, enforced mechanically). Tabula distills a
  candidate invariant blind (distillation head, 95–97) and emits its coefficient vector.
  Ansatz reconstructs the candidate and certifies it numerically
  (`killing_tensor_residual` / Killing–Yano, §58/§69).
- **Calibration ladder (run in full, the rigorous path):** Kerr (M,a) → Kerr–Newman (M,a,Q;
  charge preserves Carter) → Kerr–de Sitter (M,a,Λ; rational Carter) → bumpy-quadrupole
  (Carter destroyed).
- **Pre-registered verdicts (frozen before running):**
  - *Tabula, blind:* EXISTS iff a low-degree-library invariant stays conserved on **held-out**
    trajectories (held-out variance-ratio < ε), at the lowest library degree that works
    (parsimony). For calibration metrics the cosine-to-textbook is a bonus check only — the
    primary verdict uses held-out conservation alone, so the identical rule transfers to the
    frontier (Move D), where there is no textbook answer to lean on.
  - *Ansatz, from metric:* EXISTS iff the reconstructed K has Killing-tensor residual < tol at
    N sampled points (and/or a Killing–Yano root exists).
  - *Agreement (frozen):* the two EXISTS/DESTROYED verdicts must match cell-by-cell —
    Kerr/KN/Kerr-dS → EXISTS (both), bumpy → DESTROYED (both). A mismatch is a finding.
- **Validates.** The full falsifiability pipeline end-to-end — neural discovery → exact
  certification — with both halves real and independent. **Honest size:** on the ladder it
  re-derives *known* invariants (a methods milestone, not new physics); the new physics is
  Move D. This is the leg that retires the "conjecture handoff" overclaim by doing it properly.

#### Move B — the numeric ringdown bridge  *(✅ CLOSED 2026-06-19; leg 3b, upgrades the spine)*
**Outcome:** established. Ansatz's eikonal Kerr QNM from the *exact metric* matches deepstrain's
measured GW250114 220 to a few percent — quality factor Q₂₂₀ to 1–7%, Mω_R₂₂₀ to 3% — while the
non-spinning Schwarzschild eikonal misses by 40–50% (so the agreement is the light ring, not a
fit). `Ω_c·b_c = 1` exact: the LIGO ringdown and the EHT shadow are the same photon orbit. Leg 3's
ansatz↔deepstrain link is now numeric, not propositional. →
[legB_ringdown_bridge/FINDINGS.md](legB_ringdown_bridge/FINDINGS.md). Original plan below.
- **Question.** Does ansatz's exact QNM structure agree numerically with deepstrain's measured
  GW250114 ringdown?
- **Who.** Ansatz: `eikonal_qnm` (real frequency set by the photon-ring orbital frequency;
  overtone damping spaced by (n+½)) and the no-hair template (§72). deepstrain: the measured
  220/221 ringdown frequency, damping, and δ.
- **Pre-register.** The measured fundamental sits within the eikonal band; the measured overtone
  structure (real-frequency near-degeneracy, (n+½) damping ladder) is consistent with the
  eikonal prediction within measurement error.
- **Honest size.** Eikonal-level (static lapse; ~3% on Schwarzschild; Kerr-spin corrections
  approximate). The parameter-free relations are the cleanest use. Converts leg 3 from a
  proof↔test proposition into a numeric exact↔measured comparison, scoped honestly.

#### Move C — coordinate-free invariant cross-measure  *(✅ CLOSED 2026-06-19; mixed result)*
**Outcome (mixed, reported honestly):** ansatz's coordinate-free Weyl invariant *is* present in
the frame-randomized tidal field and a net recovers its **magnitude** (MLP R²=0.96) but **not
linearly** (R²=0.02) — the legibility gap (P1, P2 ✅). It does **not** recover the **fine
structure**: the exact Petrov O/D boundary (0.75, not >0.95) and the rank-ordering across 3
decades (Spearman 0.56) fail (P3, P4 ✗). The finding: the learned representation captures the
gross invariant, but the algebraically-special edge (near conformal-flatness) is where ansatz's
exact construction is irreplaceable — the same shape as Move D's hierarchy. →
[legC_invariant_crossmeasure/FINDINGS.md](legC_invariant_crossmeasure/FINDINGS.md). Plan below.
- **Question.** Does tabula's learned representation recover ansatz's coordinate-free Weyl
  invariants / Petrov type — e.g. can a net trained on observations tell Petrov-D (black hole)
  from Petrov-O (conformally flat), blind?
- **Who.** Ansatz: `invariant_fingerprint` (Weyl I/J, Kretschmann), `petrov` — exact labels.
  Tabula: probe whether its bottleneck/representation linearly carries those invariants.
- **Validates.** Whether the inductive oracle's learned geometry aligns with exact
  coordinate-free truth — the §4A invariant cross-measure, now with a coordinate-proof reference.

#### Move D — the integrability boundary of a deformed black hole  *(✅ CLOSED 2026-06-19)*
**Pivot (recorded):** the menu named rotating-EdGB, but recon showed ansatz's EdGB is *O(a)
slow-rotation*, where the Carter constant trivially survives via the spherical L² — not a
frontier test. We retargeted to the genuinely-open question: **where does Kerr's hidden symmetry
die under a quadrupole deformation, swept ε=0→0.35, measured three independent ways** (tabula's
blind distillation, ansatz's exact Killing residual, SALI chaos index).

**Outcome — a three-boundary hierarchy (a principled disagreement = the finding).** "Is it
integrable?" split into three answers: the **exact** Killing tensor (ansatz) dies at ε*≈0⁺; an
**approximate** invariant (tabula) survives to ε≈0.07 (the gradual KAM transition); **chaos**
(SALI) sets in only at ε≈1.0 (originally bounded as ">0.35"; *located* by the Move-G falsification,
which also validated SALI on a chaotic control). The pre-registered single agreed boundary (P3) was
*falsified in exactly the anticipated way* (PREREG §6) — no single method sees the hierarchy; only
the three together do. Move G confirmed the hierarchy is real *as an ordering* (the methods give
different verdicts at the same ε — the KAM band), with the caveat that the specific boundary *values*
are threshold-dependent. → [legD_integrability_boundary/FINDINGS.md](legD_integrability_boundary/FINDINGS.md).

*(The original "discover a brand-new invariant nobody has written down" framing still awaits a
metric class where ansatz can supply a full — not slow-rotation — deformed metric whose Carter
analog is suspected but unconfirmed; rotating EdGB at full spin, once ansatz reaches it, is the
natural target.)*

#### Tier 3 — cheap consistency checks  *(✅ CLOSED 2026-06-19)*
- §75 area-theorem: GW150914 `M_irr,f = 58.6 ≥ √(m₁²+m₂²) = 46.9` (area increased, 1.56× margin);
  radiated 4.7% < 29.3% cap. §74 polarization: GR's 2 tensor modes consistent with measured.
  Textbook consistency checks. → [legTier3_consistency/FINDINGS.md](legTier3_consistency/FINDINGS.md).

#### Move E — do the meta-findings survive outside GR?  *(✅ CLOSED 2026-06-19; the cross-domain capstone)*
**Question (the only one with real headroom):** are the bridge's two meta-findings — the
*legibility gap* (Move C / leg 2) and the *bulk/edge boundary* (Moves C, D) — facts about black
holes, or about **learned-vs-exact structure on a curved space**? Tested in two non-GR curved
domains from tabula's own atlas (the neural ring S¹, the hyperbolic disk), each vs a **flat
control**. **Outcome — a qualified yes:** both reproduce in the curved domains and vanish in the
flat controls; the **bulk/edge boundary *scales* with curvature** (edge/bulk error 0.78→2.32 as
r_max→1, flat stays ~0.5) — the strong result; the **legibility gap is curvature/topology-specific
(16× the flat control) but modest**. The frozen *aggressive* thresholds were not all met (reported
honestly); the directional contrast + the bulk/edge scaling carry the conclusion: these are facts
about curvature and learning, of which the GR results are one instance. →
[legE_curvature_universality/FINDINGS.md](legE_curvature_universality/FINDINGS.md).
*(Caveat, corrected by Move F: the "curvature" wording here is imprecise — see Move F.)*

#### Move F — curvature or boundary?  *(✅ CLOSED 2026-06-19; corrects Move E)*
Move E's hyperbolic disk confounded curvature and a boundary. A 2×2 isolation (hyperbolic =
curved+boundary, sphere S² = curved+no-boundary, flat disk = flat+boundary, flat torus = flat+no-
boundary) shows the bulk/edge effect fires in **only one cell — hyperbolic (3.81×)**; the sphere
(0.49×), flat disk (0.78×), and torus (0.51×) all stay quiet. So it is **neither curvature alone
nor a boundary alone**: the driver is a **conformal boundary where the metric *diverges*** (the one
space with unbounded distance). That is exactly a **black-hole horizon** (diverging proper distance
/ the near-horizon hyperbolic throat) — a sharper and more GR-relevant statement than "curvature."
→ [legF_curvature_vs_boundary/FINDINGS.md](legF_curvature_vs_boundary/FINDINGS.md).
*(Sharpened again by Move G/Test 3c: even "conformal boundary" overstates it — a **flat** space with
a **diverging distance** fires (4.5×), so curvature is incidental; the driver is the **metric/distance
divergence** itself.)*

#### Move G — adversarial falsification  *(✅ CLOSED 2026-06-20; tried to BREAK the main claims)*
A deliberate break-attempt, outcome-neutral. **The spine survived its headline attack:** the bottleneck
counter is genuinely *calibrated* — it tracks true dimension (corr 0.98 on synthetic d=1–6), is *exact*
on flat manifolds, and reports pure noise as 8 (not 2), so it is **not biased toward 2**. But the attack
revealed a real ±1 imprecision: on *curved* manifolds it overcounts by +1 (the leg-7b curvature
inflation, confirmed by a flat-vs-curved control), so the **vacuum**-BH counts (Schwarzschild, Kerr) are
threshold-fragile (Kerr = 2 at the frozen 2% rule but 3 at 1%), while the **charged**-BH counts (RN, KN)
are robust. **Move A survived** two attacks: DESTROYED on noise/shuffled/scrambled data (no hallucinated
invariants) and recovers the **true a² to 0.0% across spins 0.1–0.9**. **Move B survived:** measured Q
and Mω_R independently imply the *same* spin (0.818 vs 0.816), a two-observable consistency, not a
one-parameter fit. **Claims CHANGED by the attacks** (the sign of honest falsification): Move F's
"curvature" → **pure metric divergence** (a flat space with a diverging distance fires; a curved space
without divergence does not); the synthesis's edge is **fundamental but coordinate-dependent in
severity**; and the spine's count is **calibrated but only ±1 accurate on curved manifolds**. **Move D
survived & was strengthened:** the three-boundary hierarchy is real *as an ordering* (the methods
disagree at the same ε — the KAM band), SALI was validated on a chaotic control, and the chaos
boundary was *located* at ε≈1.0. → [legG_falsification/FINDINGS.md](legG_falsification/FINDINGS.md).

#### Move H — the horizon is a learnability edge  *(◐ CLOSED 2026-06-20; prediction holds, recipe refuted)*
Took the (battle-tested) edges finding from diagnostic to predictive + constructive on the *real*
horizon. **Prediction — SUPPORTED:** a learned emulator of a horizon-diverging GR quantity
(`1/√(−g_tt)` Schwarzschild, `√(g_rr)` Kerr, from ansatz's exact metric) fails *at* the horizon —
edge error **85–88×** the bulk, while a flat null (`Q=r`) shows none. So the horizon genuinely is a
learnability edge; the abstract principle makes a correct, controlled GR prediction. **Recipe —
REFUTED & dropped:** the hoped-for bulk-learn/exact-edge hybrid beats the pure-asymptotic emulator
but **loses to pure-learned** at every matching radius and at every divergence strength (p=0.5–3).
The reason *refines the whole synthesis*: near a divergence the **exact asymptotic evaluated at noisy
position is just as wrong as the learned emulator** (`δQ ∝ (r−r_h)^{−p−1}δr → ∞`), so the edge failure
is **observation-noise amplification**, not learned-vs-exact. Hence **"exact owns the edge" holds only
for *direct-exact* tasks** (A, B — ansatz computes from its exact metric, no noisy intermediate), and
**not for *noisy-recovery* tasks** (E, F, H — both methods fail at the edge together; the edge belongs
to observation precision). The recipe claim is withdrawn; the failure bought the real mechanism. →
[legH_horizon_learnability/FINDINGS.md](legH_horizon_learnability/FINDINGS.md).

#### Move I — are the edges one mechanism, or several?  *(✅ CLOSED 2026-06-20; a falsified prediction → the taxonomy)*
Tested whether all the "edges" reduce to one mechanism, via one discriminator: does the edge survive
perfect observation? **Prediction I1 (the divergence edge vanishes at σ=0) was FALSIFIED** — it is
5.69× at σ=0 — and chasing why gave the answer: it is **resolution-limited** (shrinks with data; the
exact closed-form has zero error), so the exact form owns it and finite-resolution learning fails.
**I2 held:** D's integrability edge is **physical** (var-ratio 5×10¹⁵× the noise floor on clean
geodesics — the structure is genuinely gone). **Result — TWO kinds of edge:** recovery/resolution
(structure exists, exact closed-form owns it, learning fails, noise defeats even exact) vs physical
(structure absent). This reconciled F/G/H and corrected H's over-broad "neither owns it." →
[legI_edge_taxonomy/FINDINGS.md](legI_edge_taxonomy/FINDINGS.md).

### 10.3 Order / status — Phase 2 COMPLETE (+ explorations E, F, falsification G, H, I)
**A ✅ · B ✅ · C ✅ · D ✅ · Tier 3 ✅ · E ✅ · F ✅** (2026-06-19). Move A validated the
discovery→verify instrument (blind recovery of the exact Carter constant); B made the spine's
ringdown link numeric (eikonal Kerr QNM vs GW250114, a few %); D took the pipeline to a
genuinely-open question (the three-boundary integrability hierarchy); C cross-measured the
coordinate-free invariant (recovered in the bulk, not at the algebraically-special edge); E tested
whether the meta-findings survive outside GR; F isolated the driver of the bulk/edge effect to a
**conformal boundary where the metric diverges** (not curvature generically — correcting E).
**Through-line (as corrected by F and G):** a learned representation recovers an exact structure in
the bulk and loses it at the *edge* — the horizon/light-ring (B), the algebraically-special limit
(C), the integrability boundary (D). For *distance recovery* specifically (E/F/G), the edge is
pinned precisely: it is wherever the **metric/distance diverges** (a black-hole horizon; curvature is
incidental — a flat space with a diverging distance shows it too, G/3c). **But Move H corrects the
mechanism for *recovery* tasks:** the edge there is **observation-noise amplification at the
divergence** (`δQ ∝ (r−r_h)^{−p−1}δr`), which afflicts the exact construction *as much as* the learned
one when both take a noisy observable as input. So "exact owns the edge" is true for **direct-exact**
tasks (A, B — ansatz computes from its exact metric) but **false for noisy-recovery** tasks (E, F, H —
the edge belongs to observation precision, not to exact-vs-learned). **Move I then resolved the
taxonomy** (and corrected H's over-broad reading): the edges are **TWO genuinely different kinds.**
**(1) Recovery/resolution edges** (the metric/distance diverges or a signal vanishes — F, H, C): the
exact structure *exists* — the **exact closed-form owns the edge** (zero error at exact input), while
finite-resolution *learning* fails at the diverging gradient (shrinking only slowly with data), and
*observation noise* defeats even the exact form (H). **(2) Physical edges** (the exact structure
*ceases to exist* — D's integrability loss, the exact Killing tensor gone for ε>0): nothing recovers
what is not there; the var-ratio is physical (5×10¹⁵× the noise floor on clean geodesics). So the
honest final synthesis is **three statements**: a learned representation loses exact structure at edges
where the metric **diverges/degenerates**; for *recovery* edges the **exact closed-form owns the edge**
(learning fails; noisy input defeats even exact); for *physical* edges the structure is **absent**, and
in **direct-exact** tasks (A, B) there is no edge at all. Survived adversarial falsification (G);
refined by a failed recipe (H) and a falsified prediction (I). Open frontier: a full-spin deformed
metric with an unconfirmed Carter analog (awaits ansatz beyond slow-rotation EdGB); whether *every*
edge in physics is one of these two kinds.

### 10.4 The loop closes — source-project upgrades feed back (2026-06-21)

The bridge's own review fed concrete upgrades back into the source repos, and those now upgrade the
bridge legs in return — the cross-validation cycle running both directions:
- **ansatz** built §77 (precise Leaver QNM + the 221 overtone), §78 (symbolic Killing-tensor
  verifier), §79 (geodesic + chaos lens), §80 (Kerr Petrov), §82 (integrability frontier), §83
  (tetrad-free Weyl) — essentially the whole bridge-driven list.
- **deepstrain** built §12 (multi-event δ stacking, σ 0.27→0.095), echoes §11 (non-detection →
  exclusion curves), §08 N=300 (the underpowered injection fix), §13/§14 (more events + the δ SNR wall).

**Bridge legs upgraded by these:**
- **Move A v2 — a PROOF, on every rung.** §78 re-certifies tabula's blind-distilled Carter constant
  *symbolically* — `∇₍ₐK_bc₎≡0` proven for **Kerr, Kerr–Newman (all Q), and Kerr–de Sitter (all Λ)**
  (non-vacuous: control rejected, K ∝̸ g, correct Λ→0 limit) — *and* the **DESTROYED** rung proven the
  other way: Kerr's Carter tensor on the bumpy metric has residual `∝ ε·a² ≠ 0` (zero only at ε=0). The
  whole discovery→verify ladder is now a theorem on every rung, EXISTS and DESTROYED alike — not a
  numeric residual.
- **Move B v2 — precise & numeric.** §77's exact Leaver 220 inversion reproduces deepstrain's remnant
  (two independent QNM codes agree); the 221 overtone (eikonal had none) gives the no-hair δ = −0.159,
  **independently matching deepstrain's measured δ = −0.151 to 0.008**, Kerr-consistent; §12 tightens
  σ(δ) to 0.095 over 8 events. Leg 3's no-hair link is now a precise two-mode comparison.
- **Independent convergence (Move D ↔ ansatz §82).** From the *metric/symbolic* side, ansatz §82
  deformed Kerr and found the canonical Carter tensor is no longer Killing yet **no detectable chaos**,
  fate **undetermined** — exactly the bridge's Move D hierarchy / Move I "physical edge, KAM-robust"
  conclusion, reached by a completely independent route. Evidence, not echo, at the meta level.
- **Leg J resolves the "undetermined" fate.** Two calibrated attacks settle it for the bump:
  a *complete symbolic Killing–Yano search* (Kerr-gated, exact linear algebra) finds **no exact KY tensor
  survives to degree 4** → by Eisenhart no exact Carter-type Killing tensor (the strict horn **closed**);
  and the **§79 Lyapunov exponent** (validated — Kerr floor; legG's SALI corroborating) stays at the floor
  for every accessible orbit (near-circular *and* Schmidt-built eccentric/inclined, **to ε=1.2**) → the KAM
  tori survive, **no chaos in reach**, even as the canonical Carter constant is violated (drift 7→18%).
  Verdict: **formally non-integrable, near-integrable** — matching the Kerr-deformation literature (Brink
  III/IV; arXiv:1807.08594), by proof *and* dynamics. Two instruments were *failed and discarded honestly*:
  the dimension scan (zoom-whirl gate failure) and the Carter-saturation chaos proxy (a positive control
  showed it could not be validated as a chaos detector → superseded by the Lyapunov).
- **Four-method convergence (bridge ↔ ansatz §84/§85).** ansatz independently attacked the same question on
  *its own* bump: §85 (numeric SVD Killing-tensor search) finds no conserved quadratic; §84 (Poincaré,
  validated on Hénon–Heiles — the positive control our chaos detector lacked, and sharper than Lyapunov)
  finds regular-or-destroyed, never chaotic. ansatz's *direct symbolic* search swamped (7.5 h) — so the
  bridge's KY-route is a method ansatz lacks, and §84/§85 are methods the bridge lacked. Porting §85's
  numeric search onto *our* bump (`numeric_killing_search.py`) retires the non-KY-origin caveat at rank 2.
  **Four methods, two projects, two bump families, one verdict** — formally non-integrable, near-integrable.
  Only residual: higher-rank/quartic tensors and thin sub-resolution chaos (both expected to confirm).

---

*Independence got you three clean instruments. The bridge is where you let them read the same thing — once, carefully, blind — and see if the universe gives the same answer three ways.*

