# Leg 1 — Pre-registration: "how many numbers is a black hole?" (ansatz vs tabula)

*Frozen 2026-06-17, before any bridge code is written or any comparison made.*
*Discipline: THE_BRIDGE.md §2 (blind, pre-registered, never tune one to match the
other, disagreements are findings) and §8.1 (cheapest leg first).*

This is the **ansatz ↔ tabula leg of the spine** (§3, §4A): does tabula's neural
bottleneck-count of irreducible numbers, inferred from *observations only*, equal
ansatz's exact moduli count, computed from *the equations*? deepstrain's measured
δ is **not** part of this leg — it closes the triangle later (§3 step 3).

---

## 1. Scope decision (and why it is honest, not convenient)

The doc's headline phrasing is "Kerr = 2, Kerr–Newman = 3." But:

- ansatz emits **exact observables** (photon sphere, shadow `b_c`, ISCO, light
  bending, precession, redshift) **only for the static spherical lapse**
  `f(r)` — `conjecture_machine/scripts/45_observables.py`, `49`, `50`, `51`.
- ansatz can *discover and verify* Kerr (`44_discover_rotating.py`) but does
  **not** emit Kerr's observables today.
- The source repos are **read-only**. Adding rotating-observables physics to
  ansatz is forbidden by the workspace rules.

Therefore leg 1 uses the family ansatz **already serves exactly**: the static
charged family. Kerr is deferred to a later leg, reachable additively via *new
bridge code* that imports ansatz's engine read-only (not by editing ansatz).

The three families:

| Family | Static lapse `f(r)` | Generating params |
|---|---|---|
| **A — Schwarzschild** | `1 − 2M/r` | `M` |
| **B — Reissner–Nordström (RN)** | `1 − 2M/r + Q²/r²` | `M, Q` |
| **C — dyonic RN** | `1 − 2M/r + (Q²+P²)/r²` | `M, Q, P` |

Family C is included **on purpose**: ansatz's hair criterion
(`34_hair_criterion.py`) *proves* electric and magnetic charge enter `f`
identically as `Q²+P²`. So C is the pre-registered test of a principled
disagreement (see §4).

---

## 2. The two counting conventions (decided up front — §2 rule 2)

"How many numbers" is ambiguous until we fix whether the overall scale counts.
We register **both**, and predict both, so neither oracle can be nudged after the
fact.

- **Dimensionful count** `N_dim` — number of independent parameters of the
  generating family, *including the mass/length scale `M`*.
- **Observational-shape count** `N_shape` — number of independent **dimensionless**
  observables, i.e. with `M` scaled out (e.g. `b_c/M`, `r_isco/M`, bending angle).
  This is what survives if the absolute scale is not measurable.

### ansatz (ground-truth) predicted counts — read from the equations, blind to tabula

| Family | `N_dim` (algebraic moduli) | `N_shape` (dimensionless, observable) |
|---|---|---|
| A Schwarzschild | **1** (`M`) | **0** (all observables are fixed multiples of `M`) |
| B RN | **2** (`M, Q`) | **1** (`q = Q/M`) |
| C dyonic RN | **3** (`M, Q, P`) | **1** (`(Q²+P²)/M²`) — degenerate in one combination |

The C row is the crux: algebraic `N_dim = 3`, but the **observable** shape count is
**1**, because `Q` and `P` enter every observable only through `Q²+P²`.

---

## 3. The experiment (what each oracle does, blind)

### ansatz side — exact, from the equations
Compute the moduli count directly: for each family, the count is the number of free
constants in the lapse that survive ansatz's verifier (it already proves these —
`28_maxwell.py`, `32_no_hair.py`, `34_hair_criterion.py`). No fitting. This yields
the table in §2 by inspection of the proved lapse. The exact observable *values*
(`b_c`, `r_ph`, `r_isco`, bending) come from `45/49/50/51` and are used **only** to
generate tabula's input — never shown to tabula as labels, never as the metric.

### tabula side — neural, from observations only (blind)
Adapt tabula's in-context bottleneck-counting machinery
(`SpaceTime/curvature/scripts/12_incontext_counting.py`, `10_mdl.py`) so that,
**instead of its own world generator**, it consumes an observation dataset produced
by ansatz:

- Each **object** is one draw of the family parameters (protocol fixed in §3.1).
- Each object's **observation vector** is a set of ansatz's exact dimensionless
  observables (`b_c/M`, `r_ph/M`, `r_isco/M`, light-bending angle at fixed impact
  parameters, redshift at fixed radii). **Never the metric, never `M,Q,P` directly.**
- Sweep the bottleneck width `d`; locate the accuracy/MDL **knee**. The knee `d*`
  is tabula's inferred count.

Two readouts, matching §2:
- feed **dimensionful** observables (include an absolute-scale channel) → compare `d*` to `N_dim`;
- feed **dimensionless** observables only → compare `d*` to `N_shape`.

