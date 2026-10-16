# V13: pre-registration of the bridge's screen for Manko–Novikov's chaotic sea ("K20")

*2026-10-16. Written and committed BEFORE any V13 code or MN orbit exists. The bridge has not seen any of tabula's
K20 outputs. None exist yet: tabula's screen is frozen at SpaceTime 9aca9a4 plus amendments and is still at the build
stage.*

**Purpose.** This is rung 3 of the chaos-proof plan (fleet/MOONSHOT_REVIEW_2026-10-16.md §1; quantum
PREREG_chaos_horseshoe_phase2.md, 78e2d63/40ad82b). The task is to locate MN's chaotic sea numerically at the certified
points and at the fallback point, and to deliver what quantum needs to build h-sets. Tabula runs an independent screen
(curvature/notes/k20_mn_screen_prereg.md). The two are compared under the protocol in §7, which is sealed before
either side exchanges results.

**What is known in advance:**
- All published MN chaos is at χ = 0.9, q = +0.95 (GLM 2008, LGAC 2010, CLA 2011, CHL 2012; per tabula's full-text
  read, k20_literature.md).
- Islands are near zero width there for q ≲ 0.4.
- Nothing is published at our points.

## 1. Points (M, a, β) as in V9; χ = a/M, k = √(M² − a²), q = β k³/M³ (quantum's MN_METRIC.md convention)
| id | (M, a, β) | χ | q | role |
|---|---|---|---|---|
| p1 | (5, 3, 1/5) | 0.6 | +0.1024 | certified MR point |
| p2 | (13, 5, −1/3) | 5/13 | −0.26217 | certified MR point |
| F5-R | (89, 80, 13394411/1186380) | 80/89 | 19/20 | quantum's fallback (B6); its verdict counts for the fallback |
| C0 | (1, 0.9, 0.95/0.19^{3/2}) | 0.9 | 0.95 | published point; instrument control only |

Kerr nulls: the same (M, a) with β = 0, same code path.

Units: E is per unit rest mass (μ² = 1). Levels are quoted as (E, ℓ) with ℓ = L_z/M, so the published level
(E, L_z) = (0.95, 3) at M = 1 is (0.95, 3).

## 2. Physics, independent of tabula and quantum code
- The metric functions are the bridge's V9 transcription (`v9_nve.mn_functions`), already gated exactly against
  quantum's fields (V8/V9 FINDINGS).
- Reduced 2-DOF Hamiltonian in prolate (x, y):
  - H = ½[g^xx p_x² + g^yy p_y² + W(x, y)] = −½;
  - W = g^tt E² − 2 g^tφ E L_z + g^φφ L_z².
- Equations are built by sympy, lambdified, and checked against finite differences at 20 random points
  (relative error < 1e−8) before use.
- Section Σ = {y = 0, p_y > 0}, coordinates (x, p_x). This is quantum's section and tabula's.

## 3. Shared levels: one per point, named by a mechanical rule BEFORE any orbit (geometry only)
- **Permitted bound region:** a connected component of the equatorial allowed set {x : −1 − W(x, 0) ≥ 0}.
  - It must be a closed x-interval that lies entirely inside D's x-range (x − 1 ≥ δ_x) and does not extend to
    x = 1000.
  - It must also be at least 0.05 wide in x.
  - The off-equator extent is not required.
- **Candidate order:**
  - p1 and p2: their MR levels in V9 row order, converted to (E/μ, L/(μM)), i.e. (1/2, 0), (1/3, 0), (1/2, 1/(2M)).
  - F5-R: the published level (0.95, 3).
- The first candidate with a permitted bound region is the shared level.
- If none has one, use the nearest grid level that does.
  - Grid: E ∈ {0.900, 0.905, …, 0.995}, ℓ ∈ {1.0, 1.1, …, 4.5}, matching tabula's scan range.
  - Nearest by d = |ΔE|/0.005 + |Δℓ|/0.1 from the FIRST candidate. Ties go to lower E, then lower ℓ.
- **D's δ_x:** quantum's rule (§3.4). δ_x = (x_CTC − 1) + 0.025, rounded UP to a multiple of 0.05, where x_CTC is the
  outer x-extent of {g_φφ < 0} over |y| < 1, located on a 400 × 200 (x, y) grid and refined by bisection on y = const
  lines.
  - Singular rule: R² = x² + y² − 1 ≥ max(0.25, (2R_s)²).
- **Geometry gate G-q,** before the shared levels are used. The bridge's equatorial CZV code must reproduce CLA 2011's
  thresholds at C0 (as transcribed by tabula, 3880145):
  - at E = 0.95, the inner and outer regions join at L_z ≈ 2.99761912 (to 1e−3), and the outer region vanishes at
    L_z ≈ 3.40935;
  - at L_z = 3, the regions are separate for E ≤ 0.95038, and the outer region vanishes at E ≈ 0.93210.
  - A failure stops V13 until it is root-caused. A misscaled or flipped β would fail this gate.
