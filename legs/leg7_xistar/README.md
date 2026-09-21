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
