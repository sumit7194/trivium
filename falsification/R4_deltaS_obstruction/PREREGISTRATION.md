# R4 — Pre-registration: is "non-factorization" a faithful proxy for the K1 obstruction (ΔS≠0)?

*Frozen 2026-07-24, before `code/r4_deltaS.py` is written or run. Falsification v2, Tier R — precision
hygiene on a K1 finding. K1 killed the Longo identity `S_rel = 2π·boost-energy` for cross-cut squeezes and
wrote: the identity fails "iff the excitation entangles across the cut / because coherent-state displacements
factorize (ΔS=0)." R4 asks whether **operator non-factorization** faithfully tracks the true obstruction —
which is exactly **ΔS ≠ 0** — or whether a genuinely-entangling (non-factorizing) operation can still have
ΔS = 0 (in which case "non-factorization" was sufficient-but-not-necessary language).*

## The exact statement (from K1)

For a Gaussian excitation of the vacuum, `S_rel = Δ⟨K⟩ − ΔS` (exact first law); the Longo identity
`S_rel = 2π·boost-energy = Δ⟨K⟩` holds **iff ΔS = 0**. So the true obstruction is **ΔS ≠ 0**. K1 attributed
ΔS = 0 for coherent states to displacement operators *factorizing* across the cut, and ΔS ≠ 0 for squeezes to
their *not* factorizing.

## Minimal model (frozen)

A 2-mode Gaussian toy — the conceptual minimum. Mode A (inside), mode B (outside); the **vacuum is a
two-mode squeezed state** TMS(s), s = 0.5 (its cross-cut entanglement; reduced-A symplectic eigenvalue
ν_vac = cosh 2s). Entropy of a mode with symplectic eigenvalue ν: `s_ent(ν) = h((ν+1)/2) − h((ν−1)/2)`,
h(x)=x ln x. An excitation is a Gaussian unitary (symplectic S): γ → SγSᵀ; ΔS ≡ s_ent(ν'_A) − s_ent(ν_vac),
ν'_A = √det(A-block of γ'). Operations: displacement (no covariance change), single-mode squeeze (local or in
a rotated cross-cut mode), beamsplitter BS(θ), two-mode squeeze TMS(r). **Non-factorizing** = the symplectic
is not (local_A ⊕ local_B) and not a bare mode-swap.

## Frozen gates

- **R4a — straddling ≠ entangling (the clean hygiene point).** A **cross-cut displacement** (support on both
  sides of the cut, but a displacement) has **ΔS = 0 exactly** and leaves the identity exact, while a
  **cross-cut single-mode squeeze** has **ΔS ≠ 0** and breaks it. PASS = the obstruction is ΔS, and *spatial
  straddling of the cut is not itself the obstruction* (displacements straddle yet satisfy the identity).
- **R4b — the postulate (search): does an operator-non-factorizing excitation with ΔS = 0 exist?** Scan
  genuinely-entangling 2-mode symplectics (BS(θ) × TMS(r) grid, plus rotated-mode squeezes) for **ΔS = 0**
  (|ΔS| < 1e-9) at a point that is **non-factorizing and non-trivial** (γ' ≠ γ_vac, not local, not swap).
  Two pre-registered outcomes, both clean:
  - **FOUND ⇒ postulate TRUE (K1 wording amended):** non-factorization is *sufficient but not necessary*;
    the faithful characterization is "ΔS ≠ 0," and "entangles across the cut" over-states it. The example is
    reported; K1's FINDINGS gets a one-line precision amendment.
  - **NOT FOUND (only local / swap / trivial give ΔS = 0) ⇒ postulate FALSE (K1 wording SURVIVES):** for this
    class, operator-non-factorization ⟺ ΔS ≠ 0, so K1's language was exactly faithful. Reported as SURVIVES,
    with the scan coverage stated (so "not found" carries its honest scope, not a universal claim).
- **R4c — framing.** Either way, R4 pins that the Longo-identity obstruction is **exactly ΔS ≠ 0**, and
  settles whether "non-factorization" is a faithful name for it. Precision hygiene on a banked finding — no
  new physics; 2-mode toy, not the full chain.

## Honest scope

- A **characterization** question (what obstructs the identity), on the minimal 2-mode Gaussian model, not
  the N=96 chain. The chain's K1 verdict is unaffected; R4 only sharpens the *wording* of its mechanism.
- "NOT FOUND" is scoped to the searched symplectic family (stated), never a proof of non-existence in
  general. Exact covariance arithmetic (float64 is ample here — no deep-wedge cancellation).
- Bridge-solo; reuses only the entropy formula, not K1's chain build.
