# Move B — Findings: the numeric ringdown bridge (leg 3b)

*Run 2026-06-19. Comparisons and predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md)
before the eikonal QNM was compared to the measured ringdown. Upgrades the spine's leg 3.*

## Result in one line

Ansatz's **eikonal Kerr QNM, computed from the exact metric**, matches deepstrain's **measured
GW250114 220 ringdown** to a few percent — quality factor `Q₂₂₀` to **1–7%** and dimensionless
frequency `Mω_R₂₂₀` to **3%** — while the Schwarzschild (non-spinning) approximation misses by
**40–50%**. The spine's ansatz↔deepstrain ringdown link is now a **numeric exact↔measured
comparison**, not a proposition; and the agreement is the *light ring* (`Ω_c·b_c = 1` exact), so
the LIGO ringdown and the EHT shadow are demonstrably the same photon orbit.

## The comparison (all four frozen predictions pass)

Measured GW250114 (deepstrain, real O4 data, read-only): 220 mode `f = 257.76 Hz`,
`τ = 4.944 ms`; remnant `M = 78.8 M⊙`, `χ = 0.787 [0.641, 0.887]`; no-hair `δ = −0.16` (Kerr
inside 90%).

| quantity | measured | ansatz eikonal Kerr | agreement | prediction |
|---|---|---|---|---|
| **Q₂₂₀** (M-independent, `πfτ`) | **4.00** | 3.73 (χ=0.787) · 3.96 (χ=0.815) | **6.8% · 1.1%** | P1 (<25%) ✅ |
| **Mω_R₂₂₀** | **0.629** (SBI M) | 0.609 (χ=0.787) | **3.1%** | P2 (<15%) ✅ |
| Q₂₂₀, Schwarzschild χ=0 | 4.00 | 2.00 | 50% off | P3 (spin essential) ✅ |
| Mω_R, Schwarzschild χ=0 | 0.629 | 0.385 | 39% off | P3 ✅ |
| **Ω_c · b_c** (shadow–ringdown) | — | **1.000000** (all χ) | exact | P4 ✅ |

→ `results/legB_ringdown_bridge.png` plots `Q(χ)` and `Mω_R(χ)` with the measurement and its 90%
spin CI overlaid; the eikonal curve threads the measured point inside the CI.

## What this establishes

- **Leg 3 is now numeric.** It closed the spine at the level of a *proposition* ("ansatz proves
  no-hair; deepstrain measures δ≈0") because ansatz had no QNM module. Ansatz now computes the
  ringdown frequency from the metric, and it agrees with the real measured 220 to a few percent.
  The count-triangle's measured leg gains a numeric ansatz cross-check it never had.
- **The agreement is physics, not a fit (P3).** The non-spinning Schwarzschild eikonal is 40–50%
  away from the data; only the Kerr spin correction — the prograde photon ring of the exact
  metric — brings ansatz into agreement. Nothing was tuned: the eikonal QNM is read straight off
  the light-ring orbital frequency and its Lyapunov exponent.
- **One photon ring, two instruments (P4).** `Ω_c·b_c = 1` holds exactly at every spin, so the
  measured ringdown pitch is `m` over the exact shadow radius: the LIGO ringdown (deepstrain) and
  the EHT shadow (ansatz `§45/§68`) are the *same* unstable photon orbit, seen two ways.
- **Method gate.** The whole construction is validated by the Schwarzschild limit: the
  exact-metric code reproduces `Ω_c = λ = 1/(3√3)`, `Q = 2`, `b_c = 3√3`, `Ω_c·b_c = 1` to
  machine precision before any Kerr value is trusted.

## Honest limits (stated up front, per §7)

- **Eikonal limit.** ℓ=2 is not ℓ→∞, so the eikonal QNM carries an intrinsic few-to-~15% error
  vs the exact (Leaver) Kerr 220 — which is exactly the size of the residual agreement gap, and
  is *better* than the band we pre-registered. The precise overtone spectrum is numerical
  (Leaver / the `qnm` package); ansatz supplies the exact potential and the exact eikonal limit
  and flags that it does not do Leaver (§56 D). This is a light-ring–level comparison, honestly
  scoped, not a precision-spectroscopy claim.
- **No new physics.** QNM↔light-ring (Cardoso et al.), the no-hair test, and Kerr spectroscopy
  are textbook / LVK-active. The contribution is turning the spine's ringdown link into a real
  number cross-checked against real data, by an exact engine.
- **Single event, dominant mode.** GW250114, ℓ=m=2, n=0. The measured 221/δ (Kerr-consistent) is
  the empirical no-hair side leg 3 already used; here the headline is the 220 light-ring match.
- **Spin from the measurement.** χ is taken from deepstrain's posterior; the comparison reads its
  90% CI, within which the eikonal curve agrees.

## Spine status

The §5 count-triangle's measured leg now has a numeric ansatz cross-check: the same Kerr remnant
whose no-hair δ≈0 says "2 numbers" also rings at the frequency ansatz's exact light ring predicts.
**Leg 3 → leg 3b: the ringdown bridge is numeric.**

## Update (2026-06-21) — Move B v2: precise (Leaver) ringdown + the numeric no-hair test

ansatz gained the **precise QNM oracle** (§77, Leaver via `qnm`, bridge-driven), so the spine's
ringdown link is upgraded from the eikonal (few-to-15%) to an exact, two-mode, numeric no-hair test:
- **The 220 inversion reproduces deepstrain's own remnant.** Inverting the measured 220 with exact
  Leaver (its M-independent Q fixes χ, then f fixes M) gives **(M, χ) = (74.8, 0.815)** — matching
  deepstrain's 220-fit exactly (two *independent* QNM codes, ansatz's `qnm` and deepstrain's `rdlib`,
  agree).
