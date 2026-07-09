# Leg X — Pre-registration: the entropic hinge on a lattice (relative entropy = 2π × boost energy)

*Frozen 2026-07-10, before `code/entropic_hinge.py` is written or run. The computable core of the week's
Dorau–Much result (PRL 2026, arXiv:2510.24491 — the QFT upgrade of Jacobson 1995): via modular theory, the
relative entropy between the vacuum and a **coherent excitation** of a free scalar field, restricted to a
Rindler wedge, equals the **boost energy** of the classical wave (Bisognano–Wichmann; Longo 2019,
Casini–Grillo–Pontello 2019):*

    S_rel  =  2π ∫_{x>0} x · T₀₀[f](x) dx        (c = ħ = 1)

*The bridge tests this identity **numerically on a harmonic chain** — Gaussian-state methods, exact at the
level of covariance matrices, no field-theory approximations — and, as the sharpest gate, **measures the 2π**
(the Unruh/Bisognano–Wichmann constant) from entropy data alone. The quantum sister is independently
implementing the same check, blind (round-6 Ask 2); the cross-gate happens when both exist.*

## Setup (frozen)

- Chain: N = 96 sites, Dirichlet, H = ½Σp² + ½qᵀKq, K = (2+μ²)I − hopping, **μ = 0.5** (ξ = 2 sites).
- Region A = sites 49…96; the entangling cut sits at x_c = 48.5 (site units, 1-indexed).
- Coherent excitation: displacement of the vacuum by classical data (f, π_f=0),
  f_j = a·exp(−(j−j₀)²/(2σ²)), **σ = 2.5**, amplitude a = 1 (S_rel is exactly quadratic in a; value
  irrelevant). Baseline packet center **j₀ = 60.5** (x₀ ≡ j₀−x_c = 12); scaling sweep x₀ ∈ {8, 10, 12, 14}.
- Lattice T₀₀ (frozen convention): site term ½μ²f_j² at x_j; link term ½(f_{j+1}−f_j)² at x_{j+½}.
- Machinery: reduced covariances X_A = (½K^{−1/2})_AA, P_A = (½K^{1/2})_AA; symplectic spectrum ν_k from
  X_A^{1/2}P_A X_A^{1/2} = Wν²Wᵀ; modular quadratic form A_q = X_A^{−1/2} W diag(ν_k ε_k) Wᵀ X_A^{−1/2}
  with ε_k = ln((ν_k+½)/(ν_k−½)); then **S_rel = ½ f_Aᵀ A_q f_A** (same-covariance displaced Gaussians;
  ΔS = 0 for coherent states, so S_rel = Δ⟨K_mod⟩ exactly).
- **Precision (frozen, and itself a finding):** the boost weight 2πx lives in ν_k−½ ~ e^{−ε}; reaching
  x ≈ 20 needs ν−½ ~ e^{−2π·20} ≈ 10⁻⁵⁵ — **impossible in float64** (caps at ε≈32, i.e. x≈5). The
  computation therefore runs in **mpmath at dps = 60** (via ansatz's venv, read-only), with modes dropped
  below ν−½ < 10⁻⁵⁰ (count reported). A deliberate float64 run is included to *exhibit* the failure.

## Frozen gates

- **X1 — the identity (baseline packet, x₀ = 12).**
  |S_rel / (2π Σ (x−x_c)·T₀₀) − 1| < **8%** (tolerance covers lattice dispersion at σ=2.5 and the O(a/2)
  cut-position convention).
- **X2 — measure the 2π (primary gate; offset-free).** Over x₀ ∈ {8,10,12,14} (rigid integer shifts, so the
  packet's own energy E = ΣT₀₀ is constant), S_rel is linear in x₀ with slope 2πE. Gate: fitted
  slope/(E) = **2π within 3%**. This is the Unruh/Bisognano–Wichmann constant measured from entanglement
  data — the number that carries Jacobson's temperature and Dorau–Much's modular flow.
- **X3 — control (placebo).** The same packet placed in the **complement** (x₀ = −10, i.e. j₀ = 38.5):
  displacement outside A's algebra leaves the reduced state invariant ⇒ S_rel(A) must be
  < **2%** of baseline (Gaussian tails only).
- **O4 — the precision wall (observation, not gated).** The float64 pipeline at x₀ = 12 under-reports
  S_rel (modular spectrum truncated at ε≈32). Reported as a walls-are-instrument-relative instance: the
  boost weight is *arithmetic-precision-limited*, a wall set by the number format, not the physics.

## Honest framing (fixed in advance)

- This validates the **identity that the derivations hinge on** — not the derivations' conclusion. Deriving
  the semiclassical Einstein equations additionally assumes S = A/4 (Dorau–Much state this); no lattice
  computation touches the operator-algebraic (type III) structure.
- Lattice ≠ continuum: Dirichlet walls, dispersion at σ=2.5, half-site cut ambiguity — hence X2 (slope) is
  primary, X1 (absolute) secondary.
- Cross-implementation: quantum's blind twin (round-6 Ask 2) gates later; this leg stands alone.

## Anchors (read-only)

Dorau & Much, arXiv:2510.24491 (PRL 2026) · Jacobson, gr-qc/9504004 · Longo 2019 (entropy of coherent
states) · Casini–Grillo–Pontello 2019 · Bisognano–Wichmann 1976. Interpreter: ansatz `.venv` (mpmath 1.3.0).
