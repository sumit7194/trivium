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
- Does **amortization predict sim→real transfer** in GW data? (If yes: the most original result available here.)
- Is tabula's strong-field error in the regime real ringdowns actually constrain — i.e., does it *matter*?
- Does "geometrizes ⟺ universal ∧ conservative" survive an exact proof on the ansatz catalog?
- Does any bridge result, phrased as "when is a learned geometry legible/transferable," generalize to the curvature-atlas domains outside GR?

---

## 10. Future Roadmap

We have established a five-option roadmap for the next phase of the project:

### Option A: Resolving the Phase-Shift Curvature Problem (Leg 7b)
*   **Problem**: In Leg 7, the autoencoder resolved $4$ dimensions instead of the physical $2$ for locked Kerr ringdowns due to "phase-shift curvature" (translation shifts of wave peaks in the time-domain create highly curved manifolds).
*   **Plan**: We will implement pre-processing and coordinate transformations (such as Fourier/magnitude spectra, phase alignment, or Hilbert envelopes) to remove phase-shift variance before bottleneck compression, and test if the autoencoder can recover the true physical dimensionality ($2$ for locked, $4$ for free).

### Option B: Rotating Strong-Field Curriculum (Leg 5b)
*   **Problem**: Leg 5 targeted the static Schwarzschild shadow ($b_{crit} = 3\sqrt{3}$). Rotating Kerr spacetimes have asymmetric shadows due to frame-dragging.
*   **Plan**: We will use the ansatz engine to compute exact Kerr shadow boundaries and train targeted networks to reconstruct the spin parameter $a$ and viewer inclination $\theta_0$ from null geodesics.

### Option C: Generalized Conjecture Handoff (Leg 4b)
*   **Problem**: The symbolic geometrization proof in Leg 4 was restricted to a $1+1D$ static metric and simple linear velocity drag.
*   **Plan**: Generalize the symbolic proof to a full $3+1D$ metric and test non-conservative forces like electromagnetic Lorentz forces or non-linear drag.

### Option D: Integrability Fingerprints (Leg 5c)
*   **Problem**: The count-triangle (§5) shows that counts diverge under some conditions (such as dyonic degeneracy), but we have not verified whether the neural bottleneck count can detect a hidden symmetry.
*   **Plan**: Kerr geodesics are integrable due to the Carter constant (a conserved quantity beyond energy and angular momentum), but deforming the metric breaks this integrability. We will feed the neural bottleneck network geodesic trajectory data from an exactly-integrable system (Kerr, with Carter constant certified by ansatz) versus a deformed non-integrable system, and evaluate whether the bottleneck count (`tabula`) detects a difference (i.e., whether integrability leaves a representational fingerprint).

### Option E: Physics-Grounded Echo Templates (Leg 8b)
*   **Problem**: `deepstrain`'s echo search currently relies on phenomenological templates for exotic near-horizon structures, which may miss real signals due to template mismatch.
*   **Plan**: Use `ansatz` to generate the exact near-horizon metric and reflection structure of an echo-producing exotic object (such as a wormhole or gravastar). Convert these exact solutions into physics-grounded wave templates and feed them to `deepstrain`'s search pipeline to search for echoes in real LIGO data.

---

*Independence got you three clean instruments. The bridge is where you let them read the same thing — once, carefully, blind — and see if the universe gives the same answer three ways.*