#### 3.0 Instrument clarification (recorded 2026-06-17, before any run, predictions unchanged)
Tabula's `12_incontext_counting.py` uses a DeepSets **set-encoder** because its
observations are *stochastic* draws of a latent form; the bottleneck-width knee then
reveals the dof. Our ansatz observables are **deterministic** functions of `(M,Q,P)`,
so faithfully reusing that exact task would require *inventing* nuisance noise — extra
researcher degrees of freedom we don't want. We therefore use tabula's other, more
direct bottleneck-counting instrument: a **bottleneck autoencoder** (the SciNet
bottleneck the whole `curvature/` project is built on, cf. `10_mdl.py` bits-per-body).
The count is the **intrinsic dimension of the observable manifold** — the smallest
bottleneck width `d` at which reconstruction saturates. "Accuracy" in the frozen knee
rule (§4) is read as held-out **R² = 1 − MSE/Var** (monotone non-decreasing in `d`),
so the rule applies verbatim. **All predicted counts and the agreement criterion are
unchanged.** This is a pre-run instrument choice, not a post-hoc deviation (no data
seen yet); the §4B set-encoder variant is left as an optional robustness follow-up.

To enforce blindness mechanically: ansatz (sympy venv) writes only the **observation
arrays** to `.npz`; the counting harness (torch venv) reads only those arrays — it
never imports ansatz, never sees the metric or `(M,Q,P)`.

#### 3.1 Generation protocol (frozen so "true count" is unambiguous)
- A: `M ~ U[1, 3]`.
- B: `M ~ U[1, 3]`, `q = Q/M ~ U[0, 0.9]`.
- C: `M ~ U[1, 3]`, `Q, P` drawn so `(Q²+P²)/M² ~ U[0, 0.81]` with the **angle**
  `atan2(P,Q) ~ U[0, 2π]` (the degenerate direction is sampled fully, so a net
  *could* in principle try to encode it — and should fail to, per the prediction).
- Per object: `k = 8` observation samples (matching tabula's `K_CTX`), each a vector
  of the observables above evaluated at fixed, pre-listed probe points.
- Train/knee protocol inherited from `12_incontext_counting.py` (DeepSets set-encoder,
  width sweep, held-out accuracy). Seeds and step counts recorded in results.

---

## 4. Predictions and agreement criterion (frozen)

**Knee-detection rule (frozen):** `d*` = the smallest bottleneck width `d` whose
held-out accuracy is within **2%** of the plateau accuracy (max over the sweep),
*and* where increasing `d` by 1 improves accuracy by **< 1%**. (Same rule for both
readouts; reported with a multi-seed band, ≥ 3 seeds.)

**Agreement criterion (frozen):** the two oracles **agree** on a family/convention
cell iff `d* == N` exactly (integer match). Off-by-one or larger is a **disagreement
= finding**, not a bug.

### Predicted outcome table

| Cell | ansatz `N` | tabula `d*` (predicted) | If it matches | If it disagrees |
|---|---|---|---|---|
| A, dimensionful | 1 | 1 | scale is the one number | net under/over-counts → learnability diagnostic |
| A, shape | 0 | 0 | Schwarzschild is shapeless | — |
| B, dimensionful | 2 | 2 | clean 2-number agreement | — |
| B, shape | 1 | 1 | `Q/M` is the one shape | — |
| **C, dimensionful** | **3** | **2** (predicted) | — | **pre-registered principled disagreement** |
| **C, shape** | **1** | **1** | — | — |

The **C-dimensionful** cell is the headline pre-registration: ansatz says 3 (it can
prove `P` is a real modulus), tabula should say **2**, because the third number is
**observationally invisible** (`Q²+P²` degeneracy). Per THE_BRIDGE.md §3 this is
the *good* "tabula < exact" outcome — "the net found compressibility the parameter
count misses (MDL < moduli dimension), a genuine information-theoretic finding."
Here we additionally know the **mechanism** (EM-duality degeneracy, proved by
ansatz `34`), which makes it a clean, explained finding rather than a mystery.

### What each global outcome would mean (decided before running)
- **A, B agree on both conventions** → clean ansatz↔tabula triangulation of black-hole
  dimensionality; the two oracles speak the same language. Proceed to close the
  triangle with deepstrain (§3 step 3).
- **C disagrees exactly as predicted (3 vs 2)** → the bridge's first real finding:
  the observational moduli count is strictly below the algebraic one, by a degeneracy
  we can name. Strengthens, not weakens, the result.
- **tabula > exact anywhere** → net wasting capacity / not converged → learnability
  diagnostic (rerun with more steps/seeds before concluding).
- **C agrees (tabula says 3)** → tabula found a way to read `P` from observations we
  didn't expect it to → re-examine whether the observable set secretly leaks `P`
  (measurement-vs-engine check, §7).

---

## 5. Independence safeguards (§2)

- tabula never sees the metric or `M,Q,P` — only ansatz-computed **observables**.
  This is the architectural blindness the doc says to lean on (§2 last line).
- The knee-detection rule, conventions, and predicted counts above are **frozen by
  this commit**; they will not be edited after seeing results. Any post-hoc change
  is logged as a deviation in `JOURNAL.md`, with the original prediction preserved.
- Neither oracle's threshold or sampling is tuned to make `d*` land on `N`.

## 6. Deliverables of this leg
- `code/` — additive bridge code: an ansatz-observable generator (imports
  `conjecture_machine` engine read-only) + a counting harness adapted from
  tabula's `12_incontext_counting.py` (original code preserved, changes commented).
- `results/` — the knee sweeps, multi-seed bands, and the filled §4 outcome table.
- A short findings note appended to `JOURNAL.md`.
