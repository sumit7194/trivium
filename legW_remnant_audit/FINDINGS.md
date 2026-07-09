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
