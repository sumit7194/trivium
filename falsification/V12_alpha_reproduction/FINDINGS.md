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

## Post-seal correction and comparison with ansatz (2026-10-11)
**Correction.** The pre-registration says ansatz's per-level α values and CIs "are not" known to the bridge. That
statement was **false when written**. The bridge's own claims ledger (outreach/, local) already listed them from
ansatz's §150 report, and the one-pager quoted 0.055 and 0.093.
- What WAS fixed before computing any α: the procedure, every threshold, seeds, windows and the verdict rules.
- Nothing was tuned on α. The 10 amendments concern gates on synthetic data, the separatrix, the metric chart, the
  windows and the integrator; none uses an α value.
- But V12 is not blind to ansatz's numbers, and it should not be described as blind.

**Comparison** (pre-registered rule: they AGREE if the 95% CIs overlap). Ansatz's values are from §150 via the
ledger: L3 is the addendum-2 rerun, and its Kerr values are WLS.

| Level | TS, bridge | TS, ansatz | Kerr, bridge | Kerr, ansatz | Agree? |
|---|---|---|---|---|---|
| L1 | 0.044 [0.032, 0.055] | 0.055 [0.044, 0.067] | 1.008 [0.906, 1.129] | 1.055 [0.997, 1.112] | yes, both |
| L2 | 0.075 [0.060, 0.089] | 0.093 [0.079, 0.109] | 0.955 [0.861, 1.072] | 1.039 [0.978, 1.098] | yes, both |
| L3 | 0.147 [0.124, 0.170] | 0.159 [0.132, 0.186] | 0.938 [0.843, 1.049] | 1.039 [0.906, 1.203] | yes, both |

**All six AGREE.**
- **Pattern worth stating:** the bridge's values are lower in all six cells: TS by 0.011–0.018, Kerr by 0.05–0.10.
  Same-direction offsets suggest a shared systematic, not noise.
- **Candidates:** window definition and width; estimator (binomial MLE vs WLS, though the bridge's own WLS equals its
  MLE to 0.002, so the estimator is unlikely); K (2000 vs 1500); and ε_sep matching (exact bisection vs a 0.01 m
  grid, which moves the Kerr partner L by about 0.1%).
- **Not pursued further:** this is a few-percent effective-exponent difference that does not touch the contrast.

## Secondary (pre-registered, outside the verdict): the OUTER transition (addendum 5)
Same design at the outer survive/plunge edge (K = 2000, seeds 15000+):

| Level | TS α̂ [CI] | TS hits (3e−3 → 3e−5) | Kerr α̂ [CI] |
|---|---|---|---|
| L1 | 0.653 [0.578, 0.739] | 406, 145, 56, 39, 42 | 0.938 [0.836, 1.056] |
| L2 | 0.665 [0.588, 0.760] | 388, 142, 53, 46, 31 | 1.009 [0.912, 1.126] |
| L3 | **1.150** [1.017, 1.303] | 403, 109, 26, 11, 6 | 0.972 [0.870, 1.092] |

**Reading.**
- The fractality is **concentrated at the INNER transition**, the one nearest the plunge, where α̂ is 0.04–0.15.
- At the outer edge:
  - L1 and L2 start smooth-like (hits fall ≈ 3× per half-decade) but flatten at about 2% of x0 at small ε. That is a
    small residual sensitive set.
  - L3 is fully smooth (α ≈ 1, like Kerr).
- This supports the "thin chaotic layer near the separatrix" reading: the chaos is localised, not spread over the
  whole basin boundary.
- The outer windows' fits are INCONCLUSIVE under the primary rule (TS CI upper end not < 0.5), as expected for a
  secondary not designed for it.

## E1, depth and horizon (pre-registered; definitions in addendum 12): the crossover test is NOT EVALUABLE (noise-dominated)
L1 pair, K = 2000, rtol 1e−13, ε = 3e−3 … 1e−6 (8 values). `results/v12_E1_analysis.json`.

| Run | r (rtol 1e−11 vs 1e−13) | Hits, ε = 3e−3 → 1e−6 | Retained after f ≥ 3r | Slopes / α |
|---|---|---|---|---|
| TS, N = 300 | **0.173** (346/2000) | 1094, 1051, 1012, 933, 879, 871, 819, 754 | 2/8 | s(3e−3 → 1e−3) = 0.036 |
| TS, N = 600 | **0.217** (435/2000) | 859, 805, 820, 791, 729, 747, 732, 688 | 0/8 | — |
| Kerr, N = 300 | 0.001 (2) | 417, 120, 36, 18, 8, 2, 0, 0 | 5/8 | s = 1.13, 1.00, 0.63 → α̂ 1.03 [0.92, 1.16] |
| Kerr, N = 600 | 0.001 (2) | 417, 120, 36, 18, 8, 3, 0, 0 | 5/8 | identical, α̂ 1.03 |

**Reading under the pre-registered rules.**
- The script's automatic label, "FLAT TO EPS_MIN", is **overruled**. "No crossover" holds only because the noise rule
  leaves 2/8 (N = 300) and 0/8 (N = 600) TS ε values.
- The registered question (does ε_c fall with N?) **cannot be answered** at this precision. E1 is NOT EVALUABLE.

