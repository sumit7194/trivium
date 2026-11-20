# V24 FINDINGS: Fable's capture-edge foundations (flat-plane reduction R; inequalities I1, I2)

*2026-11-20. Pre-registration 26aec7e; amendment A1 (post-result, implementation only). Code: the Bridge's own TS2
metric (V11 loader, ts45), sympy, and mpmath interval arithmetic with recursive bisection. Nothing from Fable's
checks/.*

| check | result |
|---|---|
| **R1** conformal flatness g_xx(x² − 1) = g_yy(1 − y²), plus the identity H = F⁻¹[½(p_u² + p_v²) + ½F(W + 1)] − ½ | **PASS, exact** (both cancel to 0) |
| **I1** ∂V/∂x > 0 on {V ≤ 0} ∩ 1.5 ≤ x ≤ 9.49 | **PASS**: 0 undecided, 0 violations (2067 boxes registered; 71 after A1). Float sample: min 0.0075 on 16,099 Hill points |
| **I2** ∂V/∂(y²) > 0 on {V ≤ 0} ∩ 9.3 ≤ x ≤ 77.1 | Registered: **INCONCLUSIVE** (11,165 undecided, all at y² ≥ 0.99988, the axis; 0 violations). Diagnosed: the (s − 1) factors in the denominators straddle 0 in interval arithmetic. After **A1** (removing factors of known sign exactly): **PASS**, decided on the first box. ∂V/∂s's numerator is positive on the whole box (float sample: min ∂V/∂s = 11.7 over 20,000 points of the full box, not only Hill's region) |
| NEG-I1 (extended to 9.6) | **FIRES**: 1230 proven-wrong-sign boxes near x ≈ 9.599 (Fable's ridge is 9.4995) |
| NEG-I2 (reversed sign) | **FIRES**: 39,738 proven violations |

**Verdict:**
- R1 CONFIRMED; I1 CONFIRMED.
- I2: registered INCONCLUSIVE (an implementation limit), CONFIRMED after A1 (a post-result fix to the implementation;
  no domain or rule change).
- The checker can see failures: both negative controls fired.

**What this establishes:** the flat-plane form, the funnel (Lemma F) and the alternating-returns inequality behind
Lemma R / L2′ are now independently confirmed, by interval arithmetic with the Bridge's own metric. Calling it a
*proof* would also need an audited interval library (mpmath.iv is not formally verified) and the exact rational
coefficients, which are used here.

**Not covered yet:**
- I3 (the convexity condition, which needs a validated γ);
- Lemmas G, Q, E and L3′;
- the hole lemma;
- the lobe conditions T, C1 and C2;
- Fable's R3 redesign (the separatrix map).

Environment: Python 3.14.5 (conjecture_machine .venv), sympy 1.14.0, mpmath 1.3.0, macOS 27.2.
