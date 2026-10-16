# V13 findings

## Geometry (a554dc6)
- **G-q: PASS.** CLA's four thresholds reproduce to ≤ 1.7e−5. The C0 inner region is at ρ 0.7194–2.1246.
- **Shared levels:** p1 (37/40, 29/10), p2 (1/2, 0) (the MR level), F5-R (19/20, 3).

## Equatorial ring singularity: independent confirmation of tabula (SpaceTime 1e13988, literature c0186da)
- **B = 0 ring (A3).** It sits at x_s = 1.92982825852 (C0) and 1.92192258792 (F5-R), from (x − 1)a² = x + 1 with
  a = −b, and B(x_s) ≤ 5e−100. It is outside the horizon segment (R ≈ 1.65).
- **Kretschmann scalar.** `code/v13_kretschmann.py`, `results/v13_kretschmann.json`. The bridge's route is
  independent of tabula's:
  - the V9 metric transcription;
  - EXACT sympy first and second derivatives, lambdified to mpmath at 60 digits (tabula used numeric mp.diff);
  - Christoffel → Riemann → K assembled in the bridge's own code.
- **Validation:** β = 0 reproduces Kerr's closed form at 3 points to ≤ 6e−59 relative.
- **Results**, equatorial, both sides of x_s, d = |x − x_s|:

  | | d = 1e−2 | 1e−3 | 1e−4 | 1e−5 |
  |---|---|---|---|---|
  | C0, x > x_s | 1.82e14 | 1.191e20 | 1.100e26 | 1.091e32 |
  | C0, x < x_s | −4.2e13 | 9.81e19 | 1.079e26 | 1.089e32 |
  | F5-R (M = 89 units), x > x_s | 2.9e6 | 1.870e12 | 1.726e18 | 1.711e24 |

  - K grows by 10⁶ per decade, i.e. K ∝ d^−6, the same law as Schwarzschild's r = 0.
  - The C0 values agree with tabula's (1.19e20, 1.10e26, 1.09e32) to 3 digits.
  - F5-R matches C0 after the M⁴ scaling (89⁴ ≈ 6.3e7).
- **Conclusion: CONFIRMED.** There is a naked curvature ring singularity on the equator outside the horizon, at
  χ ≈ 0.9 and q ≈ 0.95.
- **Literature (tabula's full-text check):** not identified in the MN literature. Brink 2008 (arXiv:0807.1179,
  Fig. 10) states "no singularities outside". Precedent in TS δ=2: Kodama–Hikida, gr-qc/0304064.
- **Caveats for any write-up:**
  - The Manko–Novikov 1992 original is not read (closed access).
  - Two implementations from one fleet share the MN formula source chain (ansatz manifest → V9; tabula's script). An
    outside check of the metric formula against MN 1992 is still owed.
