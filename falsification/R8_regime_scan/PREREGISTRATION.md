# R8 — Pre-registration: is κ's scheme-dependence a property of the QUANTITY, or of the REGIME?

*Frozen 2026-07-26, before `code/r8_regime.py` is written or run. Falsification v2+, Tier R. **This applies
[L9](../../FALSIFICATION_V2.md) — quantum's lesson, adopted the same day — to our own banked result.***

## Why this exists

**M2** killed the area-law coefficient κ as **scheme-dependent**: 0.30 / 0.41 / 0.51 across three UV
regulators, a **51% spread**. [A2](../A2_wall_audit/FINDINGS.md) filed it as a **species-3 (definitional)**
wall — "the quantity is not a quantity; report the scheme-dependence *as* the result."

**That was measured at a single point.** M2's operators are massless: the radial K has only the gradient term
and the centrifugal `ℓ(ℓ+1)/j²`. No regime was scanned.

Today quantum showed exactly that assumption failing on someone else's result: five legitimate entropic
clocks *disagree* at weak coupling (|τ| = 0.181) and *converge* once interactions dominate (|τ| = 0.990),
with a switch-on at **Λ ≈ 2–4**. Their lesson, now **L9**: *when probing definitional robustness, scan the
physical regime — the interesting answer is usually a boundary, not a yes/no.* We asked them to scan someone
else's claim. R8 turns it on ours.

## The postulate (M2/A2's implicit claim, now stated explicitly so it can fail)

**"κ's scheme-dependence is a property of the quantity, not of the regime — the across-regulator spread does
not switch off anywhere."**

## Method

Add a mass to M2's radial operator. In the Srednicki decomposition (lattice spacing a = 1, `r_j = j`) a mass
term contributes `½m²Σφ_j²`, i.e. **`K → K + m²·I`**. Regulator order frozen: **mass first, then regulator** —

- `K_bare(m) = K_bare + m²I`
- `K_impr(m) = K_impr + m²I`
- `K_hd(m)  = K_bare(m) + γ·K_bare(m)²`  (γ = 0.1, as M2)

Everything else is M2 verbatim (`entropy_from_K`, `extract_kappa`, N = 200, L0 = 500, ns = [15…40]), so the
m = 0 point *is* M2.

**The regime knob is `m·n`** — sphere radius over correlation length, the dimensionless analogue of
quantum's Λ. Scan **m ∈ {0, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0}**, spanning `m·n` from ~0.05 (deeply
conformal, where M2 ran) to ~40 (deeply gapped).

**Metric:** relative across-regulator spread `Δ(m) = (max κ − min κ) / mean κ`. At m = 0 this is M2's 51%.

## Frozen gates

- **R8a — regression.** At m = 0 the three κ must reproduce M2 (≈ 0.30 / 0.41 / 0.51, spread ≈ 51%, within
  2%). **If this fails the massive extension is untrustworthy and every later gate is void.**
- **R8b — the scan (decisive).**
  - **SURVIVES** iff `Δ(m) ≥ ½·Δ(0)` at *every* countable regime point — no switch-off; the species-3 label
    on κ is unconditional and M2 is strengthened.
  - **KILLED** iff `Δ(m) < ⅕·Δ(0)` at any countable point — the regulators *agree* in some regime, so κ's
    scheme-dependence is **regime-bounded**. M2/A2 then need the same qualifier Barontini's claim needs, and
    quantum's single observation becomes a **pattern**: definitional walls have boundaries.
  - **PARTIAL/UNDECIDED** if Δ lands between ⅕ and ½ of Δ(0), or if too few points are countable.
- **R8c — the collapse trap (pre-registered, because it is the obvious way to fool ourselves).** In the
  gapped regime entropy is suppressed and **κ → 0**. A relative spread computed on three near-zero numbers is
  noise, and a *shrinking* spread there would be an artifact, **not** scheme-independence. **A regime point
  counts only if `min κ across regulators > 0.01`**; non-countable points are reported as *not measurable*,
  never as agreement. Absolute κ values are reported at every point so any collapse is visible.

## Honest scope

- **Zero novelty.** Massive-scalar entanglement entropy on a lattice is textbook; the area law is *more*
  robust for gapped theories than critical ones. The falsifiable content is entirely about **whether our own
  banked species-3 label survives a regime scan** — a self-audit, not physics.
- **κ only.** R6's log coefficient `b` is out of scope: it was not robustly resolvable for one of the three
  regulators even at m = 0, so scanning it would compound an unresolved quantity. Stated rather than quietly
  dropped.
- The mass is added to the *radial* operator in M2's own conventions; no claim is made that this is the
  unique lattice massive scalar, and the regulator-ordering choice above is a convention frozen in advance.
- Bridge-solo; imports M2's module; numpy only.
