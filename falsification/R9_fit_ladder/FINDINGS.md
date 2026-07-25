# R9 — Findings: R6's log coefficient is not extractable at all. UNDECIDED, with the reason found.

*Run 2026-07-26; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2+,
Tier R. **Closes an UNDECIDED we opened ourselves this morning** — and closes it by showing the question was
never answerable on this instrument.*

## Result in one line

**UNDECIDED(extraction unstable).** `b` does not **converge** as the fit model is extended — it moves by up
to **14× its own jackknife error** between consecutive model orders, with the higher-derivative regulator
running from **−0.27 → −11.37 → −45.86**. So neither "truncation artifact" nor "robust measurement" is
established: **R6's b = 2.32 / 3.72 / 0.52 is a property of a particular truncation, not of the theory.**
R6 stays UNDECIDED — but we now know *why*, which is the finding.

## The ladder

| model | b bare | b improved | b higher-deriv | **Δ_b** | mean jk err | cond |
|---|---|---|---|---|---|---|
| **M3** `a n²+b log n+c` (R6's) | 2.171 | 3.442 | −0.268 | 3.711 | 0.120 | 2.7e1 |
| **M4** `+ d/n` | 3.011 | 3.091 | −11.369 | 14.460 | 0.775 | 1.7e2 |
| **M5** `+ e/n²` | 1.376 | −3.068 | −45.857 | 47.233 | 2.974 | 8.0e2 |

**R9a regression: PASS to 0.00%** — R6's model on R6's radii reproduces 2.322 / 3.718 / 0.522 exactly, so the
pipeline is R6's and the later gates are live.

## L12 decided this, and it took both probes

This is the second time today [L12](../../FALSIFICATION_V2.md) (quantum's lesson) has settled a verdict, and
here the two probes point *opposite ways*:

- **Floor probe — PASSES.** Δ_b sits **31× / 19× / 16×** above the jackknife noise at M3 / M4 / M5. The
  spread is unambiguously above the numerical floor at every order.
- **Limit probe — FAILS.** `b` itself drifts by up to **14× its own error** between consecutive orders. There
  is no limit for it to be a measurement *of*.

Taking the floor probe alone — which is what R6 effectively did — gives "the spread is real, b is
non-universal." That is precisely the wrong conclusion, and it is the one R6 shipped. **A quantity that
swings by 45 units depending on which subleading terms you include has not been measured, however far its
spread sits above the noise.**

## The instrument note — my conditioning guard was the wrong quantity

R9c pre-registered a **condition-number** gate (>10¹⁰ ⇒ unreliable), borrowed from tabula's catch that
collinear columns manufacture structure. It reported **2.7e1 / 1.7e2 / 8.0e2 — "fine" at every order**, while
`b` was swinging by tens.

**The condition number was the convenient quantity, not the right one** — [L8](../../FALSIFICATION_V2.md), on
my own gate, in the very run where I applied L8's source lesson to someone else. A well-conditioned design
matrix guarantees the *coefficients are determined by the data*; it says nothing about whether the
coefficient you care about is **stable under a change of model**. The right test is the direct one added
here: does the estimate move by more than its own error when you extend the model? It does, by 14×.

That guard is now the operative one, and it generalises: **for any coefficient extracted from a truncated
expansion, report its drift across model orders in units of its own error.**

## A post-hoc observation, flagged as such and NOT gated

Not pre-registered, so it decides nothing, but it is visible and worth recording for whoever picks this up:
at **M4**, the two conventional regulators **agree to 2.6%** — bare 3.011 vs improved 3.091 — collapsing from
their 1.27 spread at M3. The entire M4 spread is carried by the **higher-derivative** regulator (−11.37),
which was also the one R6 found "not resolvable" at M3. `K_hd = K + γK²` is a more aggressive modification
than a stencil change, and it is plausibly not in the same regulator family at all.

**This is a hypothesis, not a result.** Testing it would need the ladder rerun on a regulator set chosen to
share a common continuum limit at a stated order — which is exactly the design quantum used in their 2D build
(four regulators verified to agree to 1e-6…1e-10 at small k). Our three were never checked for that.

## What this does to R6

R6's status is unchanged (**UNDECIDED**) but its epitaph is now written:

- R6's **mechanism** was wrong (retracted this morning — spatial/spacetime dimension conflated).
- R6's **numbers** are real but are an artifact of the M3 truncation; they do not survive model extension.
- So R6's original **KILLED** verdict was wrong *twice over*, by two independent routes, and the honest
  status is: **this instrument cannot extract the subleading log coefficient of the 3D area law.**

By [A2's taxonomy](../A2_wall_audit/FINDINGS.md) that is a **species-1 (precision/instrument)** wall, not the
species-3 (definitional) one R6 claimed. Prescription: *keep pushing — a bigger instrument.* And the wall is
demonstrably crossable in principle: **quantum measured a universal log to 0.6% of c/6** in D = 2 with exact
free fermions and a proper continuum-limit scan. Different instrument, different reach — ours does not get
there in D = 4 with a 3-term fit on 20 radii.

## Honest scope

- **Zero novelty.** That a truncated fit contaminates a subleading coefficient is standard numerical
  practice. The falsifiable content was whether **our own banked R6 result survives its own pre-registered
  caveat.** It does not.
- **No theoretical value of b was asserted or compared against** (**L10**) — the gate was the three
  regulators against each other, which is what R6's pre-registration required and its FINDINGS violated.
- A negative result about our instrument, not about the physics. Nothing here says the universal log does not
  exist in D = 4; it says we cannot see it.
- Same lattice, same regulators, same pipeline as M2/R6; only the fit model and radius count changed.
- Bridge-solo; imports M2's module unchanged; numpy only.

## Inputs & artifacts

`code/r9_ladder.py` · `results/r9_ladder.json`. Resolves the *why* of
[R6](../R6_arealaw_log/FINDINGS.md)'s UNDECIDED. Applies **L12** (quantum) and catches an **L8** failure
(tabula) in its own pre-registered guard.
