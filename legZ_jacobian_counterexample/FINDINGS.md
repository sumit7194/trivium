# Leg Z — Findings: the Jacobian counterexample, independently verified

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the run. The capstone of
the Falsification Ledger campaign, pointed outward: the campaign killed eight of the family's own toy
postulates; here the family independently verifies the biggest real postulate-kill in decades — the
**disproof of the Jacobian conjecture** (open since 1939), announced ~2026-07-20 (L. Alpöge with Claude
Fable 5; primary source T. Tao's digestion, 2026-07-21). Exact SymPy, no sister needed.*

## Result in one line

**Verified, exactly.** A degree-7 polynomial self-map of ℂ³ with Jacobian determinant **identically −2**
(SymPy expanded the full 3×3 determinant and it collapses to the constant −2) sends **three distinct
points** — (0,0,−¼), (1,−³⁄₂,¹³⁄₂), (−1,³⁄₂,¹³⁄₂) — to the **same image** (−¼,0,0). Constant nonzero
Jacobian (local invertibility everywhere) + a genuine collision (global non-injectivity) = **the Jacobian
conjecture is false in dimension 3**, hence in every dimension ≥ 3. The plane case remains open.

## The gates

| gate | check | result |
|---|---|---|
| Z1 | `det(∂Fᵢ/∂zⱼ)` expanded in ℚ[z₁,z₂,z₃] equals the constant −2 identically | **PASS** — expands to `-2` |
| Z2 | three points pairwise distinct; each maps to (−¼,0,0) in exact rationals | **PASS** — all three hit (−1/4, 0, 0) |
| Z3 | F: ℂ³→ℂ³, total degree 7 | **PASS** — component degrees [7, 6, 4] |

The map (transcribed from Tao's digestion, hand-verified at all three collisions before coding):
```
F₁ = (1+z₁z₂)³ z₃ + z₂²(1+z₁z₂)(4+3z₁z₂)      [degree 7]
F₂ = z₂ + 3z₁(1+z₁z₂)² z₃ + 3z₁z₂²(4+3z₁z₂)   [degree 6]
F₃ = 2z₁ − 3z₁²z₂ − z₁³z₃                      [degree 4]
```

## leg-W discipline, and why this verification is trustworthy

The single biggest risk was transcribing a polynomial from a summarized web source (exactly the leg-W
failure mode). Two independent guards held:
1. **Hand-checked before coding** — all three collisions were confirmed by exact-fraction arithmetic during
   transcription (e.g. at (1,−³⁄₂,¹³⁄₂): 1+z₁z₂ = −½, so F₁ = (−⅛)(¹³⁄₂) + (9/4)(−½)(−½) = −13/16 + 9/16 =
   −¼).
2. **Self-validating gate** — a mis-transcribed coefficient would break Z1 (det ≠ −2) or Z2 (a collision
   fails). All three gates passing is strong evidence the map is faithful *and* the counterexample is real.
   A failure would have indicated *our* transcription error, not a wrong counterexample — and there was none.

## Why the family verified this (Z4, framing — not a gated claim)

The counterexample is the sharpest possible instance of **"locally-invertible-everywhere ⇏
globally-invertible"** — a check that passes perfectly at *every point* (constant nonzero Jacobian, the
strongest local condition, on the most rigid functions there are) still fails to guarantee the *global*
conclusion. That is the **same inference template** as the localization postulate labelled ASSUMED in the
emergent-gravity anatomy ([legX_entropic_hinge](../legX_entropic_hinge/FINDINGS.md)): *"a relation holds at
every local patch ⟹ the global statement follows."* The Jacobian conjecture was that template's best case,
and last week it **failed by explicit counterexample**. This is recorded as a structural rhyme and an
external reminder that the template is never free — **not** a technical transfer into Jacobson's argument
(no such transfer exists; the localization postulate is a physics assumption, this is an algebraic fact).

Two further resonances worth noting: the counterexample was **found by a machine and understood by humans
retroactively** (Tao: it "looks like a massive miracle" in raw form) — the family's own discover→verify
pattern at the top of mathematics; and it is a **falsification**, the ledger's whole philosophy — an
87-year-old conjecture fell not to a proof but to someone hunting the counterexample.

## Honest scope

- This **verifies** a published counterexample exactly; it does not discover or reprove it. The value is an
  independent, reproducible, same-week confirmation from the family's instrument, plus the structural note.
- The plane (dim-2) case of the conjecture **remains open** — unaffected by this result.

## Inputs & artifacts

- T. Tao, "A digestion of the Jacobian conjecture counterexample" (2026-07-21); counterexample by L. Alpöge
  with Claude Fable 5. · `code/verify_jacobian.py` (exact SymPy, run via ansatz venv) ·
  `results/jacobian_verify.json`.
