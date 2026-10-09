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
| P₁ = (3/2, 1/3) | 2 | 4 | 6 | 9 | 12 | **16** | 20 | not run (memory) |
| P₂ = (7/4, −2/5) | 2 | 4 | 6 | 9 | 12 | **16** | 20 | not run (memory) |
| trivial count | 2 | 4 | 6 | 9 | 12 | 16 | 20 | 25 |

Every bound was reached at N = r+1.

**Verdict: CONFIRMED at valence 1–7, at both physical points.**
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
