# V13 p1 orbit 55: labelled POST-HOC diagnostic (no registered verdict changes)

## PREREG (written 2026-10-18 before any diagnostic computation; only the sealed screen numbers were looked at)

**Status: post hoc, labelled.** The registered counted-screen verdict for p1 (1/60 CHAOTIC, orbit 55) and the §7
Jaccard FAIL stand as registered whatever this note finds. Sealed input `results/v13_counted_p1.json`
(sha256 b2f3b3c9…b5da, re-verified before use) is read only.

**Object.** p1 = (M, a, β) = (5, 3, 1/5), χ = 0.6, level (E, ℓ) = (37/40, 29/10), L_z = ℓM = 29/2, B9 domain.
Orbit 55: x0 = 6.870002791181163, p_x0 = 0, sealed A1 = −6.408 (thr −7.21), A2 = +0.0275 (thr −0.0025), rtol 1e−11.

**Seen before writing this (from the sealed JSON listing only):** all 59 other READ p1 orbits have A2 < 0 (range
about −0.109 to −0.004) and about 10 of them have A1 > −7.21. Nothing else about orbit 55 has been computed.

**Methods.**
1. *Maximal Lyapunov exponent.* New numba DOP853 (same tableau/step control as v13_orbit) on the 8-dim system
   (z, w), w' = Df(z) w, with the exact second derivatives of the regularised field (as in v13_var). w is
   renormalised to unit Euclidean norm at the step end after every section crossing; λ(t) = Σ ln|w| / t, reported
   per unit proper time τ and per return. Domain and drift checked at every step (B9 for p1; base for C0).
   Orbit 55 and control (i) to N_L = 20000 returns (10× the screen) at rtol 1e−12 if the timing allows on one core,
   otherwise as many as fit in ~1.5 h (≥ 4000). Controls: (i) the READ p1 orbit with the most negative A1
   (orbit 14, A1 = −10.26); (ii) a C0 inner base-domain orbit that read CHAOTIC in `v13_c0_gate.json`
   (orbit 20, x0 ≈ 3.1095, p_x0 = 0), for as many returns as it stays in the base domain (≤ 20000).
   Two different initial tangent vectors for orbit 55 (agreement check).
2. *Section geometry.* On orbit 55's N_L section points: correlation dimension D₂ (Grassberger–Procaccia, points
   scaled to unit box in x and p_x, slope of log C(r) on r ∈ [10^−2.5, 10^−1.5]); NAFF dominant frequency on
   successive 2000-return windows (spread of ν); the 0–1 test K on successive 2000-return windows and on the full
   series. Same quantities for control (i).
3. *A2 calibration.* Mean, sd, max, min of A2 over the 59 other READ p1 orbits (sealed values); z-score and rank of
   0.0275; comparison with the p1 Kerr-null A2 values (`v13_kerr_null_p1.json`, read only) and the −0.0025
   threshold. Also A1's distribution (how many regular-labelled orbits exceed −7.21).
4. *Integrator check.* Orbit 55 with the registered integrator `v13_orbit.make/integrate`, 2000 returns, at rtol
   1e−11 (must reproduce the sealed A1/A2 exactly), 1e−12 and 1e−13; A1/A2 at each; section-point separation between
   the 1e−12 and 1e−13 runs vs return number (linear growth = regular phase drift, exponential = chaos).

**Decision rules (fixed now).**
- *Lyapunov-regular:* log–log slope of λ(t) over the last decade of returns ≤ −0.7 (consistent with ln t / t), AND
  λ at the final return ≤ 3× control (i)'s λ at the same number of returns.
- *Lyapunov-chaotic:* slope over the last decade ≥ −0.3 (saturation) AND final λ ≥ 10× control (i)'s.
- otherwise *Lyapunov-inconclusive* (e.g. λ below the ln N/N floor of the run length).
- *Geometry curve-like:* D₂ ≤ 1.3 and window-ν spread ≤ 1e−5 cycles/return; *area-filling:* D₂ ≥ 1.7 or spread
  ≥ 1e−3; else intermediate.
- *Long-window K:* K(full N_L) < 0.1 counts for regular; > 0.5 counts for chaotic.
- **Verdict:** "likely regular" iff Lyapunov-regular AND curve-like AND K(full) < 0.1. "likely chaotic" iff
  Lyapunov-chaotic AND (area-filling OR K(full) > 0.5). Anything else: "inconclusive". The C0 control must read
  Lyapunov-chaotic (slope ≥ −0.3, λ ≫ control (i)) or the instrument is declared not validated and the verdict is
  "inconclusive".
