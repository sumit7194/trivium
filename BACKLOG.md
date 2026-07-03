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
| A1 | **Amortization → sim→real transfer in GW data** — does an NPE's amortization gap *predict* its transfer? Flagged in §9 as "the most original result available here." | THE_BRIDGE §9 | surprise | L | **DONE** (2026-06-24, leg L): per-parameter sim *legibility* predicts real-data precision (M 0.86→tight, δ 0.09→wide; identical ranking). Concrete but 3-param/1-event; mechanism = shared Fisher info. Cross-model version (deepstrain's 5 NPE variants, A1 full): amortization gap does NOT predict transfer (corr≈0); sim→real gap is domain-shift, not amortization. Hypothesis refuted (weak test). |
| A2 | **Quartic (rank-4) Killing-tensor search** — rank-2 excluded two ways; extend §85's basis to quartic to retire leg J's last residual. | legJ FINDINGS; ansatz §85 | confirm | S | **DONE** (2026-06-24, `numeric_quartic_search.py`): Kerr recovers C₀+C₀²; bump has no quartic invariant (obstruction ~1e-3). A pure-spatial SVD artifact was caught via a momentum-dependence check. Residual now only rank ≥6. |
| A3 | **Targeted resonance chaos hunt** — compute orbital frequencies, sit *exactly* on low-order resonances (vs the fine scan we did). | legJ verdict | confirm | M | **DONE** (2026-06-24, leg M): at the bump's 1:3 resonance, λ at the Kerr floor (0.018) and Carter drift tracks eccentricity not the resonance → REGULAR resonance, no chaos. leg J's null holds at the likeliest place. |
| A4 | **Direct upper limit on λ** — convert leg 8 v2's amplitude exclusion into a limit on the wormhole parameter λ. | leg8 FINDINGS §3 | confirm | M | **DONE** (2026-06-24, `reflectivity_limit.py`): reframed as the standard echo product — effective-reflectivity upper limit R_eff ≲ 0.20–0.26 (90%, A90/ringdown-SNR). A direct λ limit stays weak/model-dependent (amplitude is barrier-set), so the robust statement is the reflectivity bound, as leg 8 §3 anticipated. |
| A5 | **Precise multi-event no-hair** — extend Move B v2's exact-Leaver 221 δ test to GW150914 + GW170814 (deepstrain §13). | legB FINDINGS | confirm | S | **DONE** (2026-06-24, leg B `precise_multievent.py`): deepstrain §18 exported raw per-event fits; exact-Leaver 220 inversion reproduces (M,χ) across 5 robust events; per-event δ is 221-info-limited (2/5 rail), stacks to mean −0.007 (Kerr-consistent, loose). |
| A6 | **Scramble signature in richer-info deepstrain models** — test the no-hair δ SBI / PBH learned stages (tone-count was info-limited). Overlaps A1. | leg2 FINDINGS | surprise | M | **DONE** (2026-06-24, leg L): no scramble signature — δ is info-limited even in the richer NPE (linear 0.08, nonlinear 0.09), while M/χ legible. Corroborates leg 2; localizes the limit to δ. |
| A7 | **Hybrid recipe for stronger divergences** — H3 failed for mild 1/√; try 1/(r−r_h) or higher-order asymptotic; might flip H3. | legH FINDINGS | surprise | M | **DONE** (2026-06-24, `strong_divergence.py`): stronger divergence does NOT flip H3. Deeper reason found — the asymptotic at NOISY position has a catastrophic error tail near r_h (noise amplification) that dominates the mean; learned smoothing wins at every noise/strength. Reinforces H3-negative; corroborates Move I ('noise defeats even exact'). |
| A8 | **Base-model shortcut in native convention** — feed the base model un-normalized data (test loudness shortcut where it lives). | leg2 FINDINGS | confirm | S | **DONE** (2026-06-24, `extract_base_native.py`): no loudness shortcut even natively (loudness→label AUC 0.49; amplitude scatter swamps the 221 energy). Nuance: code encodes loudness (R²0.87) but doesn't exploit it; invariant legible (AUC 0.76). P4-False robust to convention. |
| A9 | **MDL lens on the count** — third leg of the count-triangle: code-length of the observation set → does it converge to 2? | THE_BRIDGE §9 | surprise | M | **DONE** (2026-06-24, leg K `mdl_count.py`): nonlinear intrinsic-dim = observable count (1,2,2), dyonic≈RN confirms Q²+P² degeneracy — a 4th lens. Linear MDL overcounts (5,7,7) via curvature. §9 answered: parting is the code, not the physics. |
| A10 | **"Geometrizes ⟺ universal ∧ conservative" as an exact proof** on the ansatz catalog (Move E was only directional). | THE_BRIDGE §9 | confirm | M | **DONE — well-posed revival** (2026-06-26, leg Q): the ill-posed "exact proof" form stays retired, but its reframe (does a learned geometry become *legible* iff the metric is *KY-integrable*?) is **CONFIRMED**. tabula §127's neural `legible` column vs leg O's symbolic `KY-integrable` column agree **5/5** across the catalog (Kerr/KN/KdS/Taub–NUT legible+integrable; bumpy neither), Matthews **φ=1.0**; the two single-repo metrics (Schwarzschild, bumpy-strong) also consistent. Two independent repos, identical verdict metric-by-metric. `legQ_geometrizes_integrability/`. |

