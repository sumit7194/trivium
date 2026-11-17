# V18: the bridge's independent check of DeepStrain's METRICS errata draft (DeepStrain 5499fc6)

*2026-11-17. Sources read independently by the bridge: the arXiv HTML renderings of 2406.11986v2 (METRICS, Chung &
Yunes) and 2207.11267v2 (Pierini & Gualtieri, "PG"). DeepStrain's script and draft were not read; only its three
claims, as stated in its message. The published PRD version was not checked (paywalled).*

## E1: the GR horizon angular velocity. CONFIRMED
METRICS Eq. (25) prints Ω_H^(0) = a/(2Mb), with b = √(1 − a²) and r± = M(1 ± b) (Eq. 17). For Kerr, Ω_H = a/(r₊² + a²)
in units with M = 1. Since (1 + b)² + a² = 2(1 + b), this is a/(2M(1 + b)).
- At a = 0.69: the printed form gives 0.4766; the correct value is 0.2001.
- The neighbouring κ^(0) = b/(2M(1 + b)) is correct: 0.2099, equal to the Kerr value.

## E2: the 033 polar linear coefficient in the PG comparison, Eq. (131). CONFIRMED
Every PG-derived coefficient in METRICS Eq. (131) equals 16 × PG's C₂ coefficients:
- the constant: C₂ of r = 0;
- the linear term: m·C₂ of r = 1;
- the quadratic term: C₂ of r = 2a plus m²·C₂ of r = 2b.

8 of the 9 coefficients match exactly. The exception is the 033 linear imaginary part:
- PG Table 2 (r = 1, Im l = 3) has C₂ = +1.18e−3, so 16 × 3 × 1.18e−3 = **+0.05664**;
- METRICS prints **−0.05664 i**.

This is a sign error in the reprint. It is cosmetic for the paper's conclusions.

## E3: the printed fitting polynomials (Eqs. 125–130) and the "close to PG" statement. CONFIRMED in substance; numbers differ
- The printed degree-8 fits are shown truncated at a⁴, with alternating coefficients of O(10²–10³). The truncated
  form is unusable beyond very small spin. For 022P (Eq. 126) against the tabulated data, the bridge finds:
  - a = 0.1: 9.3% (modulus), or Re 8.7% / Im 14%;
  - a = 0.2: 431% (modulus), or Re 436% / Im 358%.

  DeepStrain quotes 16% and 383%; the definition of the error measure needs reconciling.
- The text says w₀, w₁ and w₂ are "close" to PG's slow-rotation coefficients. For 022P:
  - w₁ = −2.518 − 0.411i against PG's −0.335 + 0.0006i;
  - w₂ = 48.47 + 9.60i against PG's −0.320 + 0.304i.

  They are not close. That's expected: low-order coefficients of a high-degree least-squares fit on [0, 0.85] are not
  Taylor coefficients.

## NEW (not in the draft, as far as the bridge knows): Tables 1 and 2 appear to have swapped contents or captions
- At a = 0, "Table 1, nlm = 022" polar gives −0.8787 − 0.1150i. That matches PG's **033** value (−0.8725 − 0.1150i) and
  METRICS's own 033P fit, w₀ = −0.8728.
- "Table 2, nlm = 033" polar gives −0.2258 − 0.0753i. That matches PG's **022** value (−0.2250 − 0.0752i) and the 022P
  fit, w₀ = −0.2152.
- The axial columns show the same swap: Table 1 axial is 0.1129, against the 033A fit's 0.1097; Table 2 axial is 0.0595,
  against the 022A fit's 0.0552.
- PG's own labels check out independently: its l = 2 GR value is C₀ = 0.37367, the Kerr 022 frequency.

**Status:** an inference from the HTML rendering. It needs confirming in main.tex (DeepStrain holds the source) before
it goes into the note.
