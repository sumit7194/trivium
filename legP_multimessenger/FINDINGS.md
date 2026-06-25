# Leg P — Findings: the multi-messenger no-hair test is a forecast, not yet a test (B2)

*Run 2026-06-24 (backlog B2). ansatz §93 frames a no-hair null test: a Kerr hole's spin read three ways
(EHT shadow, X-ray ISCO, LIGO ringdown) must agree; disagreement ⇒ non-Kerr. This leg confronts it with
real multi-messenger data. **Scope note (logged):** this leg ingests external EHT/X-ray data, relaxing the
bridge's strict "three independent siblings" rule for one forward-looking test; the exact maps are ansatz,
the ringdown leg is deepstrain.*

## Result in one line

The three-way spin-consistency no-hair test **cannot run on current data** — the three messengers probe
**disjoint mass ranges** (no single object has two of the spins) — and even a *future* single-object
measurement would have **limited power**: ansatz's exact maps show the three Kerr-spin readings barely
disagree under a near-horizon deformation (spread < 0.034 for ε ≤ 1), so detecting a non-Kerr deviation
needs spin precision *better than today's best*, with the **ISCO** the most sensitive leg and the **EHT
spin precision the bottleneck**.

## (1) The three messengers on real data — three different objects

| object | messenger | mass | spin a* | σ_a | source |
|---|---|---|---|---|---|
| **M87*** | EHT shadow | 6.5×10⁹ M⊙ | ≈0.80 (range 0.1–0.98) | ~0.30 | [EHT asymmetry/spin studies](https://arxiv.org/abs/2003.02163) |
| **Cygnus X-1** | X-ray ISCO (continuum) | 21 M⊙ | >0.95 (≈0.97) | ~0.05 | [Gou et al. 2014](https://ui.adsabs.harvard.edu/abs/2014ApJ...790...29G/abstract) |
| **GW250114** | LIGO ringdown | ~63 M⊙ | 0.77 [0.61,0.86] | ~0.10 | deepstrain (read-only) |

The masses span **8 orders of magnitude**. No single object carries two of these spins, so the per-object
three-way consistency null — the actual no-hair test — **has no data to run on today.**

## (2) The one map we can validate on real data

ansatz's exact QNM↔spin map applied to deepstrain's GW250114 ringdown reproduces the measured remnant spin
χ ≈ 0.77 (this is Move B v2). So the *ringdown* leg of the triangle is validated on real data; the EHT
shadow and X-ray ISCO maps are exact (ansatz §86/§87) but applied to *other* objects.

## (3) The forecast — how much non-Kerr could the test catch?

Using ansatz's exact deformation sensitivity (§93), the spin-spread induced by a near-horizon deformation ε:

| ε | ISCO-spin | shadow-spin | ringdown-spin | spread |
|---|---|---|---|---|
| 0.0 | 0.600 | 0.600 | 0.600 | 0.0001 |
| 0.5 | 0.573 | 0.587 | 0.587 | 0.014 |
| 1.0 | 0.541 | 0.575 | 0.575 | 0.034 |
| 3.0 | 0.898 | 0.999 | 0.999 | 0.10 |

(Large-ε rows hit the a→1 inversion ceiling; the clean regime is ε ≲ 1.) The spread is **small** — the three
messengers probe overlapping strong-field radii, so a deformation shifts them *together*. Consequences:
- **Current EHT-limited precision (σ_a ≈ 0.30):** detects only gross deviations (ε ≳ 5).
- **Even an all-three single object at combined σ ≈ 0.05:** catches only ε ≳ 1 (spread 0.034 < 0.05).
- The **ISCO disagrees most** (near-horizon, §88's complementary sensitivity), so an X-ray-precision ISCO
  spin on a hole that *also* has a ringdown is the most promising pairing.

## Verdict

The multi-messenger no-hair triangulation is a **forecast, not yet a test**: it needs one object with ≥2
messenger spins (current data lacks it — disjoint masses), and even then the spin-maps are similar enough
that only sizable deformations (ε ≳ 1) are detectable at plausible precision. ansatz supplies the exact maps
and the deformation sensitivity; the EHT spin precision is the bottleneck. **The natural first target is a
galactic black hole with both an X-ray ISCO spin and a (next-gen / LISA-band) ringdown** — the two tightest,
most complementary legs on one object.

## Honest limits
- Relaxes the bridge's 3-siblings rule (external EHT/X-ray data) for this forward-looking leg.
- A "forecast" using point spin-values + nominal precisions, not a full likelihood; the deformation is
  §93's specific near-horizon `ε/r³` (a different deformation would shift the sensitivity).
- Re-uses textbook spin-inference maps; the contribution is the *quantitative reach forecast* and the
  explicit data-gap finding, not a new no-hair constraint.

## Artifacts
- `code/forecast_multimessenger.py` — the real-data table, the ringdown cross-check, and the ε-sensitivity
  forecast (reuses ansatz §93 maps read-only). `results/forecast_multimessenger.json`.
