# Leg Z — Pre-registration: independent verification of the Jacobian-conjecture counterexample

*Frozen 2026-07-24, before `code/verify_jacobian.py` is run. Not a family postulate — an **outward
verification**, and the natural capstone to the Falsification Ledger campaign: the campaign killed eight of
our own toy postulates; here the family independently checks the biggest real postulate-kill in decades.
The **Jacobian conjecture** (open since 1939) was disproved ~2026-07-20 by an explicit degree-7 polynomial
map on ℂ³ with constant nonzero Jacobian that is nevertheless non-injective — found by L. Alpöge with Claude
Fable 5. Primary source: T. Tao, "A digestion of the Jacobian conjecture counterexample" (blog, 2026-07-21).*

## The claim under test (map transcribed from the primary source)

```
F₁ = (1+z₁z₂)³ z₃ + z₂²(1+z₁z₂)(4+3z₁z₂)
F₂ = z₂ + 3z₁(1+z₁z₂)² z₃ + 3z₁z₂²(4+3z₁z₂)
F₃ = 2z₁ − 3z₁²z₂ − z₁³z₃
```

**leg-W discipline applied.** The map is transcribed from Tao's digestion (a summarizer can mangle a
polynomial — leg W's lesson). Two guards: (a) all three collisions were **hand-verified during
transcription** before any code was written (each lands on (−¼,0,0) by exact fraction arithmetic); (b) the
verification is **self-validating** — a wrong transcription makes det ≠ −2 or breaks a collision, so a gate
failure would indicate a transcription error, *not* that the counterexample is false.

## Frozen gates

- **Z1 — constant nonzero Jacobian (the "local invertibility everywhere" condition).** The Jacobian
  determinant `det(∂Fᵢ/∂zⱼ)`, computed and expanded exactly in ℚ[z₁,z₂,z₃], must equal the constant **−2**
  identically: `expand(det − (−2)) == 0`. This is the property that made the conjecture's hypothesis hold in
  its strongest form.
- **Z2 — global non-injectivity (the conjecture's conclusion, violated).** The three points
  p₁=(0,0,−¼), p₂=(1,−³⁄₂,¹³⁄₂), p₃=(−1,³⁄₂,¹³⁄₂) are **pairwise distinct**, and
  `F(p₁)=F(p₂)=F(p₃)=(−¼,0,0)` **exactly** (rational arithmetic, no rounding). Constant-nonzero-Jacobian +
  a genuine collision = the conjecture is false in dimension 3.
- **Z3 — the stated shape.** F: ℂ³→ℂ³ (a self-map of 3-space), total degree exactly **7**.
- **Z4 — the structural lesson, logged (the reason this was worth verifying for us).** The counterexample
  is the sharpest possible instance of *"locally-invertible-everywhere ⇏ globally-invertible."* This is the
  same inference template as the localization postulate in the emergent-gravity anatomy
  (`legX_entropic_hinge`): "a check passes at every point ⟹ the global claim holds." The Jacobian
  conjecture was that template's best case (rigid polynomials, constant Jacobian) and it **failed** — an
  external, world-scale reminder that the template is never free. Recorded as commentary, not a gated
  numeric claim, and **not** a technical transfer into Jacobson's argument (no such transfer is asserted).

## Honest scope

- This **verifies** a published counterexample; it does not discover or reprove it. Value = an independent,
  exact, reproducible confirmation from the family's own instrument, days after announcement — plus the
  structural note tying it to leg X.
- Pure SymPy, exact rationals, stdlib-adjacent. No sister needed; runs entirely bridge-side.
