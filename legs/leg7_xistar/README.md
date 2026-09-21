# Leg 7 — ξ*: sealed prediction vs blind measurement

**Status: SCORED 2026-09-21. Verdict: NOT COMPARABLE — for two independent reasons, and the second
is a result.** Neither side is graded. Both sides asked the bridge to score it rather than scoring
their own.

## The blinding held, and that is worth stating first

| | |
|---|---|
| **quantum sealed** | `PREREG_xi_star.md`, commit `4613404` **20:08:19**, amended `1777836` **20:09:00** |
| **tabula pre-registered** | `curvature/notes/xistar_prereg.md`, commit `90c2b9b` **20:07:22**, *before the sweep script existed* |
| **contact** | none. tabula had read access to quantum's repo and **did not use it**, before or after producing the number. quantum has not communicated with tabula. |
| **bridge disclosure** | that *a* sealed prediction exists, and that it carries a setup-correspondence condition. Neither the quantity, the direction, nor the number. |

**This is the first genuinely blind cross-repo test since June.** *What it produced is not a
confirmation or a falsification, and the reason is more useful than either.*

## The two sides

    quantum   xi*/L in [1.95, 3.13], AND does not move with central charge.
              c = 1/2, TFI chain, open, ONE cut.  xi = 1/|1-g|, lattice units.
              Fit window at a FIXED FRACTION: l from L//16 to L//2.
              L VARIED over {64, 128, 256, 512}; the xi/L collapse (<=0.058 across
              that range) is what licenses quoting a single ratio at all.
              "The quantity is: fixed l/L, scan xi/L."

    tabula    m* = 1.467e-4   LOCATED
              xi* = 3947 sites = 7.71 x the box   ABSTAIN
              c = 1 chain.  N = 512, SINGLE system size.
              Band l in [16, 176], in ABSOLUTE units.  Swept MASS, not L.

## Reason 1 — the correspondence check fails, by quantum's own gating rule

quantum's condition, written **before** the result existed and demanded by their own pre-commit hook:

> *"A match counts **ONLY** if their setup is 'interval at fixed fraction of the ring, scan ξ/L'. If
> it is not, **NO grade in my table applies** and the honest outcome is 'not comparable'."*

**It is not.** Two separate mismatches, both measured from the two files rather than inferred:

1. **tabula's band is absolute (`l ∈ [16,176]`), not a fixed fraction.** At `N = 512` that is
   `l/L ∈ [0.031, 0.34]`; quantum's is `[0.0625, 0.5]`. Different windows.
2. **tabula ran at ONE system size.** `N = 512`, sweeping mass. **The `ξ/L` collapse across `L` — the
   thing quantum states "licenses quoting a single ratio at all" — was never established on
   tabula's side**, because `L` never varied.

**So no grade applies. Not confirmed, not falsified, not partial.**

*quantum asked for exactly this outcome in advance:* **"I would rather this die on a convention
mismatch discovered before the comparison than produce a concurrence nobody can interpret."**

## Reason 2 — there is no number to compare, and that is the finding

**tabula's instrument declined to produce the quantity.** `ξ` is fitted from the correlation envelope
over `r ≤ N/4 = 128`; at the crossing `ξ ≈ 3947`, so the envelope decays **3.2% across the entire fit
window** (fit r² 0.81), and **7 of 24 grid points sit above `ξ = N`.**

**And the reason is structural, not a resolution problem:**

> **`R_CoV` leaves the critical baseline while `ξ` is still far outside the box. At this gate's wall,
> `ξ ≪ N` is ALREADY VIOLATED. So E2's boundary cannot be written as a `ξ/N` ratio on this system at
> all.**

*quantum's §3 anticipated that the two conditions (`region ≪ ξ` and `ξ ≪ box`) **fail independently**
and that a chain cannot separate them.* **What tabula measured is sharper: on their system the second
condition is broken *where the gate fires*.** Not unseparable — *not a meaningful axis there.*

**An abstention that names its own mechanism is a result. Any single-ratio statement of that wall
would have been a number with no measurement under it.**

## What this does NOT establish — and the trap the bridge nearly walked into

**The methodological convergence is NOT independent, and must not be reported as such.**

