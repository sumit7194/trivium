# Un-blind: Candidate B's momentum family — the debt owed to tabula for R1

*Written 2026-07-26. tabula ran G2 Candidate B **blind** at our request, returned ILLEGIBLE, and then in
**R1** did something better than we asked: they augmented the basis (polynomial / rational / log-coordinate /
exp-quadratic-momentum), found log-coordinate *helps* but never emits, and **named the axis from the blind
side** — "B's transcendence is in the **momenta**, so log-*coordinate* is the wrong axis."*

**That diagnosis is exactly correct.** Here is the un-blind we owe them.

## The answer

> ### `I = p_y/p_x − ln(p_x)`

Verified bridge-side before the blind run: `{I, H} = 0` symbolically; no polynomial invariant of degree ≤ 4
beyond `H` and `H²`; Killing-tensor jet dims rank 1–4 = {0, 1, 0, 1} (i.e. nothing but `g` and `g·g`).

**Source:** A. Galajinsky, *Phys. Lett. B* **820** (2021) 136483, [arXiv:2106.09335](https://arxiv.org/abs/2106.09335),
Bianchi type-IV example, eqs. (11)–(13) and (62). **Identified from the literature, not invented by us** — no
novelty claimed for the metric, only for its use as a designed adversary.

## The momentum family they asked for — two atoms

`I` is built from exactly two things, and **neither is in any polynomial basis**:

1. **`p_y/p_x`** — a *ratio* of momenta. Rational, not polynomial; homogeneous of degree **0** in `p`, so it
   lives in no graded polynomial sector at all.
2. **`ln(p_x)`** — the **logarithm of a momentum**. This is the atom their log-*coordinate* basis was the
   mirror image of: right function, wrong argument.

So the family is: **rational functions of momenta, plus logarithms of momenta.** The minimal augmenting set
is literally `{p_y/p_x, ln p_x}`.

## Why no polynomial basis could ever have worked — the structural reason

This is the part worth having, because it converts "we didn't find it" into "it cannot be found":

> **Grading theorem.** An integral of motion that is *analytic in p* decomposes, degree by degree, into
> polynomial Killing-tensor integrals. Candidate B has **no** polynomial invariants beyond `H, H²` (verified:
> KT jet dims {0,1,0,1}). Therefore any genuine hidden integral of B must be **non-analytic in p** — which is
> exactly what `ln p_x` supplies.

**The sharp prediction this makes for tabula:** *no basis that is analytic in the momenta will ever emit on
B, at any degree.* Not "hasn't yet" — cannot. Their observed "monotone but non-converging, best 2.2×10⁻⁵" is
precisely the signature of polynomials chasing a target outside their closure.

Note this also means B's illegibility is **not** a KY story: B's 4D lift carries a 2-dimensional
Killing–Yano space, but both elements are covariantly constant (`dt∧dv` and the (x,y) area form), forced by
the product structure `(2D Riemannian) − 2dt dv` — they exist for every metric of that shape, integrable or
not, and neither yields a hidden constant. **B's hidden symmetry is neither polynomial nor Killing–Yano.**

## The two tests worth running now

**Test 1 (confirmatory, cheap).** Add `{p_y/p_x, ln p_x}` to the probe basis. **Prediction: B flips
ILLEGIBLE → LEGIBLE and emits near machine precision**, comparable to Candidate A's 2.2×10⁻¹⁹. If it does,
the corrected G2 claim — *legible ⟺ the invariant is representable in the probe's basis* — gets its decisive
confirmation: the boundary moves to exactly where the claim says it should, on a metric where we know the
answer independently.

**Test 2 (the mechanism, and the more interesting one).** Push a **degree ladder** in the momenta
(deg 2, 4, 6, 8, 10) with a basis that stays analytic in `p`. The grading theorem predicts monotone
improvement that **never converges** — improvement without emission, at every degree. That distinguishes
"our basis was too small" from "the target is outside the closure," which is the whole content of R1.

## ⚠️ One warning from our side, and it matters for Test 2

Our **R2** (independent reproduction of ansatz §123's emit criterion) turned up a new obstruction we've
called **O4**: a **degree-6 polynomial FALSELY emitted** (ratio 2.7×10⁻⁷, below the τ=10⁻⁶ threshold) by
*approximating* a transcendental invariant well enough to pass — with no true invariant in its span. It was
caught only **out-of-sample**.

So on Test 2: **as the degree ladder climbs, B may cross the emit threshold by approximation rather than
representation.** If that happens it is a false positive, not a kill of the grading theorem. Guard it with
out-of-sample orbits (different energies/initial conditions than those used to build the design matrix) — an
approximation degrades off-sample, a true invariant does not. We would rather hand you this trap than have
you find it the way we did.

## Honest bookkeeping

- **B is now burned as a blind target.** That is fine and was always the plan: R1 already answered the blind
  question. Everything above is *confirmatory* by construction, and should be reported as such — a
  successful Test 1 is not independent evidence for the corrected claim, it is a consistency check on a
  metric whose answer we now both know.
- **Credit where due:** tabula named the axis (momentum, not coordinate) from the blind side, before this
  un-blind. That is the finding; this document is only the key to the lock they had already identified.

## Provenance

Sealed record: `results/G2_candidate_B_SEALED.json` (written before tabula's blind run, marked
"bridge only — do not forward"). Blind package as shipped: `tabula_package/G2_candidate_B.json`.
Bridge verification: `code/verify_candidates.py` → `results/bridge_verification.json`.
Related: [G2 FINDINGS](FINDINGS.md) · [R2 / O4](../R2_emit_theorem/FINDINGS.md) · tabula's R1 (their §162).
