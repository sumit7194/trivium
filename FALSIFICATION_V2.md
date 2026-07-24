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
| **R1** ✓ DONE 2026-07-24 (tabula) — **KILLED, axis named** · ~~"B legible with augmented basis"~~ B stays ILLEGIBLE across polynomial/rational/**log-coordinate**/exp(quadratic-momentum); log-coord *helps* (2.6e-5→1.3e-5) but never emits. Sharpening: B's transcendence is in the **momenta**, so log-*coordinate* is the wrong axis ⇒ **legible ⟺ representable in the probe's MOMENTUM basis**, not coordinate basis. Un-blind (name B's momentum family) is the bridge's to run. [tabula 162] The corrected G2 claim ("legible ⟺ polynomial-representable *in the probe's basis*") is instrument-relative; this tests whether the boundary moves with the basis as the claim predicts. | tabula: rerun B with an augmented basis (already drafted as the round-9 ask in SISTER_REQUESTS). Either verdict sharpens: legible ⇒ "representable-in-basis" confirmed as the law; still illegible ⇒ the obstruction is deeper than basis span. | G2. Turns the corrected claim's key word ("representable") into a measured, movable boundary. |
| **R2** ✓ DONE 2026-07-24 — **CROSS-GATE CLOSED + new obstruction O4** · ansatz proved it (§123, 6/6); bridge **independently reimplemented** the emit criterion (own code, no import) and reproduced all four teeth (⟸ no false negatives; the pendulum illegible→legible flip on adding a cos atom; G1/G2 catch O1/O2; scales match §123). **Found O4** — a deg-6 poly FALSELY emits (2.7e-7<τ) approximating the transcendental invariant below the floor; not in §123's map; caught only out-of-sample; relayed to ansatz. Two of my own bugs caught by A1's too-clean instinct + R2d's scale check. [falsification/R2_emit_theorem](falsification/R2_emit_theorem) · **"emit succeeds ⟺ the invariant lies in the span of the probe basis"** — the corrected G2 claim promoted from empirical boundary to **provable theorem about the emit-or-certify engine** (its emit step is a linear certificate; existence-in-span should be exactly decidable). | ansatz + bridge: formalize the engine's emit criterion; prove the biconditional over the engine's actual algorithm, or extract the counterexample condition (noise floor? conditioning?). | G2. **The single most valuable v2 item**: a small real theorem about what a linear-probe learner can read. Prior-art sweep mandatory before any claim (SINDy/regression-representability literature exists). |
| **R3** ✓ DONE 2026-07-24 — **KILLED (p=2), law measured** | ~~"Σ/δQ = c·r² …"~~ Measured p(Σ/δQ)=0.89→1 (**linear, not r²**); decomposition Σ=S_rel~r² (2.02), δQ=Δ⟨K⟩~r (1.12) ⇒ the patchwise first law holds EXACTLY to first order, the violation is the second-order residual; coefficient patch-independent 0.76%. [falsification/R3_clausius_scaling](falsification/R3_clausius_scaling) (v1 measured Σ(ℓ) at fixed drive and saw Σ/δQ → 0 as r → 0; v2 nails the *law*.) | bridge: r-sweep × ℓ-sweep on the existing K3 build (machinery unchanged). Fit the exponent; find where the window breaks. | K3. Payout: a quantitative "near-equilibrium window" — the closest a lattice can get to *quantifying* (not proving) the localization postulate's domain of validity. Completes the leg X → K3 arc. |
| **R4** ✓ DONE 2026-07-24 — **postulate TRUE** · root-found a non-factorizing entangling op BS(π/6)·TMS(0.295) with **ΔS=0** (BS disentangles, TMS entangles, they cancel) ⇒ the Longo obstruction is EXACTLY ΔS≠0; "non-factorization" is sufficient-but-not-necessary. K1 wording amended (chain verdict unaffected). Instrument note: a 60×60 grid falsely reported NOT-FOUND (codim-1 zero set) — root-finding is the right tool (feeds G7). [falsification/R4_deltaS_obstruction](falsification/R4_deltaS_obstruction) · **"There exist non-factorizing excitations with ΔS = 0"** — i.e. K1's obstruction is exactly ΔS≠0, and "non-factorization" (the language we used) is sufficient-but-not-necessary. | bridge: Gaussian search for a cross-cut operation with ΔS = 0 (fine-tuned two-mode squeeze pairs); if found, the identity holds despite non-factorization. | K1. Cheap; fixes the *wording* of a finding we already banked — precision hygiene. |
| **R5** ✓ DONE 2026-07-24 (tabula) — **KILLED-as-stated, half confirmed** · low-mode concentration CONFIRMED (first ~16 modes carry the bulk) but 95%-saturation at **m\*≈24** (JSON; report said ~40) ≫ predicted ~10. Sensors: signal is **spatially DISTRIBUTED** — 0.48 at 4 nodes → 0.73 at 128. **Low-rank-in-frequency, high-rank-in-space**: the K5 wall is spectrally cheap, spatially expensive. [tabula 163] | tabula (or bridge probe): retrain K5's discriminator on truncated modal data; measure accuracy vs modes/sensors. | K5. Payout: *where* geometry hides in a recording — the information-localization curve, feeding the walls theme. |
| **R6** ✓ DONE 2026-07-24 — **KILLED (b regulator-dependent), with the mechanism** · fitted log coefficient b = **2.32 / 3.72 / 0.52** across bare/improved/higher-deriv (across-spread 1.31 ≫ within-jackknife 0.29) — b moves with the scheme *exactly like κ*. The kill is the **expected physics**: in **odd** spatial dimension (3D) there is **no conformal anomaly ⇒ no universal log term** (the protected subleading quantity is a *constant*, the F-term, not a log), so `b·log n` fits scheme-dependent lattice residue. Completes M2's ledger: of {exponent, κ, log}, **only the exponent is universal — and in 3D the log was never going to be.** Pre-registered odds favored UNDECIDED(precision); data were sharper and returned a clean mechanism'd KILL. [falsification/R6_arealaw_log](falsification/R6_arealaw_log) · ~~"The subleading (log) coefficient of the 3D area law is regulator-INDEPENDENT"~~ | bridge: extract the log coefficient across M2's three regulators from the existing infrastructure. | M2. Completes the "what is universal in the area law" story: exponent yes, κ no, log — **no (and structurally so: odd-d has no universal log; the universal subleading content is the constant c).** |

## Tier S — the spectral-geometry / KK arc, continued

| ID | Postulate | Attack | Notes |
|----|---|---|---|
| **S1** | **"Flat 4-tori are NOT spectrally determined — and therefore a KK compactification's mass tower cannot determine the hidden T⁴, even in principle."** Verify a **Schiemann pair** (4D isospectral non-isometric lattices): theta series agree term-by-term to high order (exact integer arithmetic); non-isometry proven exactly (lattice invariants). | bridge: theta-series enumeration + exact lattice arithmetic. V3 already noted the 4D counterexamples exist; this *builds* one and states the KK punchline. | The physics headline of the drums arc, now in the actual KK setting (tori, no boundary). Dimension boundary made complete: audible ≤ 3 (Schiemann's theorem), deaf ≥ 4 (his pairs). Feeds route 5: only eigenfunction-level data (K5's channel) could tell them apart. |
| **S2** ✓ DONE 2026-07-24 — **SURVIVES** · rest-buzz on a **curved** hidden S³ reads `√(n(n+2))` to **0.42% worst** (0.02% for ℓ≥1), **no missing levels**; ℓ-independence for ℓ≤n + the **n≥ℓ cutoff** ⇒ degeneracy **(n+1)² measured, not asserted**. Control S2c: the S³ level **n=3 (m²=15) is producible by NO unit-radius flat T³** — 15 is not a sum of three squares (exhaustive search; Legendre verified, not invoked), and the degeneracies diverge (S³ perfect squares 4,9,16,25,36,49 vs erratic r₃ 8,12,0,24,48,8). **Two instrument catches, both mine:** single-probe chi-square nulls silently dropped levels (fixed: 8-probe averaged power spectrum + MISSING reporting), and `ü=−(H−1)u` gave the ℓ=0 zero mode a *negative* stiffness from FD boundary placement → e³² blowup burying every peak (fixed: `ü=−Hu`, `m²=ω²−1`; method detail, gates untouched). [falsification/S2_s3_tower](falsification/S2_s3_tower) · ~~"The rest-buzz instrument reads ANY hidden manifold whose Laplacian is known: the S³ tower is n(n+2)."~~ (Rung 1 of `KK_EXTENSION_NOTES.md`.) | bridge FD on S³; gate against the exact Casimir spectrum. | The curved-space generalization of legs S/U. **Payout: the instrument is a METHOD, not a flat-space artifact — rung 1 of the (A) ladder climbed.** Zero novelty in the physics (textbook S³/SU(2) Casimir); the (B) cliff untouched. |
| **S3** ✓ DONE 2026-07-24 — **UNDECIDED(gate mis-specified); postulate SUPPORTED, KILLED definitively excluded** · KK on ℝ^{1,3}×drum: masses `m_k²=λ_k` (eigenVALUE) vs vertices `g_ijk=∫ψiψjψk` (eigenFUNCTION). **δ_spec falls 5.24%→0.67%** (isospectral, K2 reproduced) while **δ_coup RISES 0.09%→1.86%**, h→0 limit **+2.137%**, against a congruent-mirror **null extrapolating to +0.007%** (a clean ∝h artifact: δ_coup·n = 39.3,39.6,39.7,39.8,39.8). S3a ✅ S3c ✅ S3d ✅; **S3b failed only on my own `δ_coup>10·δ_spec` bar — unreachable by construction** (δ_spec is staircase-limited to ≈h^0.97, already documented in K2 ⇒ would need n≈450). Not relabelled; S3′ re-registered instead. Also caught: a verdict-logic `else` branch that printed "KILLED — the couplings agree too" against its own run's numbers. [falsification/S3_drum_compactification](falsification/S3_drum_compactification) · ~~"A KK reduction on a GWW-drum cross-section yields two field theories with identical mass towers but distinguishable local physics."~~ | bridge: FD tower on both drum cross-sections (connectivity-asserted per L2) + a local observable that separates them. | Unifies the whole arc — K2 (same tower) + K5 (locals leak) — in field-theory language. **Payout: identical particle masses, cubic vertices differing by ~2% — the tower can't tell them apart, a scattering amplitude can.** Toy setting; zero novelty (GWW/Sunada + textbook KK overlaps); the join and the convergence control are the bridge's part. |

## Tier A — audits (new tier, born from L2)  ·  **A1 ✓ DONE 2026-07-24 — SURVIVES** (93 too-clean values across 17 files, all exact-by-construction or the caught K2 bug; 0 new suspects; complete-baseline guard installed; M4's K2-entangled uniform floor confirmed clean = operator identity). [falsification/A1_tooclean_audit](falsification/A1_tooclean_audit)

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
3. ~~**S1** — Schiemann pair~~ **✓ DONE 2026-07-24 — KILLED** (exact: same theta to norm 400, det 35852544 both; degree-2 Siegel differs at bucket (48,96,−24), 0 vs 4). Flat 4-tori are not spectrally determined; the KK tower cannot fix the hidden T⁴ in dim ≥ 4. [falsification/S1_schiemann_tori](falsification/S1_schiemann_tori)
4. **A1** — too-clean audit (cheap; institutionalizes L2)
5. **R3** — the Clausius scaling law (reuses K3 machinery end-to-end)
6. ~~**S2**~~ **✓ DONE 2026-07-24 — SURVIVES** (curved-space rung: rest-buzz reads √(n(n+2)) to 0.42%, degeneracy (n+1)² measured via the n≥ℓ cutoff; n=3/m²=15 producible by no unit flat T³). The instrument is a method, not a flat-space artifact. [falsification/S2_s3_tower](falsification/S2_s3_tower) · ~~**S3**~~ **✓ DONE 2026-07-24 — UNDECIDED(gate), postulate SUPPORTED** (identical towers, vertices differing by a 2.14% h→0 limit vs a 0.007% null; the failing condition was my own unreachable bar). [falsification/S3_drum_compactification](falsification/S3_drum_compactification)

**Round-10 standing (2026-07-24) — v2 COMPLETE.** Every pre-registered v2 item has fired: Tier R (R1 KILLED ·
R2 CROSS-GATE+O4 · R3 KILLED · R4 postulate-TRUE · R5 KILLED-as-stated · R6 KILLED), Tier A (A1 SURVIVES),
Tier S (S1 KILLED · S2 SURVIVES · S3 UNDECIDED-gate/SUPPORTED), plus G8 SURVIVES.

**Ledger: 6 kills · 3 survivals · 1 postulate-true · 1 undecided · 1 cross-gate closed · 1 new obstruction
(O4) — and 7 self-caught instrument bugs, every one a silent failure that looked like a result.** The kills
carry mechanisms (R3's first-order law, R6's odd-d no-universal-log, S1's Siegel witness); the survivals
carry localized obstructions (S2's curved-space reach, A1's standing guard). The seventh bug is a new
species — **the wall was my own pre-registered threshold** — which is now itself a G7 data point.

**Open, carried:** the S3′ re-registration (frozen in S3's FINDINGS, deliberately not run same-day) · the O4
relay to ansatz · sister-dependent items G6/G1/G5/K6/G4 · G7 (standing meta-claim, fed seven times, still
unfalsified).

Sister-dependent carryovers from v1, unchanged: G6's three vacuum-vs-vacuum pairs · G1 · G5 · K6 · G4
(parked on the symplectic integrator) · G8 (deepstrain standing challenge) · G7 (standing meta-claim, fed
five times, still unfalsified).

## What v2 is not

Same as v1, verbatim: not a route to new laws of nature; not a claim that survivors are true; not exempt
from the house rules. The realistic ceiling moved up slightly in one place only — R2/M6, where round 1's
kill left an actual provable-looking statement on the table. That is what an informed round means.
