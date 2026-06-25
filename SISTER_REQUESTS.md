# Sister-project requests — what would unblock the bridge's open items

*The bridge keeps the three source repos READ-ONLY. These are requests to relay to the relevant sister
project's own Claude session (the way ansatz's §77/§78/… upgrades were produced). Each unblocks a bridge
item that is currently PARTIAL or PARKED. Compiled 2026-06-24.*

---

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

## → ansatz (conjecture_machine): B1 (full EMRI inspiral) — ✅ FULFILLED for circular (2026-06-26); dQ/dτ remains for eccentric-inclined

ansatz delivered `emri.py` with a Peters-validated `quadrupole_flux` (`dE/dτ, dL/dτ`) on Manko–Novikov. The
bridge used it (leg M step 3, `inspiral_mn.py`) to drive a **self-consistent quasi-circular inspiral** that
traverses the ω_r:ω_θ resonance sequence — Q=0 on circular equatorial orbits, so no dQ/dτ was needed. The
MN bump lowers ω_φ at each resonance crossing by a deviation growing inward (−4.8% at 3:4 → −12.6% at 1:3).
**B1 is closed for the circular case.**

**Remaining (smaller) ask — `dQ/dτ`:** a Carter-flux for **eccentric + inclined** inspirals, so the bridge
can drive a generic (not just circular) orbit through a resonance and see the resonant kick on the *third*
integral. The `dE/dτ, dL/dτ` halves already exist; only the Carter-flux is missing.

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
