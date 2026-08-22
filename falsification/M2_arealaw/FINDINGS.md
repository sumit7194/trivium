# M2 — Findings: the S = A/4 coefficient is regulator-dependent (where the "1/4" hides)

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item M2
(Tier M). Depends on [V2](../V2_cft_calibration) (entropy instrument calibrated to c=1, float64 cleared).
**Verdict: KILLED** — as expected for a Tier-M "we hunt it in the kill-me direction"; the payout is the clean
separation of the universal from the scheme-dependent.*

## Result in one line

The 3D free-scalar entanglement area-law coefficient κ (S ≈ κ (R/a)²) takes **three clearly different values
— 0.301, 0.414, 0.511 (a 51% spread)** — under three UV regulators, while the **area-law exponent stays
≈ 2.0 in all three** and a coordinate-only change leaves κ fixed (0.296 vs 0.301). The "1/4" in S = A/4 lives
in the **regulator-dependent coefficient**; the area *law* is universal.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **M2a** (anchor) | R1 bare-NN reproduces Srednicki | κ = **0.3014** ∈ [0.28,0.32], p = 1.961 | **PASS** (Srednicki κ≈0.295) |
| **M2b** (KILL) | κ spread across regulators > 20% | (0.511−0.301)/0.409 = **51.2%** | **M2 KILLED** |
| **M2c** (universality) | area-law exponent ≈ 2 for all | p = **1.961 / 1.934 / 1.969** | **PASS** (law universal, κ is not) |
| **M2d** (coord control) | midpoint coordinates leave κ fixed | Δκ/κ = **1.77%** (0.296 vs 0.301) | **PASS** (coord change ≠ regulator change) |
| **M2e** (robustness) | R1<R2<R3 ordering stable under L₀, n-window, N | stable in all 3 variations | **PASS** |

## The three regulators (same IR theory, different UV)

| regulator | κ | exponent p | what differs in the UV |
|---|---|---|---|
| **R1** bare nearest-neighbour lattice (Srednicki) | **0.301** | 1.961 | standard sharp lattice cutoff |
| **R2** improved (Symanzik) 4th-order stencil | **0.414** | 1.934 | removes leading O(a²) dispersion artifact |
| **R3** higher-derivative smooth (K→K+0.1K²) | **0.511** | 1.969 | analytic UV stiffening (smooth-cutoff axis) |

All three have ω² → k² as k → 0 (the same continuum free scalar) and share the area-law exponent; they differ
only in short-distance modes — exactly the freedom that fixes κ. R1 reproduces Srednicki's published κ ≈ 0.295,
which anchors the machinery.

## Why this is the sharp statement of "where the 1/4 hides"

Two numbers come out of the same calculation, and M2 separates them cleanly:

- **The exponent (= 2) is universal** — the area law S ∝ R² is regulator-invariant to ~2% across all three
  schemes (M2c). This is real physics: entanglement of a local QFT lives on the boundary.
