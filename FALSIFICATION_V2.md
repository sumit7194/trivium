# Falsification Ledger v2 — the informed round

*Drafted 2026-07-24, after the v1 campaign closed (11 resolved bridge-side + round-8 sister round: 8 KILLED,
4 SURVIVED, 1 parked; see `FALSIFICATION_LEDGER.md` for the corpses). v2 is not more postulates for their own
sake — every entry below is **bred from a v1 corpse**: a kill that exposed a sharper question, a survival
that located an obstruction, or a bug that taught a discipline. Same eligibility filter, same three-valued
verdicts, same standing rules (pre-register first; prior-art sweep before excitement; UNDECIDED is an
answer). Nothing here has been run.*

---

## What round 1 taught (the lessons that shaped v2)

| # | lesson | where it came from |
|---|---|---|
| L1 | **Proxies masquerade as laws when the catalog is homogeneous.** KY⇔legible held 8/8 only because Collinson/Dietz–Rüdiger force KT⇒KY on type-D vacua — the catalog's restriction manufactured the coincidence. *Weapon: designed adversaries and deliberately heterogeneous catalogs.* | G2 |
| L2 | **Too-clean is a bug smell.** "Exact, resolution-independent isospectrality" was a disconnected-grid triviality — the resolution-independence itself was the tell. *Discipline: any result cleaner than the instrument's order predicts gets an adversarial audit before celebration.* | K2 (tabula's catch) |
| L3 | **Design kills to output curves, not booleans.** K1's deviation *measured* ΔS; K3 produced Σ(ℓ); M4 produced the α^p law (p=0.998); M2 separated exponent (universal) from coefficient (scheme). A kill that returns a mechanism is worth ten that return "no." | K1, K3, M4, M2 |
| L4 | **Survivals localize.** The inside-wedge squeeze *surviving* K1's identity is what located the true obstruction (ΔS≠0 via non-factorization across the cut). Pre-register survivals as informative, not as failures to kill. | K1 |
| L5 | **Independence pays twice per round.** tabula caught our K2 grid bug; our independent derivation caught tabula's indexing bug. *Neither repo could have caught its own.* | round 8 |
| L6 | **The outward turn works, event-driven.** Leg W (audit found real published errors) and leg Z (verified the Jacobian counterexample same-week) — but only when a target presents itself; never manufactured. | legs W, Z |
| L7 | **Walls keep being instrument-relative.** G7 fed five times in one campaign (float64→mpmath, ℓ-tail, dsolve→hand, simplify→substitution, CK order-1→2). G7 stays open and standing. | G7 |

---

## Tier R — refinements bred from kills (the heart of v2)

| ID | Postulate (precise) | Attack | Born from / payout |
|----|---|---|---|
| **R1** | **"Candidate B (transcendental invariant) becomes LEGIBLE when the probe basis is augmented with log/rational terms."** The corrected G2 claim ("legible ⟺ polynomial-representable *in the probe's basis*") is instrument-relative; this tests whether the boundary moves with the basis as the claim predicts. | tabula: rerun B with an augmented basis (already drafted as the round-9 ask in SISTER_REQUESTS). Either verdict sharpens: legible ⇒ "representable-in-basis" confirmed as the law; still illegible ⇒ the obstruction is deeper than basis span. | G2. Turns the corrected claim's key word ("representable") into a measured, movable boundary. |
| **R2** | **"emit succeeds ⟺ the invariant lies in the span of the probe basis"** — the corrected G2 claim promoted from empirical boundary to **provable theorem about the emit-or-certify engine** (its emit step is a linear certificate; existence-in-span should be exactly decidable). | ansatz + bridge: formalize the engine's emit criterion; prove the biconditional over the engine's actual algorithm, or extract the counterexample condition (noise floor? conditioning?). | G2. **The single most valuable v2 item**: a small real theorem about what a linear-probe learner can read. Prior-art sweep mandatory before any claim (SINDy/regression-representability literature exists). |
| **R3** | **"The patchwise Clausius violation obeys a weak-drive scaling law: Σ/δQ = c·r² + O(r⁴), with c independent of patch size for ℓ ≫ ξ."** (v1 measured Σ(ℓ) at fixed drive and saw Σ/δQ → 0 as r → 0; v2 nails the *law*.) | bridge: r-sweep × ℓ-sweep on the existing K3 build (machinery unchanged). Fit the exponent; find where the window breaks. | K3. Payout: a quantitative "near-equilibrium window" — the closest a lattice can get to *quantifying* (not proving) the localization postulate's domain of validity. Completes the leg X → K3 arc. |
| **R4** | **"There exist non-factorizing excitations with ΔS = 0"** — i.e. K1's obstruction is exactly ΔS≠0, and "non-factorization" (the language we used) is sufficient-but-not-necessary. | bridge: Gaussian search for a cross-cut operation with ΔS = 0 (fine-tuned two-mode squeeze pairs); if found, the identity holds despite non-factorization. | K1. Cheap; fixes the *wording* of a finding we already banked — precision hygiene. |
| **R5** | **"The drum-discrimination signal is concentrated in low modes: K5's accuracy vs number-of-modes curve saturates by mode ~10."** | tabula (or bridge probe): retrain K5's discriminator on truncated modal data; measure accuracy vs modes/sensors. | K5. Payout: *where* geometry hides in a recording — the information-localization curve, feeding the walls theme. |
| **R6** | **"The subleading (log) coefficient of the 3D area law is regulator-INDEPENDENT"** — the universal companion to M2's kill (κ moved 51%; the exponent held; the log term, tied to the conformal anomaly, should also hold). | bridge: extract the log coefficient across M2's three regulators from the existing infrastructure. Honest odds: subleading extraction is numerically delicate; UNDECIDED(precision) is a live outcome. | M2. Completes the "what is universal in the area law" story: exponent yes, κ no, anomaly-log — measured. |

