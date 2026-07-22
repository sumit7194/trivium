# V2 — Findings: the entropy instrument reproduces c = 1 (CFT calibration)

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item V2
(Tier V, validation), run as the calibration gate for [M2](../M2_arealaw). **Verdict: SURVIVES** — the
covariance-matrix entanglement-entropy instrument reproduces the exact 1+1 CFT result, so M2 may trust it in
3D.*

## Result in one line

A single interval on a near-critical 1+1 harmonic ring (N=500, μ=1e-4) has entanglement entropy
S(L) = (c/3) ln[(N/π)sin(πL/N)] + const with **c = 0.977** (R² = 1.000000) — the free-boson central charge
c = 1 to within the expected lattice finite-size effect; a gapped control (μ=0.5) instead **saturates**
(pseudo-c = 0.000), and float64 agrees with mpmath to **5×10⁻⁹**.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **V2a** (primary) | c = 3·slope of S vs ln[(N/π)sin(πL/N)] | **c = 0.9766** (want [0.95,1.05]) | **PASS** |
| **V2b** | logarithmic form, R² | **1.000000** (want >0.999) | **PASS** |
| V2b control | gapped μ=0.5 chain saturates | ΔS(20→200) = 0.000, pseudo-c = 0.000 | **PASS** (log is a criticality signature) |
| **V2c** | float64 vs mpmath (dps=30) entropy | rel **5.2×10⁻⁹** (want <1e-6) | **PASS** — float64 adequate for M2 |

## Why this matters for M2

M2 computes the 3D area-law coefficient by Srednicki's radial decomposition — a sum over angular-momentum
sectors of exactly this kind of 1D covariance-entropy calculation. V2 shows the instrument returns the right
number on a case with an exact analytic answer (c = 1), and that **float64 is precise enough** (no leg-X-style
modular precision wall for interval/ball entropies — the symplectic spectrum here is shallow). M2 may
therefore run its per-l-sector eigendecompositions in float64 for speed, with confidence.

The 2.3% shortfall of c below 1 is the standard lattice discretisation effect at finite L (the fitted window
is UV-affected at small L); it is inside the frozen tolerance and is not tuned. The point of V2 is
instrument validation, not a precision measurement of c.

## Honest limits

Validation postulate, expected to survive (Tier V) — its value is instrument hardening. Lattice ring with a
small-mass IR regulator; fit window chosen by standard Casini–Huerta practice (UV-safe small-L cut, IR-safe
L ≪ ξ), stated in advance so it is not a free knob.

## Inputs (read-only) & artifacts

Calabrese–Cardy 2004 · Casini–Huerta 2009 · reuses the leg X / K1 covariance-entropy machinery.
`code/v2_cft.py` · `results/v2_cft.json`. Interpreter: conjecture_machine `.venv` (numpy 2.4.6, mpmath 1.3.0).
