# The Bridge — Capstone

*State of the program, **2026-07-26**. A single reading map for the whole body of work: what the bridge is, the
full scoreboard, the results that hold the weight, the patterns that recurred, and — given equal billing —
what failed or stayed out of reach. Every number here traces to one gated leg and its commit; this document
introduces **no new claim**. If a figure below disagrees with a leg's `FINDINGS.md`, the leg wins.*

---

## 1. What the bridge is

Four sibling projects, built with **independent roots on purpose**, cross-validated read-only:

| project | repo | epistemology — *how it knows* |
|---|---|---|
| **ansatz** | conjecture_machine | **deductive** — exact symbolic+numeric GR; proves metrics, invariants, hair-counts. The ground-truth oracle. |
| **tabula** | SpaceTime/curvature | **inductive** — neural geometry-from-observation; sees only observations, never the metric. The representation oracle. |
| **deepstrain** | BlackHole | **empirical** — real LIGO ringdown/echo/PBH searches; sensitivity from injections, significance from measured background. The measurement oracle. |
| **quantum** | [vestigium](https://github.com/sumit7194/vestigium) | **foundational** — verified QM-foundations lab (KK projections, weak measurement, detector geometry, entropic time). Joined 2026-07-03; repo public 2026-07-26. |

The bridge keeps all four **READ-ONLY** and holds one discipline (THE_BRIDGE.md §2):

> *Independence is capital you have been accumulating. The bridge is where you spend it — so spend it
> cleanly.* … *Never tune one oracle to match another. If they disagree, that's a result, not a bug to fix.*

Every leg follows **pre-register → build → gate → document**: the prediction and the agreement criterion are
frozen in a `PREREGISTRATION.md` *before* the compute runs. The north star, verbatim from the working
sessions: **robustness and correctness is the only north star.**

**Scale.** 36 pre-registered gated legs **plus 26 falsification attacks** (`falsification/`), across four
repos. No single leg is the asset — the triangulation is.

**Two halves.** Legs A–V *build* cross-validated results. The **falsification campaign** (from 2026-07-22)
tries to *destroy* them, including a **self-audit tier** that turns the method on the bridge itself. Both
halves are reported here; the second is younger and has already killed one of the first's headline claims.

---

## 2. The scoreboard

Verdicts are quoted as the legs state them — passes, nulls, and refutations alike. `commit` is a representative hash.

### The spine — "how many numbers is a black hole?" (the founding triangle)

| leg | question | verdict | key number | commit |
|---|---|---|---|---|
| 1 | moduli count vs inferred observable count | **agree + named departure** | RN 2/2; dyonic 3→2 (Q²+P² degeneracy, ansatz-proved) | `0b0b9d6` |
| 1b | same for rotating holes | **pass** | Kerr=2, KN=3; KN-Δ-symmetric=2 (controlled) | `d59e189` |
| 2 | does the legibility law explain the sim→real tone-count gap? | **useful negative** — no scramble signature; gap is *information-limited* | reproduces deepstrain's own parked verdict | `cfd1acb` |
| 3 | do proof, representation, and measurement concur? | **the spine closes** — all three give 2 | δ=−0.16 [−0.46,+0.33]; BF=2.6 for 2- vs 3-number | `f847b6a` |
| Tier3 | are ansatz's exact bounds consistent with GW150914? | **pass** | area-theorem margin 1.56×; radiated 4.7% < 29.3% cap; 2 tensor modes | `7d9e4aa` |

### Phase-1 exploratory legs

| leg | question | verdict | key number | commit |
|---|---|---|---|---|
| 4 | is pure friction non-geometric? (1+1D) | **mixed** — conservativeness proved; universality = WEP restatement | A₁=0 identically when conservative | `6f1ca54` |
| 5 | does a targeted curriculum sharpen shadow-edge accuracy? | **pass** (H1); H2 false | error 23%→2%, variance 20× down; b_crit 6.39→5.31M | `d51c1b3` |
| 5b | curriculum on asymmetric Kerr shadows? | **mixed** — retrograde improves, prograde degrades | retrograde 3.47%→1.32%; prograde 2.30%→19.1% | `0bfd2e3` |
| 5c | can the bottleneck count fingerprint Carter-breaking? | **false** — both exact & deformed return 2 (KAM tori) | σ(K) jump 5.7×10⁵, count unmoved | `dfeb1f2` |
| 6 | does orthogonal structure protect indirect-observation legibility? | **pass** | scramble gap 0.31 (generic) vs 0.048 (orthogonal) | `cfd1acb` |
| 7 | what dimension does noisy ringdown appear? | **H1/H3 false** — clean 4D (curvature), noisy → 0D | knee 4 (predicted 2); +noise → 0 | `bac36cf` |
| 7b | does FFT magnitude recover true dimensionality? | **conditional pass** — restores 2D in standardized space only | locked FFT-std knee=2 (R²=99.83%) | `566f010` |
| 8 | is the exact echo-delay law right; do GW150914 echoes exist? | **theory pass; search null** | Δt∝−8M ln(λ); Abedi anchor 98.5–99.7%; p≈23% | `d4af77a` |
| 8b | do physics-grounded wormhole templates hold search sensitivity? | **mixed / underpowered** | 50%-recovery 0.85σ→1.25σ; comb ties ML | `91bd4fb` |

### The Move cycle (A–I) — pre-registered discovery→verify + adversarial falsification

| move | question | verdict | key number | commit |
|---|---|---|---|---|
| A | blind neural discovery + exact certification of a hidden symmetry | **pass** | recovered Carter coeff cosine 1.0000; certify gap 4 OOM | `acad48e` |
| B | does exact QNM match the measured ringdown numerically? | **pass, three pipelines** | v2 δ=−0.159 vs measured −0.151 (Δ0.008); v3 remnant Δ=0.00 M⊙ | `6ab92cd` |
| C | does learned geometry recover the coordinate-free Weyl invariant? | **mixed** — bulk yes, edge no | magnitude R²=0.96; Petrov O/D 0.75 (<0.95); exact owns the edge | `4b05902` |
| D | where does a deformed Kerr lose its hidden symmetry? | **pass — a 3-boundary hierarchy** | exact ε*≈0⁺; approximate ε*≈0.07 (KAM); chaos ε≈1.0 | `213dc6c` |
| E | do the meta-findings survive outside GR? | **qualified** — track *curvature*, modest size | legibility gap 0.127 (16× flat control) | `388d9ae` |
| F | is the edge curvature or boundary? | **pass — corrects E**: it's metric divergence | flat-diverging fires 4.5×; curved sphere quiet 0.49× | `be49ea9` |
| G | do the main claims survive adversarial falsification? | **survive, sharpened** | counter calibrated corr 0.98 but +1 on curved; vacuum counts threshold-fragile | `aab96c3` |
| H | is the horizon a learnability edge; does a hybrid beat pure-learned? | **H1 pass, H3 refuted** | horizon edge/bulk 85–88×; noise-amplification is the real bottleneck | `b059bb1` |
| I | are all the edges one mechanism or two? | **pass — two kinds** | recovery edge → 0 at exact; physical edge var-ratio 5×10¹⁵ | `3aadfb9` |

### Extension legs (J–V)

| leg | question | verdict | key number | commit |
|---|---|---|---|---|
| J | deformed-Kerr fate: chaos or near-integrable? | **formally non-integrable, dynamically regular** | no KY to degree 4; thin-layer chaos at ε≈0.98; Carter drift 7→18% bounded | `837d4fc` |
| K | do MDL, moduli, and measured DOF agree on the count? | **pass** — nonlinear ID confirms observable count | linear MDL overcounts 5/7/7; nonlinear steps +1.21, +0.04 | `cb97410` |
| L | does amortized-NPE legibility predict real precision? | **mixed** — ranking holds; amortization gap orthogonal | M>χ>δ identical; corr(amortization,transfer)=+0.04 | `832b606` |
| M | how does broken integrability show in EMRI frequency? | **pass** — a frequency-map shift, regular resonances | bump lowers ω_φ −4.8% (3:4) → −12.6% (1:3) | `5299c64` |
| N | does discover→verify generalize past Killing tensors? | **pass** — recovers a geometric-phase holonomy | geodetic precession 1.322 vs exact 1.316 (0.5%) | `d22e5ad` |
| O | is the KY search a reusable classification instrument? | **pass** | KY on Kerr/KN/KdS/Taub–NUT; none on bumpy; incl. non-Kerr Taub–NUT | `b76d1fb` |
| P | can three messengers constrain non-Kerr deviations? | **can't-run + forecast** (honest data gap) | 3 objects, 8 mass orders apart; spread <0.034 at ε≤1 | `03c5c97` |
| Q | are legible metrics exactly the KY-integrable ones? | **pass — 8/8, φ=1.0** | tabula legibility ⟺ symbolic KY-integrability; 3 non-integrable classes | `3b69c49` |
| R | does tabula's regime detector survive on GR ground truth? | **pass + diagnosed scope boundary** | Kerr/MN-outer EMIT-regular; integrable≠regular dissociation; di-hole = scope boundary | `70d5e2f` |
| S | does m_n=n/R hold across four independent routes? | **pass — first four-repo cross-validation** | quantum 0.22% · FDTD 0.66% (cross-impl 0.44%) · learned 1.44%, R²=0.99996 | `d84e74a` |
| T | does the family's own instrument close Mercury's books? | **pass — consistency, not detection** | 568.4 − 532.3 = 36.1 vs exact GR 43.0, within ~1σ of 6.6″/cy floor | `4e9c643` |
| U | does the 6D twist split the KK tower (the axion)? | **pass** | tower m=√(n₁²+n₂²) err 0.33%; χ splits √2→1.241/1.692, Δ(m²) 0.25% match | `d8515fd` |
| V | box-dimension (from GR orbits) on quantum's detector wall? | **pass** | Cantor D=0.6309 exact; reproduces quantum's JS 0.342/0.438 to 2 decimals | `c24d725` |

### The falsification campaign (2026-07-22 →) — postulates stated *to be killed*

Pre-register → attack → **three-valued verdict** (KILLED / SURVIVES / UNDECIDED). Full detail in
[FALSIFICATION_LEDGER.md](FALSIFICATION_LEDGER.md) (v1) and [FALSIFICATION_V2.md](FALSIFICATION_V2.md) (v2+).

| tier | what it attacks | outcome |
|---|---|---|
| **K** (expected kills) | sharpening shots | K1–K5 **all KILLED**, each yielding a mechanism, not a bare "no" |
| **G** (genuine bets) | the real uncertainty | **G2 KILLED** — the flagship *legible ⟺ KY-integrable* fell to designed adversaries. **G7 KILLED** (see §4a). G6 SURVIVES (partial) |
| **M** (moonshots) | low odds, stated up front | **M2 KILLED** (κ scheme-dependent); **M6 KILLED by its own prior-art gate** |
| **V** (validation) | expected to survive; harden instruments | V1, V2, V3 **all SURVIVE** — the instrument canaries held |
| **R** (refinements) | bred from v1 corpses | R1–R9: 4 killed, 1 postulate-true, 3 undecided, 1 cross-gate + a new obstruction (**O4**) |
| **S** (spectral/KK) | the drums→tori→curved arc | **S1 KILLED** (flat 4-tori not spectrally determined); **S2 SURVIVES**; S3 supported |
| **A** (self-audit) | **the bridge's own record** | **A1 SURVIVES** · **A2 KILLED G7** · **A3 KILLED** (a load-bearing citation was never verified) |

**Running total: 12 kills, 6 survivals, 4 undecided, 1 postulate-true — and 10 self-caught instrument bugs,
every one a silent failure that looked like a result.**

---

## 3. The five load-bearing results

The work that carries the weight — each a place where independent epistemologies concur, or disagree for a
named reason, on something none could establish alone. **One of them is a falsification of our own flagship
claim, and it belongs here on merit: the replacement is sharper than what it replaced.**

1. **The count triangulates (spine + K).** A black hole is a **2-number object**, confirmed three
   independent ways — ansatz *proves* it, tabula *infers* it from observation, deepstrain *measures* it
   consistent — with a fourth (info-dimension, leg K) agreeing, and the one departure (dyonic 3→2)
   *predicted and mechanism-proved* (Q²+P² degeneracy). A claim surviving deduction, representation-learning,
   and empirical measurement at once is confirmed in a way no single method gives.

2. **~~legible ⟺ KY-integrable (leg Q)~~ → FALSIFIED, and replaced by something sharper (G2, R1, R2).**
   Leg Q's **8/8, φ=1.0** agreement across the catalog is a real measurement and stands. **The law it was
   read as does not.** All 8 metrics were *found, not designed*, and Collinson 1976 forces KT⇒KY on type-D
   vacua — so the catalog's homogeneity manufactured the coincidence (**L1**). Designed adversaries killed
   it both ways: Candidate A (Killing tensor, **no** KY root) is **legible**; Candidate B (transcendental
   invariant) is **illegible**. Legibility tracks neither KY nor integrability but **representability in the
   probe's basis** — and R1 named the axis (the *momentum* basis, not coordinate). *This is the program's
   most valuable result precisely because it is a kill:* a flagship claim was replaced by a mechanical,
   movable boundary, and the replacement was then confirmed in both directions on a metric whose answer we
   knew independently.

3. **The GW250114 stack (Move B v1→v3 + start-time referee + mimicker status).** Three independent QNM
   pipelines (exact-Leaver, NPE, field-standard `ringdown`) agree on the remnant to **0.00 M⊙**; the exact
   221 overtone gives δ=−0.159, matching the *measured* δ=−0.151 to **0.008**. A spin tension that surfaced
   in v3 was then **explained** as one measured 9-point start-time systematic (leg B, `0ff1ffa`) — and in
   ansatz §110's two-light-ring taxonomy every tested observable reads "one ring" (leg 8 §7). Triangulation
   did its job twice: it surfaced the systematic, then it accounted for it.

4. **The KK ladder, 5D → 6D → curved (legs S + U + S2).** The KK mass tower `m_n=n/R` established across **four repos by
   four failure-mode-disjoint routes** (symbolic proof / direct numerics / independent FDTD / neural
   discovery, leg S) — then extended to **6D** where the bridge's own T² simulator reproduces the
   sum-of-two-squares tower and shows the **twist χ is a measurable axion**, splitting the degeneracy exactly
   per the SL(2,ℝ)/SO(2) coset metric (leg U) — then shown to be a **method, not a flat-space artifact**:
   the same rest-buzz instrument reads a **curved** hidden S³ to 0.42%, with degeneracy (n+1)² *measured*
   via the n≥ℓ cutoff (S2). The founding discover-then-verify pattern, run through a hidden *dimension*.

5. **The self-audit tier — the method turned on itself (A1, A2, A3).** The bridge audited its own record
   three times and the audits **bit**. A1 swept 93 too-clean numbers (all legitimate; a standing guard
   installed). **A2 killed G7**, the program's own headline meta-claim, and replaced it with a four-species
   wall taxonomy that three sisters then tested out-of-sample — amending it twice. **A3** found a
   load-bearing theorem cited five times across the corpus with no identifier and no verification record;
   it turned out to be *true*, which is the point: **an unverified claim of ours was false the same week,
   and the process was identical. Only the luck differed.** A program that only reports its hits is not
   doing cross-validation; one that will not audit its own scoreboard is not either.

---

## 4. The recurring themes

Four patterns showed up across legs that were designed independently. Gathering their instances is the point
of this section — each theme is only visible once its scattered appearances sit together. **One of the four
has since been killed by our own audit and replaced; it is kept below with its corpse visible, because how a
theme dies is worth as much as the theme.**

### 4a. ~~Walls are instrument-relative~~ → **KILLED, and replaced by a four-species taxonomy**
This was the program's recurring theme, promoted to meta-claim **G7** and "fed" eight times. **A2 attacked it
deliberately and it died** — on the strict reading it is *false* (S1: two flat 4-tori, provably non-isometric
and provably isospectral — no instrument upgrade crosses a wall where the information is not in the channel),
and on the permissive reading it is *unfalsifiable* (saving it requires counting any channel change and any
unbounded "in-principle" instrument as an upgrade).

**Why eight rounds missed it is the finding:** *you only notice a wall as a wall when you cross it.* All eight
"confirmations" were precision walls, which announce themselves. Information and definitional walls never feel
like walls — they feel like **results**. S1 felt like *discovering* that 4-tori aren't spectrally determined;
M2 felt like *measuring* that κ is scheme-dependent. So they were filed as findings and never put to G7. The
meta-claim was tested against a sample that structurally excluded its own counterexamples.

**The replacement** — four species, *not* a partition, with membership that can depend on regime and on a
computable crossover:

| species | diagnostic | prescription |
|---|---|---|
| **1 · precision** | does it converge as you refine? | keep pushing |
| **2 · information** | do two distinct configurations give *identical* in-channel data? | **change channel** |
| **3 · definitional** | do two legitimate conventions give different limits? | stop measuring; report the scheme-dependence *as* the result |
| **4 · model fidelity** *(deepstrain)* | does the error stay put as the measurement improves? | improve the **model**, not the measurement — and locate the crossover |

All three sisters then tested it out-of-sample and **two amended it**: deepstrain contributed species 4 (an
SNR-independent waveform bias, crossover at SNR≈124); quantum showed species 3 can *switch off* with a
physical parameter (Λ≈2–4) — while our own R8 showed κ's does **not**, so "definitional" must be checked per
case. quantum then confirmed the species-2 prescription against a species-3 wall: κ's regulator spread is
unmoved by refinement (41.8→41.7%) while mutual information's dies as s^−2.26 on the same lattice.

The old theme's instances remain true as *species-1* cases: δ is information-limited given SNR (legs 2, 7, L); MN thin-layer chaos is below
box-dimension's resolution but above the frequency-drift detector's (leg J); di-hole chaos is unreachable by a
trajectory 0-1 test but reachable by a section frequency-drift (leg R); a CNN ties a realizable matched-filter
bank because both are capped by *bank mismatch*, not by learned-vs-classical (Phase-5 note, `84b54d0`); and the
quantum probe images the Cantor boundary only down to its wavelength λ≈6.3 cells (leg V). The bridge's chaos
lenses and tabula's tile *complementary* regions — which is exactly why multi-instrument cross-validation is
worth doing.

### 4b. Discover-then-verify generalizes
The Move-A architecture (blind neural discovery → exact certification) is not tied to Killing tensors. It
recovered a **geometric-phase holonomy** (leg N, 0.5%), the **Laplace–Runge–Lenz vector** on real ephemerides
(leg T), and a **hidden dimension** (legs S, U). Same skeleton, four different classes of hidden structure.

### 4c. One number, many routes
The most trustworthy results are dimensionless quantities reached by disjoint methods: the count (four lenses),
the remnant mass (three QNM pipelines, Δ=0.00 M⊙, Move B), the KK ladder (four repos, leg S), the axion split
(FD simulator vs closed-form coset, leg U). Agreement across methods with *disjoint failure modes* is the
asset.

### 4d. Disagreements are findings — the correctness ledger
The discipline "if they disagree, that's a result" repeatedly caught **real bugs**. This is the program's
strongest existence proof that cross-validation earns its keep:

- **A metric bug in a source repo, surfaced by the bridge.** Pushing the MN positive control to extreme spin
  exposed that ansatz's `manko_novikov` was *never asymptotically flat for q≠0* (`g_xx → 0.085×` Minkowski at
  infinity) — invisible to the vacuum check. ansatz fixed it (§102); q=0 stayed byte-identical to Kerr, so all
  bridge results held (`25248c4`). A correctness win the bridge *found*, in a sibling, that the sibling's own
  checks could not see.
