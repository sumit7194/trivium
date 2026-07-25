# R6 — Findings: the 3D area-law log coefficient measured regulator-dependent — MECHANISM RETRACTED

> ## ⚠️ MECHANISM RETRACTED 2026-07-26 — the dimension-parity claim below is INVERTED
>
> Prompted by quantum's L9 re-test of this very item. **The rule is even *SPACETIME* dimensions ⇒ universal
> log** (Casini–Huerta; the coefficient is the conformal anomaly on the sphere), odd spacetime ⇒ a universal
> constant (F-term). This document says *"in **odd** dimension — here 3D — the universal subleading term is
> instead a constant"* — conflating **spatial** with **spacetime** dimension.
>
> R6 was a **d = 3 spatial** scalar, i.e. **D = 4 spacetime — EVEN**. So a universal log **should** exist
> here. quantum's independent check makes the error unmissable: their TFIM is d = 1 spatial (D = 2, even) —
> "odd spatial dimension" by this document's own wording — and they measured the universal log converging on
> **c/6 to 0.6%**.
>
> **Retracted:** the mechanism ("odd d has no universal log, so `b·log n` fits scheme-dependent residue")
> and the claim that the kill was "the expected physics."
> **Stands as measurement:** b = 2.32 / 3.72 / 0.52 across the three regulators, across-spread 1.31 ≫
> within-jackknife 0.29. Those numbers were measured and are unaffected.
> **Status downgraded:** from *KILLED with a mechanism* to **UNDECIDED** — the measurement now demands an
> explanation we do not have. R6's own pre-registration listed the leading candidate: *"further subleading
> terms that a 3-parameter fit may fold into b"*, which it named as a live UNDECIDED cause and which this
> document then talked past. A second possibility, flagged as **open and not asserted**: the massless
> *minimally* coupled lattice scalar may not extract the same log as the conformal one. **Neither is claimed
> here** — that is the point of the retraction.
>
> **quantum's ξ/L question, answered:** M2/R6's operators are **massless** (verified while building
> [R8](../R8_regime_scan) — there is no mass term; I had to add `m²I` myself). So **ξ = ∞, ξ/L = ∞**, far
> above their ≳ 2.5 boundary. R6 was *not* a simulation-design artifact of their kind — which is precisely
> why the wrong-mechanism problem is the live one.
>
> **The discipline failure, named:** R6's pre-registration said *"No theoretical value for b is asserted from
> memory (leg-W discipline)."* The FINDINGS then asserted a *structural* claim from memory anyway. Same
> failure mode as [M6](../M6_prior_art_gate/FINDINGS.md)'s retraction today — a mechanism asserted without
> being checked — two days older.


*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier R — the universal companion to M2's kill. M2 showed the 3D entanglement area-law **coefficient κ is
scheme-dependent** (0.30/0.41/0.51, 51% spread) while the **exponent stays ≈2** (universal). R6 asked
whether the **subleading log coefficient b** in `S(n) = a·n² + b·log n + c` is universal like the exponent —
or scheme-dependent like κ.*

## Result in one line

**KILLED (b regulator-dependent).** Fitted b = **2.32 / 3.72 / 0.52** across the bare / improved /
higher-derivative regulators — an across-regulator spread of **1.31**, far larger than the mean
within-regulator jackknife error **0.29**. The log coefficient moves with the UV scheme *exactly like κ*.
The pre-registered "most-likely" outcome was UNDECIDED(precision); the data were sharper than that and
returned a clean KILL, with a mechanism.

## The gate table

| regulator | κ (fit a) | b (log) | b jackknife | log term resolvable? |
|---|---|---|---|---|
| R1 bare NN | 0.300 | **2.32** | 2.34 ± 0.08 | yes |
| R2 improved | 0.411 | **3.72** | 3.73 ± 0.05 | yes |
| R3 higher-deriv | 0.510 | **0.52** | 0.44 ± 0.75 | **no** (log adds nothing, ×1.0) |
| control (midpoint) | 0.296 | −0.45 | — | coordinate change, not a regulator |

