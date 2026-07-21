# Leg W — Findings: the bridge's discipline pointed outward — an arithmetic audit of the G₂-remnant paper

*Run 2026-07-10; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code was written. The
first leg to audit something **outside the family**: Pinčák, Pigazzini, Pudlák & Bartoš, "Geometric origin
of a stable black hole remnant from torsion in G₂-manifold geometry," GRG 58(3), 2026 (open access) — the
paper behind the week's "black hole information paradox solved" world press. Audit of the paper's quoted
numbers against its own formulas; the 7D Einstein–Cartan model itself is out of scope.*

## Result in one line

The paper's two quoted remnant masses are **mutually inconsistent by 10.2×** — its GeV value
(4.96×10⁻¹⁵ GeV, eq. 47) follows exactly from its own formula M = ⟨τ₀⟩²/M_Pl, but its **kg value
(9×10⁻⁴¹ kg, abstract + eq. 20) is 10.18× too high**; the formula-true value is **0.884×10⁻⁴¹ kg**,
consistent with a dropped leading zero — and the kg number is the one propagated by ScienceDaily,
Live Science, SciTechDaily, and the SAS press release. Meanwhile the paper's headline
**1.515×10⁷⁷-qubit** claim is verified at 0.07% — but it is *exactly* the standard Bekenstein–Hawking
entropy of a solar-mass hole converted to bits: correct arithmetic, no model-specific physics.

## The gates

| gate | claim | recomputed | verdict |
|---|---|---|---|
| W1a | M_res = 4.96×10⁻¹⁵ GeV (eq. 47) | 246²/1.22×10¹⁹ = 4.960×10⁻¹⁵ GeV | **PASS** (ratio 1.000) |
| W1b | M_res ≈ 9×10⁻⁴¹ kg (abstract, eq. 20) | 4.960×10⁻¹⁵ GeV × 1.78266×10⁻²⁷ = **0.884×10⁻⁴¹ kg** | **FAIL** (ratio 10.18×) |
| W2 | 1.515×10⁷⁷ qubits (solar mass) | 4π(M☉/M_Pl)²/ln2 = 1.514×10⁷⁷ bits | **PASS** (ratio 1.0007) |

W1b's failure mode is precise: 9×10⁻⁴¹ kg back-converts to 5.05×10⁻¹⁴ GeV — ten times the paper's own
eq. 47. One of the two numbers must be wrong, and the GeV one is the one that follows from the formula.
0.884×10⁻⁴¹ ≈ "0.9×10⁻⁴¹" → "9×10⁻⁴¹" is the natural typo path.

## Observation O3 (not gated, frozen as commentary)

