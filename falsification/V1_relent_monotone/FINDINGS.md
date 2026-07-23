# V1 — Findings: relative entropy is monotone under region inclusion (the canary is alive)

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item V1
(Tier V — validation). **Verdict: SURVIVES.** This is the canary for the entire leg-X / K1 / K3 stack: a
violation would have meant our machinery is wrong, not that a theorem is.*

## Result in one line

Across **72 measurements** — 3 excitation types × 2 nesting families × 12 region sizes — relative entropy is
**non-decreasing along every inclusion chain** with **zero violations**, is non-negative everywhere (the four
"negative" entries are **−5.9×10⁻⁵⁹**, i.e. round-off at dps = 60), and the coherent full-wedge value
**54.0289** reproduces leg X's cross-gated **54.03** to 0.00%.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **V1a** (primary) | S_rel non-decreasing along every inclusion chain | **0 violations / 72 points** | **SURVIVES** |
| **V1b** | positivity (Klein) | min value **−5.9e-59** (round-off; dps=60) | **PASS** |
| **V1c** | anchor to leg X | full-wedge coherent S_rel = **54.0289** vs 54.03 (**0.00%**) | **PASS** |
| **V1d** | saturation shape (observation) | squeezed/F1 rises 0.3393 → 1.0515, then plateaus | as expected |

## The measurements

| excitation | family | S_rel along the chain (first values … last) | monotone | positive |
|---|---|---|---|---|
| coherent (ΔS=0) | F1 (outward from cut) | 0.0000, 0.0000, 0.0000, 0.0000, 0.0027, 0.0878, … , **54.0289** | ✅ | ✅ |
| coherent (ΔS=0) | F2 (inward from far end) | 0.0000, … , **49.5302** | ✅ | ✅ |
| squeezed straddling cut (ΔS≠0) | F1 | 0.3393, 0.5317, 0.7164, 0.8650, 1.0142, 1.0439, … , **1.0515** | ✅ | ✅ |
| squeezed straddling cut (ΔS≠0) | F2 | 0.0000, … , **0.4710** | ✅ | ✅ |
| squeezed inside wedge (ΔS=0) | F1 | 0.0000, … , **17.3456** | ✅ | ✅ |
| squeezed inside wedge (ΔS=0) | F2 | −0.0000, … , **15.9010** | ✅ | ✅ |

Two nesting families were used deliberately: **F1** grows outward from the entangling cut (the physically
natural chain, the one K3 used), **F2** grows inward from the far end of the wedge — an independent chain of
inclusions that must obey the same inequality. Both do. Testing only F1 would have left the possibility that
monotonicity was an artifact of one particular geometry.

## Why this matters (the canary role)

K1's kill, K3's entropy-production curve and leg X's hinge identity all rest on the same Gaussian modular
pipeline: reduced covariances → symplectic spectra → modular form G → S_rel = Δ⟨K⟩ − ΔS. Monotonicity of
relative entropy under restriction (Uhlmann/Lindblad) is a **theorem**, so any violation would have
invalidated that pipeline and every result built on it. K3 observed monotonicity in one configuration in
passing; V1 exercises it deliberately across three physically distinct excitations — including the two cases
K1 taught us to distinguish (ΔS = 0 for coherent and for a squeeze *inside* the wedge; ΔS ≠ 0 only for a
squeeze *straddling* the cut) — and two independent nesting geometries. It holds everywhere.

The **V1c anchor** ties the canary to already-cross-gated ground: the coherent full-wedge relative entropy
reproduces leg X's 54.03, which quantum's blind twin independently confirmed. So the pipeline is not merely
self-consistent, it lands on a number two implementations agreed on.

## Honest limits (frozen in advance)

- Validation postulate, expected to survive. A "SURVIVES" is worth exactly one thing: the stack does not
  violate a theorem it must obey. It is **not** evidence for any of K1/K3's substantive claims — those stand
  or fall on their own gates.
- Toy model (harmonic chain, Gaussian states), as throughout this arc.
- Monotonicity is tested along **inclusion chains**, which is what the theorem constrains — not between
  arbitrary unrelated regions, where no inequality is implied and none was checked.

## Inputs (read-only) & artifacts

Uhlmann 1977 · Lindblad 1975 · Casini 2008 · [leg X](../../legX_entropic_hinge) (the 54.03 anchor, blind-twin
cross-gated); reuses [K1](../K1_squeezed) `k1_squeezed.py`. `code/v1_monotone.py` ·
`results/v1_monotone.json`. Interpreter: conjecture_machine `.venv` (mpmath 1.3.0).
