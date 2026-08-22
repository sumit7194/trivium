# K5 — Findings: a net CAN hear the shape of a drum (eigenfunctions leak through projections)

> **⚠️ THE NUMBERS BELOW CANNOT BE CHECKED FROM THIS REPOSITORY.** This leg has no code and no
> artifacts — the only one in `falsification/` with neither.
> *(Scope corrected 2026-08-22: I first wrote "the only one of 31", which was a sweep of
> `falsification/` reported as a repo-wide result. A full-repo sweep finds **eight further study
> directories with a FINDINGS and no artifact of any kind** — leg4, leg5, leg5b, leg5c, leg6, leg7,
> leg7b, leg8b, all last touched 2026-06-19. They have code, unlike this one, so their numbers are
> regenerable in principle; none has been regenerated. K5 is unique only in having no code either.)* The separations 0.76 and 0.98 are **tabula's**, relayed
> here and correctly attributed, but nothing here produces them and **if their numbers move or are
> withdrawn, this file will keep asserting them.** Re-request rather than re-cite if you build on this.
> *(Hoisted to the top 2026-08-22: the audit note saying this was at 71% of the document, which is a
> hedge — discoverable, honest, and invisible to the reader it can mislead.)*

*Recorded by the bridge 2026-07-24 from tabula's round-8 run. Ledger item K5 (Tier K). **Verdict: KILLED.**
The test case is the bridge's [K2](../K2_isospectral_drums) drums build — which tabula also found a bug in;
that correction is recorded honestly below and in K2's own findings.*

## The postulate

> **"A neural net trained on projections can learn ONLY the spectrum"** — behavioural data carries no more
> than eigenvalues.

The GWW drums are the ideal adversary: two provably non-congruent domains with **identical spectra**. If a net
can tell them apart from projected/behavioural data, then that data carries strictly more than the eigenvalue
tower — and K5 dies.

## Result

**KILLED.** On a corrected discretisation, tabula's net separates the two isospectral drums at:

| arm | separation |
|---|---|
| shared-interior, position-blind, held-out nodes | **0.76** |
| modal arm | **0.98** |
| eigenvalue tower (control) | chance |
| stripped controls | chance |

The controls are what make it a result: the **eigenvalue tower alone sits at chance**, exactly as the
postulate says it must — the drums *are* isospectral. Yet the projections separate them. So the extra
information is not in the spectrum.

**The mechanism, in tabula's phrase:** *a recording is the spectrum weighted by eigenfunction overlaps.*
Identical eigen**values**, different eigen**functions** — and a projection samples the eigenfunctions. That is
a sharp, mechanistic statement of what representation learning actually accesses, which is precisely the
sharpening K5 was posed to produce.

## The bug in the bridge's test case (found by tabula, confirmed by the bridge)

tabula could not run K5 on the bridge's original K2 build, and correctly diagnosed why: the bridge's grid used
the **same offset in x and y**, so every grid point lying on an internal diagonal was dropped (a strict
in-triangle test puts such points in no triangle). Those dropped lines **disconnected each drum into 3
congruent pieces**, identical between the two drums — the two discrete operators were *one matrix relabelled*
(`max|L₂[P,P] − L₁| = 0` exactly). K5 was untestable on it, and the bridge's own "exact, resolution-independent
isospectrality" was a triviality rather than transplantation.

The bridge confirmed this independently (3 components, sizes 360/360/120 at n=16, component-wise identical
spectra), fixed the grid (distinct offsets so no point can lie on any edge), and added a **connectivity
assertion** as a regression guard. See [K2 FINDINGS](../K2_isospectral_drums/FINDINGS.md) for the full
correction. **Credit where due: the sister caught the bridge's bug — which is exactly what independent
instruments are for.**

## Honest limits

- The result is tabula's, on tabula's instrument, at their thresholds; the bridge records and cross-references
  it rather than re-deriving it.
- tabula flagged that their **D2 raw-waveform drum arm missed its strength gate** — a *learnability* limit, not
  an information one (their fix round demonstrates the distinction). The kill rests on the arms that passed.
- 2D Dirichlet drums remain an *analogy* for a KK mass tower, as frozen in K2 — this says what projections of a
  Laplacian eigenproblem carry, not anything about literal extra dimensions.

## Inputs & artifacts

tabula round-8 §C · the bridge's [K2](../K2_isospectral_drums) drums build (`code/k2_drums.py`, corrected) ·
Gordon–Webb–Wolpert 1992 · Kac 1966.

---

## Audit 2026-08-22 — this leg has no code and no artifacts

Found by applying quantum's §16 check across all 31 legs: **K5 is the only one with a FINDINGS and
neither.** The separations 0.76 and 0.98 are tabula's, correctly attributed here and in the header — but
**nothing in this repository can produce them**, and if tabula's numbers move or are withdrawn, this file
will keep asserting them. That is the hazard logged in `DISCLOSURES.md` today, sitting in a leg from a
month ago: *a cross-check is only as good as the other instrument's current state, and a message freezes
a snapshot of it.*

**Not fixed by writing code here** — reproducing tabula's net is their work, and duplicating it would
produce a second instrument sharing my assumptions rather than a check (§2). What is recorded instead:
these numbers are **relayed, unreproducible from this repo, and should be re-requested rather than
re-cited** if anything is built on them.

**What WAS fixed is the part that was mine.** This leg claims *"the bridge confirmed this independently
(3 components, sizes 360/360/120 at n=16)"* — the number justifying K2's grid-offset correction. It was
**not reproducible from committed code**, because `k2_drums.py` now sets `A_OFF, B_OFF = 0.5, 0.25`:
running HEAD produces the *fixed* build, and the buggy signature cannot be obtained from it.

> **A repair can erase its own justification.** The evidence for a fix usually lives only in the broken
> version, and fixing is precisely what removes the broken version from the repo. quantum's §16 does not
> catch this — the number's producer *was* committed, and then edited so it no longer produces it.

`K2_isospectral_drums/code/bug_regression.py` drives the offsets as a parameter and asserts both
directions, plus whether the guard added to prevent the regression actually fires:

    equal offsets  (0.5, 0.5 )  -> components [360, 360, 120]     bug signature reproduces
    distinct       (0.5, 0.25)  -> components [904]                single connected interior
    connectivity guard fires on the buggy grid     AssertionError: DISCONNECTED into 3 components
    and does NOT fire on the fixed grid

Both directions, because a guard never shown to fail is a decoration. Artifact:
`K2_isospectral_drums/results/bug_regression.log`.