- **A false positive in the bridge's own detector.** The two-trajectory Lyapunov read λ≈+0.32 on a
  box-dim-*regular* orbit — finite-difference force noise. Caught by the positive control; ansatz then
  *independently reproduced* it and shipped de-noised defaults (§105). The de-noised λ and box-dim agree the
  orbit is regular (`df89527`).
- **A convention trap.** `section_freq` returns the *complement* of the epicyclic ratio (a 2/3 resonance
  appears at ν=1/3); the naive lock-counting statistic would have false-flagged the smooth Kerr riser, so the
  discriminator was switched to slope-collapse (leg M).
- **An SVD artifact**, unmasked by a momentum-dependence check in the quartic Killing-tensor search (leg J,
  A2); **data leakage** found and fixed in the rotating curriculum (leg 5b); **threshold-fragility** of the
  vacuum-BH counts surfaced under adversarial test (Move G). Sisters caught their own too — deepstrain's
  co-injection protocol shrank an apparent 10% matched-filter win to a 3% tie.
- **A sister caught a bridge bug that invalidated a celebrated result.** tabula could not run K5 and correctly
  diagnosed why: the bridge's drum grid used the same offset in x and y, silently **disconnecting each drum
  into 3 congruent pieces**, so the two "isospectral" operators were *one matrix relabelled*. Our
  "exact, resolution-independent isospectrality" was a triviality. Verdict survived on the continuum theorem
  plus convergence; the mechanism was retracted and a connectivity assertion installed (**L2**).
