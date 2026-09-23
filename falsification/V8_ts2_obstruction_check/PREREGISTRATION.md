# V8 — Pre-registration: a second-session check of quantum's Tomimatsu–Sato δ=2 obstruction

*Frozen 2026-09-24, before any derivation or code. This is the bridge's own lane: independent verification
of a sister's claim, as in V5 and V7.*

## Why

quantum's proof tool (Stage 2b′, `ce2cab8`) reports a Morales–Ramis **OBSTRUCTION** for TS δ=2. The setting:
- the equatorial particular solution y = 0, p_y = 0, with σ = 1;
- (E, L, μ²) ∈ {(1,0,4), (1,0,9), (1,1,4)};
- (p, q) ∈ {(3/5, 4/5), (4/5, 3/5)}.

Its own grade is "post-failure; monodromy uncorroborated". Its strongest form (called ξ₁) rests only on Kovacic's
necessary conditions plus a logarithmic singular point, the same kind of argument as the published Zipoy–Voorhees
δ=2 proof (arXiv:1302.4234). If it stands, it would be a proof that TS δ=2 is not meromorphically integrable near
that solution. A preliminary prior-art check found no such proof in print. So it needs a second route before
anyone leans on it.

## What this check is, and is not

- **NOT blind.** The bridge has read quantum's report: the singular-point list (x = 0, a ring quartic, a turning
  sextic, and ∞ of order 4), b = 3/4 with N = 2 and a log term at x = 0, b = −3/16 elsewhere, and "min Σα = 2 > max α∞ = 1".
  It has also read ansatz's sealed expectation (non-integrable).
- **Independent in code and derivation.** The bridge derives the normal variational equation itself, from
  ansatz's metric component files. It imports nothing from quantum. The metric is shared input (data). Its vacuum
  property rests on ansatz's Schwartz–Zippel check; V8 re-checks it at fresh random rational points.
- It checks the ξ₁ route only. It does not re-check ξ₂, monodromy, or quantum's Stage-1 calibration.

## Steps and predictions (each gets its own verdict)

- **V8a — set-up.** The metric is even in y, so y = 0, p_y = 0 is an invariant plane for the geodesic flow.
  Vacuum holds at 3 fresh random rational points per parameter value.
- **V8b — the NVE.** Along Γ, with x as the independent variable (a finite covering, as in the ZV paper), the
  normal variational equation in (y, p_y) reduces to z″ = r(x) z with r ∈ ℚ(x). The bridge lists r's finite
  singular points (factored over ℚ), their pole orders, and the order of r at ∞.
- **V8c — local analysis.** At each singular point, the leading coefficient b and the exponent difference.
  - **Prediction:** at x = 0, exponent difference N = 2 (integer), with a **nonzero logarithmic term**, which the
    bridge checks by its own Frobenius recursion;
  - **prediction:** the other finite singular points have exponent difference ½, with b = −3/16.
- **V8d — Kovacic.**
  - A log point implies the local monodromy contains a nontrivial unipotent, which excludes Kovacic's cases 2
    and 3.
  - Case 1 requires some choice of exponents with d = α∞ − Σ_c α_c ∈ ℤ≥0.
  - **Prediction:** no choice gives d ∈ ℤ≥0, so case 4 holds, G = SL(2, ℂ), and G⁰ is non-abelian: the Morales–Ramis
    obstruction.

## Controls (each must behave before the TS rows are read)

- **ZV δ=2 (q = 0)**, built by the bridge from the standard static form f = ((x−1)/(x+1))²,
  e^{2γ} = ((x²−1)/(x²−y²))⁴, ω = 0, not from ansatz's files. It must give OBSTRUCTION by the same code. That is
  the known answer.
- **Kerr (δ = 1)**, from ansatz's same-pipeline Kerr file at (3/5, 4/5). It must **NOT** give OBSTRUCTION: either
  there is no log point, or a case-1 d ∈ ℤ≥0 survives.
- If either control misbehaves, V8 is **REFUSED** and the TS rows are not read.

## Verdicts

- **CONFIRMED:** V8a–V8d reproduce the obstruction on every row, and the controls behave.
- **DISAGREES:** a row where the bridge finds a case-1 d ∈ ℤ≥0, or no log point. That is reported as a conflict
  with quantum's result, with the details.
- **INCONCLUSIVE:** the bridge can't complete a step, for example because the Frobenius log test is ambiguous.
  "Can't reproduce" is never "refuted" (the V5 lesson).

## Scope, which travels with any verdict

Meromorphic integrals only, in a complex neighbourhood of Γ, at the tested (p, q) and (E, L, μ²) only, on the
supplied metric. It says nothing about how much chaos there is. It is AI checking AI.
