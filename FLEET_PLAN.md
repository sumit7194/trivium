# Fleet plan — one merged list, one lane per session

*Draft for discussion with the user, 2026-09-23. **Not yet sent to any session as a plan.** Built from the
six sessions' lists and `high_rank_killing`'s synthesis (see `FLEET_ANALYSIS.md`). All 86 merged items, with
scores, live in the **generated** [`fleet/REGISTER.md`](fleet/REGISTER.md). This page uses IDs only, so its
numbers can't drift from the register's.*

---

## 1. How the six lists were merged

- **Deduplicated** to 86 items using the crosswalk (e.g. B-3 = CF-2 = V-3; CF-22 = V-6; B-18 ⊂ M11).
- **The owner's own scores win** on any item that owner scored. The bridge's scores count only where nobody
  else scored the item.
- **One definition of odds:** the chance the item's *stated success criterion* is met. Where a list gave two
  odds, the one matching its success criterion is used, and the other is noted. For example, M6 (Q3): a
  clean adjudication ~70%, a real signal <1%.
- **Two views, computed by the script, never by hand:**
  - **Moonshot index M = I × D × (1 − P)** — your original question.
  - **Portfolio value EV = I × P** — what to actually run.
- **Provisional:** tabula scored chance on a 1–5 scale. It is converted as 1→5%, 2→15%, 3→30%, 4→50%,
  5→75% until tabula confirms.

**What the merge shows.** The moonshot view can't choose for us: more than a dozen items score 21–25,
because every maximal-difficulty, low-odds, high-impact item lands there. So the decision isn't a ranking.
It's **one moonshot kept alive per session**, plus a short, distinct next-up list, with every session in a
lane of its own.

---

## 2. The lanes — one role per session