- **The bridge's independent reimplementation found an obstruction the original missed.** Re-deriving ansatz
  §123's emit criterion in our own code reproduced all four teeth *and* surfaced **O4**: a degree-6 polynomial
  that **falsely emits** by approximating a transcendental invariant. tabula reproduced it at degree 8. Three
  repos then independently converged on the same defence (generalisation testing) — which R7 showed is the
  **only** one available, because approximation and representation are indistinguishable in-sample.
- **Two retractions of our own, in one day, same failure mode.** M6 asserted a mechanism *from reading* and
  shipped it unrun (R7 measured it false by 28×); R6 asserted one *from memory* against its own pre-registered
  discipline, and it was **inverted** — caught by quantum re-testing the item. Both are recorded in place with
  the original wording struck rather than deleted.

---

## 5. The honest-miss ledger

Pre-registered fails, nulls, and can't-runs — given equal billing, because a program that only reports its
hits is not doing cross-validation.

- **A1 refuted** — an NPE's amortization gap does **not** predict its sim→real transfer (corr≈+0.04, leg L).
- **Leg P can't run** — no single object has ≥2 spins across the three messengers; reported as a forecast + an
  explicit data gap, not a constraint (`03c5c97`).
- **Echoes null** — no GW150914 echo at the exact predicted spacings (leg 8, p≈23%); ML and comb searches null
  at the Abedi Δt on 4 events (`beb3a0b`).
