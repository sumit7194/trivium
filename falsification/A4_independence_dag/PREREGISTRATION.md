# A4 — Pre-registration: the independence DAG, i.e. a deliberate attack on the bridge's founding claim

*Frozen 2026-09-22, before any extraction is written or run, and before the four sisters reply to their
half of it. Falsification v2+, Tier A (audits). **This is an attack on the claim that makes every other
result in this repo worth having.***

## The claim under attack

Stated three times in this repo and never once measured:

> **THE_BRIDGE.md §2 / README rule 2 / PROGRAM_II.md:847** — *"They are kept ignorant of each other so
> that when two oracles agree, the agreement is evidence and not an echo."*

**Three assertions, zero measurements.** The claim is load-bearing for all five results in CAPSTONE §3,
because every one of them is of the form *"independent epistemologies concur."* If the independence is
not there, the concurrence is not evidence.

## Why this item exists — the bias it is correcting

This is structurally identical to the bias [A2](../A2_wall_audit) was built to attack. A2's sentence was:

> *"We have recorded confirmations exclusively and have never once gone looking for a counterexample."*

**For independence, we have not even recorded confirmations. We have recorded the policy.** Every
mention is a restatement of the rule or a defence of it; none is a check that it held.

And the fleet already owns the mechanism. **L11**: *"A claim relayed from a sister is not corroborated —
it is repeated."* **L11 is the rule. A4 is the first audit of whether we have obeyed it.**

## Definitions (frozen — the audit is worthless without these)

- **Edge** = a transfer of content between two repos of the family, in either direction, through *any*
  channel: a bridge relay, a user paste, a direct read of a sibling directory, or shared code.
- **Edge type**, exactly one per edge:
  - `RESULT` — a number or verdict from A stated to B.
  - `METHOD` — a technique, diagnostic, or rule from A given to B.
  - `CODE` — an implementation shared or imported.
  - `ASSUMPTION` — a framing, premise, or target definition from A adopted by B.
  - `TASK-FRAME` — B asked to compute something where the ask itself encodes A's answer.
  - `REFUSED` — proposed and declined. **These are recorded as findings, not as absences.**
  - `DECLARED-NULL` — an explicit "no transfer this round," stated at the time.

## The echo condition — all four required

An edge is **CONTAMINATING** iff:

    E1  content crossed A -> B;
    E2  it was load-bearing for a number B subsequently produced;
    E3  the crossing PRECEDED B's production of that number;
    E4  B's number was then compared against A's, and the agreement was counted as evidence.

**E4 is not decoration.** A transfer that corrupts a number nobody ever cross-compares costs nothing
evidentially. It may be a different fault; it is not an echo.

### The two hard cases, decided now rather than later

- **METHOD transfer is contaminating iff the method IS the measurement procedure for the compared
  quantity.** Shared hygiene ("sample the null, don't reason about it") does not turn two measurements
  into one. Shared *measurement procedure* does. Anchored in a rule this family already wrote:
  *"reproducing a known number by importing someone else's implementation is that implementation run
  twice, which is ONE measurement, not two."*
- **A shared error is NOT an echo.** Two repos adopting the same wrong premise is a correlated prior,
  logged separately as `CORRELATED-PRIOR`. It is a real fault with a real cost, and it is not what the
  independence claim is about. Conflating the two would inflate the kill.

## Frozen gates

- **A4a — mechanical census.** A script sweeps `SISTER_REQUESTS.md` and the repo's `*.md` for transfer
  language and emits candidate edges with `file:line` + context. **The enumeration must be mechanical,
  not curated by me.** The script classifies nothing. PASS iff ≥ 30 distinct edges are recovered; below
  that the audit has no power and is reported as such.
- **A4b — the positive control, and the audit is VACUOUS without it.** The census must independently
  recover the **L1 / Collinson** edge — already documented in FALSIFICATION_V2 as ansatz asserting and
  the bridge repeating, *"looked like two repos agreeing when it was one asserting and one repeating."*
  This is a **known-true echo**. A census that cannot find the one we already know about has not been
  shown able to return "something," and its nulls mean nothing. *(TIER 2, TASK.md.)*
- **A4c — classification.** Every edge gets exactly one type and an E1–E4 determination, each condition
  marked **met / not met / undetermined**. **An edge with any condition undetermined is recorded as
  NOT contaminating** — the conservative default, because the burden is on the kill.
- **A4d — the reception half, which is not mine to fill.** This census sees **sends**, not **receives**.
  An edge exists only if content was received *and used*. Four sisters are asked their half
  independently, and **any edge they report that the census missed is itself a finding about the
  census's completeness**, recorded as such rather than quietly added.
- **A4e — the verdict.**
  - **KILLED** iff ≥ 1 of CAPSTONE §3's five load-bearing results rests on a comparison with a
    CONTAMINATING edge.
  - **WOUNDED** iff contaminating edges exist but none touches a load-bearing result — the claim is
    true where it is spent, and the policy leaks elsewhere.
  - **SURVIVES** iff none exist **and** A4b fired.
  - **VACUOUS** iff A4b did not fire, whatever else was found.
- **A4f — the payout.** Whatever the verdict, produce the DAG: every edge labelled and dated. If the
  claim dies it must die into something more useful — a channel rule saying which transfers are free and
  which must be declared before a cross-comparison is allowed to count. **A kill with no replacement is
  a worse outcome than a survival.**

## Pre-registered expectations (stated so they can be held against me)

1. **The README's literal wording is FALSE and I expect to have to restate it.** The repos are
   demonstrably *not* "ignorant of each other" — they address each other by name, correct each other,
   and refuse each other's asks. What is actually defensible is a narrower claim about *when* content
   crosses relative to measurement. I expect the audit's main product to be that restatement.
2. **I expect WOUNDED, not KILLED** — specifically, that the five load-bearing results are clean by
   **accident of chronology** (the spine closed before most relay traffic existed) rather than by
   policy. If that is what the data shows, *"clean by luck"* is the finding, and it is not a defence.
3. **I expect the largest category to be `METHOD`,** and under the frozen rule most of those are benign.
   I am aware this is the rule that most protects my prior, which is why it was frozen before the count.
4. **I expect at least one unlogged channel** — content that reached a sister without passing through
   SISTER_REQUESTS.md. This is the one thing my census structurally cannot see, and it bounds every
   completeness claim A4 makes.

## Honest scope

- This is an **audit of our own record**, not new physics. Its value is that it prices the evidence
  everything else in this repo is quoted in.
- **Ceiling on completeness:** transfers nobody logged cannot be recovered. A4d exists because of this,
  and it only narrows the gap — it does not close it.
- The bridge is **the fleet's busiest transfer channel**, which makes this repo the interested party.
  I am auditing a claim whose failure is mostly *my* doing. The frozen definitions and the
  conservative default (undetermined ⇒ not contaminating) bound that, and do not eliminate it.
- Read-only over the sisters, per rule 2. Their half is **asked, never taken.**
