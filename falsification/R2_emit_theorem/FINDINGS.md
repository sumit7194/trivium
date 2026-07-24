# R2 — Findings: the emit⟺span theorem, reproduced independently — and a new obstruction (O4)

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier R — the flagship. ansatz proved (§123, 6/6) that the emit engine's linear core satisfies **emit ⟺ a
nonconstant invariant I ∈ span(Φ) is conserved**. The bridge reimplemented the criterion from the stated
algorithm — **its own code, no import of §123** — and reproduced the theorem's teeth. Cross-gate CLOSED, and
the second implementation surfaced a false-positive mode (O4) not in §123's obstruction map — independence
earning its keep (L5).*

## Result in one line

The emit⟺span theorem is **reproduced independently on all four fronts** (R2a–R2d PASS): representable
invariants always emit, the pendulum flips illegible→legible the instant a `cos` atom is added, the G1/G2
guards catch the O1/O2 obstructions, and the scales match §123. **And the degree sweep found a NEW
obstruction O4** — a degree-6 polynomial *falsely emits* (σ_min/σ_max = 2.7×10⁻⁷ < τ_rel) despite the
pendulum having no polynomial invariant: a rich basis approximates a smooth transcendental invariant below
any fixed floor. To be relayed to ansatz.

## The gates (all PASS)

| gate | check | result |
|---|---|---|
| R2a | ⟸ no false negatives | harmonic emits (σ_min/σ_max = **4.6×10⁻¹⁵**); the exact rep. invariant x²+p² gives ‖Mc‖/‖M‖ = **3×10⁻¹⁰** (< τ_rel) — representable ⇒ always emitted |
| R2b | basis-relativity flip | polynomial deg-2 **6.9×10⁻²** (no emit) → **+cos atom 2.2×10⁻¹²** (emit): same system, opposite legibility, purely from the probe |
| R2c | obstruction map | O1 hidden identity {x,p,2x+3p} emits but is off-orbit rank 2<3 ⇒ **G1 flags it**; O2 aliasing 1 orbit→1 null, 6 orbits→0 ⇒ **G2 collapses it** |
| R2d | cross-implementation | harmonic 4.6e-15 (§123 ~4e-16) · pendulum-poly 4.4e-4 (§123 ~8.8e-3) · pendulum+cos 2.2e-12 (§123 ~2.8e-12) — same physics, two implementations |

## Approximation vs representation (the degree sweep)

| basis | σ_min/σ_max | emit? |
|---|---|---|
| polynomial deg 2 | 6.89×10⁻² | no |
| polynomial deg 4 | 4.39×10⁻⁴ | no |
| polynomial deg 6 | **2.69×10⁻⁷** | **yes (false)** |
| poly(4) + cos atom | 2.18×10⁻¹² | yes (true) |

Higher polynomial degree buys a *better approximation* (the ratio falls monotonically) but the polynomial is
never the exact invariant — until, at deg-6 over these bounded orbits, the approximation dips below the floor
and the criterion *falsely* reports an invariant. Adding the **right atom** (cos) jumps straight to exact
representation (2×10⁻¹², eight orders below the deg-2 value). *That* is the corrected G2 law made mechanical:
legibility is representation, not approximation — and the two are separable, in a table.

## O4 — the new obstruction (independence earned its keep, L5)

§123's obstruction map has O1 (hidden identity, caught by G1), O2 (finite-data aliasing, caught by G2), O3
(measure-zero coincidence, probability 0). The bridge's independent reproduction adds a fourth:

> **O4 — smooth-approximation false-positive.** Over a *bounded* orbit set, a sufficiently rich basis
> approximates a smooth transcendental invariant closely enough that σ_min/σ_max falls below any fixed
> relative floor τ_rel, and the criterion emits a quantity that is **not** a true invariant. Neither G1 (the
> polynomial is full-rank off-orbit) nor G2 (it *is* nearly constant on all sampled orbits) catches it. The
> guard that does: **out-of-sample testing** — a true invariant stays conserved on new / wider-range orbits;
> an approximation drifts. This surfaced at deg-6 here because §123's deg-4 demo sat just above the floor.

This is a genuine, relayable contribution to the theorem's scope — exactly why the family reimplements
sister results rather than banking them on trust.

## Two bugs of mine, both caught by the family's own discipline

1. **Constant-column false-emit.** My first run reported σ_min/σ_max = **0.00e+00 for *everything*** —
   because the polynomial basis included the constant φ=1, which per-orbit centring turns into an all-zeros
   column (a trivial null). **Caught by A1's own instinct**: exact-zero everywhere is the "too-clean" tell.
   Fixed by excluding the constant (it is the additive piece being subtracted, not a candidate invariant).
2. **Near-harmonic regime.** My first pendulum orbits were small-amplitude, where cos x ≈ 1−x²/2 makes the
   system nearly harmonic and a polynomial basis *nearly* legible (ratio 2×10⁻⁵ — marginal). **Caught by
   R2d's cross-check against §123's scale** (their 8.8×10⁻³ flagged the regime mismatch). Fixed with
   large-angle, strongly-anharmonic librations — revealing en route that legibility is *data-range-relative*
   too, not only basis-relative.

## Honest scope

- A **cross-implementation reproduction** of ansatz's §123 theorem + adversaries; the theorem is ansatz's,
  the prior art is the Sparse-Invariant / SID null-space literature (Liu–Madhavan–Tegmark;
  Kaiser–Kutz–Brunton, arXiv:1811.00961). **Zero novelty claimed** — the payout is the independence check on
  the family's most valuable v2 result, plus the O4 obstruction.
- Exact/near-machine numeric, Yoshida-4 symplectic (its ~10⁻¹⁰ conservation floor sits far below τ_rel, so a
  true invariant reads as a null); finite bases; autonomous invariants; guards G1/G2.
- O4 is offered to ansatz as a scope note, not asserted as a defect — §123's theorem is correct *given* its
  guards; O4 identifies a regime (rich basis, bounded data) where an additional out-of-sample guard is needed.

## Inputs & artifacts

ansatz §123 `scripts/123_emit_theorem.py` (the theorem, verified read-only, not imported) · `code/emit_reproduce.py`
(the bridge's independent implementation) · `results/emit_reproduce.json`.
