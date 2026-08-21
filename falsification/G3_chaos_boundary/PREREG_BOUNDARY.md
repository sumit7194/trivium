# G3 — Pre-registration: does the boundary survive adequate counting statistics?

*Frozen 2026-08-21 before `code/g3_power.py` is written or run. Additive; the original
[PREREGISTRATION.md](PREREGISTRATION.md) gates and the [FINDINGS](FINDINGS.md) verdict are untouched.
This runs forward-look **item 0**, which [FINDINGS](FINDINGS.md) names as the cheapest route to a
conclusive item, ahead of every instrument fix.*

## The question

G3's reported boundary δ\* = 1.1 rests on escape counts of **4/100 at δ=1.3 against 0/99 at δ=1.5** —
the sharpest contrast the ladder contains. Fisher exact on that pair gives **p = 0.121**. *The only
discriminating conjunct in the detector cannot separate the ladder's own extremes.* Power analysis says
~300 orbits per arm reaches **p ≈ 5e-4** on the same effect size.

**If the boundary does not survive that, every instrument fix in the item is moot.**

## Design

- **δ = 1.3 and δ = 1.5 only.** Not a ladder — the two arms of the decisive contrast.
- **Identical sampling at both δ**, which is the whole point: `x₀` at step **0.001** over **±0.08**
  around each of the two bisected separatrix edges ⇒ **322 orbits per δ**. The previous run used step
  0.002 over ±0.1 (~100/δ). **Denser sampling of a comparable window, not a wider one.**
- **N = 200 crossings**, matching the run that produced 4/100 and 0/99, so the escape criterion
  (`ncross ≤ 0.85·N`) means the same thing.
- **Both estimators computed on every orbit** (FFT and NAFF), and **crossing series persisted** —
  forward-look item 4, so no future re-analysis needs re-integration.
- **Per-orbit checkpointing.** The machine has lost power four times in three days, most recently
  ~09:17Z today. A cut costs one orbit.

## Frozen gates

- **B1 — the decisive test.** Fisher exact on δ=1.3 escapes vs δ=1.5 escapes, at n ≈ 322 per arm.
  - **BOUNDARY REAL** iff **p < 0.01**. The escape difference is not a counting artifact, δ\* means
    something, and the instrument work becomes worth doing on an effect known to exist.
  - **BOUNDARY NOT SUPPORTED** iff **p ≥ 0.05**. At this n that is a genuine null, not an underpowered
    one, and δ\* = 1.1 should be withdrawn outright rather than left standing as "unsupported".
  - **UNDECIDED** iff 0.01 ≤ p < 0.05 — suggestive, still not conclusive, and the honest report is that
    tripling n was not enough.
- **B2 — the rate must be estimated, not just tested.** Report both escape fractions with exact binomial
  95% intervals. A p-value alone does not say how large the effect is, and the effect size is what any
  future power calculation needs.
- **B3 — drift stays uninformative, or the story changes.** Report the two-sample KS on drift (both
  estimators) between δ=1.3 and δ=1.5 at this n. [FINDINGS](FINDINGS.md) established drift carries no
  information at n≈100 (p=0.503). **If it separates at n≈322, that finding needs revisiting** — a null at
  low n and a signal at high n is what an underpowered test looks like, and I should not be able to
  dismiss that possibility by having asserted it earlier.
- **B4 — A1 guard liveness.** Report the observed dH distribution against DH_MAX = 1e-4. The guard
  rejected **0 of 599** orbits in the previous run, with the worst orbit 4.6e+07 below threshold. If it
  again rejects nothing, it is reported as inert rather than as a discipline in force.

## Declared in advance

- **This cannot resurrect the drift conjunct.** Even if B1 says the boundary is real, drift's gain varies
  2.1× with bin offset and longer records do not fix it (measured today: 16× more data buys 1.4×,
  non-monotonically). B1 is a statement about **escape**, and escape alone.
- **NAFF is the instrument of record for any cross-δ drift comparison here**, because at N ≥ 800 both
  floors sit ~6 orders below the real signals so floor cannot discriminate, while NAFF's gain spread is
  0.000 against FFT's 0.6. *At N = 200 this run's drift numbers inherit the gain problem and are reported
  for B3 only, not as a cross-δ measurement.*
- **Expected cost ~12–15 h**, single-core, <500 MB, no external services. Flagged to all four sister
  sessions before starting; ansatz cleared it (their contention is RAM during rank steps, not CPU).
- **A null is a real outcome and is the more likely one.** 4/100 vs 0/99 may simply be two draws from the
  same small rate.

---

# ADDENDUM — the control must survive BOTH matchings (frozen 2026-08-22, before either finishes)

The δ=1.0 control has **one** separatrix band where every treatment δ has **two**. So it cannot be matched
to them on orbit count *and* on x₀ spacing simultaneously — halving the step buys matched **n** at half
the **spacing**; keeping the step buys matched spacing at half the **n**.

**Choosing one would make the headline a fact about my matching choice.** ansatz's §85 precedent is exact:
their "obstruction grows with ε" was **ensemble composition, not physics**, because the surviving-orbit
count varied with the swept variable, so the arms differed by construction. *When the selection criterion
depends on the swept variable, care within an arm cannot fix it — the other matching has to be a second
arm.*

**FROZEN COMMITMENT, made before either run reports:**

- **Arm A — matched n.** `HALF=0.08, STEP=0.00025`, one edge ⇒ ~320 orbits. *(launched first)*
- **Arm B — matched spacing.** `HALF=0.08, STEP=0.0005`, one edge ⇒ ~160 orbits, same x₀ spacing as the
  treatment δ.

> **The FINDINGS headline — "eight of nine δ sit at or below the integrable control" — must hold under
> BOTH arms.** Holding under both makes it a statement about the spacetimes. Holding under one makes it a
> statement about my matching choice, and the addendum will say which. **If the arms disagree, the headline
> is withdrawn**, not reported with a caveat.

Both arms are ~2 h and single-core. This is worth the compute *precisely because it can fail.*