The remnant's **own** Bekenstein entropy at M_res is 4π(M_res/M_Pl)² ≈ 2×10⁻⁶⁶ nats, versus the ~10⁷⁷-qubit
storage claim — a **~143-order-of-magnitude gap** that the paper's trapped-QNM/interior mechanism must
carry entirely. This is the standard information-capacity objection to remnant scenarios
([Chen–Ong–Yeom review](https://arxiv.org/abs/2412.00322)); logged as physics context, not an arithmetic
verdict.

## Honest limits

- **Source-text caveat.** Quoted values were extracted from the Springer open-access page by web fetch
  (2026-07-10); the kg figure is independently corroborated by the abstract as quoted in the SAS press
  release and multiple press outlets. Before any outward communication (e.g. a note to the authors), the
  PDF's eq. 20 should be read directly; if it differs, this audit amends transparently.
- **Typo-class finding, not a refutation.** The model's internal logic is untouched — the correction makes
  the remnant *lighter* by 10×, not the mechanism wrong. What the finding does show: the number in every
  headline is not the number the paper's own formula gives.
- M_KK^min ≈ 8.6×10¹⁵ GeV and S_I ~ 6×10⁶⁶ were not auditable from the OA page (derivations not
  extractable) — out of scope, as pre-registered.
- **Conditional round-6 Ask 3 (ansatz, 7D Einstein–Cartan reduction check): now unlocked but demoted in
  urgency.** The audit's verdict is that the paper's checkable layer contains one press-propagated
  arithmetic slip and one standard-physics number in new clothes; a full torsion-engine build to check the
  symbolic layer is defensible but no longer the best use of ansatz's queue ahead of the flux atlas and
  Jacobson. Recommendation: keep Ask 3 parked.

## Inputs & artifacts

- Paper: [DOI 10.1007/s10714-026-03528-z](https://link.springer.com/article/10.1007/s10714-026-03528-z)
  (OA) · press: [ScienceDaily](https://www.sciencedaily.com/releases/2026/06/260624025506.htm) ·
  [SAS release](https://sav.sk/index.php?doc=services-news&lang=en&news_no=13537&source_no=20).
- `code/remnant_audit.py` (stdlib) · `results/remnant_audit.json`.

---

## RE-AUDIT (2026-07-22) — from the PDF. Conclusion confirmed; our v1 evidence was partly a tool artifact.

The v1 audit was challenged on exactly the right point: it never read the paper. Its numbers came from the
Springer OA page through an automated fetch whose text extraction is done by a small summarizing model. The
PDF has now been read directly. **The verdict survives and is stronger. Two of v1's cited quotes do not.**

### What the paper actually says (PDF, verbatim, with locations)

| item | value | where |
|---|---|---|
| the formula | **M_res = ⟨τ₀⟩²/M_Pl**, Eq. (37) | p.16 |
| the VEV | ⟨τ₀⟩ ≈ 246 GeV | abstract, p.10, p.16, p.26 |
| the Planck mass | **M_Pl ≈ 1.22×10¹⁹ GeV** — "Inserting the numerical values ⟨τ₀⟩ ≈ 246 GeV, λ = 1, M_Pl ≈ 1.22e19 GeV" | p.10, verbatim |
| the remnant mass | **≈ 9×10⁻⁴¹ kg** | abstract; Conclusions item 1: "M_res = ⟨τ₀⟩²/M_Pl ≈ 9e−41 kg" |

The paper quotes **one** mass, not two, and states it *next to the formula it is supposed to follow from*.

### The verdict, now from primary source only

Evaluating **the paper's own Eq. (37) with the paper's own two constants**:

    M_res = 246² / 1.22×10¹⁹ GeV = 4.960×10⁻¹⁵ GeV = 8.843×10⁻⁴² kg = 0.884 × 10⁻⁴¹ kg

The paper states **9 × 10⁻⁴¹ kg** — larger by **10.18×**. To obtain 9×10⁻⁴¹ from Eq. (37) with
⟨τ₀⟩ = 246 GeV one needs M_Pl = 1.2×10¹⁸ GeV, i.e. **the paper's own Planck mass with the exponent reduced
by one**. The formula-true value 0.884×10⁻⁴¹ is what "≈ 0.9×10⁻⁴¹" would round to, so a dropped leading
zero (or a slipped exponent) reproduces the published figure exactly. **The finding stands, and no longer
depends on any tool-extracted text.**

### W2 confirmed against the paper's own equations

The qubit chain is reproduced step-by-step from Eqs. (59)–(62) using the paper's own constants
(M_Pl = 2.176×10⁻⁸ kg, M_☉ = 1.989×10³⁰ kg): 9.1406×10³⁷ → 8.3551×10⁷⁵ → 1.0499×10⁷⁷ nats →
**1.5147×10⁷⁷ qubits** vs the paper's 1.515×10⁷⁷ — **0.02%**. Arithmetic correct. And the paper's own
Eqs. (46)→(58) derive it as `S = 4π(M_BH/M_Pl)²`, i.e. **exactly Bekenstein–Hawking**, confirming v1's
observation that the headline number carries no model-specific physics. Note the paper uses the *correct*
Planck mass here (2.176×10⁻⁸ kg) — the slip is confined to the remnant-mass statement.

### Correctness ledger — our own failure, and it is the serious one

v1 asserted that "the paper's **two** quoted masses are mutually inconsistent — eq. 47 gives 4.96×10⁻¹⁵ GeV,
eq. 20 gives 9×10⁻⁴¹ kg." **Neither citation is real.** The paper quotes no GeV value for M_res, and the kg
value is in the abstract/conclusions, not eq. 20. The extraction model almost certainly *computed*
⟨τ₀⟩²/M_Pl itself — despite an explicit instruction not to compute — and dressed it as a quotation with an
invented equation number. Because that fabricated number happened to equal the correct formula output, it
looked *corroborating*, which is precisely why it went unchallenged: **a hallucination that agrees with your
hypothesis is the hardest kind to catch.**

Gate **W1a is VOID** — it tested agreement between the formula and a quote that does not exist.

The process lesson, now standing policy for the bridge: **an automated text extraction is not a source.**
For any claim about what an external document says, the primary document must be read directly before the
claim is written down — and doubly so when the extraction supports what we already expect. v1 also flagged
"verify the PDF before any outward note"; that caveat was correct and is now discharged, but the fabricated
citations should never have been written as quotations in the first place.

### Net

- **The physics finding is confirmed and strengthened** — sourced entirely from the PDF, using only values
  the paper itself prints, and it is a typo-class slip (the model is untouched; the remnant is simply 10×
  lighter than published).
- **Our evidence chain was contaminated** by fabricated citations, published in FINDINGS and a commit
  message for one day before being caught by a challenge from the user.
