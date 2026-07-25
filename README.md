# The Bridge — *trivium*

**Cross-validation of four deliberately-independent physics projects.**
The founding question — *how many numbers is a black hole?* — was answered three
independent ways: deductive proof, inductive representation-learning, and empirical
measurement on real LIGO data. A fourth, deliberately-independent QM-foundations lab
joined 2026-07-24. The whole point is that the projects were built with independent
roots on purpose, so when two agree it is **evidence, not an echo** — and when they
disagree, that disagreement is a finding, not a bug.

> **Start here:** [CAPSTONE.md](CAPSTONE.md) (state of the whole program — scoreboard, load-bearing
> results, and the honest-miss ledger) · [SPINE_SUMMARY.md](SPINE_SUMMARY.md) (the founding result) ·
> [THE_BRIDGE.md](THE_BRIDGE.md) (the design doc) · this README (the operating contract).
>
> **[FALSIFICATION_LEDGER.md](FALSIFICATION_LEDGER.md)** (v1) **+ [FALSIFICATION_V2.md](FALSIFICATION_V2.md)**
> (v2, "the informed round") — the standing programme of postulates stated *to be killed*:
> pre-register → attack → three-valued verdict, never vibes. **24 attacks and counting** in
> [`falsification/`](falsification), including a standing self-audit tier that turned the method on
> itself — auditing our own too-clean results, attacking our own headline meta-claim (killed), and
> sweeping our own findings for unverified citations (caught one, corrected it). Kills come with an
> extracted mechanism, not a bare "no"; survivals are logged as "survived N attacks," never as "true."

## The four oracles (independent public repos this bridges)

| Oracle | Repo | Role |
|---|---|---|
| **ansatz-machine** | [github.com/sumit7194/ansatz-machine](https://github.com/sumit7194/ansatz-machine) | **deductive** — exact metrics, moduli/hair-count, exact observables (shadow, ISCO, light-bending) proved by a SymPy engine. The ground-truth oracle. |
| **tabula-geometrica** | [github.com/sumit7194/tabula-geometrica](https://github.com/sumit7194/tabula-geometrica) | **inductive** — neural bottleneck/MDL counting; the legibility law. Blind to metrics by design. The representation oracle. |
| **deepstrain** | [github.com/sumit7194/DeepStrain](https://github.com/sumit7194/DeepStrain) | **empirical** — no-hair δ on real O3a/O4 ringdowns, echo search, PBH search. Sensitivity from injections, significance from measured background. The measurement oracle. |
| **vestigium** | [github.com/sumit7194/vestigium](https://github.com/sumit7194/vestigium) | **foundational** — a verified QM-foundations lab (measurement problem, entanglement, Kaluza–Klein projections). Every result checked against exact analytics or a real experiment. Joined 2026-07-24. |

This repo (*trivium* — "three roads," predating the fourth oracle) contains **only**
the bridge: the cross-validation code, pre-registrations, and findings. It reads from
the four repos above but never modifies them, and never makes them aware of each
other. To reproduce, check out the four repos as siblings of this one (local dirs
`conjecture_machine`, `SpaceTime`, `BlackHole`, `quantum` respectively) — the bridge
scripts import their engines read-only.

## Operating rules (non-negotiable for this workspace)

1. **Everything bridge-related lives here**, under `/Users/sumit/Github/TheBridge`.
   All notes, new docs, all code, all results. Nothing bridge-related is written
   into the four source repos.
2. **The four source repos are read-only.** We import from them and read their
   data, but never modify them. They are kept ignorant of each other so that when
   two oracles agree, the agreement is *evidence and not an echo* (THE_BRIDGE.md §2).
3. **Any source code reused here is additive.** When adapting code we bring over,
   add comments explaining the change and **never delete the original lines** —
   old code stays alongside new, clearly marked.
4. **Pre-register → build → gate → document** (the shared ethos of all four repos).
   No comparison is made before its prediction and agreement-criterion are written
   down. Disagreements are findings, not bugs (THE_BRIDGE.md §2 rules 1–4).
5. **A mechanism claim carries its receipt.** Every causal/explanatory statement in a
   FINDINGS doc carries a number from our own results, a resolvable identifier for a
   source actually read, or an explicit `[asserted, unverified]` tag — REPRODUCED
   beats CITED. Two same-day self-corrections (2026-07-26) are why this rule exists.

## Bootstrapping order (historical)

The program started with a single spine (ansatz's exact moduli-count vs tabula's
neural count, then deepstrain's measured δ closing the triangle — `leg1_moduli_count/`
onward). That thread is long since closed; **CAPSTONE.md is the current state**, and
new work now enters through the falsification ledgers, not this list.

## Layout

```
THE_BRIDGE.md              the design doc (the map)
CAPSTONE.md                state of the whole program — start here
README.md                  this file (the operating contract)
JOURNAL.md                 dated activity log, one entry per working session
FALSIFICATION_LEDGER.md    v1 postulate ledger
FALSIFICATION_V2.md        v2 postulate ledger ("the informed round") + the lessons (L1…)
SISTER_REQUESTS.md         asks relayed to the four sibling sessions + their replies
falsification/<ID>_name/
  PREREGISTRATION.md       gates frozen BEFORE the code that tests them
  code/                    bridge code (imports source repos read-only)
  results/                 raw outputs (JSON)
  FINDINGS.md              the verdict, the mechanism, and what it cost to get there
leg<N>_name/                bootstrapping-era legs (pre-falsification-ledger); see CAPSTONE.md
```
