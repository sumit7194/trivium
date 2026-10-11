# V10 — Findings: the bridge's independent jet-prolongation bound for TS δ=2

*2026-10-10, ~03:15–03:50 IST. Pre-registration `e3b4b63`, plus the addendum for valence 7–8. The bridge's own code
(`code/v10_jet.py`), sharing nothing with ansatz's `_kt_jet.py`. Exact over GF(2³¹ − 1); numpy elimination.*

## Controls: all pass

| Control | Point | Bound found | Expected |
|---|---|---|---|
| Flat space, valence 1 | (2, 1/3) | **3** (p_t, p_φ, p_z) | 3 |
| Kerr (M = 1, a = 1/2), valence 1–4 | (7/2, 1/3) | **2, 5, 8, 14** | 2, 5, 8, 14 (Carter found) |
| ZV δ=2, valence 6 | (3/2, 1/3) | **16** | 16 (Kruglikov–Matveev) |
| TS p = 3/5, valence 7 | (3/2, 1/3) | **20** | 20 (Vollmer, Theorem 1) |

**Detection and stability.** Flat space and Kerr show that the code *detects* tensors beyond the trivial ones. The
Kerr bounds hold steady at N = r+1, r+2 and r+3. No nullity anywhere fell below the trivial count, so the
built-in under-count check found no bug.

**Metric input.** The series evaluator reproduces sympy's exact value, ∂_x and ∂_x∂_y of g_TT, g_Tφ and g_xx at the
point, for both TS parameter points.

## Targets: TS δ=2, p = 4/5

| Valence | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| P₁ = (3/2, 1/3) | 2 | 4 | 6 | 9 | 12 | **16** | 20 | 25 |
| P₂ = (7/4, −2/5) | 2 | 4 | 6 | 9 | 12 | **16** | 20 | 25 |
| trivial count | 2 | 4 | 6 | 9 | 12 | 16 | 20 | 25 |

Every bound was reached at N = r+1.

**Verdict: CONFIRMED at valence 1–7, at both physical points** (extended to 1–10 in the Addendum 2 results below).
- There is no ∂t, ∂φ-invariant Killing tensor beyond the trivial p_t^a p_φ^b H^c, up to valence 7. This is
  ansatz-free and local near each point.
- It independently reproduces ansatz's jet result for p = 4/5 at r1–7, with a different builder, solver, points and code.
- **Valence 8:** stopped by the bridge's own 3 GB guard (the elimination makes copies). No verdict. ansatz's FLINT
  run covers r8–10.

## Scope, which travels with the verdict
- Invariant tensors only. This is the class Liouville integrability needs, since a fourth integral must commute with
  p_t and p_φ.
- Local near the evaluation points, which are inside the physical region.
- These are polynomial (Killing-tensor) integrals. It complements, and does not replace, the Morales–Ramis result for
  meromorphic integrals.
- Non-blind: the bridge knew ansatz's final bounds.
- AI checking AI. No human has checked it.

## Addendum 2 results (2026-10-10): valence 8–10, after the memory-only instrument fix

**Re-validation PASS.** The fixed solver (int32, in place, chunked) reproduces the rank of all 21 earlier runs exactly:
flat r1, Kerr r1–4, ZV r6, TS p=3/5 r7, and TS p=4/5 r1–7 at both points.

| Valence | P₁ = (3/2, 1/3) | P₂ = (7/4, −2/5) | trivial | matrix | rank time |
|---|---|---|---|---|---|
| 8 | 25 | 25 | 25 | 9900 × 9075 | ~90 s |
| 9 | 30 | 30 | 30 | 15730 × 14520 | ~5 min |
| 10 | 36 | 36 | 36 | 24024 × 22308 | ~24 min |

All at N = r+1. **The verdict now reads CONFIRMED at valence 1–10, at both physical points.**

- TS δ=2 at p = 4/5 has no ∂t, ∂φ-invariant Killing tensor beyond p_t^a p_φ^b H^c, up to valence 10.
- Two fully independent implementations agree over the whole range: ansatz's `_kt_jet.py` (FLINT and Rust) and the
  bridge's V10 (numpy).
- At valence 6 a third, global method agrees: ansatz's B1, sampled and dense, in its box.

