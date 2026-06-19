# Move D — Pre-registration: the integrability boundary of a deformed black hole

*Frozen 2026-06-19, before any deformation is swept. Discipline: THE_BRIDGE.md §2 and §10.2
Move D. Built on the pipeline validated in [Move A](../legA_symmetry_discovery/FINDINGS.md).*

## Why this target (and why NOT rotating EdGB)

The §10.2 Move-D menu named rotating-EdGB. Recon of ansatz's EdGB track (`scripts/19–22`,
`docs/EDGB.md`) shows it is **slow-rotation, O(a)** — frame-dragging `g_tφ` on a spherically
symmetric static EdGB background. A spherically symmetric metric *trivially* conserves total
angular momentum `L²` (the a=0 Carter constant), and to O(a) that survives, so the Carter
question there is trivially EXISTS — not a frontier test. Presenting it as one would overclaim.

The genuinely-open, tractable question instead: **a generic quadrupole deformation of Kerr
breaks the exact Carter constant, but KAM theory says an *approximate* invariant persists for
small deformations. Where is the boundary — and do tabula (data-driven) and ansatz
(metric-based), plus an independent chaos indicator, agree on it?** The boundary location for
this family is not textbook; computing it by three independent routes that concur is the result.

## 1. The question

> As Kerr is deformed by a quadrupole bump of strength ε, the exact quadratic Killing tensor
> is destroyed for any ε>0; an *approximate* (KAM) hidden symmetry persists until some ε*.
> Do the two bridge oracles — tabula's blind distillation (held-out conservation) and ansatz's
> Killing-tensor residual — agree on ε*, and does it coincide with the onset of chaos (SALI)?

## 2. The deformed family (frozen)

The same bump as Move A's `bumpy` rung, swept: Kerr (M=1, a=0.6) with
`g_tt → g_tt·(1 + ε·cos²θ·R0/r)`, `R0=6`, over
`ε ∈ {0.00, 0.02, 0.05, 0.08, 0.12, 0.18, 0.25, 0.35}`. ε=0 is exact Kerr (= Move A's Kerr
rung, a built-in sanity anchor); ε=0.35 is Move A's `bumpy` (already DESTROYED). The boundary
ε* lies in between.

## 3. Three independent measurements per ε (frozen)

All read the SAME blind geodesic trajectories (ansatz emits, only trajectories cross — the
Move A boundary). For each ε:
- **tabula (blind):** the Move A distiller's held-out (split-by-trajectory) variance-ratio of
  the best low-degree invariant. Lower = more conserved.
- **ansatz (metric):** the Move A certifier's metric-scale-normalized Killing-tensor residual
  of tabula's reconstructed candidate. Lower = closer to a true Killing tensor.
- **chaos indicator (independent):** SALI (Smaller ALignment Index) of the geodesic flow —
  evolve two deviation vectors, track their alignment; SALI→0 ⇒ chaotic, O(1) ⇒ regular. This
  is the method tabula's own script 95 used as its cross-check, computed here on the bridge side.

## 4. Predictions (frozen)

- **P1 (anchor).** At ε=0 both oracles say EXISTS (tabula varratio < ε_T=1e-2, ansatz
  norm-resid < 1e-3) and SALI is regular — reproducing Move A's Kerr rung.
- **P2 (monotone).** tabula varratio(ε) and ansatz resid(ε) both increase monotonically with ε.
- **P3 (agreement — the headline).** The boundary ε* where tabula crosses ε_T and where ansatz
  crosses its threshold coincide **within one sweep step**. A larger gap is a finding.
- **P4 (gradual, KAM).** The transition is gradual, not a step: there is a range of ε where the
  invariant is approximately but not exactly conserved (varratio measurably above the ε=0 floor
  yet below ε_T) — the KAM regime — before it crosses. And the SALI chaos onset coincides with
  the symmetry-loss boundary (regular below ε*, chaotic above).

## 5. Agreement criterion (frozen)

The leg **succeeds** iff (a) P1 holds, (b) tabula's and ansatz's boundary ε* agree within one
sweep step (P3), and (c) the chaos onset (SALI) is on the same side of ε* as predicted (P4).
Disagreements (e.g. tabula sees approximate conservation where SALI already shows chaos) are
findings about what each method actually measures, not bugs.

## 6. What outcomes mean (decided before running)

- **All three boundaries coincide** → a triangulated integrability boundary: representation
  (tabula), exact geometry (ansatz), and dynamics (SALI) concur on where Kerr's hidden symmetry
  dies under deformation. The strongest outcome.
- **tabula's boundary > SALI's** → tabula's approximate invariant persists into the weakly-chaotic
  regime (KAM islands the distiller still fits) — a real, interpretable gap, not an error.
- **ansatz resid grows from ε=0 with no plateau** → confirms the exact Killing tensor dies
  immediately (any ε>0), with only the *approximate* invariant (tabula/SALI) showing a finite ε*.
- **Non-monotone** → numerical/sampling artifact; investigate (measurement-vs-engine, §7).

## 7. Independence safeguards (§2)

Same data-flow blindness as Move A: ansatz emits only trajectories; tabula distills blind; ansatz
certifies the candidate; SALI is computed from the metric independently of tabula. The family, ε
grid, three measurements, thresholds, and predictions above are frozen by this commit.

## 8. Deliverables

- `code/export_sweep.py` (ansatz venv) — sweeps ε, emits `results/traj_eps*.json` + computes SALI.
- `code/distill_sweep.py` (tabula venv) — distills each ε blind → `results/candidate_eps*.json`.
- `code/certify_sweep.py` (ansatz venv) — certifies each ε → `results/certify_eps*.json`.
- `code/plot_boundary.py` — the three-curve boundary figure.
- `FINDINGS.md` — the boundary table, the three-way agreement, honest limits.
