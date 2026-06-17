# Leg 3 — Findings: the spine closes — "how many numbers is a black hole?"

*Run 2026-06-17. Predictions and criteria frozen in [PREREGISTRATION.md](PREREGISTRATION.md)
before the measured-DOF computation.*

## Result in one line

All three independent epistemologies return **2**: ansatz **proves** the moduli count is
2, tabula **inferred** 2 from observations (leg 1), and deepstrain's **measured** no-hair
δ is consistent with 2 (no third number resolved). The spine triangulates.

## The §5 count-triangle

| Oracle | how it knows | count | basis |
|---|---|---|---|
| **ansatz** | proves (exact) | **2** | Kerr 2-parameter; scalar no-hair proved (`32`/`33`); charge = 1 number, electric≡magnetic (`34`) |
| **tabula** | infers (neural) | **2** | RN observable manifold intrinsic dim = 2 (leg 1); dyonic degeneracy showed observable ≤ algebraic |
| **deepstrain** | measures (real data) | **2** | GW250114 no-hair δ = **−0.16 [−0.46, +0.33]** 90%; δ=0 inside CI; σ(δ)≈0.24 |

- **C1 (measurement consistent with DOF = 2): TRUE.** δ=0 sits well inside the 90% CI.
  Savage–Dickey density ratio BF(2-number : 3-number) = **2.6** (prior δ∼U[−1,1]) / **1.3**
  (prior U[−0.5,0.5]) — a weak-to-moderate Bayesian preference for *exactly two numbers*;
  the prior-free statement is that any third number (a hair) is constrained to σ(δ)≈0.24.
- **C2 (the triangle closes — all three = 2): TRUE.**

See `results/leg3_nohair_delta.png`: δ=0 (the 2-number / Kerr point) sits comfortably
inside the measured posterior — no hair is resolved.

## What is and isn't claimed (the honest core)

**The genuine result** is a *triangulation of the count*: three methods that never saw
each other's answer — deductive proof, inductive representation-learning, empirical
measurement on real LVK strain — concur that a black hole is a **2-number object**. A
claim that survives all three independent routes is confirmed in a way that is hard to get
(THE_BRIDGE.md §6, the triangulation lens).

**The family caveat (registered up front, not discovered after).** The three legs do not
all probe the *same* black hole:
- tabula's leg-1 count was on the **charged-static** family `(M, Q)`;
- deepstrain's δ is on the **rotating-vacuum** family `(M, χ)`;
- ansatz proves *both* are 2-parameter.

So the concurrence is on the **number 2**, across independent methods *and* across two
different 2-parameter black-hole families — not on a single shared object. Stated this
way it is honest and still strong; stated as "all three measured the same hole" it would
be overclaiming (§7).

**No new physics.** No-hair, QNM spectroscopy, and the Kerr moduli count are textbook /
established-active. The contribution is the **method + the unusual end-to-end ownership +
the three-way cross-validation**, framed honestly (§7). deepstrain's δ is a clean
independent re-analysis, not a frontier no-hair claim (LVK does that).

## A through-line worth recording

Leg 1 found that the *observable* count can fall **below** the *algebraic* count (dyonic:
3 algebraic moduli, 2 observable, because `Q²+P²` is a degeneracy). Leg 3's no-hair test
is the empirical face of the same question — "is there a number beyond the obvious ones?"
— and finds **no** extra number for the astrophysical hole (δ≈0). Both legs are instances
of one principle: **the number of numbers you can resolve is a measured/derived quantity,
not an assumption**, and for the astrophysical black hole every method resolves 2.

## Honest limits

- **δ posterior approximated as Gaussian** from its published 90% interval (median −0.16,
  CI [−0.46, +0.33]); the Savage–Dickey BF is therefore approximate and prior-dependent
  (reported with a prior sensitivity). The primary empirical statement is prior-free
  (δ=0 in CI, σ(δ)≈0.24).
- **Single event.** GW250114 only; multi-event stacking would sharpen σ(δ) (deepstrain's
  own noted v2 direction).
- **ansatz has no QNM module**, so there is no *numeric* ansatz→deepstrain bridge (e.g.
  exact Kerr 221 vs the fitted overtone); the link is at the level of the proposition and
  the count, as the doc's §4C "proof ↔ test" intends.
- The family caveat above bounds the "same object" reading.

## Artifacts
- `code/measured_dof.py` — Savage–Dickey BF from deepstrain's δ posterior (read-only) +
  the assembled count-triangle.
- `results/measured_dof.json`, `results/leg3_nohair_delta.png`.
