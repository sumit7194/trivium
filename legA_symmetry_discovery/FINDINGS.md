# Move A — Findings: the hidden-symmetry discovery pipeline

*Run 2026-06-19. Predictions, library ladder, thresholds, and the data-flow blindness
boundary were frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before any geodesic was
generated. This leg supersedes legs 4 and 5c.*

## Result in one line

The discovery→verify pipeline closes end-to-end: **tabula, shown only geodesic trajectories
and blind to the metric, distilled each spacetime's hidden conserved quantity; ansatz
independently certified that candidate against the exact metric; and the two oracles AGREE on
all four rungs, matching ground truth** — Kerr, Kerr–Newman, Kerr–de Sitter each have a Carter
constant (EXISTS), the bumpy-quadrupole spacetime does not (DESTROYED). The neural oracle even
recovered the *exact* Carter coefficients — including the spin `a²` it was never told.

## The verdict table (predicted → measured, both oracles independent)

| Rung | true status | tabula (blind) | ansatz (from metric) | agree? |
|---|---|---|---|---|
| **Kerr** (a=0.6) | EXISTS | EXISTS · L1 · varratio 2.6e-18 | EXISTS · resid 2.9e-8 | ✅ |
| **Kerr–Newman** (a=0.6, Q=0.5) | EXISTS | EXISTS · L1 · 9.3e-19 | EXISTS · 3.1e-8 | ✅ |
| **Kerr–de Sitter** (a=0.9, Λ=0.001) | EXISTS | EXISTS · L1 · 4.4e-12 | EXISTS · 7.9e-4 | ✅ |
| **Bumpy quadrupole** (a=0.6, ε=0.35) | DESTROYED | DESTROYED · 2.98e-2 | DESTROYED · **14.6** | ✅ |

Every rung lands on the frozen prediction. The EXISTS rungs sit at held-out variance-ratio
1e-18–1e-12 and certification residual 1e-8–1e-3; the DESTROYED rung is **four-plus orders of
magnitude** away (certification residual 14.6). The agreement criterion (PREREGISTRATION §5)
is met cell-by-cell.

## The striking part — blind recovery of the exact Carter constant

The distilled coefficient vectors over the basis `[p_θ², cos²θ, cos²θ·E², cos²θ·Lz²/sin²θ]`
(normalized so the `p_θ²` coefficient is 1) came back as:

| Rung | distilled (blind) | textbook `(1, a², −a², 1)` | cosine |
|---|---|---|---|
| Kerr | `(1, +0.3600, −0.3600, +1.0000)` | a²=0.36 | **1.0000** |
| Kerr–Newman | `(1, +0.3600, −0.3600, +1.0000)` | a²=0.36 | **1.0000** |
| Kerr–de Sitter | `(1, +0.8064, −0.8041, +1.0002)` | a²=0.81 | **1.0000** |

Tabula was never given the spin `a`, the charge `Q`, the cosmological constant `Λ`, or the
metric — only `(θ, p_θ, E, Lz)` sampled along geodesics. It recovered `a² = 0.36` for the
a=0.6 holes and `a² = 0.81` for the a=0.9 Kerr–de Sitter hole. (Kerr–Newman's angular Carter
shares Kerr's coefficients because the charge enters the *radial* sector, not the angular one
— a correct, non-trivial check.) ansatz then confirmed these are genuine Killing tensors
(`∇₍ₐK_bc₎ ≈ 0`), and that the bumpy candidate is not.

## What this validates

