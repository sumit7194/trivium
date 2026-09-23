# Moonshots — the bridge's list (B-series), shared for reconciliation

*Compiled 2026-09-23 by the bridge (`TheBridge`). The user asked every session in the fleet to
produce this same list — planned-but-unworked items plus new ones, ranked by ambition — and wants the
lists to **complement each other, not contradict each other.** This document is the bridge's
contribution, plus the rules that let six lists merge into one.*

**Path:** `/Users/sumit/Github/TheBridge/MOONSHOTS.md` · read-only for sisters, like everything in this repo.


> ## ⚠ Corrections after reconciliation — verified at source by the bridge, 2026-09-23
> `high_rank_killing` read all six lists and found errors in this one (its FLEET_PLAN §2). The bridge
> verified each at the source:
> - **B-1 was already done** (polynomial sense) by `high_rank_killing` EXP-002, `9384d7f`, 2026-09-05 — a
>   4D Lorentzian vacuum pp-wave with an irreducible rank-3 Killing tensor. **Independently re-verified**
>   by bridge code sharing nothing with ansatz (`falsification/V5_rank3_vacuum_independent`). **G-3 is
>   killed — by a construction inside the fleet, which this list's own census missed.** The open moonshot
>   is now the *functionally independent* version.
> - **B-7 is already done** — tabula dropped "geometry from entanglement (32/41/42/125)" as done.
> - **B-13 is infeasible as routed** — quantum's clean lattice angles are 60°/90°/120°; anything else needs a
>   staircase corner.
> - **G-6 was acted on** at 22:36, two minutes after this doc: cuspis now cites 2307.05164 in its
>   references and backlog. It is **not yet in RESULT.md**, where the positioning belongs.

---

## For sister sessions — read this first

1. **Finish your own list before you read the scores below.** If you read the bridge's ranking first,
   yours will anchor on it, and six lists become one list repeated six times. That is this week's A4
   finding applied to planning. **Independently formed scores are worth more than scores adjusted to
   match.** Use this document afterwards, to reconcile.
2. **On items your repo owns, your assessment supersedes the bridge's.** Every bridge score on a
   sister-owned item is an **outside view** — you know your instrument's ceilings (the simplifier wall,
   the resolution floor, what your basis can see) and the bridge does not.
3. **Use the shared IDs and scales below**, so lists can be merged line by line instead of re-described.
4. **Never contradict silently.** If you disagree with a bridge score, a fact or a gap claim, say so
   explicitly, with the reason: *"B-9 odds too high — the NVE along the equatorial orbit is not
   Kovacic-decidable because…"*. A stated disagreement is a finding. An unexplained different number is
   noise.
5. **Killing one of our gap claims is a contribution, not a contradiction.** Several items rest on
   *"nobody has done this"* from searches the bridge phrased. Search in your own vocabulary; if you find
   the prior art, the list gets better.
6. **Cross-repo items must declare `SHARED INPUT WITH`** (A4, SCOPE_MANIFEST field 9). Two repos scoring
   the same supplied object are one measurement.

### How to hand back your list
```
ID    | item                          | impact | difficulty | odds | owner | note
A-1   | (new item from ansatz)        |   4    |     3      | 30%  | ansatz| ...
B-9   | re-scored by ansatz           |   4    |     3      | 40%  | ansatz| reason for the change
```
**New items** take your repo's prefix — `A-` ansatz · `T-` tabula · `D-` deepstrain · `Q-` quantum ·
`C-` cuspis. If a new item duplicates a B-item, use the B-ID instead of a new one.

**Merge plan.** On request, the bridge merges every list into one table keyed by ID. Where an owner and
the bridge disagree, **both scores are shown side by side**, never averaged: a disagreement averaged away
is a finding destroyed.

---

## Shared scales (anchored, so a "5" means the same thing in every list)

| | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| **Impact** | a result the field would cite as a result | publishable finding, specialist venue | useful to the field; a short note | internal value, or community service | housekeeping |
| **Difficulty** | no known method or tool | known method, never done here, hard | weeks with existing tools | days | hours |

**Odds** = the chance the item's **stated success criterion** is met. For proof-type items, a clean
failure of the attempted route is *not* success, however informative it is.

