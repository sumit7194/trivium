# V12 findings: the bridge's independent reproduction of the TS δ=2 fractal-basin exponent α

*Sealed 2026-10-11, before ansatz's per-level α values were seen. Pre-registration: `PREREGISTRATION.md`, addenda
1–10. No human has checked this.*

## Primary result: REPRODUCED (3/3 pairs CONTRAST REPRODUCED)
K = 2000 x0 per system, nested ε ∈ {3e−3, 1e−3, 3e−4, 1e−4, 3e−5}, N = 300 section crossings, rtol 1e−11.
Numba DOP853 (validated against scipy, gates G3⁗ and addendum 10). Binomial-MLE α with a 1000-sample bootstrap CI.
Measured synthetic CI coverage: smooth 96%, fractal 93% (addendum 3).

| Level | System | L | Hits per ε (3e−3 … 3e−5) | α̂ (MLE) | 95% CI | α (WLS) |
|---|---|---|---|---|---|---|
| L1 | TS p = 4/5, E = 0.97 (retrograde) | +5.125 | 1040, 1007, 951, 908, 849 | **0.044** | [0.032, 0.055] | 0.044 |
| L1 | Kerr p = 4/5 (matched ε_sep) | +2.55380 | 404, 129, 40, 14, (6) | **1.008** | [0.906, 1.129] | 1.007 |
| L2 | TS p = 4/5, E = 0.97 (retrograde) | +5.875 | 827, 678, 641, 611, 579 | **0.075** | [0.060, 0.089] | 0.074 |
| L2 | Kerr p = 4/5 | +2.92753 | 408, 140, 43, 18, (6) | **0.955** | [0.861, 1.072] | 0.953 |
| L3 | TS p = 3/5, E = 0.95 (prograde) | −16/3 | 469, 327, 291, 254, 243 | **0.147** | [0.124, 0.170] | 0.146 |
| L3 | Kerr p = 3/5 | −2.58926 | 422, 147, 49, 18, (7) | **0.938** | [0.843, 1.049] | 0.937 |

(·) means an ε with fewer than 10 hits, excluded from the fit by the pre-registered rule.
- Every Kerr control is within [0.85, 1.15] with its CI containing 1.
- Every TS CI upper end is < 0.5 and disjoint from its Kerr partner's CI.
- 0 orbits excluded (no CAPPED or FORBIDDEN rows). Max |2H + 1| on survivors is ≤ 2.0e−10.

**Reading.**
- At matched relative distance from each system's own separatrix, Kerr's survive/plunge boundary is smooth
  (α ≈ 1: hits fall about 3× per half-decade of ε).
- TS δ=2's boundary is fractal and close to "flat": at L1, 42–52% of start points in the window stay uncertain as ε
  shrinks 100×.
- The contrast holds in both orbit senses: retrograde at p = 4/5, prograde at p = 3/5.
- As with ansatz's analysis, these α are EFFECTIVE exponents over ε ∈ [3e−5, 3e−3] at N = 300 (addendum 2), not
  asymptotic dimensions.

## α-independent by-product: realisation sensitivity (gate G3, addenda 6–10)
The fraction r of window start points whose base outcome changes across rtol 1e−11 … 1e−14 (a lower bound, from 4
tolerances):
- **TS L1: 0.373;**
- **TS L3: 0.067;**
- **Kerr 4/5 and Kerr 3/5: 0.000 each** (0/75).

In TS, a sizeable share of start points sits on chaotic transients whose outcome is decided by integration-error-sized
perturbations. In Kerr, none does.

## Independence from ansatz (and what is shared)
**Shared:** the TS component files (sealed, ansatz's), the levels and the outcome rules (from the spec), and the
Python stack (identical: CPython 3.14.5, numpy 2.4.6, scipy 1.18.0 — see ENVIRONMENT/).

**Bridge's own:**
- the Kerr chart (regularised, addendum 5);
- L_sep by bisection to 1e−10, gated on the analytic BPT circular orbits to ≤ 5e−10;
- the window procedure;
- seeds and K = 2000;
- the numba DOP853 integrator (ansatz: DP5(4));
- the binomial-MLE estimator (ansatz: WLS, reported here as secondary).

## Process record (honest)
Ten amendments were made before any α was computed. Several followed failed gates, each root-caused:
- G1 aimed at the wrong circular-orbit branch;
- the G4 fitter bands were mis-calibrated;
- the bridge's own Kerr chart was numerically singular at the ergosurface (ansatz's and tabula's codes were checked
  clean);
- the window spanned both edges;
- G3's position criteria were ill-posed on sensitive orbits; the final validation (addendum 10) is a post-failure
  judgement and is recorded as one.

**Environment:** CPython 3.14.5, numpy 2.4.6 (Accelerate), scipy 1.18.0 (Accelerate), sympy 1.14.0, mpmath 1.3.0,
numba 0.65.1, macOS 26.5 arm64. The env stamp is embedded in `results/v12_fit_primary.json`.

## Pending (pre-registered extensions)
E1 (ε down to 1e−6, N = 300 vs 600, rtol 1e−13), E2 (perturbing p_x), and the outer-transition secondary. After the
seal: comparison with ansatz's per-level α and CIs.
