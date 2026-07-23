# M4 — Pre-registration: does coupling a second field make the hidden geometry audible?

*Frozen 2026-07-23, before `code/m4_coupling.py` is written or run (classes of coupling were scouted to set
honest thresholds; the production script re-derives everything under the gates). Ledger item M4 (Tier M).
Second postulate off the [K2](../K2_isospectral_drums) drums build — the arc's "one build, three postulates".*

## The postulate under attack (Ledger M4)

> **"The GWW isospectral pair becomes distinguishable at ANY nonzero coupling to a second field"**
> (spectral degeneracy is measure-zero fragile).

[K2](../K2_isospectral_drums) established that the two Gordon–Webb–Wolpert drums have identical Dirichlet
spectra to ~10⁻¹⁵, exactly (transplantation is a combinatorial bijection). M4 asks the sequel the ledger
cares about: **what does it take for the hidden geometry to become audible?**

## Method (frozen — reuses the K2 build)

Couple a static second field by adding a potential V(x,y) to the Dirichlet Laplacian on each drum:
**H = −∇² + V**, discretised exactly as in K2 (offset cell-centre grid, 5-point Dirichlet Laplacian, aligned
resolutions only, N₁ = N₂ enforced). Compare the lowest 12 eigenvalues of the two drums and report
**split ≡ max|Δλ| / λ̄**. Resolutions **n ∈ {32, 64}**; couplings applied at strengths α as listed below.

Coupling classes tested (frozen):
1. **none** (control — must reproduce K2's isospectrality),
2. **uniform** V = c (a constant mass term),
3. **linear ramp** V = α·x (generic, global),
4. **localized Gaussian bump** V = α·exp(−|r−r₀|²/0.2), r₀ = (1.5,1.5),
5. **radial well** V = α·|r−r₀|²,
6. **tile-local** V = α·(frac x + frac y) — a candidate one might *hope* is protected by the tile structure.

## Frozen gates

- **M4a — the KILL (primary): "ANY" is false.** A **uniform** coupling V = c leaves the two spectra identical:
  **split < 1e-10**. Trivially, H = −∇² + cI shifts every eigenvalue by the same c, so isospectrality is
  preserved. → **KILLED as literally stated**: there exists a nonzero coupling under which the drums remain
  indistinguishable. → SURVIVES only if even a constant coupling splits them (which would indicate a bug).

- **M4b — the fragility (the postulate's real content, expected to hold).** Every **spatially-varying**
  coupling class (3–6 above) splits the spectra at unit strength by **split > 1e-4**, i.e. far above the
  ~1e-15 isospectral floor. The degeneracy is not robust to a position-dependent probe.

- **M4c — first-order scaling.** For the linear-ramp and Gaussian-bump classes, the splitting is **linear in
  the coupling strength** at small α: fitting split(α) ∝ α^p over α ∈ {0.01, 0.03, 0.1, 0.3} gives
  **p ∈ [0.9, 1.1]**. This certifies the splitting is a genuine first-order perturbation effect (the two
  drums' eigenfunctions differ in how they weight the potential), not a numerical accident or a
  higher-order artifact.

- **M4d — the protection mechanism (what the kill teaches).** The protected class is exactly the **constants**:
  the tile-local candidate (6) — the most plausible "structured" coupling one might expect the transplantation
  to protect — **must split** (> 1e-4), demonstrating that tile-locality alone is *not* protection. Reported
  together with the constant case, this brackets the answer: uniform ⇒ deaf, anything that distinguishes
  points in space ⇒ audible.

- **M4e — canary.** The no-coupling control reproduces K2 (split < 1e-10) and all conclusions hold at both
  n = 32 and n = 64 (the split values agree to within 10% between resolutions for the unit-strength cases).

## Honest limits (fixed in advance)

- Toy model: a static scalar potential standing in for "coupling to a second field", on the 2D drums. Not a
  dynamical two-field system, and not a KK reduction — the drums remain an *analogy* for a mass tower (as
  frozen in K2).
- The expected outcome is a **split verdict** and that is fine: the postulate's literal "ANY" dies to a
  trivial counterexample while its substantive claim (measure-zero fragility) is confirmed. Both halves are
  reported; the kill is not dressed up as more than it is.
- No novelty claimed: that a constant shifts a spectrum rigidly, and that generic perturbations break
  accidental degeneracies at first order, are textbook. The payout is the *quantitative* bracket on what makes
  the hidden geometry audible, on the family's own instrument, continuing the K2 arc.

## Anchors (read-only)

Kac 1966 · Gordon–Webb–Wolpert 1992 · Cleve Moler (transplantation, 2012) · standard Rayleigh–Schrödinger
first-order perturbation theory. Reuses [K2](../K2_isospectral_drums) `k2_drums.py`. Interpreter:
conjecture_machine `.venv` (numpy 2.4.6, scipy 1.18.0).
