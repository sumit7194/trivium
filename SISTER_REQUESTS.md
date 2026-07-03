# Sister-project requests — what would unblock the bridge's open items

*The bridge keeps the three source repos READ-ONLY. These are requests to relay to the relevant sister
project's own Claude session (the way ansatz's §77/§78/… upgrades were produced). Each unblocks a bridge
item that is currently PARTIAL or PARKED. Compiled 2026-06-24.*

---

## Round-5 status (2026-07-03) — the QUANTUM project joins as the 4th sister

`/Users/sumit/Github/quantum` (local-only, QM-foundations lab) is now formally in the family: it already
runs the sister-ask pattern itself (3 asks → ansatz §111–§113 KK proofs + trap; tabula §157 KK-mass
discovery), and the bridge's **leg S** joined its flagship claim (m_n = n/R) across all four repos, gated.
No open asks this round — the sisters' autonomous output (deepstrain §22/§23 referee + follow-up A; ansatz
§110/§112/§113; tabula EXP-15/§157; quantum `fractal_boundary`/`kk_projection`) was consumed read-only
into legs B/S/8/T/U/V. Parked frontier unchanged
(MN deep sea). **leg U** then took ansatz's two *new* KK sections one rung up: §112's proven 6D T²
diagonal-metric tower and §113's twist-is-an-axion, reproduced on the bridge's own two-loop simulator (the
axion measured as a degeneracy-splitting). A natural *optional* sister ask sits here if wanted: a **neural
6D** discovery (tabula) or **6D direct numerics** (quantum) would give leg U the same four-route breadth
leg S has — currently it is bridge-numeric + ansatz-symbolic only.

## Round-4 status (2026-07-02) — no open asks; sisters self-directed and integrated

All prior asks are fulfilled. This round the sisters worked autonomously and the bridge integrated their
output read-only (no new requests were needed):
- **ansatz §105/§106** — natively reimplemented the bridge's frequency-drift detector (reproduces MN
  orbit_A/orbit_B to the digit) and exhibited **ZV δ=2's** own thin-layer chaos → legs J + O (`837d4fc`).
  The bridge's instrument propagated *upstream* — the first tool (not bug) to flow into a source repo.
- **deepstrain R2v2 + E3** — field-standard `ringdown` package re-detects the GW250114 overtone (three
  pipelines agree on M to 0.00 M⊙) → Move B v3 (`6ab92cd`); echo search at the Abedi-predicted Δt, all
  null → leg 8 (`beb3a0b`).
- **tabula EXP-1..12 frontier** — the "representability frontier" (5 verdicts, 3 axes). The bridge
  cross-validated its **regime detector** against exact-GR ground truth → **leg R** (`70d5e2f`): the
  integrable≠regular dissociation on Manko–Novikov, matching bridge ground truth.

**One standing item (either repo, no rush):** the MN **deep chaotic sea** at x<1.5 — beyond trustworthy
integration on both sides; needs a higher-precision (symplectic / extended-precision) integrator before the
frequency-drift detector can be pointed at it. Parked, not requested.

## → deepstrain (BlackHole): A1 (amortization → transfer) — ✅ FULFILLED (2026-06-24): §19 artifact delivered; bridge verdict in leg L (amortization does NOT predict transfer, corr≈0). Decisive follow-up (more variants/injections, C2ST) optional.

<details><summary>original ask</summary>

**Why it's blocked:** the bridge (leg L) showed the *per-parameter* legibility predicts real-data precision
on ONE NPE. The deeper claim — does an NPE's **amortization gap predict its transfer** — needs *several*
NPEs spanning a range of amortization, which only deepstrain can train.

**The ask (concrete):**
1. Train ~5 no-hair δ NPE **variants** that deliberately span a range of amortization. Levers (any 1–2):
   - training-set size (you already have two points — 09_posterior and 09_posterior_150k — add e.g. ~10k,
     ~500k);
   - summary-net capacity (`Embed n_out`, conv width);
   - flow expressivity (`num_transforms`, `hidden_features`).
2. For each variant, report TWO numbers on a common held-out set:
   - **amortization gap (on SIM):** simulation-based calibration error (SBC / coverage deviation from
     nominal), **or** a C2ST between the amortized posterior and a per-x reference (importance-resampled or
     a short MCMC). Either is a fine "how much did amortization compromise the per-x posterior" proxy.
   - **transfer (sim→real):** coverage on REAL O4-noise injections (your §09 R2 already does these) minus
     the sim-noise coverage — how much the inference degrades sim→real.
3. Save the checkpoints + a small JSON `{variant, amortization_gap, transfer}`.

**What the bridge then does:** correlate amortization_gap vs transfer across the variants (read-only) — the
full §9 test. With 2 points it's a hint; ~5 makes a real correlation. *Prediction to falsify:* bigger
amortization gap → worse (or better!) transfer — genuinely unknown, which is why it's the "most original."

---

</details>

## → deepstrain (BlackHole): A5 (precise multi-event no-hair) — ✅ FULFILLED (2026-06-24): §18 raw tone fits delivered; bridge result in leg B (220 cross-check across 5 events; 221 info-limited).

<details><summary>original ask</summary>

**Why it's blocked:** Move B v2's exact-Leaver δ test needs the **raw 220/221 tone fits** (f, τ, amplitudes)
per event. Currently only GW250114 (§06) has them; §13's other 7 events expose only the NPE δ posterior.

**The ask:** export, per event in §13 (GW150914, GW170814, GW170104, …), the raw single-/two-mode ringdown
fit — `f_220, τ_220, f_221, τ_221` (+ amplitudes) — as you already do for GW250114 in §06.

