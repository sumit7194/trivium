# Move G — Pre-registration: adversarial falsification of the bridge's main claims

*Frozen 2026-06-19. A deliberate attempt to BREAK our own results. Each test is designed so that a
specific failure mode, if present, shows up as a signal. Stated outcome-neutrally — the goal is to
find where the claims fail, not to confirm them. We report whatever happens.*

## The mindset (the operating rule for this leg)

For each claim we ran a control that **should be null if the claim is real and should fire if the
claim is an artifact.** We commit, before running, to reporting the raw result regardless of which
way it goes. A claim that survives a genuine break-attempt is stronger; one that breaks is corrected.

## Test 1 — Move A: does the discovery pipeline HALLUCINATE invariants? (negative controls)

Move A's headline: tabula blindly recovered the exact Carter constant (cosine 1.0000). The dangerous
failure mode: a flexible distiller finds "conserved" structure in data that has none.
- **1a NOISE:** replace the Kerr trajectories with random noise of the same shape. A sound method →
  DESTROYED (held-out var-ratio > ε_T). If it says EXISTS, the method hallucinates invariants.
- **1b SHUFFLE:** take the REAL Kerr trajectories but shuffle `p_θ` across timesteps within each
  trajectory (destroys the conserved θ–p_θ relation). A sound method → DESTROYED. If EXISTS, it is
  fitting spurious structure.
- **1c TIME-REVERSAL/SCRAMBLE of the labels:** permute which trajectory each sample belongs to. →
  DESTROYED expected.
- *Falsified iff* any control returns EXISTS (var-ratio < ε_T = 1e-2). *Survives iff* all → DESTROYED.

## Test 2 — Move A: does it recover the TRUE spin, or a fixed answer? (generalization)

Move A recovered `a²` for a=0.6 and a=0.9. Failure mode: the basis forces a fixed output, so "recovery"
is an artifact. Run the distiller on Kerr at **five spins** a ∈ {0.1, 0.3, 0.5, 0.7, 0.9} and check the
recovered `c_cos2_E2/c_ptheta2` tracks the TRUE `−a²` across all of them.
- *Falsified iff* the recovered coefficient does NOT track `−a²` (e.g. flat, or wrong). *Survives iff*
  it tracks `−a²` with high correlation across spins it never "expected."

## Test 3 — Move F: break "metric divergence" (additional 2×2 cells)

Move F concluded the bulk/edge effect needs a conformal boundary where the metric diverges. Three
break-attempts:
- **3a HEMISPHERE** (positive curvature + a *finite-metric* boundary): if the effect needs only
  "curvature + boundary", this fires; if it needs *divergence*, it stays null. *Predicted null* — a
  fire falsifies "metric divergence."
- **3b UNBOUNDED-FLAT** (a flat space sampled to huge radius — unbounded distance, but *constant*
  sensitivity): isolates "unbounded distance" from "diverging sensitivity." A fire would mean mere
  unboundedness causes it.
- **3c FLAT-WITH-DIVERGING-METRIC** (a flat space given a distance that diverges at a fake boundary,
  `d = −log(1−r)`): if a FLAT space with a diverging metric FIRES, then curvature is irrelevant and
  it is purely the divergence — sharpening F further (and falsifying any residual "curvature" reading).
- *Outcomes:* 3a fire ⇒ F wrong (it's curvature+boundary). 3c fire ⇒ F right and curvature-free
  (pure divergence). 3b fire ⇒ it's unboundedness, not divergence rate.

## Test 4 — The synthesis: is "exact owns the edge" fundamental, or coordinate-dependent?

The synthesis says a learned method loses the edge. Failure mode: the edge is only hard in the
*observation coordinates we chose* (Euclidean), not fundamentally. Give the learned recoverer the
**intrinsic radius `r`** (the natural coordinate) instead of Euclidean `(x,y)`, on the hyperbolic disk.
- *Falsified (qualified) iff* learning then recovers the edge fine (edge/bulk drops to ~1) — the edge
  failure is representation-dependent, not a fundamental learned-vs-exact divide. *Survives iff* the
  edge stays hard even with the intrinsic coordinate (the divergence is irreducible).

## Honest commitment

We report the raw outcome of every control. Any "FALSIFIED" is recorded as prominently as any
"SURVIVED", and the affected claim's wording in THE_BRIDGE / FINDINGS is corrected accordingly. No
threshold or control is changed after seeing results.

## Deliverables
- `code/falsify_moveA.py` — the noise/shuffle/scramble controls + the multi-spin generalization.
- `code/falsify_moveF.py` — the hemisphere / unbounded-flat / flat-diverging cells + the
  intrinsic-coordinate (Test 4) probe.
- `FINDINGS.md` — per-test SURVIVED / FALSIFIED, with corrections where anything broke.
