# Leg T — Pre-registration: the Mercury anomaly accounting (tabula's real-data precession × ansatz's exact GR term)

*Frozen 2026-07-03, before `code/anomaly_accounting.py` is run. This is the historical Le Verrier
decomposition performed with sister instruments: tabula measured Mercury's TOTAL perihelion precession on
real 120-year JPL Horizons data (EXP-15 P4: LRL-azimuth drift 1900–2020); the bridge subtracts the
literature Newtonian planetary-perturbation value and compares the residual against the exact GR advance —
computed from the Schwarzschild formula evaluated with **tabula's own instrument-measured GM☉** (μ̂_LRL,
discovered from the ephemerides to 1e-6 relative). Explicitly NOT a GR detection claim: the GR share is
inseparable from the Newtonian secular trend in an LRL drift alone (recon conclusion); this is an
anomaly-ACCOUNTING consistency test at the measurement's precision floor.*

## Inputs (frozen)

- tabula EXP-15 (`156_newton_from_ephemerides.json`, read-only):
  `P4_measured_precession_arcsec_per_century = 568.435`, `P4_known_total = 575.0`,
  `P3_mu_hat_LRL = 2.9591194e-04 AU³/day²` (their measured GM☉), `mu_true = 2.9591221e-04`.
- Literature Newtonian secular contribution (planetary perturbations, external anchor — same role Abedi
  Table I played in leg 8): **532.3 ″/century** (Clemence 1947, Rev. Mod. Phys. 19, 361; the standard
  planetary-perturbation total; solar oblateness ~0.03″/cy, negligible here).
- Mercury elements (standard): a = 0.3870989 AU, e = 0.2056307, period 87.969 d; c = 173.1446 AU/day.

## Frozen predictions

- **T1 (the exact GR term):** Δφ_GR = 6πμ/(c²a(1−e²)) per orbit, evaluated with tabula's μ̂_LRL, converted
  to ″/century, must reproduce the canonical **≈ 43.0 ″/cy** (42.9–43.1). Using the *instrument-measured* μ
  vs the true μ must not change it beyond 0.001% (their μ error).
- **T2 (the accounting):** residual ≡ measured_total − Newtonian_literature = 568.4 − 532.3 = **36.1 ″/cy**.
  Measurement floor: tabula's total is off the known total by |568.4 − 575.0| = 6.6 ″/cy (~1.1%) — adopt
  σ_meas ≈ 6.6 ″/cy. **Gate: |residual − Δφ_GR| < 2σ_meas (13.2 ″/cy).** Expected: |36.1 − 43.0| = 6.9 ″/cy
  → within ~1σ. PASS = the GR term is required and sufficient to close Mercury's books at the instrument's
  floor; FAIL = a real tension to chase.
- **T3 (honest framing, fixed in advance):** whatever the numbers, the claim is *consistency of the
  accounting at a ~7″/cy floor* — not an independent GR detection (the ephemerides have GR baked in, and
  the Newtonian share is 12× larger and only separable via the external literature anchor).
