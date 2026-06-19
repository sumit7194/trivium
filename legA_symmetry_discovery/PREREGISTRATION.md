# Move A — Pre-registration: the hidden-symmetry discovery pipeline

*Frozen 2026-06-19, before any geodesic is generated or any invariant distilled.*
*Discipline: THE_BRIDGE.md §2 (blind, pre-registered, never tune one to match the other,
disagreements are findings) and §10.2 Move A.*

This is the **inductive→deductive discovery pipeline**, and it **supersedes legs 4 and 5c**:
- Leg 4 (conjecture handoff) was a 1+1D special case with a tautological universality check.
- Leg 5c tried to fingerprint integrability by *counting* the bottleneck dimension and **failed**
  (it returned 2 for both integrable and deformed orbits).

Here tabula's new **distillation head** (SpaceTime scripts 95–97) *discovers the conserved
quantity itself* from trajectories, and ansatz *certifies it* from the metric. Both halves
were built independently in the two repos; this leg connects them under a frozen criterion.

---

## 1. The one question

> Can the inductive oracle (tabula) **discover** a spacetime's hidden conserved quantity from
> geodesic trajectories *alone* — blind to the metric — and can the deductive oracle (ansatz)
> **independently certify** that candidate from the metric, so that the two agree, case by
> case, on *which spacetimes have a hidden symmetry and which do not*?

The hidden symmetry in question is the **Carter constant** (a quadratic Killing tensor), the
conserved quantity beyond the manifest energy `E = −p_t` and azimuthal `L_z = p_φ`.

---

## 2. The calibration ladder (4 rungs, run in full)

All metrics in Boyer–Lindquist coordinates, geometric units `G = c = 1`, `M = 1`,
`Σ = r² + a²cos²θ`. The exact forms are frozen here; the precise SymPy implementation lives in
committed `code/` (additive bridge code that imports ansatz's tensor engine read-only).

| # | Rung | Defining structure | Carter constant — **true status** |
|---|---|---|---|
| 1 | **Kerr** `(M,a)` | `Δ = r² − 2r + a²`, standard Kerr | **EXISTS** (textbook quadratic Killing tensor) |
| 2 | **Kerr–Newman** `(M,a,Q)` | `Δ = r² − 2r + a² + Q²` | **EXISTS** (charge sits in `Δ_r`; separability preserved) |
| 3 | **Kerr–de Sitter** `(M,a,Λ)` | `Δ_r = (1−Λr²/3)(r²+a²) − 2r`, `Δ_θ = 1 + (Λ/3)a²cos²θ`, `Ξ = 1+Λa²/3` | **EXISTS but rational** in `cosθ` (the `Δ_θ` denominator) |
| 4 | **Bumpy quadrupole** `(M,a,ε)` | Kerr + an `O(ε)` quadrupole deformation introducing a non-Staeckel `r–θ` coupling (exact form pinned in `code/`, `ε` frozen at 0.35; reduces to Kerr at `ε=0`) | **DESTROYED** (no quadratic Killing tensor; Hamilton–Jacobi does not separate) |

Rung 3 is the sharp sub-test: its Carter constant is **rational** (needs the `1/Δ_θ` factor), so a
purely polynomial distillation library should *fail* there and the rational library should
*succeed* — exactly the structure tabula's script 97 found (polynomial only approximates,
Λ-aware rational is exact, cosine 0.9999).

---

## 3. The blindness boundary (data flow — the independence is mechanical, per §2)

Only two artifacts cross the bridge, and neither repo imports the other:

```
   ansatz (exact metric)                         tabula (neural distiller)
   ─────────────────────                         ────────────────────────
   build metric tensor                  ──►       reads ONLY trajectory .npz
   integrate geodesics            trajectory      finds conserved g(x,p) blind
   write trajectory arrays           .npz         emits candidate coefficient .json
                                                          │
   reconstruct K from coeffs     candidate          ◄─────┘
   certify: ∇₍ₐK_bc₎ < tol ?       .json
```

- **ansatz → tabula:** geodesic phase-space trajectories only — `{x^μ(τ), p_μ(τ)}` arrays for
  many initial conditions per rung, **plus** the per-trajectory manifest constants `E, L_z`
  (these are *not* the metric — they are the obvious `∂_t, ∂_φ` conserved quantities any
  trajectory analysis recovers; tabula could re-extract them as the constant `p_t, p_φ`). The
  metric, the parameter values `(a, Q, Λ, ε)`, and the word "Carter" are **never** sent.
- **tabula → ansatz:** the candidate invariant as a coefficient vector over a named basis
  library + the library id, so ansatz can reconstruct `K = Σ cᵢ φᵢ` (or `Σ cᵢ φᵢ/Δ_θ`) and test it.
- Enforced as in leg 1: ansatz writes `.npz`/reads `.json` in its venv; tabula reads `.npz`/writes
  `.json` in its venv; no shared imports.

**Anti-leakage (lesson from legs 5b/5c, frozen here):** the train/test split is **by
trajectory**, never by timestep — no two samples from the same geodesic may straddle the split.
The held-out conservation metric is evaluated on **entirely unseen trajectories**.

---

## 4. The two independent verdicts (frozen rules + thresholds)

Each oracle issues an **EXISTS / DESTROYED** verdict per rung, by its own rule, without seeing
the other's.

