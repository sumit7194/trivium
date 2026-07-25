# A3 — Findings: KILLED. A load-bearing theorem claim was cited five times, never verified — and it happened to be true

*Run 2026-07-26; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the census script existed.
Falsification v2+, Tier A — the third audit, after [A1](../A1_tooclean_audit) (too-clean numbers) and
[A2](../A2_wall_audit) (walls). Filed because **two retractions landed in one day with an identical failure
mode**: a mechanism asserted without being checked.*

## Result in one line

**KILLED.** A systematic sweep found a **new load-bearing ASSERTED-UNVERIFIED claim**: *"Collinson 1976 /
Dietz–Rüdiger 1981 force KT ⇒ KY on type-D vacua"* — cited **five times** across the corpus including in
**L1, the first lesson of the entire v2 ledger**, with **no identifier and no verification record anywhere**.
On checking, **it is true**. That is precisely what makes it the finding: **R6's unverified claim was false,
this one was true, and the process was identical. Only the luck differed.**

## The census (A3a)

| | |
|---|---|
| findings documents swept | **25** |
| candidate mechanism claims | **123** (gate needed ≥20 — **PASS**) |
| of which near a headline (candidate load-bearing) | **24** |
| documents with hits | 25 (i.e. all of them) |

Connectives: `because` 35 · `why` 32 · `mechanism` 29 · `therefore` 14 · `the reason` 5 · `since` 5 ·
`hence` 5 · `explains` 2 · `due to` 1.

## The classification (A3b) — and the split that actually matters

Most near-headline hits are **MEASURED** (backed by our own numbers) or self-referential section headings.
The risk does not live in prose generally; it lives in one specific category. Sorting every external-authority
mention in the corpus:

| category | how the claim is backed | examples | risk |
|---|---|---|---|
| **REPRODUCED** | we measured it ourselves | Srednicki (M2a anchor: κ = 0.3014 ∈ [0.28, 0.32]) · GWW (K2's convergence run) · **Legendre (S2: "verified, not invoked" — exhaustive integer search)** | none — the strongest form |
| **READ** | primary source fetched/quoted | Cerviño–Hein (S1, transcribed from the PDF) · Oellerich & Emelianenko, Ray 2026 (M6, today) · Galajinsky (the Candidate-B un-blind) | low |
| **RELAYED / REMEMBERED** | **neither reproduced nor read** | **Collinson / Dietz–Rüdiger** · Witten's no-go · **Casini–Huerta (R6 — inverted)** · Collins–d'Inverno–Vickers · Longo's theorem statement | **live — R6 is the proof** |

**The mechanical metric:** across findings documents and both ledgers, **6** external-authority mentions
carry a resolvable identifier (arXiv / DOI / journal + volume) and **96** do not. The raw ratio overstates
the problem — many of the 96 are repeat mentions, and several are *reproduced*, which beats a citation. But
it locates the exposure precisely: **the RELAYED/REMEMBERED row is where R6 came from, and nothing in our
process distinguishes it from the rest at write-time.**

## The new instance (A3c — the kill)

> **L1, `FALSIFICATION_V2.md`:** *"KY⇔legible held 8/8 only because Collinson/Dietz–Rüdiger force KT⇒KY on
> type-D vacua — the catalog's restriction manufactured the coincidence."*

This is the stated reason the G2 kill was structurally predictable — the first lesson of the v2 ledger, and
the justification for the whole "designed adversaries" programme. It appears in `FALSIFICATION_V2.md:16`,
`FALSIFICATION_LEDGER.md:248`, `JOURNAL.md:1098`, `G2/FINDINGS.md:40` and `G2/results/G2_candidate_A_SEALED.json`.
It **originated in ansatz's sealed record** and we propagated it verbatim. Not one instance carries a
journal, volume, DOI, or arXiv ID, and no document anywhere records that we read it.

**Verified today, and it holds:** Collinson, C. D. (1976), *"On the relationship between Killing tensors and
Killing–Yano tensors,"* **Int. J. Theor. Phys. 15, 311–314** — all type-D vacuum solutions admitting a Killing
tensor also admit a Killing–Yano tensor. Companion: Dietz & Rüdiger (1981), *"Space-times admitting
Killing–Yano tensors,"* **Proc. R. Soc. Lond. A 375, 361**. References now added at every site.

**One qualifier flagged OPEN, not asserted:** the adjacent literature on separability structures in type-D
vacua states equivalences conditioned on the spacetime being **without acceleration**. Whether Collinson's
result carries that condition is *not settled by what we read today*. Our catalog (Schwarzschild, Kerr, KN,
KdS, Taub–NUT) is acceleration-free, so **L1's use is sound for our catalog either way** — but the blanket
phrasing "on type-D vacua" may be missing a hypothesis. Flagged, not resolved; resolving it needs the primary
text, which is paywalled.

**Why this counts as KILLED under the frozen gate.** A3c specified: *KILLED iff ≥1 new load-bearing
ASSERTED-UNVERIFIED claim is found.* One was. The gate turns on **whether it was verified, not whether it
was right** — and that is the correct reading, because:

> **R6's unverified structural claim was inverted and sat in a title for two days.
> L1's unverified structural claim was correct and has sat in the ledger for weeks.
> We did the same thing both times. We got a different result both times, by luck.**

A process that produces a correct claim by luck is not a process that produces correct claims.

## A second observation the sweep forced

**The claim came from a sister, and we adopted it without independent check.** L5 says independence pays
because neither repo can catch its own bugs — but that only works if the receiving repo actually *checks*
rather than *relays*. Round 8 imported ansatz's justification into our ledger's first lesson in one hop, with
no verification step in between. **Cross-repo propagation is a channel for unverified claims to acquire the
appearance of corroboration** — it looked like two repos agreeing when it was one repo asserting and one
repeating. Worth naming, because our whole method rests on independence being real.

## The payout (A3d) — the standing rule, adopted

> **Every mechanism or external-authority claim in a findings document carries one of:
> (a) a number from our own results, (b) a resolvable identifier for a source we actually read, or
> (c) an explicit `[asserted, unverified]` tag.**

Option (c) is not a defeat — it is *cheap and honest*, and it makes the next R6 visible at write-time rather
than two days later via a sister. The three-way categorisation above (REPRODUCED / READ /
RELAYED-REMEMBERED) is the working form of the rule, and **REPRODUCED beats CITED**: S2's *"Legendre's
criterion verified, not invoked"* and M2a's Srednicki anchor are the models to copy.

Baseline for the next audit: **6 / 102** mentions currently resolvable.

## Honest scope

- **An audit of our own documents.** No new physics; the value is one caught claim plus a write-time guard.
- **Completeness ceiling:** the census only finds claims phrased with the nine listed connectives. Mechanism
  claims made without them are invisible to it — stated, not claimed away.
- **This audit was not blind** — R6 and M6 were known and are excluded from the "new" count, which is why
  the gate turns on what the sweep found *beyond* what prompted it.
- The Collinson verification rests on secondary sources describing the result, not the paywalled original;
  the acceleration-free qualifier is explicitly left open rather than guessed. **This document's own
  citation is therefore READ-at-second-hand, and says so.**
- Bridge-solo; read-only over our own docs.

## Inputs & artifacts

`code/mechanism_census.py` (mechanical enumeration; classifies nothing) · `results/mechanism_census.json`
(123 candidates). Prompted by the same-day retractions of [M6](../M6_prior_art_gate/FINDINGS.md) and
[R6](../R6_arealaw_log/FINDINGS.md). Follows [A1](../A1_tooclean_audit) and [A2](../A2_wall_audit).
