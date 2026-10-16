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

## Build log (no MN verdicts)
- **Gate A2: PASS.** The regularised W, g^xx, g^yy and g_φφ equal the unregularised forms to ≤ 1e−38 relative (40
  digits, 50 points with |A| > 0.1 at each of C0, F5-R, p1, p2). `results/v13_gate_A2.json`.
- **Integrator** (`code/v13_orbit.py`): the V12 numba DOP853 on the regularised field, with section recording and
  B9/base domains. A smoke run at C0 gave 200 returns in about 0.1 s, with drift ~1e−10 (development check only).
- **Indicator self-test** (`code/v13_indicators.py`, `results/v13_indicator_selftest.json`; standard map, N = 2000):
  - regular orbits: log10 Δν = −11.0 and −10.4, K = 0.00;
  - chaotic orbits: log10 Δν = −1.1 and −0.7, K = 1.00.
  - PASS, after one fix: the first attempt fed NAFF a signal built from p mod 2π, which jumps, and that mis-scored
    one regular rotational curve at −0.7. The self-test now uses e^{ix}, the map's natural angle. MN section curves are
    closed and continuous, so they keep the centred (x, p_x) signal.
- **Rule for development smoke tests:** no MN orbits from shared or gate levels are inspected before thresholds are
  fixed. Pipeline smoke runs use Hénon–Heiles and Kerr only.

## Kerr null at χ = 0.9 (C0 and F5-R's χ ≈ 0.9 partner; A6). Thresholds fixed here, before any MN orbit is scored.
- ℓ_w = 2.7, E_b = 0.997727579 (the merge of the bound region with the plunge region). Levels: E_b − 1e−4, E_b − 1e−3,
  E_b − 1e−2 and E_b − 0.03 at ℓ_w, plus the shared level (0.95, 3).
- **Pilot:** rtol 1e−11 at every level.
- **C2 pilot self-test: PASS.** At rtol 1e−7 the drift is 6.4e−6, which fails as it should; at 1e−11 it is 2.7e−10.
- **READ per level:** 35, 57, 60, 60 and 60 of 60.
  - The ABSTAIN orbits are all LEFT_D (plunging) at the two levels nearest the barrier: 25 and 3.
- **Thresholds** (class-wise max of the per-level training p99s): **A1 > −7.61, A2 > 0.0193.**
- **C1: PASS.** Held-out READ orbits: 0 of 136 CHAOTIC (CP95 upper bound 2.2%; binomial p = 1.0).
- Files: `results/v13_kerr_null_C0.json`, `_analysis.json`, `v13_pilot_selftest_C0.json`.

## C0 instrument gate (A3: base domain, drift ≤ 1e−8; thresholds from the χ = 0.9 Kerr null)
- **Inner region** (ρ 0.719–2.125): 50 of 60 READ; **49 of 50 CHAOTIC (98%)**, against a required ≥ 50%.
- **Outer region** (ρ 2.386–13.639): 60 of 60 READ; **0 of 60 CHAOTIC**, against a required ≤ 10%.
- **The sea sits at ρ ≈ 0.72–2.1**, as published (CLA/LGAC).
- **C0 gate (inner and outer): PASS.**
- **C3** (regular orbits on the published islands, NOT CHAOTIC on both arms): pending. It needs the islands located
  by the bridge's own fixed-point search.
- **Finding, not a gate** (A3: the same orbits under the B9 domain at 1e−9):
  - inner region: **59 of 60 orbits leave D** before 2000 returns, so 1 is READ (and it is NOT CHAOTIC);
  - outer region: 0 of 60 leave D, 60 READ, 0 CHAOTIC.
  - **Essentially all of the published inner-region chaos at C0 involves orbits that enter the neighbourhood of the
    equatorial singular ring, the CTC-adjacent zone that B9 excludes.**
- Sealed for the exchange with tabula: `results/v13_c0_gate.json` (sha256 below, recorded at commit).
6a705e2bd53443e8755387d68913857d99658f25a09053be21266e41cfbd74d1  falsification/V13_mn_chaotic_sea/results/v13_c0_gate.json

## C0 exchange with tabula (§7; both sealed before the exchange: tabula a1c5051 / dd6c102c…, bridge d24e034 / 6a705e2b…)

| | bridge V13 | tabula K20 | §7 |
|---|---|---|---|
| inner CHAOTIC | 49/50 = 0.98 [0.894, 0.999] | 75/80 = 0.9375 [0.860, 0.979] | CIs overlap: AGREE |
| outer CHAOTIC | 0/60 [0, 0.060] | 0/100 [0, 0.036] | AGREE |
| inner leaving D_B9 before 2000 returns | 59/60 (median 15 returns) | 95/100 (median 16) | AGREE |
| base-CHAOTIC leaving D_B9 before 500 returns | 49/49 | 75/75 | AGREE |

- The two screens are independent: different indicators (NAFF and 0–1 test, against FTLE ratio and correlation
  dimension), different code, and their own Kerr nulls.
- **Both find the published C0 inner chaos real, and lying entirely in the singular-ring/CTC neighbourhood that D
  excludes.**
- Limitation on the bridge side: section points were not stored, so the bridge's sea-ρ statement uses starting
  points only.
