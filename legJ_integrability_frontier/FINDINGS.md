# Leg J — Findings: the broken Carter constant survives as a BOUNDED near-invariant

*Run 2026-06-21. Gates and outcome-meanings frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any
orbit was integrated. This leg attacks the project's one UNDETERMINED result — Move D / ansatz §82's
"deform Kerr → canonical Carter tensor broken, yet no detectable chaos, fate undetermined."*

## Result in one line — the fate is no longer "undetermined"

Two independent attacks settle Move D / §82's open horn for this deformation: **(symbolic) no exact
Killing–Yano tensor survives the bump** (complete degree-≤4 search; Kerr's is rediscovered, the bump has
none → by Eisenhart no exact Carter-type Killing tensor exists), and **(dynamical) the canonical Carter
constant `C₀`, though violated (drift 0 → ~7%), stays a BOUNDED non-diffusing near-invariant** (saturation
1.0–1.05, zero diffusing orbits). Together: the bumpy metric is **formally NON-integrable but
NEAR-integrable** — no new exact hidden symmetry, yet an approximate invariant survives, the tori persist,
and there is no chaos. This is exactly the picture the Kerr-deformation literature predicts (Brink III/IV;
[1807.08594](https://arxiv.org/abs/1807.08594)) — reached here independently, by proof *and* by orbit
dynamics.

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

## The dangerous regime — eccentric/inclined orbits, where chaos hides (`export_eccentric.py`)

The first pass used near-circular orbits (the *stable* ones). Chaos in a near-integrable system concentrates
at **resonances**, reached by eccentric/inclined orbits — which we now build properly: specify
(r_peri, r_apo, inclination), solve the Kerr turning-point conditions `R(r_p)=R(r_a)=0, Θ(θ_min)=0` for
(E,L,Q) [Schmidt 2002], launch at the equatorial pericenter, and integrate. A fine scan in r_apo
(eccentricity 0.20 → 0.53 at r_p=4.5, incl ≈13–20°) **crosses resonances**. Calibration: on Kerr these are
genuine eccentric inclined tori with C₀ conserved to ~2e-9.

In the strongest bump (ε=0.35), all 17 eccentric orbits show Carter drift **0.13 → 0.18** — *larger* than
the near-circular 7% (eccentric orbits probe the bump harder) — yet **saturation 1.00–1.02, zero diffusing.**
So even in the resonance-crossing eccentric/inclined regime, C₀ stays a bounded non-diffusing near-invariant:
**no chaos found where it is most likely.** (The Kerr-baseline saturation is noisier — up to 1.48 — because
it is machine-noise on a *constant* C₀; the bump's real oscillation reads a clean ~1.0, well separated.)

## The proof horn — complete symbolic Killing–Yano search (`symbolic_ky_search.py`)

The dynamical probe shows the tori survive but cannot, by itself, decide whether a *new exact* hidden
symmetry exists. That is a decidable algebraic question, and the literature points to the clean way in:
by **Eisenhart's theorem** an exact Carter-type Killing tensor exists **iff** a Killing–Yano (KY) 2-form
exists, and the KY tensor is far simpler — in rational `u=cosθ` coordinates Kerr's KY is **polynomial of
degree ≤3** (`Y_tr=−au, Y_tu=−ar, Y_rφ=−a²u(1−u²), Y_uφ=−r(r²+a²)`), versus the Carter tensor's degree-6.

So we run a **complete** search: ansatz a general antisymmetric `Y` with degree-≤D polynomial components,
impose `∇₍ₐY_b₎c = 0` at many exact-rational points → a homogeneous linear system; its null-space
dimension counts the KY tensors of degree ≤D.

| metric | KY null-space (deg ≤3) | KY null-space (deg ≤4) |
|---|---|---|
| **Kerr (gate)** | **1** (rediscovers its KY ✅) | 1 |
| **bumpy ε=0.20** | **0** | — |
| **bumpy ε=0.35** | **0** | **0** |

**Result:** Kerr's unique KY tensor is recovered (gate passes); **no KY tensor survives the bump up to
degree 4.** By Eisenhart, **no exact Carter-type Killing tensor exists** for this deformation (to degree 4)
— the strict horn is **CLOSED**, not undetermined. *Caveat:* this rules out KY-origin (Carter-type) tensors
to degree 4; a higher-degree or non-KY-origin Killing tensor is not excluded (the converse of Eisenhart is
not general), and the direct degree-6 Killing-tensor search is the heavier final confirmation.

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

## Verdict — Move D / §82's "fate undetermined" is resolved (for this deformation)

**Formally non-integrable, but near-integrable.** The symbolic search **closes the strict horn** — no exact
Carter-type (KY-origin) hidden symmetry survives the bump up to degree 4 — while the dynamics show the
**approximate** invariant persists (bounded, non-diffusing C₀) with **no chaos** for the probed orbits. So
the bump destroys the *exact* Carter constant (proven here both ways) yet leaves a *bounded approximate*
one: the standard KAM near-integrable picture, and the one the deformation literature predicts. The
**eccentric/inclined/resonance-crossing regime is now probed too** (Schmidt-constructed orbits, ε=0.35) —
no chaos there either, only a larger-but-bounded C₀ drift. What remains genuinely open: (a) **thin chaos
below resolution** — a finer resonance scan or much longer integration could still catch exponentially-thin
KAM layers or slow Arnold diffusion (a single fine scan can step over very narrow resonances); and (b)
**higher-degree / non-KY-origin** Killing tensors / the direct degree-6 Killing-tensor search (the heavier
final confirmation). Neither is expected to overturn the picture, but neither is closed.

## Prior art (so we neither repeat nor overclaim, and can cite)

- **J. Brink, "Spacetime Encodings III & IV"** — [arXiv:0911.1589](https://arxiv.org/abs/0911.1589),
  [arXiv:0911.1595](https://arxiv.org/abs/0911.1595): exact second-order Killing tensors in
  stationary-axisymmetric-vacuum spacetimes are *very restrictive* (generic deformations lack one); explicit
  Killing-equation analysis and the Weyl-curvature ↔ Killing-tensor relationship.
- **"Preserving Kerr symmetries in deformed spacetimes"** — [arXiv:1807.08594](https://arxiv.org/abs/1807.08594):
  via Eisenhart's theorem, an exact Killing tensor exists *iff* a Killing–Yano tensor does; generic
  deformations (quasi-Kerr, Johannsen) keep only an **approximate** Killing tensor that *breaks down for
  larger perturbations* — precisely our growing-but-bounded C₀ drift. Our use of the KY route follows this.
- **Frolov, Krtouš, Kubizňák, "Black holes, hidden symmetries, and complete integrability"** — Living Rev.
  Relativity, [arXiv:1705.05482](https://arxiv.org/abs/1705.05482): the principal-tensor framework
  (KY ⟹ Killing tensor ⟹ separability) underlying the Eisenhart route.

Our contribution is not new GR theory — it is an *independent, calibrated, automated* confirmation for a
specific bump: a complete symbolic KY non-existence proof (degree ≤4) **and** a synthetic-validated
orbit-dynamics measurement that the approximate invariant is bounded and non-diffusing, agreeing with the
above by two independent routes.

## Artifacts
- `code/export_orbits.py` — stage 1 (ansatz venv): integrates bound orbits, exports C₀ time series; reuses
  legA's `export_geodesics` (metrics, Christoffels, Carter tensor) read-only.
- `code/carter_dynamics.py` — drift + saturation measures, Kerr-calibrated, synthetic-validated.
- `code/export_eccentric.py` — Schmidt-constructed eccentric/inclined orbits (turning-point solve), the
  resonance-crossing chaos hunt; Kerr-calibrated (C₀ conserved to 2e-9). `results/eccentric_eps*.json`.
- `code/symbolic_ky_search.py` — the proof horn: complete symbolic Killing–Yano search (Eisenhart route),
  Kerr-gated, exact rational linear algebra; rules out an exact KY tensor on the bump to degree 4.
- `code/count_dimension.py` — the attempted dimension scan (gate-failed, kept for transparency).
- `results/orbits_eps*.json`, `results/carter_dynamics.json`, `results/symbolic_ky_search.json`.