across-regulator spread of b = **1.31**  ≫  mean within-regulator jackknife error = **0.29**  ⇒ **KILLED**.

## The mechanism (why this KILL is the *expected* physics, not a defeat)

The kill is not "our fit failed" — it is what the entanglement-entropy literature predicts, and it sharpens
the story M2 began:

- **Odd spatial dimension has no conformal anomaly ⇒ no universal log term.** The universal (scheme-
  independent) subleading quantity in the sphere EE is a *log* only in **even** dimension (where it carries
  the conformal-anomaly / central-charge coefficient). In **odd** dimension — here 3D — the universal
  subleading term is instead a **constant** (the "F-term"), and the coefficient of `log n` is **not** a
  protected quantity. So a `b·log n` fit in 3D is fitting a term the theory does *not* protect: it absorbs
  whatever finite-radius lattice residue the particular regulator leaves behind. That residue is
  scheme-dependent — hence b is scheme-dependent. R3's b is not even resolvable (adding the log term does not
  reduce its residual: ×1.0), which is the same statement from the other side: there is no real log there to
  fit.
- **This completes M2's "what is universal in the area law" ledger**, now with all three rungs measured on
  the same instrument:
  - **exponent ≈ 2** — universal (M2);
  - **κ** (leading area coefficient) — scheme-dependent, 51% spread (M2);
  - **b** (log coefficient) — **scheme-dependent** (R6, this finding), *because 3D has no universal log at all*.
  The universal subleading content in 3D lives in the **constant** c, not in b — R6 did not target c (out of
  the frozen gate), and that is the honest next question, not a claim made here.

## The instrument note

The pre-registration flagged UNDECIDED(precision) as most likely because b is a ~10⁻⁴ relative correction on
the κn² term. In fact two of three regulators resolved b sharply (jackknife errors 0.05–0.08) — but they
resolved it to *different, scheme-specific* values, which is the KILL. The one regulator where the log was
**not** resolvable (higher-deriv, ×1.0 improvement, error 0.75) is consistent with the same conclusion: no
protected log to find. So the instrument was good enough to decide — it just decided KILLED rather than
UNDECIDED. Honest read: our lattice resolves b's *scheme-dependence*, and the physics says that is all there
is to resolve, because the protected 3D subleading term is a constant, not a log.

## Honest scope

- A **lattice** statement about a free scalar's sphere EE — not a black hole's S = A/4. Zero novelty
  (Srednicki; Bombelli–Koul–Lee–Sorkin; Casini–Huerta on the F-term / odd-d universal constant;
  Solodukhin for the even-d log). The value of R6 is *internal cross-validation*, not new physics: it
  confirms on our own instrument that only the exponent is universal, and pins *why* the log is not.
- **No theoretical value for b was asserted from memory** (leg-W discipline): the decisive comparison was the
  three regulators *against each other*. The dimension-parity fact (log ⇒ even d, constant ⇒ odd d) is
  invoked only to *interpret* a KILL that the data delivered on their own — not to manufacture the verdict.
- The `a·n²+b·log n+c` model is a truncation; further subleading terms (1/n, …) are folded into the fit.
  That contamination is part of *why* a 3D log coefficient is not a clean universal — which is the finding,
  not a caveat against it. Bridge-solo; reuses M2's V2-calibrated entropy pipeline.

## Inputs & artifacts

`code/r6_log.py` (fits S(n)=a·n²+b·log n+c per regulator, jackknife on b) · `results/r6_log.json`.
Reuses `M2_arealaw/code/m2_arealaw.py` (`extract_kappa`, `K_bare/K_impr/K_hd/K_mid`). No sister — the
free-scalar EE instrument is bridge-local. Companion kill to M2 (κ scheme-dependent); together they say:
**of {exponent, κ, log}, only the exponent is universal — and in 3D the log was never going to be.**
