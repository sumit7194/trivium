# A2 — Findings: G7 is KILLED — and the reason we never noticed is the finding

*Run 2026-07-26; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the census script existed.
Falsification v2+, Tier A. **This was a deliberate attack on our own headline meta-claim**, filed because G7
had been "fed" eight times and never once attacked — every entry logged at the moment we *crossed* a wall.*

## Result in one line

**G7 KILLED on the strict reading, VACUOUS on the permissive one — both horns, as pre-registered.** The
cleanest counterexample is our own **S1**: two flat 4-tori, *provably non-isometric* and *provably
isospectral*, which discharges the frozen proof obligation exactly. And the reason eight rounds of
"confirmation" missed it turns out to be structural, not accidental — see *Why G7 kept surviving* below.

## The census (A2a)

Mechanical sweep of every `*.md` in the repo — **no curation by me**, precisely so the sample could not drift
toward my disclosed prior:

| | |
|---|---|
| markdown files swept | **130** |
| raw wall-language hits | 200 |
| minus G7-boilerplate lines | **173** |
| documents containing hits | 43 |
| **distinct walls after de-duplication** | **16** (gate needed ≥10 — **PASS**) |

Language tags: `wall` 119 · `parked` 23 · `unreachable` 11 · `cannot` 9 · `in-principle` 7 · `not-determined`
3 · `out-of-reach` 2 · `blocked` 1 · `undecidable` 1.