**What the data do establish (descriptive, not a registered verdict).**
- TS's uncertain fraction is nearly flat over 3.5 decades: 55% → 38% (N = 300) and 43% → 34% (N = 600), with no
  sign of approaching α = 1.
- 17–22% of TS window start points change outcome under a change of integration tolerance (a 1e−11 → 1e−13 level
  perturbation). Kerr's figure is 0.1%, and Kerr is unchanged between N = 300 and 600.
- Therefore any finite-time crossover scale ε_c(N) for TS lies BELOW the resolution of double-precision integration
  (≲ 1e−11 relative). The "genuine fractal vs finite-time artefact" question needs either:
  - higher-precision integration (quad or mpmath) at selected x0, or
  - a different discriminator, e.g. ansatz's fixed-ε horizon test, where α is unchanged between N = 300 and 600
    (0.055 vs 0.051).
- This is consistent with strong exponential sensitivity (long chaotic transients) in TS and its absence in Kerr. It
  sharpens the contrast but does not by itself prove a fractal dimension.

## E2′, perturbation direction p_x (addendum 11: rescaled ε {3e−4 … 3e−6}, same x0 as E2)
- **Kerr control PASSES:** α̂ = 1.051 [0.905, 1.228]; hits 168, 58, 13, 4, 1; r = 0.000.
- **TS, all ε:** α̂ = 0.045 [0.034, 0.056]; hits 1110, 1031, 974, 973, 884. The same value as the x direction (0.044).
- **Under addendum 11's noise rule as written:** TS r = 0.179, and f ≥ 3r leaves 1/5 ε, so E2′ is formally
  **INCONCLUSIVE**.
- (E2 with the original ε set was VOID on Kerr saturation; addendum 11.)

## A tension in the pre-registration, and a post-hoc robustness check (labelled post hoc)
Two parts of this pre-registration pull against each other:
- addendum 6 says realisation-sensitive points legitimately count as uncertain at every ε, as they should for
  chaotic dynamics;
- the E1/E2′ rule "exclude ε with f < 3r" discards exactly the ε where such points are a large share.

The primary x-direction analysis applied no such rule (none was registered for it).

**Post-hoc check that settles which reading matters.** Recompute α using ONLY the x0 whose base outcome is identical at
rtol 1e−11 and 1e−13 (tolerance-invariant). Realisation-sensitive points cannot contribute there.
`results/v12_posthoc_invariant_subset.json`:

| Run | Invariant x0 | Hits (invariant subset) | α̂ (invariant) [CI] | α̂ (all) |
|---|---|---|---|---|
| Primary L1 TS (x) | 1665/2000 | 817, 767, 710, 666, 602 | **0.065** [0.051, 0.078] | 0.044 |
| Primary L1 Kerr (x) | 1999/2000 | 403, 128, 39, 13, 5 | 1.020 [0.924, 1.132] | 1.008 |
| E2′ TS (p_x) | 1641/2000 | 853, 772, 738, 704, 630 | **0.061** [0.047, 0.073] | 0.045 |
| E2′ Kerr (p_x) | 2000/2000 | 168, 58, 13, 4, 1 | 1.051 [0.893, 1.246] | 1.051 |

**Reading (post hoc).**
- The flat uncertainty profile is NOT an integration-noise artefact. Among TS start points whose outcome is
  tolerance-stable, 36–38% are still uncertain at the smallest ε, and α stays at 0.06 in both perturbation
  directions.
- Kerr is unchanged at about 1.
- Removing the realisation-sensitive points raises TS α only slightly (0.044 → 0.065).
- The contrast (TS ≪ 1, Kerr ≈ 1) is robust to (a) the integration tolerance, (b) the perturbation direction, and (c)
  excluding every tolerance-sensitive orbit.

**Caveat on the post-hoc tolerance-invariant check (added 2026-10-11, from ansatz's HP probe gate G3).** Among 20
"tolerance-stable" TS L1 orbits (same outcome at DP5 1e−11 / 1e−12 / 1e−13), one (x0 = 9.925681556) PLUNGES at crossing
283 in double-double (~32-digit) integration while surviving 300 at all double tolerances. So "tolerance-invariant at
double precision" is a PROXY for a resolved outcome, not a guarantee.
- The post-hoc subset analysis above therefore shows that the flat profile is not caused by outcomes that flip WITHIN
  double precision. It does not exclude sensitivity below double precision; that sensitivity would itself be a chaos
  signature.
- The HP probe's base run (DD R1/R2, N = 600) will quantify how many double-stable orbits change outcome at higher
  precision.

## Downstream: ansatz's high-precision crossover probe (2026-10-12), which settles the question E1 could not answer
Double-double integration, ε = 1e−8 … 1e−20.
- **Pre-registered verdict: SUPPORTS FINITE-TIME ARTEFACT.** ε_c(300) = ε_c(600) = 1e−14; TS uncertainty vanishes at
  ε ≤ 1e−17; Kerr is clean at every ε.
- Outcomes are determinate at 32 digits for 98% of double-sensitive x0.
- Post-hoc reading (ansatz, labelled): ε_c tracks orbit lifetime, i.e. transient chaos (a chaotic saddle).
- Consequence for this record: V12's α values stand as EFFECTIVE exponents over [3e−5, 3e−3]. The "fractal" language is
  qualified to "fractal-like down to ~1e−14"; no strict-limit fractal is claimed. This is the user's direction: read
  the results as they came out, not as hoped.