- **The 221 overtone — which the eikonal could not produce — is now a numeric test.** The exact-Leaver
  Kerr 221 prediction (f=254.5 Hz) vs the measured 221 (f=214.1 Hz) gives the no-hair deviation
  `δ ≡ (ω₂₂₁_meas − ω₂₂₁_Kerr)/ω₂₂₁_Kerr` (deepstrain's definition) = **−0.159**, which **independently
  matches deepstrain's NPE-measured δ = −0.151 [−0.46,+0.32] to 0.008**, and is **Kerr-consistent**
  (δ=0 in the 90% CI).
- **Multi-event tightening (§12):** stacking sharpens `σ(δ)` from 0.274 (1 event) to **0.095 (8 events)**.

So leg 3's no-hair link is now a precise, numeric, two-mode comparison whose δ ansatz and deepstrain
reproduce by independent routes — a real cross-validation upgrade over the v1 light-ring-level test.
See `code/precise_ringdown.py`, `results/precise_ringdown.json`.

## Update (2026-06-24) — A5: precise multi-event no-hair (deepstrain §18 raw tone fits)

deepstrain §18 exported per-event raw 220/221 fits; `code/precise_multievent.py` runs Move B v2's exact-Leaver
inversion across the 5 robust-220 events (GW250114, GW150914, GW170814, GW170104, GW190828). **The 220
inversion reproduces deepstrain's (M,χ) exactly** (≤0.000 in χ — both apply the Leaver/qnm map; a multi-event
reproducibility check). **The per-event δ is 221-information-limited:** 2/5 events rail the 221 at the 180-Hz
floor and the rest are low-confidence (the two-tone can't split ~6-Hz tones at this SNR — deepstrain's caveat,
leg 2/7's info-limit). The 3 usable δ's (−0.058, −0.104, +0.139) stack to mean δ=−0.007 (Kerr-consistent),
wide 0.243 spread. So Move B v2 extends to the catalog **at the 220 level**; multi-event *no-hair* tightening
comes from NPE δ stacking (§12: σ 0.27→0.095), not raw per-event 221 fits — the 221 stays signal-limited.
`results/precise_multievent.json`.

## Update (2026-06-26) — start-time robustness: the no-hair δ survives the dominant ringdown systematic

The biggest systematic in ringdown spectroscopy is *when* the ringdown starts (early ⇒ overtone/nonlinear
contamination; late ⇒ no SNR). Move B's exact-Leaver no-hair test was run at the **peak** (t0=0), so the
fair question is whether its Kerr-consistency is a start-time artifact. deepstrain §16 re-fit the GW250114
NPE δ posterior at offsets **0–12 ms** past the peak; `code/starttime_robustness.py` reads it (read-only)
and frames it against leg B's independent exact-Leaver δ.

- **Independent routes agree at the peak.** leg B's exact-Leaver δ = **−0.159** matches deepstrain's t0=0
  NPE median **−0.161** to **0.002** — the bridge's exact δ and deepstrain's learned δ coincide at the peak.
- **Kerr-consistent at EVERY start time.** Across t0 = 0, 2, 4, 6, 8, 12 ms the δ median wanders in
  [−0.16, +0.07], but **δ=0 (Kerr) sits inside the 90% CI at all six** — the no-hair conclusion does not
  depend on the start-time choice.
- **Systematic ≪ statistical.** The start-time drift (std **0.084** across t0; peak-to-late **0.175**) is
  **5.2× smaller** than the statistical 90% half-width (**0.437**). So the no-hair test is **SNR-limited,
  not start-time-systematic-limited** — tightening it needs more data/SNR (corroborating leg 2 / leg 7's
  information limit on δ), not better start-time control.

So Move B's headline — the exact-Leaver δ is Kerr-consistent — is **robust to the dominant ringdown
systematic**, and the bridge's exact δ tracks deepstrain's learned δ as the fit window is moved.
`results/starttime_robustness.json`.

## Update (2026-07-02) — Move B v3: the field-standard package joins, and three pipelines converge on one remnant

deepstrain R2v2 (§21) re-measured GW250114 with the **field-standard `ringdown` package** (Isi/Farr
frequency-domain coherent pipeline, Kerr-templated, NUTS; R̂ ≤ 1.004) — giving Move B a third, fully
independent route. `code/package_crosscheck.py` crosses it with ansatz's exact Leaver:

- **Spectrum check (two QNM codes):** at the package's own median (M=74.8, χ=0.729), ansatz's exact-Leaver
  220/221 frequencies reproduce the package's implied spectrum to **0.12% / 0.15%** — the Leaver
  continued-fraction and the package's internal Kerr spectrum are interchangeable.
- **Three-pipeline remnant:** bridge exact-Leaver ← raw two-tone fit (v2): **(74.8, 0.815)** · deepstrain
  NPE: **(76.3, 0.766)** · package n2: **(74.8 [70.4–79.0], 0.729 [0.644–0.795])**. The **mass agrees to
  0.00 M⊙** between the exact-Leaver inversion and the field-standard package — three methodologically
  disjoint routes (algebraic inversion / learned SBI / FD Bayesian), one remnant mass.
- **Honest tension (spin):** v2's χ=0.815 sits *just above* the package's 90% [0.644, 0.795] — traceable to
  the raw two-tone fit's f220 (257.8 Hz) vs the package's (236.3 Hz): a time-domain damped-sinusoid fit and
  an FD coherent Kerr-templated fit split the same two-mode signal differently between f220 and χ at fixed
  M. A real cross-pipeline systematic that the triangulation *surfaced* — logged, not smoothed over.
- **The overtone is decisive, and Kerr wins again:** A221/A220 = 1.017 with **P(A221 < 10%·A220) = 0.000**
  — the 221 is *required* by the data in the field-standard pipeline; and the n1→n2 mass shift
  (84.6 → 74.8 M⊙) is the classic unmodeled-overtone bias, resolved by adding the 221. A Kerr-templated
  two-mode fit succeeding decisively corroborates v2's independent δ = −0.159 (Kerr-consistent) from the
  outside. `results/package_crosscheck.json`.

## Update (2026-07-03) — the v3 spin tension RESOLVED: one start-time knob, three pipelines, closed picture

v3 logged an honest tension (χ=0.815 from the raw-fit inversion vs the package's 90% [0.644, 0.795]).
deepstrain's follow-up B answers it (§22 start-time sweep + §23 NPE-package loop; `code/starttime_resolution.py`,
read-only): the package's remnant is a **start-time family** — across 9 offsets (0–5.4 ms, all R̂<1.005)
M drifts **74.7 → 65.9 M⊙** and χ by −0.074 as early-time merger content is excluded; the **NPE sits at the
peak** of that family (inheriting the +7.9 M⊙ early-time bias, its CI nesting the package's); and the raw
two-tone fit's f220=257.8 Hz vs the package's 236.3 Hz are **positions on the same measured curve** —
different effective start/weighting, not method disagreement. The v3 mass agreement (Δ=0.00 M⊙ at peak)
stands; the χ offset was the same knob's imprint. Crucially the **overtone stays real at every start**
(P(A221≈0)=0.000 at peak; A221/A220 decays 1.01→0.52 as the start moves late — the physical τ221≈1.4 ms
behaviour). The tension we refused to smooth over in v3 is now a quantified systematic — the triangulation
did its job twice: first surfacing it, then (via deepstrain's referee) explaining it.
`results/starttime_resolution.json`.

## Artifacts
- `code/starttime_resolution.py` — the v3-tension resolution (deepstrain §22/§23 read-only): the start-time
  family, NPE's position in it, the closed three-pipeline picture. `results/starttime_resolution.json`.
- `code/package_crosscheck.py` — Move B v3: exact-Leaver vs the `ringdown` package (spectrum check,
  three-pipeline remnant, overtone reality). `results/package_crosscheck.json`.
- `code/starttime_robustness.py` — reads deepstrain §16's δ-vs-start-time + leg B's exact-Leaver δ; the
  start-time robustness + systematic-vs-statistical analysis. `results/starttime_robustness.json`.
- `code/eikonal_kerr_qnm.py` — ansatz side: eikonal Kerr QNM from the exact metric, Schwarzschild-gated.
- `code/compare_ringdown.py` — measured-vs-eikonal comparison + frozen-prediction verdicts.
- `code/plot_ringdown.py` — the Q(χ), Mω_R(χ) figure with GW250114 overlaid.
- `results/eikonal_kerr_qnm.json`, `compare_ringdown.json`, `legB_ringdown_bridge.png`.