- **Output, committed before any orbit:**
  - per point: δ_x, R_s, the candidate checks and the chosen (E, ℓ) as rationals;
  - the 200 × 200 Jaccard grid box, defined from geometry only as in tabula's 9aca9a4: the x-range of the shared
    level's equatorial region, and p_x ∈ ±√(max allowed p_x²) over that range.

## 4. The bridge's screen: independent indicators (not MEGNO, not FTLE, not correlation dimension)
Accuracy standard:
- per-orbit |H + ½| drift ≤ 1e−9 up to the reading time;
- DOP853 at rtol 1e−13;
- a pilot runs on 12 orbits spread across the region and REFUSES when empty, with a self-test that injects a
  known-bad orbit;
- n_in vs n_analysed per cell, plus the excluded orbits by fate and would-be verdict;
- a cell with more than 25% excluded is UNREADABLE.

Two arms, AND rule:
- **A1, frequency-map diffusion (Laskar NAFF).**
  - Measure the section-return frequency and the x-oscillation frequency over returns [1, 1000] and [1001, 2000].
  - The diffusion index is log₁₀|Δν/ν| on the dominant frequency.
- **A2, the 0–1 test for chaos (Gottwald–Melbourne 2009, correlation method), on x at the 2000 returns.** It gives
  K ∈ [0, 1], using the median over 100 random c values.
- **Verdict:**
  - CHAOTIC needs both arms above the matched-null p99.
  - REGULAR needs both below the null p50.
  - Anything else is MIXED.
- **Matched Kerr null:**
  - same (M, a), β = 0, same section and returns;
  - matched in proximity, with d_min = section distance to the nearest located hyperbolic periodic orbit, in 4 log bins;
  - matched in return count.
  - Per-bin gate: if the held-out Kerr CHAOTIC rate is above the CP95 bound of 1%, the bin reads "cannot discriminate".
- **Controls:**
  - C0 at the published level must show ≥ 50% CHAOTIC in the inner region and ≤ 10% in the outer region, and must
    place the sea at ρ ≈ 0.72–2.1. If C0 fails, nothing at p1/p2/F5-R is reported as a result.
  - Regular orbits on C0's published islands must be NOT CHAOTIC on both arms.
  - The Kerr null must be ≤ 1%.

## 5. Structure for quantum (quantum's list (ii), 40ad82b message)
- **UPOs:** periods 1–3 by Newton on Pⁿ from a seed grid. For each, the eigenvalues and eigenvectors of DPⁿ (by
  variational equations), the D-margins along the orbit, and the A1/A2 verdict of its neighbourhood.
- **Transition graph:** for each hyperbolic UPO, grow the unstable manifold from a 1e−6 segment along the unstable
  eigenvector (and the stable manifold backward). Record numerical intersections (sign changes of a cross-distance
  function) with the other UPOs' manifolds, and the iterate n at which each first appears.
- **Splitting angle** at the primary homoclinic point of each candidate UPO, at segment lengths 1e−6 and 1e−7
  (error estimate).
- **Per candidate:** the maximum one-return stretch; the plunge/escape fraction in a 1e−3 neighbourhood; the
  fraction of the CHAOTIC section cloud inside D.
- **Transversality:** the minimum |ẏ| at y = 0 crossings over the sea's orbits.

## 6. Predictions (written first)
- **p1:**
  - the shared level falls back to the grid (the MR levels are too deep to have a bound region in D);
  - CHAOTIC ≤ 5% of D-interior bound orbits;
  - no hyperbolic period ≤ 3 UPO pair with a numerical heteroclinic cycle.
- **p2:** the same as p1, with CHAOTIC ≤ 10%. Low confidence: oblate (q < 0), unstudied.
- **F5-R:**
  - the shared level is (0.95, 3) itself;
  - CHAOTIC ≥ 30% of the inner bound region;
  - at least one hyperbolic period ≤ 3 UPO with a homoclinic connection by n ≤ 6;
  - the fraction of the sea inside D is below 50% (the published sea sits near the CTC/plunge zone). This is the
    prediction most at risk.

## 7. Comparison with tabula (fixed 2026-10-16, bridge ↔ tabula)
- On each shared level:
  - region overlap: Jaccard ≥ 0.5 on the 200 × 200 grid;
  - CHAOTIC fractions: 95% CIs overlap;
  - return-time medians: within ×2;
  - splitting angles: within the combined stated errors.
- Disagreements are reported, never tuned.
- Sealing: commit plus the sha256 of each result JSON, sent to the other side before any exchange of numbers.
- A disagreement does not block quantum's MN run. It is reported in A-K20, and quantum may only build h-sets in
  regions where both screens agree.

## 8. Budget and environment
- At most 2 cores at nice 10. The environment is stamped per tools/envstamp.py (bridge venv).
- A wall-clock budget is not a stop rule. An exhausted screen is reported as "not located within budget".

## 9. Failure handling
A failed gate is root-caused and amended (amendments are numbered and committed before the outputs they govern), never
silently retried.
