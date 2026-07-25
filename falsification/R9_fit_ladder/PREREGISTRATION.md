# R9 — Pre-registration: was R6's non-universal log a real result, or a truncated fit?

*Frozen 2026-07-26, before `code/r9_ladder.py` is written or run. Falsification v2+, Tier R. **This closes an
UNDECIDED we opened ourselves today.***

## Why this exists

[R6](../R6_arealaw_log/FINDINGS.md) measured the subleading log coefficient across three regulators —
**b = 2.32 / 3.72 / 0.52**, across-spread 1.31 ≫ within-jackknife 0.29 — and called it KILLED, explained by
"odd d has no universal log." **That mechanism was retracted today** (prompted by quantum): the rule is even
*spacetime* dimensions, and R6 was **D = 4 spacetime — even — so a universal log SHOULD exist there**.
quantum's TFIM (D = 2, also even) measured exactly such a log converging on **c/6 to 0.6%**.

So R6 sits at **UNDECIDED**: the numbers stand, the explanation is gone, and the expectation is now the
*opposite* of what R6 concluded. R6's own pre-registration named the leading suspect and the write-up then
talked past it:

> *"further subleading terms that a 3-parameter fit may fold into b"*

R9 tests exactly that. `S(n) = a·n² + b·log n + c` is a **truncation**. If the true expansion carries `1/n`,
`1/n²`, … terms, a 3-parameter fit has nowhere to put them but into `b` — and *how much* leaks in would
depend on the regulator, manufacturing a spread from a universal quantity.

## The postulate

**"R6's across-regulator spread in b is a fit-truncation artifact: extending the model collapses it."**

## Method

Reuse M2/R6 verbatim (`extract_kappa`'s tail-extrapolated `S_ext(n)`, N = 200, L0 = 500, the three regulators
`K_bare/K_impr/K_hd`). Radii extended to **n = 6, 8, …, 44 (20 values)** — more than R6's 9, because a
5-parameter fit on 9 points is not a fit. Extra radii are nearly free: they index into the same
eigendecompositions.

**The model ladder**, fitted per regulator:

| order | model |
|---|---|
| M2 | `a·n² + c` |
| **M3** | `a·n² + b·log n + c`  ← **R6's model** |
| M4 | `a·n² + b·log n + c + d/n` |
| M5 | `a·n² + b·log n + c + d/n + e/n²` |

At each order, extract `b` for all three regulators, plus a **jackknife** error (drop-one radius).

## Frozen gates

- **R9a — regression.** At order M3 with **R6's original radii**, reproduce b = 2.32 / 3.72 / 0.52 to within
  5%. **If this fails, the pipeline differs from R6's and every later gate is void.**
- **R9b — the ladder (decisive).** Track the across-regulator spread `Δ_b(order)`.
  - **postulate TRUE (R6's spread was truncation)** iff `Δ_b` **collapses** with model order — specifically
    `Δ_b(M5) < ½·Δ_b(M3)` **and** `Δ_b(M5)` falls below the mean jackknife error at that order (i.e. the
    regulators become consistent). R6 would then flip: **b is universal after all**, and R6's kill was a
    truncation artifact.
  - **postulate FALSE (R6's measurement is robust)** iff `Δ_b` stays ≥ ½·Δ_b(M3) at every order. The spread
    survives model extension, and the puzzle deepens rather than resolves.
  - **UNDECIDED(conditioning)** if the higher-order fits are ill-conditioned — see R9c.
- **R9c — the conditioning guard (tabula's lesson, applied to our own fit).** `{n², log n, 1, 1/n, 1/n²}` on
  a bounded radius range is a **badly conditioned basis** — this is exactly tabula's catch that
  *collinear columns manufacture structure*. Compute the fit design matrix's condition number at each order.
  **A model order whose condition number exceeds 10¹⁰ is reported as UNRELIABLE and excluded from the
  verdict**, never silently used. If M5 is unreliable the verdict rests on M4.
- **R9d — L12, applied.** Deciding "is the spread real?" needs **both** probes: the **floor** (jackknife
  error — is Δ_b above noise?) **and** the **limit** (does Δ_b vanish as the model is extended?). Both are
  reported at every order; neither alone decides.

## What is deliberately NOT done

**No theoretical value of b is asserted or compared against** — the gate is the three regulators *against
each other*, exactly as R6's pre-registration required and its FINDINGS then violated. The known D = 4 sphere
log coefficient is not invoked from memory (**L10**). If the regulators converge, the finding is "consistent
with a universal value," and stating *which* value would require a verified source we do not currently have.

## Honest scope

- **Zero novelty.** That a truncated fit contaminates a subleading coefficient is standard numerical
  practice; the D = 4 universal log is textbook. The falsifiable content is **whether our own banked R6
  result survives its own pre-registered caveat.**
- A collapse would **not** prove b universal in general — only that our measurement no longer shows it
  non-universal, which is a weaker and honest claim.
- Same lattice, same regulators, same instrument as M2/R6; only the fit model and radius count change. A
  failure here is a fit failure, not a physics result.
- Bridge-solo; imports M2's module unchanged; numpy only.