**What the bridge then does:** invert each event's 220 via exact Leaver → (M, χ), predict the 221, compute a
per-event precise δ, and stack — extending Move B v2 from one event to the catalog (a real multi-event
no-hair precision test).

---

</details>

## → ansatz (conjecture_machine): B1 + FD-fix + chaos launcher — ✅ ALL FULFILLED (2026-06-26, §101 commit b05e2b3)

ansatz delivered `emri.py` (Peters-validated `quadrupole_flux`) → B1-full quasi-circular inspiral (leg M
step 3): the bump lowers ω_φ at each ω_r:ω_θ resonance by −4.8%→−12.6%. Then §101 closed the three follow-ups:
- **`dQ/dτ` Carter flux** (`quadrupole_flux(carter=True)`) → leg M step 4: the inclined inspiral **de-inclines**
  (Kerr clean); the leading-order kludge degrades on the strong bump (flagged).
- **FD-noise Lyapunov fix** — ansatz *independently reproduced* the bridge's false-positive (λ≈0.32 on a
  regular orbit) and shipped the de-noised defaults → leg J gap closed.
- **`mn_bound_orbit` launcher + genuine-chaos validation** (box-dim 1.34 on Hénon–Heiles §84; λ 2.09 on the
  di-hole §79) → leg J's detectors are now validated *on* chaos.

**Remaining (refined) asks:**
1. **Reliable inclined-orbit flux on the strong bump** — ✅ **FULFILLED (2026-06-26, ansatz `f4cc1b1`)**: two
   bugs fixed (convergence-plateau cutoff for `dE`, Burke–Thorne RR force for `dQ`). Bridge re-ran
   `inspiral_inclined.py`: MN q=0.2 `dE/dτ` now physical, `dQ/dτ` < 0 and monotone — the inclined inspiral
   de-inclines cleanly **in the bump** too (leg M step 4 updated). B1's eccentric-inclined case is unblocked.
2. **MN chaotic initial data** — ✅ **RESOLVED (2026-06-26, ansatz §102 `3e08fef`+`3468cc2`)**, with two
   outcomes bigger than the ask:
   - **A metric correctness bug, found + fixed.** Making MN computable at χ=0.9, q=0.95 exposed that
     `manko_novikov` was *never asymptotically flat for q≠0* (g_xx → 0.085× Minkowski at infinity; the vacuum
     check couldn't see it). Fixed; q=0 byte-identical to Kerr; **orbit paths preserved** → all bridge box-dim/
     section/positive-control results invariant (B1-full re-verified unchanged; B1-eccentric flux re-run).
   - **The chaos is an honest null at that extreme.** χ=0.9,q=0.95 splits into three wells — inner
     CTC-degenerate (near-rod naked singularity), second-region lens abutting it, outer clean+regular. The
     chaotic basin is **pathology-bound**, not a clean sea; MN's geometric chaos is thin-layer near resonances
     (same elusiveness as ZV). §99's no-Carter (non-integrable) proof stands.
   - **Open (optional) path to a *clean* positive control:** moderate q (~0.3–0.6, clean metric) + literature
     ICs + a **rotation-number sweep** across a low-order resonance to resolve the thin layer (gross box-dim
     grazes it ≤1.22; the finite-differenced Hamiltonian makes high-res sections compute-prohibitive). Not
     required — the detectors are already validated on Hénon–Heiles + di-hole.

## → deepstrain (BlackHole): echo Δt ↔ Abedi — ✅ FULFILLED (2026-06-26): §18 `18_abedi_crosscheck.json` → leg 8 (`abedi_crosscheck.py`); the formula reproduces Abedi 2017 Table I to 98.5–99.7%, the literature anchor.

## → tabula (SpaceTime/curvature): ZV γ-metric legibility — ✅ FULFILLED (2026-06-26): §132 `132_zv_gamma_metric.json` → leg Q; legible⟺KY-integrable now 7/7 (φ=1.0), a 2nd independent non-integrable case.

<details><summary>original ask</summary>

**The ask (bigger):** an EMRI **GW-flux / radiation-reaction** model — `dE/dτ, dL/dτ` (and ideally `dQ/dτ`)
for inspiraling orbits in Kerr and the bumpy metric (Teukolsky-based, or a calibrated post-Newtonian/
kludge flux). **What the bridge then does:** drive a self-consistent inspiral through a resonance and read
off the waveform's resonance-crossing signature.

</details>

---

## A10 (geometrizes-proof) — ✅ FULFILLED (2026-06-26): well-posed reframe answered + bridged in leg Q (legible ⟺ KY-integrable, 5/5, φ=1.0)

The ill-posed form ("geometrizes ⟺ universal ∧ conservative as an *exact proof* on the ansatz catalog")
stays retired — not a metric theorem. The **well-posed revival** — does a learned geometry *become legible*
**iff the metric is integrable** (admits a Killing tensor)? — was answered by tabula (§127) and bridged in
**leg Q**: tabula's neural `legible` column vs leg O's symbolic `KY-integrable` column agree **5/5** across
the catalog (Kerr/KN/KdS/Taub–NUT legible+integrable; bumpy neither), Matthews **φ=1.0**; the two
single-repo metrics (Schwarzschild, bumpy-strong) are consistent too. Two deliberately-independent repos,
identical per-metric verdict — the clean, cross-validated version of the §9 claim.

<details><summary>original ask</summary>

- *tabula ask:* run the geometrization/legibility probe on observations from each catalog metric
  (Kerr, KN, KdS, Taub–NUT, bumpy).
- *bridge then:* correlate "geometrizes (legible)" against leg O's "KY-integrable" column. A clean,
  testable version of the §9 claim.

</details>
