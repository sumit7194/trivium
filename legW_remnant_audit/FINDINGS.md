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

---

## RE-AUDIT v3 (2026-07-22) — I over-corrected. Eq. (20) is real, W1a is UN-VOIDED, and there is a SECOND slip.

The v2 re-audit above contains **my own error**, and it is the mirror image of v1's. v1 trusted an extraction
without reading the paper. v2 then read the paper — but only pages 1–4, 9–10, 15–17 and 24–26 — and from
that **partial** read declared: *"The paper quotes no GeV value for M_res anywhere."* That statement is
**false**. Page 8, which v2 never opened, contains Eq. (20):

> *"Using the geometric relation M_res = ⟨τ₀⟩²/M_Pl with ⟨τ₀⟩ = 246 GeV and M_Pl = 1.22 × 10¹⁹ GeV gives*
> **M_res = (246 GeV)²/(1.22 × 10¹⁹ GeV) ≃ 5 × 10⁻¹⁵ GeV ≃ 9 × 10⁻⁴¹ kg."**   (Eq. 20, p.8)

**Both values, in one equation, on one line.** So v1's core framing — *the paper's two quoted masses are
mutually inconsistent* — was **correct**, and closer to the truth than my correction of it. Gate **W1a is
UN-VOIDED**: it tested a quote that genuinely exists (the paper prints ≃5×10⁻¹⁵ GeV; v1's "4.96×10⁻¹⁵" was
the extraction being more precise than the source). Only v1's *equation number* for it ("eq. 47") was wrong.

### Slip 1 — Eq. (20): the mantissa is right, one exponent digit is wrong

| quantity | value | status |
|---|---|---|
| 246²/1.22×10¹⁹ | 4.9603×10⁻¹⁵ GeV | paper prints **≃5×10⁻¹⁵ GeV** — **correct** |
| that value in kg | 8.84×10⁻⁴² kg → rounds to **9×10⁻⁴² kg** | paper prints **≃9×10⁻⁴¹ kg** — **off by 10.18×** |

The forensics are now exact, and cleaner than either hypothesis entertained earlier: **the mantissa "9" is
precisely right, and only the exponent is wrong — −42 printed as −41.** The number it converts *from* is
correct and printed on the same line. It is a one-character unit-conversion slip, not a calculation error
and not a dropped zero.

### Slip 2 — Eq. (25) vs Eq. (17): the same quantity, in a third unit, wrong by ~200×

Eq. (17), p.7: *"m_phys ≃ 1 × 10⁻¹⁵ GeV"* — that is **10⁻⁶ eV**.
Eq. (25), p.9: *"m_φ ~ v²/M_Pl ≃ 10⁻³ eV"*, described in the same sentence as *"the same order of magnitude
as the torsion-Higgs mass computed in Eq. (17)."*

But v²/M_Pl = 4.96×10⁻¹⁵ GeV = **4.96×10⁻⁶ eV**. So:

- the paper's **claim** (same order as Eq. 17 = 10⁻⁶ eV) is **correct** at the true value 5×10⁻⁶ eV;
- the paper's **printed number** (10⁻³ eV) is **202× larger** and is *not* the same order as Eq. (17),
  contradicting its own sentence.
- A GeV→eV conversion using 10¹² instead of 10⁹ reproduces the printed figure (4.96×10⁻³ ≈ 10⁻³ eV).

### The unifying finding

**Both slips are unit conversions of the same, correctly-computed quantity.** The paper derives
v²/M_Pl = 5×10⁻¹⁵ GeV and states it correctly (Eq. 20). It then converts that one number into kg (Eq. 20,
wrong by 10×) and into eV (Eq. 25, wrong by ~200×). The underlying physics number is right in both places;
only its expression in other units fails. That is why the errors survived review: the derivation is sound
and the primary quantity is correct — the failures are in the last inch.

