# Moonshots — planned-but-unworked items, plus new ones, ranked by ambition

*Compiled 2026-09-23 by the bridge, at the user's request. Sources: every planning file across the
fleet (below), then a literature pass on each item. **Ranked the way the user asked: highest impact,
highest difficulty and lowest odds first** — a moonshot ranking, not a to-do order. A separate
"what I'd actually do" section is at the end.*

**Mined:** `TheBridge/{BACKLOG, PROGRAM_II, FALSIFICATION_LEDGER, FALSIFICATION_V2, CAPSTONE}` ·
`BlackHole/ROADMAP.md` · `quantum/{PROPOSALS, HANDOFF}.md` · `conjecture_machine/CLAUDE.md` ·
`SpaceTime/CLAUDE.md` · `corner_function/TODO.md` · `hidden_symmetry/TODO.md` · `high_rank_killing/TODO.md`.

**Scales.** Impact and Difficulty 1–5. **Odds** = rough chance of a clean, reportable success, stated
so it can be held against me. **D** = planned in our docs · **N** = new, proposed here.

> **Read the gap claims with care.** Several items rest on *"nobody has done this"* — a negative
> literature claim from searches the bridge phrased. That is exactly the shape quantum's rule warns
> about, and ansatz's own sweep once missed a 2013 theorem because it said *"first integral"* rather
> than *"Killing tensor."* Every item marked **⚠ gap** needs a widened prior-art sweep, in every
> neighbouring vocabulary, **before any compute is spent.**

---

## The ranked list

| # | Item | Src | Owner | Impact | Diff. | Odds |
|---|---|---|---|:-:|:-:|:-:|
| 1 | A **Ricci-flat Lorentzian 4D** spacetime with an **irreducible rank ≥ 3** Killing tensor | N | ansatz | 5 | 5 | ~3% |
| 2 | A **closed-form rotating black hole in scalar-Gauss–Bonnet** gravity | D | ansatz | 5 | 5 | ~5% |
| 3 | The **mechanism** behind near-universal corner entanglement a(θ)/C_T in 3d CFTs | D | cuspis | 5 | 5 | ~5% |
| 4 | **Why** the physical black hole carries a principal tensor — which spacetimes admit one | D | hidden_symmetry | 5 | 5 | ~5% |
| 5 | A **computer-assisted proof of chaos** in a black-hole spacetime | N | bridge + quantum | 5 | 5 | ~10% |
| 6 | **Any-rank** Killing tensor for the fleet's deformed-Kerr family | D | ansatz | 4 | 5 | ~15% |
| 7 | **Emergent geometry from entanglement**, recovered by a neural bottleneck | N | quantum + tabula | 4 | 4 | ~15% |
| 8 | **Quantum Darwinism in a critical environment** — is redundancy's log fixed by c? | D | quantum | 4 | 4 | ~15% |
| 9 | **Rigorous all-rank non-integrability of Manko–Novikov** (Morales–Ramis) | N | ansatz | 4 | 4 | ~25% |
| 10 | **"If Kerr is wrong, would we see it?"** — the second founding question | D | all four | 4 | 4 | ~30% |
| 11 | **Blind rediscovery** of the 2026 exact rotating hairy black hole | N | ansatz | 3 | 4 | ~20% |
| 12 | Discoverability diagnostic on **real data with unknown invariants** | D | tabula | 3 | 3 | ~25% |
| 13 | Sub-45° corner values checked by an **independent lattice route** | D/N | quantum | 3 | 3 | ~40% |
| 14 | **How errors propagate in an AI research fleet** — a measured case study | N | bridge + all | 4 | 2 | ~60% |
| 15 | **Pole structure** of the sGB QNM spin series | D | deepstrain / ansatz | 2 | 3 | ~50% |
| 16 | Position deepstrain's **L3 null** against the 2026 orthonormal-mode GW250114 analysis | N | deepstrain | 3 | 2 | ~60% |
| 17 | **G4:** certify Manko–Novikov's deep chaotic sea numerically | D | bridge + quantum | 2 | 3 | ~50% |
| 18 | CNN-accelerated **subsolar PBH** rate limit on public O4 data | D | deepstrain | 2 | 3 | ~60% |
| 19 | Echo non-detections → **real upper limits** | D | deepstrain | 2 | 2 | ~80% |
| 20 | Systematic **table-reproduction audit** of recent GR/QNM papers | N | deepstrain / ansatz | 2 | 1 | ~80% |

