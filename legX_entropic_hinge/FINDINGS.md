# Leg X — Findings: the entropic hinge on a lattice — S_rel = 2π × boost energy, and the 2π measured

*Run 2026-07-10; gates X1/X2/X3 (+ observation O4) frozen in [PREREGISTRATION.md](PREREGISTRATION.md)
before the code was written. The computable core of the week's Dorau–Much result (PRL 2026,
arXiv:2510.24491 — the QFT upgrade of Jacobson's 1995 thermodynamic derivation of the Einstein equations):
for a **coherent excitation** of a free scalar, the relative entropy w.r.t. the vacuum on a Rindler wedge
equals **2π × the boost energy** of the classical wave (Bisognano–Wichmann; Longo 2019;
Casini–Grillo–Pontello 2019). The bridge tested the identity on a harmonic chain with exact Gaussian-state
methods — and measured the 2π itself from entropy data.*

## Result in one line

On a 96-site chain, the wedge relative entropy of a coherent wavepacket tracks 2π×boost-energy to **1.5%**
at every tested distance (X1 PASS); the **slope** of S_rel against packet distance — the offset-free
signature — recovers the **Bisognano–Wichmann constant 2π to 1.63%** (measured 6.1806 vs 6.2832; X2 PASS,
primary gate); a packet placed in the complement produces S_rel = **1.1×10⁻⁹** of baseline (X3 PASS,
placebo exact); and the same pipeline in ordinary double precision recovers only **11.5%** of the answer
(O4) — the boost weight lives exponentially deep in the modular spectrum, making this a
walls-are-instrument-relative instance where the wall is the **floating-point format**.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| X1 | identity at baseline (x₀=12): S_rel / 2πΣ(x−x_c)T₀₀ | **0.9848** (tol 8%) | **PASS** |
| X2 (primary) | slope of S_rel vs x₀ ÷ packet energy = 2π | **6.18058** vs 6.28319 → **1.63%** (tol 3%) | **PASS** |
| X3 | complement control (x₀=−10) | S_rel/baseline = **1.08×10⁻⁹** (tol 2%) | **PASS** |

The sweep (S_rel vs 2π·boostE): x₀=8: 36.02/36.58 · x₀=10: 45.03/45.72 · x₀=12: 54.03/54.86 ·
x₀=14: 63.00/64.01 — a uniform ≈1.5% deficit (lattice dispersion + the O(a/2) cut-position convention,
exactly why X2's slope was frozen as the primary gate; it cancels the offset and lands at 1.63%).

## O4 — the precision wall (the leg's second finding)

The modular weight of a mode at wedge depth x is ε ≈ 2πx, carried by symplectic eigenvalues at
ν−½ ~ e^(−2πx): reaching x≈20 requires resolving **10⁻⁵⁵** — float64 (ε capped ≈32, x≈5) recovers just
**11.5%** of S_rel. The production run used mpmath at dps=60 (ε_max 109.7, x-reach ≈17.5; 32/48 modes
beyond the 10⁻⁵⁰ floor dropped, their weight zeroed — visible as the slight 0.9843 dip at x₀=14, whose
tail crosses the reach). The Rindler wedge's entanglement structure is *arithmetic-precision-limited*: a
wall set by the number format, not the physics — the family's recurring theme, number-format edition.

## Why this is a bridge result

- It validates, numerically and with a placebo control, **the identity on which both papers hinge** —
  Jacobson 1995's δQ = TδS (the 2π *is* the Unruh temperature) and Dorau–Much 2026's relative-entropy
  version. "Measuring 2π from entanglement data" is the whole thermodynamic-gravity story in one number.
- It is the bridge's own, exact-method instrument (covariance-matrix Gaussian states — no field-theory
  approximation at any step; the lattice and the cut convention are the only approximations, and the
  primary gate is designed to cancel them).
- **quantum's blind twin is in flight** (round-6 Ask 2, relayed 2026-07-10): an independent implementation
  of the same check, deliberately without shared code. When it lands, the cross-implementation gate makes
  this a leg-S-pattern two-route result.

## Honest limits (frozen in advance)

- Validates the **hinge identity, not the derivations' conclusion** — getting the semiclassical Einstein
  equations additionally assumes S = A/4 (Dorau–Much say so themselves); nothing here touches the
  operator-algebraic (type III) machinery.
