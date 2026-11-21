# V27: non-rational axis data (K5). Bridge checks of Gemini Neon T12/T13/T16 (2026-11-21, before code)
Neon's outputs: /Users/sumit/Github/neon_work/onlykerr/T12_K5_SUMMARY.md and T16_UNIVERSAL_SUMMARY.md. They are
UNVERIFIED.

**A1 (Curzon reduction, exact).** f0 = e^{−2M/z} with w = −2M/z gives P̃ = ã − e^w. With x = e^w the NVE becomes
v_xx + v_x/x + (3/16)/(x − ã)² v = 0.
- Check this symbolically.
- Exponents: {0, 0} at x = 0, {1/4, 3/4} at x = ã, and ±i√3/4 at ∞.

**A2 (group computation, exact).**
- Take M0 = [[1, 1], [0, 1]] and M_ã = [[u, −(1 + u²)/τ], [τ, −u]], with u symbolic.
- Let g_k = M0^k M_ã M0^{−k}, h1 = g0g1 and h2 = g0g2.
- **Claim:** tr h1 = −2 − τ², tr h2 = −2 − 4τ², and tr[h1, h2] − 2 = −4τ⁶. Check these identically in u, τ.
- The parameterisation is valid when it covers every pair (parabolic M0, trace-0 M_ã) with tr(M0M_ã) = τ, up to
  conjugation. Check: tr M_ã = 0, det = 1, tr(M0M_ã) = τ.

**A3 (single-energy barrier examples, exact).**
- f0 = 1 − e^{z/√3}cot(z/2) at a = 1 (P = e^{z/√3}cot(z/2)), Y = sin z, C = √3/2:
  Y″ − (3/4)Y′²/Y + C + (3/4)(P′/P)²Y ≡ 0.
- P = sin(√3 z)/cosh z, u = (√3/4)cot(√3 z) + (3/4)tanh z: u′ + u² + (3/16)(P′/P)² ≡ 0.

**PASS** = each identity holds to exact 0 (sympy simplify, or numeric at 5 random complex points to below 1e−25 at
30 digits).

**Must-fail controls:**
- A2 with M0 replaced by diag(λ, 1/λ) must give tr[h1, h2] = 2.
- A3 with √3 replaced by 1.7 in the second example must leave a nonzero residual.

**Literature (to check after the computation):** whether axis-geodesic first-order non-integrability for
Curzon–Chazy is new relative to Georgiev 2019 (equatorial / periodic-orbit method).

---
## Addendum B (2026-11-21 ~11:20, before the target run): check of Neon T21 Theorem 1 on its own worked example
Source: /Users/sumit/Github/neon_work/onlykerr/T21_summary.md (UNVERIFIED). Theorem 1 is the annulus winding-number
obstruction. Its hypotheses on a circle: all zeros and poles of P_a inside are simple, |m| >= 2, N_in + P_in >= 3,
and ||eta|| <= 1/15. Conclusion: SL2. The Bridge re-derived the proof steps by hand (see the summary). This addendum
checks numerically the quantities the proof uses, on Neon's example. Scope: one example, so this is NOT a proof check
of Theorem 2.

**Target:**
- f0 = prod_{k=1..8} (1 - z/2^{k^2}); the factors for k >= 9 differ from 1 by < 2^{-68} on the circle.
- a = 0.7, circle |z| = R = 2^{12.5}.
- P_a = a - f0, so P_a'/P_a = f0'/(f0 - a).
- Code: code/v27_B_lib.py (DOP853, rtol 1e-12) and code/v27_B.py.
- Interpreter: conjecture_machine/.venv (CPython 3.14.5).

**Clauses, each on the claim's own circle and example:**
- **B1 (counts).**
  - The winding of P_a around the circle is 3 (|raw - 3| < 1e-3). f0 is entire, so P_in = 0; hence m = 3 and
    N_in + P_in = 3.
  - Simplicity: Newton from 2, 16, 512 finds the three a-points inside, all with |f0'| > 1e-6 there.
  - The three a-points are distinct, which accounts for all of the winding.
- **B2 (eta).**
  - max |eta| on 2^16 points is < 1/15.
  - The 2^16-point and 2^14-point maxima agree to 1e-6.
  - Neon's stated value: |max eta - 0.06045| <= 1e-4.
- **B3 (trace).**
  - |tr M - (-1869.187)| <= 0.01, which is Neon's stated value at its stated 3 decimals, with margin.
  - |tr M| > 27, the proof's own bound.
- **B4 (det).** |det M - 1| <= 1e-6, i.e. 100 x the pre-run C3 floor of 6.9e-9.
- **B5 (D-infinity step).** The winding of v+ v- (the Floquet eigen-solutions) around the circle is 1, with
  |raw - 1| < 0.01. That gives a winding of 2 for Y, as the proof states.

**Controls, PRE-RUN alone (results/v27_B_controls_prerun.txt):**
| Control | Expect | Pre-run |
|---|---|---|
| C3 Euler P = z^3 at the same R (integrator floor) | tr = -2cosh(pi sqrt23/2) | relerr 1.3e-13, det-1 6.9e-9 |
| C1 must-escape (z-1)(z-2), \|z\| = 20 | tr = -2cosh(pi sqrt2), winding(v+v-) = 1, N + P = 2 < 3 | relerr 2.3e-13, winding 1.0000, m = 2 |
| C2 must-fail hypothesis: same f0 at R = 2^9.3 | max\|eta\| > 1/15 is flagged | 1.448 (flagged) |

**PASS** = B1-B5 all hold. A FAIL on any clause is recorded as registered.
