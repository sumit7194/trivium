# V14 Amendment B1: closing the Float64 rounding gap (bridge, 2026-10-18)

Pinned environment, unchanged: Julia 1.13.2, TaylorModels 0.13.1, TaylorIntegration 0.18.19, IntervalArithmetic 1.0.12,
TaylorSeries 0.23.1 (`julia/Manifest.toml`). No package was upgraded or modified. Git HEAD at run time is recorded in
each result JSON.

## 1. What the package does internally (read from `~/.julia/packages/TaylorModels/uhtsT/src`)

### `validated_integ` (`valid_integ/validated_integ.jl`): the integrator V14 used before B1
- **Float64 throughout the polynomial.** The state is `x::Vector{Taylor1{TaylorN{Float64}}}`. TaylorIntegration's
  `taylorstep!` builds the time coefficients by the Taylor recurrence in plain Float64. Each coefficient is a TaylorN
  in the normalised initial-box variables ξ, truncated at degree orderQ = 2. The next step's initial condition is
  `evaluate(x, δt)`, also Float64. The step-start time labels are Float64 sums.
- **Where intervals are used.** These are used only for the remainder Δ of each step, in `remainder_taylorstep!`:
  - an interval Taylor series `xI` of the *whole box* at the step start (`Taylor1{Interval}`, order 17) gives a trial
    Δx = xI[17]·[0,δt]^17;
  - Δ0 = dx[16](box)·δt^17/17 and Δdx = dxI[17]·δt^17;
  - the step is accepted if Δ0 + Δdx·δt ⊆ Δx. Otherwise, up to 50 Picard passes are tried, using
    `Taylor1{TaylorN{Interval}}` arithmetic on x + Δx.
  - Remainders are summed step by step (`rem = rem_old + Δ`). They are not carried through f.
- **Three gaps (B1 named only the first).**
  1. *Float64 rounding* of every coefficient operation (the recurrence, the TaylorN products and the step-transfer
     Horner) is not in Δ. This is the registered gap.
  2. *ξ-truncation.* Terms of degree > orderQ in ξ are dropped by the TaylorN products, both in the Float64
     polynomial and in the interval Picard pass, and are **never bounded**. (1 + ξ)³ at order 2 returns
     1 + 3ξ + 3ξ², and the ξ³ term is lost. This gap was not known when B1 was registered. It is much larger than the
     rounding gap for any box with non-trivial width.
  3. The first-branch acceptance test does not bound f(p + δ) − dx for the trial δ. It compares the polynomial's last
     coefficient with the interval series. The accumulated remainder `rem_old` is added, not propagated through the
     flow.
  - Gaps 2 and 3 cannot be repaired by adding a rounding term. So **B1 option 2 (an a-posteriori rounding bound on
    `validated_integ`) would not have made V14 rigorous.**

### `validated_integ3` (`valid_integ/validated_integ3.jl`, same package and version): what B1 uses
- **Float64 is used only for the candidate.** The polynomial p1 from TaylorIntegration (Float64) is copied into
  `x1N` (TaylorModel1{TaylorModelN{5, Float64}}). Nothing is assumed about its accuracy.
- **Intervals end to end in the validation.** In `_validation3!` / `_picard_pass!`:
  - p1's coefficients are copied exactly into `x1NI` (TaylorModelN{5, **Interval{Float64}**} coefficients);
  - f! is evaluated in that interval arithmetic. TaylorModelN products (`arithmetic.jl`, `remainder_product`) bound
    the neglected ξ-degrees 3–4 (exactly at degree 3; by products of ranges above it) into the TaylorModelN
    remainders;
  - integration (`integrate!`) divides interval coefficients by k, and the τ-tail goes into the remainder;
  - the self-map test is **Δ2 + R(p2 − p1) ⊆ Δ1**. Here p2 is the interval Picard image, and R is an interval-Horner
    range of p2 − p1 over τ ∈ [0, h] and σ ∈ [−1, 1]⁵ (`_poldiff_bound`). So every rounding committed while building
    the Float64 p1, and every rounding in the Picard operator, is inside the accepted remainder.
  - This is option 1 as registered: "every coefficient operation is enclosed".
- **Step transfer.** The state at the step end is evaluated rigorously (`__evaluate!` → `_horner!` in Interval{Float64},
  with residuals in the remainder). It is then re-parametrised by **rigorous QR (Lohner) preconditioning**
  (`qrprecondition!`, with verified inverses à la Rump/Neumaier), giving a new linear initial set L(σ) ⊇ previous image,
  with zero remainder.
- **Time.** `TI._exact_step` makes t_k + h_k exactly representable, so the labels are exact elapsed times. V14 verifies
  this per run in BigFloat (`tdrift3 == 0`, in all runs).