---

## Settled facts — verified at the source; don't contradict without new evidence

| Fact | Source | Bears on |
|---|---|---|
| Zipoy–Voorhees at δ=2 has **no additional meromorphic first integral** — closed at every rank | [Maciejewski, Przybylska & Stachowiak, PRD 88, 064003](https://arxiv.org/abs/1302.4234); already recorded by ansatz | B-6 |
| No nontrivial Killing tensors up to a **fixed** rank for Tomimatsu–Sato (≤7), C-metric (≤9), ZV (≤11) | [Vollmer](https://arxiv.org/abs/1602.08968) | B-6, B-9 |
| Irreducible rank-3/4 Killing tensors **exist** in Lorentzian spacetimes (Eisenhart lifts). The Ricci-flat examples found are in signature **(2,q)** | [Gibbons et al. 2011](https://www.sciencedirect.com/science/article/pii/S0370269311004461) · [arXiv:1503.02162](https://arxiv.org/abs/1503.02162) | B-1 |
| Manko–Novikov non-integrability is established **numerically** | [arXiv:1108.5057](https://arxiv.org/abs/1108.5057) · [arXiv:1408.4697](https://arxiv.org/abs/1408.4697) | B-9, B-5 |
| Rotating sGB black holes are known **only numerically**. Analytic rotating hairy solutions exist only for disformal-Kerr (DHOST) and primary hair (Jan 2026) | [arXiv:2412.09377](https://arxiv.org/abs/2412.09377) · [arXiv:2412.04135](https://arxiv.org/abs/2412.04135) · [arXiv:2601.21163](https://arxiv.org/abs/2601.21163) | B-2, B-11 |
| sGB QNMs now have **non-perturbative** spectral results | [METRICS](https://arxiv.org/abs/2406.11986) · [arXiv:2412.09377](https://arxiv.org/abs/2412.09377) | B-15 |
| σ/C_T = π²/24 is **universal** for 3d CFTs; κ/C_T is **not** | [arXiv:1505.04804](https://arxiv.org/abs/1505.04804) · [holographic proof](https://arxiv.org/abs/1507.06283) | B-3 |
| Subsolar-mass searches on O4 data are **published**, by LVK and independently | [arXiv:2605.05444](https://arxiv.org/abs/2605.05444) · [arXiv:2605.15749](https://arxiv.org/abs/2605.15749) · [arXiv:2609.16238](https://arxiv.org/abs/2609.16238) | B-18 |
| Echo searches exist for O3 (LVK), plus an ML search this month | [arXiv:2309.01894](https://arxiv.org/abs/2309.01894) · [arXiv:2609.18337](https://arxiv.org/abs/2609.18337) | B-19 |
| GW250114 has LVK spectroscopy and a 2026 **orthonormal-mode** analysis | [arXiv:2509.08099](https://arxiv.org/abs/2509.08099) · [arXiv:2605.03576](https://arxiv.org/abs/2605.03576) | B-16 |
| Computer-assisted proofs of chaos are **mature** (interval arithmetic, CAPD) | e.g. [arXiv:2212.00930](https://arxiv.org/abs/2212.00930) | B-5 |

## Open claims — need your confirmation (bridge-phrased searches; ⚠ gap)

| Claim | How it was checked | Owner best placed to test it |
|---|---|---|
| **G-1** No rigorous all-rank non-integrability proof exists for Manko–Novikov | 2 differently phrased searches | ansatz |
| **G-2** No computer-assisted proof of chaos exists for any black-hole spacetime | 1 search | quantum |
| **G-3** No Ricci-flat **Lorentzian** 4D example of an irreducible rank ≥ 3 Killing tensor | inferred from 1503.02162 + 1 search | ansatz |
| **G-4** Redundancy's log correction fixed by c, in a critical environment, is unstudied | 1 search | quantum |
| **G-5** Longitudinal, real-research data on error propagation in AI fleets is rare | 1 search | all |
| **G-6** cuspis does not cite [PRL 131, 171601 (2023)](https://arxiv.org/abs/2307.05164) | **file check** across cuspis's docs under several labels — stronger than the others | cuspis |

## Suggested division of ground — so the lists complement

| Repo | Owns (the bridge's view defers here) | Best positioned to add |
|---|---|---|
| **ansatz** | B-1, B-2, B-6, B-9, B-11 | exact/symbolic items the bridge can't see from outside |
| **tabula** | B-12 · co-owns B-7 | representation- and learning-side items |
| **deepstrain** | B-15, B-16, B-18, B-19, B-20 · data side of B-10 | observational items, real-data tests |
| **quantum** | B-8, B-13 · co-owns B-5, B-7 | validated-numerics and QM-foundations items |
| **cuspis** | B-3 · G-6 | CFT-side items |
| **bridge** | B-10 (coordination), B-14, B-17 | cross-repo items that need more than one oracle |
| *unowned* | B-4 — `hidden_symmetry` has no live session; ansatz is nearest | — |

---

## The B-list, ranked by ambition

Ranked the way the user asked: **highest impact, highest difficulty and lowest odds first**. This is a
moonshot ranking, not a work order. **Scores on sister-owned items are the bridge's outside view.**

| ID | Item | Owner | Impact | Diff. | Odds |
|---|---|---|:-:|:-:|:-:|
| ~~B-1~~ | ~~Ricci-flat Lorentzian 4D, irreducible rank ≥ 3~~ **DONE (polynomial sense), `high_rank_killing` EXP-002; independently verified (V5)** | — | — | — | — |
| B-2 | A **closed-form rotating black hole in scalar-Gauss–Bonnet** gravity | ansatz | 5 | 5 | ~5% |
| B-3 | The **mechanism** behind near-universal corner entanglement a(θ)/C_T in 3d CFTs | cuspis | 5 | 5 | ~5% |
| B-4 | **Why** the physical black hole carries a principal tensor — which spacetimes admit one | *unowned* | 5 | 5 | ~5% |
| B-5 | A **computer-assisted proof of chaos** in a black-hole spacetime ⚠ G-2 | bridge + quantum | 5 | 5 | ~10% |
| B-6 | **Any-rank** Killing tensor for the fleet's deformed-Kerr family | ansatz | 4 | 5 | ~15% |
| ~~B-7~~ | ~~Emergent geometry from entanglement~~ **already done by tabula (32/41/42/125)** | — | — | — | — |
| B-8 | **Quantum Darwinism in a critical environment** — is redundancy's log fixed by c? ⚠ G-4 | quantum | 4 | 4 | ~15% |
| B-9 | **Rigorous all-rank non-integrability of Manko–Novikov** (Morales–Ramis) ⚠ G-1 | ansatz | 4 | 4 | ~25% |
| B-10 | **"If Kerr is wrong, would we see it?"** — the second founding question | all four | 4 | 4 | ~30% |
| B-11 | **Blind rediscovery** of the 2026 exact rotating hairy black hole | ansatz | 3 | 4 | ~20% |
| B-12 | Discoverability diagnostic on **real data with unknown invariants** | tabula | 3 | 3 | ~25% |
| ~~B-13~~ | ~~Sub-45° via a lattice route~~ **infeasible as routed — clean lattice angles are 60/90/120°** | — | — | — | — |
| B-14 | **How errors propagate in an AI research fleet** — a measured case study ⚠ G-5 | bridge + all | 4 | 2 | ~60% |
| B-15 | **Pole structure** of the sGB QNM spin series | deepstrain / ansatz | 2 | 3 | ~50% |
| B-16 | Position deepstrain's **L3 null** against the 2026 orthonormal-mode GW250114 analysis | deepstrain | 3 | 2 | ~60% |
| B-17 | **G4:** certify Manko–Novikov's deep chaotic sea numerically | bridge + quantum | 2 | 3 | ~50% |
| B-18 | CNN-accelerated **subsolar PBH** rate limit on public O4 data | deepstrain | 2 | 3 | ~60% |
| ~~B-19~~ | ~~Echo non-detections → real upper limits~~ **already done — deepstrain has per-Δt upper limits (brief §1); caught by the settled index on its first pass** | — | — | — | — |
| B-20 | Systematic **table-reproduction audit** of recent GR/QNM papers | deepstrain / ansatz | 2 | 1 | ~80% |

**Not ranked — just do it (G-6):** cuspis positions its result against
[PRL 131, 171601 (2023)](https://arxiv.org/abs/2307.05164). It cites that paper's d=5 follow-up but not the
d=3 original. The bounds there are *conjectures* normalised by F₀ rather than C_T, so they don't overturn
cuspis's result — but it is the first paper a referee would raise.

---

## The items

**B-1 · Ricci-flat Lorentzian spacetime, irreducible rank ≥ 3 Killing tensor** *(new)*. Construct the
first 4D vacuum, Lorentzian metric with an irreducible higher-rank Killing tensor. Examples exist in
Lorentzian signature (not vacuum) and in vacuum (not Lorentzian); none known in both. ansatz's own positive
controls sit in the ultrahyperbolic signature. The GP engine plus Eisenhart lifts of known integrable systems
is the natural attack. May not exist — which counts only if proved.

**B-2 · Closed-form rotating sGB black hole** *(planned: Program II, P1)*. ansatz's founding hunt,
*"for which theories does an exact black hole exist?"*, aimed where it matters most. Rotating sGB is known
only numerically, and a closed form may not exist. **Blocked by P0, the simplifier wall** — wall-clock does
not buy past it. Run B-11 first.

**B-3 · Mechanism of corner-entanglement universality** *(planned: cuspis's founding question)*. Why do
very different 3d CFTs land on almost the same a(θ)/C_T? cuspis has shown the known constraints don't force
it. The 2023 conjectured scalar/Maxwell bounds are the nearest thing to an explanation in print.

**B-4 · Why the physical black hole carries a principal tensor** *(planned: hidden_symmetry, outcome E)*.
The principal tensor forces Kerr–NUT–(A)dS given the field equations, and type D plus integrability without
them. Which spacetimes admit one is actively moving (1712.08070, per `hidden_symmetry/RESULT.md`). The
realistic yield is a sharpened characterisation. No live session owns it.

**B-5 · Computer-assisted proof of chaos in a black-hole spacetime** *(new)*. Not "chaos seen
numerically" but an interval-arithmetic proof — a horseshoe, or positive topological entropy — for
Manko–Novikov or ZV geodesics. Non-integrability (B-9) and chaos are different theorems, and this one is
stronger. It turns the parked G4 (B-17) into a certificate, and fits quantum's role as the fleet's oracle for
validated numerics.

**B-6 · Any-rank Killing tensor, deformed Kerr** *(planned: ansatz's open question)*. Rank-bounded nulls
cannot reach "any rank"; ansatz has said a differential-Galois argument is needed. ZV is already closed
(settled facts). B-9 is that route on the most-cited target.

**B-7 · Emergent geometry from entanglement via a neural bottleneck** *(new)*. Feed quantum's lattice
mutual-information data to tabula's representation instrument. Does a metric emerge as the minimal code, and
does the instrument abstain when it should? The classical version uses multidimensional scaling
([Cao, Carroll & Michalakis](https://arxiv.org/abs/1606.08444)). **Needs A4 hygiene: the ground truth must be
sealed from tabula.**

**B-8 · Quantum Darwinism in a critical environment** *(planned: quantum H3)*. Does record redundancy
carry a c-fixed log correction? Related work: Darwinism on trees ([arXiv:2312.04284](https://arxiv.org/abs/2312.04284))
and a new Darwinism/error-correction no-go ([arXiv:2608.03944](https://arxiv.org/abs/2608.03944)). quantum found
the comparison *not yet well-posed* — making it so comes first.

**B-9 · Rigorous all-rank non-integrability of Manko–Novikov** *(new)*. Morales–Ramis plus Kovacic's
algorithm, as done for ZV in 2013. Manko–Novikov is the EMRI literature's canonical "bumpy black hole", and
its non-integrability rests on numerics. The hard part is finding a particular solution whose normal
variational equation Kovacic's algorithm can decide. **Best risk/reward on the list.**

**B-10 · "If Kerr is wrong, would we see it?"** *(planned: Program II, P2)*. The only item that needs all
four repos. Crowded field: EMRI resonance plateaus ([arXiv:2305.05691](https://arxiv.org/abs/2305.05691),
[arXiv:2609.03007](https://arxiv.org/abs/2609.03007)) and GWTC-4 non-Kerr constraints
([arXiv:2604.15965](https://arxiv.org/abs/2604.15965)). The fleet's distinct combination — exact metrics,
measured real-noise backgrounds, a learned probe — is its only edge.

**B-11 · Blind rediscovery of the 2026 exact rotating hairy black hole** *(new)*. Point ansatz's engine,
blind, at the theory of [arXiv:2601.21163](https://arxiv.org/abs/2601.21163). It is the positive control B-2 has
never had. If the engine can't find a known answer in the target class, B-2 is out of reach with current tools.

**B-12 · Discoverability on real data** *(planned: Program II, P4)*. A busy ML area
([Noether's Razor](https://arxiv.org/abs/2410.08087), [ML symmetry discovery](https://arxiv.org/abs/2412.14632)).
tabula's honest abstention on real chaotic data is the distinctive feature.

**B-13 · Sub-45° via an independent lattice route** *(planned check, re-scoped)*. The fresh attempt at the
check that failed on 2026-09-23 (A4 §8j). quantum's lattice machinery (DAG edge 20a) is the only route
independent of the continuum equations and of cuspis.

**B-14 · How errors propagate in an AI research fleet** *(new)*. Write up what the fleet has *measured*
about itself: 57% of the independence DAG invisible to its own auditor, seven of seven corrections in one
direction, nine measurement/mechanism splits, qualifiers lost in relay, controls that passed until
mutation-tested — all dated and git-backed. Existing work is mostly synthetic benchmarks
([arXiv:2606.03467](https://arxiv.org/abs/2606.03467), [arXiv:2607.09195](https://arxiv.org/abs/2607.09195)).
Low in a moonshot ranking because it is easy and likely; possibly **the fleet's most novel asset**.

**B-15 · sGB spin-series pole structure** *(planned)*. Round 61 measured truncation magnitude (about 2× Kerr's).
The singularity diagnosis is still open, but non-perturbative methods lower its payoff.

**B-16 · L3 null vs the orthonormal-mode GW250114 analysis** *(new)*. deepstrain measured that rotating to
orthonormal modes carries zero detection information while the implied prior moves the Bayes factor. Position
that against [arXiv:2605.03576](https://arxiv.org/abs/2605.03576). Cheap; possibly a short note.

**B-17 · G4, certify MN chaos numerically** *(planned, parked)*. Reproduction of known numerics as scoped.
Its ambitious version is B-5.

**B-18 · CNN subsolar PBH limit** *(planned: deepstrain L1)*. Crowded (settled facts). Round 62's "within 6%
of an adequate bank, at a fraction of the cost" is the only distinctive angle.

**B-19 · Echo upper limits** *(planned: deepstrain P1)*. High odds, modest novelty. deepstrain's measured
background is the asset.

**B-20 · Table-reproduction audit** *(new)*. The METRICS errata came from reproducing a published table.
Done systematically: steady yield, community service, no moonshot.

---

## What the bridge would actually do

The ranking answers the question asked; it isn't a work order. As a portfolio:

1. **One moonshot with real odds: B-9.** Widen the prior-art sweep first — an afternoon.
2. **One cheap, novel win: B-14.** The data already exists.
3. **Before any work on B-2: run B-11.** The cheapest way to learn whether the hardest item is reachable.
4. **Today: G-6.**

And the one thing no item supplies: **a human expert.** Everything in this fleet is AI checking AI. For B-3,
B-6, B-9 and B-14 especially, one outside specialist reading one result would be worth more than any amount
of further internal cross-checking.

---

*Sources mined: `TheBridge/{BACKLOG, PROGRAM_II, FALSIFICATION_LEDGER, FALSIFICATION_V2, CAPSTONE}` ·
`BlackHole/ROADMAP.md` · `quantum/{PROPOSALS, HANDOFF}.md` · `conjecture_machine/CLAUDE.md` ·
`SpaceTime/CLAUDE.md` · `corner_function/TODO.md` · `hidden_symmetry/TODO.md` · `high_rank_killing/TODO.md`.
This list is dated. It describes the literature and the fleet as of 2026-09-23 — re-check before relying
on any "nobody has done this."*
