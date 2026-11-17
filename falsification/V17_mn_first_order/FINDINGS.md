# V17: findings. Independent first-order check of ansatz §153 (Manko–Novikov quadrupole on Kerr)

*2026-11-17. Pre-registration aea5ffb, with amendments 1 (0e8de6b), 2 (3e6557b) and 3 (5f0b714). The bridge's own
code: v17.py on V10's jet machinery and V9's MN transcription. Results: results/v17_runs.jsonl and v17_driver.log.
The seal is results/V17_SEAL.sha256. Non-blind: the headline of §153 was known; its code, MN file, points and
parameters were not.*

## Verdict: CONFIRMED (agrees with §153)
At first order in the MN quadrupole parameter β, **only the trivial Killing tensors survive at every valence 1–6**.
S equals the floor (2, 4, 6, 9, 12, 16) for every combination of:
- both parameter sets, (M, a) = (5, 3) and (13, 5);
- both points, P_A = (3/2, 1/3) and P_B = (2, −1/4);
- both primes, 2³¹ − 1 and 2³¹ − 19.

All 48 target runs reached the floor already at N = r + 1, with no escalation needed. The two formulations agree
everywhere (S_A = S_B), and the Kerr basis gate holds in every run (rank equals the Kerr count 2, 5, 8, 14, 20, 30).

So Carter (valence 2), Carter² (4) and Carter³ (6) all fail to extend at first order, and so does every other non-trivial
combination of Kerr tensors up to valence 6.

## Controls: 96 of 96 pass (attempt 2, under amendment 3)
| Control | Expectation | Result, valence 1–6, both points, both primes |
|---|---|---|
| Kerr family, ∂/∂M (survival visible) | Kerr count | 2, 5, 8, 14, 20, 30 |
| Kerr family, ∂/∂a | Kerr count | 2, 5, 8, 14, 20, 30 |
| Null coordinate change, −L_ξ G₀ | Kerr count | 2, 5, 8, 14, 20, 30 |
| Sabotage, x·y in the tt slot (death visible) | < Kerr count at valence 2 | floor at every valence: 2, 4, 6, 9, 12, 16 |

The series-exactness gate (amendment 3) passed for all 12 case × parameter × point combinations, including the target.

## What went wrong on the way (disclosed)
1. **Amendment 1, before any run.** The registered null vector field would have created a g^xy term, which V10's
   operator cannot represent, so the field was replaced.
2. **Amendment 2, after the sign check.** Both signs of a pass the Carter gate, as they must, because they differ by
   the trivial tensor 4a p_t p_φ. The gate was shown able to fail.
3. **Attempt 1 failed a control: the null control "killed" Carter at valence 2.**
   - Root cause: a Lie derivative of a truncated series loses its top-order coefficient, and that creates a false
     constraint.
   - Fix: build that control one order higher, then truncate.
   - New mandatory gate: series exactness.
   - Attempt 1's logs are kept. The lesson: **death verdicts are sensitive to top-order series accuracy**, and the gate
     now guards it.

## Grade and scope
- **Exact modular arithmetic, two primes, two points, two parameter sets. Not a theorem.**
  - A rank drop mod q could fake a death. Two primes and the controls make that unlikely, but they don't exclude it.
  - A jet-level death is a necessary-condition failure near the point: no smooth first-order K₁ exists there.
- **Not covered:**
  - the pole-order ladder: the bridge has no independent partial-survival control. ansatz's §141 ladder reproduction is
    its own;
  - valence above 6;
  - second order in β;
  - global questions.
- **Consistency:** this fits V10-MN, the exact non-perturbative MN with a trivial bound to valence 10, and the known
  chaos in MN. It adds the first-order statement: no Kerr hidden symmetry can be continued even infinitesimally along
  the MN quadrupole direction.

## Comparison with ansatz §153 (sealed e85f7f4)
- **ansatz:** floor 2/4/6/9/12/16 at valence 1–6, with Carter, Carter² and Carter³ dead.
- **Bridge:** identical, by independent code, a different chart point set, a different formulation (explicit basis +
  solvability), and two primes.

**AGREE.** Non-blind, because the headline was known before running.
