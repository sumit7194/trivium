# Leg R — Pre-registration: tabula's frontier regime detector, blind, on exact-GR trajectories

*Frozen 2026-07-02, BEFORE running tabula's detector on any bridge data. tabula's EXP-9/10 "robust
detector" (script 150: verdict | ABSTAIN | MIXTURE, 0-1-test-based trajectory branch, N_MIN_TRAJ=800
reliability floor) was validated on ITS menu (Kepler/Lorenz/Hénon–Heiles/Bell/geometry — 9/9, zero wrong
confident verdicts). It has never seen general-relativistic geodesic data. The bridge feeds it exact-metric
section series — UNLABELED — whose ground truth the bridge has established with three validated instruments
(symbolic KY/Carter algebra; box-dimension; the frequency-drift detector). This is the dynamics-level
analogue of leg Q: an independent neural/statistical instrument vs exact-GR ground truth.*

## The blind inputs (section series, (x, p_x) per y=0 up-crossing)

| tag | source (hidden from detector) | ground truth | n crossings |
|---|---|---|---|
| S1 | Kerr a=0.5, E=0.95, L=2.8, x0=5.0 | regular (integrable, Carter) | ≥800 |
| S2 | Kerr a=0.5, x0=4.5 — the **1:3 resonant island** | regular (island; broke our naive rotation number) | ≥800 |
| S3 | MN a=0.5, q=0.5, x0=4.0 (outer) | regular (box-dim 1.06→1.15 converged; drift 0.0000) | ≥800 |
| S4 | MN a=0.9, q=0.6, Lz=3.0, x0=7.70 — the **2/3 resonance centre** | regular (drift 0.0000) | ≥800 |
| S5 | MN inner **orbit_A** (χ=0.9, q=0.95; ansatz §104 adaptive) | regular island (drift 0.0000; box-dim 1.203) | 800 |
| S6 | MN inner **orbit_B** (same params) | **thin chaos** (drift 0.980; box-dim 1.219) | 126 |

## Frozen predictions

- **P1 (regular sweep):** S1–S5 all return **EMIT-regular** (per-orbit K < 0.3). Any CERTIFY-CHAOS on
  S1–S5 is a **false positive** on integrable/regular GR data — a real finding about the 0-1 test's
  GR behaviour (the resonant island S2 is the designed trap: it broke our centroid-angle rotation number).
- **P2 (the short chaotic orbit):** S6 (126 crossings < their 800 floor) returns **ABSTAIN
  (too-few-points)** — the *honest* outcome by their own gate. We pre-register this as **evidence of an
  instrument sample-complexity gap**: the bridge's frequency-drift detector resolved S6's chaos at 126
  crossings (validated, length-matched control); tabula's 0-1 branch declares itself underdetermined below
  800 — a concrete, cross-repo instance of tabula's own EXP-12 "sampling axis" (N_resolve differs by ≥6×
  between instruments on the same data).
- **P3 (secondary, sub-floor diagnostic):** bypassing their gate, the raw 0-1 K on S6 is reported for
  information only (their floor caveat applies): K > 0.7 would be a third-instrument hint of chaos;
  an ambiguous K is *consistent with their floor being right* — either way no strong claim from a
  sub-floor reading.
- **P4 (verdict count):** zero wrong *confident* verdicts (their design claim, now tested off-menu).

## Gate

The exercise VALIDATES the frontier detector on GR data iff P1 holds in full (5/5 regular, no false
chaos) and any S6 outcome is either ABSTAIN or CERTIFY-CHAOS (never EMIT-regular). Partial failures are
findings, not embarrassments — they localize where the 0-1 test needs GR-specific care.

---

## Amendment (2026-07-02, before the corrected run) — representation fix + re-freeze

**What went wrong (transparently):** the v1 plan fed tabula's detector single Poincaré *section* series.
Its `infer_type` requires raw-trajectory ENSEMBLES `(N_orbits, timesteps, D)`, so every input returned
**UNKNOWN** (`results/frontier_verdicts.json`) — no verdict, hence no information gained about the corrected
test, so re-freezing predictions now is legitimate. The raw 0-1 K on a section series was also scrambled
(S6-chaos → −0.617), confirming the section is the wrong representation for their trajectory instrument.
*This mismatch is itself a recorded finding:* the two repos' chaos instruments consume different
representations (tabula: 0-1 test on raw trajectory ensembles; bridge: frequency-drift on single sections) —
they are not naively pipe-compatible.

**Corrected inputs** (`generate_trajectories.py`) — raw geodesic trajectory ensembles, the representation
tabula validated on, on three exact-GR classes with independent bridge ground truth:

| class | source | ground truth | expect |
|---|---|---|---|
| C1 | Kerr = `manko_novikov(q=0)`, 20 bound orbits | integrable + regular | EMIT-regular |
| C2 | MN `q=0.5` outer, 20 bound orbits | **non-integrable** (illegible §144, no KY leg O) but **KAM-regular** (leg J) | EMIT-regular |
| C3 | Majumdar–Papapetrou di-hole (§79) | chaotic (λ=2.09) | CERTIFY-CHAOS |

**Re-frozen predictions:**
- **Q1:** C1 → EMIT-regular; C3 → CERTIFY-CHAOS (the detector's basic GR competence — regular integrable vs
  chaotic, off its Kepler/Lorenz menu).
- **Q2 (the prize — the dissociation):** C2 → **EMIT-regular** (0-1 test sees KAM tori). If so, then on the
  *same* MN q=0.5 metric tabula's two instruments **DISSOCIATE**: the legibility probe (§144) reads
  **illegible/non-integrable**, the regime detector reads **regular** — exactly tabula's own EXP-7
  dissociation (law-learnability ≠ predictability), instantiated on an exact GR metric, and matching the
  bridge's dual ground truth (non-integrable [leg O] yet dynamically regular [leg J]). A CERTIFY-CHAOS on C2
  would *contradict* the bridge's box-dim/frequency-drift regularity — a real tension to chase.
- **Q3:** zero wrong confident verdicts (their design claim, tested off-menu on GR data). ABSTAIN is always
  an honest outcome, not a failure.

**Gate:** validated iff Q1 holds (C1 regular, C3 chaos) with zero wrong confident verdicts. Q2 is the
scientific payload (the cross-instrument dissociation), reported regardless.
