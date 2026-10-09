# V10 — Pre-registration: an independent jet-prolongation bound on Killing tensors for TS δ=2

*2026-10-10, ~03:10 IST. Written and committed BEFORE any V10 code runs.*

**Purpose.** ansatz's `_kt_jet.py` (commit c126f5c) reports that for TS δ=2 at p = 4/5, the jet-prolongation upper bound
on the dimension of the space of ∂t, ∂φ-invariant Killing tensors equals the trivial count at every valence 1–10, and
at p = 3/5 for valence 8–10. That method follows Kruglikov–Matveev 2012 and Vollmer 2016. Its linear algebra was
cross-checked (FLINT against Rust), but its **matrix builder** is a single implementation. V10 is a second, fully
independent builder and solver.

**What the bridge knows of ansatz's run.** Its final bounds (r1–10 = 2, 4, 6, 9, 12, 16, 20, 25, 30, 36), its points
(1/2, 2), (3, 1/3), (5/4, 1/2) and (2, 1/5), its prime 2147483647, a few matrix sizes, and its formulation (unknown
jets to order d+1). The bridge has not read its code.

## Method: the bridge's own

**Polynomial and bracket.** F = Σ_{|α|=r} K_α(x, y) p^α in (p_t, p_φ, p_x, p_y), and
{H, F} = Σ_{q∈{x,y}} (∂H/∂p_q ∂_q F − ∂_q H ∂F/∂p_q). Each coefficient of p^β (|β| = r+1) gives a linear first-order
PDE in the K_α.

**Jet system.**
- Unknowns: the Taylor coefficients of each K_α at a point P, to order N.
- Equations: the Taylor coefficients of every PDE, to order N−1.
- Coefficients: computed exactly over GF(q), q = 2³¹ − 1, by the bridge's own truncated bivariate power-series
  arithmetic, evaluated on the metric expression tree (TS components from ansatz's sealed data files via V8's loader; ZV,
  Kerr and flat space written here).
- Elimination: the bridge's own numpy routine, not FLINT.

**Why the bound is valid.** A Killing tensor's N-jet lies in ker(E_N). The map from Killing tensors to jets is
injective for N ≥ r (a valence-r Killing tensor is determined by its r-jet). And rank_q ≤ rank_Q. So
nullity_q(E_N) ≥ dim(KT) for every N ≥ r, and we start at N = r+1.

**Built-in under-count check.** The trivial tensors p_t^a p_φ^b H^c (a+b+2c = r) always lie in the kernel, so a
nullity below the trivial count means a BUG.

## Controls, run first; any failure means STOP
1. Flat space, spherical (r, y = cos θ), at P = (2, 1/3): valence 1 bound = 3 (p_t, p_φ, p_z). This tests detection.
2. Kerr, Boyer–Lindquist (r, y), M = 1, a = 1/2, at P = (7/2, 1/3): valence 1–4 bounds 2, 5, 8, 14. This tests detection of
   Carter.
3. ZV δ=2 at P = (3/2, 1/3): valence 6 bound 16 (Kruglikov–Matveev).
4. TS p = 3/5 (`t1o2`) at P = (3/2, 1/3): valence 7 bound 20 (Vollmer Theorem 1).

## Targets
TS δ=2, p = 4/5 (`t1o3`), at P₁ = (3/2, 1/3) and P₂ = (7/4, −2/5), both inside the physical region. Valence 1–6.

## Rule
For each (valence, point), try N = r+1, r+2 and r+3, and use the smallest bound found.
- **CONFIRMED** at a valence if the bound equals the trivial count at both points.
- **NOT CONFIRMED** if the bound is above the trivial count at N = r+3. This is INCONCLUSIVE, not a positive claim: a
  prolongation bound above the floor does not show that a tensor exists.
- **STOP** on any control failure, or on any nullity below the trivial count.

Memory is self-limited to 3 GB. Single-threaded.

## Addendum, ~03:40 IST: before running, after r1–6 landed
Extend the targets to valence 7 and 8 for TS p = 4/5 at P₁ and P₂. The rule is unchanged. Trivial counts are 20 and 25.
Memory guard stays at 3 GB; r8 is about 9900 × 9075 entries.

## Addendum 2, 2026-10-10 ~02:05 IST: instrument fix, and targets valence 8–10 (before running)
*Clock correction: the "~03:10" and "~03:40" times above were the bridge's estimates. The commit timestamps are
authoritative.*

**Instrument change, memory only.** The valence-8 run was stopped by the bridge's own 3 GB guard. The elimination
copied the whole matrix several times per pivot. It now:
- stores the matrix as int32 (all entries are below Q < 2³¹);
- eliminates in place;
- updates rows in chunks of 1024, in int64.

The arithmetic is identical.

**Re-validation first.** The fixed code must reproduce, with the SAME rank, every earlier run:
- flat r1;
- Kerr r1–4;
- ZV r6;
- TS p=3/5 r7;
- TS p=4/5 r1–7 at P₁ and P₂.

Any mismatch means STOP.

**Targets:** TS p = 4/5, valence 8, 9 and 10, at P₁ and P₂, with N = r+1, then r+2 if needed. Trivial counts are 25, 30
and 36. The rule is unchanged.

**Resource guard, sized to the box and not arbitrary.** Kill if the process RSS exceeds 10 GB or system memory free
falls below 10%. Single-threaded. The valence-10 matrix is about 24024 × 22308 int32 entries (≈ 2.1 GB).
