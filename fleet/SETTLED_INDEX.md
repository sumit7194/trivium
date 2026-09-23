# Fleet settled-results index — a catalogue of what's already done

*Maintained by the bridge. Started 2026-09-23. **Status only — never the result.***

## Why this exists

On 2026-09-23 the fleet's planning lists named at least four items as open or new that were **already done
inside the fleet**: the bridge's B-1 (the rank-3 vacuum tensor), B-7 (geometry from entanglement) and B-19
(echo upper limits), and ansatz's #1. Every list had been built from TODO files; none checked what was *done*.
This catalogue is the check.

## How to use it

1. **Before listing an item as open or new, look its question up here.** If it's SETTLED, cite the pointer
   instead of re-proposing it. If it's PARTIAL, state what's left.
2. **The index gives status and a pointer, never the answer.** It does not say *what* was found. That keeps it
   compatible with ansatz's rule that plans share questions, not conclusions: an agreement is only evidence
   if the checker didn't know the answer.
3. **If you're running a blind or sealed check, don't open the pointer.** Knowing that a question is settled
   is fine; reading how it was settled is not.
4. **Status changes go through the bridge**, with a date. Every entry here is dated, because a status in prose
   doesn't update itself (L18).

**Status words:** **SETTLED** (done, with the scope stated at the pointer) · **PARTIAL** (what's missing is
named) · **IN PROGRESS** (who is on it) · **OPEN** · **PAUSED** (waiting on a decision) · **CLOSED–NEGATIVE**
(done, didn't work) · **WITHDRAWN** (claimed, then retracted).

---

## Black holes and integrability

| Question | Status | Where | As of |
|---|---|---|---|
| Lorentzian vacuum spacetime with a polynomially irreducible rank-3 Killing tensor | **SETTLED** — the spacetime is prior art (Filyukov 2017); the tensor is new | ansatz RESULTS §147 · bridge V5, V6 | 09-23 |
| …the same, with a *functionally independent* tensor | **OPEN** | fleet item H-2 / ansatz #1 | 09-23 |
| Zipoy–Voorhees δ=2: any additional integral, any rank? | **SETTLED** (literature, 2013) | arXiv:1302.4234 · ansatz §134 | 09-23 |
| Zipoy–Voorhees ranks 1–6, exact | **SETTLED** (now a control, not a result) | ansatz §124, §126 | 09-23 |
| Exact test recovers Kerr's Carter constant | **SETTLED** (control) | ansatz §127 | 09-23 |
| sGB metric at O(χ²), derived | **SETTLED** | ansatz §128–§129 | 09-23 |
| Does sGB keep Carter at rank 2? | **SETTLED** | ansatz §130 | 09-23 |
| sGB irreducible Killing tensors at ranks 3, 4, 6 | **SETTLED** within the stated ansatz and denominator | ansatz §131–§133, §137 | 09-23 |
| sGB rank 8 | **IN PROGRESS** — ansatz queue (the L⁸ pair to follow) | ansatz weekend queue | 09-23 |
| Which deformations of Kerr keep Carter | **SETTLED** (scope at the pointer) | ansatz §139 | 09-23 |
| Does dCS keep a rational Carter constant? | **SETTLED** | ansatz §145 | 09-23 |
| Is dCS integrable overall (any degree, non-polynomial)? | **OPEN** — the literature contradicts itself | fleet item K8 | 09-23 |
| The pole-order ladder | **PARTIAL** — parity grading found; ℓ-dependence open | ansatz §141–§146 | 09-23 |
| Manko–Novikov: all-rank non-integrability, proved | **OPEN** — none found in print (two searches) | fleet item K5 | 09-23 |
| Manko–Novikov: chaos seen numerically | **SETTLED** (literature) | arXiv:1108.5057 | 09-23 |
| The proof tool (Morales–Ramis / Kovacic) | **IN PROGRESS** — quantum, Stage 1 (controls) | fleet plan step 1 | 09-23 |
| Cartan–Karlhede to order 2 | **SETTLED** | ansatz §122 | 09-23 |
| Emit-legibility theorem | **SETTLED** | ansatz §123 | 09-23 |
| "legible ⟺ KY-integrable" | **WITHDRAWN** — falsified; replaced by representability in the probe's basis | bridge G2, CAPSTONE §3 #2 | 09-23 |

## Real data (LIGO)

| Question | Status | Where | As of |
|---|---|---|---|
| CNN vs an *adequate* matched-filter bank, subsolar | **SETTLED** | deepstrain `aa7e411` · bridge Round 62 | 09-23 |
| H1×L1 coincidence vs a single detector | **SETTLED** | deepstrain brief §2 | 09-23 |
| Deep-FAR estimator bias (the jackknife understatement) | **SETTLED** | deepstrain brief §2 | 09-23 |
| Kerr 220 spin-series truncation, and its radius of convergence | **SETTLED** | deepstrain brief §2 | 09-23 |
| sGB background and QNM-correction truncation | **SETTLED** — polar modes only | deepstrain `cadfed9`, `7fd4c55` · bridge Round 61 | 09-23 |
| Which events make the no-hair δ informative | **SETTLED** | deepstrain brief §2 | 09-23 |
| σ(δ) saturation vs SNR | **SETTLED** — positioned against arXiv:2509.17315 | deepstrain RELATED_WORK | 09-23 |
| Three METRICS errata | **SETTLED** on arXiv v2; journal version unchecked | deepstrain `4a7687e` · bridge Round 61 | 09-23 |
| **Echo non-detections → per-Δt upper limits** | **SETTLED** | deepstrain brief §1, `echoes/notes/lab_notebook.md` | 09-23 |
| Orthonormal modes: detection information | **CLOSED–NEGATIVE** (L3) | deepstrain ROADMAP | 09-23 |
| Three-tone spectroscopy | **CLOSED–NEGATIVE**, information-limited; reopens at ρ_rd ≈ 38 | deepstrain ROADMAP L5 | 09-23 |
| Larger SSL pool | **CLOSED–NEGATIVE**, saturates | deepstrain ROADMAP L6 | 09-23 |
| Coherent network echo search | **WITHDRAWN** | deepstrain ROADMAP L4 | 09-23 |
| Re-score LVK's O4a subsolar triggers | **IN PROGRESS** — deepstrain | fleet plan step 1 | 09-23 |

## Corner entanglement

> **⚠ SEALED TOWARD QUANTUM (while its sub-45° check is registered or could be reopened).** Rows marked 🔒
> concern the small-angle region. **quantum must not open their pointers.** Their wording here is pure status
> by design; it was redacted on 2026-09-24 after earlier wording leaked content.

| Question | Status | Where | As of |
|---|---|---|---|
| Do the known constraints bound κ/C_T from above? | **SETTLED** (re-derived by quantum) | cuspis SHARED_BACKLOG S1 | 09-23 |
| What the ~1% collapse actually is | **SETTLED** | cuspis S2 | 09-23 |
| Can ⟨TT⟩ and ⟨TTT⟩ data order the band? | **SETTLED** | cuspis S3 | 09-23 |
| A lower bound on κ/C_T at n = 1 | **PARTIAL** — rests on an assumed n → 1 continuation | cuspis S4 | 09-23 |
| Can the rectangle bootstrap bound κ from above? | **SETTLED** | cuspis S5 | 09-23 |
| What a₀ ≠ 0 requires | **SETTLED** (the exponent is prior art) | cuspis S6 | 09-23 |
| 🔒 a₀ by theory | **SETTLED** as measured | cuspis S7 | 09-24 |
| 🔒 The free scalar's a₀ | **PARTIAL** (scope at the pointer) | cuspis S8 | 09-24 |
| The trial function's constant | **SETTLED** | cuspis S9 | 09-23 |
| 🔒 The scalar residual below 45° | **SETTLED** as measured (scope at the pointer) | cuspis S10 | 09-24 |
| Does fixing σ and κ leave little freedom? | **SETTLED** | cuspis S11 | 09-23 |
| The Dirac / Einstein thermal-coefficient coincidence | **SETTLED** (chance) | cuspis S12 | 09-23 |
| Free-Dirac and scalar corner functions, 20°–170° | **SETTLED** | cuspis S13 | 09-23 |
| Precision Taylor coefficients c₂ … c₁₆ and a(3π/4) | **SETTLED** as measured (c₈ vs CHL09 unexplained) | quantum COORDINATION §1 | 09-23 |
| An independent check of the values below 45° | **PAUSED** — control 1 failed; the amendment is the user's decision | quantum PREREG · bridge A4 §8j | 09-23 |
| The new cusp inequalities (2609.04302 eq. 37, conformal concavity) on existing curves | **SETTLED** — tested, including a new-theory case | cuspis EXP-022, `2554c92` | 09-24 |
| Is eq. (37) a route to an absolute upper bound on κ? | **CLOSED–NEGATIVE** — invariant under Casimir dressing | cuspis EXP-022 | 09-24 |
| 🔒 Consequences of the new cusp theorems for a₀ | **SETTLED** (scope at the pointer) | cuspis EXP-022 · SHARED_BACKLOG S7a/S7b | 09-24 |
| 🔒 Helmes et al. eq. (22) as a small-angle referee | **SETTLED** (scope at the pointer) | cuspis EXP-022 · SHARED_BACKLOG trap 9 | 09-24 |
| Positioning against Bueno–Casini–Lasso Andino–Moreno 2023 | **SETTLED** — in RESULT.md §0 and §8 | cuspis `2554c92` | 09-24 |
| Cuboid bootstrap under Casimir dressing | **IN PROGRESS** — cuspis (CF-24) | cuspis's bounds chain | 09-24 |

## Representation learning (tabula)

| Question | Status | Where | As of |
|---|---|---|---|
| 2D Chern · Ollivier–Ricci · orthogonal Wong · **geometry from entanglement** · Dirac/spinor · bumped Kerr in BL · Turing-pattern topology | **SETTLED** — tabula lists them as done or published | tabula next_directions §2 (scripts 120, 124, 106/135, 32/41/42/125, 98/114, 168/174; arXiv:2409.20491) | 09-23 |
| "Two instruments agree to 2.24×" | **WITHDRAWN** | tabula next_directions §3.1 | 09-23 |
| §157 / §158 as independent replications | **WITHDRAWN as replications** — non-blind; their physics gates stand | tabula §3.7 · bridge A4 | 09-23 |

## The fleet itself

| Question | Status | Where | As of |
|---|---|---|---|
| "The repos are kept ignorant of each other" | **WITHDRAWN** — replaced by *independent data, entangled methodology* | bridge A4 | 09-23 |
| G7, "every wall is instrument-relative" | **WITHDRAWN** — killed | bridge A2 | 09-23 |
| The bridge's cross-repo code-edge census | **SETTLED** — built, mutation-tested | `ops/cross_repo_census.py` · A4 §8c–8d | 09-23 |
| The six plan lists merged into one plan | **IN PROGRESS** — draft with the user | `FLEET_PLAN.md` | 09-23 |

---

*Seeded from each repo's own published records: ansatz `RESULTS.md` section titles · deepstrain
`MOONSHOT_BRIEF_DeepStrain.md` and `ROADMAP.md` · cuspis `SHARED_BACKLOG.md` §2 · quantum
`COORDINATION_corner_research_menu.md` §1 · tabula `writeups/tabula_next_directions.md` · the bridge's
falsification ledger. **A repo's own record wins over this index.** If they disagree, this index is the stale one.*
