# A3 — Pre-registration: how many unverified MECHANISM claims are sitting in our banked findings?

*Frozen 2026-07-26, before the census script is written or run. Falsification v2+, Tier A — the third audit,
after [A1](../A1_tooclean_audit) (too-clean numbers) and [A2](../A2_wall_audit) (walls).*

## Why this exists

**Two retractions in one day, both mine, both the same failure mode: a mechanism asserted without being
checked.**

- **[M6](../M6_prior_art_gate/FINDINGS.md)** claimed "O4 is our threshold being the wrong kind, and a
  noise-calibrated cutoff dissolves it" — asserted *from reading*, shipped same-day, **never run**.
  [R7](../R7_emit_threshold/FINDINGS.md) ran it: false by 28×.
- **[R6](../R6_arealaw_log/FINDINGS.md)** claimed "odd d has no universal log" — asserted *from memory*,
  against R6's own pre-registered leg-W discipline. It is **inverted** (the rule is even *spacetime*
  dimensions), it was **load-bearing enough to be in the document's title**, and it sat undetected for two
  days until quantum's independent re-test made it unmissable.

Neither was caught by us proactively. One was caught by our own later experiment, the other by a sister.
**The question A3 asks is simply: how many more are there?**

## What counts as a mechanism claim

A **mechanism claim** is a causal or explanatory assertion in a findings document — a statement of *why* a
measured thing is so, as opposed to *that* it is so. "κ spreads 51% across regulators" is a measurement.
"κ spreads because the quantity is UV-dominated" is a mechanism claim. Gates and tables are typically
measurements; the danger lives in the prose that interprets them.

## Frozen classification (three labels, exhaustive)

- **MEASURED** — a number in our own `results/*.json` backs the claim directly.
- **CITED** — a specific external source is given **and** the audit can confirm we actually read it
  (fetched/quoted in the document), not merely name-dropped.
- **ASSERTED-UNVERIFIED** — neither. Stated from memory, intuition, or plausible reasoning.

**ASSERTED-UNVERIFIED is not automatically wrong** — most such claims are probably fine. The finding is the
*count*, the *rate*, and above all **whether any are load-bearing**.

**LOAD-BEARING** (frozen definition) = the claim appears in a document's **title**, its **"result in one
line"**, its **verdict string**, or a **frozen gate**. R6's was in the title; M6's was in a recommendation
acted on the same day. Those are the ones that do damage.

## Frozen gates

- **A3a — mechanical census.** A script sweeps every `falsification/*/FINDINGS.md` plus the two ledgers for
  mechanism-claim language (`because`, `the reason`, `mechanism`, `explains`, `due to`, `hence`, `therefore`,
  `so that`, `why`). **The script classifies nothing** — enumeration must be mechanical so the sample cannot
  be curated toward my prior. PASS iff ≥ 20 candidate claims are recovered.
- **A3b — classification.** Every *distinct* mechanism claim gets exactly one of the three labels, plus a
  LOAD-BEARING flag. Conservative default, as in A2: **if I cannot point to the backing number or the read
  source, it is ASSERTED-UNVERIFIED** — the burden is on the claim, not on the audit.
- **A3c — the verdict.**
  - **SURVIVES** iff **zero** ASSERTED-UNVERIFIED claims are LOAD-BEARING (beyond R6/M6, already retracted).
    Our interpretation prose is disciplined; the two retractions were isolated.
  - **KILLED** iff **≥ 1 new** LOAD-BEARING ASSERTED-UNVERIFIED claim is found — the two retractions were
    the visible part of a pattern, and every one found must be either checked or explicitly tagged.
- **A3d — the standing rule (the payout, whatever the verdict).** Adopt: *every mechanism claim in a FINDINGS
  carries a measurement, a verified citation, or an explicit `[asserted, unverified]` tag.* A3 is worthless
  as a one-off count; its value is installing the guard that makes the next R6 visible at write-time.

## Pre-registered expectation (recorded so it can be held against me)

I expect **KILLED** — that a systematic sweep finds more. R6's survived two days *in a title*, which is the
worst case and the one we happened to catch; less prominent ones would have no such luck. I also expect them
to cluster in **interpretation prose** rather than in gates, because gates are numeric by construction. If
the census contradicts this, that is reported first.

## Honest scope

- **An audit of our own documents.** No new physics; the value is hygiene plus a write-time guard.
- **Completeness ceiling:** the census finds claims phrased with the listed connectives. Mechanism claims
  made without them are invisible to it. Stated, not claimed away.
- Classification is a judgement call at the margins; the conservative default bounds it without eliminating it.
- **This audit is not blind** — I know about R6 and M6. They are excluded from the "new" count in A3c
  precisely so the gate turns on what the sweep finds *beyond* what prompted it.
- Bridge-solo; read-only over our own docs.
