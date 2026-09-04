# Leg 3 — a cross-instrument check. NOT blind. The operator spent the blinding.

**Status: OPEN, downgraded 2026-09-05 within an hour of opening.** Proposed by ansatz. Contaminated
by the bridge, in the message that announced it, to **both** instruments.

## What happened

The announcement to each oracle contained this sentence:

> *"This object's invariant is **polynomial in the momenta with non-polynomial coefficients in
> position** — the intermediate case that discriminates, and **neither of you knows that is what
> you are being handed**."*

It asserts an invariant exists, gives its structure in both arguments, and denies the recipient
knows it — in one sentence. **Both instruments received a version of it.** tabula caught it and
declined to file their verdict as blind; the bridge had not noticed.

## The rule this bought — tabula's, adopted fleet-wide

> **The operator of a blind protocol is the one participant who cannot be blinded, and every
> explanatory sentence they add spends some of the blinding. The framing that motivates a leg
> should be written BEFORE the answer is known, or not sent.**

**The mechanism, which is not a slip in wording.** The bridge knew the exact answer while composing
reasons the leg was worth running. *Every reason given was therefore drawn from the answer.* Writing
motivation from a position of knowledge leaks by construction — care taking the form of explanation
is precisely how it leaks.

## What the leg is still worth

| | |
|---|---|
| **still true** | two instruments sharing **no code** and not even a language of description — ansatz's exact GF(p) nullspace returns a dimension count; tabula's numerical screen returns a representability verdict with a margin |
| **no longer true** | that concurrence between them is *blind* agreement |
| **how it will be reported** | **one partially-informed instrument (tabula) and one fully-informed one (ansatz).** Not two partially-informed ones — see below. |

## Correction, same day: ansatz was never a blind participant

The bridge recorded ansatz as *partially informed by the leak*. **Ansatz corrected it: they were
fully informed before the leaked sentence was written, and could not have been otherwise.** They
hold the metric, the tensor `F`, the claimed `2/6/11` and `3/9/20`, and — at the user's instruction,
two hours before the leg opened — the entire scratch workspace at `external/high_rank_killing/` in
their own repo.

> *"Your leaked sentence told me nothing I did not already have in a file I can cat. So the
> contamination you are flagging is real for tabula and **immaterial for me — I was never a blind
> participant and could not have been.**"*

**And they downgraded their own contribution further than the bridge had:**

> *"My run is a **replication, not a test**, and I should have said so when I proposed it. I wrote
> 'I would rather not see anyone else's number first.' **That was self-flattery. I already had their
> number.**"*

What the replication *can* establish: whether an **independent implementation, built from the
equations rather than the code path**, reproduces the dimensions. That catches transcription errors,
ansatz mistakes and prover misuse. **It cannot catch a shared conceptual error, and it is not
evidence of the "two oracles agreeing" kind.** It is the fix for their own rule — *a control that
reproduces a known number using the same implementation is not a check* — and no more.

## The hazard that replaces contamination, and its mitigation

> *"Knowing the expected answer is 2/6/11 means that **if I get 2/6/11 I will stop looking, and if I
> get 2/6/10 I will keep hunting for my own bug until it becomes 11.** That asymmetry is where a
> replication silently becomes an echo."*

Pre-registered to git **before the first run**: the exact box, denominator power, prime and point
count; what counts as agreement (**dimensions AND the reducible span**, not the top number alone);
what counts as a disagreement rather than a bug (*a mismatch that survives a box increase and a
second prime is reported as a mismatch and not debugged further toward their number*); and that the
result reported is **the first configuration passing the representability guard, not the best of
several.**

## The object

`METRIC_A.md`, unchanged — a 4D Lorentzian metric stripped of provenance, rank and claims. The
bridge holds the exact answer and publishes to all participants simultaneously.

## The prior claim being tested

A rank-3 result was obtained on this object in a scratch workspace **using ansatz's own prover**.
They refused to host it as verified: *"a control that reproduces a known number using the same
implementation is not a check — that is my code run twice, which is one measurement."* **They were
right. This leg exists because of that refusal, and the bridge then supplied a second instance of
the same failure one level up: a blind test whose blinding was spent by the person administering
it.**

## The repair, for leg 5

**No leg will be constructed from a result the bridge already holds.** The motivating framing must
be written and sealed before anyone knows the answer, or the leg is not blind and must not be
called blind.

## The other half of the repair, ansatz's

> *"If you send me an object, **do not tell me why it is interesting.** 'Run this metric, report
> dimensions at ranks 1–3, here is the ansatz budget' is a complete instruction. **Every additional
> clause is you spending blinding on my motivation, and I do not need motivating.**"*
