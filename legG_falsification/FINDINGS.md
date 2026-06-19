# Move G — Findings: adversarial falsification of the main claims

*Run 2026-06-19/20. A deliberate attempt to BREAK our own results — negative controls and
break-attempts designed so an artifact would show up as a signal, reported outcome-neutral.*

## Result in one line

The main claims **survived** genuine break-attempts — and two of the tests **changed the claims**
rather than rubber-stamping them, which is the signature of real falsification rather than
confirmation theatre: Move F's "curvature" was corrected to **metric divergence** (a flat space
with a diverging distance fires; curvature is irrelevant), and the synthesis's edge effect is
**fundamental in existence but coordinate-dependent in severity**.

## The scorecard

| test | claim attacked | result | verdict |
|---|---|---|---|
| **1 hallucination** | Move A: blind Carter recovery | noise → DESTROYED (0.99), shuffle → DESTROYED (0.21), scramble → DESTROYED (1.00); real Kerr → EXISTS (2.6e-18) | **SURVIVED** |
| **2 generalization** | Move A: recovers a², not a fixed answer | recovered a² tracks true a² at spins 0.1–0.9, correlation **1.0000**, **0.0%** error | **SURVIVED** |
| **B consistency** | Move B: QNM agreement is real | measured Q → χ=0.818, measured Mω_R → χ=0.816 (agree to **0.003**, both inside the measured CI) | **SURVIVED** |
| **3 mechanism** | Move F: bulk/edge needs curvature | hemisphere 0.45× (null), unbounded-flat 0.78× (null), **flat-diverging 4.50× (FIRES)** | **SURVIVED → SHARPENED** |
| **4 fundamental?** | synthesis: exact owns the edge | edge from intrinsic radius = 1.89× (vs 3.81× in bad coords) — stays hard but milder | **SURVIVED, qualified** |

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

## Scope — what was NOT stress-tested here (no false sense of completeness)

This battery hit the strongest, most-falsifiable claims: Move A (two ways), Move B, Move F, and the
synthesis. It did **not** separately re-attack the spine (legs 1–3 — already audited; their counts
do vary correctly across families, e.g. 1/2/3 for Schwarzschild/RN/dyonic), nor Moves C, D, E
(already reported as mixed/qualified). A complete adversarial pass on those remains open. "Survived"
means "survived these specific attacks," not "proven."

## Net read

The discovery→verify pipeline (A) and the ringdown bridge (B) are robust to genuine attack. The
edges synthesis is robust but **sharper and more qualified than stated**: the bulk/edge effect is a
*metric-divergence* phenomenon (not curvature), fundamental in existence and coordinate-dependent in
degree. The corrections have been propagated to THE_BRIDGE §10.

## Artifacts
- `code/falsify_moveA.py` (Test 1), `code/export_multispin.py` + `code/falsify_moveA_test2.py`
  (Test 2), `code/falsify_moveB.py` (Test B), `code/falsify_moveF.py` (Tests 3, 4).
- `results/falsify_*.json`, `results/traj_spin_*.json`.
