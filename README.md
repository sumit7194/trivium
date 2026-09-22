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
| **cuspis** | [github.com/sumit7194/cuspis](https://github.com/sumit7194/cuspis) | **single-problem** — the entanglement-entropy corner function `a(θ)` in 3d CFTs. Not an oracle with a general method: one question, an analytic result and an arbitrary-precision instrument. Began as an evaluation workspace and was promoted. Joined 2026-09-05. |

This repo (*trivium* — "three roads," predating everything after the third oracle)
contains **only** the bridge: the cross-validation code, pre-registrations, and
findings. It reads from the repos above but never modifies them, and never makes them
aware of each other. To reproduce, check them out as siblings of this one (local dirs
`conjecture_machine`, `SpaceTime`, `BlackHole`, `quantum`, `corner_function`
respectively) — the bridge scripts import their engines read-only.

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

6. **The bridge's errors land inside its corrections**, where they inherit the
   authority of the correction. Both errors this repo committed in the 2026-09-22
   leg-6 arc were made while offering a peer a *better check than the one they had* —
   a mixed-ε ladder presented as a consistency check, and a derived quantity presented
   as an independent cross-check. A correction arrives with standing the claim it
   corrects does not have, and **that standing transfers to whatever else is in the
   message**. So the correction is the part to re-derive before sending, not the part
   to send fastest.
   *And the corollary, from the receiving side:* **the correction you are most
   confident in is the one to state with its own caveat attached, because it is the
   one the recipient will audit least.** A correction arrives with momentum — it has
   just been right, the recipient is mid-update, and adopting a frame is cheaper than
   building one. That is most of why peer review works and all of why it fails that
   way.
7. **Accuracy is not evidence of validity, and twice it has been what suppressed the
   check.** A derived `Q(0.20)` that was right to 0.2% passed as a cross-check; a
   dissolution that matched to 3% went untested for hours. *Had either been off by 30%
   it would have been caught in a second.* Re-derive any number that lands flush
   against a boundary, or that agrees to better than the instrument's own
   reproducibility — **the closer the agreement looks, the less likely anyone is to
   test it.**

## After cloning: activate the hooks

```bash
./ops/install_hooks.sh
```

**This is not optional boilerplate.** `.githooks/pre-commit` is tracked and arrives with the clone,
but `core.hooksPath` — the setting that makes git *run* it — lives in `.git/config`, which is local
and **is not cloned**. So a fresh clone has the hook as a file and not as a gate, and nothing
announces the difference: it is in git, in the diff, and reviewable. Run
`./ops/install_hooks.sh --check` to find out which you have (exit 1 if inactive).

The installer runs a known-fail control on activation, because *a hook that has only ever been seen
to pass has not been tested*. Exactly one clause blocks — the live-checkpoint guard, which compares
an mtime to a clock and has no opinion about physics. Bypass with `git commit --no-verify`.

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
