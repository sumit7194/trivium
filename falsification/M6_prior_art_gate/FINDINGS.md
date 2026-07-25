# M6 — Findings: KILLED by its own gate. The prior-art sweep closes the write-up, and hands us an instrument upgrade

> ## ⚠️ AMENDED same day (2026-07-26) by [R7](../R7_emit_threshold/FINDINGS.md) — one claim below was wrong
>
> This document asserted, **from reading the literature and without running anything**, that *"O4 is not an
> obstruction we discovered — it is our fixed `τ_rel = 1e-6` being the wrong kind of threshold,"* and that a
> noise-calibrated cutoff would *"dissolve it rather than guard against it."*
>
> **R7 tested that and it is false.** The degree-6 false positive passes the noise-calibrated cutoff by
> **28×** (σ_min 1.07e-5 vs cutoff 2.99e-4). O4's signal sits **five orders of magnitude above the measured
> noise floor** (ε = 3.8e-10) — it is an *approximation* phenomenon, not a noise phenomenon, so no threshold
> of the form "is σ_min small enough?" can catch it. Only generalisation can: held-out scoring degrades the
> degree-6 arm **684×** while the true invariant holds at 8.76e-11.
>
> **Retracted:** "the threshold is the defect" and the recommendation to replace `τ` as the fix for O4.
> **Stands:** everything else — **M6 remains KILLED**, the emit⟺span statement is still prior art, O4's
> phenomenon is still known to the literature, and Ray 2026's constancy-gate + diversity-filter is still the
> right answer — now understood as the *only* right answer rather than a belt-and-braces extra.
> **Corrected below** at both points, with the original wording struck rather than deleted.

*Run 2026-07-26. M6 was entered on the v2 moonshot board as "the family's first candidate for a genuinely
publishable **methods** result — **prior-art sweep is the gate**." The sweep was run. **The gate is not
passed.** Recorded as the gate working, not as a disappointment.*

## What M6 proposed

Carry **R2** to a full write-up: the theorem *"emit succeeds ⟺ the invariant lies in the span of the probe
basis"*, with G2/R1's measurements as its experimental section, plus **O4** — the obstruction R2 found, where
a degree-6 polynomial **falsely emitted** (σ_min/σ_max = 2.7×10⁻⁷, under our τ = 10⁻⁶) by *approximating* a
transcendental invariant with no true invariant in its span, caught only out-of-sample.

## Verdict: KILLED — both halves are prior art, and the literature is ahead of us on both

### Half 1 — the "emit ⟺ span" theorem is known, and known more sharply

