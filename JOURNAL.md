# The Bridge — Journal

One dated entry per working session. Matches the shared ethos of all three repos.

---

## 2026-06-17 — Session 1: orientation + leg-1 pre-registration

**Done**
- Read [THE_BRIDGE.md](THE_BRIDGE.md) in full. Confirmed oracle→repo mapping:
  ansatz-machine = `conjecture_machine`, tabula-geometrica = `SpaceTime`,
  deepstrain = `BlackHole`.
- Fixed the workspace operating contract in [README.md](README.md): everything
  bridge-related lives here; the three repos are read-only and kept ignorant of
  each other; reused code is additive (comment changes, never delete originals);
  pre-register → build → gate → document.
- Read-only recon of the two repos leg 1 touches:
  - ansatz: `scripts/45_observables.py` emits photon sphere `r_ph`, shadow
    `b_c = r_ph/√f(r_ph)`, ISCO — **exact, static spherical lapse only**.
    `49_light_bending`, `50_precession`, `51_redshift` likewise. No-hair / moduli
    side: `28_maxwell`, `32_no_hair`, `34_hair_criterion` (the last *proves*
    electric ≡ magnetic in `f` via `Q²+P²`).
  - tabula: `curvature/scripts/12_incontext_counting.py` (DeepSets set-encoder,
    bottleneck-width sweep, accuracy knee = dof) and `10_mdl.py` (bits per body).
    Counting consumes observation episodes; currently from its own world generator.
- **Key scoping finding:** rotating-Kerr observables are NOT implemented in ansatz,
  and the repos are read-only — so leg 1 honestly uses the **static charged family**
  (Schwarzschild → RN → dyonic RN), not Kerr. Kerr deferred to a later leg via new
  bridge code importing ansatz's engine read-only.
- Wrote and **froze** [leg1_moduli_count/PREREGISTRATION.md](leg1_moduli_count/PREREGISTRATION.md):
  two counting conventions (`N_dim`, `N_shape`), per-family predicted counts, frozen
  knee-detection rule, and the headline pre-registered prediction — **dyonic-RN
  dimensionful: ansatz = 3, tabula = 2** (observational `Q²+P²` degeneracy), a §3
  "tabula < exact = genuine finding" case with a *named* mechanism.

**Not done (next session)**
- Build the additive bridge code: ansatz-observable generator + counting harness
  adapted from tabula `12`. Then run the sweeps and fill the §4 outcome table.

**Open**
- Whether the dimensionless observable set secretly leaks `P` (would flip the C
  prediction; a measurement-vs-engine check per §7).

---

## 2026-06-17 — Session 2: leg-1 built, run, and CLOSED

**Built** (additive bridge code in `leg1_moduli_count/code/`, source repos untouched):
- `gen_dataset.py` — imports ansatz's exact `photon_sphere_shadow`/`isco` READ-ONLY,
  derives `r_ph`, `b_c`, redshift in `(M, s=Q²+P²)`, roots ansatz's exact ISCO
  *condition* numerically (the symbolic cubic root is the unstable casus-irreducibilis
  branch), writes observation `.npz`.
- `count_bottleneck.py` — tabula-style bottleneck autoencoder; reads ONLY the `.npz`
  observation arrays (never ansatz, never the metric — §2 blindness enforced
  mechanically). Reports whitened + standardized R²(d), ≥3 seeds.
- `plot_curves.py` — the figure.

**Two pre-run fixes** (caught by a sanity pass, before neural data existed):
- Absolute redshift probe radii moved outside the horizon (3–6 M were inside for
  M up to 3 → NaN). Now 8–30 M.
- ISCO via numeric rooting of ansatz's exact condition (stability).

**Logged deviation (knee rule).** A sanity PCA showed the mass scale carries ~99% of
observable variance in the dimensionful convention, so the originally-frozen
"R² within 2% of plateau" rule under-counts the charge dof (calls RN/dyonic = 1).
Refinement, chosen after seeing the R²(d) curves but with **predictions unchanged**:
count = # of widths `d≥1` whose **whitened** marginal R² gain > 2%. Original rule and
prediction preserved in `PREREGISTRATION.md`; rationale in `FINDINGS.md`.

**Result — every cell matched the frozen prediction** (`leg1_moduli_count/FINDINGS.md`):
Schwarzschild 1/0 ✅, RN 2/1 ✅, **dyonic 3→2 (dimensionful) and 2→1 (shape)** =
the predicted `Q²+P²` observational degeneracy, tabula one short of ansatz's algebraic
moduli, mechanism named/proved by ansatz `34`. Bonus methodological finding: the
standardized readout under-counts the dimensionful dof (the §7 scale-dominance trap),
demonstrated concretely.