**Census precision, reported not hidden:** the `wall` hits in `legV_fractal_boundary` are *literal physical
detector walls* (quantum's double-slit experiment), not epistemic walls — lexical false positives, excluded
at classification.

## The classification (A2b)

Full table in [`results/classification.json`](results/classification.json). Tally over 16 distinct walls:

| label | count | examples |
|---|---|---|
| **CROSSED** | 3 | leg X's float64 wall → mpmath dps=60 · the round-7 trio · the eight self-caught bugs |
| **CROSSABLE** | 6 | CK simplifier · leg Y's three pairs · G4's integrator · legJ box-counting · S3's staircase grid · leg L's SNR floor |
| **UNCROSSABLE-I** | 3 | **S1** · K2 · Witten's no-go |
| **UNCROSSABLE-D** | 3 | **M2 (κ)** · **R6 (log b)** · the landscape wall |
| contested | 1 | the evidence wall (see vacuity) |

**The conservative rule bit, and it should be recorded that it did.** *leg L / G8* looked like an
information wall — δ is information-limited in the no-hair test. But statistical indistinguishability at
finite SNR is **not** exact in-channel identity, so the proof obligation is *not* discharged, and the frozen
rule (undischarged ⇒ CROSSABLE) applies: more SNR moves the Fisher floor. It is recorded as CROSSABLE
against my prior. The rule existed to stop me counting near-misses as kills, and it worked.

## The kill (A2c, strict reading)

**W10 — S1 — alone discharges the ledger's kill condition:**

> Two flat 4-tori (Schiemann pair) that are **provably non-isometric** — the degree-2 Siegel theta differs at
> bucket (48, 96, −24): 0 versus 4 — and **provably isospectral** — theta series identical to norm 400, plus
> Schiemann's theorem. Question: *determine the hidden T⁴ from the KK mass tower.* Channel: the mass tower.
> **Two provably distinct configurations produce identical in-channel data.** No instrument upgrade crosses
> this, because the information is not in the channel at any precision.

That is exactly the A2b proof obligation, and it was already discharged by the S1 run itself — we simply
never held it up against G7. **M2 and R6 kill it a second way**, definitionally: κ = 0.30/0.41/0.51 and
b = 2.32/3.72/0.52 across three legitimate regulators. There is no limit for an instrument to converge to,
so "a better instrument" is not a coherent request. K2, the landscape wall, and Witten's no-go corroborate.

## The vacuity horn (A2c, permissive reading) — and why it isn't a rescue

The strongest defence of G7 is the **channel-change move**, and our own work supplies its best case: **K2's
wall was crossed** — K5's net separated the isospectral drums at 0.76 / 0.98 while the eigenvalue tower sat
at chance, by measuring eigen*functions* instead of eigen*values*.

So: does changing the channel count as an instrument upgrade?

- **If no** (a wall is fixed question **+** fixed channel): K5 answered a *different* question, and S1 kills
  G7. **G7 is false.**
- **If yes**: then *every* information wall is dodgeable by measuring something else, and — decisively — the
  **evidence wall** (W14) also becomes "crossable in principle," despite needing an instrument ~10¹² beyond
  anything buildable, which our own KK notes call *"not a compute wall we could out-muscle."* Under that
  reading nothing could ever falsify G7. **G7 is unfalsifiable.**

There is mechanical support for the vacuity charge sitting in the census itself: **`in principle` appears 7
times** across the corpus, and it is doing almost all of the load-bearing work in G7's phrasing. A claim that
survives only by letting "in-principle instrument" be unbounded has not survived in the sense this ledger
means. **Neither horn leaves G7 standing as written.**

## Why G7 kept surviving eight rounds — the actual finding

This is the part worth keeping, and it is a selection effect with a precise mechanism:

> **You only notice a wall as a wall when you cross it.**

Every one of the eight G7 "confirmations" was a **species-1 (precision/instrument)** wall — float64→mpmath,
the simplifier fix, chart choice, R2's constant-column, R3's exponent window, R4's grid-vs-root-find, S2's
two, S3's threshold. Those announce themselves: you're blocked, you upgrade, you get through, you log a
crossing.

**Species-2 (information) and species-3 (definitional) walls never feel like walls at all — they feel like
results.** S1 didn't feel like hitting a wall; it felt like *finding* that 4-tori aren't spectrally
determined. M2 didn't feel like a wall; it felt like *measuring* that κ is scheme-dependent. So they were
filed as findings, never as walls, and G7 was never asked about them. **The meta-claim was being tested
against a sample that structurally excluded its own counterexamples** — which is the exact failure mode the
ledger exists to prevent, running undetected inside the ledger's own headline.

## The replacement (A2d) — what G7 dies into

A kill with no replacement would be a worse outcome than a survival. The taxonomy, with an operational test
for each species and what to do about it:

| species | the diagnostic question | what to do |
|---|---|---|
| **1 · precision / instrument** | does the answer converge as you refine? | **keep pushing** — upgrade precision, algorithm, basis, compute |
| **2 · information** | do two provably distinct configurations give *identical* data in this channel? | **stop refining, change channel** — no precision helps; find an observable that separates them (this is what K5 did to K2) |
| **3 · definitional** | do two legitimate conventions give *different* limits, both correct? | **stop measuring** — the quantity is not a quantity; report the scheme-dependence *as* the result (M2, R6) |

**The family's own history validates it.** S3's mis-specified gate was exactly a species confusion: I set a
convergence bar (species-1 thinking) on `δ_spec`, whose staircase limit K2 had already documented — and the
apples-to-apples control I *also* built (GWW vs congruent null) was the species-2-aware test that actually
worked. Had this taxonomy existed two days earlier, S3 would have been pre-registered correctly.

**Proposed successor, G7′** (registered here, not run): *"Every wall the family logs is classifiable into
{precision, information, definitional}, and the classification predicts whether further effort pays."* That
is falsifiable — a wall fitting none of the three, or one where the prescription gives the wrong advice,
kills it — and it is *useful*, which G7 was not.

## Honest scope

- **An audit of our own documents**, not new physics. Value is hygiene plus one transferable rule.
- **Completeness ceiling, stated:** the census can only recover walls the family actually wrote down. Walls
  hit and never logged are invisible to it. No exhaustiveness is claimed.
- **This audit was not blind** — the pre-registration disclosed that I already suspected S1, M2 and R6. The
  gate was written so the verdict turns on discharged proof obligations rather than my prior, and the
  conservative default demoted one of my own candidates (leg L). That is the mitigation; it is not the same
  as blindness, and the result should be read with that stated.
- Classification of the loose cases is a judgement call, bounded but not eliminated by the frozen definitions.
- Bridge-solo; read-only over the repo's own docs; no sister dependency.

## A ninth instrument bug — caught mid-audit

The census script first computed `ROOT = parents[2]`, which resolves to `falsification/`, **not** the repo
root. It swept 40 files instead of 130 and returned 47 records — and **still passed the ≥10 gate**, so it
would have proceeded silently on ⅓ of the corpus, missing `JOURNAL.md`, `CAPSTONE.md`, `THE_BRIDGE.md`,
`BACKLOG.md`, both ledgers, and every `leg*/` directory. Caught only by cross-checking the file list against
an earlier ad-hoc grep that had named documents the census didn't show.

Same species as S2's and S3's: **silent under-sampling that passes its own gate.** Fixed to `parents[3]`.
Filed here rather than quietly corrected — and noted with some irony that the wall audit's own instrument
produced a species-1 wall for the audit to log.

## Inputs & artifacts

`code/wall_census.py` (mechanical enumeration; classifies nothing) · `results/wall_census.json` (173 records)
· `results/classification.json` (16 distinct walls, hand-labelled with proof obligations). Kills **G7**
([FALSIFICATION_LEDGER.md:45](../../FALSIFICATION_LEDGER.md)). Follows the template of
[A1](../A1_tooclean_audit), the tier's first audit.