- One packet family (Gaussian, π_f = 0, σ=2.5), one mass (μ=0.5), Dirichlet chain — the 1.5% X1 offset is
  not decomposed further (dispersion vs cut convention), it is simply inside the frozen tolerance.
- Interpreter borrowed read-only from ansatz's venv (mpmath 1.3.0), precedented in leg J.

## Inputs (read-only) & artifacts

Dorau & Much arXiv:2510.24491 · Jacobson gr-qc/9504004 · Longo 2019 · Casini–Grillo–Pontello 2019 ·
Bisognano–Wichmann 1976. `code/entropic_hinge.py` · `results/entropic_hinge.json`.

---

## Update (2026-07-10) — quantum's blind twin landed: cross-gate CLOSED, and their adversarial test passed

quantum's independent implementation (no shared code; Williamson-then-functional-calculus route, dps=60)
verified the identity to **≤0.06% on clean geometries** (up to 0.21% where the packet grazes the far wedge
boundary — their residual anatomy, which also explains this leg's tolerance design), and shipped an
adversarial warning: an **arccoth ordering bug** in their first build passed every thermal self-test
silently and was caught only by a **squeezed-state** regression. The bridge answered with certification
gates (frozen in the ADDENDUM before `code/certification_tests.py` ran):

- **C1** squeezed discriminator through the *production* `modular_form`: A_q = εe^{−2r}, B_p = εe^{+2r}
  recovered to **4×10⁻⁶¹** — the ordering trap is absent in this construction. PASS.
- **C2** rotated two-mode: A_q = R diag(ε_k e^{−2r_k}) Rᵀ to **6×10⁻⁶²**. PASS.
- **C3** Fock-basis end-to-end (density matrices only, no Gaussian formulas): matches ½d²ε to
  **1.9×10⁻¹⁶**. PASS.
- **C4** the record: two independent implementations agree with Longo's formula on disjoint grids, and the
  **float64 wall was measured twice independently** — bridge 11.5% recovery (O4) vs quantum's 10–14% clip
  bands. The precision wall is now a two-instrument fact.

The leg-S-pattern cross-gate is closed: the entropic hinge identity holds by two blind implementations +
an exact-formula anchor, with a placebo control and a certified-adversarially machinery. `results/certification_tests.json`.

---

## Update (2026-07-10, round-6 close) — ansatz §115 landed: the derivation's full anatomy, on the family's ledger

ansatz machine-verified Jacobson 1995 (round-6 Ask D; `scripts/115_jacobson.py`, commit `5d97d5b`, 99/99
green, three-valued throughout). Combined with this leg and quantum's twin, the family now holds the
**complete anatomy of the thermodynamic derivation of the Einstein equations** — every link labeled:

| status | link | who / result |
|---|---|---|
| **PROVEN** | Raychaudhuri identity is pure geometry (leftover zero on the free static family AND free Kasner, where σ² = t^{−2p₁−2}(p₂−p₃)²/2 enters and cancels exactly — no field equations used); θ = d(lnA)/dλ; the bifurcation expansion → the δA integral | ansatz §115 (J1, J1c) |
| **PROVEN** | the hinge theorem: S(k,k)=0 ∀ null k ⟹ S = φ·g (null-cone parametrization, 10-unknown linear system, exactly 1-param solutions) + Bianchi/∇T=0 forcing φ = R/2 + Λ ⟹ **R_ab − ½R g_ab − Λg_ab = c·T_ab**, leftover zero | ansatz §115 (J3) |
| **MEASURED** | the 2π — the Unruh/Bisognano–Wichmann factor that *is* the temperature in δQ=TδS and the modular flow in S_rel = 2π×boost-energy | bridge (this leg, 1.63%) + quantum's blind twin (≤0.06%), cross-gated |
| **ASSUMED** | the localization postulate (integral equality for all local Rindler horizons ⟹ integrand equality) — logged by the machine as ASSUMED, not proven; **the one non-theorem in the chain, in 1995 and 2026 alike** | ansatz §115 (J2), honest |
| **ASSUMED** | S = A/4 (η = 1/4G input; the constants chain κ-cancellation → c = 8πG verified given it) | ansatz §115 (J2) + Dorau–Much's own statement |

Emergent gravity's derivation, decomposed across three repos: what is geometry (proven), what is quantum
information (measured, twice, blind), and what remains postulate (named). SymPy wall logged by ansatz as
usual (free-function families, not arbitrary two-argument metrics).
