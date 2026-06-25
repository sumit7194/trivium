# Leg L — Pre-registration: amortized no-hair legibility + amortization→transfer (backlog A6/A1)

*THE_BRIDGE §9: "Does amortization predict sim→real transfer in GW data? (the most original result
available here)." leg 2 found the tone-count info-limited; this probes the richer no-hair δ SBI.*

## Method
Extract the no-hair NPE's 56-d Embed summary code on simulated ringdowns with known (M, χ, δ). Probe ladder:
linear (Ridge) vs nonlinear (MLP) held-out R² per parameter. Then compare the per-parameter sim legibility
to the real-data (GW250114) posterior precision.

## Frozen predictions
- **A6 (legibility):** M and χ are well-encoded (the NPE infers them); δ is the decisive parameter. Reading
  rule — both R² low ⇒ info-limited (like the tone-count); nonlinear≫linear ⇒ scramble signature;
  both high ⇒ cleanly legible.
  - *Expectation (not a foregone conclusion):* δ is info-limited even in the richer model (the 221 overtone
    is weak), corroborating leg 2 — OR it shows a scramble signature, meaning the legibility law bites once
    information is sufficient. Either is a real outcome.
- **A1 (transfer):** if the sim legibility ranks the real-data precision (M tightest, δ widest), then the
  amortization legibility predicts transfer — the §9 idea, concretely. Honest scope registered up front:
  3 parameters / 1 event is a ranking test, not a large-N correlation; the deeper "amortization-gap predicts
  cross-model transfer failure" needs several NPEs deepstrain would have to train.

## Discipline
deepstrain repo read-only (import sbilib + load the trained posterior; never modify). Bridge code only.
