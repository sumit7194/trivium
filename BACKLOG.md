# TheBridge — Backlog & Plan

*Living list of things noted "to try later" across the docs, plus separate-angle ideas. Compiled
2026-06-24 from a sweep of all 53 docs. Knock items out top-of-section first; update STATUS as we go.*

**Legend** — STATUS: `TODO` · `WIP` · `DONE` · `PARKED` (honest dead-end / blocked).
VALUE: `confirm` (expected outcome, tightens rigor) · `surprise` (could overturn / genuinely new).
EFFORT: `S` (hours) · `M` (a session) · `L` (multi-session / new module).

---

## A. Noted in the docs, not yet done

| ID | Item | Where noted | Value | Effort | Status |
|----|------|-------------|-------|--------|--------|
| A1 | **Amortization → sim→real transfer in GW data** — does an NPE's amortization gap *predict* its transfer? Flagged in §9 as "the most original result available here." | THE_BRIDGE §9 | surprise | L | **PARTIAL** (2026-06-24, leg L): per-parameter sim *legibility* predicts real-data precision (M 0.86→tight, δ 0.09→wide; identical ranking). Concrete but 3-param/1-event; mechanism = shared Fisher info. Deeper cross-model amortization-gap version needs several NPEs deepstrain would train. |
| A2 | **Quartic (rank-4) Killing-tensor search** — rank-2 excluded two ways; extend §85's basis to quartic to retire leg J's last residual. | legJ FINDINGS; ansatz §85 | confirm | S | **DONE** (2026-06-24, `numeric_quartic_search.py`): Kerr recovers C₀+C₀²; bump has no quartic invariant (obstruction ~1e-3). A pure-spatial SVD artifact was caught via a momentum-dependence check. Residual now only rank ≥6. |
| A3 | **Targeted resonance chaos hunt** — compute orbital frequencies, sit *exactly* on low-order resonances (vs the fine scan we did). | legJ verdict | confirm | M | **DONE** (2026-06-24, leg M): at the bump's 1:3 resonance, λ at the Kerr floor (0.018) and Carter drift tracks eccentricity not the resonance → REGULAR resonance, no chaos. leg J's null holds at the likeliest place. |
| A4 | **Direct upper limit on λ** — convert leg 8 v2's amplitude exclusion into a limit on the wormhole parameter λ (needs reflectivity→amplitude model). | leg8 FINDINGS §3 | confirm | M | TODO |
| A5 | **Precise multi-event no-hair** — extend Move B v2's exact-Leaver 221 δ test to GW150914 + GW170814 (deepstrain §13). | legB FINDINGS | confirm | S | PARKED — data-limited: only GW250114 has raw 220/221; §13's other 7 events give NPE δ only (no raw fits to invert). Needs deepstrain to export per-event tone fits. |
| A6 | **Scramble signature in richer-info deepstrain models** — test the no-hair δ SBI / PBH learned stages (tone-count was info-limited). Overlaps A1. | leg2 FINDINGS | surprise | M | **DONE** (2026-06-24, leg L): no scramble signature — δ is info-limited even in the richer NPE (linear 0.08, nonlinear 0.09), while M/χ legible. Corroborates leg 2; localizes the limit to δ. |
| A7 | **Hybrid recipe for stronger divergences** — H3 failed for mild 1/√; try 1/(r−r_h) or higher-order asymptotic; might flip H3. | legH FINDINGS | surprise | M | **DONE** (2026-06-24, `strong_divergence.py`): stronger divergence does NOT flip H3. Deeper reason found — the asymptotic at NOISY position has a catastrophic error tail near r_h (noise amplification) that dominates the mean; learned smoothing wins at every noise/strength. Reinforces H3-negative; corroborates Move I ('noise defeats even exact'). |
| A8 | **Base-model shortcut in native convention** — feed the base model un-normalized data (test loudness shortcut where it lives). | leg2 FINDINGS | confirm | S | TODO |
| A9 | **MDL lens on the count** — third leg of the count-triangle: code-length of the observation set → does it converge to 2? | THE_BRIDGE §9 | surprise | M | **DONE** (2026-06-24, leg K `mdl_count.py`): nonlinear intrinsic-dim = observable count (1,2,2), dyonic≈RN confirms Q²+P² degeneracy — a 4th lens. Linear MDL overcounts (5,7,7) via curvature. §9 answered: parting is the code, not the physics. |
| A10 | **"Geometrizes ⟺ universal ∧ conservative" as an exact proof** on the ansatz catalog (Move E was only directional). | THE_BRIDGE §9 | confirm | M | TODO |

