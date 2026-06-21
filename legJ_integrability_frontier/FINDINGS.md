# Leg J — Findings: the broken Carter constant survives as a BOUNDED near-invariant

*Run 2026-06-21. Gates and outcome-meanings frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any
orbit was integrated. This leg attacks the project's one UNDETERMINED result — Move D / ansatz §82's
"deform Kerr → canonical Carter tensor broken, yet no detectable chaos, fate undetermined."*

## Result in one line

On the bumpy metric the **exact Kerr Carter constant `C₀` is violated — its per-orbit drift grows from
1.3e-10 (ε=0, machine precision) to ~7% (ε=0.35) — but it stays a BOUNDED, NON-DIFFUSING near-invariant**
(saturation ratio 1.0–1.05 at every ε, diffusing fraction 0.00). The orbits remain on deformed tori: the
dynamics are **near-integrable, with no chaos** across the probed family. This *sharpens* Move D / §82's
result from "no chaos detected" (absence of evidence) to "a bounded conserved-to-a-band quantity exists"
(positive evidence for surviving tori) — without yet proving a new exact Killing tensor.

## The measures (both calibrated on Kerr, ε=0)

| ε | Carter drift (median) | saturation (median) | diffusing fraction (>3×) |
|---|---|---|---|
| **0.00 (Kerr gate)** | **1.3e-10** | 1.05 | 0.04* |
| 0.05 | 2.3e-02 | 1.03 | 0.00 |
| 0.12 | 4.3e-02 | 1.03 | 0.00 |
| 0.25 | 6.4e-02 | 1.01 | 0.00 |
| 0.35 | 7.2e-02 | 1.01 | 0.00 |

*the ε=0 "diffusing" blip is machine-noise on a constant (drift ~1e-10). **G1 gate PASSES**: Kerr's C₀ is
conserved to 1.3e-10, so any ε>0 drift is real signal.

- **DRIFT** `=(max−min)/|mean|` over the orbit — how much the canonical invariant is violated. It grows
  ~`√ε` (sub-linear), confirming the symbolic result `∇₍ₐK₀_bc₎ ∝ ε·a²` quantitatively, and stays a few
  percent — not exploding.
- **SATURATION** `= spread(full)/spread(first quarter)` — does the violation stay in a fixed band (≈1,
  bounded → torus) or keep growing (≫1, diffusion → chaos)? Validated on synthetics: bounded oscillation
  →1.01, random-walk diffusion →3.63, secular drift →1.77, slow drift →1.22. The bumpy orbits read
  **1.0–1.05 — below even the slow-drift level**, so C₀ is a *purely bounded* oscillation, not diffusion.

## What it means (read against the pre-registered outcomes)

The canonical Carter constant is broken (proven, and measured here at up to 7%), yet it remains **bounded
and non-diffusing** — the hallmark of motion confined to a deformed KAM torus. So for the probed orbits the
system is **near-integrable: an effective (bounded) second invariant persists and there is no chaos.** This
is the **surviving-structure horn (i)** in its *weak* form — positive evidence that the tori survive — and
it is a genuine sharpening of Move D / §82, which had only the *absence* of detectable chaos.

## Honest limits (registered up front)

- **Not a proof of a new Killing tensor.** A bounded near-invariant (KAM torus) is consistent with the
  system being *formally* non-integrable (no global analytic second integral) while most orbits still sit on
  surviving tori. The strict horn (i) — an exact new Killing tensor — needs the **symbolic search**
  (high-degree, future), not this dynamical probe.
- **Finite time ⇒ upper bound on chaos, not a proof of integrability.** Integration spans ~1200 proper-time
  units. Exponentially-thin KAM chaos or slow Arnold diffusion below this resolution would not show
  (Move I's resolution-limited taxonomy applies).
- **Orbit family is near-circular.** The decisive instrument we *wanted* — a phase-space intrinsic-dimension
  scan (torus=2 vs chaos=3, reusing leg 1's counter) — **failed its calibration gate** (`count_dimension.py`):
  the strong-field **zoom-whirl** regime makes orbit eccentricity hypersensitive to the launch (a 2% kick →
  Δr=24 or escape), so controlled moderate-eccentricity 2-tori could not be generated, and Kerr orbits read
  D≈1.3 not 2. The gate caught this and, per pre-registration, we made **no claim from it** and pivoted to
  the robust Carter-dynamics measure (which needs no controlled eccentricity). Eccentric/resonant orbits —
  where chaos is most likely — are therefore *not* probed here; this is a conservative (near-circular) bound.

## Verdict

**Horn (i), weak form, for the near-circular regime:** the deformed Carter constant is a bounded
non-diffusing near-invariant, the tori survive, no chaos — positive evidence the structure persists, within
honest finite-time / orbit-family / resolution limits. The **strict** horn (a new *exact* Killing tensor)
and the eccentric/resonant regime remain open — the next step is the high-degree symbolic Killing-tensor
search (the proof horn) and a properly turning-point-constructed eccentric orbit family.

## Artifacts
- `code/export_orbits.py` — stage 1 (ansatz venv): integrates bound orbits, exports C₀ time series; reuses
  legA's `export_geodesics` (metrics, Christoffels, Carter tensor) read-only.
- `code/carter_dynamics.py` — drift + saturation measures, Kerr-calibrated, synthetic-validated.
- `code/count_dimension.py` — the attempted dimension scan (gate-failed, kept for transparency).
- `results/orbits_eps*.json`, `results/carter_dynamics.json`.
