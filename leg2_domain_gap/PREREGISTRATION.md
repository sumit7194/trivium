# Leg 2 — Pre-registration: the legibility law as a sim→real diagnostic (tabula × deepstrain)

*Frozen 2026-06-17, before any bridge code is written. Discipline: THE_BRIDGE.md §2
and §4B (the domain-gap bridge — "the most original thing in the whole bridge" if it
lands).*

This is the **tabula ↔ deepstrain leg** (§4B). It does NOT touch ansatz.

---

## 1. The honest conceptual mapping (and a caveat that sharpens it)

THE_BRIDGE.md §4B asks: *is deepstrain's learned ringdown code **amortized**
(encoder-inferred → should transfer) or **free/stored** (→ scrambles under shift)?*

**Caveat, found in recon (not a reason to abandon — a reason to reframe).**
deepstrain's tone-count model (`ringdown_spectroscopy/scripts/11_tonecount.py`,
class `ToneCounter`) is a **feed-forward CNN encoder** (`Embed`): a shared encoder
that infers a 64-d code from the waveform. So it is **amortized by construction** —
there is no free-embedding regime. Tabula's *own* cross-test on real LLMs (Phronesis,
in `SpaceTime/writeups/legibility_law.md`) already established that **amortized-by-
default models do not exhibit the "free→scramble" failure** — the precondition isn't
instantiated. So the *literal* §4B question has a near-certain null: deepstrain's code
is amortized, not free.

**The reframe (the version worth doing).** The legibility law's real instrument is the
**probe ladder** — linear decode (legibility) vs nonlinear decode (information
presence); scramble signature = *linear-low, nonlinear-high*. The sharpened, falsifiable
question that survives the caveat:

> **Does the cross-distribution linear legibility of the task *invariant* predict
> sim→real transfer?** I.e., when deepstrain's tone-count model fails to transfer, is it
> because the *overtone-presence* signal (the invariant that must survive sim→real) is
> **linearly illegible on real data** (scramble signature) while a sim-specific
> **shortcut** (loudness/SNR) is the legibly-encoded thing — and does the transfer fix
> correspond to the invariant becoming legible on real data?

This is the Leg-3 *indirect-observation* regime of the law (the overtone is observed
indirectly, through noise + whitening), where legibility is exactly what erodes. If it
holds, the probe ladder becomes a **diagnostic for sim→real transfer in GW ML** — and
possibly a fix (force the invariant legible).

---

## 2. Specimen, distributions, and the transfer-outcome axis (all offline, read-only)

**Models (read-only checkpoints, `ringdown_spectroscopy/models/`).** The clean
single-architecture chain (same `Embed`, 64-d code), spanning the documented transfer-
fix sequence:

| checkpoint | stage | transfers? (from stored results) |
|---|---|---|
| `11_tonecount.pt` | base (first cut) | **no** — GW250114 P(2t)=0.15 (truth 2); real-noise 1t≈2t≈1.0 (shortcut) |
| `11_tonecount_norm.pt` | + RMS norm (fix A) | **no** — GW250114=0.20; real-noise still unseparated |
| `11_tonecount_realnoise.pt` | + real O4 noise (fix B) | **no** — GW250114=0.11 |
| `11_tonecount_matched.pt` | + injection-convention match (fix D) | **partial** — "transfer pathology gone" per JOURNAL |

(`_conv`/`_convbig` use a different input convention — held as an OPTIONAL secondary,
not in the primary frozen test, to keep architecture fixed.)

**Two distributions** (both built offline from cached data — no gwpy, no network):
- **SIM** = idealized-noise simulations, `sbilib.simulate_tonecount(...)` (the early
  training distribution).
- **REAL** = real O4 detector noise, injections into the cached pool
  `ringdown_spectroscopy/data/o4_noise_pool*.npz` (`sbilib.simulate_tonecount_conv`).

**Transfer-outcome axis (ground truth, per checkpoint), computed by us, blind to probes:**
- `T_real` = balanced 1-tone/2-tone **AUC on REAL-noise injections** (the model's own
  P(2-tone) separating injected 1- vs 2-tone in real noise). High = transfers.