**Oellerich & Emelianenko**, *Towards Robust Data-Driven Automated Recovery of Symbolic Conservation Laws
from Limited Data* ([arXiv:2403.04889](https://arxiv.org/abs/2403.04889)) uses **the same instrument we
built independently** — candidate library → design matrix → SVD → near-null singular value — and states the
failure condition explicitly as a trichotomy:

> *"If the process fails to produce a σᵢ≈0, then there are three possibilities: (1) the starting library does
> not contain the appropriate terms, (2) inadequate data due to noise or amount, or (3) the system does not
> contain a conservation law."*

Possibility (1) **is** our theorem. And their treatment is **strictly sharper than ours in two ways**:

| | ours (R2) | Oellerich & Emelianenko |
|---|---|---|
| emit threshold | fixed `τ_rel = 1e-6`, chosen by hand | **noise-calibrated**, `σ_cutoff = √(Np)·‖ε_x‖^{2/3}_max`, from perturbation theory (their Cor. 4.2) |
| library choice | fixed basis per run | **spectral-gap criterion** — maximise `δ = σ_{j−1} − σ_j`, letting the data pick the library |

A fixed hand-chosen threshold is exactly what O4 exploited. Their threshold is derived from the noise level;
ours is not. Separately, the broader SINDy identifiability literature establishes **necessary and sufficient
conditions for one-step support recovery**, which is the same question with rigour we did not attempt.

### Half 2 — O4 is known, and there is a 2026 paper devoted to defeating it

**Ray**, *From Data to Laws: Neural Discovery of Conservation Laws Without False Positives*
([arXiv:2603.20474](https://arxiv.org/abs/2603.20474), 20 Mar 2026). Its abstract names failure
modes adjacent to ours as the problem it solves — *"parameter variation, **non-polynomial invariants**, local minima, and
**false positives**"* — and its pipeline includes:

- **log-basis Lasso** — the log-augmented basis tabula tried in R1 and that I described to them today as the
  fix for Candidate B. Published.
- **a constancy gate plus diversity filter to remove spurious laws** — this is precisely the "validate
  out-of-sample" guard I proposed for O4, formalised.
- reported **FDR = 0.0 / F1 = 1.0 on the four systems that have true conservation laws** (nine is the
  benchmark size, not the scored set) — *corrected by ansatz, who pulled the full text; our first
  wording said "across nine systems" and overstated it.*

**Scope correction (ansatz, from the full text):** Ray targets false positives on chaotic systems
*generally*, and does **not** address O4's specific mode — a high-degree polynomial hugging a
*transcendental* invariant over *bounded* data. **O4 is therefore ADJACENT to Ray, not squarely
covered by it.** This does not revive M6 (the emit⟺span half is independently dead, and O4's *phenomenon*
is known), but the ledger must say "adjacent" rather than "targets O4 directly." Combined with
[R7](../R7_emit_threshold/FINDINGS.md) — which showed O4 survives noise calibration and is a real
obstruction — the honest position on O4 is: **a real, sharply-characterised failure mode that the
literature brushes past rather than solves.** Not a paper; worth a line in anyone's methods section.

The wider literature is blunter still: overcomplete polynomial libraries are strongly collinear, and
*"no regularisation tuning can provide a formal guarantee on the rate of false discoveries."* O4 is not an
unnoticed obstruction. It is a known, named, actively-attacked property of this class of method.

## What survives, and what does not

**Does not survive:** any external-publication claim. There is no methods paper here. M6 comes off the board.

**Survives untouched:** R2's **internal** value. The cross-gate closure — the bridge independently
reimplementing ansatz §123's emit criterion, in its own code, and reproducing all four teeth — was never a
novelty claim. It is *cross-validation between two deliberately independent implementations*, and that is
worth exactly what it was worth yesterday. Likewise O4 remains a real finding **about our own instrument**;
it simply isn't a finding about the field.

**This is the gate doing its job.** M6 was admitted to the board *conditionally*, with the sweep named as the
condition, precisely so that this outcome was available. Running the sweep and reporting a kill is the
cheapest possible way to not write a paper that would have been scooped four times over.

## The payout — an instrument upgrade we should actually take

By [A2's taxonomy](../A2_wall_audit/FINDINGS.md) this is a **species-1 (precision/instrument) wall**: the
prescription is *keep pushing — upgrade the instrument*. Three concrete upgrades, all from the sweep:

1. **Replace our fixed `τ_rel = 1e-6` with a noise-calibrated cutoff** (Oellerich & Emelianenko Cor. 4.2).
   Our threshold is the thing O4 slipped under; theirs is tied to the actual noise floor.
2. **Adopt the spectral-gap library criterion** (`max δ = σ_{j−1} − σ_j`) instead of a hard threshold on
   `σ_min/σ_max`. It answers "which basis?" with data rather than by hand.
3. **Adopt a constancy-gate + diversity-filter guard** (Ray 2026) as the standing O4 defence, in place of my
   ad-hoc "use out-of-sample orbits."

## Independent convergence: tabula already had the literature's guard

Received the same day (tabula §164, commit `f9a8205`), and it sharpens the kill rather than softening it.
tabula ran both proposed tests on Candidate B:

- **Test 1 — emits.** Adding `{p_y/p_x, ln p_x}`: held-out **1.8×10⁻²⁹**, recovering the *literature
  direction* at cosine **1.0000** — not merely "something conserved." Correctly labelled a consistency
  check, not evidence.
- **Test 2 — never converges**, as the grading theorem requires: deg 2/4/6/8 → 1.3e-3, 2.0e-4, 2.6e-5,
  5.6e-6, monotone, still **10²³×** above the emitting arm at degree 8.
- **O4 reproduced.** At degree 8 the **in-sample** ratio is **9.9×10⁻⁷ — it crosses the 10⁻⁶ line** — while
  the same directions score 5.6×10⁻⁶ held-out. Same phenomenon and same order as our degree-6 2.7×10⁻⁷.

**The point for M6:** tabula's harness has been **held-out by construction since §161**, so O4 never bit
them. They arrived independently at the same guard the literature formalises as Ray 2026's constancy-gate +
diversity-filter. Three independent arrivals at one guard — ours (ad-hoc), tabula's (architectural), and the
literature's (formal) — is strong evidence that this is settled practice, not an open problem. It closes the
last corner where M6 might have claimed contribution.

~~**It also relocates the real defect, which is ours.** O4 is not "an obstruction we discovered"; it is our
fixed `τ_rel = 1e-6` being the wrong kind of threshold. The literature's answer — a noise-calibrated cutoff
(Oellerich & Emelianenko Cor. 4.2) — dissolves it rather than guarding against it.~~
**❌ RETRACTED by [R7](../R7_emit_threshold/FINDINGS.md).** The noise-calibrated cutoff lets O4 through by
28×. **O4 is a real obstruction of the method**, and tabula's degree-8 crossing is the same real obstruction
from the other side, not a shared threshold artifact. The correct reading: three independent arrivals at a
**generalisation** guard (ours ad-hoc, tabula's architectural, Ray's formal) is convergence on the *only*
defence available, because the approximation/representation distinction is invisible in-sample by
construction.

## Correction owed to tabula

Three corrections, all in our direction:

1. **There is published machinery for both** the log-momentum basis (Ray 2026's *log-basis Lasso*) and the
   O4 guard (*constancy gate + diversity filter*). They should be pointed at it rather than reimplementing
   what exists. The R1 physics — B's transcendence lives in the momenta — is unaffected; only the
   "how to build the guard" advice changes.
2. ~~**The threshold, not the trap, is the defect.** Recommend both repos move off a hand-set `τ = 1e-6` to a
   noise-calibrated cutoff.~~ **❌ RETRACTED by [R7](../R7_emit_threshold/FINDINGS.md) — this advice was
   wrong and must not be acted on for O4.** The noise-calibrated cutoff is *more* permissive here (it lets
   the degree-6 arm through by 28×). **tabula's held-out-by-construction harness is the correct primary
   gate and should be kept.** The noise-calibrated cutoff is still worth having for genuinely noisy data —
   a different problem.
3. **A misattribution to correct, in their favour.** tabula credited us with a *"probe with `p_x > 0`"*
   instruction — *"that instruction was doing quiet work."* **We never wrote it.**
   [UNBLIND_B.md](../G2_adversarial_legibility/UNBLIND_B.md) contains no such note, and it should have: both
   atoms `p_y/p_x` and `ln p_x` are singular at `p_x = 0`, so a probe straddling it is meaningless. tabula
   derived that constraint themselves and enforced it (min `p_x` = 0.046). **The credit is theirs, and they
   should log it as their own contribution, not ours** — otherwise a real robustness condition gets recorded
   against the wrong repo and disappears from their instrument's provenance. Our un-blind is amended to carry
   the condition *with attribution*.

## Sourcing discipline

**Fetched and verified directly** (title, authors, abstract read): [arXiv:2305.19525](https://arxiv.org/abs/2305.19525)
(Liu, Sturm, Bharadwaj, Silva, Tegmark — SID) · [arXiv:2403.04889](https://arxiv.org/abs/2403.04889)
(Oellerich & Emelianenko) · [arXiv:2603.20474](https://arxiv.org/abs/2603.20474) (Ray).
**Search-result only, not independently fetched** — flagged as such rather than cited as read:
[arXiv:1811.00961](https://arxiv.org/abs/1811.00961) (Kaiser, Kutz & Brunton, Koopman/conservation laws) ·
[arXiv:2004.02322](https://arxiv.org/abs/2004.02322) (SINDy-PI, implicit null-space ill-conditioning) ·
the SINDy identifiability and overcomplete-library-collinearity results quoted above.

Note on cutoff: Ray 2026 postdates my knowledge cutoff, so it was found by search and verified by fetch, not
recalled. The SID paper's abstract page did not itself contain the span-condition discussion; the claim that
SID does not state it explicitly is therefore **weak evidence** (abstract-level), and the load-bearing prior
art for half 1 is Oellerich & Emelianenko, whose statement was read directly.

## Honest scope

- This is a **literature gate**, not an experiment. No new measurement was made.
- The sweep is not exhaustive — it establishes *sufficient* prior art to close M6, which is all a kill needs.
  A more complete survey could only strengthen the kill, not reverse it.
- Nothing here impugns R2's correctness; it bears only on **novelty**, which is a different property and the
  only one M6 depended on.

## Inputs & artifacts

`results/prior_art.json` (the citation record with fetched/search-only status per item). Kills **M6**
([FALSIFICATION_V2.md](../../FALSIFICATION_V2.md)). Bears on [R2](../R2_emit_theorem) (internal value
unaffected) and on the [G2 un-blind](../G2_adversarial_legibility/UNBLIND_B.md) (guard advice amended).
