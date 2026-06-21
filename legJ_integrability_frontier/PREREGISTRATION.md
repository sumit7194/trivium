# Leg J — Pre-registration: does a hidden symmetry survive the bump? (the Move D / §82 open horn)

*Frozen 2026-06-21, before any orbit is integrated or dimension counted. This leg attacks the one
UNDETERMINED result in the project: Move D and ansatz §82 both found that deforming Kerr breaks the
canonical Carter Killing tensor (proven, `∇₍ₐK₀_bc₎ ∝ ε·a²`) **yet show no detectable chaos** — leaving
two horns: (i) a DIFFERENT hidden symmetry survives (still integrable), or (ii) the system is
non-integrable but the chaos hides in KAM layers below Lyapunov detection.*

## What changed the plan (logged honestly)

The original recommendation was a *complete polynomial Killing-tensor existence search at degree 2*.
Inspecting Kerr's own Carter tensor first (the calibration case) showed its lower-index components are
**degree-6 numerators over Σ, Δ, (1−u²) denominators** — so a degree-2 polynomial search would not even
contain Kerr's *known* Carter constant. The honest consequence: a genuinely complete symbolic search
needs high-degree rational machinery (≳450 unknowns) that risks swamping. So this leg leads with two
**decisive, calibrated, tooling-reusing** methods and flags the full symbolic search as a heavier
follow-up — rather than ship a degree-2 search that is provably blind to the answer.

## The two methods (each calibrated on Kerr = known integrable, then run on bumpy)

**Method A — phase-space intrinsic-dimension scan (the centerpiece; reuses leg 1's counter).**
An integrable bound orbit lies on a 2-torus in the (r, u, u^r, u^θ) phase plane; a chaotic orbit fills a
3-D energy shell. So the *intrinsic dimension of the orbit's point cloud* is the integrability
diagnostic — and it is integrated over the whole orbit, so it is more sensitive to moderate chaos than a
local Lyapunov exponent. We feed the orbit cloud to **leg 1's bottleneck autoencoder counter** (the
bridge's validated intrinsic-dimension tool) plus a correlation-dimension cross-check.

**Method B — Carter-constant drift (the analytic companion; the actual C₀, not a learned proxy).**
Track Kerr's *exact* Carter constant `C₀ = K₀^{ab}p_a p_b` along bumpy geodesics. On Kerr it is conserved
(drift = 0). On the bumpy metric its spread/drift over many periods measures how badly the canonical
invariant fails — the principled version of Move D's learned-proxy variance.

## Frozen gates and predictions

- **G1 (calibration gate — MUST pass or the leg is void):** on **Kerr**, Method A reads intrinsic
  dimension **2** for every bound orbit (corr ≥ 0.95 to dim 2), and Method B gives Carter drift
  consistent with 0 (≤ integration error). If Kerr orbits do not read 2, the instrument is not
  trustworthy and no bumpy claim is made.
- **G2 (the test):** on the **bumpy** metric (a=0.6, ε swept 0 → 0.35, the Move A rung), report the
  per-orbit dimension distribution and the Carter drift vs ε. **No outcome assumed.**

## What each outcome MEANS (registered before seeing it)

- **Dimensions stay 2 across orbits + Carter drift bounded** → tori survive; consistent with horn (i)
  (a deformed invariant persists) OR chaos below this instrument's resolution. Does *not* prove a new
  Killing tensor — that needs the symbolic search — but bounds the chaotic volume from above.
- **A fraction of orbits read 3 + Carter drift grows with ε** → those tori are destroyed; horn (ii) for
  that region of phase space. The fraction vs ε is the chaotic-volume growth curve.
- **Honest scope (registered):** like leg 1, the dimension counter is resolution-limited (Move I's
  taxonomy) — it detects *thick* chaos / destroyed tori, not exponentially-thin KAM layers. A null
  (all dim 2) is an *upper bound* on chaos at this resolution, never a proof of integrability. The proof
  horn (a surviving Killing tensor) is reserved for the symbolic search (future, high-degree).

## Discipline
Source repos read-only. Stage 1 (orbit integration, ansatz venv) exports only phase-space point clouds;
stage 2 (dimension counting, tabula venv) is blind to the metric label until the verdict is assembled.
Reuses `export_geodesics.py` (integrator, g_kerr/g_bumpy) and leg 1's `count_bottleneck` AE, additively.
