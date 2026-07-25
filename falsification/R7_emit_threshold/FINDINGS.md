# R7 — Findings: O4 is a REAL obstruction. M6's same-day assertion was wrong, and is amended.

*Run 2026-07-26; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2+,
Tier R. Prescribed by [A2](../A2_wall_audit/FINDINGS.md)'s taxonomy as a species-1 wall crossing — "upgrade
the instrument." **The upgrade was run as a test rather than assumed, and it failed the decisive gate.***

## Result in one line

**Postulate FALSE.** [M6](../M6_prior_art_gate/FINDINGS.md) asserted this morning — *from reading the
literature, not from running anything* — that O4 "is not an obstruction we discovered, it is our fixed
τ = 1e-6 being the wrong kind of threshold," and that a noise-calibrated cutoff would "dissolve it rather
than guard against it." **It does not.** The degree-6 false positive sails through the noise-calibrated
cutoff by a factor of **28×**. O4 is a real property of the method, the hand-set threshold was **not** the
defect, and **the held-out guard — not any threshold — is the operative defence.**

## The data

| library | σ_min | ε (measured) | σ_cutoff (O&E) | OLD emit (τ=1e-6) | **NEW emit** |
|---|---|---|---|---|---|
| harmonic poly2 | 4.71e-15 | 4.0e-10 | 1.33e-04 | True | **True** ✅ |
| pendulum poly2 | 1.24e-01 | 1.0e-10 | 5.33e-05 | False | **False** ✅ |
| pendulum poly4 | 3.36e-03 | 2.4e-10 | 1.58e-04 | False | **False** ✅ |
| **pendulum poly6** | **1.07e-05** | 3.8e-10 | **2.99e-04** | **True** (the O4 false positive) | **True** ❌ |
| pendulum poly4+cos | 3.80e-11 | 2.4e-10 | 1.63e-04 | True | **True** ✅ |

| gate | result |
|---|---|
| **R7a** — upgrade must not break true positives | **PASS** — harmonic and poly4+cos both still emit |
| **R7b** — noise-calibrated cutoff must reject O4 | **FAIL** — σ_min 1.07e-5 vs cutoff 2.99e-4; emits anyway |
| **R7c** — spectral gap must select poly4+cos | **FAIL** — selects poly2 (see caveat below) |
| **R7d** — held-out guard must separate them | **PASS** — poly4+cos 8.76e-11 held-out; poly6 degrades **684×** |

## Why the threshold could never have worked — the mechanism

This is the part worth keeping, and it explains the failure rather than just recording it.

**O4 is not a noise problem.** Look at the numbers: the degree-6 arm's σ_min is **1.07×10⁻⁵**, while the
measured perturbation ε is **3.8×10⁻¹⁰** — the false-positive signal sits **five orders of magnitude above
the noise floor.** It is not noise being mistaken for structure. It is a rich basis genuinely fitting the
transcendental invariant well over the sampled region.

So *any* criterion of the form "is σ_min small enough?" is asking the wrong question. It cannot separate

- **small because a true invariant lies in the span** (representation), from
- **small because a rich basis approximates one that doesn't** (approximation),

because both produce a genuinely small σ_min on the sampled data. **The distinction is not visible in-sample
at all.** Only **generalisation** exposes it — which is exactly why R7d works: the approximation degrades
**684×** on orbits it was not fitted to, while the true representation stays at 8.76×10⁻¹¹.

There is also a regime effect worth stating precisely, because it partly excuses O&E's formula: their cutoff
is `√(Np)·ε^{2/3}`, and for tiny ε the exponent ⅔ **inflates** enormously (ε = 3.8e-10 → ε^{2/3} = 5.2e-7),
then √(Np) = 569 inflates again — giving a cutoff ~10⁶× the actual noise level. In a genuinely noisy setting
that is the right calibration. In our near-noiseless synthetic setting it is **far more permissive than our
hand-set τ**, which is why the upgrade made O4 *easier* to pass, not harder. **My pre-registration flagged
this exact risk** ("a stand-in for a setting the formula was not designed for") — and the risk materialised.

## R7c's failure is probably mine, not theirs — recorded conservatively

The spectral-gap criterion picked **poly2**, the worst library. But poly2's large gap (0.60) is a gap between
*non-null* singular values — it reflects a well-conditioned library with no near-null direction at all, not
evidence of an invariant. O&E almost certainly intend the criterion to rank among libraries that **already
produce a near-null σ**, which my flat implementation does not enforce.

Following A2's own conservative-default spirit: **this is recorded as a failure of my realisation, not of
their criterion.** R7c is scored FAIL for our instrument; no claim is made against
[arXiv:2403.04889](https://arxiv.org/abs/2403.04889).

## What this does to M6 — amendment required

[M6's FINDINGS](../M6_prior_art_gate/FINDINGS.md) said, in two places, that the threshold was the defect and
the cutoff would dissolve the trap. **Both statements are wrong and are amended.** What survives of M6 is
untouched and is the larger part:

- **Still true:** the emit⟺span statement is prior art (O&E's trichotomy, on the same instrument), O4's
  *phenomenon* is known to the literature (Ray 2026 targets it), and **M6 stays KILLED**. Nothing here
  revives a publication claim.
- **Now false:** "O4 is not an obstruction we discovered — it is our threshold being the wrong kind."
- **Now correct:** O4 *is* a genuine obstruction of the method, and the literature's answer to it is not a
  better threshold but exactly what Ray 2026 built — a **constancy gate plus diversity filter**, i.e. a
  generalisation test. tabula's held-out-by-construction harness (§161) was right for the right reason.

The error's shape is worth naming: **I asserted a mechanism from reading, and shipped it in a FINDINGS the
same day, without running the one experiment that would test it.** R7 exists because the assertion was
cheap to check and I had not checked it. Three of today's four documents were correct; this was the one that
was not, and it was the one with no measurement behind it.

## Correction owed to tabula (the second today)

I advised them this morning to move off `τ = 1e-6` to a noise-calibrated cutoff, on the grounds that "the
threshold is the problem." **That advice was wrong** and should not be acted on for this failure mode: on
our reproduction the noise-calibrated cutoff is *more* permissive and lets O4 through by 28×. Their existing
**held-out-by-construction harness is the correct defence and should be kept as the primary gate.** The
noise-calibrated cutoff remains worth having for genuinely noisy data — a different problem from O4.

## Honest scope

- **Zero novelty.** All three upgrades are other people's. R7 only decides which of *our* two stories about
  O4 was right, and the answer is: the one we had before this morning.
- **One system, one false-positive arm.** R7d passing does not prove held-out scoring is universally
  sufficient — it proves it handles the case that broke us, with a 684× margin.
- The ε-by-step-halving construction is a stand-in for a formula designed for noisy data. **No claim is made
  that O&E's cutoff fails in its intended regime**; the claim is that it does not address O4, which is not a
  noise phenomenon.
- Bridge-solo; reuses R2's orbit setup and code verbatim so O4 is reproduced, not re-created; numpy only.

## Inputs & artifacts

`code/r7_threshold.py` · `results/r7_threshold.json`. Reuses
[R2's engine](../R2_emit_theorem/code/emit_reproduce.py). Amends
[M6](../M6_prior_art_gate/FINDINGS.md); adopted upgrade (held-out guard) belongs in any future emit run.
