# Program II — pointing the instruments at the unknown

> **STATUS: DECIDED 2026-08-16 (see §0). Round-12 study closed 4/4; the shape below is the sisters'
> amended version, not the morning's proposal.** Pre-register → build → gate → document still governs:
> no programme begins until its own `PREREGISTRATION.md` is frozen. What this document does is choose
> **which questions are worth pre-registering**, which is a decision the ledgers were never designed to
> make.
>
> Written 2026-08-16. Supersedes nothing. `CAPSTONE.md` remains the state of the record; this is the
> state of the *intent*.

---

## 0. Decisions of record (2026-08-16)

Four decisions taken by the user after all four sisters reported. **Every one of them adopts a sister's
amendment over the original proposal.**

| # | decision | consequence |
|---|---|---|
| 1 | **P1(a′) prior-art sweep — AUTHORIZED and RUN** (ansatz) | result below: survives the novelty gate, but **demoted**; a third premise of P1 fell |
| 2 | **P0 (the simplifier wall) is the first move** | ansatz's #1; unblocks P1(b) + P3 + §122 simultaneously |
| 3 | **P4 folds into P3** | tabula's recommendation adopted; the emit-on-unknown-data programme is retired in favour of the certify side |
| 4 | **quantum's scoping accepted: oracle, not engine** | no shared integrator — each frontier keeps its own; vestigium owns reference orbits, exact-invariant monitoring, and the floor protocol |

### The P1(a′) sweep result — *survives the gate, fails the ranking, and kills P1's last premise*

ansatz ran it on authorization, from primary text. **Findings:**

- **Reconstruction is restricted, not universal.** Ernazarov–Ivashchuk applies to the special ansatz
  `ds² = A(u)⁻¹du² − A(u)dt² + u²dΩ²` — the **g_tt·g_rr = −1 subclass**, not arbitrary static spherical;
  the authors flag general metrics as future work.
- **The binding constraint is an *inequality*** — the ghost-avoidance condition
  `Φ = φ̇² = 8u⁻²f''(A−1) > 0` on an interval, which is what splits Schwarzschild into two **disconnected**
  domains at the photon sphere.
- **Solutions are non-unique** (two integration constants; two families for Schwarzschild alone), so
  *"which couplings admit metric X"* already answers *"a two-parameter family"*, constructively.
