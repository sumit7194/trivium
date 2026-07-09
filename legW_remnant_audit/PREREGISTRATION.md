# Leg W — Pre-registration: arithmetic audit of the G₂-remnant paper (Pinčák et al., GRG 58(3), 2026)

*Frozen 2026-07-10, before `code/remnant_audit.py` is written or run. The bridge's discipline pointed
**outward** for the first time: a dimensional-arithmetic audit of the published, world-press-covered paper
"Geometric origin of a stable black hole remnant from torsion in G₂-manifold geometry" (Pinčák, Pigazzini,
Pudlák, Bartoš; General Relativity and Gravitation 58(3), 19 Mar 2026, DOI 10.1007/s10714-026-03528-z,
open access). This is an audit of the paper's QUOTED NUMBERS against its OWN formulas — not a judgment of
the model's physics (7D Einstein–Cartan on M₄×S³ with G₂ structure), which is outside the bridge's scope.*

## The paper's quoted claims (as extracted from the open-access text, 2026-07-10)

- Remnant mass formula: **M_res = ⟨τ₀⟩²/M_Pl**, with ⟨τ₀⟩ = 246 GeV (electroweak VEV) and
  **M_Pl = 1.22×10¹⁹ GeV** ("used consistently throughout").
- Quoted value in GeV (eq. 47): **M_res ≈ 4.96×10⁻¹⁵ GeV** (abstract-level "≈ 5×10⁻¹⁵ GeV").
- Quoted value in kg (abstract + eq. 20): **M_res ≈ 9×10⁻⁴¹ kg** — the number propagated by ScienceDaily,
  Live Science, SciTechDaily, the SAS press release, etc.
- Remnant entropy/information: **S_remnant = 4π(M_BH/M_Pl)²**; for a solar-mass hole,
  "approximately **1.515×10⁷⁷ qubits**".

## Frozen constants (CODATA/IAU)

GeV→kg: 1 GeV/c² = 1.78266×10⁻²⁷ kg · M_Pl = 1.22×10¹⁹ GeV (the paper's own value) ·
M_Pl = 2.17643×10⁻⁸ kg · M_☉ = 1.98892×10³⁰ kg · ln 2.

## Frozen gates

- **W1a — the GeV value is self-consistent.** M_formula = 246²/1.22×10¹⁹ GeV, compared to the paper's
  4.96×10⁻¹⁵ GeV. Gate: agree within **5%**. Expected: PASS (the formula gives 4.960×10⁻¹⁵).
- **W1b — the kg value is consistent with the GeV value.** Convert M_formula to kg and compare to the
  paper's 9×10⁻⁴¹ kg. Gate: agree within a **generous factor √10 ≈ 3.16**. Expected from recon: **FAIL** —
  the formula gives ≈ 8.84×10⁻⁴² kg = **0.884×10⁻⁴¹ kg**, so the paper's kg figure appears high by
  **≈10.2×**, consistent with a dropped leading zero (0.9×10⁻⁴¹ → 9×10⁻⁴¹). If W1b fails, the finding is an
  **internal inconsistency between the paper's own two quoted values** (its GeV number follows from its
  formula; its kg number does not), not a claim about which the authors intended.
- **W2 — the qubit count.** S_bits = 4π(M_☉/M_Pl)²/ln2 vs the claimed 1.515×10⁷⁷ qubits. Gate: within
  **1%**. Expected: PASS — with the note (fixed in advance) that this number is **exactly the standard
  Bekenstein–Hawking entropy** of a solar-mass black hole converted from nats to bits; it contains no
  physics specific to the 7D model. (ansatz's S=A/4 module computes the same number; the bridge's stdlib
  suffices.)
- **O3 — observation, NOT a gate.** The remnant's own geometric (Bekenstein) entropy at M_res,
  4π(M_res/M_Pl)², is ~10⁻⁶⁶ — while the claimed storage is ~10⁷⁷ qubits. The ~143-order gap is the
  standard information-capacity objection to remnant scenarios (see Chen–Ong–Yeom, arXiv:2412.00322);
  the paper's proposed carrier (trapped QNM spectrum / interior states) must bear all of it. Logged as
  physics commentary with citation, explicitly not an arithmetic verdict.

## Honest scope (fixed in advance)

- **In scope:** only what can be recomputed from the paper's own stated formulas and constants (W1, W2, O3).
- **Out of scope:** M_KK^min ≈ 8.6×10¹⁵ GeV and the instanton action S_I ~ 6×10⁶⁶ (their derivations were
  not extractable from the OA page at audit time); the validity of the 7D Einstein–Cartan/G₂ model itself;
  whether remnants resolve the information paradox. A symbolic check of the paper's KK reduction is a
  **conditional ansatz ask (round-6 Ask 3)** gated on this leg's outcome.
- Source-text caveat: quoted values were extracted from the Springer OA page via web fetch (2026-07-10);
  the abstract's "9×10⁻⁴¹ kg" is independently corroborated by the SAS press release and multiple press
  outlets. If the PDF's eq. 20 differs from the fetched text, the audit updates — transparently, as an
  amendment.
