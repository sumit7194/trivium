# Move G — Findings: adversarial falsification of the main claims

*Run 2026-06-19/20. A deliberate attempt to BREAK our own results — negative controls and
break-attempts designed so an artifact would show up as a signal, reported outcome-neutral.*

## Result in one line

The main claims **survived** genuine break-attempts — including the headline ("a black hole is a
2-number object": the counter is calibrated, not biased toward 2) — and **three** tests changed or
qualified the claims rather than rubber-stamping them, the signature of real falsification: Move F's
"curvature" → **metric divergence**; the synthesis's edge is **fundamental but coordinate-dependent
in severity**; and the spine's count is **calibrated but only ±1 accurate on curved manifolds**, so
the vacuum-BH counts (Kerr, Schwarzschild) are threshold-fragile while the charged-BH counts are robust.

## The scorecard

| test | claim attacked | result | verdict |
|---|---|---|---|
| **1 hallucination** | Move A: blind Carter recovery | noise → DESTROYED (0.99), shuffle → DESTROYED (0.21), scramble → DESTROYED (1.00); real Kerr → EXISTS (2.6e-18) | **SURVIVED** |
| **2 generalization** | Move A: recovers a², not a fixed answer | recovered a² tracks true a² at spins 0.1–0.9, correlation **1.0000**, **0.0%** error | **SURVIVED** |
| **B consistency** | Move B: QNM agreement is real | measured Q → χ=0.818, measured Mω_R → χ=0.816 (agree to **0.003**, both inside the measured CI) | **SURVIVED** |
| **3 mechanism** | Move F: bulk/edge needs curvature | hemisphere 0.45× (null), unbounded-flat 0.78× (null), **flat-diverging 4.50× (FIRES)** | **SURVIVED → SHARPENED** |
| **4 fundamental?** | synthesis: exact owns the edge | edge from intrinsic radius = 1.89× (vs 3.81× in bad coords) — stays hard but milder | **SURVIVED, qualified** |
| **5 the spine** | "a black hole is a 2-number object" | counter tracks true dim (corr 0.98), noise→8 (not 2), exact on flat manifolds; but +1 curvature inflation → vacuum-BH counts ±1 threshold-fragile | **SURVIVED, qualified** |
| **6 Move D** | three-boundary integrability hierarchy | methods give different verdicts at same ε (KAM band real); SALI validated on a chaotic control; chaos boundary located at ε≈1.0 | **SURVIVED, strengthened** |

## What survived, and why the tests were genuine

- **Move A does not hallucinate (Test 1).** Given the flexible 3-library ladder and a held-out
  split, an overfitting method *would* have found a low-variance "invariant" in shuffled/noisy data.
  It did not — every negative control returned DESTROYED with var-ratio 0.2–1.0, three+ orders of
  magnitude above the EXISTS bar, while real Kerr returned 2.6e-18. The discovery is real.
- **Move A measures the actual spin (Test 2).** Recovered a² equals true a² to 0.0% across five
  spins the distiller never "expected" — it is reading the physics, not echoing a fixed basis.
- **Move B is a two-observable consistency, not a one-number fit (Test B).** Q and Mω_R are
  independent; they pin the *same* spin to 0.003. A tuned/coincidental agreement would have implied
  two different spins. (The Schwarzschild baseline, 40–50% off, is the built-in null.)

## What the tests CHANGED (the honest part)

- **Move F: "curvature" → metric DIVERGENCE (Test 3 sharpened the claim).** The break-attempt 3c —
  a *flat* space (Euclidean coordinates) given a distance that diverges at a fake boundary
  (`d = −log(1−r)`) — **fired at 4.50×**, even harder than the hyperbolic disk (3.81×). Meanwhile a
  *curved* space without divergence (the hemisphere) stayed null (0.45×). So curvature is **not**
  the driver and is not even necessary: the bulk/edge effect is driven by the **distance/metric
  diverging**, full stop. This further corrects Move F (which corrected Move E): the precise
  statement is *"learned recovery fails where the metric diverges"* — exactly a black-hole horizon,
  with curvature incidental.
- **The synthesis: the edge is fundamental but its severity is coordinate-dependent (Test 4).**
  Recovering the hyperbolic distance from the *intrinsic* radius still shows an edge penalty
  (1.89×), so the failure is not a pure artifact of the Euclidean observation coordinates — the
  divergence amplifies noise irreducibly. But it is **2× milder** than in the embedding coordinates
  (3.81×), so the *magnitude* of "exact owns the edge" depends on the representation. Honest
  statement: the edge is fundamentally hard (it survives the natural coordinate), and poor
  observation coordinates make it worse.

## Test 5 — THE SPINE: is the "2-number black hole" counter calibrated, or biased toward 2?

The headline of the whole project. The dangerous failure mode: tabula's bottleneck counter returns
~2 regardless of the truth, so the agreement with ansatz is an artifact. Two attacks:

**5a Calibration (synthetic manifolds of known dimension + a noise null).** Fed the EXACT leg-1
instrument (cap lifted from d≤4 to d≤8) smooth nonlinear manifolds of intrinsic dimension 1–6 and a
pure-noise control:

| true dim | 1 | 2 | 3 | 4 | 5 | 6 | noise (K=12) |
|---|---|---|---|---|---|---|---|
| counted | 2 | 3 | 4 | 5 | 5 | 6 | **8** |

Correlation(counted, true) = **0.98**; noise → 8 (not 2). **The "biased toward 2" hypothesis is
REJECTED** — the counter tracks dimension and reports noise as high-dimensional.

**5b The +1 is curvature inflation, not bias (flat-vs-curved control).** The calibration showed a
systematic **+1 overcount at low dim**. A control isolates the cause — a *linear* (flat) embedding vs
a *nonlinear* (curved) one of the same latent dimension:

| true dim | linear (flat) | nonlinear (curved) |
|---|---|---|
| 2 | **2** | 3 |
| 3 | **3** | 4 |
| 4 | **4** | 5 |

Flat manifolds count **exactly**; curved manifolds overcount by **+1**. So the imprecision is the
**leg-7b curvature-inflation effect** (a curved low-dim manifold needs an extra bottleneck dimension
to unfold) — a property of the manifold's geometry, not a counter flaw.

**5c Threshold robustness of the REAL black-hole counts.** Re-applying the knee rule to the saved
real R²(d) curves at τ ∈ {1,2,3,5}%:

| family | τ=1% | τ=2% (frozen) | τ=3% | τ=5% | ansatz |
|---|---|---|---|---|---|
| Schwarzschild | 2 | **1** | 1 | 1 | 1 |
| RN | 2 | **2** | 2 | 2 | 2 |
| dyonic (observable) | 2 | **2** | 2 | 2 | 3→2 (Q²+P² degeneracy) |
| Kerr | 3 | **2** | 2 | 2 | 2 |
| KN-full | 3 | **3** | 3 | 3 | 3 |
| KN-Δ-symmetric | 2 | **2** | 2 | 2 | 2 |

The **charged** cases (RN, KN) are threshold-robust; the **vacuum** cases (Schwarzschild, Kerr) are
**±1 fragile** — correct at the frozen 2% rule but overcounting by 1 at a stricter 1% threshold,
because their observable manifolds are more curved (5b).

**Spine verdict — SURVIVED, with an honest qualification.** The counter is genuinely calibrated (not
a 2-collapse): the strong falsification fails. But it is accurate only to **±1** on curved manifolds,
so "Kerr = 2" holds *at the frozen 2% rule* yet sits one notch above the curvature-inflation
threshold (a 1% rule would say 3); the charged-BH counts are robust. The "2-number black hole" stands
as a registered result, with the vacuum-case margins now known to be thin and tied to the leg-7b
curvature effect.

## Test 6 — MOVE D: is the three-boundary hierarchy real, and is "no chaos" meaningful?

**6a Hierarchy distinctness.** The skeptic's worry: the three "boundaries" are one ε-signal read at
three arbitrary thresholds. Direct test — do the methods give *different verdicts at the same ε*? At
ε=0.02–0.05 the answer is yes: **exact = BROKEN, approximate = intact, chaos = none** (three
different verdicts). The three verdict-regimes are
`intact/intact/regular → BROKEN/intact/regular → BROKEN/BROKEN/regular`. The middle regime is the KAM
band — the exact Killing tensor is gone yet the orbit is still conserved to 0.4% (a measured number,
threshold-independent). So the methods measure **distinct things**; the hierarchy is **real as an
ordering**. *Honest caveat:* the exact residual and approximate var-ratio are both monotonic in ε, so
the specific boundary *values* are threshold/scale-dependent — the *ordering* is the robust result.
*(A first statistic, midpoint-of-range, flagged SUSPECT; it was the wrong tool — it conflated the
exact residual's step-at-0 with its later rise. Recorded for honesty.)*

**6b Is SALI valid, and does the bump reach chaos? (the genuine break-attempt).** A positive control
— a φ-dependent (non-axisymmetric) bump that removes L_z conservation — **made SALI fire** (min-SALI
0.024 at ε=0.35), so SALI genuinely detects chaos; "no chaos" is not a dead instrument. The real
axisymmetric bump stays regular at ε=0.35 and 0.6 (confirming Move D) and reaches its first chaotic
orbits at **ε≈1.0** (min-SALI < 0.1, median still high — a mixed phase space, KAM-typical). So Move D's
"chaos boundary > 0.35, not reached" is **confirmed and now LOCATED at ε≈1.0** — far above the exact
(0⁺) and approximate (0.07) boundaries.

**Move D verdict — SURVIVED and STRENGTHENED.** The hierarchy is a real ordering of distinct phenomena
(exact 0⁺ < approximate 0.07 < chaos ≈1.0), SALI is validated, and the chaos boundary the original leg
could only bound is now located. The only correction is the honest caveat that the *values* (not the
ordering) are threshold-dependent.

## Scope — what was NOT stress-tested here (no false sense of completeness)

This battery hit the spine and most extension claims: the spine counter (calibration + threshold),
Move A (two ways), Move B, Move D (hierarchy + chaos), Move F, and the synthesis. It did **not**
separately re-attack Moves C and E — but both were *already* reported as **mixed results that did not
fully pass their own pre-registered criteria** (C: invariant recovered in the bulk but not the Petrov
edge; E: directional support but frozen thresholds missed), so they are self-bounded rather than
unexamined. "Survived" means "survived these specific attacks," not "proven."

## Net read

The discovery→verify pipeline (A) and the ringdown bridge (B) are robust to genuine attack. The
edges synthesis is robust but **sharper and more qualified than stated**: the bulk/edge effect is a
*metric-divergence* phenomenon (not curvature), fundamental in existence and coordinate-dependent in
degree. The corrections have been propagated to THE_BRIDGE §10.

## Artifacts
- `code/falsify_moveA.py` (Test 1), `code/export_multispin.py` + `code/falsify_moveA_test2.py`
  (Test 2), `code/falsify_moveB.py` (Test B), `code/falsify_moveF.py` (Tests 3, 4).
- `results/falsify_*.json`, `results/traj_spin_*.json`.