- **The adjacent classification literature does not cover it**
  ([arXiv:1903.02055](https://arxiv.org/abs/1903.02055) classifies *existence of hair*, not exact
  solvability; likewise the no-go literature, [arXiv:2210.03966](https://arxiv.org/abs/2210.03966)).
- **The genuine gap, by the authors' own omission:** they never state that any metric admits **no** valid
  (U, f) pair, and call ghost avoidance solvable *"at least locally"*. **The failure locus is
  uncharacterised.**

**⇒ What actually survives is the inverse-image question:** *for which metrics in a graded family does the
ghost-avoidance condition admit **no** globally valid solution — i.e. where does reconstruction **fail**?*
Open, and the house's own move (three-valued, exhaustive over a graded family, same shape as §112/§114's
obstruction maps).

**⇒ But it is DEMOTED, on ansatz's argument, and the second reason is disqualifying alone:**

1. **Size** — footnote-sized, not programme-sized. *"Sold as more, it would not survive contact."*
2. **Wrong engine.** Our verifier is three-valued on **equalities** — symbolic zero-testing with
   Richardson handled by numeric-first spot checks. The GAC is an **inequality that must hold on an
   interval**, so deciding it is **quantifier elimination / positivity over a semialgebraic set —
   Tarski/CAD territory**. SymPy is thin there and does not degrade gracefully, and there is **no
   calibrated experience with it anywhere in 123 sections.** This is *not* the simplifier wall we
   measured; it is a **capability we have never built or validated.**

**And it kills P1's last surviving premise.** The original rationale was that this question was open
*"because asking it requires a machine that can carry the symbolic load."* That was wrong twice over:
humans asked it **by hand** (the novelty gate, this morning), and now — **the hard part in this corner is
not symbolic load at all, it is deciding inequalities, which is a different discipline.** ansatz's own
summary: *"worth knowing before PREREGISTRATION.md, not after."*

**Ranking of record (ansatz's, unchanged but now better evidenced):**
**P0 fix the wall → P3 (equality-shaped, therefore our engine's actual competence) → P1(a′) only as a
short obstruction-map item and only after a positivity/CAD path is validated → P1(b) 5D stationary last.**

---

## 1. The reframe — why the program should change shape now

vestigium's README states the plan the whole family has been executing without naming it:

> *"each experiment is checked against exact analytics or a real published measurement, so that when
> the machinery is later pointed at an open question, the machinery itself is not in doubt."*

That sentence describes all five repos. Two and a half months of instrument-building, cross-validation
and self-audit: 36 gated legs, 27 falsification attacks, 12 kills, 6 survivals, 10 self-caught
instrument bugs, a self-audit tier that killed the program's own headline meta-claim.

And — stated plainly, because the ledgers do not state it anywhere —

> **the machinery has never once been pointed at a question whose answer nobody knows.**

Every result in the corpus is a reproduction, a cross-check, a consistency statement, or an honest
null. ansatz's own README says it: *"our actual solutions are rediscoveries, so this is a capability
demo, not a novelty pillar."* vestigium's says it: *"Nothing in it is new physics."* tabula reproduces
Kaluza–Klein, Newton, and Mercury. deepstrain measures nulls and consistency with Kerr. The bridge
compares all four to each other.

**That was correct discipline and it is now complete.** The instruments are verified; the verification
is what the last ten weeks bought. The next substantial thing this program can do is not another leg of
validation. It is **the first result whose answer was not already in a book.**

Four candidate programs follow. They are ranked by my conviction that they produce something
substantial, and each is stated with its failure mode visible — because under the house rules a
structured, exhaustive null is a result, and every program below is designed so that its null is one.

---

## 2. The four programs

### P0 — The simplifier wall: one blocker wearing three hats *(added 2026-08-16 on ansatz's read; they rank it #1)*

**This was not in the original four, and it may be the item that gates the rest.** ansatz's answer to
"what does a weeks-scale campaign cost?" corrected the axis rather than the number:

- **Breadth scales fine.** Many cheap candidates × weeks = genuinely more coverage. That axis really is
  untouched, and is the one worth using.
- **Depth does not scale, at all.** *"More wall-clock does not buy you past a simplifier wall."* §122 is
  the proof: the ceiling was removed entirely, unlimited time given — 4.6 h, then 6 h+ overnight, never
  completed. **The blowup is per-operation, not per-campaign; a single `simplify()` that never returns is
  immune to scheduling.** Measured contrast from §119: the same seven tetrad-normalisation dot products
  took **>8.5 minutes** under `sp.simplify` and **0.3 seconds** under `cancel(together(expand(·)))`.
  Kasner at exponent denominator 13 never finishes the Weyl tensor at all.

**The structural finding, and it is the most useful thing anyone said today about the ansatz half:**
**P1(b) 5D stationary, P3 rank 3–4 on deformed Kerr, and §122's Kerr order-2 CK all hit the *same* wall**
— rotating, two-variable, expression swell. *"That is not three risks; it is one blocker wearing three
hats."* ⇒ cracking it (rational charts, escalating normal forms, caching — the §119/§122 direction)
**unblocks all three**, and is concrete and measurable in a way a weeks-long campaign is not.

**ansatz's own ranking of Program II's ansatz half:** (1) **fix the wall**, (2) **P3**, (3) **P1(a′)**
only if its classification sweep comes back clean, (4) **P1(b)** last — 5D stationary is the deepest
water and the wall bites hardest there. Adopted as **decision 2** (§0).

#### P0 scoped, pre-PREREGISTRATION (ansatz, 2026-08-16) — *awaiting authorization to run Phase 1*

**The baseline, from their durable logs.** §122 order-2 CK: Schwarzschild M=1 **32 s**, M=2 **32 s**,
ZV δ=1 **37 s** — all complete. Schwarzschild in the **isotropic chart >80 s and WALLS** — *same
geometry as M=1, 2.5×+ the cost, purely the chart.* Taub–NUT and Kerr **never reached**; the battery
never completed in 4.6 h, then 6 h+ overnight. Against that, §119's one clean before/after: seven
tetrad-normalisation dot products, **>8.5 min** under `sp.simplify` vs **0.3 s** under
`cancel(together(expand(·)))`. And §01's chart lesson: Kerr in Boyer–Lindquist **500 s → UNPROVEN**, in
rational u=cos θ **VERIFIED in 9 s** — same spacetime.

**Their discipline, stated first:** *"I will not propose a fix first. I have guessed at §122's cost three
times this week and been wrong three times."* **P0's first deliverable is a measurement, not a patch.**

- **Phase 1 — LOCALISE.** Per-stage profile of *one* Kerr order-2 signature (`weyl_tensor`,
  `null_tetrad`/`canonical_frame`, `covariant_derivative_weyl` at orders 1 and 2, invariant extraction,
  functional-rank). **Deliverable: a table attributing ≥80% of wall-clock to named stages.** Bounded by
  §122's global-deadline machinery, resumable from the signature cache.
- **Phase 2 — TEST THE REPRESENTATION HYPOTHESIS**, which they believe is the real answer. McNutt/Coley
  et al. ([arXiv:1709.03362](https://arxiv.org/abs/1709.03362)), doing exactly this computation, write
  that it can be done *"in compact form using the GHP formalism"* and omit the details. **We compute in
  raw tensor components: ∇∇C is a 6-index object, 4096 slots, each a full symbolic expression.** If Kerr's
  intermediates are *intrinsically* large rather than badly normalised, **no simplifier cascade helps and
  the fix is representational** — carry Ψ_i and spin coefficients, not components. Falsifiable by Phase 1:
  supported if ≥80% of time sits in `covariant_derivative_weyl` / component normalisation rather than
  frame algebra.
- **Phase 3 — FIX what 1–2 indicate**, explicitly *not* pre-committed: (a) GHP/NP representation for the
  derivative tower · (b) generalise §119's escalating cascade out of `ck.zsimp` into `gr_engine` ·
  (c) rational-chart policy enforced rather than advisory · (d) caching, if profiling says it pays.

**Success criterion — binary, currently FALSE, not gameable by relaxing a threshold:**
> **§122 completes its full catalog including Kerr a=1/2 and Taub–NUT, unbudgeted, in under 60 minutes
> wall-clock on this machine, all G6 verdicts green, no section reporting RESOURCE-WALLED.**

Secondary/diagnostic: the isotropic-chart order-2 signature completes at all; Phase 1 attributes ≥80%;
and **no regression — §116/117/118/123 keep their exact verdicts (9/9, 12/12, 6/6, 7/7), bit-identical.**

**The null, pre-registered as an output (house rule 5):** if Phase 1 shows the cost is *intrinsic
expression size* in the rotating two-variable case, then **"the wall is not crossable by normalisation;
order-2 CK on rotating metrics requires a GHP-style representation change"** is the deliverable, **P0
terminates there**, and **P3 and P1(b) inherit that constraint explicitly rather than discovering it.**

**Scope boundary they asked to have written in:** P0 touches `gr_engine.py` and `ck.py`, which sit under
**104 gated batteries**. *"Any P0 commit that cannot reproduce 116/117/118/123 exactly is reverted, not
debugged forward"* — the frozen-verdict clause is what stops a performance change from silently altering
physics.

*Their own note on the three failed P1 premises, which belongs here rather than in a scoreboard:* two of
the three corrections came from measurements they only had because §122 had already burned 4.6 hours and
an overnight shutdown in front of them. **"The process worked, but it worked by measurement, not by
foresight."***

---

### P1 — The hunt ansatz was built for, at the scale it was never run

**The question:** *for which theories does an exact black hole exist?*

**What already exists.** `conjecture_machine` is a complete propose → reduce → verify → novelty →
evolve loop. It rediscovers Schwarzschild blind in 3 generations, BTZ in 1, Tangherlini in 2; it found
Kerr and Kerr–Newman blind in the stationary hall; it has catalog memory (discover → generalize →
remember → recognize); it has a Cartan–Karlhede decision procedure closing the fingerprint's declared
VSI blind spot. The verifier is dimension-agnostic and three-valued.

**What has never happened.** Everything above runs "on a laptop CPU in minutes." **The campaign has
never been run at scale.** There is a Mac that runs unattended for days, and a standing rule that
effort is not a reason to drop an item. The gap between "minutes" and "weeks" is the entire unexplored
axis of the machine's own design.

**Two targets, in ansatz's own §6 unmined territory:**

**~~(a) The EdGB inversion — the move I rate highest in the whole document.~~ → KILLED at the gate,
2026-08-16, by ansatz's prior-art sweep. Struck, not deleted.**

> The proposal was: instead of fixing the theory and hunting the metric, **fix a metric ansatz family and
> solve for which coupling functions admit it exactly** — *for what class of scalar–Gauss–Bonnet couplings
> does an exact static black hole exist?* — justified on the claim that "nobody has asked it, because
> asking it requires a machine that can carry the symbolic load."
>
> **It has been asked, it has a name, and it was done by hand.** The **"reconstruction procedure"** of
> Nojiri & Nashed. Verified by ansatz at primary source, abstract read rather than snippet:
> Ernazarov & Ivashchuk, [arXiv:2406.01301](https://arxiv.org/abs/2406.01301) — *"The action contains the
> potential U(φ) and the Gauss-Bonnet coupling function f(φ)… certain implicit relations for U(φ) and f(φ)
> which lead to exact solutions to the equations of motion for a given metric"* — **including the
> Schwarzschild test case**. An active genre: Nashed has applied it to Hayward, to f(R,G), to
> non-metricity GB, plus a 2026 nonminimal-coupling reconstruction ([arXiv:2603.22517](https://arxiv.org/abs/2603.22517)).
>
> **The justification clause was the worst part of it and is struck regardless of what replaces it.**
> "Requires a machine that can carry the symbolic load" was wrong on the facts — humans did this by hand,
> and my sentence was an assertion dressed as a deduction. **L10**, and the third overclaim of mine this
> day. The M6 gate bought exactly what it exists to buy: the cheapest possible way not to write a paper
> that was already written.

**(a′) What survives — classification, not construction.** ansatz's sweep found the literature does
*construction* (Ernazarov & Ivashchuk are explicit: two families for Schwarzschild, **no exhaustiveness
claim**) and found **no no-go / all-couplings result**. So a narrower question is defensible:
**exhaustive classification to stated order** — *"within this graded family of couplings, these and only
these admit an exact black hole, certified three-valued"* — which is the null-as-result framing this
section already argues for. **It needs its own prior-art sweep before anyone believes it is open**, and
ansatz has offered to run that properly rather than have it discovered downstream. **Not authorized.**

*One honest note from ansatz, labelled as what it is:* the 2024 paper's contribution is partly finding a
**typo** in Nojiri–Nashed's relation for U(φ). Hand-derived, error-prone literature is where this
discipline adds value — but that is a **verification** contribution, not a novelty one, and must be sold
as such.

**On the prerequisite, better news than the roadmap implied.** ansatz §10 *already* goes beyond Einstein:
it derives the EdGB reduced field equations by varying the reduced action (symmetric criticality, Kanti
conventions), validated against Kanti et al. PRD **54**, 5049 (1996). The gap to an inversion is
generalising a *fixed* coupling e^φ to a *free* f(φ). **A rung, not a rebuild** — `verify()`'s
`G_ab = Λg_ab` core stays untouched, with the reduced-action path already sitting beside it.

**(b) 5D stationary vacuum, hunted properly.**
ansatz §6(a) already establishes the territory: no uniqueness theorem, classification of 5D stationary
vacuum solutions **still open**, MacCallum's assessment that higher-D work is "for the most part still
at the stage of using only very simple metric forms," and in d ≥ 6 rings and saturns known only
approximately. Injection test first, per ground rule 2 — **rediscover Myers–Perry blind**, and ideally
the Emparan–Reall black ring — then hunt where the catalog thins.

**The risk, priced honestly.** A century of extremely good relativists found solutions only where
symmetry did the work. The hit rate here may be exactly zero. But this program is built so that zero is
still an output: *"no exact solution exists in this ansatz family to degree N, exhaustively searched,
certified by a three-valued verifier"* is a real statement about where solutions **aren't**, and
nobody has ever produced such certificates because nobody had a machine that could. Ground rule 5 —
null results are results — was written for exactly this.

**Owner: ansatz.** Bridge role: none until there is something to cross-validate. This one is theirs.

---

### P2 — The second founding question: *if Kerr is wrong, would we see it?*

**Why this is the right successor.** The first founding question — *how many numbers is a black hole?*
— was answered by making four independent oracles converge on **2**. It closed. The constellation has
never since had a question of that caliber: one that **requires all four repos** and cannot be answered
by any of them alone. This is that question, and the program is uniquely equipped for it in a way that
is not rhetorical:

| link | who owns it | what already exists | band |
|---|---|---|---|
| exact non-Kerr spacetimes | **ansatz** | ZV, Manko–Novikov, bumpy vacua — *proved*, not fitted (§97–110) | both |
| dynamics + resonance structure | **bridge** | frequency-drift detector, Poincaré sections, box-dimension, the devil's staircase; legs D/J/M/R; G3's escape-conjunct scan | **LISA only** |
| waveform-level signature | **bridge + deepstrain** | leg M's frequency-map shifts; leg 8b's template machinery | both |
| detectability in *real measured noise* | **deepstrain** | injection-calibrated sensitivity; the ringdown-δ Fisher/systematic floor | **LIGO today** |
| is the signature *representable* at all? | **tabula** | the representability frontier + the discoverability diagnostic | both |

> **AMENDED 2026-08-16, same day, on deepstrain's read — two links in the chain above were mis-scoped by
> me, and one number reframes the whole programme.** Recorded here rather than quietly fixed, per §4.
>
> **(i) The deep-FAR ladder does not belong in P2.** My brief asked deepstrain what deformation is
> detectable *"given the deep-FAR ladder (1/decade on 80.5 yr)"*. That is a **category error**: the
> ladder is a *detection* threshold — how loud a signal must be to not be noise — while P2 asks a
> *parameter-estimation* question about a signal already detected. The ladder does not bound the second
> quantity at all. Struck from P2's scope; it would have been a persuasive-looking mistake.
>
> **(ii) The dynamics link and the detectability link are for different detectors.** Resonance crossings,
> frequency drift and chaos onset need ~10⁴–10⁶ orbits to accumulate observable phase; LIGO's
> stellar-mass BBH give ~10–100 in-band cycles. **The dynamics apparatus the bridge already owns is a
> LISA question**, and deepstrain's link cannot test it — not because it is hard, but because the cycles
> are not there. That half of P2 is therefore an explicit **LISA forecast**, not a measurement in
> existing data. The map keeps its value; its framing changes.
>
> **(iii) The number that reframes it.** On GW250114 — the loudest event ever recorded — the *data-only*
> Fisher error on δ is **0.3205 against a prior width of 0.2887**: the data are less informative than the
> prior, and the published posterior is **86.2% prior**. Current 2σ exclusion is |δ| ≳ 0.5, i.e. the whole
> prior range: **essentially nothing is excluded today.** The asymptotic floor is δ_sys = **0.0723** at
> crossover **SNR ≈ 124** — ×5 in SNR, ~×125 in rate.
>
> **(iv) Species-4 is not a label, it is P2's central obstruction — this belongs in the abstract.**
> Searching for a deformation while the Kerr waveform model carries systematic error at scale δ_sys makes
> *"Kerr + small deformation"* and *"slightly wrong Kerr model"* **degenerate by construction.** You
> cannot claim a deformation below your own model error. ⇒ **P2's answer is bounded by NR waveform
> accuracy, not by detectors or by statistics.** More events do not fix it; better detectors do not fix
> it; only better waveform models do.
>
> **(v) The strongest LIGO channel is one nobody in the family owns.** deepstrain's ranking:
> **inspiral spin-induced quadrupole** (deviation from Kerr's M₂ = −χ²M³, entering the PN phase over
> hundreds of cycles — plausibly ×10–100 better than ringdown δ, *but requires inspiral PE machinery no
> sibling has*) > ringdown δ (prior-dominated) > echo spacing (**probes near-horizon/ECO structure — a
> different deformation class; must not be merged into this map**) > EMRI drift (LISA).
>
> **(vi) A named blocker, to resolve before building anything.** deepstrain's link needs an injectable
> **h(t; ε)** and, for the ringdown channel, the **QNM spectrum ω_lmn(ε)** of the deformed spacetime —
> which on non-Kerr backgrounds generally **does not separate**. If ansatz cannot produce ω_lmn(ε), the
> ringdown link should be **dropped from the map rather than left as an open box**. Also required: the
> map **ε → δ**, without which δ_sys = 0.072 says nothing about any deformation parameter.
>
> **Net:** question right, chain needs re-scoping before a line of code. deepstrain's own summary —
> *"we could never see a deformation that small with LIGO ringdowns"* — is stated here, in the proposal,
> rather than discovered at the end of it.

**The deliverable** is a quantitative map: **deformation → observable signature → detectability
threshold**, every wall labelled by species per A2's taxonomy (precision / information / definitional /
model-fidelity), with the crossover computed wherever species 1 or 4 applies.

**Why it is substantive regardless of outcome.** No single group typically owns proof-grade non-Kerr
metrics *and* real measured LIGO backgrounds *and* a theory of what a learned probe can represent. That
vertical integration is precisely what the independence discipline bought, and this is the question
that spends it. It is LISA-relevant; it is what the no-hair programme actually wants to know past δ;
and unlike P1 it **cannot fail to produce an artifact**, because the map is itself the result.

**Immediate live input — stated carefully, because an earlier draft of this document overclaimed it.**
G3's overnight scan leaves **two** δ silent, not one: δ=1.5 and δ=1.05 both fire zero orbits, and in
**both** cases it is the *escape* conjunct that goes quiet while drift stays **455× and 511× above the
resolution floor**. The integrable control δ=1.0 (Schwarzschild) likewise sits at **2980× floor with
zero escapes** — i.e. the drift conjunct *alone* would false-positive on a provably integrable metric,
which the campaign already has on record.

So the defensible statement is **not** "the boundary is non-monotonic." It is: **the escape conjunct
fires non-monotonically in δ across the scanned window, and whether that is structure or a
separatrix-window artifact is undetermined.** Species-1 (search/precision) is live and untested either
way. δ=1.02 is the one remaining unscanned value and is running now.

This matters to P2 beyond bookkeeping: the conjunct that goes quiet is exactly the one G3's
PREREGISTRATION addendum (change 4) singled out as needing independent liveness — the same vacuous-
conjunct failure mode that already bit this item twice. **P2's dynamics link cannot be trusted until it
is resolved**, which makes this P2's first sub-question rather than a loose end. *(Provenance: the
overclaimed version came from reading a commit headline instead of the results table; caught by the
sibling bridge session holding the uncommitted δ=1.05 row — **L10**, and an instance of L2's
"too-clean summary" smell.)*

**Then the instrument itself came apart, across four exchanges in one day** — deepstrain reading the
numbers blind, the bridge session testing on banked orbits, this session checking code and statistics.
Consolidated verdict, replacing the running account:

**① The statistic cancels its own signal.** `floor` is not a resolution floor — it is `np.median(drift)`
over that δ's *own* orbits, with `DRIFT_FIRE = 3.0`. So the logged number is a max/median outlier ratio,
self-normalised per δ. On **δ=1.0, Schwarzschild, provably integrable, the drift conjunct clears its own
threshold by ≈993×**, ranking 2nd of 8. The bridge session then measured the decisive quantity — not the
outlier but the **pass fraction** — over 599 banked orbits: **35.0–42.9% of orbits clear 3×median at every
single δ**, spread 7.9 points, *not ordered with fired/silent* (δ=1.5, silent, passes 39.4%; δ=1.3, four
fired, passes 37.0%). A 3×-median cut on a heavy-tailed sample passes ~40% by construction. **The drift
conjunct contributes no evidence to the AND; the detector is escape-only.**

**② The escape conjunct has no counting statistics.** Escapes per δ are **4, 0, 4, 2, 1, 0, 0** out of
~100 orbits — the entire "boundary" is integer counts between 0 and 4. Checked here: 4-vs-0 is a
conditional-binomial **p = 0.125, z = 1.53σ** (the bridge session's "~2σ" was generous), and across 8 δ
the expected number of contrasts that extreme is **exactly 1.00**, with **P(at least one) = 0.66**. The
δ=1.1-vs-δ=1.5 contrast (1 vs 0) carries **p = 1.00 — literally no information.** ⇒ **the scan cannot
support any boundary claim, monotonic or otherwise**, and this survives fixing ①.

**③ The control was never matched.** δ=1.0 was scanned over **one** separatrix band `[9.67]` with **50**
orbits; every treatment δ used **two** bands (inner 4.1–8.1, outer 10.1–18.7) with 98–101. The control
therefore **never sampled the inner band at all**.

**④ A live hypothesis, not yet a correction — deepstrain's rescue attempt.** The control has the *lowest
median drift in the run* (2.91e-06 vs 9.6e-06–5.2e-05), which is the physically right direction, so the
discriminating quantity may be **the median itself — which max/median divides out**. Worth testing, but
**not adoptable yet**, for two reasons found here: (a) ③ supplies a complete alternative — inner orbits
are deeper and drift more *by construction*, chaos or not, and the control lacks that band entirely;
(b) the within-deformed spread is **5.5×** against a control-to-nearest gap of only **3.3×**, and the
medians do **not** order with δ (2.9, 11.9, 9.6, 16.3, 52.5, 29.2, 46.4, 29.0 ×10⁻⁶). If it survives a
matched control it changes the verdict from *"drift is dead"* to *"drift was measured with a statistic
that cancels its own signal"* — better for G3, worse for every drift number on the existing record.

**⑤ Data loss, disclosed by the bridge session.** `main()` never copies `orbits_archive` on resume, so
per-orbit data was dropped: 498 orbits recovered from HEAD, **δ=1.05's 100 orbits are gone**, and
**δ=1.0's and δ=2.0's were already lost** — so **the control cannot be pass-fraction tested at all.**
That is the one row anyone would most want, and its absence is why ④ is a hypothesis rather than a result.

**The fix, and it is this family's own discipline.** δ=1.0 is not a sanity check — it is a **null
distribution**, to be used the way deepstrain uses time-slides: *measure the background, read the
threshold off it*, rather than re-deriving a threshold from the population under test. Their ordered
programme: **(1)** median drift vs δ — does it rise off δ=1.0? (the physics claim); **(2)** two-sample
KS / rank-sum of each δ's population against the control (the calibrated test, whole distribution, statable
null); **(3)** a tail statistic only if anything is left for it to add. All three require **one matched
rescan of the control** — same band count, same N — which now settles ①, ③ and ④ at once.

**⑥ A fourth vacuous gate — and this one is the item's own integration guard.** quantum predicted drift
should track |ΔH| through the A1 guard. **The correlation is real** (pooled ρ = **+0.552**, p = 4.0e-41
over 498 orbits, consistent at every δ) — a genuine prediction, and it landed. **The mechanism is dead on
three counts:** the largest |ΔH| in the ladder is **2.158e-12** against a guard of **1e-4**, so the guard
is non-binding by **4.6e+07×**; the distinctive separatrix-amplification claim measures **ρ = +0.007,
p = 0.87 — zero**; and the loudest orbit in the ladder has **better-than-median** energy conservation.
Drift and ΔH are plausibly both driven by a common *"how hard is this orbit to integrate"* factor, with
ΔH far too small to be the agent.

**The byproduct is the larger result: `A1 guard rejections = 0 of 599`.** dH spans 1.672e-13 … 2.158e-12
against a 1e-4 threshold. **The A1 integration guard has never rejected anything — it certifies nothing.**

> **⑦ And the reason it never fires is now a mechanism, not a margin — the sharpest finding of the thread.**
> Two hypotheses for the anomalously small dH were killed cleanly. **Projection is dead, verified twice:**
> `p_on_shell` appears **exactly once**, in the initial condition, and the loop body is `_rk4` alone — so
> **dH is measured, not constructed** — and a direct h-sweep on one ZV δ=1.3 orbit gives
> **1.045e-03 → 6.817e-05 → 5.933e-06 → 3.729e-07** at h = 0.04/0.02/0.01/0.005, ratios **15.3×, 11.5×,
> 15.9×: textbook h⁴.** *A projected quantity would sit at solve-residual level and not scale with h.*
>
> **That leaves a seven-order contradiction: 6.8e-05 on a directly-integrated orbit at h=0.02, against
> ~1e-12 banked — same integrator, same step.** The resolution: `integrate()` evaluates H **only inside
> `if prev < 0.0 <= s[1]`**, i.e. **only at section crossings — always the same orbital phase.** If the
> energy error is bounded-oscillatory (as expected for KAM-torus orbits, where truncation terms average
> over each period rather than accumulating), **sampling at one fixed phase does not measure its
> amplitude — it measures the error at that phase, which can sit arbitrarily close to a node.**
>
> **⚠️ THE PHASE-LOCKED-SAMPLING HYPOTHESIS WAS FALSIFIED BY ITS OWN AUTHOR WITHIN THE HOUR — and I had
> endorsed it here as "the sharpest finding of the thread." Struck.** Measuring the same orbits both ways:
> **every orbit that *completes* its record gives a crossings-vs-every-step ratio of 1.1–1.3×.** No phase
> artifact, no suppression at the section; **the banked ~1e-12 is genuine for the recorded arc.** It is
> **not** an L13 instance and must not be filed as one. The enormous ratios (1e+07–1e+10×) belong
> *exclusively* to orbits that **terminate early**, where fixed-step RK4 loses energy catastrophically
> during the terminal plunge and no further crossings occur — **the documented, intended behaviour of a
> fix that was correct**, since the old version evaluated dH mid-plunge and rejected exactly the escaping
> orbits it existed to certify.
>
> **quantum's bounded-oscillation reading is the surviving explanation and takes the credit**: error is
> bounded-oscillatory on regular orbits and blows up secularly only where there is no torus — which is
> precisely the plunge.
>
> **But it leaves something sharper than what was proposed.** The A1 guard certifies the **bound, recorded
> portion** of an orbit and is **structurally silent about the escape itself — and escape is the only
> discriminating conjunct in the fire criterion.** One terminating orbit integrates its escape at
> **|dH/H| = 1.663e-03, ~17× *above* the guard threshold the run reports it as passing.** ⇒ **the guard is
> inert in two senses: it has rejected nothing (0/599), and it cannot in principle speak to the quantity
> that decides `n_fired`.** *(Caveat carried into FINDINGS: the terminating orbits are bisected separatrix
> edges, marginal by construction, so these ratios are not a random sample.)*
>
> **This redirects the arbiter.** The h-sweep now has a better target: **sweep the *escaping* orbits.
> If an orbit's escape verdict changes with h, `n_fired` is a step-size artifact — and `n_fired` is the
> entire detector.**
>
> **What must not be written until it resolves:** *"H is conserved to ~1e-12, the integration is clean on
> energy."* The honest form is narrower — **bounded-oscillatory on regular orbits, recorded at a fixed
> phase, with the recorded value not an upper bound on the energy error.** **Phase error is untouched by
> any of this**, so the RK4 step-size sweep remains the arbiter.
That is the **fourth** gate in this single item that turns out to certify nothing: run 1's dead drift
conjunct · run 2's vacuously-passing control · the non-discriminating drift conjunct · and now the guard
itself. **This is no longer a G3 anecdote; it is a pattern in how this campaign builds gates**, and it
belongs in the lessons ledger rather than in one FINDINGS file. *(Not all bad news: H is conserved to
~1e-12 throughout — the integration is clean on energy.)*

**What survives as the arbiter:** the **RK4 step-size sweep**, on the distinction that **energy
conservation and phase accuracy are different failure modes** — RK4 can hold H to 1e-12 while accumulating
real phase error over ~1.2M steps, and it is *phase* error that `drift()` measures. Not pre-empted, just
no longer motivated through the guard. The **non-uniform-sampling test cannot run from banked data**
(orbit records keep no crossing-time series) and needs a rerun that persists them — still the leading
candidate for the residual excess, *because the synthetic assumed uniform sampling and reproduced the
floor's order but not its tail*. And the **n=50 conditioning concern is now top-priority for the control
specifically**: δ=1.0 is the only δ at n=50 against ~100 everywhere else, and it is the row every
absolute-scale statement leans on.

**Bearing on P2.** The bridge's chaos apparatus *is* P2's dynamics instrument, and **the instrument is now
the open question, ahead of any boundary it might measure.** The honest current headline is that it
reduces to **escape-counting at N = 0–4**, on a ladder whose drift statistic is uninformative and whose
integration guard has never fired. Verdicts and FINDINGS belong to the session running G3; δ=1.02
continues and will be banked, but it cannot settle this.

**Owner: all four.** Bridge integrates. This is the flagship.

---

### P3 — Settle a real open integrability question, certificate-grade

Leg J left something **genuinely open**, not merely unfinished: deformed Kerr is *"formally
non-integrable, dynamically regular"* — no Killing–Yano tensor to degree 4, thin-layer chaos only at
ε≈0.98, Carter drift bounded at 7→18% — but **whether any higher-rank Killing tensor survives is
undetermined.** That is an open mathematical question sitting inside our own corpus, currently filed as
a diagnosis.

ansatz's `is_killing_tensor` proves `∇₍ₐK_bc₎ ≡ 0` **symbolically** (§78) — certification is a theorem,
not a numeric residual. So: push the search to **rank 3–4 with exhaustive graded bases**, and either

- **find one** — a new conserved quantity on a non-Kerr spacetime, which is new mathematics touching
  Carter-constant uniqueness; or
- **certify non-existence to stated order** — which converts leg J's diagnosis into a theorem.

The natural proposer is Move A's discover-then-certify skeleton (blind neural discovery → exact
certification), pointed for the **first time at structure that is not known to exist**. Every previous
use recovered something already known to be there (Carter, the holonomy, the LRL vector, the hidden
dimension).

**Shared infrastructure with P2.** Both P2's dynamics link and the long-parked **G4** (the Manko–Novikov
deep chaotic sea at x < 1.5 — the oldest open wall, species-1, crossable in principle) are blocked on
the same missing tool: **a symplectic / extended-precision integrator.** One build unblocks three
frontiers.

**Owner: ansatz (symbolic) + bridge (the discovery front-end).** Integrator: see the quantum ask below.

> **ansatz's read (2026-08-16): feasible, machinery proven and calibrated, gated on P0 not on mathematics.**
> §98 already ran exhaustive rank-4 on ZV; §121 reports Killing-tensor dims 0,1,0,1 against a flat-2D
> control of 3,6,10,15, so the graded-basis search works *and* is calibrated. Pointing it at deformed Kerr
> is the same code. **The risk is not the method — deformed Kerr is rotating and two-variable, so it meets
> the §122 wall.** They rank P3 **second**, behind fixing that wall.
>
> **Pre-registration note they flagged, which must survive into any gate:** §98's own caveat is that
> excluding rank ≤ 4 does **not** exclude rank ≥ 6. *"Certify non-existence" must carry its order in the
> title, not in the footnotes.*

#### The certificate standard, built and gated by tabula (script 166, `b95bce4`) — *P3's numerical half now has a spec*

**⚠️ The finding that travels beyond P3, and beyond this repo.** tabula planted a **per-realization
nuisance channel** — a calibration-offset stand-in with *zero dynamical meaning* — and the engine found it
at held-out ratio **4.2e-17, MORE conserved than the genuine invariant's 1.2e-16**, passing out-of-sample
validation **completely**. The mechanism is not subtle once stated: **held-out validation catches
overfitting, not confounding — a nuisance constant generalises flawlessly precisely because it is
genuinely constant.**

This does not contradict **R7** (out-of-sample is the only defence against **O4**, the smooth-approximation
false positive) — it is a *different* failure mode. But it means the family's certificate defence was
**incomplete**, and neither repo was testing for it: **any certificate resting on out-of-sample validation
alone is exposed.** tabula had pre-registered the condition that would have killed the new clause as
ceremony (*if the confound fails C3, C4 is unnecessary*); **it did not trigger.**

**The four clauses — any one missing ⇒ curiosity, not certificate:**
- **C1 · basis named.** Every null scoped to (family, order); the verdict string is
  `CERTIFY-NO-INVARIANT-IN[family, orderN]`, so the instrument is *structurally incapable* of emitting an
  unqualified "no invariant exists". **This is ansatz's "carry the order in the title" enforced in code
  rather than in review** — two repos converging on the same requirement from opposite ends.
- **C2 · conditioning gated.** Count is `null(W) − deficiency(F)`, never raw `null(W)` (§165). **Trap
  inside the fix: measuring deficiency on W *deletes the finding*, since a true invariant IS a rank
  deficiency of W. Measure on F.**
- **C3 · out-of-sample.** Held-out *realizations*, never in-sample (§164 / O4).
- **C4 · state-functionality (new).** The candidate must be **a function of the dynamical state**, verified
  by predicting it on held-out realizations from their states alone; auxiliary/metadata channels excluded
  by construction, split declared.

**Two self-corrections they recorded, and the first is the fourth instance of a family-wide pattern.**
C4's gate was frozen at an absolute R² > 0.9 and was **unreachable by construction** — feeding it the
*true energy*, definitionally a function of the state, scores only 0.658/0.750 in that harness. **Fixed
with a positive control, not a lowered bar:** C4's statistic is now state-functionality *relative to a
manifest invariant measured in the identical harness*, so every implementation ships its own control.
Second: `--fast` was trimming trajectory *count*, exactly the resource C4's coverage needs — exposing an
asymmetry worth carrying: **C4 rejects cheaply and robustly, confirms only with coverage.** For screening
that is the right way round.

**Their answers to P3's three design questions:**
1. **The ladder runs over TWO axes, and conflating them is what cost round 9.** (i) coordinate-coefficient
   class (polynomial → rational → log); (ii) **momentum** function class (polynomial → rational-in-momenta
   → transcendental). Candidate B was illegible in *every* basis on axis (i) and legible **instantly** on
   axis (ii). For deformed Kerr, index by **(momentum class, momentum degree, coordinate class) with the
   momentum axis primary** — because that is where the grading theorem bites: *an integral analytic in p
   decomposes degree-by-degree into polynomial KT integrals, so the whole analytic-in-p axis is decidable
   and finite.* **P3's rank 3–4 sits at the top of axis (ii)'s first rung, not off it.**
2. **The conditioning gate has no threshold, by design** — *"a fixed threshold is the object we spent
   round 9 removing."* Report p, rank(F), and `null(W) − deficiency(F)`; a library is admissible **iff
   rank(F) = p**, else refuse it. Correction is exact at full sampling, ±1 at coarse.
3. **The handoff, which is the actual division of labour.** *Certify out cheaply:* full-rank library,
   held-out ratio far above the emit line at every degree, no deficiency, **degree sequence
   descending-but-not-converging** (the §97/§160 approximation signature) — most of the ladder by volume,
   and not worth symbolic effort. *Escalate to ansatz:* anything that **emits**; any degree sequence
   **converging** toward machine precision rather than plateauing; and — importantly — **any family where
   the conditioning gate refuses the library**, because *"I could not condition this" is not the same as
   "nothing is there" and must not be silently absorbed into the null.* *Never claim:* non-existence
   outside a named family. **The union over screened families is a map of where we looked, not a theorem**
   — only symbolic certification converts a rung into one, *"which is precisely why the escalation list is
   the deliverable and not a leftover."* The handoff is **one-directional by design**: their certify is
   evidence of absence only relative to F, and their emit is a pointer, never a proof.

---

### P4 — The wildcard: point the discoverability diagnostic at the dark

tabula's representability frontier produced an instrument nobody else has: a diagnostic that infers,
**from raw data alone, with no labels and no ground truth**, whether a system hides a legible conserved
structure — and **abstains honestly** when underdetermined. It has been validated on a real chaotic
laser, real tidal records, and ambiguous real sunspot data.

Every one of those had a known answer. **The mind-opening use is the one where nobody knows.** Point it
at real observational data from systems where the existence of a hidden invariant is genuinely open —
turbulence regimes, biological oscillators, whatever raw observation series can be obtained — and use
it as a **screening instrument**: *is there an undiscovered invariant in here?*

**Stated with its weakness visible:** "substantial" is fuzzier here than in P1–P3, the abstention rate
on genuinely hard real data is unknown, and a screening result is a *lead*, not a finding. It earns its
place because it is the purest available form of the reframe in §1 — a verified instrument pointed into
the dark — and because a single positive lead would be worth more than most of P2's map.

**Owner: tabula.** Bridge role: adjudicate any positive lead against exact ground truth before it is
believed.

> **AMENDED 2026-08-16 on tabula's read — P4 is MIS-SCOPED. Their recommendation is to fold it into P3,
> and I accept it.** Three errors, all mine:
>
> **(i) It conflates two instruments.** The laser / tides / sunspots validation belongs to the
> *chaos-regular detector* (§154: 0-1 test, one-step R², surrogates). The **invariant screener** — the one
> this section proposes pointing at the dark — has touched real data **exactly once**: §156, Newton from
> ephemerides, and it worked *because nature supplied the ensemble* (six bodies, one law, six different
> invariant values).
>
> **(ii) Structural blindness, not difficulty.** The engine finds combinations constant *within* a
> realization and varying *across* them. Segmenting one long series gives every segment the same value ⇒
> zero across-ensemble variance ⇒ **the invariant is whitened out by construction** — the mechanism they
> deliberately used in §161 to suppress H2. **Turbulence records and biological time series fail the
> precondition, not the difficulty test.** And heterogeneous realizations are worse: a per-unit nuisance
> constant (calibration offset, subject identity) is constant-within and varying-across, i.e. a
> **guaranteed false positive that passes out-of-sample validation perfectly** — the held-out defence
> catches overfitting, not confounding.
>
> **(iii) The circularity at P4's centre.** This section assigns the bridge to adjudicate leads against
> exact ground truth — but *"if the law is known well enough to adjudicate, the answer was in a book."*
> **The instrument's output is believable only where it isn't needed.** The only escape is *prospective*
> falsification: a closed-form candidate invariant plus a pre-registered prediction on not-yet-collected
> data, gated by §165's conditioning check and §162's basis disclosure (*"representable in family F"*,
> never *"exists"*). And a null screen is near-worthless, since §162/§164 **proved** illegibility is
> basis-relative — it says something about our library, not the world.
>
> **⇒ Fold into P3.** The certify side, not the emit side: §160–165's basis ladder + conditioning gate
> cheaply yields **"no invariant representable in family F to order N, conditioning-gated,
> out-of-sample validated"**, handing surviving families to ansatz's symbolic prover. Real division of
> labour, same discover-then-certify skeleton P3 already names.
>
> **The convergence this exposes, and it may be the document's real finding.** tabula: *"this is also the
> shape of P1's null — the certificate genre is what this family is actually good at."* Independently,
> ansatz's surviving P1(a′) is **classification, i.e. a certified null to stated order**, and P3 is
> **certify non-existence to stated order**. Three sisters, no coordination, same shape. **The distinctive
> product of this program may not be pointing verified instruments at unknown answers — it may be the
> certified null.**

---

## 3. Assignments — what each repo should study

**Nothing below is started. Each session is asked to read, think, and form an opinion — including the
opinion that a program is wrong, mis-scoped, or already done by someone else.**

| repo | primary | secondary | the specific thing to think hardest about |
|---|---|---|---|
| **ansatz** (`conjecture_machine`) | **P1** — EdGB inversion + 5D stationary hunt at campaign scale | **P3** — rank 3–4 KT certificates on deformed Kerr | Is the inverted EdGB question *well-posed*? What exactly does the verifier need beyond `G_ab + Λg_ab`, and what is the honest cost of a weeks-long campaign vs. a minutes-long one? |
| **tabula** (`SpaceTime`) | **P4** — discoverability screening on unknown-answer data | **P2** — the legibility verdict on non-Kerr signatures | What real dataset is worth screening, and what would a *positive* lead have to look like before you'd believe it rather than abstain? |
| **deepstrain** (`BlackHole`) | **P2** — detectability thresholds for non-Kerr signatures in real measured noise | finish L2 (running) and L4's remaining rungs | Given the deep-FAR ladder and the species-4 model-fidelity wall (crossover SNR≈124), *what deformation size would actually be detectable* — and is that number embarrassing or encouraging? |
| **quantum** (`vestigium`) | **the precision integrator** — see below | the corner-log thread; the unbridged foundations suite | You are the only repo that has *proved* a computation impossible in float64 and then done it anyway (`hinge_mp.py`, e⁻¹⁰⁰ modular tails). P2/P3/G4 are all blocked on symplectic/extended-precision integration. Is that the same muscle, and would you own it? |

**On the quantum ask specifically.** This is deliberately not a foundations question, and that is the
point: the bridge's oldest parked wall (G4) and P2's dynamics link and P3's chaos boundary are *all*
blocked on trustworthy long-time integration of geodesics in deformed vacua, and vestigium is the only
sibling with demonstrated extended-precision muscle. If the answer is "that is not our kind of
question," that is a legitimate answer and should be said.

---

## 4. What this document is not

- **Not a pre-registration.** No prediction is frozen here, no gate is stated, no agreement criterion
  exists. Every program needs its own `PREREGISTRATION.md` before any code runs. (**Rule 4.**)
- **Not a claim.** Nothing above carries a receipt because nothing above is a result. The literature
  positioning in P1 — "nobody has asked this" — is **`[asserted, unverified]`** and must survive a
  prior-art sweep *before* the work, not after. M6 was killed by exactly that gate, and it should be
  run here first. (**Rule 5 / L10.**)
- **Not a reordering of the ledgers.** FALSIFICATION_LEDGER and FALSIFICATION_V2 keep their standing
  items. G3 finishes, G4 stays parked until the integrator exists, the sister rounds continue.
- **Not a licence to relax independence.** P2 in particular routes results between all four repos.
  Read-only stays read-only; the sister-ask pattern stays the channel; agreement stays evidence only
  because the repos stay ignorant of each other. (**Rule 2 / L5.**)

---

## 5. The one-sentence version

**The instruments are validated — that was the last ten weeks' product. The substantial thing now is
the first result whose answer wasn't in a book, and the two best-posed candidates are *"for which
theories does an exact black hole exist?"* and *"would we see it if Kerr were wrong?"***