- `T_event` = P(2-tone) on **GW250114** (truth: 2-tone; high = correct transfer).

**Labels available per generated sample** (`make_batch` already returns these):
- INVARIANT: tone label `y∈{0,1}`; continuous overtone amplitude ratio `frac`; overtone
  matched-filter SNR `osnr`.
- SHORTCUT: total/loudness SNR of the segment (the "loud⇒2-tone" feature the diagnostic
  chain caught).

---

## 3. The experiment (probe ladder on the Embed code)

For each checkpoint × each distribution (SIM, REAL), extract the 64-d `Embed(x)` code on
a balanced labelled set. Then run the probe ladder (tabula's instrument; sklearn):
- **linear** = ridge regression / logistic, 5-fold CV → legibility `r` (or AUC).
- **nonlinear** = kNN → information-presence `r`.

Decode three targets from the code:
1. **invariant** — tone label `y` and overtone `osnr`;
2. **shortcut** — loudness SNR;
3. cross-distribution: probe **trained on SIM codes, tested on REAL codes** (the key
   quantity — does the code's legible axis survive the shift?).

The blindness boundary (as in leg 1): a deepstrain-side extractor (ringdown venv) writes
only `(code, labels)` arrays to `.npz`; the tabula-side probe (sklearn venv) reads only
those arrays.

---

## 4. Predictions and criteria (frozen)

Let `L_inv^within` = linear legibility of the invariant within a distribution,
`L_inv^cross` = linear legibility trained-SIM/tested-REAL, `N_inv` = nonlinear (kNN) on
REAL, `L_short` = linear legibility of the loudness shortcut.

- **P1 — invariant info is present in every checkpoint** (sanity): `N_inv` (nonlinear,
  REAL) > 0.7 for all four. (If the overtone weren't even in the code, the leg is moot.)
- **P2 — the scramble signature on non-transferring checkpoints:** for `base/norm/
  realnoise`, on REAL data the invariant is *linearly* far less legible than it is
  nonlinearly present: `N_inv − L_inv^cross ≥ 0.20` (linear-low / nonlinear-high).
- **P3 — legibility tracks transfer (the headline):** across the four checkpoints,
  `L_inv^cross` is **monotonically associated** with the transfer axis `T_real`
  (Spearman ρ ≥ 0.8 over the 4 points). The transferring checkpoint has the most
  linearly-legible-on-REAL invariant.
- **P4 — the shortcut is the legible competitor early:** for `base/norm`, `L_short`
  (loudness) on REAL **exceeds** `L_inv^cross` (the net legibly encodes loudness, not the
  overtone). The fix reduces `L_short − L_inv^cross`.

**Agreement / outcome interpretation (decided now):**
- P2 ∧ P3 hold → **the legibility law diagnoses sim→real transfer**: transfer failure =
  the invariant in the scramble regime on real data. This is the §4B headline result.
- P3 holds but P2 fails (invariant linearly legible on real even when it fails to
  transfer) → transfer failure is **not** a legibility phenomenon here; report as a clean
  negative that bounds the law's reach (still a finding — §2 rule 4).
- P1 fails for some checkpoint → that checkpoint never encoded the overtone; exclude and
  note (the model used only the shortcut — itself consistent with P4).

**Never tuned:** probes are off-the-shelf (ridge/logistic + kNN, fixed k, CV); no
threshold is moved to make a checkpoint land. Predictions frozen by this file.

## 5. Deliverables
- `code/extract_codes.py` (ringdown venv) — load checkpoint read-only, build SIM+REAL
  labelled batches, write `(code, labels)` `.npz`. Imports deepstrain `sbilib/rdlib`
  read-only; additive (no edits to their repo).
- `code/probe_ladder.py` (sklearn venv) — read `.npz`, run linear/nonlinear/cross probes,
  compute `L/N` table and the `T`-axis correlation.
- `results/` — the probe table, the legibility-vs-transfer plot, filled §4 verdicts.
- findings appended to `JOURNAL.md` / a `FINDINGS.md`.