- *Integrator check passes* iff the rtol 1e−11 rerun reproduces the sealed A1/A2 to ≤ 1e−6 and the 1e−12 vs 1e−13
  values agree to |ΔA1| ≤ 0.5 and |ΔA2| ≤ 0.01. A failure is reported; it does not by itself change the verdict
  rule above.

Resources: one core (NUMBA_NUM_THREADS = OMP/OPENBLAS = 1), nice 10, ≤ 1 GB.

---

## RESULTS (post hoc, labelled; computed after the PREREG above)

**Verdict (by the pre-registered rule): orbit 55 is LIKELY REGULAR.** It is a smooth rotational invariant curve with
rotation number ν = 0.498490 per return, just below the 1:2 resonance. The CHAOTIC call is a false positive of the
AND rule at this χ. The registered p1 count (1/60 CHAOTIC) and the §7 Jaccard FAIL are NOT changed.

Run: 2026-10-18, HEAD f8ad6cb (no commit made), Python 3.14.5, numpy 2.4.6, scipy 1.18.0, sympy 1.14.0, numba
0.65.1, macOS 26.5 arm64. One core, nice 10, peak RSS 0.43 GB. Every run took ≤ 2 min. The sealed inputs' sha256 values
were re-verified in code. The intermediate .npz files are in the session scratchpad (not in the repo); rerun
`code/v13_p1_o55_diag.py lyap …` and then `analyze` to regenerate them.

### 1. Maximal Lyapunov exponent (exact variational equations, rtol 1e−12, renormalised every return)

| orbit | returns | λ per return | λ per τ | ln N / N | slope of log λ, last decade | drift |
|---|---|---|---|---|---|---|
| **55**, tangent a | 20000 | 3.93e−4 | 1.22e−6 | 4.95e−4 | **−0.850** | 3.5e−12 |
| **55**, tangent b | 20000 | 3.52e−4 | 1.09e−6 | 4.95e−4 | −0.836 | 2.0e−12 |
| control (i), p1 orbit 14 (A1 −10.26) | 20000 | 3.79e−4 | 1.22e−6 | 4.95e−4 | −0.849 | 5.0e−12 |
| 55, extended (extra) | 200000 | 4.92e−5 | 1.52e−7 | 6.10e−5 | −0.888 | 3.6e−11 |
| control (i), extended (extra) | 200000 | 5.09e−5 | 1.63e−7 | 6.10e−5 | −0.888 | 5.0e−11 |
| control (ii), C0 inner orbit 20 (CHAOTIC), base domain, rtol 1e−11 | 13546 | **0.755** | 0.118 | 7.0e−4 | −0.006 | 4.7e−8 |
| control (ii), the same orbit at rtol 1e−12 | 595 | 0.755 | 0.116 | 1.1e−2 | −0.109 | 1.9e−8 |

- **Orbit 55: Lyapunov-regular.** λ(t) tracks ln t / t at every checkpoint from 10 to 200000 returns, and it equals
  the clearly regular control (ratio 1.04 at 20000 returns, 0.97 at 200000).
- **Control (ii): Lyapunov-chaotic, so the instrument is validated.** It saturates at 0.755 per return, about 2000×
  orbit 55's value.
- Both C0 runs ended CAPPED (step-size collapse near the ring, as expected in the base domain). Their drifts (4.7e−8
  and 1.9e−8) exceed the base gate's 1e−8 acceptance, so this is a control reading, not a READ. λ agrees between the
  two tolerances to 1e−4.
- A thin chaotic layer with λ < ~5e−5 per return (stretching e-fold time > 20000 returns ≈ 6.5e6 τ) cannot be
  excluded by any finite run. The geometry below shows no width at the 10^−3.5 scale either.

### 2. Section geometry (orbit 55, 20000 returns)
- x ∈ [4.618, 6.870], p_x ∈ [−0.273, 0.273]. Plotted (scratchpad only), it is one smooth closed oval around the
  central fixed point.
- **Correlation dimension D₂ = 1.002** on r ∈ [10^−2.5, 10^−1.5], and 1.057 on [10^−3.5, 10^−2.5]. Control (i):
  1.010 and 1.077. At 200000 returns, orbit 55 gives 1.001 and 1.008. **Curve-like.**
- **NAFF ν on ten 2000-return windows: spread 1.87e−6** (≤ 1e−5, curve-like). Control (i): 3.6e−10.
  - Orbit 55's larger spread is not diffusion. Over 100 windows (200000 returns) it stays bounded at 2.1e−6, and it is
    strictly periodic with a period of about 24 windows (next point).
- **K, the 0–1 test, on the full series:** −3.3e−4 at 20000 returns and −3.9e−5 at 200000 returns (< 0.1, regular).
  C0 control: 0.998.
