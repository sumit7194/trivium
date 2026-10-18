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
- **What both establish:** the published C0 inner chaos is real, and NO base-CHAOTIC orbit stays inside D_B9 for 500
  returns. Every one reaches the excluded neighbourhood of the singular ring / CTC zone (within ~0.025) within
  ≤ ~126 returns.
  - The chaotic orbits' section points span the WHOLE inner region (ρ 0.72–2.12, tabula's section points).
  - So the sea is the inner region, and its orbits keep visiting the excluded zone. It is NOT confined to that zone.
  - (Correction, at tabula's note: an earlier wording here, "lying entirely in the neighbourhood that D excludes",
    overstated this.)
- **The comparison is INCOMPLETE:** the registered region-overlap criterion (Jaccard ≥ 0.5) and the return-time
  comparison could not be evaluated, because V13 stored no section points. This is a gap, not an agreement.
  - Fix: the counted screens store (x, p_x, τ) per crossing (v13_screen, from this commit on).

## C3: published islands NOT CHAOTIC (C0)
- The bridge's own elliptic period-1 fixed points (Newton on P, with the exact variational Jacobian) are at x = 2.26508
  (ρ = 0.8859) and x = 19.18295 (ρ = 8.3503). These are the published inner and outer islands (CLA u₀ and u₀′; tabula
  reports ρ ≈ 0.8–1.05 and 8.35).
- 10 orbits per island (x offsets ±0.2–4% of x_c, p_x = 0), base domain, 1e−8: **20 of 20 READ, 0 CHAOTIC. C3 PASS.**
- Sealed: `results/v13_c3.json` (sha256 below).
a9264f320d6e84c1c465ddae29211058b854b4231d07d2f668a881dc8e949939  falsification/V13_mn_chaotic_sea/results/v13_c3.json
- **C3 exchange:** AGREE. Tabula's island centres are x = 2.265080299244 and 19.182948559923, within 5e−6 of the
  bridge's, and both screens PASS.
  - Tabula found its own I2 (correlation dimension) passed vacuously there: launches within 1e−3 of the centre sat
    below its fixed D₂ windows. Tabula adds a saturation guard, as an amendment before reading any counted verdict, and
    a post-hoc supplementary C3/C4 using the bridge's offsets.
  - V13 does not share this failure mode. A2 (the 0–1 test) is scale-invariant, and A1 (NAFF) is a frequency, well
    defined for small curves.

## Kerr nulls at the other three χ (A6); one bug fixed
- **p1** (χ = 0.6): ℓ_w = 2.9. Thresholds A1 > −7.21, A2 > −0.0025. **C1: PASS, 0 of 90.** E_b − 1e−2 and E_b − 0.03
  have no bound region inside D, so the level set is smaller.
- **p2** (χ = 5/13): ℓ_w = 3.1. Thresholds A1 > −6.93, A2 > −0.0005. **C1: PASS, 0 of 60.** Same two levels absent.
- **F5-R** (χ = 80/89), first run INVALID at the two barrier-nearest levels (0 of 60 READ).
  - **Bug:** the hard-coded proper-time cap τ_max = 1e9 is in units with M = 89, so orbit periods are 89× longer than
    at C0 and 2000 returns exceed the cap.
  - **Fix:** τ_max = 1e9·M (v13_screen; also 1e12 in v13_upo). The F5-R null is being rerun; its first-run thresholds
    are void.
  - C0 (M = 1) and p1/p2 (M = 5, 13) were checked: no orbit there hit the cap. Every SURVIVE-with-<2000-returns fate
    is absent at those points.
