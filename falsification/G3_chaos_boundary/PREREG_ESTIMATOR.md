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

---

# RESULTS — 2026-08-16. **The replacement FAILS its own gates. Outcome (c).**

45 fresh orbits (23 at δ=2.0, 22 at δ=1.0), crossing series persisted, **both estimators scored on the
identical orbits** so every comparison below is like-for-like.

| gate | result |
|---|---|
| **E1** — synthetic floor must improve ≥10× | **FAIL** — NAFF 1.22e-05 vs FFT 5.17e-06. *Worse.* |
| **E2** — must not silence §106's layer | **PASS**, both estimators |
| **E3** — control must go quiet and the ordering invert | **VOID as specified** — my grid error, see below. Valid only as an estimator comparison. |
| **E4** — two-sample discrimination (L13) | **FFT PASSES (p=0.0404), NAFF FAILS (p=0.5368)** |

**All four were required. NAFF fails E1 and E4. It is not the fix.**

## E2 — PASS. The positive control holds.

| x₀ | ncross | escaped | FFT | NAFF |
|---|---|---|---|---|
| 8.044 | 84 | ✓ | 2.61e-02 | **2.99e-02** |
| 8.048 | 83 | ✓ | 2.10e-02 | 1.12e-02 |
| 8.050 | 144 | ✓ | 2.06e-02 | 2.01e-02 |

Three escaping orbits bracketing §106's quoted 0.027. **NAFF reports the layer slightly louder, not
quieter** — it does not achieve a low floor by going deaf, which was the failure mode E2 existed to catch.

## E3 — VOID as specified. My error, disclosed.

The fine window was placed at x₀ ∈ [9.600, 9.624]. **δ=1.0's separatrix is at 9.66667**, so the dense
sampling missed it entirely and no orbit above 9.64 survived. The original run sampled ±0.1 around 9.66667
at step 0.002. **These are not the same population**, so the observed control max/median of 187.3 cannot be
compared with the run's 2980, and no conclusion about "the control going quiet" is drawn.

What remains valid is the **like-for-like estimator comparison on identical orbits**:

| δ=1.0 (22 orbits, 0 escaped) | median | max | max/median | ≥3× median |
|---|---|---|---|---|
| FFT | 6.16e-06 | 1.154e-03 | **187.3** | 7/22 |
| NAFF | 2.22e-05 | 5.596e-04 | **25.2** | 6/22 |

**NAFF's max/median on an integrable metric is 7.4× tighter** — genuinely less spurious structure where
true drift is exactly zero. That is real and in NAFF's favour.

## E4 — the decisive failure, and it inverts the expected direction

Two-sample KS on log₁₀ drift, δ=2.0 (contains the layer) vs δ=1.0 (integrable):

```
FFT :  KS = 0.387,  p = 0.0404   SEPARATES
NAFF:  KS = 0.217,  p = 0.5368   does NOT separate
```

**The incumbent discriminates and the replacement does not.** The mechanism is the one already documented:
NAFF's floor on the control is 3.6× higher (2.22e-05 vs 6.16e-06), because it measures the true incoherent
error while the FFT peak's coherent bias cancels in the half-split. That inflated floor pushes NAFF's
control distribution up into the δ=2.0 distribution and destroys the separation.

⚠️ Both p-values are marginal at n≈22 and neither would survive correction for multiple comparisons.
**E4 should be read as "NAFF does not demonstrate discrimination," not as "FFT is validated."** FFT's
p=0.0404 is itself a cross-δ comparison and therefore subject to the very gain distortion documented in
FINDINGS — it cannot be ruled out that part of that separation *is* the artifact.

## What this means

**The two properties are in genuine tension, and NAFF trades the wrong one.** It buys gain stability
(spread 0.025 vs 0.839) and a tighter control (25 vs 187); it pays with a 3.6× higher floor, and at these
sample sizes the floor is what decides discrimination. **The incumbent's gain instability remains real and
unaddressed** — NAFF is simply not the way to address it.

**The untested half of the original prescription is the one that should have gone first.** FINDINGS item 1
named *"a proper frequency-analysis method **or far longer records**."* Only the first was tried. Longer
records attack **both** defects at once: the FFT interpolation bias scales with bin width ~1/N, so more
crossings shrink the floor *and* flatten the gain variation, with no change of estimator and no new
failure modes. **That is the next thing to try, and it was available all along.**

*Caveat carried forward: E5's gain measurement is synthetic, and gain cannot be measured on real orbits at
all — measured drift = gain × true drift + noise, and on real data the true drift is unknown by
construction. Non-escaping orbits have true drift ≈ 0, so gain multiplies nothing and the effect is
structurally undetectable there. A real-orbit check at δ=2.0 came back ρ = −0.114, p = 0.631, which is
therefore uninformative rather than refuting.*
