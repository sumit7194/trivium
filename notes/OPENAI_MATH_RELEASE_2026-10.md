# The OpenAI maths manuscript release (Oct 2026): a screening note for future reference

Screened 2026-10-19 by the bridge. Source: github.com/openai/math (CONTENTS.md; 719 manuscripts, 372 result families,
released 2026-10-06; 3 withdrawn on 2026-10-07). Only some are Lean-formalized. **Treat every claim as unverified,
and apply our own rigour (independent checks) before relying on anything.**

## Method
- A keyword screen of all 372 family blocks: integrability, geodesics, Kerr, Killing tensors, chaos/horseshoe,
  Hamiltonian systems, Lyapunov exponents, computer-assisted/interval methods, cosmic censorship, CFT
  (stress tensor, ANEC, QNEC, central charge).
- The abstracts of the 6 candidates were read.

## Candidates and relevance
| # | Claim | Relevance |
|---|---|---|
| 146 | Standard map: positive metric entropy for all large parameters (Sinai's conjecture); Lean comparator files StandardMapEntropy/Lyapunov/Components.lean | Closest to the chaos-proof programme (it is much stronger than a horseshoe, for a different system). **Possible future use: its Lean definitions of Lyapunov exponents, entropy and hyperbolic components for 2D maps, when we state our horseshoe result in Lean.** Check Mathlib compatibility and soundness first. |
| 264 | Strong cosmic censorship near two-ended Kerr data | Context for the MN naked-ring write-up (censorship framing). Citation-level only. |
| 260 | Spacetime Penrose inequalities incl. rotation | Context only |
| 147 / 150 | Near-boundary Birkhoff conjecture (billiards); ergodicity and weak mixing of irrational triangular billiards | Integrability cousins; not usable |
| 282 | Scale ⇒ local conformal symmetry in 4D unitary QFT (under stated hypotheses) | **Possible background for cuspis** (whose bounds assume conformal symmetry). Not yet shared; the user says share later if needed. |

## Not found
Nothing on Morales–Ramis/Ziglin integrability, geodesics in exotic spacetimes, Killing tensors, Ernst-potential
solutions, or interval-arithmetic ODE proofs.