## B. Separate angles (new directions, off the current trajectory)

| ID | Item | Why it's different | Value | Effort | Status |
|----|------|--------------------|-------|--------|--------|
| B1 | **Make leg J observational (EMRI/LISA)** — toy EMRI inspiral in the bumpy metric, hunt resonance-crossing glitches → connect "no Carter constant" to a LISA-detectable signature. | turns an abstract proof into a path to real data | surprise | L | **PARTIAL** (2026-06-24, leg M): the observable is the FREQUENCY-MAP shift (Kerr near 1:2, bump near 1:3), NOT chaotic glitches (resonances are regular). Premise corrected. Full waveform (GW fluxes/radiation reaction) is the remaining step. |
| B2 | **Multi-messenger no-hair triangulation** — pull external EHT shadow + X-ray ISCO spin, combine with deepstrain ringdown spin, run ansatz §93's three-way consistency. | new data source; breaks strict-3-siblings but a real new triangulation | surprise | L | **DONE** (2026-06-24, leg P): the test can't run on current data (3 messengers, disjoint masses, no single object has ≥2 spins). Forecast: spin-spread small (<0.034 at ε≤1) → needs a single multi-messenger object AND sub-0.05 precision; ISCO most sensitive, EHT the bottleneck. Honest forecast + data-gap finding. |
| B3 | **Topological discover→verify** — aim Move A's pipeline at a winding number / holonomy (cf. tabula §113/§114) instead of a Killing tensor. | different *class* of hidden structure, same architecture | surprise | M | **DONE** (2026-06-24, leg N): the discover→verify architecture GENERALIZES to a geometric-phase holonomy (geodetic precession) — blind discover 1.322 vs exact 1.316 (gate <2%); spin shifts it (geometric, not topological). θ-bump equatorially blind (off-equatorial loop = next step). |
| B4 | **Discover→verify as a survey** — run the pipeline across the ansatz catalog (Kerr/KN/KdS/Taub-NUT/…): which admit rank-2 vs rank-4 KTs? | turns a single-metric test into an instrument | confirm | M | **DONE** (2026-06-24, leg O): uniform KY survey — Schwarzschild/Kerr/KN/KdS/Taub–NUT all KY-integrable (gate ✅), bumpy NONE. Instrument generalizes incl. non-Kerr Taub–NUT. |

---

## Phase 1 (2026-06-24 marathon) — DONE

Cleared in one session: **A2, A3, A6, A7, A9, B3** done · **A1, B1** partial · **A5** parked.
Every high-value item on the board addressed; the honest-result discipline held throughout.

## Phase 2 (fresh) — the remaining 5

| order | item | character | needs |
|---|---|---|---|
| ✅ | **B4 catalog survey** | **DONE** (2026-06-24, leg O): uniform KY survey classifies the catalog — Schwarzschild/Kerr/KN/KdS/**Taub–NUT** all KY-integrable (gate ✅), bumpy NONE (leg J). Instrument generalizes (incl. non-Kerr Taub–NUT). | — |
| 2 | **A10 geometrizes-proof** | sharpen Move E's directional "tracks curvature" on the ansatz catalog | scoping — what exactly to prove |
| 3 | **A4 direct λ limit** | leg 8 upgrade; likely a *reframe* (DS echo amplitude is barrier-set, λ-weak → bounds reflectivity, not λ directly) | the reflectivity→amplitude model |
| 4 | **A8 base-model native convention** | niche leg-2 follow-up (small) | feed base model un-normalized data |
| ✅ | **B2 multi-messenger no-hair** | **DONE** (2026-06-24, leg P): forecast, not yet a test — disjoint masses (no single object has ≥2 messenger spins); spin-spread too small for current precision. ISCO most sensitive, EHT bottleneck. | external data ingested (logged) |

Finishing the PARTIALs (A1 cross-model amortization; B1 full EMRI waveform) needs new external inputs
(several NPEs deepstrain would train; GW fluxes) — bigger, separate efforts.

Update STATUS + a one-line result inline when done.