## Tier S — the spectral-geometry / KK arc, continued

| ID | Postulate | Attack | Notes |
|----|---|---|---|
| **S1** | **"Flat 4-tori are NOT spectrally determined — and therefore a KK compactification's mass tower cannot determine the hidden T⁴, even in principle."** Verify a **Schiemann pair** (4D isospectral non-isometric lattices): theta series agree term-by-term to high order (exact integer arithmetic); non-isometry proven exactly (lattice invariants). | bridge: theta-series enumeration + exact lattice arithmetic. V3 already noted the 4D counterexamples exist; this *builds* one and states the KK punchline. | The physics headline of the drums arc, now in the actual KK setting (tori, no boundary). Dimension boundary made complete: audible ≤ 3 (Schiemann's theorem), deaf ≥ 4 (his pairs). Feeds route 5: only eigenfunction-level data (K5's channel) could tell them apart. |
| **S2** | **"The rest-buzz instrument reads ANY hidden manifold whose Laplacian is known: the S³ tower is n(n+2)."** (Rung 1 of `KK_EXTENSION_NOTES.md`, stated as a falsifiable gate.) | bridge FD on S³ (or spectral method); gate against the exact Casimir spectrum; five-route extendable later (ansatz proof anchor exists in the audited paper's Eq. 26–27 lineage — cite, don't trust). | The curved-space generalization of legs S/U — the crown jewel's next rung as a v2 entry. |
| **S3** | **"A KK reduction on a GWW-drum cross-section yields two field theories with identical mass towers but distinguishable local physics."** (K5's lesson lifted from analogy to an actual compactification: cylinder ℝ × drum.) | bridge: FD tower on both drum cross-sections (fixed grid, connectivity-asserted per L2) + a local-correlator observable that separates them. | Unifies the whole arc — K2 (same tower) + K5 (locals leak) — in field-theory language. Medium effort. |

## Tier A — audits (new tier, born from L2)

| ID | Item | Attack |
|----|---|---|
| **A1** | **The too-clean audit:** "every 'exact' numerical agreement in the family's published results (agreement ≫ the method's order predicts) is either a proven combinatorial identity or a bug." Sweep all results JSONs for exactness anomalies; each one found gets classified. | bridge: grep-and-classify across all repos' results; K2's corpse is the template (resolution-independence = the tell). Cheap, self-contained, and the kind of thing that catches the *next* K2 before a sister has to. |

## Tier Z — outward (standing, event-driven; never manufactured)

- **Z-criteria** (from legs W/Z): primary source obtainable; a checkable layer within exact reach; verification is self-validating. Targets are *events*, not a queue to fill.
- **Z2 (candidate):** *digest the digestion* — verify Tao's structural mechanism behind the Jacobian counterexample (the Sym¹×Sym² multiplication-map construction) symbolically, not just the endpoint map. Bounded, educational, genuine depth beyond leg Z's endpoint check.
- **Z3 (watch):** Pinčák erratum/reply — if the authors respond, the follow-up is theirs to shape; our part is done.

## Moonshots v2

| ID | Item | Honest odds |
|----|---|---|
| M1 (carried) | 5D charged rotating equal-spin hunt → obstruction theorem | unchanged: solution unlikely, obstruction decent |
| **M5** | **mini-CLASSI**: CK-certificate database over the full family catalog — the "surface CK more" instrument, publishable-genre (JOSS), pending the quantum session's GitHub/PyPI prior-art sweep (still owed) and the Kerr/Taub–NUT simplifier walls | instrument-building: low risk, real (small) audience |
| **M6** | R2 carried to a full write-up if it proves: "what a linear-probe emit engine can and cannot read" — theorem + the G2/R1 measurements as its experimental section | the family's first candidate for a genuinely publishable *methods* result; prior-art sweep is the gate |

## Recommended firing order (when the Mac is next free)

1. **R2** — the theorem attempt (highest value; mostly symbolic; bridge+ansatz)
2. **R1** — file the drafted tabula ask (sister-side; zero bridge compute)
3. **S1** — Schiemann pair (bridge-side, self-contained, exact arithmetic, beautiful)
4. **A1** — too-clean audit (cheap; institutionalizes L2)
5. **R3** — the Clausius scaling law (reuses K3 machinery end-to-end)
6. **S2 → S3** — the curved-space rung, then the drum compactification

Sister-dependent carryovers from v1, unchanged: G6's three vacuum-vs-vacuum pairs · G1 · G5 · K6 · G4
(parked on the symplectic integrator) · G8 (deepstrain standing challenge) · G7 (standing meta-claim, fed
five times, still unfalsified).

## What v2 is not

Same as v1, verbatim: not a route to new laws of nature; not a claim that survivors are true; not exempt
from the house rules. The realistic ceiling moved up slightly in one place only — R2/M6, where round 1's
kill left an actual provable-looking statement on the table. That is what an informed round means.
