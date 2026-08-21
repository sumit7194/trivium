# T2 — Findings: the null holds, and conditioning cannot change what the criterion *says*

*Run 2026-08-21 for tabula. Gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code.
Bridge-solo; **I did not build the conditioning**, which is the point of the exercise.*

## Gates

| gate | result |
|---|---|
| **T2a** — positive control must emit | **PASS** (after two self-caught failures, below) |
| **T2b** — null must NOT cross 1e-10 | **PASS** — sits **9 orders above** the threshold |
| **T2c** — conditioning movement | **PASS, but reinterpreted** — see §3 |

```
                     uncond       cond      movement  emits  corr(H)
varied (positive)  8.596e-13   7.707e-13     1.12x    YES    1.000
pinned (null)      7.054e-04   5.205e-04     1.36x    NO     0.000
raw variant, no column normalisation:
varied (positive)  8.597e-13   8.866e-13     0.97x    YES    1.000
pinned (null)      6.079e-04   5.391e-04     1.13x    NO     0.000
```

**The conditioned degree-6 pipeline does not emit on a chaotic substrate with no second invariant.**
Independent substrate (Hénon–Heiles near E=1/6), independent implementation. That is what tabula asked for.

## 1. The positive control failed twice first, and both were mine

- **Basis mis-specification.** I applied tabula's degree-2 *coordinate* cap to Hénon–Heiles, whose potential
  contains `x²y` and `y³`. **H was not representable in my own basis** — I asked the readout to find
  something it structurally could not express. Identical in form to the H2³ problem tabula had described to
  me an hour earlier.
- **Substrate quality.** With the basis fixed, the readout found H at **correlation 1.000** but returned
  2.2e-10 against a 1e-10 bar — **T2a failed as frozen.** The ceiling was my velocity-Verlet energy error,
  not the readout. Cutting dt 4× at matched duration moved it to 7.7e-13. Recorded as a stated post-hoc
  change; it is conservative, since more headroom on the positive makes the null *more* stringent.

**A null from a pipeline that has not passed its positive control says nothing.** Both failures were caught
by that gate and neither would have been visible in the null.

## 2. ⚠️ The finding that matters more than the null

**The generalised eigenproblem is invariant under invertible linear reparametrisation of the feature
basis.** For `Cw v = λ Ct v`, the map `F → FD` gives `Cw → DᵀCwD`, `Ct → DᵀCtD`, and the eigenvalues are
unchanged. Column normalisation is such a map. **So is SVD rescaling at unchanged dimension.**

Verified against a known ground truth (planted ratio 9.999e-05):

| basis | recovered ratio |
|---|---|
| original | 8.0814e-05 |
| arbitrary invertible mix | **8.0814e-05** |
| SVD-whitened, dim unchanged | **8.0814e-05** |
| **diagonal rescale, 1e16 dynamic range** | **9.1097e-14** ← wrong by 9 orders |

Two consequences:

**(a) In exact arithmetic, conditioning at unchanged dimension is a no-op for this readout.** It cannot
change what the criterion *says* — only what a finite-precision solver can *resolve*. tabula's sixteen
orders is therefore necessarily a numerical recovery, not a mathematical change, and **a reparametrisation
cannot manufacture a signal that is not in the data.** That is a stronger argument for their fix than this
null is.

**(b) Ill-conditioning drives the ratio spuriously SMALL — toward false EMISSION, never toward false
CERTIFY.** A basis with 1e16 dynamic range reported 9.1e-14 where the truth was 1.0e-04. Since **every
verdict in tabula's ladder is CERTIFY (a large ratio)**, this failure mode cannot have produced them: it
pushes the wrong way. Their verdicts are robust to it *by direction*, independent of any control.
*(Observed on one construction; stated as measured, not proved in general.)*

## 3. Retraction of my own T2c framing

I reported the movement figures (1.12×, 1.36×) as independently corroborating tabula's 12%. **Withdrawn.**
Given §2 those movements are *numerical noise in the eigensolver*, not a measurement of a real effect —
and my normalised and raw baselines agree to four digits (8.596e-13 vs 8.597e-13), which is the invariance,
not an accident. The movement magnitude carries no information; the invariance argument replaces it.

## 4. Honest scope

- **My conditioning was never the aggressive intervention theirs is.** Because of §2 it *cannot* be, in any
  basis. So this run does not reproduce their 16-order recovery and cannot corroborate its magnitude — only
  that no emission appears on a null.
- **Islands bias toward emission.** At E₀ ≈ 0.98/6 the chaotic sea dominates but regular islands survive,
  and an island orbit genuinely has a second invariant. Contamination makes emission *more* likely, so
  **non-emission is the conservative direction to be wrong in.**
- **The right check for tabula is stability, not this null.** If the intervention is purely numerical, what
  distinguishes a real resolution recovery from solver noise is whether the conditioned answer is *stable*
  under tolerance and precision — a tol sweep, or float128. Convergence confirms; wandering does not.

## Inputs & artifacts

`code/t2_null.py` (dt=0.005), `code/t2_null_dt02.py` (frozen first attempt), `code/t2_raw.py` ·
`results/t2_null_dt005.json`, `results/t2_raw.json`. 70 trajectories per ensemble, velocity-Verlet,
train/test split over trajectories. Requested by tabula.
