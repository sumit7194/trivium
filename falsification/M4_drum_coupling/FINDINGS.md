# M4 — Findings: what it takes to make hidden geometry audible

> ## ⚠️ CORRECTION (2026-07-24) — observable rebuilt after K2's grid bug; **conclusions unchanged**
>
> M4 was built on [K2](../K2_isospectral_drums)'s discretisation, which turned out to disconnect each drum
> into congruent pieces (see K2's correction). M4's original observable compared the two drums' spectra
> directly against that spurious ~10⁻¹⁵ floor. On a *correct* grid the drums are isospectral only in the
> continuum, so at finite h their spectra already differ by ~2×10⁻², which **swamped the coupling signal** —
> re-running the original M4 on the fixed grid made the first-order scaling read p ≈ 0.03 (flat), i.e. the
> measurement was gone.
>
> **Fix:** a **differential observable** — compare each drum's *own* coupling-induced shift
> δᵢ = λᵢ(V) − λᵢ(0). Common-mode discretisation error cancels, and the measurement becomes resolution-stable
> (n=32 vs n=64 agree to ~1%). **Every M4 conclusion survives**, now on a sound footing: the numbers below are
> the corrected ones.

*Run 2026-07-23, observable corrected 2026-07-24; gates frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before the code. Ledger item M4
(Tier M), second postulate off the [K2](../K2_isospectral_drums) drums build. **Verdict: KILLED as literally
stated — but the postulate's substance survives**, and that split is the finding.*

## Result in one line

A **uniform** coupling V = c shifts **both** drums identically (differential 2×10⁻¹³ — zero distinguishing
power), so "distinguishable at ANY nonzero coupling" is false — while **every** spatially-varying coupling
tested distinguishes them at O(1) (ramp 0.67, bump 1.45, radial 1.06, tile-local 0.14), **linearly** in
coupling strength (p = 0.9997, 1.0014). Hidden geometry
becomes audible precisely when the probe can tell points apart; a globally uniform probe stays deaf.

## The gates

| gate | what | result | verdict |
|---|---|---|---|
| **M4a** (KILL) | uniform V=c adds no distinguishing power | **2.1e-13 / 2.1e-13 / 2.1e-13** at c=1/5/50 | **"ANY" is FALSE → M4 KILLED** |
| **M4b** | every spatially-varying coupling distinguishes | ramp 0.67, bump 1.45, radial 1.06, tile-local 0.14 | **PASS** (fragility confirmed) |
| **M4c** | linear in strength, p ∈ [0.9,1.1] | **p = 0.9997** (ramp), **1.0014** (bump) | **PASS** — genuine first-order effect |
| **M4d** | tile-locality is not protection | tile-local 0.14 ≫ 2e-13 | **PASS** |
| **M4e** | resolution stability | n=32 vs n=64 agree <2%; uniform control 1.9e-13 at n=64 | **PASS** |

## The two halves of the verdict (both reported, neither dressed up)

**The literal postulate dies to a trivial counterexample.** H = −∇² + cI shifts every eigenvalue by the same
c, so a constant coupling — which *is* a nonzero coupling — preserves isospectrality exactly. The word "ANY"
is simply too strong. This is not a deep failure; it is a boundary condition on how the claim may be stated.

**The substance survives, emphatically.** Every coupling that varies in space distinguishes the drums
(differential observable, α = 1, n = 32):

```
  linear ramp   V = α·x                     0.67
  gaussian bump V = α·exp(−|r−r₀|²/0.2)     1.45
  radial well   V = α·|r−r₀|²               1.06
  tile-local    V = α·(frac x + frac y)     0.14
```

against a uniform-coupling floor of **2×10⁻¹³** — twelve orders of magnitude. The degeneracy is measure-zero
fragile exactly as the postulate intended.

## Why the splitting is first-order (M4c)

Fitting the raw differential ∝ α^p over α ∈ {0.01, 0.03, 0.1, 0.3} gives **p = 0.9997** (ramp) and
**p = 1.0014** (bump)
— textbook Rayleigh–Schrödinger. The two drums' eigenfunctions weight the potential differently at first
order, so ⟨ψ|V|ψ⟩ differs immediately. The degeneracy is not protected by any symmetry that survives a
position-dependent perturbation; it is an *accidental* (transplantation) degeneracy of the pure Laplacian.

## The protection mechanism (M4d — what the kill teaches)

The natural guess is that a coupling respecting the drums' tile structure would be protected by the same
transplantation that makes them isospectral. **It is not:** the tile-local potential splits as strongly as a
generic one (0.14 vs a 2e-13 floor). The reason is structural — transplantation does not merely permute the 7 tiles, it maps
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