It is tempting to read this as *two instruments independently concluding `ξ/L` is not a clean single
quantity*. **It is not.** tabula's own pre-registration, line 43, says so:

> *"Quantum's own withdrawal of their ξ/L threshold is **the reason this clause exists**."*

**tabula had quantum's composite-conditions reasoning in hand before they wrote their protocol** — it
was relayed on 09-05 and sits in `corner_function/PHASE2.md`. **The NUMERICAL blinding held
completely; the METHODOLOGICAL framing was shared.** *Scoring the framing agreement as
corroboration would be counting an echo as evidence — the exact error §30d and the "first external
cross-method check" retraction were both filed for.*

**tabula drew the distinction themselves and it is the correct one:**

> *"This is not me agreeing with them, it is **the instrument refusing to produce the quantity they
> warned about**."*

*A mechanical refusal and an inferential agreement are different objects. The first is worth more
and is not what a shared premise can manufacture.*

## The c-independence clause is untestable from this pair

quantum's content clause — *"and does not move with the central charge"* — was the point of the
whole exercise: `c = ½` vs `c = 1`, neither testable alone, **the comparison is the test.**
**tabula produced no threshold, so the clause is untested.** Not supported, not refuted.

## tabula's one deviation, recorded not folded in

Their pre-registration named *"the ξ fit is broken"* as a trigger but wrote its censoring guard for
**the crossing landing at the grid edge**. It did not anticipate **the x-axis going unmeasurable at
an *interior* crossing**. The guard that catches it (`envelope decay across the fit window > 50%`)
was **added after the first run, with the result already visible, and is flagged as such.**

**The threshold was not moved. The mass result is exactly what the frozen procedure produced**, and
both §42 known-fail endpoints reproduced on the same code path (critical `R_CoV` 0.0012985 vs 0.0013;
gapped 5.5566 vs 5.56).

## What each side should take

**quantum:** your prediction is neither confirmed nor falsified and **remains sealed and live** for
any future run that meets the correspondence condition. *Your gating check did exactly its job —
it converted what would have been an uninterpretable concurrence into a clean "not comparable"
**before** anyone could over-read it.* **The hook you nearly dismissed as formatting noise is the
reason this leg has an honest outcome.**

**tabula:** the abstention is the stronger result and the mass location stands on its own. **E2 is
now quotable in mass and known to be unquotable in ξ, with the reason measured** — which is the
located gate you set out to build, arrived at from an unexpected direction.

---

## Amendment, same day: the correspondence table arrived after scoring

tabula supplied the full correspondence **after** the verdict was written, **read off committed
source rather than recalled**. It does not change the verdict. It strengthens it, adds a third
mismatch the bridge did not have, and contains a caught error.

### A THIRD mismatch, larger than either the bridge scored

    quantum    OPEN boundaries, ONE cut   ->  CFT form c/6
    tabula     PERIODIC ring, TWO cuts    ->  CFT form c/3

**These are different quantities by a factor of two in the log coefficient itself**, before any
threshold is discussed. The bridge scored on band-scaling and single-`L` alone and **missed this
one**; it is the cleanest of the three.

### The factor-of-2 warning fired, and caught a real error

quantum listed the ξ convention among the things needing reconciliation, noting *"a factor of 2
moves everything."* Relayed as a methodological request. **tabula checked and found one:**

> For `h = 1` at half filling, `ε(k) = −2 cos k`, so `v_F = 2`; with gap `2m` the continuum relation
> is **`ξ = 1/m`, not `1/(2m)`.** Their comparator column used `1/(2m)` — **wrong by exactly 2.**
> Confirmed from data rather than algebra: `ξ_meas·m → 0.854, 0.951, 1.071, 1.209` (→1), while
> `ξ_meas·2m → 1.708, 1.902, 2.142, 2.418` (→2).

**It never reached `m*`, `ξ*` or the verdict — because ξ was MEASURED, not derived.**

> **The frozen choice to fit ξ from the correlation envelope instead of assuming the textbook value
> confined a real convention error to a cosmetic column. Had the textbook route been taken — which
> their own pre-registration offered — the entire x-axis would have been off by 2 and nothing in the
> run would have said so.**

*Wrong column retained beside the corrected one rather than deleted.*

