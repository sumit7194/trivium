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

---

# Hold-out validation, and the structural law beating the fitted one

The s=6 figure rests entirely on extrapolating one step past the measured range — which is what produced
my retracted 7.31–9.37 GB, and before that ansatz's 4.75 GiB/prime. So the law is no longer quoted
without hold-out errors beside it. Method from quantum; in `code/peak_law.py` rather than a heredoc.

**Free power law** — fit exponent and scale, predict the next point:

| fit on | exponent | predicted | measured | error |
|---|---|---|---|---|
| l ≤ 60 | 3.45 | 1.557 GB | 1.669 GB | 6.7% |
| l ≤ 70 | 3.55 | 2.616 GB | 2.808 GB | 6.8% |
| l ≤ 80 | 3.62 | 6.100 GB | 6.539 GB | 6.7% |

**6.7, 6.8, 6.7 — same size, same direction, every time.** A one-directional error of constant magnitude
is a **mis-specified model, not measurement scatter**. The fitted exponent keeps landing below the true
local one because a pure power law has nowhere to put a fixed overhead.

**Structural form** — exponent **fixed at 4** from n = l², fitting only scale and offset:

| fit on | predicted | measured | error |
|---|---|---|---|
| l ≤ 60 | 1.671 GB | 1.669 GB | **0.1%** |
| l ≤ 70 | 2.807 GB | 2.808 GB | **0.0%** |
| l ≤ 80 | 6.773 GB | 6.539 GB | 3.6% |

`a = 6.474e-08`, `c = +0.094 GB`. Residuals fall from ±0.8 GB to ±0.06 GB.

> **The model with fewer free parameters predicts better.** That is the evidence that l⁴ is the
> *mechanism* rather than a good fit — a fitted exponent can absorb anything, and this one was absorbing
> the overhead and paying for it at every extrapolation.

quantum's line is the right statement of what makes this trustworthy: not two numbers matching, but **a
measurement landing on a structurally derived exponent**. Their n×n with n = l² was derived with no
measurement at all, in a different study, from different code.

## Three estimates of s=6

    free power law (this study)          12.39 GB
    structural l^4 (this study)          13.52 GB
    quantum's study, independent code    14.40 GB

Best box reading of the day: **7.0 GB free / 10.1 GB available.** s=6 misses on every one of them, and
the hold-out error is nowhere near large enough to close the gap.

---

# The fitted offset fails quantum's two-routes check — it is a fudge, not a measurement

quantum ran the structural model on their own data and found **no improvement**: their fitted exponents
were already 3.90–3.99, because their ~30 MB overhead was *measured off an `init` phase and subtracted
before fitting*, so their exponent was never asked to absorb it. **The fix matters in proportion to how
much unmodelled overhead the exponent is being made to swallow** — a sharper statement than either of us
had, and it came from a failed replication.

Then they did the check that matters: fitting the offset as a **free parameter** recovered
**c = +35.7 MB** against **30.4 MB measured independently** from the phase label. Two routes, no shared
arithmetic, 15% apart.

**I ran the same check and mine fails.**

My fitted `c` is **+93.5 MB** (or +79.4 MB refitting with two more points). The independently measurable
quantities from my own phase labels are: correlators `after_corr − base` = **5–6 MB**, and the
interpreter baseline **47–48 MB**, which is already subtracted. **Nothing measurable equals 79–94 MB.**

The prediction it makes at small `l` also fails:

| l | model | measured | |
|---|---|---|---|
| 30 | 0.146 GB | 0.106 GB | **+38%** |
| 35 | 0.191 GB | 0.157 GB | **+21%** |

And the residuals across the whole range are **structured, not scattered**:

    l=30  -26 MB    l=50   -8 MB    l=80  +68 MB
    l=35  -20 MB    l=60   +7 MB    l=100 -35 MB
    l=40  -17 MB    l=70  +30 MB

A smooth arc through zero and back. **`a·l⁴ + c` is still mis-specified for this study** — `c` is
absorbing an `l`-dependent term (working arrays that scale below l⁴), which is exactly the error I had
just diagnosed in the *free power law*, one level down. I wrote "a fitted overhead of +94 MB" in a commit
message as though it were a physical quantity. **It is a fitted fudge that matches nothing.**

*Caveat on the two new points: l=30 and l=35 collected only 3 and 6 samples. They are at the edge of the
validity guard and are weak evidence individually; the residual structure across all eight points is the
stronger signal. l=20 and l=25 returned INVALID — too fast to sample — which is precisely the
`0.0 MB in ?` failure quantum found in their probe, and it also means the original sequential run's
"l=20: 0.05 GB, l=30: 0.05 GB" readings were never measurements at all.*

## What survives

    s=6 (l=120):  13.52 GB  ->  13.55 GB on the refit

**The decision is insensitive to the defect.** That is worth stating precisely, because it is the third
time today a conclusion has survived its reasoning: here the survival is *demonstrated* by refitting
rather than assumed, and the offset term is small compared to the l⁴ term at l=120 — which is why a
mis-specified `c` cannot move the answer even though it is wrong.