- **F5-R null rerun** (with the cap fixed): READ 35, 56, 60, 60 and 60 of 60, matching C0's pattern. Thresholds
  A1 > −7.64, A2 > 0.0200 (C0's: −7.61 and 0.0193). **C1: PASS, 0 of 136.**

## Counted screen: sampling bug in the first p1 run (fixed; disclosed)
- p1 run 1 sampled every equatorial bound interval at (37/40, 29/10), including a second, ring-adjacent component
  [1.076, 2.767] that is not inside D (it starts at p1's B = 0 point, x ≈ 1.0759). Its 30 orbits all read LEFT_D.
- Run 1, as observed before the fix (kept as `results/v13_counted_p1_RUN1_INVALID_wrong_component.json`):
  - the shared component [3.271, 7.756] gave 30 of 30 READ and 1 CHAOTIC.
  - That one orbit (x0 = 6.817) has margins A1 = −6.50 against a threshold of −7.21, and A2 = −0.001 against −0.0025.
    A2's Kerr-null threshold is degenerate (Kerr K ≈ 0), so this verdict is marginal. It is reported as registered,
    with its margins.
- **Fix:** the counted screen samples only components that pass the A8 2-D bound-in-D test. p1 is rerun. p2's run
  sampled only its single valid component, so it stands: **READ 60/60, CHAOTIC 0/60.** F5-R reruns after the fix.

## Counted screens and structure stage (chain finished 2026-10-17 ~03:20). RAW; edges await A9
- **Counted screens** (60 orbits per point, sampling only the A8 bound-in-D component; all 60 READ at every point):

  | point | level (E, ℓ) | component | CHAOTIC |
  |---|---|---|---|
  | p1 (rerun) | 37/40, 29/10 | [3.2707, 7.7556] | **1/60**: orbit 55, x0 = 6.8700, A1 = −6.41 (threshold −7.21), A2 = +0.0275 (threshold −0.0025) |
  | F5-R | 19/20, 3 | [5.4542, 31.1419] | 0/60 |
  | p2 | 37/40, 3 | [3.3886, 5.7411] | 0/60 (unchanged) |

  The p1 orbit clears both arms by a clear margin. Its A2 is positive, unlike run 1's marginal orbit (x0 = 6.817).
  It sits near run 1's marginal orbit, which suggests a thin chaotic layer around x ≈ 6.8–6.9 at p1. That reading is
  post hoc and unconfirmed.
- **UPOs** (period ≤ 3; all have area_ok, i.e. det = 1 to tolerance):

  | point | hyperbolic | of which whole orbit in D |
  |---|---|---|
  | C0 | 12 | 11 |
  | F5-R | 17 | 11 |
  | p1 | 10 | 0 |
  | p2 | 0 | 0 |

- **Transition graphs** (kmax 5, δ 1e−7):
  - **C0:** 31 polyline crossings among the 11 in-D UPOs, including self-loops at UPOs 1, 3 and 6, and
    cycles (1 ↔ 3, 1 ↔ 4, 1 ↔ 6, 3 ↔ 6). Minimum angle 0.29 rad.
  - **F5-R:** 48 crossings, with a dense strongly connected block among UPOs 2–7. The minimum angle is 0.011 rad, and
    21 crossings are below 0.05 rad.
  - p1 and p2: no in-D hyperbolic UPO, so no graph.
- **A7 per-point reading (registered wording, pending A9):**
  - C0 and F5-R: "saddle-in-D candidates exist";
  - p1 and p2: "none found within the search" (period ≤ 3). At p1 this sits alongside one CHAOTIC counted orbit, so
    the search may be too short there (period > 3).
- **Not yet claimed:** any confirmed homo/heteroclinic connection. The crossings are between chords and were never
  refined, so A9 (pre-registered above) must confirm each edge first.
- Sealed (sha256), before any exchange with tabula:
  bab2fbf56efe6ba453394fe1a0e4f3d6d8bfdfe64e8f2a086ccdf2cf26dddad0  falsification/V13_mn_chaotic_sea/results/v13_counted_F5R.json
  b2f3b3c9f705b5da476ad90aa130baefd5bb023525660301022cd3e3b66b5c9c  falsification/V13_mn_chaotic_sea/results/v13_counted_p1.json
  c26e468e21bb31176d2ac34e8cafb567c3e2d84912f3f6befba134ae84f6af2a  falsification/V13_mn_chaotic_sea/results/v13_counted_p2.json
  bcf67d676c6fc508e15f39d7d4d649f0e78ba1ba0ae8d398c2930708424e190d  falsification/V13_mn_chaotic_sea/results/v13_graph_C0_19o20_3.json
  9ad6f36a16686695d72e48ad2f8f4f81f33484027d749e0c28d2a65169617f54  falsification/V13_mn_chaotic_sea/results/v13_graph_F5R_19o20_3.json
  9c6e29d9f82d113132fbf1cb44586906ef49b310bcd38d6319e3ccfcd758bc7e  falsification/V13_mn_chaotic_sea/results/v13_graph_p1_37o40_29o10.json
  11261ff00ad457fefd709c93170da97494d89c2afa295b13308105732824bd95  falsification/V13_mn_chaotic_sea/results/v13_graph_p2_37o40_3.json
  110c96284aa7f314373ed433c0101c544a330891342caf7e272ba3f62e05d5ba  falsification/V13_mn_chaotic_sea/results/v13_upo_C0_19o20_3.json
  84ab1056952c0a5331d30396186537396d1cb0b60fd4490636259a49b2f06176  falsification/V13_mn_chaotic_sea/results/v13_upo_F5R_19o20_3.json
  728f80aac659437af6c15bce94b42cc9d89fcd88781bb9a607c4a16971312933  falsification/V13_mn_chaotic_sea/results/v13_upo_p1_37o40_29o10.json
  13a396884d5fae1a92ea2c21931eeffb267d72037e382905d30dc0e662fd8949  falsification/V13_mn_chaotic_sea/results/v13_upo_p2_37o40_3.json

## Protocol deviation (2026-10-17, logged at tabula's note)
- Before tabula sealed, the bridge's message to tabula included summary counts from the bridge's C0 structure stage:
  in-D UPOs, raw crossings and self-loops. Class: early disclosure of unsealed comparison data.
- **Mitigation:** tabula's C0 UPO search ran in its earlier sealed gate run. All of its in-D, manifold and confirmation
  rules (A10, A10.1, A12) were committed beforehand (tabula 5a7d93d), so its C0 result cannot be steered toward the
  bridge's numbers. C0 is informational in tabula's analysis.
- **Rule from now on:** no counts, edge lists or verdict summaries go to the other side until both have sealed.

## A9 edge confirmation: result as registered (code/v13_a9_confirm.py; results/v13_a9_confirm_{C0,F5R}.json, HEAD 3d304bd)
- **CONFIRMED: C0 1 of 31 (8 → 4), F5-R 1 of 48 (9 → 2).**
  - **No self-loop is confirmed, and neither point has a strongly connected component.**
  - **As registered, A9 does NOT give numerical evidence of a horseshoe inside D at either point.**
- **C0, 8 → 4:**
  - residual 2.4e−11, angle 0.913 rad, chord 8.7e−3;
  - s agreement between rtol 1e−13 and 1e−12 is 8.1e−7, just inside the 1e−6 limit;
  - the connecting orbit stays in D: min x−1 = 0.947, R = 1.674, smallest g_φφ in the box 0.167.
- **F5-R, 9 → 2:** residual 4.8e−10, angle 0.069 rad (0.328 in the scaled metric), s agreement 6.4e−8; min x−1 0.939,
  R 1.664.
- **Failure breakdown** (an edge can fail more than one check):

  | point | first failing check = 1 (chords) | first failing check = 2 (residual) | failing check 1 / 2 / 3 / 4 / 5 |
  |---|---|---|---|
  | C0 | 13 | 17 | 13 / 30 / 1 / 9 / 28 |
  | F5-R | 6 | 41 | 6 / 47 / 2 / 3 / 46 |

  - **Long-chord edges** (chords 0.03–1.06) are polyline artefacts: Newton lands elsewhere or doesn't converge, and 9
    (C0) and 3 (F5-R) of them leave D.
  - **Every short-chord edge** (18 C0, 42 F5-R), including the C0 self-loops at UPOs 1, 3 and 6 and the F5-R
    self-loops at 2–7, **passes checks 1, 3 and 4 and fails check 2, mostly also check 5.**
- **Why checks 2 and 5 fail** (verifier's diagnosis; partially verified):
  - Each return adds about 1e−12 of noise at rtol 1e−13. A single-shooting composition over a + b iterates multiplies
    it by the total stretch, up to ~1e6. The map is therefore rough at ~5e−6 (scaled), far above the 1e−9 residual
    limit.
  - Newton reaches that noise floor on every short-chord edge (residual/noise ≤ 0.55 on C0 and ≤ 0.95 on F5-R).
  - s itself is exponentially ill-conditioned, while the refined POINT moves by only ≤ 3e−5 (C0) and ≤ 8e−4 (F5-R)
    between tolerances.
  - So **A9's checks 2 and 5 were mis-designed for long single-shooting compositions.** This is the bridge's
    design error and is recorded as such. It is not evidence for or against the crossings.
- **No bug was found in the existing code.** All UPOs, λ values and recorded crossings were reproduced exactly. After
  its first pass the agent added a guard (check 5 cannot pass if Newton takes no step). It affected two unconfirmed
  edges and changed no verdict.

## Note from V15 (2026-10-17): ring structure across the MN family
- V15 Q1 shows that for every q > 0 (all V13 points: C0, F5-R, p1, p2) there is exactly ONE B = A = 0 ring, on the
  equator. For q < 0 there is no equatorial ring, but there is a pair of off-equator (±y) B = A = 0 rings.
- D_B9 was designed around the equatorial ring and the CTC zone. A q < 0 study would need D redesigned around the
  off-equator pair. This does not affect any V13 result.
- V15 verifier: the ring is a genuine, reachable curvature singularity (K ∝ d⁻⁶), outside the horizon, for the
  axis-regular metric that V13 uses.

## A10 multiple-shooting confirmation: result as registered (results/v13_a10_{controls,C0,F5R}.json; code/v13_a10_multishoot.py)
- **Controls PASS, so A10 is valid.**
  - **HH positive control at E = 1/6, as registered:** all 54 homoclinic self-loops tried are CONFIRMED_MS. Worst
    residual 2.4e−14, smallest angle 0.22.
  - **Negative controls:** a crossing shifted by 1e−3 along W^u fails check 2 in every case (residuals 1.2e−8 to
    1.1e−4 on MN, 1.9e−8 on HH).
  - The agent's first control run had HH manifolds too short (0 crossings). It is kept, labelled INVALID.
- **C0: 16 of 18 scoped edges CONFIRMED_MS.**
  - Self-loops at UPOs 1, 3 and 6; one strongly connected component {1, 3, 4, 6}.
  - Edges inside the SCC have residuals 6e−12 to 5.3e−11. Minimum margins: x−1 = 0.947, R = 1.674, g_φφ box 0.180.
  - **Failures:**
    - 8→3 fails check 2 (residual 1.0e−10).
    - 8→4 fails check 5 only through a "Newton must take a step" guard carried over from A9. That guard is NOT in
      A10's text, and by the text 8→4 passes (its points agree to 2.4e−11).
    - **Bridge reading: the stricter count, 16/18, is primary; 17/18 by the text alone.** The SCC and self-loops are
      the same either way.
- **F5-R: 35 of 42 CONFIRMED_MS.**
  - Self-loops at UPOs 2–7; one SCC {2, …, 8}. All 7 failures are on check 2.
  - Worst confirmed residual 9.4e−11; smallest angle 0.014 rad; condition number up to 4.5e6; minimum margins
    x−1 = 0.939, R = 1.664.
- **A9 verdict wording: at C0 and at F5-R, NUMERICAL EVIDENCE OF A HORSESHOE INSIDE D_B9** (confirmed transverse
  homoclinic self-loops and a confirmed cycle of heteroclinic connections whose connecting orbits stay inside D).
  **This is not a proof.** The proof belongs to the computer-assisted programme (quantum, plus the V14 replay).
- **Caveats (recorded, not tuned away):**
  1. **Spec flaw, found by the agent:** a segment is one P^{pow}. For the most expanding UPOs (C0 UPO 8, F5-R UPO 9;
     stretch ~4e4 per segment) the integrator noise per segment is 1e−10 to 5e−9, at or above check 2's 1e−10 limit.
     So check 2 near the limit is partly luck.
     - Every failed edge is in that regime. Within the C0 SCC, residuals are at least 2× below the limit, and the
       noise floors there are 1e−11 to 1e−10.
     - An UNREGISTERED, labelled diagnostic with single-return segments passes checks 2, 3, 5 and 6 on 60 of 60
       edges, with residuals ~1e−12. It is supporting evidence only.
  2. The comparison with tabula's independent A12 confirmation is pending; both sides must seal first, and blinding
     is on.
  3. Commit drift: C0 was run at f585656 and F5-R at d417089 (code unchanged between them for these files).

## §7 exchange with tabula: seals and the bridge's side
- **Tabula's K20 official counted analysis, SEALED at SpaceTime 41d57be:**
  - 197_analysis_p1.json 5623aa8b…d553;
  - 197_analysis_p2.json 928f0ce5…be0f;
  - 197_analysis_F5R.json e6a21746…d7e5;
  - post-hoc, labelled: 197_c3_supplement.json e3b3f895…54e2 (586951e).
  - Tabula's informational C0 add-on is still running. Bridge C0 edge data stays withheld until it is sealed.
- **Bridge seals:**
  - counted screens c365279 (hashes above);
  - A9 v13_a9_confirm_C0 220e224f…0358 and _F5R ed54a07c…71b7 (267035d);
  - A10 controls 836f4566…e7ef, C0 a4602110…7710 and F5R 3e098030…e589 (085ac13).
- **Bridge side of the counted-screen comparison** (results/v13_s7_exchange_bridge.json, derived read-only from the
  sealed JSONs). Each CHAOTIC count has a Clopper–Pearson 95% CI. Grid = 200 × 200 over the bound-in-D x-range ×
  ±√(max p_x²):

  | point | CHAOTIC | 95% CI | return-time median (all READ) | chaotic grid cells / all READ cells |
  |---|---|---|---|---|
  | p1 | 1/60 | [0.0004, 0.089] | 319.5 | 331 / 12855 |
  | p2 | 0/60 | [0, 0.060] | 753.6 | 0 / 13095 |
  | F5-R | 0/60 | [0, 0.060] | 14005.6 | 0 / 11898 |

## §7 counted-screen comparison: OUTCOME
- Tabula (sealed 41d57be): 200 orbits per level, all READ, Clopper–Pearson 95%. The grids are identical to the
  bridge's (x edges to < 1e−11, the same p_x half-widths).

  | point | bridge CHAOTIC | tabula CHAOTIC | fractions (CI overlap) | return-time medians (bridge / tabula) | chaotic-region Jaccard |
  |---|---|---|---|---|---|
  | p1 | 1/60 [0.0004, 0.089] | 0/200 [0, 0.018] | AGREE | 319.5 / 315.0, AGREE | **FAIL** (331 cells vs 0) |
  | p2 | 0/60 | 0/200 | AGREE | 753.6 / 752.5, AGREE | AGREE (both empty) |
  | F5-R | 0/60 | 0/200 | AGREE | 14005.6 / 13676.1, AGREE | AGREE (both empty) |

- **Registered result: the p1 region criterion FAILS. Everything else agrees.**
- **Tabula's post-seal diagnosis (from its sealed data):** its orbit x0 = 5.2558 covers 97% of the bridge's orbit-55
  cells and reads REGULAR with margin (λ₂ 5.5e−5 vs p99 9.6e−5; D₂ ≈ 1.0, curve-like). The bridge's CHAOTIC call
  rests on A2 = +0.0275 against a NEGATIVE Kerr-null threshold (−0.0025), already flagged as degenerate in p1 run 1,
  and on A1 = −6.41 vs −7.21.
  - **The bridge's reading, post hoc and labelled:** orbit 55 is likely a false positive of the AND rule at this χ,
    with A2 inside regular-orbit scatter.
  - A labelled diagnostic (a long-time variational Lyapunov estimate for orbit 55, and A2 against the regular-orbit
    K scatter) is to be run. The registered verdict is not changed.

## IMPORTANT geometric caveat on the A10 "horseshoe inside D" evidence (bridge, 2026-10-18)
- The confirmed SCC UPOs at C0 and F5-R lie in the INNER component (section x ≈ 2.0–4.1), not in the counted
  shared-level component (F5-R [5.45, 31.14]).
- Their connecting orbits come within ~0.02 in x of the singular ring:
  - C0: min x − 1 = 0.947, i.e. x 1.947 vs x_s 1.9298; min R 1.674 vs R_s 1.6505;
  - F5-R: min x 1.939 vs x_s 1.9219; min R 1.664 vs R_s 1.6413.
  - The UPOs themselves reach x ≈ 2.01 on the section, 0.087 from the ring.
- They satisfy D_B9's registered tests (the g_φφ box test excludes the CTC side). But **"inside D" here means in the
  strong-field zone right next to the ring singularity, on its non-CTC side, not far from it.** Earlier wording in
  the bridge's morning summary ("away from the ring singularity") overstated this, and is corrected there.
- For any proof built on these h-sets: the claim is chaos in a region that stays a finite (small) distance from the
  singular ring and outside the CTC zone. Whether the h-sets keep a safe margin under interval enclosures is for
  quantum's design (S9) to verify.