- **Choices made before any B1 Q1 result:**
  - `midrad = false`, so the products use the generic IntervalArithmetic directed rounding rather than the package's
    midpoint-radius kernel;
  - orderQ 2, orderT 16, abstol 1e-20 and maxsteps 20000, as in Q0/Q1;
  - Q0 is also recorded with the default `midrad = true`, as data: 5/5 also.
- **One package defect, handled fail-closed.** `validated_integ3.jl:467` refers to an undefined `t0`. It is reached
  only when a step's Picard validation has failed all the way down to a step of zero length. `b1_poincare.jl` catches
  exactly that `UndefVarError` and fails that image (the piece is not certified).
- **Cost of rigour.** The enclosures are much wider than `validated_integ`'s non-rigorous ones.
  - Same thin Rössler segment: 15–20× in x at t = 6–12. A level-2 support box: image y-width 4.4 instead of ~0.2.
  - Likely cause (diagnosed, not proven): every step re-linearises the set into a parallelepiped L(B), and `qr` is
    called without column pivoting. The parameter states and the zero-width x direction are not the cause (the
    widths are identical with float parameters and in a 3-D system; scratch probe).
  - This is a property of the method, and it was not tuned.

## 2. The fix (option 1; why not option 2)
- Option 1 is feasible within the pinned versions, via `validated_integ3`. `validated_integ` itself cannot take
  Interval coefficients: its caches are typed `Taylor1{TaylorN{T}}` with T the box's float type.
- Option 2 was therefore not implemented, and no rounding-bound formula had to be derived. It would also not have
  been sufficient, because of gaps 2 and 3 above.
- Code (all new; no existing file edited):
  - `julia/b1_rigor.jl`: the B1 step, `rig_eval3` (interval range of each TaylorModelN coefficient + its remainder,
    interval Horner in τ restricted to the validated domain, + TM1 remainder), `tdrift3`, and the kept ε_n time
    widening (intersected with [0, h], sound because the labels are verified exact);
  - `julia/b1_poincare.jl`: q1_poincare.jl with only the integrator and the coefficient enclosure swapped (`diff`
    shows nothing else);
  - `julia/b1_q0.jl`, `julia/b1_q1_cover.jl` (a copy of q1_rossler_cover.jl; base t-sets now from
    r1_generic_*.spec), `julia/b1_q1_merge.jl`, `julia/b1_validate.jl`.

## 3. Validation against 256-bit references (`results/b1_validation.json`; `julia/b1_validate.jl`)
- **Reference integrator.** Our own 256-bit Taylor code (order 40), independent of TaylorSeries. It agrees with the
  50-digit mpmath Q0 reference to ≤ 4.3e−40 at T = 5 on all 5 points.
- **(B) The registered gap, measured.** The test: is the reference inside poly + remainder at every step end of
  `validated_integ`, Q0's 5 points?
  - The pre-B1 TM excluded the 256-bit reference at **145 of 1299** step ends.
  - |reference − Float64 polynomial| reached **66×** the package's remainder (per-point medians 0.10–0.45×).
  - So the Float64 rounding gap is real, not hypothetical.
- **(B) B1 at every step.** With `validated_integ3`, at τ = 0, h/2, h of every step, all 3 components, 5 points:
  **4113 of 4113** samples are inside.
  - Smallest relative margin (distance to the nearer end ÷ width) is 0.0106.
  - Largest |ref − midpoint| ÷ radius is 0.979.
- **(A) The ξ-truncation gap, x′ = x², x0 ∈ [1 − r, 1 + r], exact solution, t = 0.4.**

  | r | pre-B1 max \|exact − TM poly\| / \|rem\| | pre-B1 range contains exact? | B1 contains exact? | B1 overestimate |
  |---|---|---|---|---|
  | 0.1 | 3.8e12 | no | yes | 1.1e−3 |
  | 0.01 | 4.1e9 | no | yes | 1.9e−5 |
  | 0.001 | 4.2e6 | no | yes | 1.9e−7 |

  The deviation scales as r³: the dropped ξ³ term.
- **(C) Q1 spot check.** 12 sampled pieces (M, N, W2 M′, W3 M; a level-2 box, a level-3 box and a level-3 edge piece
  each): **52 of 52** 256-bit P² values (centre and corners) lie inside the B1 enclosures of y, z and the return time.

## 4. Re-qualification
- **Q0 (`results/b1_q0.json`): PASS, 5 of 5 contain the 50-digit reference.**
  - Widths 3.3e−13 to 4.4e−12.
  - Relative margin to the nearer end ≥ 0.035.
  - Labels exact (tdrift 0). T reached exactly. 53–130 steps.
  - Same 5/5 with `midrad = true` (data).

