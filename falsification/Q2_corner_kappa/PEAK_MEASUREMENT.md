# What s=6 actually costs — measured, not projected

## Why this was measured at all

The s=6 decision was about to rest on **~7.2 GB**, obtained by scaling s=5's remembered "~5 GB" by
(L/800)². ansatz had just cancelled their rank-4 rung after discovering their published 4.75 GiB/prime
was a real measurement of the **wrong phase** — correct about the rank step, silent about the assembly
that preceded and dominated it, by 8×. That projection and mine were the same kind of object.

So: one regulator, RSS sampled every 0.25 s, recording the high-water mark **and the phase it occurs
in**. Calibrated on s=5, where the answer was already known — *a probe that cannot reproduce a known
answer cannot be trusted on an unknown one.*

## Result

    TRUE PEAK 5.92 GB, reached during: entropy l=100

Three things the projection had wrong:

**The remembered figure was low.** "~5 GB" was really **5.92 GB**, and the run drove genuinely-free
memory to **0.09 GB**.

**The peak is not in the correlators.** They finish in under a second at **0.05 GB**. The entire cost is
in `entropy_big` at the largest `l`. The projection scaled **L**, and L is not the parameter that
governs the peak — `l` is.

**And the two answers agree anyway.** This is the part worth keeping:

    wrong model  (scale L², peak in correlators):   7.20 GB
    measured     (scale l, peak in entropy_big):    7.31 GB      <- 1.5% apart

> **A model can be wrong about the parameter, wrong about the phase, and still land within 1.5% of the
> right answer.** Had I run s=6 on the projection and had it fitted, that would have read as
> confirmation of the L² model. The agreement is a coincidence of this particular rung and carries no
> information about the next one.

## The extrapolation is itself a projection, so it is stated as a range

| l range | local exponent |
|---|---|
| 40 → 60 | l^4.02 |
| 50 → 70 | l^4.14 |
| 60 → 80 | l^3.58 |
| 70 → 90 | l^2.23 |
| 80 → 100 | l^1.16 |

**Not stable.** Extrapolating l=100 → 120 across that range gives **7.31 – 9.37 GB**, and nothing in
this measurement narrows it — tightening the exponent would cost about what running s=6 costs.

## Decision: s=6 is NOT run

Against a box reading **6.98 GB free / 10.10 GB available** at its best today, and where s=5's 5.92 GB
already drove free memory to 0.09 GB with three other sessions resident:

- the **low** end of the range fits only in *available*, i.e. only if several GB of inactive are
  reclaimed under a fast allocation, which is when this machine stalls rather than fails cleanly
- the **high** end does not fit at all
- and the range cannot be narrowed for less than the cost of the run

**Recorded as a resource limit on the instrument, not as a result about the physics.** s=5 stands as the
last rung; the corner-coefficient convergence question stays open at that resolution rather than being
answered by a run that pages.
