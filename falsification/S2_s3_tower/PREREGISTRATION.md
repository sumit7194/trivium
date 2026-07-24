# S2 — Pre-registration: does the rest-buzz instrument read a CURVED hidden manifold? (the S³ tower is n(n+2))

*Frozen 2026-07-24, before `code/s2_s3_tower.py` is written or run. Falsification v2, Tier S — **rung 1 of
the mathematical ladder** in `KK_EXTENSION_NOTES.md`, stated as a falsifiable gate. Legs S (5D, one hidden
loop, `m_n = n/R`) and U (6D, hidden T², `m = √(n₁²+n₂²)` + axion splitting) established the **rest-buzz
instrument** on **flat** hidden spaces: evolve a massless wave on the hidden manifold, **measure** the
rest-frame oscillation frequency from the time series (FFT), never inject it. S2 asks whether that
instrument survives the move to a **curved** hidden space.*

## The postulate

**"The rest-buzz instrument reads ANY hidden manifold whose Laplacian is computable — on S³ it must read the
Casimir tower `m² = n(n+2)`, with degeneracy `(n+1)²`."**

The flat cases gave sum-of-squares towers. S³ is the first genuinely curved rung — the setting real
compactifications use (the audited G₂ paper's S³×S⁴ lineage). If the instrument is a *method* and not a
flat-space coincidence, it reads this too.

## The reduction (frozen before coding)

Unit S³, metric `dχ² + sin²χ·dΩ₂²`, χ ∈ (0,π). For `ψ = R(χ)·Y_ℓm`, the substitution **`R = u/sin χ`**
turns the radial Laplacian into a 1D Schrödinger operator:

> **`H u ≡ −u'' + [ℓ(ℓ+1)/sin²χ]·u = (λ+1)·u`,  with `λ = −Δ_{S³}` eigenvalue.**

So the exact spectrum is `λ + 1 = (n+1)²` ⇒ **`λ = n(n+2)`**, for integer `n ≥ ℓ`, and the rest-buzz
frequency is `m = √λ = √(n(n+2))`. Grid: **staggered midpoints** `χ_j = (j+½)h`, `h = π/N`, `N = 400`, so
`sin χ` never vanishes on-grid and the `ℓ(ℓ+1)/sin²χ` barrier supplies the boundary behavior (`u ~ χ^{ℓ+1}`);
ℓ = 0 gets plain Dirichlet. Sectors **ℓ = 0,1,2,3**.

## The instrument (must stay the rest-buzz, not a diagonalization)

For each ℓ: seed a **deterministic pseudo-random, smoothed** initial profile `u₀` (nothing about the tower
injected), evolve `ü = −(H−1)u` by leapfrog with `dt` set from a **Gershgorin** bound on `H−1` (stability,
not tuning), record the modal overlap `a(t) = ⟨u(t),u₀⟩`, and read the **FFT peak frequencies** of `a(t)`
in the physical window `ω < 12`, with parabolic sub-bin interpolation — exactly legs S/U's procedure.
Frequencies are **measured**, never inserted.

## Frozen gates

- **S2a — the tower.** Measured buzz peaks in each ℓ-sector must land on `√(n(n+2))` for `n = ℓ … 6`.
  **PASS** iff every matched level agrees within **1.5%** (the FD instrument floor at N=400), for all four
  ℓ-sectors.
- **S2b — the degeneracy, measured not asserted.** Level `n` must appear at the **same** frequency in every
  sector with `ℓ ≤ n` (**ℓ-independence within 1.0%**) and be **absent** from every sector with `ℓ > n`
  (no measured peak within **3%** of `√(n(n+2))`). PASS ⇒ the level count is
  `Σ_{ℓ=0}^{n}(2ℓ+1) = (n+1)²` — the curved-space analogue of leg U's within-shell degeneracy, with the
  `n ≥ ℓ` cutoff as the sharp structural tooth.
- **S2c — curved vs flat, the discriminating control.** A flat T³ of unit radii gives `m² = n₁²+n₂²+n₃²`
  (a sum of three squares). By **Legendre's three-square theorem** an integer is a sum of three squares iff
  it is *not* of the form `4^a(8b+7)`. Test each S³ level `m² = n(n+2)` for three-square representability
  by **exhaustive integer search** (no theorem trusted from memory — the search is the proof). Report the
  first level that **no flat unit T³ can produce**. This is the honest control that the instrument is
  reading *curvature* and not re-deriving a flat tower, and it ties S2 to the Tier-S spectral arc (S1/S3):
  the curved tower is *audibly* not a flat one.
- **S2d — instrument validation (internal, not independent physics).** Cross-check the buzz peaks against a
  direct dense diagonalization of the same `H`. Agreement validates the *reading*, not the physics — stated
  as such, never counted as a second route.
- **A1 guard.** FD on a curved space must carry **O(h²) error, not exactness**. Any level matching to
  ~1e-15 is a **bug smell** (per L2 / the A1 audit), to be reported, not celebrated.

## Verdict rule (three-valued)

- **SURVIVES** — S2a and S2b both PASS: the rest-buzz instrument, unmodified in method, reads the curved
  tower and its degeneracy. The ladder's rung 1 is climbed.
- **KILLED** — the measured tower is systematically *not* `n(n+2)` beyond FD error, or the `n ≥ ℓ` cutoff
  fails: the instrument was a flat-space coincidence, and legs S/U's generality claim is overstated.
- **UNDECIDED(numerics)** — endpoint-singularity pollution (the `1/sin²χ` barrier) prevents clean peak
  reading. Live outcome, reported with the spectra that made it undecidable.

## Honest scope

- **Zero novelty.** `n(n+2)` is the textbook Laplace spectrum of S³ (equivalently the SU(2) Casimir
  `4j(j+1)`, `n = 2j`); the degeneracy `(n+1)²` is standard. **Nothing here is claimed as new physics.** The
  falsifiable content is entirely about **our instrument's reach** — whether a method built and validated on
  flat hidden tori transfers to curved ones — plus S2c's flat-vs-curved discriminator as a bridge finding.
- **No eigenvalue asserted from memory into the gate** (leg-W discipline): `n(n+2)` enters as the
  *prediction being tested*, derived above from the stated metric, and the measurement is independent of it.
  Legendre's criterion is likewise **verified by exhaustive search**, not invoked.
- This is (A)-sense richness in `KK_EXTENSION_NOTES.md`'s terms — a rung on the mathematical ladder. It says
  **nothing** about whether our universe has hidden dimensions; the (B) cliff is untouched and remains
  uncrossable by this or any simulation here.
- Bridge-solo; own code; read-only from sisters. Pure numpy.
