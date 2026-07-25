# A2 — Pre-registration: the wall audit, i.e. a deliberate attack on G7

*Frozen 2026-07-26, before the census script is written or run. Falsification v2+, Tier A (audits, born from
L2 — the tier A1 created). **This is an attack on our own headline meta-claim.***

## Why this item exists — the bias it is correcting

**G7:** *"Every wall the family has hit is instrument-relative — for each logged wall there exists an
in-principle instrument upgrade that crosses it."* Kill condition on the ledger: *"First wall proven
uncrossable kills it."*

G7 has been "fed" **seven or eight times** (float64→mpmath · the CK simplifier fix · chart choice ·
R2's constant-column · R3's exponent-window · R4's grid-vs-root-find · S2 ×2 · S3's own threshold) and
recorded each time as unfalsified. **But every one of those was logged at the moment we crossed a wall.**
We have recorded confirmations exclusively and have never once gone looking for a counterexample. That is
precisely the selection bias this ledger exists to prevent, sitting inside our own meta-claim. A2 goes
looking.

**Disclosure of prior (this audit is NOT blind).** Before freezing, I already suspect three counterexamples —
S1 (isospectral 4-tori), M2 (κ scheme-dependent), R6 (no universal log in odd d). Because I cannot un-see
them, the gate below is written so that the verdict is decided by **stated criteria and discharged proof
obligations**, not by my prior. Any wall I nominate must survive the same criteria as one I did not.

## Definitions (frozen — the audit is worthless without these)

- **Wall** = a logged instance where the family sought a result and could not obtain it, *relative to a
  stated question and a stated data channel*.
- **CROSSED** — already crossed; the upgrade that crossed it is named and cited.
- **CROSSABLE** — not yet crossed, but a physically realizable upgrade (precision, algorithm, basis/chart,
  compute, an obtainable channel) is nameable. G7-consistent.
- **UNCROSSABLE-I (information-theoretic)** — the sought quantity is not a function of the channel at all.
  **Proof obligation:** exhibit two configurations that are *provably distinct* and *provably identical
  in-channel*. Nothing less discharges it.
- **UNCROSSABLE-D (definitional)** — the sought quantity is not well-defined independently of a convention,
  so there is no limit for an instrument to converge to. **Proof obligation:** exhibit two legitimate
  conventions yielding different limits, both correct.

## The crux, named in advance so I cannot dodge it later

The strongest defence of G7 is: *"S1's wall isn't 'can't distinguish the tori', it's 'can't distinguish them
**from the spectrum**' — change the channel (measure eigenfunctions, as K5 did) and you cross it."* That
defence must be confronted directly, because it forces a dilemma:

- **Strict reading** — a wall is defined relative to a *fixed question **and** channel*. Then changing the
  channel answers a *different* question, and an UNCROSSABLE-I wall genuinely **kills G7**.
- **Permissive reading** — any channel change counts as an instrument upgrade. Then G7 can never fail,
  because one can always propose measuring something else. **G7 becomes unfalsifiable.**

Both horns are findings. A claim that survives only by being unfalsifiable has not survived in the sense this
ledger means.

## Frozen gates

- **A2a — mechanical census.** A script sweeps every `*.md` in the repo for wall-language and emits candidate
  wall records with `file:line` + context. **The enumeration must be mechanical, not curated by me**, so the
  sample cannot be cherry-picked toward my prior. The script **classifies nothing**. PASS iff ≥ 10 distinct
  walls are recovered (below that the audit has no power and is reported as such).
- **A2b — classification.** Every wall in the census gets exactly one label by the frozen definitions, with
  its proof obligation explicitly **discharged or not discharged**. An UNCROSSABLE claim with an undischarged
  obligation is recorded as **CROSSABLE** (the conservative default — the burden is on the kill, not on G7).
- **A2c — the verdict on G7.**
  - **SURVIVES** iff every wall is CROSSED or CROSSABLE.
  - **KILLED** iff ≥ 1 wall is UNCROSSABLE with its proof obligation **discharged**.
  - **VACUOUS-AS-STATED** iff the only reading of "instrument upgrade" that saves G7 is the permissive one —
    recorded as a *separate* finding, with the restatement that would give G7 content again.
- **A2d — the taxonomy payout.** Whatever the verdict, produce the classification table. If G7 dies, it must
  die *into* something more useful than it was: a rule for telling, when you hit a wall, which kind you face
  and whether to keep pushing. A kill with no replacement is a worse outcome than a survival.

## Pre-registered expectation (stated so it can be held against me)

I expect **G7 KILLED on the strict reading and VACUOUS on the permissive reading**, with S1 the cleanest
counterexample (the Schiemann pair is a *theorem*, not a precision limit — the two tori are provably
non-isometric and provably identical in-channel, which is exactly the A2b proof obligation, already
discharged by the S1 run). I expect the surviving useful content to be the three-way taxonomy
(precision / information / definitional). **If the census turns up walls that contradict this, they are
reported first, not last.**

## Honest scope

- This is an **audit of our own documents**, not new physics. Its value is hygiene and a transferable rule.
- The census is only as good as the family's own logging: walls we hit and never wrote down cannot be
  recovered. That is a **stated ceiling on completeness**, not a claim of exhaustiveness.
- Classification is a judgement call in the loose cases; the frozen definitions and the
  conservative-default rule (undischarged ⇒ CROSSABLE) exist to bound that judgement, not to eliminate it.
- Bridge-solo; read-only over the repo's own docs; no sister dependency.