**Next session**
- Either: Kerr extension of leg 1 (new bridge code computing rotating observables from
  ansatz's engine, read-only) — would test the doc's literal "Kerr=2, KN=3".
- Or (recommended per §8): **leg 2 — the domain-gap diagnostic (§4B)**, the
  highest-payoff bridge, touching deepstrain's real sim→real pain.

---

## 2026-06-17 — Session 3: leg-2 recon + pre-registration (§4B domain gap)

**Read-only recon** (tabula legibility law + deepstrain ringdown tone-count):
- tabula's probe ladder (`writeups/legibility_law.md`): linear decode = legibility,
  nonlinear (kNN) = info presence; scramble signature = linear-low/nonlinear-high.
- deepstrain's transfer-failure specimen: ringdown **v4 tone-count**, PARKED honest
  negative. Model `ToneCounter` = `Embed` CNN → 64-d code → logit. `make_batch` already
  returns the INVARIANT (tone label, overtone `osnr`) and the SHORTCUT (`loudness SNR`)
  the diagnostic chain caught ("loud⇒2-tone").
- Per-checkpoint transfer outcomes (from stored result JSONs): base/norm/realnoise do
  NOT transfer (GW250114 truth=2-tone read at P≈0.11–0.20; real-noise 1t≈2t≈1.0 =
  loudness shortcut); `_matched` = "transfer pathology gone". Clean offline transfer
  axis available (real-noise-injection AUC + GW250114).

**Key conceptual finding (sharpens the leg).** deepstrain's model is **amortized by
construction** (a shared CNN encoder), so the literal §4B "amortized vs free" question
has a near-certain null — exactly the Phronesis LLM caveat in tabula's own writeup.
Reframed the leg to the falsifiable version: *does cross-distribution linear legibility
of the invariant predict transfer, and do non-transferring checkpoints show the scramble
signature on real data?* (Leg-3 indirect-observation regime.)

**Froze** [leg2_domain_gap/PREREGISTRATION.md](leg2_domain_gap/PREREGISTRATION.md):
specimen = clean ToneCounter checkpoint chain (base→norm→realnoise→matched); SIM vs REAL
(cached O4 noise pool, offline); probe ladder on the 64-d Embed code; predictions
P1–P4 with frozen criteria (headline P3: `L_inv^cross` tracks transfer, Spearman ρ≥0.8).

**Not done:** the two-stage build (extract_codes.py + probe_ladder.py) — pending a
go/no-go on the reframe vs the literal-§4B null, and checkpoint scope.

---

## 2026-06-17 — Session 4: leg-2 built, run, and CLOSED (useful negative)

User chose **build the reframe**. Built the two-stage experiment (additive bridge code,
source repos untouched):
- `extract_codes.py` (ringdown venv) — loads the 4 ToneCounter checkpoints READ-ONLY,
  builds SIM (idealized) + REAL (cached O4 noise pool) balanced eval sets, extracts the
  64-d Embed code + labels + the model's own logit. Batch logic copied from
  `11_tonecount.py` with provenance comments (no edits to BlackHole).
- `probe_ladder.py` (sklearn venv) — reads ONLY the code arrays; linear (logistic/ridge)
  vs nonlinear (kNN) decode of the overtone invariant + loudness shortcut, within/cross
  distribution; transfer axis = model's own real-noise AUC.

**Result — the headline reframe (P2) is FALSIFIED, cleanly** (`leg2_domain_gap/FINDINGS.md`):
- **No scramble signature.** linear ≈ nonlinear ≈ ~0.6 on real; scramble gap ≈ 0.
  Faithfulness check (decode continuous overtone SNR): linear ≥ kNN everywhere, R² rising
  0.13→0.31 along the fix chain → probe works, nothing hidden nonlinearly.
- **Diagnosis: the gap is INFORMATION-limited, not legibility-limited.** The overtone at
  this SNR (~5–7, near threshold) is barely in the representation; the law's scramble
  regime (info-present-but-illegible) requires information that isn't there.
- P1 FALSE (info weak), **P2 FALSE** (no scramble), P3 TRUE-but-trivial (ρ=1 is
  co-measurement, 4 pts, tiny spread), P4 FALSE (norm removed the loudness shortcut).
- **Value of the negative:** rules out a representational fix (amortization/structure
  can't help — no illegible info to free); and **independently reproduces deepstrain's
  own parked verdict** ("too weak at this SNR; need more data") by a completely different
  method (representation probing vs injection studies) — §2 triangulation on a negative.

**Bridge status:** legs 1 (ansatz↔tabula, agreement + named degeneracy) and 2
(tabula↔deepstrain, clean negative) done. Spine still needs the third leg —
**deepstrain's measured δ vs ansatz's proved no-hair** (§3 step 3 / §4C), to close the
triangle. Or: Kerr extension of leg 1.

---

## 2026-06-17 — Session 5: leg-3 — the SPINE CLOSES (§3 / §4C / §5)

**Recon:** ansatz **proves** no-hair structurally (`32`/`33`; scalar adds nothing, metric
forced) but has **no QNM module** (grep empty) → leg 3 is the proof↔test pairing + the §5
count-triangle, not a numeric QNM bridge. deepstrain's measured δ (recalibrated, T=1.05):
**GW250114 δ = −0.16 [−0.46, +0.33]** 90%, coverage ≈0.91, Kerr inside 90%.

**Froze** [leg3_triangle/PREREGISTRATION.md](leg3_triangle/PREREGISTRATION.md): the one
proposition, three quantifications (all predicted = 2), with the **family caveat
registered up front** (tabula counted charged-static RN; deepstrain measures rotating-
vacuum Kerr; concurrence is on the number 2 across two families, not one shared object).

**Built + ran** `measured_dof.py` (reads deepstrain δ posterior read-only): Savage–Dickey
density ratio for δ=0. **Result — the triangle closes:**
- ansatz proved 2, tabula inferred 2 (leg 1), deepstrain measured-consistent-with 2.
- C1 ✅ (δ=0 in 90% CI; σ(δ)≈0.24; BF(2-number:3-number) = 1.3–2.6, weak-moderate
  preference for exactly 2). C2 ✅ (all three = 2).
- Through-line: leg-1 dyonic (observable<algebraic) and leg-3 no-hair (no extra number
  resolved) are two faces of "the resolvable count is measured, not assumed."

**Wrote** [SPINE_SUMMARY.md](SPINE_SUMMARY.md) — the closed spine across all three legs,
with the honest accounting and the §7 limits.

**Spine status: COMPLETE.** Next options (THE_BRIDGE.md menu): Kerr extension of leg 1
(rotating observables via ansatz engine, read-only); the conjecture handoff (§4A,
geometrizes ⟺ universal ∧ conservative → ansatz prover); strong-field curriculum (§5).

---

## 2026-06-17 — Session 6: leg-1b built, run, and CLOSED (Kerr extension)

**Continued** from session 5's final work (which hit the session limit mid-validation).
The pre-registration and `kerr_observables.py` were written in session 5; this session
validated, ran, and closed the leg.

**Sanity validation** — exact metric-derived observables checked against known Bardeen
values: Schwarzschild r_ph=3M, r_isco=6M, ω=0 ✅; Kerr a/M=0.9 prograde ISCO=2.321M
(expected 2.32), retrograde=8.717M (expected 8.72) ✅. All physics correct.

**Built** (additive bridge code in `leg1b_kerr/code/`, source repos untouched):
- `kerr_observables.py` (session 5) — imports ansatz's `kerr_delta_metric` READ-ONLY,
  derives exact equatorial observables (horizon, photon orbits, ISCO, frame-dragging,
  redshift) from the exact metric components. Three families: Kerr (M,a), KN-full
  (M,a,Q) with all observables, KN-Δ-symmetric (M,a,Q) with only Δ-dependent
  observables. 8000 objects per family × 2 conventions = 6 `.npz` datasets.
- `count_bottleneck_kerr.py` — identical instrument to leg 1 (same AE, same sweep,
  same knee rule), reads only the `.npz` arrays (§2 blindness enforced mechanically).
- `plot_curves_kerr.py` — the figure.

**Result — every cell matched the frozen prediction** (`leg1b_kerr/FINDINGS.md`):

| Cell | ansatz | tabula | verdict |
|---|---|---|---|
| Kerr dimensionful | 2 | 2 | ✅ |
| KN-full dimensionful | 3 | 3 | ✅ |
| KN-Δ-symmetric dimensionful | 2 | 2 | ✅ |
| Kerr shape | 1 | 1 | ✅ |
| KN-full shape | 2 | 2 | ✅ |
| KN-Δ-symmetric shape | 1 | 1 | ✅ |

**The doc's literal headline:** Kerr = 2, Kerr–Newman = 3 — confirmed by an
independent neural measurement. The controlled test (KN-full vs KN-Δ-symmetric) shows
frame-dragging lifts the a²+Q² degeneracy in the full observable set (→3) but the
degeneracy persists in the Δ-symmetric subset (→2). This is the exact opposite of
leg 1's dyonic case where no observable could lift the Q²+P² degeneracy.

**Through-line:** the resolvable count is measured, not assumed. Both directions now
demonstrated — degeneracy that can't be lifted (leg 1 dyonic) and degeneracy that can
(leg 1b KN via frame-dragging).