- *Extras, NOT pre-registered:*
  - **Spectral lines.** All the strong lines of the centred signal are integer combinations of a single frequency:
    ±ν, ±(1−2|ν|) = ±0.00302, ±3ν mod 1 = ∓0.49547, ±0.00604. That is a quasi-periodic, one-frequency invariant curve.
  - **Phase-sorted roughness.** With points sorted by frac(nν), the full-series ν gives a median |Δx|/range of
    9.0e−6 (control (i): 4.5e−6). The points lie on a smooth curve.
- **Geometry verdict: curve-like** (no island chain, no area filling).

### 3. A2 calibration (sealed values, read only)
- **The other 59 READ p1 orbits** (all labelled NOT_CHAOTIC):
  - K: mean −0.0131, sd 0.0168, min −0.109, max −0.0039. None is positive, and none is above −0.0025.
  - Orbit 55's 0.0275 ranks 60/60, z = +2.4.
  - |K| of regular orbits reaches 0.109 (orbits 17, 52 and 16: −0.109, −0.074 and −0.056). Chaotic orbits read
    K ≈ 1.
- **p1 Kerr null (180 READ):** K mean −0.0069, sd 0.0020, max −0.0018.
  - The −0.0025 threshold sits inside this narrow Kerr band, whose sd is 8× smaller than the MN regular-orbit scatter
    at the same χ.
  - The A2 arm therefore separates "slightly negative" from "slightly positive" K, not regular from chaotic. This is
    the degeneracy already flagged in p1 run 1.
- **A1:** 9 of the 59 regular-labelled orbits are above −7.21 (max −3.30). Orbit 55 ranks 55/60. The Kerr null's own
  A1 max is −3.29. A1 alone does not single out orbit 55.
- **Why orbit 55's K is positive** (mechanism, from the extras):
  - ν = 0.49849 is near 1/2, so x_n carries a slow alias line at 0.00302 cycles per return (period about 331 returns).
    That period is comparable to the test's ncut = 200 lags.
  - The line's phase relative to a 2000-return window advances 2000(1 − 2|ν|) mod 1 = 0.0415 cycles per window. So K
    (and the windowed ν) oscillate with a 24.1-window period. This is observed: K runs from −0.041 to +0.028 over 100
    windows.
  - The sealed screen window sits at the maximum of that cycle: K = +0.0275, against a 100-window maximum of +0.0281.
  - **The registered AND rule fires on 46 of 100 successive 2000-return windows of this single regular orbit.** A2
    fires on 46/100 and A1 on 100/100. Control (i) fires on 0/100.
  - So 0.0275 is outside the other orbits' single-window scatter in sign, but inside this orbit's own window-to-window
    scatter.

### 4. Integrator check (registered v13_orbit.integrate, 2000 returns)

| rtol | A1 | A2 | drift |
|---|---|---|---|
| 1e−11 | −6.407584 | 0.0275101 | 1.2e−11 |
| 1e−12 | −6.407560 | 0.0275101 | 1.4e−12 |
| 1e−13 | −6.407559 | 0.0275101 | 1.6e−13 |

- The 1e−11 rerun reproduces the sealed values and section points **bit-for-bit** (ΔA1 = ΔA2 = 0, max point
  difference 0).
- 1e−12 vs 1e−13: |ΔA1| = 4.7e−7 and |ΔA2| = 6.7e−9. **PASS.** The orbit-55 reading is not integrator noise; it
  reflects the orbit's true near-1/2 rotation number.
- The 1e−12 and 1e−13 section points separate as 4e−13 (return 1), 6.4e−10 (100), 3.6e−9 (1000) and 1.9e−8 (2000).
  That is polynomial phase drift; at λ = 0.75 per return the separation would saturate within ~40 returns.

### Applying the pre-registered rule
- Lyapunov-regular: YES (slope −0.850 ≤ −0.7; ratio 1.04 ≤ 3).
- Curve-like: YES (D₂ 1.002 ≤ 1.3; ν spread 1.9e−6 ≤ 1e−5).
- K(full) < 0.1: YES (−3.3e−4).
- C0 control Lyapunov-chaotic: YES. Integrator check: PASS.
- **Conclusion: orbit 55 is likely regular.**

**Implication (post hoc, for the record; no registered number changes):**
- The p1 counted CHAOTIC call and the §7 region FAIL stem from a known weakness: a near-zero Kerr-null A2 threshold
  meets a regular orbit whose rotation number is close to 1/2.
- This agrees with tabula's diagnosis (its overlapping orbit at x0 = 5.2558 reads REGULAR, D₂ ≈ 1).
- Any future screen should calibrate the 0–1 arm against MN regular-orbit scatter or longer windows, as a new
  pre-registration, not a retrofit.

Files: `code/v13_p1_o55_diag.py`, `results/v13_p1_o55_diag.json`, this note.