- **Q1 (`results/b1_q1.json`; workers `b1_q1_base_W1.json` and `b1_q1_W2_W3.json`, logs `b1_q1_*.log`): FAIL.**
  - Inputs and setup:
    - the base t-sets and cover lines were read from `r1_generic_{MM,MN,NM,NN}.spec` (only `.spec` files were read,
      no JSONs), and were asserted equal (exact rationals) to the ex_cone boxes. All checks are true;
    - the spec sha256s of ex_cone, W1, W2 and W3 are unchanged from Q1;
    - the section {x = 0, ẋ > 0} in (y, z) is now recorded as confirmed by quantum;
    - same ladder and same checks. Nothing was tuned.

  | covering | B1 | pre-B1 Q1 |
  |---|---|---|
  | base M⟹M, M⟹N, N⟹M, N⟹N | **UNDECIDED** (ladder exhausted) | CERTIFIED (level 2) |
  | W1 M⟹M, M⟹N | REJECTED, certified (b) failure at **level 2** | REJECTED, level 1 |
  | W1 N⟹M | REJECTED, level 1 | REJECTED, level 1 |
  | W1 N⟹N | **UNDECIDED** | CERTIFIED (level 2) |
  | W2 M′⟹M′, N⟹M′ | REJECTED, level 1 | REJECTED, level 1 |
  | W2 **M′⟹N** | **UNDECIDED** | CERTIFIED (level 2) |
  | W2 N⟹N | **UNDECIDED** | CERTIFIED (level 2) |
  | W3 M⟹M, M⟹N | REJECTED, level 1 | REJECTED, level 1 |
  | W3 N⟹M, N⟹N | **UNDECIDED** | CERTIFIED (level 2) |

  - **Gate, by the registered rules:**
    - the four example coverings are **not** certified (all UNDECIDED);
    - W1, W2 and W3 are each REJECTED (each has certified (b) failures);
    - W2 M′⟹N is **not** certified (UNDECIDED).
    - So **Q1 does not pass on the fixed pipeline.**
  - **11 decision changes against pre-B1.** 9 CERTIFIED → UNDECIDED, and 2 REJECTED moved from level 1 to level 2.
    - There is **no opposite CERTIFIED decision** (no FAIL in the comparison-rule sense).
    - B1 certifies nothing that pre-B1 rejected. No pre-B1 certified covering is refuted.
  - **Why UNDECIDED (from the per-level data; all are method limits, not evidence against the coverings):**
    1. *Images that could not be computed.* The package's rigorous QR step ("QR preconditioning could not be
       verified; exiting") stopped integration. Each such image fails closed.
       - At level 3 this hit 10 of 4096 M support boxes, 18 of 4096 N support boxes, 11 of 4096 W2 M′ boxes, and
         1 of 256 N edge pieces at levels 2 and 3.
       - Every level-1 support box (4×4) failed outright: Picard validation shrank to a zero-length step (the
         fail-closed `t0` defect).
       - For base M⟹N, N⟹M, N⟹N and W1/W2/W3 N⟹N, these failed images are the **only** obstruction. At level 3,
         (a) passed on 4086 of 4096 boxes (M⟹N) and 4078 of 4096 (the N-source coverings), with no certified
         violation and max |s_N| ≤ 0.81 on the strip boxes. For the N-source coverings, the one N edge piece makes
         (b) UNDECIDED at levels 2–3.
    2. *Wider enclosures (wrapping).* For base M⟹M, 959 level-3 strip boxes have an |s_N| upper bound up to 1.18,
       and for W2 M′⟹N, 1150 boxes have one up to 1.71. Under pre-B1 these were < 1, though not rigorous.
  - Runtime: 2 processes at nice 10, 8.1 h and 8.3 h wall (29247 s and 29815 s), 9424 and 9488 images, RSS ≤ 1.3 GB
    each.

## 5. Status and what this means
- **B1's rounding fix is in place, and Q0 re-qualifies.**
- **V14 does not re-qualify on Q1 within the registered ladder.** By the prereg's wording this is "S6 replay
  UNDECIDED (method limit)" until a further amendment.
- Also new: the pre-B1 integrator had a second, larger, unregistered gap (ξ-truncation). So the pre-B1 Q1
  "CERTIFIED" decisions were never rigorous certificates, beyond the rounding caveat already disclosed.
- Possible next steps, each needing its own pre-registration (none was tried here):
  - an adaptive refinement rung for failed or wide boxes;
  - a QR with column pivoting (would need code outside the pinned package);
  - a different rigorous integrator.

## Verification status
- **Verified:** Q0 5/5. The B1 step-by-step containment (4113 of 4113). The pre-B1 rounding exceedances (145 of 1299,
  up to 66×). The ξ-truncation failure of pre-B1 and its absence in B1 on x′ = x². The Q1 spot check (52 of 52). The
  Q1 decisions and the counts above (read from the JSONs).
- **Partially verified:** the rigour of `validated_integ3` rests on reading its source (Picard self-map with
  R(p2 − p1), TaylorModelN tail bounds, verified-inverse QR) plus the tests above. The midpoint-radius kernel was
  avoided (`midrad = false`). No line-by-line proof of the package was done.
- **Unverified:** the cause of the wide enclosures (QR without pivoting) is a diagnosis from scratch probes, not
  proven.