## B. Separate angles (new directions, off the current trajectory)

| ID | Item | Why it's different | Value | Effort | Status |
|----|------|--------------------|-------|--------|--------|
| B1 | **Make leg J observational (EMRI/LISA)** — toy EMRI inspiral in the bumpy metric, hunt resonance-crossing glitches → connect "no Carter constant" to a LISA-detectable signature. | turns an abstract proof into a path to real data | surprise | L | **DONE** (2026-06-26, leg M step 3 `inspiral_mn.py`): the observable is the FREQUENCY-MAP shift, NOT chaotic glitches (resonances are regular). Premise corrected, and now a **self-consistent quasi-circular inspiral** (ansatz's Peters-validated flux drains E,L; Q=0 so no dQ/dτ kludge) **traverses** the ω_r:ω_θ resonance sequence — the MN bump lowers ω_φ at each crossing by a deviation growing inward (−4.8% at 3:4 → −12.6% at 1:3). Kerr-ISCO-gated. Eccentric-inclined inspiral (needs dQ/dτ) is the further step. |
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
| ✅ | **A10 geometrizes-proof** | **DONE — well-posed revival** (2026-06-26, leg Q): ill-posed "exact proof" stays retired; the reframe (legible ⟺ KY-integrable) is **CONFIRMED** — tabula §127 `legible` vs leg O `KY-integrable` agree 5/5, φ=1.0; two independent repos, identical per-metric verdict. | tabula §127 ingested (read-only) |
| ✅ | **A4 direct λ limit** | **DONE** (leg 8 `reflectivity_limit.py`): reframed → effective-reflectivity upper limit R_eff ≲ 0.20–0.26 (90%). λ limit stays model-dependent, as anticipated. | — |
| ✅ | **A8 base-model native convention** | **DONE** (leg 2 `extract_base_native.py`): no loudness shortcut even natively (AUC 0.49); code encodes loudness but doesn't exploit it. P4-False robust. | — |
| ✅ | **B2 multi-messenger no-hair** | **DONE** (2026-06-24, leg P): forecast, not yet a test — disjoint masses (no single object has ≥2 messenger spins); spin-spread too small for current precision. ISCO most sensitive, EHT bottleneck. | external data ingested (logged) |

Both PARTIALs are now resolved: **A1** (cross-model amortization) refuted via deepstrain's 5 NPE variants
(leg L); **B1** (full EMRI) closed via ansatz's `emri.py` flux — a self-consistent quasi-circular inspiral
traverses the resonance sequence (leg M step 3). The remaining open extension is an **eccentric-inclined**
EMRI inspiral, which needs a dQ/dτ flux from ansatz (sister-request).

Update STATUS + a one-line result inline when done.

## Phase 3 (2026-06-26) — Tier-1 close-out + Tier-2 extensions

The A-board (A1–A10) and B-board (B1–B4) are now all DONE or honestly retired. This session also added
robustness/extension passes (each cross-validates an existing headline against a new metric, systematic, or
sister-repo artifact):

| item | leg | result |
|---|---|---|
| **A10 revival** | leg Q | legible ⟺ KY-integrable: tabula §127 vs leg O agree 5/5, φ=1.0 (`5176f7d`) |
| **MN positive control** | leg J | caught our Lyapunov detector false-positiving on FD-noise; box-dim is the anchor (`7c3598c`, `e38d3d5`) |
| **B1-full** | leg M | flux-driven quasi-circular inspiral traverses ω_r:ω_θ resonances; bump shifts ω_φ −5%→−13% (`750231c`) |
| **ZV γ-metric** | leg O | 2nd non-integrable case, in prolate (x,y) coords: δ=1 gate ✅, δ=2 → no KY (`c94616d`) |
| **start-time robustness** | leg B | no-hair δ Kerr-consistent at every start time 0–12ms; SNR-limited, not systematic (`d190fed`) |
| **topological discover→verify** | leg N | tabula §120 Chern completes B3's topological end; geometric (+22%) vs topological (±0.7%) (`711a01f`) |

## Phase 4 (2026-06-26) — all three sister-requests fulfilled and integrated

The three asks relayed to the sister sessions all came back and are now bridged:

| ask | sister deliverable | bridge integration |
|---|---|---|
| **dQ/dτ Carter flux** (B1-eccentric) | ansatz §101 `quadrupole_flux(carter=True)` | leg M step 4 (`7296ced`): inclined inspiral de-inclines (Kerr clean); kludge limit on strong bump flagged |
| **MN bound-chaos launcher + FD fix** | ansatz §101 `mn_bound_orbit`, `geodesic_chaos.lyapunov` de-noised | leg J (`df89527`): FD false-positive cross-confirmed + fixed; detectors validated on genuine chaos (Hénon–Heiles 1.34, di-hole 2.09) — **gap closed** |
| **Echo Δt ↔ Abedi** (leg 8) | deepstrain §18 `18_abedi_crosscheck.json` | leg 8 (`3ae5fdb`): formula reproduces Abedi 2017 Table I to **98.5–99.7%**, literature anchor |
| **ZV γ-metric legibility** (A10) | tabula §132 `132_zv_gamma_metric.json` | leg Q (`bc08ec8`): legible⟺KY-integrable now **7/7, φ=1.0**, 2nd independent non-integrable case |

**Three genuinely-new findings from the round-trip:** (a) ansatz *independently reproduced* the bridge's
FD-noise Lyapunov false-positive and shipped the fix — a cross-repo confirmation; (b) both repos *independently*
confirm MN's bound chaos is unreachable by the equatorial launcher (box-dim tops ~1.2) — a launch-data limit;
(c) **the bridge's push to χ=0.9/q=0.95 surfaced a real correctness bug** — the shared `manko_novikov` was
never asymptotically flat for q≠0 (g_xx → 0.085× Minkowski), now fixed (`3e08fef`), paths preserved so all
path-based bridge results are invariant (B1-full re-verified; B1-eccentric flux re-run). The bridge's
"push to the extreme" caught a latent bug the vacuum check couldn't — its value proposition realized a 3rd time.

**Remaining — both since RESOLVED (stale as of 2026-07-02, kept for the record):**
- ~~Relativistic Carter flux~~ — **DONE** (ansatz `f4cc1b1` + the `3e08fef` metric fix): the inclined
  inspiral de-inclines cleanly on Kerr AND the bump (leg M step 4).
- ~~MN chaotic initial data~~ — **DONE and exceeded** (ansatz §102–§104 + bridge frequency-drift): MN's own
  thin-layer chaos exhibited (leg J 2026-06-26d); detector upstreamed (§105) and 3-for-3 incl. ZV (§106).
The only parked frontier: the deep chaotic sea at x<1.5 (needs higher-precision integration, both repos).

## Phase 5 (2026-07-02) — round-4 sister sweep integrated

Sisters kept working; the bridge integrated the day's output (recon → 4 legs):

| item | leg | result |
|---|---|---|
| **detector flows upstream** | leg J + leg O | ansatz §105 natively reimplemented the bridge's frequency-drift detector (reproduces MN orbit_A 0.0000 / orbit_B 0.980 to the digit) and §106 exhibited **ZV δ=2's** own thin-layer chaos — closing §97/§98's caveat. leg O's ZV row now backed at all 3 levels (symbolic + neural + dynamical). The **4th cross-repo win**, and the first *instrument* (not bug) to propagate. (`837d4fc`) |
| **Move B v3** | leg B | deepstrain R2v2's field-standard `ringdown` package independently detects the GW250114 overtone; three pipelines (exact-Leaver / NPE / Isi–Farr) agree on **M to 0.00 M⊙**; a spin systematic honestly surfaced (`6ab92cd`) |
| **Abedi loop closed** | leg 8 | deepstrain E3 searched the formula-predicted Δt on 4 events (incl. GW250114) — all clean nulls (`beb3a0b`) |
| **frontier cross-validation** | **leg R (new)** | tabula's regime detector, blind on GR ensembles: Kerr + MN q=0.5 both EMIT-regular; the **integrable≠regular dissociation** (regime-regular vs legibility-illegible on MN q=0.5, the EXP-7 dissociation on a GR metric) matches the bridge's dual ground truth. C3 di-hole = diagnosed scope boundary (scattering chaos escapes the 0-1 test) (`70d5e2f`) |

**A recurring theme, now explicit (walls are instrument-relative, not absolute).** tabula's frontier
(EXP-12: sample complexity `N_resolve ~ 1/δ²` diverges at a verdict wall) is the *theory*; the bridge keeps
hitting *GR instances* of the same law — δ is information-limited given SNR (leg 2/7); MN thin chaos is below
box-dimension's resolution but above the frequency-drift detector's (leg J); di-hole chaos is unreachable by
a trajectory 0-1 test but reachable by a section frequency-drift (leg R). No discovery limit here is
absolute; each is a statement about a *specific instrument at a specific sampling*. The bridge's three chaos
lenses (box-dim, de-noised Lyapunov, frequency-drift) and tabula's (0-1 test) tile complementary regions —
which is exactly why the multi-instrument, multi-repo cross-validation is worth doing.

**Open (unchanged):** the deep chaotic sea at x<1.5 (higher-precision integration, both repos).

## Phase 6 (2026-07-03) — round-5: the family grows to four

| item | leg | result |
|---|---|---|
| **v3 spin tension resolved** | leg B | deepstrain's §22/§23 start-time referee: the raw-fit/package/NPE differences are ONE measured 9-point systematic family (M 74.7→65.9); NPE sits at the peak; overtone decisive at every start. Surfaced by v3, explained by the referee (`0ff1ffa`) |
| **KK tower, 4 repos** | **leg S (new)** | m_n = n/R by four disjoint routes: ansatz-proven reduction (§111, trap caught) · quantum direct numerics (0.22%) · tabula independent FDTD (0.66%; cross-impl 0.44%) · tabula neural discovery from projections (1.44%, R²=0.99996). Gate PASS — the first FOUR-repo cross-validation; **quantum welcomed as the 4th sister** (`d84e74a`) |
| **GW250114 mimicker status** | leg 8 §7 | ansatz §110's two-light-ring taxonomy × the bridge stack: prompt ringdown = one-ring Kerr physics (3 pipelines), echoes null at the Planck Δt, R_eff≲0.2 — every tested observable reads "one ring"; scoped as consistency, not horizon proof (`69c7977`) |
| **Mercury anomaly accounting** | **leg T (new)** | pre-registered Le Verrier decomposition: tabula's real-data 120-yr total (568.4″/cy) − Clemence Newtonian (532.3) = 36.1 vs exact GR 43.0 (computed with tabula's own measured GM☉) — closes within ~1σ of the 6.6″/cy instrument floor. Consistency, not detection (`4e9c643`) |
| **learned ≈ classical at the wall** | note | deepstrain follow-up A: a CNN forward pass TIES a realizable 1,619-template matched-filter bank (0.472 vs 0.489, identical injections; both far under the true-template oracle 0.72) → the operative wall is TEMPLATE-BANK MISMATCH, not learned-vs-classical — another entry in the walls-are-instrument-relative ledger (Phase 5), and their co-injection protocol shrank an apparent 10% MF win to a 3% tie (their own north-star catch) |

**Family status:** four sisters (ansatz · tabula · deepstrain · quantum), two new legs (S, T), 20 legs + 8
moves total. Open frontier unchanged: MN deep sea x<1.5 (higher-precision integrator, parked).
