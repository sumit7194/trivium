# Leg 2 — Findings: the legibility law as a sim→real diagnostic (tabula × deepstrain)

*Run 2026-06-17. Predictions P1–P4 frozen in [PREREGISTRATION.md](PREREGISTRATION.md)
before any code. The headline reframe was **falsified** — cleanly, and usefully.*

## Result in one line

The legibility law does **not** explain deepstrain's ringdown tone-count sim→real gap:
there is **no scramble signature**. The probe ladder instead diagnoses the failure as
**information-limited** (the overtone signal is barely in the representation at all, on
sim *or* real) — independently corroborating deepstrain's own parked-negative verdict.

## The probe-ladder table (REAL data, 64-d Embed code, 4-checkpoint fix chain)

| checkpoint | transfer `T_real` | linear (legibility) | nonlinear kNN (info) | scramble gap |
|---|---|---|---|---|
| base | 0.576 | 0.586 | 0.566 | **−0.02** |
| + norm (fix A) | 0.618 | 0.613 | 0.610 | −0.00 |
| + realnoise (fix B) | 0.638 | 0.644 | 0.623 | −0.02 |
| + matched (fix D) | 0.618 | 0.629 | 0.613 | −0.02 |

Continuous overtone-SNR decode (REAL), linear vs kNN R²: 0.13/0.09 → 0.24/0.21 →
0.28/0.25 → 0.31/0.28 along the chain. **Linear ≥ nonlinear in every cell.**
(Computed by `probe_ladder.py` from the saved `osnr_real` arrays — reproducible from
`code/`; see `results/probe_ladder.json` fields `L_osnr_real` / `N_osnr_real`.)

## Verdicts on the frozen predictions

- **P1 (invariant info present, kNN > 0.7): FALSE.** Nonlinear decode of the overtone
  tops out at ~0.62 AUC — the overtone is only weakly in the code, even nonlinearly.
- **P2 (scramble signature on non-transferring checkpoints, gap ≥ 0.20): FALSE — the
  headline.** The scramble gap is ≈ 0 everywhere: linear legibility ≈ nonlinear
  presence. There is no "information present but illegibly stored" — the signature the
  law needs is **absent**. The faithfulness check seals it: the code *does* carry
  continuous overtone-SNR, and **linear decodes it at least as well as kNN**, so the
  probe works and nothing is hiding nonlinearly.
- **P3 (legibility tracks transfer, Spearman ≥ 0.8): TRUE but near-trivial.** ρ = 1.00,
  but `L_inv_cross` (linear AUC of code→tone on real) and `T_real` (the model head's own
  real AUC) are essentially the *same measurement*, over only 4 points with tiny spread
  (0.59–0.64). Reported as co-measurement, **not** as evidence for the law.
- **P4 (shortcut beats invariant early): FALSE.** After `norm_seg` (fix A) removes
  absolute loudness from the input, loudness is *less* linearly decodable than the
  (weak) invariant. The loudness-shortcut lived in the input scale, which normalization
  deleted — so it does not appear in these normed checkpoints' codes. (The base model's
  pre-norm shortcut was not tested in its native un-normalized convention — see limits.)

## What this means (a useful negative — THE_BRIDGE.md §2 rule 4, §7 "nulls are results")

The legibility law's scramble regime requires **information present but linearly
illegible**. Here the information is *not present* to begin with: the overtone-presence
signal at this SNR (overtone matched-filter SNR ~5–7, near threshold) is genuinely thin
in the representation. So the law correctly **does not apply**, and the probe ladder is
exactly the tool that shows it — `linear ≈ nonlinear ≈ low` is the fingerprint of an
**information-limited**, not legibility-limited, gap.

This is a real bridge result, not a dead end:
- It **rules out** a representational fix. Forcing amortization or invariant-preserving
  structure (the law's levers) cannot help, because there is no illegible information to
  liberate. The bottleneck is SNR/data.
- It **independently reproduces deepstrain's own conclusion.** deepstrain parked v4 as
  an honest negative — "black-box ML tone-count is too weak at this data/SNR scale …
  come-back-later: more data / coherent model" — reached via injection studies. The
  probe ladder reaches the *same* verdict by a completely different route (representation
  probing). Two independent methods, one conclusion: the §2 triangulation logic working
  even for a negative.
- It **bounds the legibility law's reach** on real GW data: the law governs *how*
  information is encoded, and is silent when there is too little information to encode.

## Honest limits

- **snr-matched, overtone-only eval.** Eval used `snr_match=True` (loudness decorrelated
  from the label), so the absolute AUCs reflect the *hard* overtone-presence regime, not
  the model's reported 0.72 (which had a partial loudness cue). This is the faithful test
  of overtone *legibility*, but the numbers are convention-dependent.
- **Base-model shortcut untested in its native convention.** ~~All checkpoints were fed
  `norm_seg` input; the base model was trained pre-norm, so its loudness shortcut (P4)
  was not probed where it lives.~~ **Resolved (2026-06-24, A8 — `extract_base_native.py`):** fed the base
  model its native input (un-normalized, NOT SNR-matched, so 2-tone is genuinely louder). Result: **no
  loudness shortcut even natively.** Loudness→label AUC = **0.49** (useless) because the per-event amplitude
  scatter (±30%) swamps the small 221 energy. Nuance: the native code *strongly encodes* loudness
  (code→loudness R² = 0.87) yet does NOT exploit it (it's uninformative for the label), while the invariant
  stays legible (code→tone AUC = 0.76). So **P4-False is robust to the convention** — "the code represents
  loudness" ≠ "the model uses loudness as a shortcut." See `results/base_native_probe.json`.
- **4 checkpoints, narrow transfer spread.** This was a parked honest-negative, so the
  transfer outcomes barely separate (~0.58–0.64); P3 is underpowered by construction.
- **Tone-count only.** Other deepstrain models (the no-hair δ SBI, the PBH learned
  stages) may have a richer information regime where the scramble signature *could*
  appear — untested here.

## Artifacts
- `code/extract_codes.py` — loads deepstrain checkpoints read-only, extracts the 64-d
  code on SIM + REAL (cached O4 noise), writes `(code, labels, logit)` `.npz`.
- `code/probe_ladder.py` — linear/nonlinear/cross probes; reads only the `.npz`.
- `code/plot_ladder.py` — `results/leg2_probe_ladder.png`.
- `results/codes_*.npz`, `results/probe_ladder.json`.