- **δ is information-limited** — the no-hair overtone carries too little information to fingerprint at current
  SNR, even in the richer NPE (legs 2, L); not a legibility effect.
- **Leg 5c false** — the bottleneck count cannot fingerprint Carter-breaking (KAM tori keep dim=2).
- **Move H hybrid refuted** — a hybrid recipe does not beat pure-learned; observation noise amplification is
  the real bottleneck.
- **The di-hole scope boundary** — scattering chaos escapes the trajectory 0-1 test; diagnosed honestly as a
  domain limit, not a detector failure (leg R).
- **Parked frontier** — the MN deep chaotic sea at x<1.5 is beyond trustworthy integration on both sides;
  needs a symplectic / extended-precision integrator before the frequency-drift detector can point at it.
- **Cut legs** — the original legs 9–12 were removed in an integrity audit (`b6edddc`) as not meeting the bar.
- **R6 retracted twice over** — its mechanism was inverted (spatial vs *spacetime* dimension) and its numbers
  turned out to be an artifact of a 3-term truncation: extending the fit makes `b` **diverge** by 14× its own
  error (R9). Honest status: *this instrument cannot extract the subleading log at all* — a species-1 wall,
  not the species-3 one R6 claimed.
- **M6 killed by its own gate** — the "publishable methods result" was admitted conditionally on a prior-art
  sweep. The sweep found both halves already in the literature, with sharper thresholds than ours. The gate
  did exactly what it was for: the cheapest possible way to not write a paper that would have been scooped.
