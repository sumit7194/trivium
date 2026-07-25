# G3 — Findings: UNDECIDED(search). The hunt was below its own resolution floor, by construction.

*Run 2026-07-26 (24 min); gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Tier G — the
oldest unfired bet on the v1 ledger, and the first new Tier-G attack since the campaign opened. **A null, with
a diagnosis. G3 remains OPEN.***

## Result in one line

**UNDECIDED(search)** — the pre-registered live outcome. **G3b failed**: ansatz §106's exhibited ZV δ=2 layer
did not reproduce, so the frozen rule voids the later gates and **G3 is not decided either way**. The reason
is quantitative and was knowable in advance: **our frequency-drift measure's smallest non-zero readable value
is 0.0333, and the layer we were hunting sits at 0.027.** The signal was *below the instrument's floor* — the
scan could not have succeeded.

## The gate table

| gate | result |
|---|---|
| **G3a** — integrable control (δ=1.0 = Schwarzschild) must not fire | PASS *(but weakly — see below)* |
| **G3b** — reproduce §106's δ=2 layer | **FAIL** — 0 orbits fired · **later gates VOID** |
| **G3c** — the δ boundary | not evaluated (voided) |
| **G3d** — species classification | not evaluated (voided) |

The scan itself is uninformative and is reported so: **max drift came out at exactly 6.67×10⁻² for every
single δ — including δ = 1.0, which is Schwarzschild and provably integrable.** A detector returning an
identical value for an integrable and a non-integrable metric is measuring nothing.

## The diagnosis — why it was doomed before it ran

`drift()` splits an N-crossing series in half and compares the dominant FFT frequency of each half. With
**N = 60**, each half has 30 points, so the FFT bin spacing is **1/30**, and the smallest non-zero drift the
measure can return is **2/N = 0.0333**. Every observed value was a multiple of that quantum — which is why
they were all identical.

| quantity | value |
|---|---|
| our resolution floor, 2/N at N=60 | **0.0333** |
| §106's layer drift | **0.027** |
| §106's island/torus controls | ~1e-4 |
| ⇒ our floor vs the target signal | **1.2× too large** |
| N required to resolve 0.027 | **N ≫ 74**; §106 used **~200** |

**So the budget, not the physics, decided this run.** §106 found the layer with ~200 crossings and `x0` steps
of **0.002** in a razor-thin window; we used **60 crossings and 9 samples across a wide band**. By
[A2's taxonomy](../A2_wall_audit/FINDINGS.md) this is a textbook **species-1 (precision)** wall with a
*computable* crossing point — the prescription is "keep pushing," and the amount of pushing is now known.

## Two bugs, and the same gate failing vacuously twice

**① The orbits were exactly planar (found and fixed mid-run).** ZV is reflection-symmetric about the equator,
so starting at `y = 0` with `p_y = 0` leaves the orbit **exactly** in the plane — `y == 0.00e+00` forever,
verified directly. It then never crosses the section, no series exists, and every δ reported "too few clean
orbits." **§106's condition is `p_x = 0`, and I had it inverted.** Since `p_on_shell` solves for `p_x` given
`p_y`, reaching `p_x = 0` requires bisecting `p_y` — now `py_at_px_zero()`. Tenth self-caught instrument bug
of the campaign, same species as all the others: **a silent failure that looked like a result.**

**② The integrable control passed vacuously — twice, in two different ways.** This is the part worth keeping:

- **Run 1:** G3a PASSED with **zero orbits**. A control that passes because nothing ran is not a control.
  Fixed by requiring ≥5 clean orbits.
- **Run 2:** G3a PASSED again — but only because *no orbit escaped*, the second half of the `drift AND escape`
  conjunction. The drift half was **dead** (returning 0.0333 for Schwarzschild). A conjunctive gate passes
  whenever *either* conjunct is silent, so **a broken conjunct hides inside a passing control.**

The lesson generalises beyond this item: **a conjunctive fire-criterion needs each conjunct independently
validated on the control**, or the control certifies only that the conjunction is silent — which it would be
even with every component broken. That is the same family as R9's condition-number guard and S3's threshold:
*the gate measured the convenient thing, not the thing that would catch the failure* (**L8**).

## The one substantive observation

Long-lived orbits at δ=2 exist only in a **narrow band `x₀ ∈ [10,16]`** — outside it orbits plunge within
1–2 crossings (x₀=6: 632 steps, 0 crossings; x₀=8: 3844 steps, 2 crossings; x₀=20+: escape). The band moves
with δ, so the code now locates it **per δ** rather than assuming it. That is a real (small) piece of
structure for whoever runs this properly, and it bounds where the search should look.

## What a real attempt needs

Stated so the next attempt is cheaper than this one:

- **N ≳ 200 crossings** per orbit (≈700k integration steps each) — not 60.
- **Fine `x₀` stepping (~0.002)** inside the located band — not 9 samples across it.
- A **drift estimator that is not FFT-bin-quantized** (e.g. rotation-number or phase-unwrap based), so the
  resolution floor is set by the data rather than by `2/N`.
- Budget: this run was 24 minutes and was ~1.2× below threshold. A correct run is plausibly **hours**, which
  is a legitimate reason to schedule it rather than squeeze it.

## Honest scope

- **G3 is not decided.** Nothing here bears on whether non-integrable ZV metrics have detectable chaos; the
  instrument never reached the question. **No claim is made about the δ-boundary**, which was the point of the
  exercise and remains unmeasured.
- The pre-registration named this outcome in advance — *"the search is delicate and may fail … UNDECIDED(search)
  is a live, pre-registered outcome, and would itself be a species-1 statement about the hunt, not about the
  physics."* It is recorded as exactly that.
- §106's layer drift (0.027) and the Lukes-Gerakopoulos reference are **relayed from ansatz's §106 header**,
  `[asserted, unverified]` on our side (**L10**). They enter here only as the *target scale* for a resolution
  calculation, never as a result.
- Bridge-solo; imports ansatz read-only (`_zv_invariant`, `poincare`); ansatz unmodified.

## Inputs & artifacts

`code/g3_boundary.py` · `results/g3_boundary.json`. Attacks **G3** (v1 ledger, Tier G), which stays **OPEN**.
