# V14: pre-registration of the bridge's independent replay of the chaos-proof covering relations (quantum S6)

*2026-10-16. Written before any V14 covering code exists. Quantum's R1 (Rössler) has PASSED (ce66e54), and the
bridge knows its decisions. Quantum's HH-PRIMARY is running, and the bridge has not seen its results.*

## Role
Quantum's phase-2 pre-registration (S6) requires a second implementation of every covering relation that the
horseshoe claim rests on. CAPD/MPFR is quantum's engine. V14 uses **TaylorModels.jl 0.13.1** (Julia 1.13.2,
IntervalArithmetic 1.0.12 with Float64 intervals; pinned in `julia/Manifest.toml`). It shares no code and no
arithmetic library with CAPD or MPFR.

## What V14 computes
For a t-set ("h-set") pair (M, N) and a map P (a Poincaré return, or its iterate):
- The checks of AZ 2001 Def. 2, as used in quantum's T0/B8:
  - **(b)** the image of M's left edge lies in N's left side, and the image of M's right edge lies in N's right side
    (or the reverse, with the orientation recorded);
  - **(a)** the image of M's whole support misses {|u| ≤ 1, |s| ≥ 1} in N's frame. The strong form |s| < 1 is
    recorded as data.
- The Poincaré map is built by the bridge from the validated flowpipe:
  - for each Taylor-model step, the section function is bounded over the step;
  - the crossing time is enclosed by interval root-isolation on the step's time polynomial, plus its remainder;
  - transversality (the section gradient · field excludes 0) is certified on the crossing enclosure, else that piece
    FAILS closed;
  - the image is the flowpipe evaluated on the crossing-time enclosure.
- Edges and supports are subdivided by a fixed, pre-stated ladder (8, 32, 128 pieces per edge; 4×4, 16×16, 64×64 boxes
  per support). The first level at which every piece certifies is recorded. An exhausted ladder is UNDECIDED.
- Energy-level systems (HH, Kerr, MN) need the S9 analogue: the eliminated momentum is enclosed from H = E on the
  correct branch, and every crossing enclosure must contain H = E.

## Gates (in order; each must pass before the next)
- **Q0, flowpipe sanity:**
  - the harmonic oscillator over 2π contains its exact image (done: `julia/smoke.jl`);
  - Rössler's validated flow, at 5 points, contains a high-precision (mpmath, 50-digit) non-rigorous reference at
    T = 5.
- **Q1, Rössler qualification on quantum's exact specs** (`qsim/capd/horseshoe_results/r1_*.spec`, read as inputs):
  - reproduce the 4 example coverings as CERTIFIED;
  - reproduce W1, W2 and W3 as REJECTED (certified failure, or UNDECIDED at the top of the ladder, recorded as which).
  - W2's M′⟹N must certify (quantum notes this is a genuine covering).
- **Q2, HH qualification:** the 7 (5.1) coverings on AZ 2001's published M0–M4 as CERTIFIED, and W-AZ1/W-AZ2 as
  REJECTED. Run only after quantum's HH-PRIMARY result is sealed (commit + sha256) and sent. V14's HH decisions are
  committed before the bridge reads quantum's HH JSONs.
- **Q3, MN replay (after A-K20):** every covering in quantum's MN claim.

## Comparison rule (matching quantum's MR cross-path rule)
- **FAIL** = opposite CERTIFIED decisions on any check. A FAIL is investigated, never averaged; the claim waits until
  it is resolved.
- **UNDECIDED** on one side is not a disagreement. It is reported as "overlap only".
- Margins (how far inside a side each edge image lies) are compared as data, not as a gate.

## Wording
On success, the claim's S6 line reads: "an independent implementation (TaylorModels.jl, Float64 intervals) certifies
the same covering relations". If V14 cannot certify the MN coverings within its ladder, the line reads "S6 replay
UNDECIDED (method limit)", and the fallback (CAPD in Weyl coordinates, representation-independent only) is invoked by
quantum's registered rule.

## Budget and environment
- At most 2 cores at nice 10, and no wall-clock stop rule.
- Julia and package versions are pinned; each result JSON records them.

## Disclosure (2026-10-16): partial unblinding on HH
While answering a process question, quantum told the bridge one qualitative fact about its first HH pass: on coarse
16×16 boxes, condition (b) passes and condition (a) fails, for 4 of the 7 coverings. The bridge has seen no numbers
and no per-covering decisions. V14's HH run is unaffected: it uses its own pre-stated subdivision ladder, and its
decisions are committed before the bridge reads quantum's JSONs. Quantum's registered HH run is its first pass. The
adaptive pass is a disclosed post-hoc escalation (quantum b2d1c1a).
