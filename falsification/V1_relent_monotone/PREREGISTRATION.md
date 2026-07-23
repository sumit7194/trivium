# V1 — Pre-registration: relative entropy is monotone under region inclusion (the ultimate canary)

*Frozen 2026-07-23, before `code/v1_monotone.py` is written or run. Ledger item V1 (Tier V — validation,
expected to SURVIVE). This is the **canary for the entire leg-X / K1 / K3 stack**: monotonicity of relative
entropy is a theorem, so if our machinery violates it we have a bug, not a discovery.*

## The postulate (Ledger V1)

> **"Relative entropy is monotone under region inclusion on our chain"** (proven in QFT).

For nested regions **A ⊆ B**, restricting a state to the smaller algebra cannot increase distinguishability:

    S_rel(ρ_A ‖ σ_A)  ≤  S_rel(ρ_B ‖ σ_B) .

This is monotonicity of relative entropy under the restriction (a CPTP map) — Uhlmann's theorem, the same
inequality that underwrites the Bekenstein bound and Casini's entropic arguments. It is **not** in question
physically; the question is whether **our instrument respects it**.

## Why it matters here (the canary role)

K1's kill, K3's entropy-production curve, and leg X's hinge identity are all built on the same Gaussian
modular machinery: reduced covariances → symplectic spectra → modular form G → S_rel = Δ⟨K⟩ − ΔS. A monotone
violation would invalidate all three. K3 already observed monotonicity in one configuration in passing; V1
tests it deliberately, across **multiple excitation types and multiple nesting families**, so the canary is
genuinely exercised rather than assumed.

## Setup (frozen — inherits K1)

- Chain N = 96, μ = 0.5, entangling cut x_c = 48.5, region A = sites 49…96; mpmath **dps = 60**.
- **Excitation types (3):** (i) **coherent** displacement packet inside the wedge (leg X's baseline, ΔS = 0);
  (ii) **squeezed straddling** the cut (K1's kill geometry, ΔS ≠ 0); (iii) **squeezed inside** the wedge
  (K1's local-unitary case, ΔS = 0).
- **Nesting families (2):** (F1) slabs growing **outward from the cut**, A_ℓ = first ℓ sites of the wedge;
  (F2) slabs growing **inward from the far end**, B_m = last m sites of the wedge. F1 is the physically
  natural nesting; F2 is an independent chain of inclusions that must obey the same inequality.
- Region sizes ℓ, m ∈ {1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 40, 47}.

## Frozen gates

- **V1a — monotonicity (primary).** For every excitation type and every nesting family, S_rel is
  **non-decreasing** along the inclusion chain: S_rel(ℓᵢ) ≥ S_rel(ℓᵢ₋₁) − **1e-12** (the tolerance is pure
  numerical slack, not physics). → **SURVIVES** if satisfied everywhere. → **KILLED (= BUG)** on any decrease
  exceeding the tolerance; in that case the run **stops and is flagged for review**, since a genuine violation
  of Uhlmann monotonicity would mean the machinery — not nature — is wrong.

- **V1b — positivity.** S_rel ≥ 0 everywhere (Klein's inequality), for all types and sizes. A negative value
  is likewise a bug signature.

- **V1c — the anchor.** For the coherent excitation at the full wedge, S_rel must reproduce leg X's measured
  value **54.03** to < 1% — tying the canary to the already-cross-gated leg-X result (which quantum's blind
  twin independently confirmed).

- **V1d — saturation (observation, not a pass/fail).** S_rel should rise while the region grows into the
  excitation's support and then **plateau**, since a region containing the whole excitation already
  distinguishes it maximally. Reported as the shape of the monotone curve.

## Honest limits (fixed in advance)

- Validation postulate, expected to survive; the value is instrument hardening, not discovery. A "SURVIVES"
  here is worth exactly one thing: the K1/K3/leg-X stack does not violate a theorem it must obey.
- Toy model (harmonic chain, Gaussian states), as everywhere in this arc.
- Monotonicity is tested along **inclusion chains**, which is what the theorem constrains — not between
  arbitrary unrelated regions, where no inequality is implied.

## Anchors (read-only)

Uhlmann 1977 (monotonicity of relative entropy) · Lindblad 1975 · Casini 2008 (relative entropy and the
Bekenstein bound) · [leg X](../../legX_entropic_hinge) · reuses [K1](../K1_squeezed) `k1_squeezed.py`.
Interpreter: conjecture_machine `.venv` (mpmath 1.3.0).
