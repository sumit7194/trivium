# G3 — Pre-registration: replacing the drift estimator

*Frozen 2026-08-16, **before `code/naff_drift.py` is written or run.** New file; additive. The G3 gates in
[PREREGISTRATION.md](PREREGISTRATION.md) are untouched and the completed run in
[FINDINGS.md](FINDINGS.md) is not revisited — this pre-registers the **instrument replacement** named as
item 1 of that document's forward-look.*

## Why

[FINDINGS](FINDINGS.md) established that `drift()`'s floor is **FFT peak-estimation sampling variance, not
dynamics**: fed synthetic quasiperiodic series with true drift identically zero, it returns median
4.9e-06 against the run's own δ=1.0 floor of 2.9e-06 — reproduced within 2× with no metric, no integrator
and no force. Consequently the drift conjunct is uninformative (pass fraction 35–43% at *every* δ; KS
separates no pair; Spearman ρ=+0.089 against |δ−1|), and eight of nine δ rank at or below the integrable
control on the statistic the fire rule uses.

**The named fix is a better frequency estimator, not a better integrator.** Nothing about symplectic
methods or extended precision touches a peak-estimation floor.

## What is being built

A **NAFF-style** estimator (Laskar's Numerical Analysis of Fundamental Frequencies): instead of taking the
interpolated FFT bin peak, refine ω by **maximising the Hanning-windowed Fourier amplitude
|Σ x(t)·w(t)·e^{−iωt}|** over a continuous ω, seeded at the FFT peak. The textbook motivation is the
convergence rate — a Hanning-windowed refined estimate converges as ~1/N⁴ against ~1/N² for a plain peak.
*[asserted, unverified] per **L10** — the claim enters here only as motivation; the gates below measure our
own floor directly and never rely on it.*

Same input, same interface, same `|f₁ − f₂| / max(f₁, f₂)` half-split comparison. **Only the frequency
estimate changes**, so the comparison against the existing estimator is like-for-like.

## Frozen gates

- **E1 — the synthetic floor must drop, and by a stated margin.** On the *identical* synthetic
  zero-true-drift series used in FINDINGS (3 incommensurate tones, N=200, 400 draws), the new estimator's
  **median** and its **max/median** must both fall below the current estimator's. **PASS requires ≥10×
  improvement in the median floor.** Anything less is not worth a rescan and will be reported as such.
- **E2 — it must not silence a real signal (the positive control, and the decisive gate).** Applied to
  freshly integrated orbits, the new estimator must **still find §106's δ=2.0 layer at x₀ ≈ 8.0369 /
  8.0409** — the one solid positive this item has. **An estimator that quiets everything is not an
  improvement, it is a broken instrument that happens to agree with our null.** This is the same logic as
  G3b, applied to the instrument rather than the physics.
- **E3 — the integrable control must go quiet.** At δ=1.0 (Schwarzschild, **true drift exactly zero**) the
  new estimator's max/median must fall **materially** below the current 2980, and must sit **below** the
  δ=2.0 value from E2. **The current ordering — control ranking 2nd of 8, above six deformed spacetimes —
  must invert.** If the control stays loud, the floor was never the estimator and this diagnosis is wrong.
- **E4 — discrimination, per L13.** Report the **two-sample** comparison (KS) of the drift distribution at
  δ=2.0 against δ=1.0, using the new estimator. **Aliveness is not discrimination**: a non-degenerate
  spread that overlaps the control gates nothing. This is the check that would have caught the old
  estimator on day one, and it is now applied to its replacement before any claim is made.

**All four are required.** E1 alone would be a numerical curiosity; E1+E2+E3 without E4 would repeat this
item's central mistake.

## Declared in advance

- **Crossing series will be persisted this time** (item 4 of the FINDINGS forward-look). The current
  records store only summary fields, which is why tonight's re-analysis needed re-integration at all.
- **Cost is bounded and stated up front:** δ=1.0 and δ=2.0 only, reduced orbit counts, no full ladder. A
  full rescan is **not** authorised by this document and would need its own budget.
- **Live outcomes, named now.** (a) The estimator improves and the control inverts ⇒ the FINDINGS
  diagnosis is confirmed and a full rescan becomes worth costing. (b) The estimator improves but the
  control stays loud ⇒ **the diagnosis in FINDINGS is wrong**, the residual excess is not peak-estimation
  variance, and that must be recorded as a correction. (c) The estimator does not improve ⇒ NAFF is not
  the fix and the item returns to the sampling-geometry and step-size candidates.
- **Nothing here revisits G3's verdict.** G3 remains KILLED as stated with the boundary UNMEASURED
  regardless of how this comes out.
