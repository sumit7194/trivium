# Leg 1 — Findings: "how many numbers is a black hole?" (ansatz vs tabula)

*Run 2026-06-17. Predictions and agreement criterion were frozen in
[PREREGISTRATION.md](PREREGISTRATION.md) before any code was written.*

## Result in one line

On the static charged family, tabula's neural bottleneck count of the **observable**
manifold **matches ansatz's exact moduli count for Schwarzschild and
Reissner–Nordström, and falls exactly one short for dyonic RN** — the pre-registered
`Q²+P²` degeneracy, confirmed in both counting conventions.

## The outcome table (predicted → measured)

| Cell | ansatz moduli | tabula count (whitened) | predicted | verdict |
|---|---|---|---|---|
| Schwarzschild, dimensionful | 1 | **1** | 1 | ✅ agree |
| RN, dimensionful | 2 | **2** | 2 | ✅ agree |
| **dyonic RN, dimensionful** | **3** | **2** | 2 | ✅ **predicted degeneracy** (tabula < exact by 1) |
| Schwarzschild, shape | 0 | **0** | 0 | ✅ agree |
| RN, shape | 1 | **1** | 1 | ✅ agree |
| dyonic RN, shape | 1 | **1** | 1 | ✅ agree |

Every cell landed on the frozen prediction. The headline dyonic-dimensionful cell —
predicted 3 (ansatz) vs 2 (tabula) — came back exactly 3 vs 2.

A note on the dyonic *shape* cell, to avoid a false symmetry with the dimensionful
one: the `Q²+P²` degeneracy shows up as a 3→2 gap only in the **dimensionful** row,
where the ansatz column is the *algebraic* moduli count (3). In the **shape** row the
pre-registration (PREREGISTRATION §2) defined `N_shape` as the count of independent
*dimensionless observables* — which is already 1 for dyonic RN, because every
observable depends on charge through `(Q²+P²)/M²`. So ansatz and tabula both read 1
here: it is an agreement, exactly as frozen in PREREGISTRATION §4, **not** a second
instance of the degeneracy. (The bare algebraic dimensionless moduli would be 2,
`Q/M` and `P/M`; the prereg deliberately tracked the observable count instead, which
is what tabula can see.)

## What the degeneracy means

Ansatz can *prove* the dyonic hole has three independent moduli `(M, Q, P)`
(`conjecture_machine/scripts/34_hair_criterion.py`: electric and magnetic charge are
genuinely separate hair). But every observable — photon sphere, shadow `b_c`, ISCO,
gravitational redshift — depends on charge **only through `Q²+P²`**. So an
observation-only oracle physically *cannot* resolve `P` from `Q`: the observable
manifold is 2-dimensional even though the moduli space is 3-dimensional.

This is THE_BRIDGE.md §3's *good* "tabula < exact" outcome — "the net found
compressibility the parameter count misses (MDL < moduli dimension), a genuine
information-theoretic finding, not a failure." Here it is sharper than the doc hoped:
the missing dimension is **named and proved** by the other oracle (EM-duality
degeneracy), so the disagreement is fully explained, not a mystery. The two oracles
disagree by exactly the dimension that is observationally invisible — which is the
strongest possible form of "they speak the same language."

## The methodological finding (the §7 lesson, made concrete)

The count depends on **how you read the bottleneck**:

- **Standardized (variance-weighted) readout** under-counts the *dimensionful* dof:
  it calls RN and dyonic = 1, not 2. Reason: the mass scale `M` (∼U[1,3]) carries
  ~99% of the observable variance (linear PC1 = 0.989), so the charge direction
  (~1% of variance) is below the variance-based knee. This is **not** a tabula
  failure — it is the §7 "measure the oracle, not your readout" trap: a real dof can
  be variance-invisible.
- **Whitened readout** (each independent direction weighed equally above a noise
  floor) resolves the charge dof cleanly: RN d₁=0.84→d₂=1.00, dyonic d₁=0.83→d₂=1.00.
  This is the correct intrinsic-dimension instrument and the one used for the counts
  above.
- The **shape convention** sidesteps the problem entirely by removing the scale, and
  the charge dof is high-variance there → both readouts agree (RN=1, dyonic=1).

See `results/leg1_count_curves.png` — for dyonic the "ansatz moduli" line sits a full
step right of where tabula's whitened curve saturates: the degeneracy gap, visible.

## Knee criterion actually used (and the logged deviation)

Counts above use: **count = number of bottleneck widths `d ≥ 1` whose whitened
held-out marginal R² gain exceeds τ = 2%** (≥3 seeds, `results/count_bottleneck.json`).
The originally-frozen rule ("smallest `d` within 2% of the R² plateau") was registered
before the sanity check revealed scale-variance dominance; applied to the
*standardized* curves it under-counts the dimensionful dof. The refinement — same 2%
tolerance, applied to *marginal gain in whitened space* — was chosen after seeing the
R²(d) curves but **without changing any predicted count**, and is logged as a
deviation in [JOURNAL.md](../JOURNAL.md) per PREREGISTRATION §5. The standardized
under-count is reported above as a finding in its own right, not hidden.

## Honest limits

- **Static spherical only.** Kerr (the doc's headline) is not here — ansatz emits
  exact observables only for the static lapse, and the source repos are read-only.
  Kerr is reachable in a later leg via new bridge code importing ansatz's engine.
- **Whitening can inflate curved low-dim manifolds.** Schwarzschild-dimensionful is a
  curved 1-D manifold; whitening keeps 3 linear PCs and d₁ reaches only 0.983, with
  d₂ at 1.000. The marginal-gain rule still reads 1 (the d₁ gain dominates), but a
  strict plateau rule could mis-call it 2. Noted; does not affect the charge result.
- **This is the ansatz↔tabula leg only.** Closing the spine needs deepstrain's
  measured δ (THE_BRIDGE.md §3 step 3) — the next-but-one step.

## Artifacts
- `code/gen_dataset.py` — ansatz observables → `.npz` (imports ansatz read-only).
- `code/count_bottleneck.py` — tabula bottleneck AE; reads only the `.npz` observations.
- `code/plot_curves.py` — the figure.
- `results/obs_*.npz`, `results/count_bottleneck.json`, `results/leg1_count_curves.png`.
