# R6 — Pre-registration: is the subleading (log) coefficient of the 3D area law regulator-independent?

*Frozen 2026-07-24, before `code/r6_log.py` is written or run. Falsification v2, Tier R — the universal
companion to M2's kill. M2 showed the 3D entanglement area-law **coefficient κ is regulator-dependent**
(κ = 0.30/0.41/0.51 across three UV regulators, 51% spread) while the **exponent stays ≈2** (universal).
R6 asks about the **subleading logarithmic term**: `S(R) = κ(R/a)² + b·log(R/a) + c + …`. The log coefficient
b is tied to the conformal anomaly and is *expected* to be universal (scheme-independent) like the exponent —
unlike κ. R6 tries to measure b across the same three regulators and decide.*

## The postulate

**"The subleading log coefficient b of the 3D sphere entanglement entropy is regulator-INDEPENDENT"**
(universal, like the exponent — unlike κ). This completes the "what is universal in the area law" story:
exponent (M2: universal), κ (M2: scheme-dependent), log (R6: ?).

## Method (reuses M2)

Reuse M2's `entropy_from_K` + the three regulator operators (`K_bare`, `K_impr`, `K_hd`) and its
tail-extrapolated `S_ext(n) = Σ_ℓ (2ℓ+1) S_ℓ(n)` (N=200, L0=500). Radii **n ∈ {8,12,16,20,24,28,32,36,40}**
(9 — more than M2's 6, to help separate n² / log n / const). For each regulator fit
**S(n) = a·n² + b·log n + c** (least squares); extract **b**. Uncertainty on b by **jackknife** (drop-one
radius, refit). Also fit the 2-parameter model `a·n²+c` to test whether the log term is even *resolvable*
(does adding it materially reduce the residual?).

## Frozen gates — three-valued, with UNDECIDED prominent

- **R6a — extract b per regulator**, with jackknife error. Report b(bare), b(improved), b(higher-deriv), and
  the M2 midpoint control (a coordinate change, not a regulator change ⇒ must match bare if b is physical).
- **The verdict:**
  - **SURVIVES (universal)** iff (i) the log term is **resolvable** — adding it reduces the 2-parameter fit
    residual by a clear factor — **and** (ii) the three b's agree within their jackknife errors
    (across-regulator spread ≲ within-regulator error), i.e. b is scheme-independent while κ is not.
  - **KILLED (scheme-dependent)** iff b is resolvable **but** the three b's differ clearly
    (across-spread ≫ within-error), like κ.
  - **UNDECIDED(precision)** iff b is **not robustly resolvable** — jackknife error on b comparable to |b|,
    or the log term does not materially improve the fit, or b is contaminated by other subleading structure
    (1/n, constant). **This is the pre-registered, and most likely, honest outcome:** the log term is a
    ~10⁻⁴ relative correction on the κn² leading term, and lattice/finite-R systematics may swamp it. A clean
    UNDECIDED is a real result — it says the instrument that resolves κ's scheme-dependence does **not** reach
    the subleading anomaly term, and it says so with the numbers.

## Honest scope

- Whatever the verdict, this is a **lattice** statement about a free scalar's sphere EE — not a black hole's
  S = A/4. Zero novelty (Srednicki; Bombelli et al.; Solodukhin; the 4D sphere-anomaly-EE literature).
- **No theoretical value for b is asserted from memory** (leg-W discipline): the decisive comparison is the
  three regulators *against each other*, not against a remembered anomaly coefficient. If they agree, that is
  reported as "consistent with a universal (scheme-independent) term," with the measured value stated, not a
  claimed match to a specific literature number.
- The `a·n² + b·log n + c` model is a simplification; real lattice S(n) carries further subleading terms that
  a 3-parameter fit may fold into b. This contamination is a reason UNDECIDED is likely, and is stated as
  such. Bridge-solo; reuses M2's validated (V2-calibrated) entropy pipeline.
