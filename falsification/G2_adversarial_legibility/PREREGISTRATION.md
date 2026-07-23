# G2 — Pre-registration: does "legible ⟺ KY-integrable" survive adversarial metric design?

*Frozen 2026-07-23, **before either sister is asked to build or run anything**. Ledger item G2 (Tier G — the
family's flagship claim under deliberate attack). This document fixes the joint gate in advance precisely so
that nobody — bridge or sister — can move a goalpost once the verdicts start arriving.*

## The claim under attack

[Leg Q](../../legQ_geometrizes_integrability) established, across two **methodologically independent**
instruments:

> **a learned geometry is legible ⟺ the metric is KY-integrable** — 8/8 metrics, Matthews φ = 1.0, with three
> independent non-integrable deformation classes (axisymmetric bump · ZV γ-metric δ=2 · Manko–Novikov q=0.5).

tabula's neural probe emits a verified hidden invariant for exactly the metrics leg O's symbolic Killing–Yano
survey finds integrable, and certifies "no invariant" for exactly the ones it finds non-integrable.

**But every one of those 8 metrics was found, not designed.** Nobody has ever built a metric *specifically to
break the biconditional*. G2 does that.

## What the equivalence could actually be tracking

The 8/8 record is consistent with three distinct hypotheses that the existing catalog cannot separate,
because in every entry so far KY-ness, integrability, and polynomial-invariance coincide:

| hypothesis | legibility really tracks … |
|---|---|
| **H_KY** | Killing–Yano structure specifically (the antisymmetric root, §69's Y with K = Y·Y) |
| **H_INT** | integrability — *any* Killing tensor, KY root or not |
| **H_POLY** | the existence of a **polynomial**-in-momenta invariant, whatever its geometric origin |

Two designed metrics separate them.

## The two adversarial candidates (what ansatz is asked to build)

- **Candidate A — integrable, but with NO Killing–Yano root.** A metric admitting an irreducible Killing
  tensor (rank 2 or rank 4) that is **not** the square of any Killing–Yano tensor. Integrable ✔, polynomial
  invariant ✔, KY ✘.
- **Candidate B — integrable, but with a TRANSCENDENTAL invariant.** A metric/Hamiltonian in our reach whose
  conserved quantity is **not polynomial in the momenta**, with polynomial invariants of degree ≤ 4 excluded.
  Integrable ✔, polynomial invariant ✘, KY ✘.

## The frozen decision table

tabula returns **legible** (emits a verified invariant) or **illegible** (certifies none), blind. Then:

| candidate | tabula says | conclusion (frozen now) |
|---|---|---|
| **A** (KT, no KY) | **legible** | **G2 KILLED.** Legibility does *not* require KY — the biconditional as stated is false, and legibility tracks integrability/polynomial structure instead. |
| **A** | **illegible** | **G2 survives its strongest attack.** Legibility genuinely tracks **KY specifically** (H_KY), not mere integrability — a real sharpening of the claim. |
| **B** (transcendental) | **illegible** | Supports **H_POLY**: legibility tracks *polynomial* invariants. The claim must be restated as "legible ⟺ polynomial-invariant-integrable". Consistent with, but weaker than, the KY reading. |
| **B** | **legible** | **Striking capability result**: tabula's distillation head found a non-polynomial invariant. Kills H_POLY and would need its own prior-art sweep before any claim. |

**G2 verdict rule (frozen):** G2 is **KILLED** if either candidate breaks the biconditional — i.e. a metric is
legible without being KY-integrable, or KY-integrable without being legible. G2 **SURVIVES-9/SURVIVES-10** only
if the biconditional holds on both new entries as well. **UNDECIDED** is a legitimate outcome for any candidate
that cannot be constructed, or on which either instrument walls.

## The blind protocol (non-negotiable — it is the whole asset)

1. **ansatz** constructs each candidate and computes its symbolic verdict (Killing tensor rank; KY exists or
   not; the explicit invariant). It ships the **metric only** — plus whatever tabula needs to build a geodesic
   Hamiltonian — to the bridge.
2. The bridge **seals** ansatz's symbolic verdict without showing it to tabula.
3. **tabula** runs its emit-or-certify legibility instrument **blind**, exactly as in §127/§132/§144, and
   reports legible/illegible with its own numbers.
4. The bridge **unseals and joins**, and applies the table above.

The two repos are kept ignorant of each other by design — that independence is why an agreement counts as
evidence rather than an echo. Any leakage of ansatz's verdict to tabula before step 3 **voids the round**.

## Honest limits (fixed in advance)

- A kill here is the *valuable* outcome and is stated as such in advance: it would **localize** what legibility
  actually tracks, which the ledger itself judges "arguably more valuable than the survival."
- Constructibility is a real risk: Candidate A (a Killing tensor with no KY root) and Candidate B (a
  transcendental invariant in a *geometric* setting) may not be reachable in the one-variable ansatz world.
  **UNDECIDED-by-construction is an acceptable, pre-registered outcome** — the ask is bounded, not open-ended.
- Even a survival earns only "SURVIVED-9/10 against designed adversaries", never proof. The prior-art sweep
  stays mandatory before anyone gets excited.
- Legibility is tabula's *instrument-relative* notion (emit-or-certify at their stated thresholds); a kill or
  survival is a statement about that instrument, and is labelled so.

## Anchors (read-only)

[leg Q](../../legQ_geometrizes_integrability) (the 8/8 record) · [leg O](../../legO_catalog_survey) (symbolic KY
survey) · [leg J](../../legJ_integrability_frontier) · ansatz §69 (Killing–Yano), §97/§98 (quadratic and
quartic Killing-tensor searches), §99 (MN no-Carter) · tabula §127/§132/§144 (legibility instrument).
Sister asks: [SISTER_ASKS.md](SISTER_ASKS.md).