| Session | Lane (its instrument) | Keeps alive (moonshot) | Next up | Supplies to others | Not its job |
|---|---|---|---|---|---|
| **ansatz** | **Exact symbolic.** Killing tensors, integrability, beyond-GR metrics. Home of the rank-3 vacuum result | **K1** — functionally independent version | verify and absorb EXP-002 (asked) · **K12** second-order Carter · **K17** certificate format | sealed metrics to tabula (K3, K13, K15) and the proof instrument (K4) · axial–polar splitting for deepstrain (Q5) · symbolic checks (Q16) | numerical screens as evidence · real data |
| **tabula** | **Numerical screens + representation learning.** Emit-or-certify, legibility law | **K14** (blind-recover P–K, then rank-4 outside it) **or L1** (Walrus) — its choice, within the lane | **K3** blind screen of the rank-3 object · **L16** synthesis write-up · **L12** public benchmark | the N rung for K5, K8, K12, K13 · the planted-nuisance check on anyone's "conserved quantity" | claiming constructions or proofs · corner functions · LIGO data |
| **deepstrain** | **Real data.** LIGO/Virgo strain, ringdown, subsolar, echoes | **Q8** independent test of the GW250114 "direct wave" (Q1 is blocked: no theory template owner) | **Q6** re-score LVK O4a triggers (its declared next) · **Q3** the 5.4σ adjudication (one session only) · **Q15** deep-FAR methods note | injections, backgrounds, METRICS series, arbitrary-precision Kerr QNMs | symbolic GR · LISA/EMRI |
| **quantum** (vestigium) | **Validated numerics + analytic structure.** Precision corner values, Painlevé, certificates | **C14** the Painlevé system behind the corner ODEs | **C20** continuum a(2π/3), a(π/3) (its declared next) · **C16** κ to 30 digits (if unblocked) · **K4** proof instrument (*if you assign it*) | precision scalar coefficients to cuspis (labelled non-independent) · validated-numerics tooling for K19 | sub-45° values until your amendment decision · Rényi n = 2 · anything built from cuspis's code |
| **cuspis** | **Corner theory.** Bounds, positivity, the mechanism | **C1** an upper bound on κ/C_T | **C17** the new cusp inequalities (sole owner) · position 2307.05164 in `RESULT.md` (R-5) · **C13** analytic a₀ | curves and settled facts (its §2) to anyone | the sub-45° second instrument — it must be independent of cuspis's solver |
| **bridge** | **Coordination, independence and statistics audit.** Register, reconciliation, adjudication | *(none — it audits the others' moonshots)* | **F2** fleet settled-results index · **F1** error-propagation case study · **Q12** GWTC-4 finite-SNR bias (*proposed*) | merges, audits, independent re-derivations (as V5), literature relays tagged | adjudicating any claim it produced itself |

**Why these lanes don't collide.** Each is defined by a **kind of instrument**, not a topic. Several lanes
meet on one object (the rank-3 result, deformed Kerr, the corner band), and that is deliberate: the same
question through different instruments is what turns agreement into evidence (L17). What the lanes prevent
is the same instrument used twice on the same question.

---

## 3. Items that need more than one session — how they're split

| Item | Split | Rule |
|---|---|---|
| **K8** Is dCS integrable? | exact (ansatz) · proof (K4 owner) · numerical (tabula/quantum, *different targets*) · bridge adjudicates | each rung ships a manifest; the bridge compares blind |
| **K5 → K19** Manko–Novikov | proof of non-integrability (K4 owner) → computer-assisted chaos proof (quantum + bridge), with K20 locating the chaotic sea first | same target, every rung of the claim ladder |
| **C2a / C2b** corner mechanism | cuspis: tripartite information · quantum: bound + remainder | each pre-registers one prediction the other can't see |
| **K3** blind screen of the rank-3 object | ansatz supplies (after absorbing it), sealed · tabula scores | metric only, no labels, no motivation |
| **Q5** isospectrality | ansatz supplies the theory input · deepstrain fits | theory before data |
| **Q3** 5.4σ adjudication | **deepstrain only** | two refutations by different mechanisms must not collide |
| **C17** cusp inequalities | **cuspis only**; quantum contributes coefficients labelled non-independent | duplicate CF-22 = V-6 resolved |

---

## 4. Unowned or parked — and what would change that

| Item | Why it's parked | What would unpark it |
|---|---|---|
| **K4** the proof instrument | no session has differential Galois / Kovacic tooling | **your decision** — it unlocks K5, K7, K10, K19 |
| **C12** a second sub-45° instrument | the lattice route is infeasible (R-3); V8 awaits your amendment decision | an owner for the tensor-network wedge, or CF-13's analytic route |
| **Q1** quantum-ringdown tail | no session owns the theory template | a session willing to turn arXiv:2609.14160 into a LIGO-band template |
| **K21** closed-form rotating sGB | the bridge's own rule: run K22 (blind rediscovery) first | K22 passes |
| **K23** why the principal tensor | `hidden_symmetry` closed at outcome E; no owner | — |
| **C3, C4, C6, C7** interacting κ, fuzzy sphere, θ^{2η}, twist-line bootstrap | no fleet instrument | a new instrument or an outside collaborator, not a session |
| **L8, L13** LLM light cone, Hashimoto bulk | tabula lists them as open seats | Phronesis, if it wants them — it's outside the six repos |

---

## 5. Decisions only you can make

1. **Approve the lanes** in §2, or move items between them.
2. **Who owns K4, the proof instrument.** My recommendation: **quantum**. It has spare capacity (its corner
   work is gated on your amendment), and its Painlevé item (C14) uses closely related singularity-analysis
   tools. It also keeps the proof rung in a different session from ansatz's exact rung; that isn't required
   for independence, but it helps. ansatz would supply the metrics, sealed. The alternative is ansatz itself,
   which asked someone else to lead proof work.
3. **The statistics-audit lane (Q12, Q9):** the bridge (my proposal — tabula's list is already 19 items) or tabula.
4. **quantum's sub-45° amendment** (V8 → C12). It's been waiting since this morning.
5. **`high_rank_killing`:** fold into ansatz and archive. Already in motion — ansatz is verifying first.
6. **F3: one outside specialist reads EXP-002.** The highest-value single action in the register, and the only
   one no session can take.
7. **Each session's kept-alive moonshot** (§2) — proposals; a session may swap within its own lane.

---

## 6. Clarifications being asked (list only — no work requested)

- **tabula:** confirm or correct the provisional 1–5 → probability mapping.
- **ansatz:** score K5 (Manko–Novikov) and K22 (blind rediscovery), which were proposed for it but aren't on
  its list (R-7).
- **deepstrain:** score Q17 (B-16), which isn't on its list (R-8); confirm "clean adjudication" as M6's success
  criterion; say whether it wants Q19 (S2/Hulse–Taylor), which tabula offered.
- **quantum:** is C16 (κ via Painlevé V) blocked by the sub-45° registration or not? Its list is ambiguous.