Both are also **self-evident from the paper alone**: Eq. (20) contradicts itself across a single line, and
Eq. (25) contradicts Eq. (17) via the paper's own explicit claim of order-of-magnitude equality. No external
convention or assumption is needed to see either.

### Correctness ledger — the bridge's second error in this leg, and its lesson

v2's failure was *partial reading presented as complete verification*. Having caught v1 for not reading the
source, v2 read four page-ranges out of 33, found no GeV value in them, and wrote a universal negative
("nowhere in the paper"). The correct scope for that sentence was "not in the pages I read."

Standing policy, extended: **a negative claim about a document requires reading the document, not sampling
it.** Positive claims can be made from a located quote; negative claims ("the paper never says X") require
coverage, or must be stated with their actual scope. Both v1 and v2 erred in the same direction — toward the
conclusion we already believed.

### Net after three passes

- **The finding is confirmed, and is now larger than first reported:** two independent unit-conversion slips
  (Eq. 20, factor 10; Eq. 25, factor ~200), both provable from the paper's own printed values, neither
  touching the model's mechanism.
- **The bridge erred twice getting here** — once by trusting an extraction, once by over-correcting from a
  partial read — and both errors are recorded above rather than quietly rewritten.

---

## RE-AUDIT v4 (2026-07-22) — ALL 33 PAGES READ. v1 was right; my v2/v3 accusations were false.

The full PDF has now been read cover to cover (pp. 1–33). The record must be corrected **in v1's favour**,
and against my own two "corrections".

### Retraction: the extraction never hallucinated

**Eq. (47) exists, on p.19, and reads exactly:**

> *"Given ⟨τ₀⟩ ≈ 246 GeV and M_Pl ≈ 1.22e19 GeV, the remnant mass is:*
> **M_res = (≈246 GeV)²/(≈1.22e19 GeV) ≈ 4.96e−15 GeV."   (47)**

v1 reported "eq. 47 gives 4.96×10⁻¹⁵ GeV". That is **verbatim correct** — the equation number, the value,
and all three significant figures. **v2's claim that the extraction "computed the value itself and attached
an invented equation number" is retracted in full**, as is v3's residual claim that "only the equation
number was wrong." Neither was true. The tool read the paper correctly; I accused it of fabrication on the
basis of not having read pp. 8 and 19.

**Gate W1a is restored, PASS.** The paper prints a GeV value in *two* places (Eq. 20 p.8, Eq. 47 p.19), both
correct, and a kg value that does not follow from either.

### The four checkable statements, all located

| # | where | paper prints | correct value | status |
|---|---|---|---|---|
| 1 | **Eq. 47, p.19** | M_res ≈ 4.96×10⁻¹⁵ GeV | 4.9603×10⁻¹⁵ GeV | ✅ correct |
| 1 | **Eq. 20, p.8** | "≃ 5×10⁻¹⁵ GeV ≃ **9×10⁻⁴¹ kg**" | 5×10⁻¹⁵ GeV = 8.91×10⁻⁴² → **9×10⁻⁴² kg** | ❌ **10.2×**; mantissa right, exponent −42→−41 |
| 2 | **Eq. 25, p.9** vs **Eq. 17, p.7** | m_φ ~ v²/M_Pl ≃ **10⁻³ eV**, "same order as Eq. 17" | v²/M_Pl = 4.96×10⁻⁶ eV; Eq. 17 = 10⁻⁶ eV | ❌ **202×**; contradicts its own Eq. 17 |
| 3 | **Eq. 49, p.19** | "(1.22×10¹⁹)²/246 ≈ **6.05×10¹⁵ GeV**" | 6.050×10³⁵ GeV | ❌ **10²⁰**; mantissa right, exponent off by 20 |
| 4 | **Eq. C.7, p.31** vs **Eq. 48, p.19** | S_inst = 8π²·**2.5×10³³** → exp(−2×10³⁵) | Eq. 48 gives (M_Pl/M_res)² = 6.05×10⁶⁶ → 4.78×10⁶⁸ | ❌ uses the **unsquared** ratio; also contradicts Eq. 45 (exp(−10⁶⁹)) |

