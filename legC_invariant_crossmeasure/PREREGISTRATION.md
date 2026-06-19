# Move C — Pre-registration: the coordinate-free invariant cross-measure

*Frozen 2026-06-19, before any probe is trained. Discipline: THE_BRIDGE.md §2, §4A, §10.2 Move C.
Uses ansatz's new coordinate-free oracles (§57 `petrov`, §76 `invariant_fingerprint`).*

## The question

> Ansatz computes **coordinate-free** curvature invariants (Weyl I/J, Kretschmann) and the
> Petrov algebraic type — exact, frame-independent. A net that learns from observation sees the
> **tidal field** (geodesic deviation `E_ij = R_{0i0j}`), which is **frame-dependent**. Does a
> blind representation of the frame-randomized tidal field **recover ansatz's exact coordinate-
> free invariant and Petrov class** — and (the legibility lens, leg 2) is that invariant
> *linearly legible* from the raw observation, or only *nonlinearly present*?

## 1. The two sides (both read-only / exact)

**ansatz (exact, coordinate-free labels).** For each metric: the Kretschmann scalar `K` and the
Weyl invariant (from `invariant_fingerprint`, §76, symbolic), and the Petrov type (§57). These
are the frame-independent ground truth.

**observations (frame-dependent, what a net sees).** The electric tidal tensor
`E_ij = R_{0i0j}` (geodesic-deviation / tidal-force tensor) in a static orthonormal frame,
computed numerically from the exact metric, then **rotated by a random SO(3) frame** at every
sample so no coordinate frame is shared. The net sees only the 6 independent components of the
symmetric 3×3 `E_ij`. Gate: the construction must reproduce Schwarzschild `E = (M/r³)·diag(−2,1,1)`
and de Sitter `E ∝ Λ·δ_ij` (isotropic).

## 2. The metrics (ansatz-labelled)

- **Petrov-O (conformally flat, Weyl = 0):** Minkowski (E=0), de Sitter (E isotropic ∝ Λ, several Λ).
- **Petrov-D (Weyl ≠ 0, the algebraically-special black-hole structure):** Schwarzschild (several M),
  Reissner–Nordström (several M, Q). Their Weyl tidal field is traceless with the `(−2,1,1)` ratio.

O is the conformally-flat / "no Weyl" class; D is the black-hole / "Weyl" class. The
coordinate-free distinction is whether the traceless-anisotropic (Weyl) part of the tidal tensor
is non-zero — which the net must detect rotation-invariantly.

## 3. The probe ladder (tabula-style, from leg 2)

On the frame-randomized `E_ij` (6 components), recover ansatz's exact labels:
- **linear** probe (ridge / logistic) — legibility;
- **nonlinear** probe (kNN / small MLP) — information presence;
- **invariant-feature** reference — a probe on the rotation-invariants `tr(E²), tr(E³)` (the
  coordinate-free content a good representation should distil), as the achievable ceiling.

Split is **by metric instance** (no shared metric across train/test) — the anti-leakage rule.

## 4. Predictions (frozen)

- **P1 (magnitude recovery).** The nonlinear probe recovers ansatz's exact Weyl/Kretschmann
  invariant from the frame-randomized tidal field with held-out **R² > 0.9**; the invariant-
  feature reference does too (it is the ceiling).
- **P2 (legibility gap — the leg-2 lens).** The invariant is **present but not linearly legible**
  from the raw frame-randomized components: linear R² is **far below** nonlinear R² (the random
  frame scrambles the linear readout, since `tr(E²)` is quadratic in the components). Scramble
  gap = nonlinear − linear **> 0.3**.
- **P3 (Petrov class).** A blind nonlinear probe classifies O vs D (conformally-flat vs
  black-hole tidal field) at **accuracy > 0.95**, matching ansatz's exact Petrov labels.
- **P4 (cross-measure agreement).** The net's recovered invariant ordering matches ansatz's exact
  ordering across instances: **Spearman ρ > 0.9**.

## 5. Agreement criterion (frozen)

The leg **succeeds** iff P1, P3, P4 hold (the learned representation recovers the coordinate-free
invariant and class that ansatz computes exactly) and P2 holds (the legibility lens: the invariant
is nonlinearly present but not linearly legible from raw frame-dependent observations).
Disagreements are findings (e.g. if linear *is* legible, the random frame did not scramble as
expected — investigate).

## 6. Honest scope (per §7)

- **O vs D** is the clean two-class test; richer types (I, N) need a non-spherical vacuum metric
  (e.g. Zipoy–Voorhees γ-metric) and are an extension, not the headline.
- **Static observers / electric tidal tensor.** The magnetic Weyl (frame-dragging) is set aside
  by using static, diagonal metrics; the tidal tensor is the observable proxy for the Weyl/Riemann.
- **No new physics.** Tidal fields, Petrov classification, and curvature invariants are textbook;
  the contribution is showing the *inductive* representation recovers the *deductive* coordinate-
  free invariant, framed through the project's own legibility lens.

## 7. Deliverables

- `code/tidal_observations.py` (ansatz venv) — numeric tidal tensor `E_ij` from each exact metric
  (Schwarzschild/de Sitter gated), frame-randomized; ansatz exact `K`/Weyl/Petrov labels.
- `code/probe_invariants.py` (tabula venv) — the linear/nonlinear/invariant-feature probe ladder.
- `code/plot_crossmeasure.py` — the legibility-gap + recovery figure.
- `FINDINGS.md` — the recovery/legibility table, verdicts, honest limits.
