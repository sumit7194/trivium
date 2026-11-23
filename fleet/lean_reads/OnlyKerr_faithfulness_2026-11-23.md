# OnlyKerr Glue.lean: faithfulness read (Layer 1), 2026-11-23
Reader: a fresh-context Opus agent (Bridge subagent) that did not write the file. Read-only: no Lean was run; grep and reading only.
Status: the Lean runs (vacuity instances V1–V7, re-running #print axioms) are PENDING, for a gap with no route beside them.

## Verdicts
| README row | Lean | Verdict | Note |
|---|---|---|---|
| 1a | elim_identity L49–52 | FAITHFUL w/ caveat | Re-derived by hand. hD (DD ≠ 0) is ALWAYS true for real a, y, so it is redundant, not a restriction. x/0 is not exploitable. |
| 1b | curzon_tr_h1/h2/comm | FAITHFUL | Over any field. hτ genuinely needed (at τ = 0, tr h1 = 2u²). |
| 2 | glue_min_pos, glue_re_pos | FAITHFUL | |
| 2 | re_pos, G1_ne_zero | FAITHFUL w/ caveat | Pointwise only; "all (k, y)" lies outside Lean. hE is redundant given hE1. |
| 2 | rescale_case1/2b/2a | FAITHFUL w/ caveat | Not used by re_pos (the chaining is done by hand). **Case 2a is proved only for the factor c = a**: if the 2a certificate is written for H/(a√(1+s)) with bound < 1, the transfer FAILS. |
| 3a–3d | k5_3a…k5_3d | FAITHFUL | The Mathlib lemmas are genuine (file:line given). Margin in 3d: 2.7e-5 in the exponent. |
| CertCases description | L144–145 | NOT FAITHFUL to the README wording | See below. |

## CertCases
- Definition: 0 < Re(H²) ∨ |Im H| < Re H ∨ (a ≤ |y| ∧ |Im H| < a). There is no k anywhere in Lean. The 2b region (|y| < a) is dropped, which is harmless. Disjunct 2 implies disjunct 1, so 2b is redundant in the glue.
- README L30 "at each (a, y), at least one holds" is quantified wrongly: H depends on k (and possibly E, s/θ), so the statement must range over all of them.
- **Possible coverage gap:** the cases list k ≤ 0 and 0 < k < 30/7, but README L35 and Glue L143 say they "cover every (k, y)". What happens at k ≥ 30/7 is not settled in these files.

## What an outside reader must trust
(1) the physics identification of c0, f0, G1, H; (2) each interval certificate on its region, including large |y|; (3) coverage of the full domain (k, y, a ∈ (0,1), E² ≥ 1, s/θ), especially k ≥ 30/7; (4) the rescaling each certificate uses (Case 2a!); (5) that the certificate's H is the Lean H; (6) that the domain is a ∈ (0,1), E² ≥ 1.

## Other findings
- Axioms: all 16 audited theorems use only propext/Classical.choice/Quot.sound, and there is no sorry/axiom/native_decide. Audit gap: g1_conj, g2_conj and M0_inv are not in Axioms.lean (add #print axioms lines).
- lake_build.log is a cached REPLAY of Glue, not a fresh elaboration (consistent hashes, but still a replay).
- README's "peak ~170 MB" is misleading: the same log shows max RSS ~2.45 GB.
- The 3d proof also uses √2 > 1.4142 (proved locally), which the README omits.

## Vacuity instances to run later (V1–V7)
In the reader's report (Bridge transcript, 2026-11-23). Key ones: V1 (DD never 0), V3 (a Case-2a-only instance), V4 (CertCases not trivially true), V5 (G1 = 0 exactly where CertCases fails: the hypothesis does real work), V6 (hτ needed).
Full snippets are saved alongside in OnlyKerr_vacuity_snippets.lean.

## Author resolution (17:03, Quantum; accepted by the Bridge)
- Case 2a: the certified quantity is θ^(-1/2)|Im H~_θ| = |Im(H/a)|, so c = a and the transfer HOLDS (algebra checked by the Bridge). Trust item: the identity H = a√(1+s)H~_θ (from T19; implemented in Bridge V26-K).
- Coverage: the domain is k < 30/7 (the theorem's range). Case 1 covers k ≤ 0 and Cases 2a/2b cover 0 < k < 30/7. NO GAP; the README wording is to be fixed.
- Provenance: Neon T19 (/u/1, 2026-11-21), fleet-verified by Bridge V26 Addendum K (mpmath iv). K2 FAILED as registered and K2′ PASSED (margin 0.99937); tails and holomorphy were read by hand.
- README/Axioms fixes (5 housekeeping items + 3 wording fixes) are held until the ZiglinCert read finishes.
**Net: FAITHFUL WITH CAVEATS once the README is reworded. No change to the Only-Kerr argument.**
