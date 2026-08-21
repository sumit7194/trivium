# T2 — Pre-registration: independent negative control for tabula's conditioned degree-6 rung

*Frozen 2026-08-21 before `code/t2_null.py` is written or run. Requested by tabula after their SVD
conditioning bought 16 orders at degree 6. Bridge-solo; **I did not build the conditioning**, which is the
point.*

## The question

tabula's conditioning recovered 9.85e-10 → 4.30e-26 on a known positive (H2) at degree 6, dimension
unchanged. Their null check used **B's own pinned ensemble** — which is the substrate the verdict is issued
on, and therefore the strongest form — but it shares everything with the verdict and cannot rule out a
failure specific to that ensemble. This runs the same question on an **unrelated chaotic substrate**.

**Chaotic Hénon–Heiles**, `H = ½(pₓ²+p_y²) + ½(x²+y²) + x²y − y³/3`, at E₀ near the escape energy 1/6
where the chaotic sea dominates and **no second invariant exists**.

**The only question asked: does anything cross the 1e-10 emit threshold?**

## One addition beyond tabula's spec, and it is the point of running it here

tabula asked for the null alone. **This runs the same substrate BOTH ways**, which their setup cannot do:

- **PINNED shell** (E₀ fixed) — the null. H has no across-ensemble variance so it is invisible, and there
  is no second invariant. **Nothing should emit.**
- **VARIED shell** (E₀ spread) — the positive. H acquires across-ensemble variance and becomes findable.
  **H should emit.**

A null on its own cannot distinguish *"correctly found nothing"* from *"pipeline is broken on this
substrate."* Running both on the *same* orbits makes the null interpretable, which is precisely the
"demonstrate the readout detects a positive on the substrate where the null is issued" discipline that
started this exchange.

## Frozen gates

- **T2a — positive control (must pass first).** On the VARIED-shell ensemble the conditioned degree-6
  pipeline must emit, i.e. return a best out-of-sample ratio **< 1e-10**, with the recovered direction
  overlapping H. **If it does not, my pipeline is not tabula's and T2b says nothing about their result.**
- **T2b — the negative control (the deliverable).** On the PINNED-shell chaotic ensemble the conditioned
  degree-6 pipeline must **NOT** cross 1e-10.
  - **PASS (supports tabula)** iff best ratio **> 1e-10** — conditioning does not manufacture emissions.
  - **FAIL** iff anything crosses 1e-10 — the threshold has moved with the conditioning and must be
    re-derived at the conditioned resolution rather than inherited.
- **T2c — conditioning must be reported both ways.** Report unconditioned and conditioned side by side.
  The claim under test is *"rescaling amplifies signal, not noise"*, so the **movement** on the null is the
  quantity of interest, not the absolute value. tabula measured 12% on their null against 16 orders on
  their positive; a comparable asymmetry here corroborates, a large movement on my null does not.

## Declared in advance

- **Island contamination biases toward emission, so a T2b pass is conservative.** At E₀ near 1/6 the
  chaotic sea dominates but regular islands survive, and an island orbit genuinely has a second invariant.
  If such orbits are in the ensemble they make emission *more* likely, so **non-emission is the safe
  direction to be wrong in.** An emission would be ambiguous between "conditioning manufactured it" and
  "islands supplied a real invariant", and would be reported as ambiguous rather than as a FAIL.
- **I have tabula's numbers** (null 2.58e-05 → 2.29e-05, 12% movement; positive 16 orders). Reproducing
  them is not a goal; my substrate is different by design. **Disagreement is informative.**
- Velocity-Verlet, matched to tabula's spec: ~70 trajectories, dt = 0.02, 2500 steps, 150 burned,
  train/test split over **trajectories**. Basis: momentum monomials to degree 6 × coordinate monomials to
  degree 2, per tabula's stated library cap. Conditioning: SVD rescaling, tol = 1e-11, **dimension
  unchanged** — rescaling, not truncation.
- **Live outcomes:** (a) T2a passes, T2b passes ⇒ independent corroboration on an unrelated substrate;
  (b) T2a passes, T2b fails ⇒ the emit threshold needs re-deriving and tabula's degree-6 demonstration is
  back in question; (c) T2a fails ⇒ my pipeline differs from theirs and this says nothing either way.
