# M4 — Findings: what it takes to make hidden geometry audible

*Run 2026-07-23; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item M4
(Tier M), second postulate off the [K2](../K2_isospectral_drums) drums build. **Verdict: KILLED as literally
stated — but the postulate's substance survives**, and that split is the finding.*

## Result in one line

A **uniform** coupling V = c leaves the two Gordon–Webb–Wolpert drums **indistinguishable** (split ~10⁻¹⁵) —
so "distinguishable at ANY nonzero coupling" is false — while **every** spatially-varying coupling tested
splits the degeneracy by 10⁻³–10⁻², **linearly** in coupling strength (p = 0.998, 1.000). Hidden geometry
becomes audible precisely when the probe can tell points apart; a globally uniform probe stays deaf.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **M4a** (KILL) | uniform V=c leaves spectra identical | **6e-15 / 8.8e-15 / 9.4e-15** at c=1/5/50 | **"ANY" is FALSE → M4 KILLED** |
| **M4b** | every spatially-varying coupling splits | ramp 9.2e-3, bump 4.0e-3, radial 2.0e-2, tile-local 8.3e-3 | **PASS** (fragility confirmed) |
| **M4c** | splitting linear in strength, p ∈ [0.9,1.1] | **p = 0.9978** (ramp), **1.0000** (bump) | **PASS** — genuine first-order effect |
| **M4d** | tile-locality is not protection | tile-local splits 8.3e-3 | **PASS** |
| **M4e** | control + resolution stability | control 1.5e-14 (n=32), 7.2e-15 (n=64); splits agree <1% | **PASS** |

## The two halves of the verdict (both reported, neither dressed up)

**The literal postulate dies to a trivial counterexample.** H = −∇² + cI shifts every eigenvalue by the same
c, so a constant coupling — which *is* a nonzero coupling — preserves isospectrality exactly. The word "ANY"
is simply too strong. This is not a deep failure; it is a boundary condition on how the claim may be stated.

**The substance survives, emphatically.** Every coupling that varies in space breaks the degeneracy:

```
  linear ramp   V = α·x                     split = 9.18e-03
  gaussian bump V = α·exp(−|r−r₀|²/0.2)     split = 3.98e-03
  radial well   V = α·|r−r₀|²               split = 1.96e-02
  tile-local    V = α·(frac x + frac y)     split = 8.28e-03      (α = 1, n = 32)
```

against an isospectral floor of ~10⁻¹⁵ — twelve orders of magnitude. The degeneracy is measure-zero fragile
exactly as the postulate intended.

## Why the splitting is first-order (M4c)

Fitting split(α) ∝ α^p over α ∈ {0.01, 0.03, 0.1, 0.3} gives **p = 0.9978** (ramp) and **p = 1.0000** (bump)
— textbook Rayleigh–Schrödinger. The two drums' eigenfunctions weight the potential differently at first
order, so ⟨ψ|V|ψ⟩ differs immediately. The degeneracy is not protected by any symmetry that survives a
position-dependent perturbation; it is an *accidental* (transplantation) degeneracy of the pure Laplacian.

## The protection mechanism (M4d — what the kill teaches)

The natural guess is that a coupling respecting the drums' tile structure would be protected by the same
transplantation that makes them isospectral. **It is not:** the tile-local potential splits as strongly as a
generic one (8.3e-3). The reason is structural — transplantation does not merely permute the 7 tiles, it maps
each output tile to a *signed linear combination* of rotated/reflected input tiles. For a multiplication
operator to commute with that mixing it must act as the same scalar on all the mixed pieces, which forces it
to be **constant**. So the protected class is exactly the trivial one, and the bracket is sharp:

> **uniform ⇒ deaf · anything that distinguishes points in space ⇒ audible.**

That is the answer to the ledger's question for this arc — *what does it take for hidden geometry to become
audible?* — and it sharpens K2 into physics: the isospectral pair is a knife-edge, not a robust degeneracy.

## Honest limits (frozen in advance)

- Toy model: a static scalar potential standing in for "coupling to a second field", on 2D drums. Not a
  dynamical two-field system and not a KK reduction — the drums remain an **analogy** for a mass tower.
- **No novelty claimed.** That a constant shifts a spectrum rigidly, and that generic perturbations lift
  accidental degeneracies at first order, are textbook. The payout is the quantitative bracket and the
  explicit refutation of the "tile-locality protects" guess, on the family's own instrument.
- The split verdict was pre-registered as the expected outcome, so neither half is a post-hoc rescue.

## Inputs (read-only) & artifacts

Kac 1966 · Gordon–Webb–Wolpert 1992 · Cleve Moler (transplantation, 2012) · Rayleigh–Schrödinger perturbation
theory. Reuses [K2](../K2_isospectral_drums) `k2_drums.py`. `code/m4_coupling.py` ·
`results/m4_coupling.json`. Interpreter: conjecture_machine `.venv` (numpy 2.4.6, scipy 1.18.0).
