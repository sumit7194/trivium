# R8 — Findings: κ's scheme-dependence SURVIVES the regime scan — and strengthens where the theory gaps

*Run 2026-07-26; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2+,
Tier R. **This applies [L9](../../FALSIFICATION_V2.md) — quantum's lesson, adopted the same afternoon — to
our own banked result**, after quantum showed the same assumption failing on Barontini's.*

## Result in one line

**SURVIVES.** The across-regulator spread of κ is **51.2% at m = 0 and never falls below it** — it *rises*
to **67.4%** in the deeply gapped regime. M2's kill is strengthened and A2's **species-3 label on κ is
unconditional**. But the scan did find a boundary, just not the one we went looking for.

## The scan

| m | m·n range | κ bare | κ improved | κ higher-deriv | **spread Δ** | countable? |
|---|---|---|---|---|---|---|
| 0.000 | 0.00 | 0.3014 | 0.4139 | 0.5107 | **51.2%** | yes |
| 0.003 | 0.04–0.12 | 0.3014 | 0.4132 | 0.5107 | 51.2% | yes |
| 0.010 | 0.15–0.40 | 0.3013 | 0.4131 | 0.5106 | 51.2% | yes |
| 0.030 | 0.45–1.20 | 0.3008 | 0.4126 | 0.5100 | 51.3% | yes |
| 0.100 | 1.50–4.00 | 0.2967 | 0.4082 | 0.5056 | 51.8% | yes |
| 0.300 | 4.50–12.00 | 0.2750 | 0.3844 | 0.4817 | 54.3% | yes |
| 1.000 | 15.00–40.00 | 0.1839 | 0.2758 | 0.3704 | **67.4%** | yes |

| gate | result |
|---|---|
| **R8a** — reproduce M2 at m=0 | **PASS** — max deviation **0.62%** from M2's 0.2998/0.4113/0.5104 |
| **R8b** — the scan | **SURVIVES** — min countable Δ = 51.2%, far above the ½Δ(0) = 25.6% bar; kill bar was 10.2% |
| **R8c** — collapse trap | **did not fire** — min κ over the whole scan = 0.184 ≫ the 0.01 floor |

## The boundary that does exist, and which way it points

Δ is **flat at 51.2–51.3% while `m·n ≲ 1`** (the conformal regime, where M2 ran) and **starts rising exactly
once `m·n ≳ 1`** — 51.8% → 54.3% → 67.4%. So there *is* a regime boundary at `m·n ≈ 1`, which is precisely
the analogue of quantum's Λ ≈ 2–4 switch-on. **It just points the other way: the scheme-dependence
strengthens rather than switching off.**

The mechanism is straightforward and worth stating, since it makes the direction predictable rather than
lucky. As the mass grows, the correlation length `ξ = 1/m` shrinks below the sphere radius; correlations
across the boundary become ever shorter-ranged, so the entanglement entropy is sourced from ever-smaller
distances near the surface. **A more UV-dominated quantity is a more regulator-sensitive one.** All three κ
fall together (0.30→0.18, 0.41→0.28, 0.51→0.37 — entropy suppressed by the gap, as expected), while their
*relative* disagreement widens.

## What this does to the taxonomy — the actually useful conclusion

quantum found a definitional wall **with** a boundary: entropic time is the experimenter's choice at weak
coupling and a property of the system once interactions dominate. We went looking for the same shape in κ
and **did not find it**.

> **Definitional walls are not uniformly regime-bounded.** Some switch off (quantum's entropic time); some
> are unconditional and even sharpen (κ). "Species-3" is therefore a label that must be **checked per case
> and per regime**, not inferred from one instance either way.

This matters because the tempting generalisation after quantum's result — *"definitional walls always have
boundaries, we just haven't found them"* — is now **falsified by a counterexample from our own repo**. L9's
prescription (*scan the regime*) stands and is vindicated; the conclusion one might have drawn from a single
scan does not. A2's amended table is updated accordingly: the caveat on species-3 reads "check the regime,"
not "expect a boundary."

## Honest scope

- **Zero novelty.** Massive-scalar entanglement entropy on a lattice is textbook, and the area law is more
  robust for gapped theories than critical ones. The falsifiable content was entirely whether **our own
  banked species-3 label** survives a regime scan. It does.
- **κ only.** R6's log coefficient `b` was deliberately out of scope — it was not robustly resolvable for
  one of the three regulators even at m = 0, so scanning it would compound an unresolved quantity. Stated in
  the pre-registration, not dropped quietly.
- **The collapse trap did not fire, but it was heading toward firing.** κ falls monotonically with mass
  (0.30 → 0.18 for the bare regulator); at `m ≳ 3` the floor would be reached and those points would be
  reported *not measurable* rather than as agreement. The scan stops before that regime, so no point in this
  table is doing that kind of work.
- The mass is added to M2's radial operator in M2's own conventions (`K → K + m²I`, mass first then
  regulator, a frozen ordering); no claim that this is the unique lattice massive scalar.
- Bridge-solo; imports M2's module unchanged, so the m = 0 row **is** M2 (reproduced to 0.62%); numpy only.

## Inputs & artifacts

`code/r8_regime.py` · `results/r8_regime.json`. Strengthens [M2](../M2_arealaw/FINDINGS.md); amends
[A2](../A2_wall_audit/FINDINGS.md)'s species-3 caveat. Applies L9, contributed by quantum in Round-11.
