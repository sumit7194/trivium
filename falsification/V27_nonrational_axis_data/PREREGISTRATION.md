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
