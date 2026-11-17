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

## RETRACTED (2026-11-17, same evening): "Tables 1 and 2 appear swapped" was the bridge's misreading
In the arXiv HTML, each table's caption sits after its data (in main.tex the \caption and \label come after the
tabular, as DeepStrain checked). The bridge paired each caption with the following table's data, which produced
the apparent offset.

Re-checked independently from the HTML: the data block that ends just before the caption "Table 1 (022)" starts at
a = 0.005 with polar −0.22664 − 0.07525i. That equals the 022P fit evaluated at a = 0.005 (−0.22663 − 0.07523i) and
PG's 022 value. **There is no swap, and no fourth erratum.**

**E3 numbers, corrected.** The bridge's first numbers were measured against the 021 table by the same misreading.
Against the true 022 table, the bridge gets:
- a = 0.1: 15.7% (modulus);
- a = 0.2: 382.5% (modulus).

The Re/Im split is in the runs below. These agree with DeepStrain's 16% and 383% (|ω_fit − ω_table| / |ω_table|).
E3 stands as DeepStrain stated it.

**Lesson recorded:** in arXiv HTML text extraction, the caption comes after the data, so pair tables by \label in the
tex, or by the caption's position, before reading values.