**Instrument log.** The first valence-8 attempt was stopped by the bridge's own 3 GB guard. That was an arbitrary cap
on an elimination that copied the whole matrix several times per pivot. It was fixed rather than accepted. The guard
is now sized to the box (kill only above 10 GB RSS or below 10% memory free), and the runs were coordinated with ansatz.

## Addendum 3 results (2026-10-10): TS p = 3/5, valence 8–10, beyond Vollmer's 7

| Valence | P₁ = (3/2, 1/3) | P₂ = (7/4, −2/5) | trivial |
|---|---|---|---|
| 8 | 25 | 25 | 25 |
| 9 | 30 | 30 | 30 |
| 10 | 36 | 36 | 36 |

All at N = r+1. **CONFIRMED.**
- At Vollmer's own parameter point there is no ∂t, ∂φ-invariant Killing tensor beyond the trivial ones, up to valence 10.
  That extends his theorem (valence ≤ 7) by three valences.
- Two independent implementations agree: ansatz's `_kt_jet.py` and the bridge's V10.
- Same scope as above: invariant, local, polynomial integrals. No human has checked it.

## Addendum 4 results (2026-10-11): V10-MN, the bridge's independent jet bound for Manko–Novikov

**Gates (commit 47e6a3c): PASS.**
- **Kerr limit** (β = 0, P_A): 2, 5, 8, 14 at valence 1–4. These are the expected Kerr values, Carter included.
- **Series identities:** 82/82 exp/√ nodes are exact at both points for both parameter sets, with 0 failures.
- **Draw independence:** never triggered, because no bound came out above trivial. Every row uses the single
  pre-registered draw t = 1056243203 (seed 20261011).

**Targets:** p1 = (M, a, β) = (5, 3, 1/5) and p2 = (13, 5, −1/3), at P_A = (3/2, 1/3) and P_B = (2, −1/4). All at
N = r+1. 40 rows in `results/v10_mn_runs.jsonl` (raw logs in `results/v10_mn_p{1,2}.log`).
Exp exponent lcm N_exp: 69 206 436 005 (p1) and 41 523 861 603 (p2).

| Valence | p1 @ P_A | p1 @ P_B | p2 @ P_A | p2 @ P_B | trivial | matrix |
|---|---|---|---|---|---|---|
| 1 | 2 | 2 | 2 | 2 | 2 | 30 × 24 |
| 2 | 4 | 4 | 4 | 4 | 4 | 120 × 100 |
| 3 | 6 | 6 | 6 | 6 | 6 | 350 × 300 |
| 4 | 9 | 9 | 9 | 9 | 9 | 840 × 735 |
| 5 | 12 | 12 | 12 | 12 | 12 | 1764 × 1568 |
| 6 | 16 | 16 | 16 | 16 | 16 | 3360 × 3024 |
| 7 | 20 | 20 | 20 | 20 | 20 | 5940 × 5400 |
| 8 | 25 | 25 | 25 | 25 | 25 | 9900 × 9075 |
| 9 | 30 | 30 | 30 | 30 | 30 | 15730 × 14520 |
| 10 | 36 | 36 | 36 | 36 | 36 | 24024 × 22308 |

**Verdict: CONFIRMED at valence 1–10.**
- Manko–Novikov at both parameter sets has no ∂t, ∂φ-invariant Killing tensor beyond p_t^a p_φ^b H^c, up to valence 10.
- This independently reproduces ansatz §151. It's non-blind as to the headline but independent in code, metric
  transcription, exp/√ handling, points and draw. The MN claim (ledger B3) now rests on two implementations.
- The bound can only be over-stated (Q(T) specialisation; see addendum 4). A trivial bound is therefore conclusive
  for the stated scope.

**Scope:** invariant, local, polynomial-in-momenta integrals near the two points, and generic-point rank (Zariski-open).
It says nothing about non-polynomial or non-invariant integrals; Morales–Ramis (V9) covers meromorphic ones. No human
has checked it.

**Environment (back-filled 2026-10-11, per the fleet reproducibility policy):** CPython 3.14.5,
`/Users/sumit/Github/conjecture_machine/.venv`; numpy 2.4.6 (Accelerate), scipy 1.18.0, sympy 1.14.0, mpmath 1.3.0,
numba 0.65.1; macOS 26.5 arm64. Pinned in `ENVIRONMENT/` (bridge_env.json, bridge_requirements.lock). Assumed
unchanged since the run; the venv was not upgraded in between.
