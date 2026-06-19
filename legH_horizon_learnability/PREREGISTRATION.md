# Move H — Pre-registration: the horizon is a learnability edge (prediction + a recipe)

*Frozen 2026-06-20. Takes the battle-tested edges finding (a learned representation fails where the
metric diverges; Moves E/F/G) from DIAGNOSTIC to PREDICTIVE + CONSTRUCTIVE, on the real
black-hole horizon. Same rigour: pre-register, gate, stay falsification-minded.*

## The claim, made predictive and useful

The bridge established (and survived falsification) that learned recovery of an exact structure
degrades at a **metric-divergence edge** — exactly a black-hole horizon. This leg tests two NEW
things on ansatz's *actual* exact metric:
1. **Prediction:** a learned emulator of a horizon-diverging GR quantity will fail at the horizon,
   with error **localized at and growing toward** the divergence — not uniformly.
2. **Recipe:** a **hybrid** (learned in the bulk + the exact near-horizon asymptotics at the edge)
   will beat both a pure-learned emulator (fails at the edge) and a pure-asymptotic one (fails in
   the bulk) — uniform accuracy.

This is GR-relevant: ML surrogate/waveform models struggle near merger/horizon; this says where (the
metric-divergence locus) and gives a fix (hand the edge to the exact structure).

## 1. The setup (ansatz's exact metric, read-only)

Emulate a quantity `Q(r)` that **diverges at the horizon**, from noisy observations of position:
- **Schwarzschild** (a=0): gravitational blueshift/redshift factor `Q = 1/√(−g_tt) = 1/√(1−2M/r)`
  → ∞ at `r=2M`. Leading edge behaviour `Q ≈ √(2M)/√(r−2M)`.
- **Kerr** (a=0.6): proper-radial metric factor `Q = √(g_rr) = √(Σ/Δ)` → ∞ at the horizon `Δ=0`
  (`r₊ = M+√(M²−a²)`). Leading edge behaviour `Q ∝ 1/√(r−r₊)`.

Learned emulator: a net (kNN / MLP) predicting `Q` from the noisy coordinate(s); trained on samples
spanning bulk→edge. "Edge" = within the near-horizon band; "bulk" = the mid-range.

## 2. The three emulators (frozen)

- **Pure-learned:** the net, everywhere.
- **Pure-asymptotic:** the exact leading near-horizon form `Q ≈ c/√(r−r_h)` (ansatz supplies `r_h`
  and the coefficient), everywhere.
- **Hybrid:** learned for `r > r_match`, exact-asymptotic for `r ≤ r_match` (one matching radius).

## 3. Predictions (frozen)

- **H1 (failure localizes at the horizon).** Pure-learned relative error in the edge band ≥ **3×**
  its bulk error (the failure is at the divergence, not uniform).
- **H2 (it tracks the divergence).** The pure-learned edge error rises monotonically as `r→r_h`,
  correlated with the metric factor `Q` itself (Spearman ≥ 0.8 between local error and `Q`).
- **H3 (the hybrid is the recipe).** The hybrid's worst-region (max over bulk/edge) relative error is
  **lower than both** pure-learned (which fails at the edge) and pure-asymptotic (which fails in the
  bulk) — i.e. `max-error(hybrid) < min(max-error(learned), max-error(asymptotic))`.
- **H4 (holds on both metrics).** H1 and H3 hold for Schwarzschild AND Kerr.

## 4. Falsification-minded controls (built in)

- **Flat null:** the SAME emulator on a quantity with NO divergence (e.g. `Q = r` in flat space) must
  show **no** edge failure (H1 ratio ≈ 1) — if it does, the effect is the emulator, not the horizon.
- **Asymptotic-in-bulk check:** the pure-asymptotic form must be measurably WRONG in the bulk
  (otherwise the hybrid is trivial / the asymptotic is just globally correct).
- We report raw outcomes; if H3 fails (hybrid does not beat both), the "recipe" claim is dropped.

## 5. Honest scope
Toy emulation of single GR quantities (not a full waveform), one matching radius, near-horizon
leading order only. The contribution is the predictive validation on the real horizon + the hybrid
recipe, unifying the GR case with the cross-domain edges finding — not a production GW emulator.

## Deliverables
- `code/horizon_learnability.py` — the three emulators on Schwarzschild + Kerr (ansatz exact metric)
  + the flat null; error-vs-position and the hybrid comparison.
- `code/plot_horizon.py` — error-vs-distance-from-horizon + the three-emulator bars.
- `FINDINGS.md` — H1–H4 outcomes, the recipe verdict, honest limits.
