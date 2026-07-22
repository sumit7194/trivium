# V2 — Pre-registration: the entropy instrument reproduces c = 1 (CFT calibration)

*Frozen 2026-07-23, before `code/v2_cft.py` is written or run. Falsification-Ledger item V2 (Tier V,
validation), run now as the **calibration gate for M2**: the covariance-matrix entanglement-entropy
instrument (leg X / K1 machinery) must reproduce a known exact CFT result before it is trusted for the 3D
area-law coefficient in M2. If V2 fails, we have a bug, not a discovery.*

## The postulate (Ledger V2)

> **"The 1+1 massless free-scalar chain's interval entanglement entropy runs as (c/3) ln L with c = 1."**

A single interval in a 1+1 CFT has entanglement entropy (Calabrese–Cardy; Casini–Huerta lattice form on a
periodic ring of N sites):

    S(L) = (c/3) · ln[ (N/π) · sin(πL/N) ] + const ,   c = 1 for the free boson.

The two endpoints of the interval each contribute c/6 · ln; the chord length (N/π)sin(πL/N) is the
finite-size conformal factor. Recovering **c = 1** validates the instrument.

## Setup (frozen)

- Periodic harmonic chain, N = 500 sites, K_ii = 2 + μ², K_{i,i±1} = −1 (periodic wrap), **μ = 1e-4** (a
  near-critical IR regulator for the massless zero mode; correlation length ξ = 1/μ = 1e4 ≫ all fitted L, so
  the chain is effectively critical over the fit window and the entropy has not saturated).
- Vacuum covariances X = ½K^{−1/2}, P = ½K^{1/2} (float64: no exponentially deep modular spectrum here, so
  double precision suffices — checked in V2c below, unlike leg X's wedge).
- Interval A = L contiguous sites centred in the ring; reduced blocks X_A, P_A; symplectic eigenvalues
  ν_k = √(eig(X_A P_A)); entropy S(L) = Σ_k s(ν_k), s(ν) = (ν+½)ln(ν+½) − (ν−½)ln(ν−½).
- **L sweep:** L ∈ {20, 30, 40, …, 200} (well inside N/2 and ≪ ξ).

## Frozen gates

- **V2a — the central charge (primary).** Least-squares fit of S(L) vs x ≡ ln[(N/π)sin(πL/N)] over the L
  sweep has slope m; **c = 3m ∈ [0.95, 1.05]**. → PASS validates the instrument; FAIL ⇒ instrument bug.
- **V2b — logarithmic form (fit quality).** The fit is genuinely logarithmic, not a power law masquerading:
  **R² > 0.999** for S vs x. (A gapped control μ = 0.5 must instead SATURATE — S(L) flat at large L,
  slope → 0 — confirming the log is a criticality signature, not an artifact.)
- **V2c — precision canary.** Recomputing the largest-L entropy in mpmath (dps = 40) agrees with float64 to
  **< 1e-6 relative**. Confirms double precision is adequate for this instrument (documents that M2 may use
  float64 for its per-l-sector eigendecompositions — no leg-X-style precision wall for ball entropies).

## Honest limits (fixed in advance)

- Validation postulate, expected to SURVIVE (Tier V). Its value is instrument hardening, not discovery.
- Lattice ring with a small mass regulator; the fit window is chosen so neither UV (small L) nor IR
  (saturation) contaminates the log — standard Casini–Huerta practice, stated so the window is not a free
  knob tuned to the answer.

## Anchors (read-only)

Calabrese–Cardy 2004 (entanglement entropy, 1+1 CFT) · Casini–Huerta 2009 (lattice entanglement entropy) ·
reuses the leg X / K1 covariance-entropy machinery. Interpreter: conjecture_machine `.venv` (numpy 2.4.6,
mpmath 1.3.0).
