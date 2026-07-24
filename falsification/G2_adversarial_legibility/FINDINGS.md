# G2 — Findings: the flagship biconditional is KILLED, and replaced by a sharper one

*Joined 2026-07-24. Gate frozen in [PREREGISTRATION.md](PREREGISTRATION.md) **before** either sister built or
ran anything; ansatz's verdicts sealed and bridge-verified before tabula ran blind. Ledger item G2 (Tier G —
the family's flagship claim under deliberate attack). **Verdict: KILLED** — the outcome the ledger itself
called "arguably more valuable than the survival."*

## Result in one line

Leg Q's **"legible ⟺ KY-integrable"** is **false**. Candidate A — integrable via an irreducible Killing
tensor with **no Killing–Yano root** — is **legible** (tabula emitted its exact quadratic invariant to
2.2×10⁻¹⁹, blind). Candidate B — integrable via a **transcendental** invariant — is **illegible**. Legibility
does not track Killing–Yano structure, and does not track integrability either: it tracks **whether the
invariant is polynomial-representable in the probe's basis**.

## The join (frozen table applied)

| candidate | sealed (ansatz, bridge-verified) | tabula, blind | frozen conclusion |
|---|---|---|---|
| **A** | integrable · irreducible rank-2 Killing tensor · **no KY root** · non-vacuum | **LEGIBLE** — exact quadratic invariant, **2.2×10⁻¹⁹** | **G2 KILLED** — legible *without* KY |
| **B** | integrable · **transcendental** invariant I = p_y/p_x − ln p_x · no polynomial invariant of degree ≤ 4 | **ILLEGIBLE** (certify-relative-to-basis; best 2.2×10⁻⁵, monotone but non-converging) | supports **H_POLY** |

Both candidates are non-KY-integrable under the reading frozen in the addendum (the *hidden* constant must
come from an irreducible K = Y·Y; B's two covariantly-constant KY forms square to *reducible* Killing tensors
and carry no hidden constant).

## What legibility actually tracks — the localization

The 8/8 record could not separate three hypotheses because KY-ness, integrability and polynomial-invariance
coincided in every catalog entry. The two designed metrics pull them apart, and the answer is unambiguous:

| hypothesis | prediction for A | prediction for B | survives? |
|---|---|---|---|
| **H_KY** — tracks Killing–Yano | illegible | illegible | ❌ **dead** (A is legible without KY) |
| **H_INT** — tracks integrability | legible | legible | ❌ **dead** (B is integrable but illegible) |
| **H_POLY** — tracks a polynomial-representable invariant | legible | illegible | ✅ **the survivor** |

> **The corrected claim: legible ⟺ the metric's hidden invariant is polynomial-representable in the probe's
> basis.** Killing–Yano structure was never what legibility was measuring — it was a *proxy*, exact on the old
> catalog because Collinson (1976) / Dietz–Rüdiger (1981) force KT ⇒ KY for type-D **vacua**, and the whole
> catalog was type-D vacuum. The moment Candidate A leaves vacuum, the proxy and the real quantity separate,
> and legibility follows the polynomial, not the KY.

That theorem is the deep reason the 8/8 was never evidence for H_KY: the coincidence was **forced by the
catalog's own restriction**, not discovered. This is exactly the failure mode adversarial design exists to
expose.

## Why the two verdicts are strong rather than lucky

- **A is a genuine blind rediscovery.** ansatz *constructed* a metric with an irreducible rank-2 Killing
  tensor; the bridge independently confirmed {Q,H} = 0 and that its four distinct mixed eigenvalues forbid any
  KY root; then tabula, never shown any of it, **emitted the same quadratic invariant to 2.2×10⁻¹⁹**. Three
  instruments, one answer, no shared code.
- **B's "illegible" is a measured boundary, not a shrug.** tabula reported
  **certify-relative-to-basis** with a monotone-but-non-converging degree sequence — the signature of
  polynomials chasing a transcendental target — and calibrated that rung deliberately (their script 160 basis
  ladder). "My basis cannot see it" is a *named, measured* limit rather than an excuse, which is what makes
  H_POLY a positive finding instead of a failure to find.
- The bridge verified ansatz's half **before** tabula ran, and the blind package was leak-checked. The
  independence that makes agreement meaningful was preserved end to end.

## Honest limits

- **Instrument-relative by construction.** "Legible" is tabula's emit-or-certify notion at their thresholds,
  and B's verdict is explicitly *relative to their polynomial basis*. The corrected claim inherits that
  scoping: it is a statement about what this probe accesses, not a theorem about learnability in general. A
  richer basis (rational, or log-augmented) could in principle make B legible — that is a well-posed follow-up,
  not a defect.
- **A is non-vacuum by necessity**, so the corrected claim is not a statement about vacuum spacetimes, where
  KT ⇒ KY makes H_KY and H_POLY indistinguishable *as a matter of theorem*. On the old catalog the original
  biconditional remains empirically correct — it was the *generalisation* that was wrong.
- Candidate B is **identified from the literature** (Galajinsky 2021), not invented, so no novelty is claimed
  for the example; the novelty, such as it is, lies in using it as an adversarial probe.
- A kill of a flagship claim deserves a prior-art sweep before anything is asserted publicly: whether
  "learned-geometry legibility tracks polynomial representability" is already known in the
  learning-dynamical-systems literature is an open question for the standing sweep.

## tabula's own honest flags (recorded, not smoothed)

- A **trajectory-indexing bug** briefly made *both* candidates read illegible, caught only because their
  hand-derived invariant contradicted the engine. Same species as the bridge's own K2 grid bug this round:
  both were caught by cross-checking a machine answer against an independently derived one, which is the only
  reason either was caught at all.
- The D2 raw-waveform drum arm missed its strength gate — a **learnability**, not information, limit.

## Inputs & artifacts

ansatz §120 (Candidate A), §121 (Candidate B, after Galajinsky, Phys. Lett. B 820 (2021) 136483) · tabula's
blind legibility run + script 160 (basis ladder) · Collinson 1976 · Dietz–Rüdiger 1981 ·
[leg Q](../../legQ_geometrizes_integrability) (the 8/8 record under attack).
`code/verify_candidates.py` · `results/bridge_verification.json` · `results/*_SEALED.json` (bridge-only) ·
`tabula_package/` (the blind package as sent).
