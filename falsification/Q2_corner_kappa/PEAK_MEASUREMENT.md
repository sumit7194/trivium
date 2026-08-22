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

---

# CORRECTION — the "unstable exponent" was my instrument, and s=6 costs ~12.7 GB not 7.3–9.4

quantum found two defects in their equivalent probe that mine shared **by construction**, and both fed
the table above.

**`ru_maxrss` never falls.** My per-l numbers were the running maximum over the whole process. I argued
this was harmless because the true peak rises with `l` — an **assumption I did not test**, while the
quantity being derived from those numbers *was* the exponent.

**Python does not return freed memory promptly.** After a large `l` the process keeps the arena, so
later points read the plateau rather than their own demand. That produces exactly the signature I
reported as a finding: **an apparent exponent that decays with l.**

## Re-measured: one point per fresh process, current RSS, baseline subtracted

| l | entropy peak | | contaminated exponent | clean exponent |
|---|---|---|---|---|
| 40 | 0.229 GB | 40→60 | 4.02 | 40→50 · **3.29** |
| 50 | 0.477 GB | 50→70 | 4.14 | 50→60 · **3.65** |
| 60 | 0.928 GB | 60→80 | 3.58 | 60→70 · **3.81** |
| 70 | 1.669 GB | 70→90 | 2.23 | 70→80 · **3.90** |
| 80 | 2.808 GB | 80→100 | **1.16** | |

The contaminated series **decays**; the clean series **rises toward 4** — and 4 is the structural answer,
independently derived by quantum in a different study: the matrices are n×n with n = l², so memory goes
as n² = **l⁴**. What I had published as a property of the algorithm ("the exponent is not stable") was a
property of my measurement.

## The extrapolation was then validated where it could be checked

Fitting only l ≤ 80 predicts **6.29 GB** at l=100. Measured in a fresh process: **6.54 GB — 4% out.**
The old contaminated single-process run reported 5.92 GB *total* for that point, i.e. it **understated**
the true entropy peak.

## Corrected answer

    s=6, l=120, validated law (exponent 3.66):   12.74 GB

**Superseding the 7.31 – 9.37 GB range recorded above — that range was 36% below the truth at its own
high end.** The decision does not change; the margin does, and it changes in the direction that matters:
s=6 was never a borderline call requiring a judgement about reclaim. It misses by roughly 3 GB against a
box whose best reading all day was 10.1 GB available and 7.0 GB free.

> **The wrong instrument produced a number close enough to the right one to support the same decision,
> and a stated reason that was entirely false.** The conclusion surviving is not evidence the reasoning
> did — which is the same lesson as the 1.5% coincidence one section above, arriving this time inside the
> measurement built to avoid it.