Items 3 and 4 are **new** and were invisible until the appendices were read. Note the pattern in 1 and 3:
in both, the **mantissa is exactly right and only the exponent is wrong** — the arithmetic was done
correctly and mis-transcribed. Item 4 is a substitution slip (ratio for ratio-squared) and is physically
inconsequential (every value is an effectively-zero decay rate), but it contradicts two other equations in
the same paper.

Item 3's physical value is *not* in doubt: Eq. 21 (p.8), Eq. 29 (p.10) and Eq. C.8 (p.31) all give
M_KK ≈ 5–8.6×10¹⁵ GeV consistently. Only the printed division in Eq. 49 fails to evaluate to its own result.

### Correctness ledger — final accounting for this leg

Three passes, and **the bridge's errors were both mine, not the tool's**:

- **v1** (extraction-sourced): conclusion correct, citation correct. Its only real flaw was *epistemic* —
  it asserted the paper's contents without having read the paper, and was right by luck of a good extraction.
- **v2**: read 4 page-ranges of 33, found no GeV value in them, and published the universal negative "the
  paper quotes no GeV value anywhere" plus an accusation of tool fabrication. **Both false.**
- **v3**: corrected part of v2 but still asserted the "eq. 47" citation was invented. **Also false.**
- **v4** (this): full read. v1 vindicated; two further errors found in the paper.

The lesson stands and sharpens: **v1's process was wrong even though its answer was right, and my
corrections were confidently wrong twice while sounding more rigorous each time.** Being the one who says
"actually, let me check" is not the same as having checked. The only pass that settled anything was the one
that read all 33 pages.

---

## RE-AUDIT v5 (2026-07-22) — independent second audit; 8 arithmetic errors + 1 structural failure

An **independent Claude session** was given the v4 findings and re-derived everything from the Springer
full text without access to this session's work. It confirmed items 1–3, inferred item 4 by proxy, and
**found four further arithmetic errors and one structural failure**. Every claim below was then
**re-verified here against the PDF** (`code/verify_crosscheck.py`) before being recorded — the second
audit is corroboration, not authority.

### Confirmed arithmetic errors (8)

| # | where | paper prints | correct | off by | note |
|---|---|---|---|---|---|
| 1 | **Eq. 20, p.8** (+ abstract, Concl. 1) | 9×10⁻⁴¹ kg | 8.84×10⁻⁴² kg | **10×** | mantissa exact |
| 2 | **Eq. 25, p.9** | 10⁻³ eV | 4.96×10⁻⁶ eV | **202×** | and 1000× off Eq. 17, which it claims to match |
| 3 | **Eq. 49, p.19** | 6.05×10¹⁵ GeV | 6.05×10³⁵ GeV | **10²⁰** | mantissa exact |
| 4 | **Eq. C.7, p.31** | 8π²×2.5×10³³ | 8π²×6.05×10⁶⁶ = 4.78×10⁶⁸ | — | uses the **unsquared** ratio |
| 5 | **Eq. 15, p.7** | 1.35×10⁻³² | 1.355×10⁻³⁴ | **10²** | mantissa exact |
| 6 | **Eq. 22, p.8** | r₄/ℓ_Pl ≃ 2.4×10³³ | 2.44×10³ | **10³⁰** | 2.4×10³³ is **M_Pl/M_res** (Eq. 48) — a quantity transplanted from another equation |
| 7 | **Eq. 45, p.18** | exp(−10⁶⁹) | 64π³×6.05×10⁶⁶ = 1.2×10⁷⁰ | ~12× | order-of-magnitude claim; mild |
| 8 | **§2.6 ΔS, p.10** | 10⁻²⁹ | 3.43×10⁻²⁷ | ~343× | |