**Not ranked — just do it:** cuspis should position their result against
[Bueno, Casini, Lasso Andino & Moreno, PRL 131, 171601 (2023)](https://arxiv.org/abs/2307.05164). They cite
its d=5 follow-up but not the d=3 original. Its bounds are *conjectures* normalised by F₀ rather than
C_T, so they do not overturn cuspis's result — but it is the first paper a referee would raise.

---

## The items

### 1 · A Ricci-flat Lorentzian spacetime with an irreducible rank ≥ 3 Killing tensor — *new* ⚠ gap
**What.** Construct the first 4D **vacuum, Lorentzian-signature** metric carrying an irreducible
higher-rank Killing tensor.
**What the literature says.** Irreducible rank-3/4 tensors *do* exist in Lorentzian spacetimes, built by
Eisenhart-lifting the Goryachev–Chaplygin and Kovalevskaya tops ([Gibbons et al. 2011](https://www.sciencedirect.com/science/article/pii/S0370269311004461)).
But the **Ricci-flat** examples found so far live in **signature (2,q)**, not Lorentzian
([arXiv:1503.02162](https://arxiv.org/abs/1503.02162)). ansatz's own positive controls sit in exactly that
ultrahyperbolic signature. A Lorentzian vacuum example would be a genuine first.
**Why this rank.** Top impact in math-phys, and it may simply not exist — which is itself a result only if
proved. The GP engine plus Eisenhart lifts of known integrable systems is the natural attack.

### 2 · A closed-form rotating black hole in scalar-Gauss–Bonnet — *planned (Program II, P1)*
**What.** ansatz's founding hunt, *"for which theories does an exact black hole exist?"*, aimed at the
theory where it matters most.
**What the literature says.** Rotating sGB black holes are known **only numerically**
([arXiv:2412.09377](https://arxiv.org/abs/2412.09377)). Fully analytic rotating hairy solutions exist only in
narrow classes — disformal-Kerr in DHOST ([arXiv:2412.04135](https://arxiv.org/abs/2412.04135)), and, new in
January 2026, exact rotating solutions with **primary hair** ([arXiv:2601.21163](https://arxiv.org/abs/2601.21163)).
**Why this rank.** A closed form in sGB may not exist at all. **Blocked by P0, the simplifier wall** —
more wall-clock does not help. Item 11 is the cheap way to find out whether the engine can succeed here.

### 3 · The mechanism of corner-entanglement universality — *planned (cuspis's founding question)*
**What.** Explain why very different 3d CFTs land on almost the same a(θ)/C_T curve.
**What the literature says.** The smooth-limit ratio σ/C_T = π²/24 is proven universal
([holographic proof](https://arxiv.org/abs/1507.06283); [original conjecture](https://arxiv.org/abs/1505.04804)).
κ/C_T is **not** universal. cuspis has shown the known constraints don't force the collapse. The 2023
bounds paper (above) offers *conjectured* scalar/Maxwell brackets — the nearest thing to an explanation.
**Why this rank.** If found, it is a real CFT result. cuspis's negative is the necessary first step, and
the remaining gap is exactly where nobody has a tool.

### 4 · Why the physical black hole carries a principal tensor — *planned (hidden_symmetry, outcome E)*
**What.** The question the hidden_symmetry workspace narrowed but could not close.
**What the literature says.** The principal tensor forces Kerr–NUT–(A)dS *given* the field equations, and
forces type D and integrability without them. Which spacetimes admit one is **actively moving**
(the null-eigenvalue class of 1712.08070, recorded in `hidden_symmetry/RESULT.md`).
**Why this rank.** Conceptual, and possibly a question of taste. A sharpened characterisation is the
realistic yield.

### 5 · A computer-assisted proof of chaos in a black-hole spacetime — *new* ⚠ gap
**What.** Not "we see chaos numerically" but a **proof**: an interval-arithmetic horseshoe, or positive
topological entropy, for geodesics in Manko–Novikov or Zipoy–Voorhees.
**What the literature says.** The method is mature — rigorous proofs of chaos exist for Lorenz, Hénon, and
the restricted four-body problem ([arXiv:2212.00930](https://arxiv.org/abs/2212.00930)), usually with the CAPD
library. **One search found none for black-hole geodesics.** Manko–Novikov chaos is established only
numerically ([arXiv:1108.5057](https://arxiv.org/abs/1108.5057)).
**Why this rank.** Non-integrability (item 9) and chaos are different theorems. This one is stronger,
harder, and would be a first in GR. It turns the parked G4 (item 17) into a certificate, and fits quantum's
declared role as the fleet's oracle for validated numerics.

### 6 · Any-rank Killing tensor for the fleet's deformed-Kerr family — *planned (ansatz's open question)*
**What.** Does the quadrupole-deformed Kerr (or the O(χ²) dCS/sGB metric) admit an irreducible Killing
tensor of **any** rank?
**What the literature says.** Zipoy–Voorhees at δ=2 is **closed at every rank** by Morales–Ramis
([Maciejewski, Przybylska & Stachowiak, PRD 88, 064003](https://arxiv.org/abs/1302.4234)) — *ansatz already
records this*, and keeps its own ZV rows as instrument controls. Vollmer rules out Killing tensors only up
to a fixed rank for Tomimatsu–Sato, the C-metric and ZV ([arXiv:1602.08968](https://arxiv.org/abs/1602.08968)).
**Why this rank.** The rank-bounded nulls cannot reach "any rank"; ansatz has said a differential-Galois
argument is needed. Item 9 is that route on the most-cited target.

### 7 · Emergent geometry from entanglement, via a neural bottleneck — *new*
**What.** Feed quantum's lattice mutual-information data to tabula's representation instrument. Does a
metric emerge as the minimal code — and does the instrument abstain honestly when it shouldn't?
**What the literature says.** Recovering geometry from entanglement is established with classical
multidimensional scaling ([Cao, Carroll & Michalakis](https://arxiv.org/abs/1606.08444)). A learned probe with
tabula's legibility law and honest abstention is a different angle.
**Why this rank.** Genuinely cross-repo, which is what the bridge exists for. **Mind A4**: the two
repos must not share a target. The ground truth must be sealed from tabula.

### 8 · Quantum Darwinism in a critical environment — *planned (quantum H3)*
**What.** In a gapless environment, does record redundancy pick up a log correction set by the central
charge c, as block entropy does?
**What the literature says.** Darwinism in structured, disordered and tree environments is studied
([arXiv:2312.04284](https://arxiv.org/abs/2312.04284)), with a new Darwinism/error-correction no-go theorem
([arXiv:2608.03944](https://arxiv.org/abs/2608.03944), August 2026). The specific c-hypothesis was not found.
**Why this rank.** quantum's own H3 found the comparison *not yet well-posed* — the first job is to make it so.

### 9 · Rigorous all-rank non-integrability of Manko–Novikov — *new* ⚠ gap
**What.** Apply Morales–Ramis (with Kovacic's algorithm) to Manko–Novikov geodesics and prove there is
**no additional meromorphic first integral** — every rank at once, as was done for ZV in 2013.
**What the literature says.** Manko–Novikov is *the* canonical "bumpy black hole" of the EMRI literature,
and its non-integrability rests on **numerics** ([arXiv:1108.5057](https://arxiv.org/abs/1108.5057),
[arXiv:1408.4697](https://arxiv.org/abs/1408.4697)). **Two differently phrased searches found no rigorous
proof.**
**Why this rank.** The best risk/reward on the list. A real gap, a proven method, a well-equipped owner
(exact symbolic machinery), and the route ansatz already named. The hard part is finding a particular
solution whose normal variational equation Kovacic's algorithm can decide.

### 10 · "If Kerr is wrong, would we see it?" — *planned (Program II, P2)*
**What.** The second founding question — the only one on the list that needs all four repos.
**What the literature says.** Crowded and active: EMRI resonance "plateaus" as non-Kerr signatures
([arXiv:2305.05691](https://arxiv.org/abs/2305.05691), [arXiv:2609.03007](https://arxiv.org/abs/2609.03007)),
and GWTC-4 constraints on non-Kerr deviations ([arXiv:2604.15965](https://arxiv.org/abs/2604.15965)).
**Why this rank.** A measured detectability map is achievable. Standing out needs the fleet's
distinctive combination — exact metrics, measured real-noise backgrounds, a learned probe.

### 11 · Blind rediscovery of the 2026 exact rotating hairy black hole — *new*
**What.** Point ansatz's GP engine, blind, at the theory in which [arXiv:2601.21163](https://arxiv.org/abs/2601.21163)
just found an exact rotating solution.
**Why this rank.** It is the **positive control item 2 has never had**: a known answer in exactly the target
class. If the engine can't find it, item 2 is unreachable with current tools — worth knowing before spending
weeks there.

### 12 · Discoverability diagnostic on real data — *planned (Program II, P4, folded into P3)*
**What.** Point tabula's diagnostic at observational data where a hidden invariant's existence is
genuinely open.
**What the literature says.** A very active ML area ([Noether's Razor, NeurIPS 2024](https://arxiv.org/abs/2410.08087);
[symmetry discovery for integrable dynamics](https://arxiv.org/abs/2412.14632)). tabula's honest abstention on
real chaotic data is the distinctive feature.

### 13 · Sub-45° corner values via an independent lattice route — *planned, re-scoped here*
**What.** The fresh attempt at the check that just failed. quantum's own **lattice** machinery (DAG edge
20a) is the one route independent of the continuum CHL equations and of cuspis.
**Why this rank.** It is the only version of the check that can do more than validate quantum's code.

### 14 · How errors propagate in an AI research fleet — *new*
**What.** Write up what the fleet has *measured* about itself: 57% of the independence DAG invisible to its
own auditor; all seven corrections one-directional; nine measurement/mechanism splits; qualifiers lost in
relay; controls that passed only until mutation-tested — all dated and git-backed.
**What the literature says.** Multi-agent error propagation is studied mostly on **synthetic benchmarks**
(failure attribution — [arXiv:2606.03467](https://arxiv.org/abs/2606.03467); auditable AI scientists —
[arXiv:2607.09195](https://arxiv.org/abs/2607.09195)). A longitudinal, real-research record with numbers is rare.
**Why this rank.** Low difficulty and good odds push it down a moonshot ranking — but it may be **the
fleet's most novel asset**. Two of this week's outside reviewers pointed at this independently.

### 15 · Pole structure of the sGB spin series — *planned (outside reviewer; deepstrain roadmap)*
Round 61 measured the truncation *magnitude* (about 2× worse than Kerr). The singularity diagnosis is still
open, but the field has moved to non-perturbative methods ([METRICS](https://arxiv.org/abs/2406.11986);
[arXiv:2412.09377](https://arxiv.org/abs/2412.09377)), which lowers the payoff.

### 16 · deepstrain's L3 null vs the orthonormal-mode analysis of GW250114 — *new*
deepstrain measured that rotating to orthonormal modes carries **zero** detection information while the
prior it implies moves the Bayes factor. A May 2026 paper analyses GW250114 with orthonormal modes
([arXiv:2605.03576](https://arxiv.org/abs/2605.03576)). A direct, cheap positioning — possibly a short note.

### 17 · G4 — certify Manko–Novikov's deep chaotic sea — *planned (parked on the integrator)*
As planned, reproduction of known numerics. Its ambitious version is item 5.

### 18 · CNN-accelerated subsolar PBH limit — *planned (deepstrain L1)*
Very crowded: LVK O4a ([arXiv:2605.05444](https://arxiv.org/abs/2605.05444)), PBH constraints
([arXiv:2605.15749](https://arxiv.org/abs/2605.15749)), an independent O4ab search
([arXiv:2609.16238](https://arxiv.org/abs/2609.16238), September 2026). Round 62's "within 6% at a fraction
of the cost" is the only distinctive angle.

### 19 · Echo upper limits — *planned (deepstrain P1)*
LVK already searched O3 for echoes ([arXiv:2309.01894](https://arxiv.org/abs/2309.01894)), and an ML echo
search appeared this month ([arXiv:2609.18337](https://arxiv.org/abs/2609.18337)). deepstrain's measured
background is the asset. High odds, modest novelty.

### 20 · Table-reproduction audit of recent papers — *new*
The METRICS errata (Round 61) came from reproducing a published table. Done systematically, that is steady
community service with near-certain yield — and no moonshot.

---

## What I'd actually do

The ranking above answers the question asked. It is not a work order. As a portfolio:

1. **One moonshot with real odds: item 9** (Manko–Novikov, Morales–Ramis). A real gap, a proven method, the
   right owner. Run a widened prior-art sweep first — that costs an afternoon.
2. **One cheap, novel win: item 14** (the AI-fleet case study). The data already exists.
3. **Before any work on item 2: run item 11.** A known-answer control is the cheapest way to learn whether
   the hardest item is reachable at all.
4. **Today: the unranked quick win** — cuspis positions against the 2023 bounds paper.

And the one thing none of these supply: **a human expert.** Everything in this fleet is AI checking AI. For
items 3, 6, 9 and 14 especially, one outside specialist reading one result would be worth more than any
amount of further internal cross-checking.
