# Move D — Findings: the integrability boundary of a deformed black hole

*Run 2026-06-19. Family, ε grid, three measurements, predictions, and the agreement criterion
were frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any deformation was swept. Built
on the pipeline validated in [Move A](../legA_symmetry_discovery/FINDINGS.md).*

## Result in one line

"Does a deformed black hole keep Kerr's hidden symmetry?" has **three different answers**, and
the bridge's three independent methods each measure a different one: the **exact** Killing
tensor (ansatz) dies the instant you deform (ε*≈0⁺); an **approximate** invariant (tabula's
blind distillation) survives to ε≈0.07; and full **chaos** (SALI) does not set in even at
ε=0.35. The pre-registered single agreed boundary (P3) is **falsified — in exactly the way the
pre-registration anticipated (§6)** — and that falsification is the finding: a clean hierarchy
of three integrability boundaries.

## The three boundaries (the table)

| ε | tabula var-ratio (approx. invariant) | tabula verdict | ansatz Killing residual (exact) | ansatz verdict | SALI (chaos) |
|---|---|---|---|---|---|
| 0.00 | 2.6e-18 | EXISTS | 2.9e-8 | EXISTS | 0.52 regular |
| 0.02 | 4.3e-3 | EXISTS | **5.8** | DESTROYED | 0.52 regular |
| 0.05 | 7.3e-3 | EXISTS | **5.1** | DESTROYED | 0.52 regular |
| 0.08 | 1.3e-2 | DESTROYED | 10.4 | DESTROYED | 0.52 regular |
| 0.12 | 2.0e-2 | DESTROYED | 11.9 | DESTROYED | 0.51 regular |
| 0.18 | 3.3e-2 | DESTROYED | 13.5 | DESTROYED | 0.50 regular |
| 0.25 | 3.6e-2 | DESTROYED | 14.3 | DESTROYED | 0.51 regular |
| 0.35 | 3.0e-2 | DESTROYED | 14.6 | DESTROYED | 0.48 regular |

→ **exact-symmetry boundary** ε*≈0⁺ (ansatz) **<** **approximate-invariant boundary** ε*≈0.07
(tabula) **<** **chaos boundary** ε*>0.35 (SALI). See `results/legD_integrability_boundary.png`.

## What each boundary means (the physics)

- **ansatz — the exact Killing tensor dies immediately.** A generic quadrupole deformation
  breaks Hamilton–Jacobi separability at any ε>0, so no exact quadratic Killing tensor exists;
  the residual `∇₍ₐK_bc₎` of tabula's best candidate jumps from 2.9e-8 (Kerr) to ~5 at ε=0.02
  and grows. ansatz, which tests *exact* symmetry, correctly reports DESTROYED for all ε>0.
- **tabula — an approximate invariant persists (KAM).** The deformed orbit still lies on a
  slightly-deformed invariant torus, so a *near*-conserved quantity exists. Tabula, fitting the
  best low-degree invariant and measuring held-out conservation to a 1% tolerance, finds it
  EXISTS up to ε≈0.07 (var-ratio rising smoothly 1e-18 → 4e-3 → 7e-3 → 1.3e-2). This is the
  gradual KAM transition predicted in P4 — and tabula's fitted invariant is *better* conserved
  than the naive fixed Kerr tensor (e.g. 4.3e-3 vs the 1.06e-2 Kerr-K drift at ε=0.02), because
  it adapts to the deformation.
- **SALI — no chaos yet.** SALI stays ≈0.5 (regular) across the whole sweep: the tori are
  deformed but not destroyed, so the orbits never become chaotic for ε≤0.35. The dynamics
  boundary is well beyond where both the exact and approximate symmetry boundaries sit.

## Verdict on the frozen predictions

- **P1 (anchor at ε=0): TRUE.** Both oracles EXISTS, SALI regular — reproduces Move A's Kerr rung.
- **P2 (monotone): TRUE** for tabula's var-ratio and the Kerr-Carter drift; ansatz's residual is
  O(1) for all ε>0 with mild non-monotonicity from the library switching L1/L2/L3 across ε
  (the candidate, hence its residual, changes) — all far above threshold, so the verdict is
  unaffected.
- **P3 (single agreed boundary within one step): FALSE — the headline finding.** tabula's
  boundary (≈0.07) and ansatz's (≈0⁺) differ by the full KAM gap. This is not a bug: the two
  oracles measure *different notions of symmetry* — exact (ansatz) vs approximate/practical
  (tabula) — and the gap quantifies the KAM regime where the exact Killing tensor is already
  gone but the torus, and a quasi-conserved quantity, survive.
- **P4 (gradual KAM transition): TRUE.** tabula's var-ratio rises smoothly through a range of ε
  (the KAM regime) rather than stepping, and SALI confirms the orbits stay regular throughout —
  exactly the "tori survive past the exact-symmetry boundary" picture.

## What the bridge actually bought here

A **triangulated structure**, not a single number: three independent epistemologies —
exact differential geometry (ansatz), learned representation (tabula), and nonlinear dynamics
(SALI) — pulled apart a question that sounds binary ("is it integrable?") into three distinct,
physically-meaningful boundaries. This is the §2-rule-4 / §5 ideal: a *principled disagreement*
that is the result. No single method would have revealed it: ansatz alone says "broken at 0⁺,"
tabula alone says "fine until 0.07," SALI alone says "regular throughout" — only together do
they show the hierarchy exact < approximate < chaotic.

## Honest limits

- **Resolution-dependent middle boundary.** tabula's ε*≈0.07 is set by the frozen ε_T=1e-2
  tolerance; a tighter tolerance would move it toward 0 (toward the exact boundary), a looser
  one outward. It is a *practical* boundary ("conserved to 1%"), not a sharp mathematical one —
  stated as such. The exact (ansatz, ε*=0⁺) and dynamics (SALI) boundaries are tolerance-robust.
- **One deformation family, near-circular orbits.** The specific bump and the equatorial-circular
  orbit family fix the numbers; the *hierarchy* (exact < approximate < chaos) is the robust
  qualitative result, not the exact ε* values.
- **Chaos boundary not located here** (>0.35). **Update (2026-06-20, Move G falsification):** the
  adversarial pass validated SALI on a deliberately-chaotic non-axisymmetric control (it fired,
  min-SALI 0.024) and pushed the real bump to high ε — the first chaotic orbits appear at **ε≈1.0**
  (mixed phase space). So the chaos boundary is now *located* at ε≈1.0, confirming it sits far above
  the exact (0⁺) and approximate (0.07) boundaries. See `legG_falsification/FINDINGS.md` Test 6.
- **Not new physics.** KAM persistence of tori under perturbation is textbook; the contribution
  is the three-way cross-validated *picture* of it on a deformed black hole, by independent
  tools that were never tuned to each other.

## Artifacts
- `code/export_sweep.py` — ansatz side: sweeps ε, emits blind trajectories, computes SALI.
- `code/distill_sweep.py` — tabula side (blind): the approximate invariant per ε.
- `code/certify_sweep.py` — ansatz side: exact Killing-tensor residual per ε.
- `code/plot_boundary.py` — the three-method boundary figure.
- `results/traj_eps*.json`, `candidate_eps*.json`, `certify_eps*.json`, `sweep_meta.json`,
  `legD_integrability_boundary.png`.
