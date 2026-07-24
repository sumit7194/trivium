# R4 — Findings: the K1 obstruction is exactly ΔS≠0 — "non-factorization" is sufficient but not necessary

*Run 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before code. Falsification v2,
Tier R — precision hygiene on a K1 finding. K1 killed the Longo identity `S_rel = 2π·boost-energy` for
cross-cut squeezes and attributed it to *non-factorization* of the operation across the cut. R4 asks whether
non-factorization faithfully names the obstruction. **It does not: the faithful obstruction is exactly
ΔS ≠ 0**, and a genuinely-entangling (non-factorizing) operation can have ΔS = 0.*

## Result in one line

**Postulate TRUE.** A non-factorizing, genuinely-entangling 2-mode operation **BS(π/6)·TMS(r\*=0.2951)** has
**ΔS = 0 exactly** (root-found): the beamsplitter *disentangles* (ΔS<0, a 50:50 BS purifies mode A), the
two-mode squeeze *entangles* (ΔS>0), and at r\* they cancel — while the operation genuinely couples A↔B. So
**non-factorization is sufficient but not necessary**; the identity fails **iff ΔS ≠ 0**, full stop. And R4a
confirms the complementary point: a cross-cut **displacement** *straddles* the cut yet has ΔS = 0 — so
spatial straddling is not the obstruction either.

## The gates

| gate | check | result |
|---|---|---|
| R4a | obstruction is ΔS, not straddling | cross-cut displacement ΔS = **0** (straddles, identity holds); cross-cut squeeze ΔS = **−0.488** (entangles, identity fails) — **PASS** |
| R4b | ∃ non-factorizing ΔS=0 op? | **FOUND** by root-find: BS(π/6)·TMS(0.2951), ΔS = 0 (bracketed −0.375 → +3.261), non-factorizing ✓, γ≠γ_vac ✓ — **postulate TRUE** |

## The mechanism

In the 2-mode toy (vacuum = TMS(s=0.5), reduced-A symplectic eigenvalue ν_vac = cosh 1 = 1.543):
- **Beamsplitter BS(θ) disentangles.** Direct computation: ν_A(θ) = √(cosh²2s − sin²2θ·sinh²2s) ≤ ν_vac,
  minimal (=1, mode A *pure*) at θ=π/4. So BS alone gives ΔS < 0.
- **Two-mode squeeze TMS(r) entangles.** ΔS > 0, growing with |r|.
- **They cancel.** At fixed θ=π/6, ΔS(BS(θ)·TMS(r)) runs from −0.375 (r=0) to +3.261 (r=2); bisection finds
  the crossing at **r\* = 0.295096**. The op there entangles A↔B (nonzero off-diagonal symplectic blocks)
  yet restores the vacuum's reduced-A entropy exactly.

Because the identity is `S_rel = Δ⟨K⟩ − ΔS` and holds iff ΔS = 0, this operation — though non-factorizing —
**satisfies the Longo identity**. Non-factorization is therefore *not* the faithful criterion.

## The instrument lesson (a G7-flavored self-catch)

My first R4b pass was a **60×60 grid scan**, which reported **NOT FOUND** (closest |ΔS| = 1×10⁻⁴) and would
have wrongly concluded "K1 wording SURVIVES." That was a **grid-resolution false-negative**: the ΔS = 0 set
is **codimension 1** (one equation), so a finite sample almost never lands on it — the near-miss 1e-4 was the
tell. **Root-finding is the correct instrument for a zero set; sampling is not.** Switching to bisection
found the exact zero and flipped the verdict. This is the same family of lesson as R2's constant-column and
R3's exponent-window — the *wall* ("no zero exists") was an artifact of the wrong instrument (feeds **G7**),
and it is logged rather than hidden.

## Consequence for K1 (the pre-registered amendment)

K1's FINDINGS gets a one-line precision note (added today): the Longo identity fails **iff ΔS ≠ 0**;
"non-factorization" / "entangles across the cut" is *sufficient but not necessary* — a non-factorizing
operation that entangles and then disentangles by the right amount (BS·TMS at r\*) has ΔS = 0 and satisfies
the identity. **K1's chain verdict is unaffected**: the cross-cut *squeezes* it tested genuinely have ΔS ≠ 0,
so the kill stands; only the *characterization* of the obstruction is sharpened from "non-factorization" to
"ΔS ≠ 0."

## Honest scope

- A **characterization** result on the minimal 2-mode Gaussian model — what obstructs the identity — not new
  physics and not a change to K1's chain verdict.
- The example is one explicit non-factorizing ΔS=0 operation (existence, which is all "sufficient-but-not-
  necessary" requires); the full ΔS=0 set in Sp(4,ℝ) is 9-dimensional, so such operations are generic, not
  fine-tuned coincidences — the BS·TMS root is simply the cleanest witness.
- Exact covariance arithmetic (float64 ample; no deep-wedge cancellation here). Bridge-solo.

## Inputs & artifacts

`code/r4_deltaS.py` (2-mode Gaussian toy, root-find) · `results/r4_deltaS.json`. Sharpens
`K1_squeezed/FINDINGS.md` (amended). No sister.
