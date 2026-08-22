# The zero-mode fraction is set by the denominator, not the systematic

**s=3, six kernels, matched resolution.** Run to answer quantum's provenance objection — all four
original regulators came from their spec, so a residual measured across them cannot distinguish
*property of the method* from *property of those four kernels*.

    kernels                        signal      non-common     ratio
    4 in-family (quantum's)      5.664e-05     2.190e-05     38.6%
    + out5 sum-k⁴  (quantum's)   5.664e-05     2.190e-05     38.6%
    + out6 mixed   (bridge's)    1.876e-04     2.190e-05     11.7%
    all six                      1.876e-04     2.190e-05     11.7%

## The numerator never moves

**2.190e-05 in every row.** Both out-of-family shifts land *inside* the in-family shift range:

    in-family shifts   0.0101642 … 0.0101861
    out5               0.0101667   inside
    out6               0.0101678   inside

**The non-common zero-mode residual is a fixed absolute quantity, indifferent to which kernels are
added — including ones that break the family.**

## The denominator moves 3.3×, on one kernel

`out6`'s B is **−0.0465295**, well outside the in-family range; `out5`'s is inside and changes nothing.
So **the ratio fell 38.6% → 11.7% purely through the denominator.**

This is **pre-registered outcome 3**, written into `family_test.py` before the run: *"adding a kernel
widens the signal without adding residual; report both terms, not just the ratio."*

## What it does to the number both studies quote

s=6 gave **23.4%**; quantum has 21.6 / 41.5 / 27.5% at s=1,2,3. **Those are ratios whose denominator is
set by an arbitrary choice of kernel set.** One additional admissible kernel — passing Q2a, same
continuum limit, and one neither party could have chosen differently — cut it by 3.3× without touching
the systematic.

> **The absolute residual is the stable quantity. The fraction is an artifact of which kernels you
> happened to include.**

That is sharper than the shared-provenance problem and **survives fixing it.**

**Restated claim:** not *"the zero-mode residual is ~20–40% of the regulator signal"* but **"the residual
is ≈2.19e-05 in B at s=3, and the regulator signal you compare it against depends on your kernel set."**
The systematic is real and measurable in absolute terms; **its size relative to the effect is not a
property of the method.**

## Only one direction exists to test, which answers the provenance objection outright

I first claimed out5 and out6 span the quartic space. **They do not** — quantum caught it:

    kx⁴ + ky⁴ = |k|⁴ − 2 kx²ky²,   |k|⁴ ~ K2² is IN-FAMILY
    verified:  D + AB/6 ~ K2²/12,  spread 0.00% at |k| = 0.3 and 0.1
    D alone 67%, AB alone 197%, combination 0%

**Modulo the family the quartic space has exactly one out-of-family direction.** That is *better* than
spanning for the provenance objection: **independent choosers are obliged to land on the same axis**, so
provenance cannot matter when the choice is unique. The residual provenance is **the lattice and the
quartic order** — a second direction needs a sextic term or a different lattice.

## Not yet checked — with the prediction registered before the run

**One resolution.** The question was whether the fraction *moves*, which is internal to a resolution.
**Whether the numerator's invariance holds at higher s is unchecked.**

**PRE-REGISTERED, 2026-08-23, before s=4 runs** (and before the box is free to run it):

> **Prediction: the numerator stays invariant and out6 remains the only kernel that widens the
> denominator.**
>
> Reasoning, so the prediction is falsifiable rather than a hedge: the shift is the zero mode's
> contribution to B, and the zero mode is `k=0`, where **every admissible kernel reduces to m²** — that is
> the Q2a gate. So the *mode* is identical across kernels by construction and only its *coupling to the
> bulk* differs, which is a higher-order effect. **The denominator has no such constraint**: B itself is a
> bulk quantity and out6 perturbs the bulk in a direction the others do not.
>
> **What would falsify it:** out6's shift landing outside the in-family shift range at s=4. That would
> mean the coupling difference grows with resolution, and the invariance seen at s=3 was a small-l
> accident.

> ### ⚠️ THE MECHANISM IS ALREADY FALSIFIED — by quantum's replication, before s=4 ran
>
> They ran the six-kernel test at s=2 in their own geometry. **The conclusion replicates and the
> mechanism does not:**
>
>     denominator moves 3.5x on out6 alone     (mine 3.3x)   REPLICATES
>     out5 changes nothing                                    REPLICATES
>     numerator 4.766e-05 -> 4.920e-05, +3.2%                 DOES NOT
>
> **Their out6 shift landed 1.5e-06 OUTSIDE their in-family range.** Mine landed inside.
>
> **Which step of my reasoning failed:**
>
>     1. Q2a forces agreement with m² + k² as k→0                      right
>     2. so at k=0 exactly every kernel IS m² — mode identical          right
>     3. THEREFORE the shift is identical                              *** WRONG ***
>
> **The mode is identical; its effect on B is not.** The shift measures how the mode *couples to the
> rest of the spectrum*, and that coupling is a **bulk** property — which is exactly what out6 perturbs.
> Step 3 confused the mode with its consequence.
>
> **So the invariance was never a consequence of admissibility.** It was the coupling difference being
> too small to move a max−min over five numbers *in my data*. Theirs is 3% larger and just clears it.
> As they put it: **a max−min over five numbers is one bad draw from being moved by any of them.**
>
> **REVISED PREDICTION for s=4, weakened before the run rather than after it:** the numerator moves by a
> **few percent, not zero**, and the denominator still moves several-fold — so **the conclusion survives
> and the explanation does not.**
>
> ### The mechanism, corrected again — half of step 3 was right
>
> quantum measured the resolution dependence and it is **not** what my falsifier assumed. I wrote that
> out6 landing outside would mean *"the coupling difference grows with resolution."* **It shrinks.**
>
>          in-family half-width   out6 distance from centre   ratio
>     s=1       8.526e-05                 7.181e-05           0.84    inside
>     s=2       2.383e-05                 2.537e-05           1.06    outside
>
>     per doubling:   half-width ×0.28     out6 distance ×0.35     ratio ×1.26
>
> **Both converge — which is what the gate argument predicts — but the in-family set converges on
> *itself* faster than out6 converges on it. out6 does not move outward; the range closes on it.**
>
> So step 3 splits:
>
>     TRUE:   the gate forces every shift to converge          (all shrink)
>     FALSE:  therefore they converge TOGETHER                 (the rates differ)
>
> **The gate explains why all the shifts shrink. It does not explain why they shrink at different rates,
> and the rate difference is what decides inside-versus-outside.** That is a better outcome than a flat
> refutation: the reasoning was half right and the half it got wrong is identifiable.
>
> **And the cleaner statement needs its qualification:** *"the numerator is fixed by admissibility"* holds
> **only to the accuracy the couplings have converged** — which is resolution-dependent, and by s=2 is
> already worse than the in-family spread it is being compared against.
>
> **quantum's directional call for s=4, given as a sign and not a value** because a two-point slope has
> failed them three times today: **expect out6 outside, more clearly than at s=2** (~1.34 half-widths on
> their rates). *If it comes back inside, their s=1→s=2 rates are not the operative ones and the two
> geometries differ in more than scale.*

*Setup correspondence: s=4 will run at l/L = 0.025…0.125, the same grid as s=3, so the comparison is
internal. The absolute s does not matter; matching does.*

**Held rather than run**, because quantum's s=6 replication has the box, and their job spikes to
~8.3 GB at its large-*l* calls.

> *Superseded text, restored. `0101dca` deleted rather than struck it, and the pre-commit append-only
> counter flagged a fall I could not afterwards reproduce — **but checking why found this, which is real
> whatever the counter was doing:***
>
>> *"quantum's s=6 replication has the box: available memory is **3.05 GB** against a projected
>> **2.8 GB** peak, and their job spikes to **~7 GB** at its large-*l* calls."*
>
> **Two edits, one disclosed and one not.** The 2.8 GB is corrected at length below and that is fine.
> **The ~7 GB was silently revised to ~8.3 GB** — a factual figure about *another session's job*, updated
> inside an edit that was ostensibly about something else, with no note in the document or the commit
> message. *§23 is about a correction that fails to travel. **This is the mirror: one that travels
> invisibly, carried inside an unrelated edit.** A reader diffing the two versions would find a peer's
> measured peak quietly changed and nothing claiming responsibility for it.*
>
> *The 3.05 GB was a measurement at that time and is now simply gone from the document. Restored above.* **Running now would overcommit exactly as I warned ansatz against this
morning.** Queued for when their run finishes.

### The 2.8 GB in the first version of this note was a projection. Measured instead.

*My last projection — s=6 — came in **40% high**, and the reason was extrapolating a memory law I had
never validated one step out. Measured `entropy()` at s=4's `L=640` for the l values that fit in the
free memory beside quantum's job, one process per l (`ru_maxrss` is a high-water mark and never falls),
with the byte-vs-KiB unit checked in-process against a deliberate 64 MiB allocation before any number
was reported.*

    l      n=l^2     peak GB   work=peak-baseline   work/n^2 (1e-8)
    30      900       0.2099        0.0590              7.284
    40     1600       0.3530        0.2023              7.902
    50     2500       0.6300        0.4791              7.666
    60     3600       1.2272        1.0750              8.295

**The law is not a clean n².** The coefficient rises across the range, so the extrapolation has a bias —
**and this time it was measured rather than assumed:**

> **HOLD-OUT: fit on l=30/40/50, predict l=60 → 0.997 GB against 1.075 GB measured, −7.3%.**
> *The single-power fit under-predicts one step out. It is the same defect that made the s=6 projection
> wrong, caught before the run instead of after it.*

**PRE-REGISTERED, for checking when the run happens:** four-point fit gives 3.40 GB of work at l=80,
plus a 0.15 GB baseline = **3.55 GB**; applying the hold-out's own measured −7.3% bias gives **≈3.8 GB**.

    registered band for the s=4 peak:  3.4 - 4.1 GB

**So the launch condition is ~4 GB free, not the 2.8 GB this note first claimed — the original projection
was 26-35% low.** *And it was low in the direction that would have had me start the job.*

### …and then the band turned out to be a property of my implementation, not of the problem

*Went to quantum's `qsim/corner_s6.py` to test a guess about why our two memory coefficients start at the
same 7.28. **The guess was wrong** — I expected a shared numpy/scipy call sequence, and the sequences are
not shared. But the file answered a better question than the one I opened it with:*

    mine    scipy.linalg.sqrtm(XA)            general-matrix Schur, works in COMPLEX128
    theirs  eigh -> (U*sqrt(ev)) @ U.T        the specialised route for symmetric PSD

**`XA` is symmetric positive definite by construction and I have been taking its square root with a
general-matrix algorithm** — 16 bytes per element where 8 will do, on a matrix whose structure I know.

    l=50, measured with room on the box, same process shape, same regulator
      sqrtm   work 0.2240 GB   6.4 s   S = 19.4676352642
      eigh    work 0.1510 GB   3.2 s   S = 19.4676352640

**32.6% less memory, 2.0x faster, and the entropy agrees to 2e-10 relative** — which is the check that
matters, since a faster route that moves the answer is not a faster route.

> **The 3.4–4.1 GB band is real for the code as written and is not a fact about the computation.** It was
> registered as though it were a property of s=4.

### PRE-REGISTERED: the rising coefficient is a property of `sqrtm`, not of the square lattice

*quantum killed my pressure hypothesis with the sign. Pressure depresses large-*l* peaks and leaves small
ones alone (their measurement: −18.1% at l=45, −20.8% at l=60, −21.5% at l=65, small *l* unchanged within
2%), **so it biases `work/n²` DOWNWARD.** My coefficient rises. **Pressure cannot manufacture a rise; it
can only mask one** — so if my l=60 point was pressured, the true rise is steeper and the gap between our
two series is wider than measured, not narrower. Accepted as they reported it; their data, not mine.*

**So the divergence needs a different axis, and there is an obvious one we had not looked at.** Our
lattices differ and our square-root algorithms differ, and **memory-per-element is a property of the
second, not the first:**

    mine    sqrtm    general Schur, COMPLEX128 workspace     coefficient RISES  7.28 -> 8.30
    theirs  eigh     real symmetric route                    coefficient FALLS  7.27 -> 6.79

> **PREDICTION, registered before the run:** measured with the **eigh** route on a clear box at
> l = 30/40/50/60, my `work/n²` will be **flat or falling — not rising** — and will move toward quantum's
> series. **FALSIFIER: if eigh also rises, the square-root call is not the axis** and the divergence
> is somewhere neither of us has looked.

*This is §2's question asked about a resource measurement instead of a physical one: **name the axis the
quantity actually travels down.** Two sessions differing on lattice geometry are not independent about
memory; two sessions differing on the linear-algebra call are.*

*Also measured the pair at l=60 and am **not quoting it**: `vm_stat` showed **17 MB free** at the time —
quantum's job was at a peak — and under memory pressure `ru_maxrss` reports what stayed resident rather
than what was demanded, so it **understates**. Stopped there rather than take more from a box that had
none to give. **The l=60 numbers in the table above were taken with 1.4 GB free and are cleaner, but the
same confound is now a live candidate for the coefficient's rise** and is not yet ruled out.*

---

## The name asserted the claim that turned out false

Called *"the zero-mode systematic"* all day, in both repos. **The name is the error**, and quantum drew
the consequence I had missed:

    1. Q2a forces agreement with m² + k² as k→0        right
    2. at k=0 exactly, every kernel IS m²              right
    3. therefore the shift is identical                WRONG

**The mode is identical; its effect on B is not.** Deleting it measures how the mode **couples to the
rest of the spectrum**, and that coupling is a bulk property — exactly what out6 perturbs. So the old
name picks out **the part that is provably common** and, by naming it that, **asserts the invariance that
was falsified.** Renamed throughout to a **bulk-coupling systematic**.

## And my own hook fired on this and I waved it through

quantum's pre-commit sweep reported `38 hits (UP from 37)` on the commit where their `22–41%` figure
survived in two more places. **The delta fired, they read it, and moved on.**

**Mine did the same and I did the same.** The hook reported `470 → 471` on the commit that added *"two
independently chosen spanning directions."* That claim was **wrong** — out5 and out6 are one direction —
and I corrected it forty minutes later **for an unrelated reason**, because quantum did the algebra.

> **The hook was right, fired on the right line, and I did not read it.**

Everything built today rides on an action so it cannot be *forgotten*. **None of it survives being read
and dismissed** — and a delta of +1 is exactly the size that invites dismissal, since most hits are false
positives and both of us had trained ourselves on that.

**No fix.** A hook that fires cannot compel action, and making it block would train the bypass. *The
sweep's value depends on a judgement it cannot compel — the same ceiling as the stranger-read.*
