# Leg R — Findings: tabula's frontier regime detector vs exact-GR ground truth (dynamics-level A10)

*Run 2026-07-02. Predictions frozen in [PREREGISTRATION.md](PREREGISTRATION.md) (with a transparent
representation-fix amendment) before any verdict was seen. tabula's EXP-9/10 "robust detector" (script 150:
`EMIT-regular | CERTIFY-CHAOS | MIXTURE | ABSTAIN`, a Gottwald–Melbourne 0-1-test instrument validated 9/9
on its own menu — Kepler/Lorenz/Hénon–Heiles/Bell/geometry) had never seen general-relativistic geodesics.
The bridge fed it exact-metric trajectory ensembles, blind, whose ground truth the bridge established with
three independent instruments (symbolic KY/Carter algebra; box-dimension; the frequency-drift detector).
This is the dynamics-level analogue of leg Q's legibility⟺integrability cross-validation.*

## Result in one line

tabula's regime detector, run blind on GR geodesic ensembles, **correctly reads both regular cases** — Kerr
(integrable) and Manko–Novikov q=0.5-outer (non-integrable but KAM-regular) both `EMIT-regular`. The prize
is what that second verdict *means*: on the **same** MN q=0.5 metric, tabula's two instruments **dissociate**
— the regime detector says **regular** while the legibility probe (§144) says **illegible / non-integrable**
— because they measure different things (is-it-chaotic vs does-an-exact-invariant-exist). That is tabula's
own **EXP-7 dissociation** (law-learnability ≠ trajectory-predictability), now instantiated on an exact GR
metric, and it **matches the bridge's dual ground truth exactly**: non-integrable (leg O: no KY tensor) yet
dynamically regular (leg J: box-dim + frequency-drift). The chaotic case (a di-hole) surfaced a clean
**scope boundary** of the 0-1 test rather than a chaos detection — diagnosed below.

## The blind test (pre-registered)

| class | GR system | bridge ground truth | tabula verdict | frac_chaotic | vs prediction |
|---|---|---|---|---|---|
| **C1** | Kerr `= manko_novikov(q=0)`, 20 orbits | integrable + regular | **EMIT-regular** | 0.00 | ✅ as predicted |
| **C2** | MN `q=0.5` outer, 20 orbits | **non-integrable** yet **KAM-regular** | **EMIT-regular** | 0.00 | ✅ as predicted (the dissociation) |
| **C3** | Majumdar–Papapetrou di-hole, 20 orbits | chaotic (λ=2.09, §79) | EMIT-regular | 0.00 | ❌ **miss** — diagnosed (scope boundary) |

C1/C2 differ **only in q** (same E, L, coordinates, integrator) — a controlled integrability comparison.

## Q2 — the dissociation (the headline)

leg Q established **legible ⟺ KY-integrable** (8/8). But "integrable" and "regular/non-chaotic" are *not the
same thing*, and MN q=0.5-outer is the metric that separates them: it has **no exact Killing tensor**
(leg O; §99) so it is non-integrable and **illegible** (tabula §144, held-out 0.60 = 2×10¹⁶× the Kerr
floor) — yet its orbits sit on **intact KAM tori** (leg J: box-dim 1.06→1.15 converged; frequency-drift
0.0000). Feeding those same orbits to tabula's *dynamical* regime detector returns **EMIT-regular**. So:

> **On one exact GR metric, tabula's legibility probe and its regime detector give opposite verdicts** —
> illegible/non-integrable vs regular — and both are *correct*, because integrability (an exact invariant
> exists) and predictability (the motion is non-chaotic) are independent axes.

This is exactly tabula's EXP-7 finding (Lorenz & Rule 30 are law-learnable yet unpredictable) — here shown
on Manko–Novikov, and cross-validated against the bridge's *symbolic* (leg O) and *dynamical* (leg J)
ground truth simultaneously. The two-repo agreement isn't a single number matching; it's two independent
tabula instruments dissociating in exactly the way the bridge's two independent instruments do.

## C3 — a scope boundary, not a chaos detection (diagnosed, pre-registered as possible)

