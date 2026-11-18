# V20: blind replication of ansatz §154. Does TS δ=2 have a transverse homoclinic point at the capture-edge level?

*Registered 2026-11-18, before any V20 code exists or runs. Sumit's go: 2026-11-18 ("yes please repeat blind check").*

## Disclosure: what the bridge has seen
- **Read in full: ansatz's TANGLE_PREREGISTRATION.md (7c43e03 + addendum 1, 6039005).** Its content:
  - the level;
  - its method (DD GBS integrator, finite-difference Jacobian and tangents, θ only);
  - its gates;
  - its G1 pendulum ratios;
  - Kerr's fixed-point start value of 4.9933985;
  - the §150 capture-edge window x0 ∈ [9.912067, 9.945202];
  - the finding that at this level the hyperbolic orbit is the unstable spherical-type orbit, not an equatorial saddle.
- **Received by message: the verdict word TRANSVERSE**, plus the qualitative statement that the TS fixed point
  "sits slightly below the §150 α window". The seal hashes are verified (3e5dd40; verdict.json da03727c…;
  ts_R2_d1e-12.json 7674f6f0…). I hashed the files without opening them.
- **NOT seen: any ansatz TS number from the run** (θ, λ, the fixed-point x*, the homoclinic point), or any of
  ansatz's tangle code or data files. None will be read before V20 is sealed (commit + sha256).
- **So the verdict word is NOT blind.** The blind quantities are the TS numbers: x*, λ_u, θ and the homoclinic-point
  location. The Lazutkin invariant Ω has no ansatz counterpart; it is the bridge's own coordinate-invariant check.

## Level
- **TS:** `ts45` (the bridge's V10 loader of ansatz's sealed TS2 t1o3 component files, p = 4/5, q = 3/5, σ = 1,
  m = 2/p), E = 97/100, L = +41/8 (retrograde). This is the same level as the bridge's V12 L1.
- **Kerr controls:** `kerr45` (the bridge's own Kerr-in-TS-chart, `kerr_ts_chart.py`; m = 1/p, a = q/p), E = 97/100, at
  - L = +2.55380 (the bridge's own ε_sep-matched partner from V12), and
  - L = +2.550268 (ansatz's partner).

  Kerr is integrable, so both must show zero splitting.

## Independent implementation (differences from ansatz in bold)
- **Field:** V11's compact symbolic build, with an exact Jacobian, compiled with numba.
- **Integration:** **scipy DOP853 in float64 with the variational equations.** Tangents and DP are exact, not finite
  differences. The section event on y = 0 (upward) is located exactly by the solver's root-finder.
- **Fixed point:** **scan** x0 over [x_lo, 30] on Fix(S) = {p_x = 0} for sign changes of g(x0) = x(P(x0, 0)) − x0. Every
  symmetric fixed point found is classified by |tr DP| (> 2 means hyperbolic). The TS target is the hyperbolic one
  nearest the bridge's own V12 window centre. It is then polished by a guarded Newton (the V16 method).
  - The Kerr x* must ALSO match the analytic unstable spherical orbit (gate B3).
- **Manifolds:** reversor S(x, p_x) = (x, −p_x), so W^s = S(W^u). **Both branches of W^u** are grown from a fundamental
  segment [s0, s0·λ] (V16 method).
  - On each branch, the first crossing of p_x = 0 away from the fixed point is a symmetric homoclinic point, refined
    by brentq in s.
  - The **outward** branch (whose first excursion has x > x*) is the one compared with ansatz.
- **Measures, per branch:**
  - θ = 2·atan(|t_x| / |t_p|) at the homoclinic point (the same definition as ansatz);
  - **Ω = Lazutkin's homoclinic invariant** (V16 closed form, Ω = (t_x·t_p)/(e_x·e_p) with t_u = λ⁻ⁿDPⁿe_u), which
    is coordinate-invariant.

## Gates (in order; any failure → STOP, VOID, reported)
- **B0, symmetry, exact (sympy):** g(x, −y) = g(x, y) for every component of ts45 and kerr45.
- **B1, reversor, numerical:** S∘P∘S∘P = id to ≤ 1e−9 at 5 points near each fixed point.
- **B2, fixed point:**
  - closure |P(z*) − z*| ≤ 1e−10;
  - |p_x*| ≤ 1e−10;
  - |det DP − 1| ≤ 1e−8 (area preservation);
  - hyperbolic (|tr DP| > 2 + 1e−6).
- **B3, Kerr against the analytic answer:** x*_Kerr = r_sph − m, with r_sph the unstable (outer double) root of
  Kerr's radial potential R(r) at Q such that R = R′ = 0 (Boyer–Lindquist, m = 1/p, a = q/p, μ = 1, at the given E
  and L). Required to ≤ 1e−8 relative. If no fixed point matches, STOP: the chart or sense is wrong.
- **B4, positive control (the same new code path, re-run on the bridge's own sealed V16 level):** TS p = 3/5,
  E = 0.94, ε = −0.01 prograde, rtol 1e−12, s0 1e−7. It must reproduce the sealed V16 Ω = 1.790e−7 within 5%, and
  the sealed V16 θ = 7.537e−4 within 5%.
- **B5, Kerr negative control:** on both Kerr partners, |Ω_Kerr| and θ_Kerr are both recorded. They define the
  numerical floor.
- **B6, precision and seed stability (TS, both branches):** the four variants (rtol ∈ {1e−12, 1e−13}) × (s0 ∈ {1e−7,
  1e−8}) must agree. Spread (max/min − 1) of θ and of Ω < 5% across the variants. Same homoclinic index n in all four.

## Verdict (V20's own)
- **TRANSVERSE (replicated):** B0–B6 pass, and on the outward branch |Ω_TS| > 1e3·max|Ω_Kerr| and
  θ_TS > 1e3·max θ_Kerr.
- **NOT RESOLVED:** the gates pass, but TS is within 1e3 of the Kerr floor. That disagrees with ansatz's word, and
  is reported and investigated. It is not taken as evidence of integrability.
- **VOID:** any gate fails.

## Blind numeric comparison (after the V20 seal: commit + sha256 sent to ansatz; only then are ansatz's numbers read)
On the outward branch, first symmetric homoclinic point:

| quantity | tolerance (relative) |
|---|---|
| x* (TS fixed point) | 1e−7 |
| λ_u (unstable multiplier) | 1e−5 |
| homoclinic index n | exact |
| homoclinic point x_h | 1e−6 |
| θ | 2% |

Each is reported as AGREE or DISAGREE. A disagreement is investigated, never averaged. The first hypotheses, in
order:
1. a different crossing or branch;
2. a momentum or chart convention (V16's θ disagreement was momentum units);
3. precision (ansatz is DD at 1e−22/1e−28; V20 is float64).

## Scope
One level, the first symmetric homoclinic point, numerical (not interval-certified). Like §154, V20 does not check
the link between this orbit and the §150 window.

## Resources
1 core, nice 10, < 1 GB, < 20 MB disk, a 5 GB disk floor. Runtime is measured on the first run and expected to be
under 1 h in total. Logged on fleet/RUN_BOARD.md.
