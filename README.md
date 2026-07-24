# The Bridge — *trivium*

**Cross-validation of three deliberately-independent black-hole physics projects.**
One proposition — *how many numbers is a black hole?* — answered three independent
ways: deductive proof, inductive representation-learning, and empirical measurement on
real LIGO data. The whole point is that the three projects were built with independent
roots on purpose, so when two agree it is **evidence, not an echo**.

> **Start here:** [CAPSTONE.md](CAPSTONE.md) (state of the whole program — scoreboard, load-bearing
> results, and the honest-miss ledger) · [SPINE_SUMMARY.md](SPINE_SUMMARY.md) (the founding result) ·
> [THE_BRIDGE.md](THE_BRIDGE.md) (the design doc) · this README (the operating contract).
>
> **[FALSIFICATION_LEDGER.md](FALSIFICATION_LEDGER.md)** — the standing programme of postulates stated *to be
> killed*: pre-register → attack → three-valued verdict. 11 resolved, including the flagship
> "legible ⟺ KY-integrable" (falsified 2026-07-24 and replaced by a sharper claim). Attacks live in
> [`falsification/`](falsification).

## The three oracles (independent public repos this bridges)

| Oracle | Repo | Role |
|---|---|---|
| **ansatz-machine** | [github.com/sumit7194/ansatz-machine](https://github.com/sumit7194/ansatz-machine) | **ground truth** — exact metrics, moduli/hair-count, exact observables (shadow, ISCO, light-bending) proved by a SymPy engine |
| **tabula-geometrica** | [github.com/sumit7194/tabula-geometrica](https://github.com/sumit7194/tabula-geometrica) | **representation** — neural bottleneck/MDL counting; the legibility law. Blind to metrics by design |
| **deepstrain** | [github.com/sumit7194/DeepStrain](https://github.com/sumit7194/DeepStrain) | **measurement** — no-hair δ on real O3a/O4 ringdowns, echo search, PBH search |

This repo (*trivium* — "three roads") contains **only** the bridge: the cross-validation
code, pre-registrations, and findings. It reads from the three repos above but never
modifies them, and never makes them aware of each other. To reproduce, check out the
three repos as siblings of this one (local dirs `conjecture_machine`, `SpaceTime`,
`BlackHole` respectively) — the bridge scripts import their engines read-only.

## Operating rules (non-negotiable for this workspace)

1. **Everything bridge-related lives here**, under `/Users/sumit/Github/TheBridge`.
   All notes, new docs, all code, all results. Nothing bridge-related is written
   into the three source repos.
2. **The three source repos are read-only.** We import from them and read their
   data, but never modify them. They are kept ignorant of each other so that when
   two oracles agree, the agreement is *evidence and not an echo* (THE_BRIDGE.md §2).
3. **Any source code reused here is additive.** When adapting code we bring over,
   add comments explaining the change and **never delete the original lines** —
   old code stays alongside new, clearly marked.
4. **Pre-register → build → gate → document** (the shared ethos of all three repos).
   No comparison is made before its prediction and agreement-criterion are written
   down. Disagreements are findings, not bugs (THE_BRIDGE.md §2 rules 1–4).

## Recommended order (THE_BRIDGE.md §8)

1. **Spine leg 1** — ansatz exact moduli-count vs tabula neural count on the same
   exact families, via the observables interface (§4A, §8.1). → `leg1_moduli_count/`
2. **Domain-gap diagnostic** — legibility law as a sim→real diagnostic (§4B).
3. **Close the triangle** — add deepstrain's measured δ (§3).

## Layout

```
THE_BRIDGE.md            the design doc (the map)
README.md                this file (the operating contract)
JOURNAL.md               dated activity log, one entry per working session
leg1_moduli_count/
  PREREGISTRATION.md     predictions + agreement criteria, frozen before building
  code/                  bridge code (imports source repos read-only)
  results/               outputs, logs, the comparison table
```
