# K5 — Findings: a net CAN hear the shape of a drum (eigenfunctions leak through projections)

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