### 4A. tabula (blind, from trajectories)
- **Library ladder (frozen, parsimony order):**
  - `L1` — quadratic polynomial in `(p_θ, cosθ, sin⁻¹θ-coupled L_z, E)` (the Kerr-tuned basis of script 97/99).
  - `L2` — `L1` divided by `Δ_θ = 1 + λ cos²θ` (the rational / Λ-aware basis), `λ` a free fit scalar.
  - `L3` — quartic polynomial extension (fallback for richer structure).
- **Verdict:** **EXISTS** iff some library in the ladder yields a candidate whose **held-out
  (split-by-trajectory) within-trajectory variance-ratio** `< ε_T = 1e-2`; report the **lowest**
  such library (parsimony). If no library in `{L1,L2,L3}` reaches `< ε_T`, verdict = **DESTROYED**.
- **Bonus (calibration rungs only, not used in the verdict):** cosine of the fitted coefficient
  vector to the textbook Carter vector, expected `> 0.98` for rungs 1–3.

### 4B. ansatz (from the metric, certifying tabula's candidate)
- Reconstruct `K_μν` from tabula's coefficients + library id, against ansatz's exact metric.
- **Verdict:** **EXISTS** iff the **Killing-tensor residual** `max|∇₍ₐK_bc₎| < tol_A = 1e-4`
  over `N = 25` random phase-space sample points (`58_killing.py` / `killing_tensor_residual`
  pattern), and/or a Killing–Yano root reproduces it (`69_killing_yano.py`). Else **DESTROYED**.
- **Three-valued honesty:** if the residual is numerically near tol but symbolically
  inconclusive, report **UNPROVEN** (not a forced pass), per ansatz's own ethos.

Thresholds `ε_T = 1e-2`, `tol_A = 1e-4`, `N = 25` are frozen by this commit. (Justification from
existing runs: tabula held-out is ~`1e-28` for Kerr vs `~0.019` for bumpy — `1e-2` separates them
by orders of magnitude; ansatz Kerr residual is `< 1e-5`.)

---

## 5. Agreement criterion (frozen) + predicted table

**Agreement on a rung** ⇔ tabula's verdict == ansatz's verdict. A mismatch is a **finding**, not a
bug. The leg **passes** iff all four rungs agree *and* match the true status in §2.

| Rung | true status | tabula (predicted) | which library (predicted) | ansatz (predicted) |
|---|---|---|---|---|
| Kerr | EXISTS | EXISTS | **L1** | EXISTS |
| Kerr–Newman | EXISTS | EXISTS | **L1** | EXISTS |
| Kerr–de Sitter | EXISTS | EXISTS | **L2 (rational)** | EXISTS |
| Bumpy quadrupole | DESTROYED | DESTROYED | none reaches `ε_T` | DESTROYED |

**Headline sub-prediction:** Kerr-dS is solved by **L2 and not L1** — the rational structure is
*necessary*, reproducing script 97 by an independent (metric-certified) route.

---

## 6. What each outcome means (decided before running)

- **All four agree as predicted** → the discovery→verify pipeline is validated end-to-end on
  known answers; the instrument is trustworthy. **Proceed to Move D** (aim it at a metric with no
  known second invariant). This is the success path.
- **tabula EXISTS where ansatz DESTROYED** (e.g. tabula "finds" an invariant for bumpy) → either
  tabula overfit a flexible library to finite data (tighten parsimony / more held-out
  trajectories and rerun) **or** a genuine higher-order invariant ansatz's quadratic-tensor test
  missed (investigate; measurement-vs-engine check, §7).
- **tabula DESTROYED where ansatz EXISTS** (e.g. misses Kerr-dS Carter) → the pre-registered
  library ladder is too weak (a learnability diagnostic — but the ladder is frozen, so this is a
  real result about distillability, not a license to add libraries post-hoc).
- **Kerr-dS solved by L1 (polynomial)** → the rational structure was not actually necessary at
  this `Λ`; re-examine whether `Λ` is large enough to matter (engine-vs-measurement).
- **ansatz returns UNPROVEN** on a rung → reported as such; the pipeline's certification is
  honestly three-valued.

---

## 7. Independence safeguards (§2)

- tabula never sees the metric, the parameters `(a,Q,Λ,ε)`, or the target name — only trajectory
  arrays + manifest `E, L_z`.
- ansatz never sees tabula's training; it only certifies the final candidate against its own exact
  metric.
- The ladder, thresholds, library set, split-by-trajectory rule, and predicted table above are
  **frozen by this commit**. Any post-hoc change is logged as a deviation in `JOURNAL.md` with the
  original preserved (per the leg-1 precedent).
- Neither oracle's threshold is tuned to make a verdict land.

---

## 8. Deliverables

- `code/export_geodesics.py` — **ansatz venv**: builds each rung's exact metric (read-only use of
  ansatz's tensor engine; Kerr/KN via `kerr_delta_metric`, Kerr-dS and bumpy via additive bridge
  construction), integrates split-by-trajectory geodesics, writes `results/traj_<rung>.npz`
  (trajectories + `E, L_z` only).
- `code/distill_invariant.py` — **tabula venv**: reads only `traj_<rung>.npz`, runs the frozen
  library ladder, writes `results/candidate_<rung>.json` (coefficients + library id + held-out
  varratio + bonus cosine).
- `code/certify_killing.py` — **ansatz venv**: reads only `candidate_<rung>.json`, reconstructs
  `K`, computes the Killing-tensor / Killing–Yano residual, writes `results/certify_<rung>.json`.
- `results/` — the per-rung artifacts + the assembled §5 verdict table.
- `FINDINGS.md` — the filled table, the headline sub-prediction outcome, honest limits, and the
  go/no-go for Move D.