We pre-registered C3 → `CERTIFY-CHAOS`; it returned `EMIT-regular`. This is **not** a false verdict on a
valid input — it is a representation boundary, fully diagnosed (`dihole_scattering_diagnostic.json`):

- The di-hole's chaos is **scattering chaos**: chaotic orbits are *unbounded* — they bounce chaotically then
  **escape** (recorded X-coordinate runs off to |X| ~ 10¹¹–10¹⁶; Lyapunov 0.15–1.53 confirms they *are*
  chaotic). A scan found **8 di-hole ICs bounded for ≥800 steps — and 0 of them chaotic** (K < 0.5): in this
  system, *bounded ⟺ regular, chaotic ⟺ escaping*.
- The 0-1 test requires a **bounded stationary observable** (it was validated on Lorenz, a *bounded*
  attractor). The raw escaping X-coordinate isn't one — the monotone run-off dominates, so the test reads
  the *signal it is given* as non-chaotic. Correct for the observable; not capturing the system.

So the miss localizes precisely, as the pre-registration anticipated: **a trajectory-ensemble 0-1 test can't
represent GR chaos that is either unbounded (di-hole → escapes) or thin+stiff (MN inner orbit_B → a 126-point
section, below the test's 800-sample floor *and* not an ensemble).** The **bridge's frequency-drift detector
reached exactly that bounded thin GR chaos** (orbit_B, drift 0.980; leg J 2026-06-26d) — so the instruments
are **complementary**: tabula's 0-1 test excels on bounded well-sampled dynamics and correctly reads the GR
*regular* cases; the bridge's section-based frequency-drift detector reaches the bounded thin chaos the
trajectory test structurally cannot.

## What this establishes

- **A third independent instrument confirms the bridge's regular-vs-integrable distinction on GR data.**
  tabula's dynamical detector reads MN q=0.5-outer as regular, agreeing with box-dim and frequency-drift —
  and *dissociating* from tabula's own legibility verdict exactly as the theory (and the bridge's ground
  truth) demands.
- **The legible⟺integrable correlation (leg Q) is sharpened, not contradicted:** legibility tracks the
  *exact invariant* (integrability), which is a strictly finer property than dynamical regularity. MN
  q=0.5-outer is the witness that they differ.
- **Instrument domains are mapped honestly:** the 0-1-test-on-trajectories and the frequency-drift-on-sections
  cover different, complementary regions of GR phase space; neither subsumes the other.

## Honest limits

- **Chaos leg is a miss, reported as such.** C3 did not yield a positive GR-chaos detection; it yielded a
  diagnosed scope boundary. The only *positive* cross-instrument chaos agreement remains bridge↔ansatz
  (§105, frequency-drift reproduced to the digit) — tabula's 0-1 test did not add one, for structural
  (representation) reasons, not because GR chaos is absent.
- **v1 representation error, logged:** the first attempt fed Poincaré *sections* to a *trajectory* detector →
  all UNKNOWN. Corrected to raw-trajectory ensembles before any verdict was scored (PREREGISTRATION
  amendment).
- **20 orbits/class, single coordinate, one (E,L) family per class** — a clean demonstration, not a
  large-N statistical study.

## Artifacts

- `code/generate_trajectories.py` — raw geodesic trajectory ensembles (Kerr / MN q=0.5 / di-hole), ansatz
  venv. `results/blind_trajectories.json`.
- `code/run_frontier_ensembles.py` — tabula's `detect_robust` (script 150) blind on the ensembles, tabula
  venv. `results/frontier_ensembles.json`.
- `code/score_ensembles.py` — unblinding vs the frozen ground truth. `results/score_ensembles.json`.
- `code/generate_series.py`, `run_frontier_detector.py`, `score_verdicts.py` — the v1 (section) pipeline,
  kept for the transparent representation-fix record. `results/frontier_verdicts.json` (all UNKNOWN).
- `results/dihole_scattering_diagnostic.json` — the C3 mechanism (scattering chaos escapes the 0-1 test's
  bounded-observable domain).