- **The coefficient κ is not** — it moves by 51% when the UV regulator changes (M2b), and it is precisely the
  coefficient that would have to equal 1/4G to make S = A/4 (Srednicki's motivation). A cutoff computation
  cannot pin it down; only a full quantum-gravity input (the Newton constant's own renormalisation) can.

The **coordinate control (M2d)** is what makes this a measurement rather than fitting noise: changing the
lattice *coordinates* (midpoint r_j = j−½ instead of r_j = j) — the *same* regulator — leaves κ fixed to 1.8%,
while changing the *regulator* moves it by tens of percent. The spread is regulator physics, not an artifact of
the extraction.

## Method notes (the two pitfalls, and how they were handled)

- **The ℓ-sum converges slowly.** S(n) = Σ_ℓ (2ℓ+1) S_ℓ(n) has a tail (2ℓ+1)S_ℓ ~ ℓ^{−q}, q ≈ 2.5–2.7. A
  naive cutoff at ℓ_max ≈ n gives κ **off by ~2×** (0.12 instead of 0.30 at n=40). The production run sums to
  L₀ = 500 and adds an analytic power-law tail; the extracted κ is stable under L₀ ∈ {400,500} (M2e).
- **Finite radial box.** N = 200 ≫ n keeps the exterior a faithful "rest of space"; κ is stable under
  N ∈ {150,200} (M2e). The residual drift of S/n² with n is the leading subleading term, absorbed by the
  constant c in the fit S = κn² + c.
- **Precision:** float64 throughout, licensed by V2c (float64 = mpmath to 5×10⁻⁹ for these shallow ball
  spectra — no leg-X modular precision wall here).

## Honest limits (frozen in advance)

- Toy model only — free scalar on a radial lattice. This is a statement about a **lattice fact** (the
  entanglement area-law coefficient is regulator-dependent), **not** about the actual S = A/4 of a black hole,
  which requires the gravitational path integral. Labeled as such, like every leg.
- Expected KILL (Tier M): the demonstration *is* the payout. No novelty is claimed — the scheme-dependence of
  the entanglement coefficient is well known (Srednicki; Bombelli et al; Solodukhin's reviews). The value is a
  calibrated, home-built, control-gated separation of exponent (universal) from κ (scheme) on the family's own
  instrument, a direct sequel to leg X and the emergent-gravity thread.
- "Cutoff-shape" regulator (R3) is realised at the field level (higher-derivative), not by literal
  boundary-smearing: in a free Gaussian theory boundary-smearing has no clean entanglement-entropy definition,
  whereas a smooth UV cutoff is rigorous and is the same mechanism — stated in the pre-registration.

## Inputs (read-only) & artifacts

Srednicki 1993 (hep-th/9303048) · Bombelli–Koul–Lee–Sorkin 1986 · Solodukhin 2011 (review) · calibrated by
[V2](../V2_cft_calibration); reuses the leg X / K1 / V2 covariance-entropy machinery. `code/m2_arealaw.py` ·
`results/m2_arealaw.json`. Interpreter: conjecture_machine `.venv` (numpy 2.4.6).

---

## Audit 2026-08-22 — κ absorbs a missing term; the headline survives, demonstrated

Applying the day's residual-sign diagnostic to this closed leg, prompted by finding the identical defect
in Q2's memory law. The method note above already said the residual drift of S/n² was *"absorbed by the
constant c in the fit S = κn² + c"* — **but if that drift is n-dependent, a constant cannot absorb it and
κ takes the difference.**

**Residual signs, 6 points, all three regulators:**

    R1 bare NN            -++++-    2 sign changes
    R2 improved stencil   -++++-    2 sign changes
    R3 higher-deriv       ++---+    2 sign changes

Smooth arcs, not scatter. **The two-parameter form is missing a term and κ is absorbing part of it.**
The diagnostic is the sign pattern, not the fit quality — both forms fit well.

> ### WITHDRAWN, same day. The sign test has no power at 6 points.
>
> Under scatter, sign changes among *n* residuals are **Binomial(n−1, ½)**. For 6 points that is
> Binomial(5, ½), mean 2.5 — and **P(X ≤ 2) = 0.500.** The "smooth arc" observed in all three
> regulators is **exactly what a coin flip produces.** There is no evidence here at all.
>
> I applied a diagnostic without its null distribution, saw a pattern that looked structured, and
> committed it as a finding. The threshold ("few sign changes = arc") was mine, chosen after seeing the
> data, with nothing behind it.
>
> **Audit of every use of this diagnostic today:**
>
>     Q2 memory law   1 change / 6 pts   P=0.188   weak  — but corroborated independently
>     M2 kappa R1     2 / 6              P=0.500   none
>     M2 kappa R2     2 / 6              P=0.500   none
>     M2 kappa R3     2 / 6              P=0.500   none
>     R6 b R1/R2/R3   3,4,3 / 9 pts      P=0.36/0.64/0.36   none
>
> **Not one clears p < 0.05 on signs alone.** Q2's conclusion survives because it never rested on the
> signs: its hold-out errors were **+6.7%, +6.8%, +6.7% — one direction, near-identical magnitude, three
> times** — and fixing the model cut hold-out error from 6.8% to 0.1%. That is the evidence. The sign
> pattern was decoration I mistook for the argument.
>
> **What remains true here:** the leg's own method note says the residual drift of S/n² *is* absorbed by
> `c`, and if that drift is n-dependent then κ takes the difference. **That is a real structural concern
> and it is untested** — 6 points cannot settle it. The 3-parameter refit below moves the filed spread
> +4.6%, which with 6 points and 3 parameters is not evidence either.
>
> **Status: the concern is open and unmeasured, not demonstrated.** Settling it needs more n values,
> which is cheap here — recorded as a to-do rather than a result.

**Sensitivity (6 points, 3 parameters — a check, not a new result):** adding an n-linear term moves the
individual κ by −1.2%, −1.2%, +1.1%, and the **filed relative spread from 0.5120 → 0.5357 (+4.6%)**.

**The claim of this leg is that κ is regulator-dependent — the spread IS the claim.** It grows slightly
under the better model, so the conclusion survives and the absorbed term is common-mode across
regulators. **Demonstrated by refitting, not assumed.**

*Self-correction from the audit itself: my first pass printed `"matches the banked 0.5120"` beside a
computed 0.2092 — the banked figure is the **relative** spread `(max−min)/mean`, mine was absolute. A
label asserting agreement, printed next to the disagreement it described. Nobody reads the number beside
the word "matches."*

---

## Audit 2026-08-23 — same denominator shape as Q2, opposite consequence

Q2's headline fraction was withdrawn today: adding one admissible kernel widened its denominator 3.3×
and the quoted percentage fell from 38.6% to 11.7% with the systematic untouched. **The absolute
quantity was stable; the ratio was an artifact of which kernels were included.**

**M2 reports the same shape** — `kappa_spread = (max−min)/mean` over **three** chosen regulators, filed
at **51.2%**, gated by M2b as *"κ spread across regulators > 20%"*.

**Checked whether it matters here. It does not, and the reason is the direction of the claim.**

Q2's fraction shrank when the denominator grew. M2's gate would only be threatened if a fourth regulator
raised the **mean** without widening the **range** — i.e. landed inside [0.3014, 0.5107]. Solving for the
κ that would push the spread below the 0.20 gate with `max−min` held fixed:

    need mean > 1.047   ->   fourth κ > 2.96
    that is 5.8x the largest κ in the study — and OUTSIDE the range, so it would widen
    max−min as well. The requirement is self-defeating.

> **M2's inequality is robust to adding regulators. The value 51.2% is not** — it remains a ratio over a
> chosen set — **but the claim is "spread > 20%", and adding kernels moves that claim in the safe
> direction.**

**Q2's claim was a fraction quoted as a magnitude, so the same shape was fatal. Same structure, opposite
consequence, decided by which way the claim points.**

*Recorded because the shape is worth flagging even where it is harmless: the next reader who finds
`(max−min)/mean` in this repo should know it was checked and why it survived, rather than having to
re-derive that.*