- **S3's gate was unreachable by construction** — a threshold set against a quantity K2 had already documented
  as staircase-limited. The postulate was supported; the frozen bar was not met; it was **not** relabelled.
- **G7 killed** — see §4a. The program's own headline meta-claim, attacked deliberately and lost.

---

## 6. Method and open frontiers

**The read-only rule + the sister-ask pattern.** The four source repos are never modified. When a leg is
blocked on something only a sibling can produce, the bridge files a concrete ask in `SISTER_REQUESTS.md`,
relayed to that sibling's own session (this is how ansatz's §77/§101/§111–§113 and tabula's §127/§157 and
deepstrain's §18/§22/§23 were produced). Notably, the flow has gone **upstream** too: the bridge's
frequency-drift detector was natively reimplemented *inside* ansatz (§105) — the first instrument, not bug, to
propagate into a source repo.

**The lessons ledger.** Twelve standing rules now govern the work, each bought by a specific failure and
several contributed by sisters — L1 proxies masquerade as laws on homogeneous catalogs · L2 too-clean is a bug
smell · L3 design kills to output curves · L4 survivals localize · L5 independence pays twice · L6 the outward
turn is event-driven · ~~L7~~ *(killed by A2)* · **L8** state the units of both sides *(tabula)* · **L9** scan
the physical regime *(quantum)* · **L10** every claim carries a receipt · **L11** a relayed claim is repeated,
not corroborated — and the *originating* repo must tag it *(ansatz)* · **L12** a residual needs both a floor
probe and a limit probe *(quantum)*. Full text in [FALSIFICATION_V2.md](FALSIFICATION_V2.md).

