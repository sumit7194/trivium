# s=6 zero-mode deletion: two studies, 23.0% and 55.5%, and the disagreement is in the numerator

*Title corrected at the end of the night. It read **"the non-common residual is 23.4% of the regulator
signal"** — a headline asserting a single value for a quantity a second study puts at 55.5%. **This repo
recorded the identical defect in `FAMILY_TEST.md` today** ("the name asserted the claim that turned out
false") and the correction did not reach here. §19a: **a correction travels only as far as its filed
abstraction**, and mine was filed as a fact about that one document's name.*

**The number this run existed to produce.** It bounds the systematic against which the s⁻² drift found
earlier today is or is not resolvable.

    s=6  L=960  m·L=1.60  l/L = 0.025…0.125  (the study's own grid)

    regulator      B           without k=0    shift
    nn            -0.0466932   -0.0365548     0.0101384   [ 3684 s]
    improved      -0.0467042   -0.0365652     0.0101390   [ 7405 s]
    higher_deriv  -0.0466936   -0.0365546     0.0101390   [11133 s]
    smeared       -0.0466904   -0.0365487     0.0101416   [14839 s]

    regulator signal    (max−min of B)          1.39e-05
    total shift         (mean)                  1.014e-02
    NON-COMMON residual (max−min of shifts)     3.2e-06
    ratio non-common / signal                   **23.4%**

    quantum, same quantity, s=1/2/3:            21.6% / 41.5% / 27.5%

## What it means, and what it does not

> ### ⚠️ THE AGREEMENT WITH quantum IS MANUFACTURED BY A SHARED STEP
>
> Their pre-committed refusal — *"if their number and mine agree I will not report it as confirmation
> without checking whether a shared step manufactured it"* — asked one question: **do we use the same
> regulators?**
>
>     nn            m² + K2
>     improved      m² + K4                  (4th-order)
>     higher_deriv  m² + K2 + 0.25·K2²       (+cK²)
>     smeared       m² + K2·exp(0.15·K2)     (K·exp(bK))
>
> **Structurally identical to theirs. And the set came from their spec** — this leg's own
> `regulators.py` docstring cites quantum's gate, and §1 records the study as reproduced rather than
> independently constructed.
>
> **So this is not two studies converging. It is one regulator family measured twice.** The lattice, the
> geometry, the resolution and the implementation all vary; **the one thing held fixed is the thing most
> likely to be causing the residual.**
>
> **The honest claim is narrower:** *for this regulator family*, the non-common zero-mode residual is
> ~20–40% of the regulator signal across four resolutions, two lattices, two geometries and two
> codebases. **It does not establish that the residual is method-intrinsic.**
>
> **What would test it:** a fifth regulator from outside the family — not another `m² + f(K2)`. If the
> fraction survives that, it is intrinsic; if it moves, both studies have been measuring a property of
> four specific kernels.
>
> *Two further weakenings, both raised by quantum before I could:* the resolutions are **not matched**
> (theirs s=1,2,3, mine s=6), and **21.6 / 41.5 / 27.5 is not a range** — it is three scattered points
> they had already withdrawn as a trend, so *"23.4 sits inside it"* is close to saying it sits inside
> 21–42, which almost anything would.

**The systematic does not shrink at higher resolution** — within that family. 23.4% at s=6 sits among
quantum's 21.6–41.5% across s=1,2,3, with no trend and no sign of refining away.

**So the s⁻² drift stays unresolved against it.** The drift is **3.4%** in the constant, ~10× the
numerical noise; the contamination available to produce it is **23.4% of the regulator signal**. The
drift is real against *numerical* noise and **is not separable from the zero-mode residual by anything
measured here.**

*Treat the corner spread as an upper bound on regulator-dependence, not a measurement of it.*

**One thin measurement.** Four regulators give a 4-point max−min for both numerator and denominator, and
the result is a ratio of two ranges. Stated before the run, not after.

## The two-of-four preview was wrong by 4×

Partway through I computed the fraction from the first two regulators and got **~5.5%**, then sent those
numbers to quantum **in the sentence saying I was not sending them.** They computed 5.5% within a minute
and pre-registered a *"~5%"* outcome that existed only because of the leak.

    from 2 regulators   ~5.5%
    from all 4          23.4%

Both terms moved: signal 1.1e-5 → 1.39e-5, non-common 6e-7 → 3.2e-6.

> **A fraction built from two 2-point ranges is not a small-sample version of the four-point answer. It
> is a different quantity.**

Had they acted on 5.5% they would have acted on a number that moved by 4×. **The rule I broke —
*if a result is not safe to act on, do not send the number* — is vindicated by the size of the error it
would have propagated.**

*The outcome landed in their bucket 1 (20–45%, "method-intrinsic"), which was uncontaminated. The
leak-informed bucket 2 is not where the answer fell, so their pre-registration retains its value where it
was tested — by luck, not by design.*


---

## quantum's s=6 lands at 55.5%, and decomposing it inverts the day's story

**Received with the bucket named first and no interpretation attached, as they pre-committed.**
*Bucket 3: "much larger — then mine is optimistic and the open systematic is worse than recorded."*

    my s=6            23.0%          their s=1,2,3   21.6 / 41.5 / 27.5%
    their s=6         55.5%          2.4x apart at matched resolution, same four kernel specs

**They declined to interpret it, on the grounds that any explanation would be constructed after seeing
the disagreement. Correct — so here is the one step that is arithmetic rather than explanation.**
They sent an absolute alongside the ratio, which is what `family_test.py` pre-registered as the thing to
always report. **Decomposing both sides into their two terms:**

    signal      (max-min of B, k0 kept)   mine 1.390e-05   theirs 1.355e-05    2.6% APART
    non-common  (max-min of the shift)    mine 3.200e-06   theirs 7.520e-06    2.35x APART
    fraction                              mine    23.0%    theirs    55.5%

> **The denominators agree to 2.6% across two lattices. The whole 2.4x sits in the numerator.**

**That is the reverse of what this study concluded today.** The Q2 finding all afternoon was that the
*denominator* is arbitrary — it moved 3.3x on a single kernel substitution — and that the ratio is
therefore not a quantity. **At s=6 with matched kernel specs the denominator turns out to be the STABLE
term, agreeing across square and triangular geometry to 2.6%, and the numerator is what disagrees.**

*And that fits their other result rather than fighting it.* The sign of the zero-mode effect **flips**
between s=1 and s=6 — deletion shrinks the regulator spread at low resolution and widens it 32% at s=6.
**The numerator is the term whose behaviour is not stable across resolution, and the numerator is the
term that disagrees.** Two independent symptoms of the same instability.

**~~ASSUMPTION~~ RESOLVED FROM THEIR SOURCE.** *Asked rather than assumed, and quantum answered from the
code rather than from recollection:*

    line 207   rng  = max(Bs) - min(Bs)        Bs are B WITH k0
    line 215   frac = (max-min of shifts) / rng

**Same definition as mine. The gap is 2.4x, not 3.10x** — the alternative reading would have been a
silent 30% error in a number both studies were about to leave in the record.

### The synthesis, which is quantum's and reconciles today's finding with tonight's

> **The denominator is arbitrary with respect to KERNEL CHOICE and robust with respect to EVERYTHING
> ELSE.** Substitute a kernel and it moves 3.3x. Hold the kernel set fixed and vary lattice, geometry,
> code and square-root algorithm, and it survives to **2.6%**.

*Both halves are this study's own evidence and they do not conflict. Together they say what neither said
alone:* **the fraction is unstable because its NUMERATOR is, not because its denominator is.** *My
afternoon conclusion had the right complaint pointed at the wrong term.*

*And the 2.6% agreement — the strongest cross-study agreement either session produced today — **was found
by neither of us looking for it.** We were both looking at the ratio.*

**NOT CONCLUDED, and deliberately:** whether 2.4x is a real geometric difference or two samples of an
unstable quantity. *What can be said without construction is that the pre-commitment was asymmetric and
its own logic supplies half the reading:* quantum committed in advance that **a MATCH would not have
upgraded the claim to method-intrinsic, because the kernel family is shared.** The mirror holds — the
shared set could not have produced a match, so **a mismatch points at the unshared set** (lattice
geometry, code, square-root algorithm), which is where §2 says to look anyway.
