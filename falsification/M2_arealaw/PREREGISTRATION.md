# M2 — Pre-registration: the S = A/4 coefficient is regulator-dependent (where the "1/4" hides)

*Frozen 2026-07-23, before `code/m2_arealaw.py` is written or run (scheme κ-values below were scouted in a
scratchpad to fix the frozen thresholds honestly; the production script re-derives them under the gates).
Falsification-Ledger item M2 (Tier M, moonshot — but the expected KILL is the clean demonstration).
Depends on **V2 PASSED** (the entropy instrument is calibrated to c=1; float64 cleared).*

## The postulate under attack (Ledger M2)

> **"The Srednicki area-law coefficient is independent of regulator scheme"** (lattice vs momentum cutoff
> vs smearing).

The entanglement entropy of a ball of radius R for a 3D free scalar obeys an **area law**
S ≈ κ (R/a)² (Srednicki 1993, κ ≈ 0.295 for his lattice). M2 claims the coefficient κ is regulator-
independent. It is not — κ is UV-sensitive, the famous reason the "1/4" in S = A/4 is not something a
cutoff calculation pins down. **Expected KILL.** The payout is the sharpest home-built statement of *exactly
where* the non-universality lives: the **coefficient κ varies with the regulator; the area-law exponent
(= 2) does not.**

## Method (frozen — Srednicki radial decomposition, on the V2-calibrated instrument)

A 3D scalar decomposes into spherical harmonics; each angular momentum ℓ is an independent 1D radial chain,
and the ball entropy is **S(n) = Σ_ℓ (2ℓ+1) S_ℓ(n)**, n = R/a. Each S_ℓ is the covariance-matrix
entanglement entropy V2 validated: ground-state covariances X = ½K_ℓ^{−1/2}, P = ½K_ℓ^{1/2} for the
ℓ-sector radial operator K_ℓ; trace out sites j > n; symplectic eigenvalues ν_k of the reduced (X,P) block;
S_ℓ(n) = Σ_k s(ν_k), s(ν) = (ν+½)ln(ν+½) − (ν−½)ln(ν−½).

- **Radial lattice:** N = 200 sites (N ≫ n so the exterior represents "the rest of space").
- **The ℓ-sum converges slowly** (tail (2ℓ+1)S_ℓ ~ ℓ^{−q}, q ≈ 2.5–3): sum explicitly to **L₀ = 500**, then
  add a **power-law tail** — fit (2ℓ+1)S_ℓ = A ℓ^{−q} on [L₀/2, L₀] and add ∫_{L₀}^∞ = A(L₀+½)^{1−q}/(q−1).
  (Under-summing ℓ is *the* pitfall here — a naive L₀ ≈ n gives κ off by 2×.)
- **Radius window:** n ∈ {15, 20, 25, 30, 35, 40}. Extract κ, c from the fit **S(n) = κ n² + c** (the
  constant absorbs the leading subleading term); area-law **exponent p** from the log–log slope of S vs n.
- **Precision:** float64 (V2c showed float64 = mpmath to 5e-9 for these shallow ball spectra — no leg-X wall).

## The three regulators (all: same continuum free scalar, ω²→k² as k→0; differ only in the UV)

- **R1 — bare nearest-neighbour lattice (Srednicki):** K_ℓ from the first-difference radial gradient,
  r_j = j. The standard sharp lattice cutoff. *Anchor:* κ must reproduce Srednicki ≈ 0.295.
- **R2 — improved (Symanzik) stencil:** the radial gradient at the 4th-order accurate 4-point stencil —
  removes the leading O(a²) lattice artifact from the dispersion. A different lattice regulator.
- **R3 — higher-derivative smooth regulator:** K_ℓ → K_ℓ + γ K_ℓ², γ = 0.1 — an analytic UV stiffening
  (Pauli–Villars-like). In a Gaussian theory a smooth cutoff is realised as a modified dispersion, so this
  is the rigorous form of the "cutoff-shape" axis. (Literal boundary-smearing is *not* used: in a free
  theory it has no clean entanglement-entropy definition — stated honestly in advance.)

## Frozen gates

- **M2a — the anchor.** R1 reproduces Srednicki: **κ_R1 ∈ [0.28, 0.32]** and exponent **p_R1 ∈ [1.90, 2.05]**.
  If this fails, the radial machinery is wrong and M2b/M2c are void.
- **M2b — the KILL (primary).** The three regulators give **resolvably different coefficients**:
  **spread ≡ (κ_max − κ_min)/κ_mean > 0.20**, and the ordering is stable under the robustness variations
  (L₀, n-window, N) below. → **KILLED** (coefficient regulator-dependent). → **SURVIVES** if all three κ
  agree within extraction jitter (spread < 0.05). → **UNDECIDED** in between.
- **M2c — the universality canary (the other half of the payout).** Every regulator has area-law exponent
  **p ∈ [1.90, 2.05]** — the R² scaling is regulator-invariant even as κ moves. This is the "the *law* is
  universal, the *coefficient* is not" statement made quantitative.
- **M2d — the coordinate control.** The **midpoint discretization** (r_j = j−½: the *same* regulator R1 in
  different lattice coordinates) leaves the coefficient invariant: **|κ_mid − κ_R1|/κ_R1 < 0.05**. This
  proves the M2b spread is regulator physics, not a coordinate/fitting artifact — a coordinate change does
  *not* move κ, a genuine regulator change does.
- **M2e — extraction-robustness (bug-catcher, not a verdict).** κ for each regulator is reported for
  L₀ ∈ {400, 500}, n-window {full, drop-smallest-n}, and N ∈ {150, 200}; the κ *ordering* R1 < R2 < R3 must
  be stable and each κ stable to a few %. A flip under these variations voids the kill.

## Honest limits (fixed in advance)

- Toy model only — free scalar on a radial lattice; labeled as such. Says nothing about the *actual* S = A/4
  of a black hole (which needs the full gravitational path integral). This isolates a *lattice fact*: the
  entanglement area-law coefficient is a regulator-dependent number.
- Expected KILL (Tier M framing: the obstruction/demonstration is the payout, not a surprise). The value is
  a clean, calibrated, home-built separation of the universal (exponent) from the scheme-dependent (κ).
- The three regulators are three UV completions of one IR theory; "same theory" means identical
  low-k dispersion, verified by ω²→k² and by the shared area-law exponent.

## Anchors (read-only)

Srednicki 1993 (hep-th/9303048, "Entropy and Area", κ ≈ 0.295) · Bombelli–Koul–Lee–Sorkin 1986 · calibrated
by [V2](../V2_cft_calibration); reuses the leg X / K1 / V2 covariance-entropy machinery. Interpreter:
conjecture_machine `.venv` (numpy 2.4.6, mpmath 1.3.0 for the V2c-style precision spot-check only).