**Open threads (all optional):**
- **Leg S/U four-route breadth** — leg U is bridge-numeric + ansatz-symbolic only; a neural 6D discovery
  (tabula) or 6D direct numerics (quantum) would give it leg S's four-route breadth.
- **The MN deep sea (G4)** — parked pending a higher-precision integrator; the oldest open wall, and a
  species-1 one (crossable in principle).
- **quantum's foundations suite** — weak-measurement/Born-rule, decoherence, Zeno, Bohmian, CSL, Wigner's
  friend remain unbridged; the fractal boundary (leg V), entropic time and the 2D κ-vs-I(A:B) build are consumed.
- **The corner-log** — quantum's 2D result used strip geometry only; corners are the obvious next thing that
  could behave differently.
- **The generator-based emit criterion (ansatz)** — deciding "does an invariant exist in span(Φ)" from
  `{I,H}=0` alone, with no data and no threshold. It would dissolve O4 *a priori* rather than catching it
  after the fact. Gated on their own symbolic prior-art sweep.

**Per-leg detail** lives in each `leg*/FINDINGS.md` and `falsification/<ID>/FINDINGS.md`; the dated narrative
in `JOURNAL.md`; the running plan and phase ledgers in `BACKLOG.md`; the original design map in
`THE_BRIDGE.md`; the standing attack programme in `FALSIFICATION_LEDGER.md` and `FALSIFICATION_V2.md`.

---

*Four ways of knowing the same physics, made to meet cleanly — and then made to attack each other, and
themselves. The contribution is method, end-to-end ownership, and cross-validation, reported honestly: hits,
misses, and retractions alike. The scoreboard above lists a killed flagship and two of our own retracted
mechanisms because a scoreboard that cannot lose is not a scoreboard. Robustness and correctness is the only
north star.*