**Eq. C.7 is now directly confirmed** — the second audit could not see it (Springer's HTML truncates
mid-Appendix C) and inferred it from the body's three inconsistent decay rates. This session has the PDF:
p.31 reads verbatim *"Γ ∼ exp(−S_inst) ∼ exp(−8π² × 2.5 × 10³³) = exp(−2 × 10³⁵)"*, and 2.5×10³³ is
M_Pl/M_res, not its square. The paper states this one quantity **three times with three values**:
exp(−10⁶⁹) (Eq. 45), exp(−6×10⁶⁶) (§7.1.3), exp(−10³⁵) (Eq. C.7 / §7.4 item 5).

**The pattern:** in items 1, 3, 5, 6 the **mantissa is exactly right and only the exponent is wrong**. That
is the signature of arithmetic performed correctly and then mis-transcribed — not of misunderstood physics.

### Item 3 is deeper than a typo — two incompatible definitions of r₄

The second audit's sharpest catch. §7.1.4 uses `r₄ ~ ⟨τ₀⟩/M_Pl²`, which gives **r₄ = 3.26×10⁻⁵² m**.
Appendix A (Eq. A.13) derives **r₄ = 3.9×10⁻³² m**. The ratio is **1.196×10²⁰** — exactly the factor by
which Eq. 49 fails. So the 10²⁰ is not a typo; it is two mutually inconsistent definitions of the same
quantity. And the §7.1.4 version is the one promoted to **Conclusions item 4 as the paper's "falsifiable
prediction"** (`r₄² ~ ⟨τ₀⟩²/M_Pl²`) — i.e. the flagship prediction rests on the relation that contradicts
the appendix which allegedly derives it.

### The structural failure — Appendix B does not derive what it claims

This is larger than all the arithmetic combined, and it sits under the paper's central claim.

- **Eq. B.8:** `ln Ω = (π/3)⟨τ₀⟩³/M_Pl³` = **8.59×10⁻⁵¹** (paper prints 8.6×10⁻⁵¹ — matches).
- **Eq. B.9:** asserts this **equals** `4π M_BH²/M_Pl²` — the Bekenstein–Hawking entropy.

Two independent problems, both verified here:

1. **Numerically false.** With the paper's own M_res, `4π M_res²/M_Pl²` = **2.08×10⁻⁶⁶** (paper prints
   2.1×10⁻⁶⁶). B.8 and B.9 differ by **4.1×10¹⁵**.
2. **Structurally impossible.** B.8 scales as `⟨τ₀⟩³/M_Pl³`; the target scales as `⟨τ₀⟩⁴/M_Pl⁴` under the
   paper's own M_res relation — *different powers*. More fundamentally, **M_BH appears nowhere in
   B.1–B.8**: the cavity radius (B.3) is `⟨τ₀⟩/M_Pl²` and the cutoff (B.6) is `M_Pl`, both fixed constants.
   A derivation containing only constants produces a **single fixed number** and cannot scale with
   progenitor mass. The step B.8 → B.9 silently replaces M_res with M_BH.

Since matching Bekenstein–Hawking entropy *is* the paper's claim to resolving the information paradox, the
microscopic derivation does not establish the result it is presented as establishing. **Stated at its
proper strength:** the derivation *as printed* contains no M_BH dependence and so cannot yield a
mass-dependent entropy. Whether the authors have an unwritten argument supplying it is unknown to us — which
is why this belongs in correspondence as a **question**, not a verdict.

### What is clean

Eqs. 59–62 (solar-mass qubit count) verify exactly (1.515×10⁷⁷, reproduced to 0.02%), and Eqs. 28/29 are
consistent with Appendix A's r₄. The derivational logic of §2 and §6 is sound; the failures are
concentrated in transcription, and in Appendix B's final step.

### Method note

This is the family's cross-validation pattern applied to an external target: two independent audits, no
shared work, each re-verifying the other before recording. The second audit corrected the first's
*coverage* (four missed errors, one missed structural failure); this session corrected the second's one
*gap* (Eq. C.7, unreachable in HTML). Neither was taken on trust.