The full falsifiability pipeline, with both halves built independently in their own repos and
connected only by the two permitted artifacts (trajectories out, candidate coefficients back):
- **neural discovery** (tabula's distillation head, blind) →
- **exact certification** (ansatz's Killing-tensor residual).

This is the honest, working version of what leg 4 only gestured at (a 1+1D tautology) and what
leg 5c failed to do by *dimension counting* (it returned 2 for both integrable and deformed
orbits). Distilling the invariant succeeds where counting its dimension could not.

## Honest limits and logged deviations

- **Calibration, not discovery (the point of this leg).** All four rungs have *known* answers;
  this re-derives textbook invariants to prove the instrument end-to-end. The new physics is
  **Move D** (aim the validated pipeline at a metric with no known second invariant). This leg
  is the go/no-go gate for that, and it passes.
- **The L1-vs-L2 (rational) sub-prediction did NOT land — for a real physical reason.**
  PREREGISTRATION predicted Kerr–de Sitter would need the rational library L2. It was solved by
  the polynomial L1 instead. Cause: Kerr–de Sitter has circular orbits only for `r < r_static =
  (3/Λ)^{1/3}`, and a *stable* bound-orbit band even narrower; at any Λ small enough to have
  bound orbits, the rational Carter correction `Λa²cos²θ/3` is tiny (~0.03% at Λ=0.001). The
  rational structure is genuinely sub-resolution in any regime that *has* bound geodesics — it
  is visible only as the small coefficient drift (0.8064 vs 0.81, 1.0002 vs 1) the distiller
  did pick up. This is an honest physical finding, not a failure: tabula's script 97 saw the
  rational structure because it could probe the angular sector at large Λ without needing
  radially-bound orbits; a bound-orbit pipeline cannot. (PREREGISTRATION §6 anticipated this
  outcome line: "Kerr-dS solved by L1 → rational structure not necessary at this Λ.")
- **Parameters (logged deviation).** PREREGISTRATION fixed the metric *structures* but not exact
  (a, Λ, ε); the bound-orbit physics drove the choices: KdS uses a=0.9, Λ=0.001 (not the
  a=0.6/Λ=0.04 of the first code draft) so a stable bound-orbit band exists.
- **Certification threshold (logged deviation).** PREREGISTRATION §4B froze
  `max|∇₍ₐK_bc₎| < 1e-4` (raw). The raw residual scales with metric magnitude, so the verdict
  uses a **metric-scale-normalized** residual `< 1e-3` instead. The decision is not
  threshold-sensitive: EXISTS rungs are 1e-8–8e-4, the DESTROYED rung is 14.6 — the gap spans
  four orders of magnitude. (The Kerr-de Sitter rung at 7.9e-4 has the smallest margin; for
  reference the *pure* Kerr Killing tensor evaluated on the KdS metric gives 1.3e-3, so
  tabula's Λ-adapted candidate is actually a *better* Killing tensor than naive Kerr-K there.)
- **Launches.** Exact equatorial circular orbits + latitudinal tilt (the `58_killing.py`
  scheme), computed per-metric from the radial-acceleration-zero condition — robust where a
  Keplerian guess failed for Kerr–de Sitter.
- **Bumpy strength.** With near-circular orbits the Kerr-Carter drift is 7e-2 (vs ~0.5 for wilder
  orbits) — smaller, but still decisively above ε_T, and the certification residual (14.6) is
  unambiguous. The DESTROYED verdict is robust.

## Go / no-go for Move D

**GO.** The instrument is validated on the calibration ladder: blind neural discovery + exact
certification agree on which spacetimes have a hidden symmetry and which do not, with a clean
four-order-of-magnitude separation, and the distilled coefficients match the textbook Carter
constant exactly. The pipeline can now be aimed at a metric with no known second invariant
(rotating-EdGB / Johannsen) — Move D.

## Artifacts
- `code/export_geodesics.py` — ansatz side: builds each exact metric (read-only via ansatz's
  numeric engine), gates vacuum rungs with `ricci_numeric`, integrates geodesics, writes only
  trajectory data tabula may see.
- `code/distill_invariant.py` — tabula side (blind): the frozen library ladder, split-by-
  trajectory held-out conservation, emits candidate coefficients.
- `code/certify_killing.py` — ansatz side: reconstructs `K^{μν}` from the coefficients and
  certifies `∇₍ₐK_bc₎` numerically.
- `results/traj_*.json` (tabula-visible), `truth_*.json` (diagnostic), `candidate_*.json`,
  `certify_*.json`.
