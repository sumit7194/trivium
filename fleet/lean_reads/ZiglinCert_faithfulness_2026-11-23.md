# ZiglinCert library: faithfulness read (Layer 1), 2026-11-23
Reader: a fresh-context Opus agent (Bridge subagent) that did not write the library. Read-only: no Lean was run. One light Python check compared the certificate files with their exported JSON.

## Verdicts
| Theorem | Verdict | Note |
|---|---|---|
| L1_common_eigvec_comm_trace (Certificate.lean:171) | FAITHFUL | |
| L5_gl2_restatement (C:282) | FAITHFUL w/ caveat | The s = 0 junk case is never hit in its only use (L6_gl2, where s ≠ 0). |
| L6_not_virtually_abelian (C:223) | FAITHFUL | Stronger than claimed (A ranges over arbitrary subgroups). |
| L6_gl2 (C:310) | FAITHFUL for the group statement | The "i.e. G⁰ non-abelian" gloss needs outside facts: monodromy ⊆ Galois group, [G:G⁰] finite, the basis. PREREG_lean_certificate_arithmetic.md:9 "⇒ G⁰ not virtually abelian" is loose. |
| L7_unipotent_one_eigenline (C:380) | FAITHFUL | |
| crit1_math (Boxes.lean:183), crit2_math (B:222) | FAITHFUL w/ caveat | Only ⇒ (soundness) is proved; the comments and prereg say ⇔. |
| cert_sound (B:285), cert_of_check (B:308) | FAITHFUL, vacuity gap | CertConclusion is trivially true for an EMPTY box, and `check` does not test lo ≤ hi. The reader checked all 132 boxes outside Lean: all non-empty and all dyadic, with 0 mismatches against the JSON. |

## Chain
- **Lean checks:** the criterion arithmetic on the exported exact-ℚ boxes (kernel `decide +kernel`, no native_decide), and the group step to "not virtually abelian" (L6_gl2).
- **Outside Lean:**
  - that the true monodromy lies in the boxes (ODE Taylor enclosures, tails, the v1/v2 engines, loop composition);
  - loop geometry;
  - the NVE derivation;
  - Morales–Ramis/Ziglin, monodromy ⊆ Galois, and [G:G⁰] finite.
- **Export:** sound. Arb → 60-digit text → arb (outward rounding) → exact Fractions → ℚ literals. No rounding risk was found.

## Outward sentences
- **EMAIL_DRAFT_expert_v2:16 (SENT to Loukes-Gerakopoulos, 2026-11-22 07:40):** "with the logic and arithmetic checked in the Lean proof assistant". OVERSTATED: the ODE enclosure arithmetic and the Morales–Ramis logic are not in Lean.
- **EMAIL_DRAFT_2007_authors_v2:51 (SENT to Dubeibe/Sanabria-Gómez/Pachón, 2026-10-17):** "Their logic and arithmetic were checked in the Lean proof assistant." OVERSTATED, for the same reason.
- **Faithful:** EMAIL_DRAFT_expert (v1):23 "final algebraic step checked in Lean". The public snapshot SUMMARY.md:19 "the final algebraic and arithmetic step, kernel-checked in Lean 4" (the page linked in the Loukes email). ONE_PAGER(_v2).
- **CLAIMS_LEDGER:**
  - :8 "logic Lean-checked" is ambiguous;
  - :50–51 "52/52" is a cross-family total sitting under MN equatorial (12/12). The total is 64/64 since 943266e;
  - :35 and :65 are accurate.
- **THEOREM.md:82 "12/12 Lean-checked (L6_gl2)":** the count is accurate. It needs "box arithmetic + group step kernel-checked; enclosures and Morales–Ramis outside Lean".
- **Suggested precise wording:** "The final step, that the certified matrix enclosures force a monodromy group that is not virtually abelian, including its interval arithmetic, was checked in the Lean proof assistant. The enclosures themselves and the Morales–Ramis theorem are not formalised."

## Other
- Axioms: only propext/Classical.choice/Quot.sound (axioms_final.log, 10-12; the library is unchanged since 7aef095). Full Certs.All build PASSED 10-12 and 11-18. The default `lake build` does NOT build the certs (they are reached only via Certs/All.lean).
- Controls weaker than the prereg: 1(b) "widen until the commutator reaches 2" became poison_comm (G with itself); control 3 (soundness spot-check) has no artefact; the Kerr controls fail via crit1 only, so crit2 is never exercised by them; lean_gen_controls.py's docstring vs code mismatch (it also widens imaginary parts).
- mr_mn_axis_lattice.py:489 hard-codes certificate_ok/gate_bit_for_bit = True (a labelling issue, not soundness; Lean re-checks).
- Vacuity snippets (to run in a gap): see the Bridge transcript; key ones are a satisfiable check-pair, two rejected pairs, the empty-box CertConclusion gap, and per-certificate non-emptiness.