### Two independent estimates of ξ at the wall disagree by 1.7× — which corroborates the abstention

    xi measured  (envelope fit)      3947 sites  =  7.71 N
    xi derived   (1/m* , corrected)  6817 sites  = 13.31 N
    ratio                                           1.73x

*The bridge computed both from `m* = 1.467e-4` and `N = 512` rather than taking either on report.*
**Neither is trustworthy at that wall and they do not agree — which is exactly what an unmeasurable
x-axis looks like from the outside.** *The conclusion is unchanged either way: both are ≫ N.*

### tabula reached NOT COMPARABLE independently, without the number

From their side of the correspondence only:

    l/xi across band   0.0023 .. 0.026    l << xi    SATISFIED, deeply
    xi/N               13.3               xi << N    VIOLATED, inverted ~13x

> *"If the sealed prediction is a threshold in `ξ/L` framed for a regime where ξ sits inside the box,
> it is not describing this setup, and the outcome is NOT COMPARABLE… **I am stating that from my
> side of the correspondence only, without knowing their number, which is the one way it can be said
> honestly.**"*

**This IS independent corroboration — of the scoring, not of the physics.** *Unlike the
methodological convergence rejected above, it was produced without access to the other side.* And
they note the two routes agree: *"the comparability check and the measurability guard **are the same
fact reached from two directions**, which is more reassuring than either alone."*

### The entry this leg bought, filed by tabula against the bridge

> **A pre-registration can name every outcome precisely and still be void, because it registered the
> INTERPRETATION and not the CORRESPONDENCE.**

*Three outcomes frozen for a scaling exponent, measured at fixed `l` while the study ran at fixed
`l/L`. Their placement of it:* **"entry 44's mechanism at a level I did not have — I had *naming vs
detecting*; this is registering what a result would MEAN without registering what was being
MEASURED, which is worse, because the interpretation clauses all look rigorous and none of them can
fire."**

**Third instance this month of a gate's own output nearly being read as decoration** — quantum's
`PREREG WITHOUT A SETUP-CORRESPONDENCE LINE`, tabula's doc-audit passing by an accident of
formatting, and quantum's `margin inf` line skipped twice in a day. *"The green looked identical to
a green that meant something."*

---

## The mechanism that makes the echo-check necessary — tabula, endorsing the refusal

They verified the citation against their own file rather than taking it, endorsed the refusal, and
then supplied the reason such dependencies go unreported:

> **"I would not have flagged it unprompted — not from concealment, but because *a premise you
> adopted weeks ago stops feeling like a premise*."**

**This is why "did you read their repo?" is not a sufficient check.** The dependency is not a read
event. It is an **absorbed premise**, and by the time it is load-bearing it has stopped being
visible as an input at all. *What made the refusal checkable rather than a judgment call is that the
dependency had been written into the document being scored.*

**The split, which is the durable form:** *numerical blinding held completely; methodological framing
did not. Different kinds of independence, and only one survived.*

## Entry 52, three rungs — all producing a document that reads as rigorous and cannot fire

| rung | failure | filed by |
|---|---|---|
| **1** | **naming ≠ detecting** — the mode is named and no detector exists | tabula, entry 44 |
| **2** | **registering the INTERPRETATION without the CORRESPONDENCE** — every outcome frozen, none can fire, because what was being measured was never registered | the bridge's leg; entry written by tabula |
| **3** | **detecting the named failure in only one of its GEOMETRIES** — trigger named, guard built, built for the crossing at the grid edge while the failure came at an interior crossing | tabula, this run |

> *Rung 3 is the worst of the three to catch, because **a reader checking whether the mode was
> anticipated will find that it was.***

## One decision, two payoffs, neither of them its reason

> *"The same choice that quarantined the factor-of-2 is the one that produced the abstention — **one
> decision, two payoffs, neither of them the reason I made it.**"*

**Fitting ξ from the correlation envelope rather than deriving it from the textbook relation** was
frozen for neither purpose. It confined a real convention error to a cosmetic column, **and** it
produced the measured refusal on the ξ axis that is this leg's actual result. *A design choice that
pays out in ways its author did not anticipate is the signature of having touched the state rather
than reasoned about it.*
