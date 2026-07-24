# R2 — Pre-registration: independent cross-implementation gate of the emit⟺span theorem

*Frozen 2026-07-24, before `code/emit_reproduce.py` is written or run. Falsification v2, Tier R — the
flagship item. ansatz proved (§123, 6/6) that the emit engine's linear core satisfies **emit ⟺ a nonconstant
invariant I ∈ span(Φ) is conserved**, with guards G1 (rank) / G2 (orbit-separating) and an obstruction map.
The bridge does not take a sister theorem on trust: it **reimplements the emit criterion from the stated
algorithm — its own code, no import of §123 — and reproduces the theorem's teeth** (the ⟸ direction, the
pendulum basis-relativity flip, the obstruction map). Cross-implementation, the leg-S/leg-X pattern applied
to a theorem.*

## Prior art (acknowledged; no novelty claimed)

This is the Sparse-Invariant / SID result — a conserved quantity is a null vector of the trajectory design
matrix (Liu–Madhavan–Tegmark; Kaiser–Kutz–Brunton, arXiv:1811.00961; the SVD-null-space conserved-quantity
literature). The theorem is ansatz's §123; the bridge's contribution is an **independent reproduction** of
the mechanism, and a cross-check of the two round-8 adversaries' shapes. The GitHub/PyPI novelty sweep stays
with the quantum session.

## The criterion (reimplemented independently from the stated algorithm)

Sample K orbits of a Hamiltonian system, N points each. Design matrix `M[(o,i),k] = φ_k(z_{o,i}) −
⟨φ_k⟩_o` (per-orbit mean-subtracted — kills the additive constant so different orbits may carry different
invariant values). SVD; **emit ⟺ σ_min ≤ τ_rel·σ_max** (τ_rel = 1e-6). The emitted invariant is the
below-floor right-singular vector. Integrator: a **4th-order symplectic (Yoshida)** — ansatz noted that
leapfrog's O(dt²) drift fakes "not in span"; a true invariant must ride near machine precision, so the
integrator's conservation floor must sit far below τ_rel·σ_max.

## Frozen gates

- **R2a — the ⟸ direction (no false negatives).** A system whose invariant IS in the basis must emit:
  harmonic oscillator H = ½(p²+x²), polynomial (quadratic) basis → **σ_min/σ_max ≤ 1e-10** (emit). And a
  *constructed* representable invariant on random data must give σ_min = 0 to machine precision (the
  symbolic ⟸ proof, checked numerically). PASS = representable ⇒ always emitted.
- **R2b — basis-relativity (the headline flip).** The pendulum H = ½p² − cos x (invariant transcendental):
  in a **polynomial** basis → **NO emit** (σ_min/σ_max > 1e-3); the **instant a cos atom is added** to the
  basis → **emit** (σ_min/σ_max < 1e-8). *Same system, opposite legibility, purely from the probe* — the
  entire content of the corrected G2 law, made mechanical. Reproduces ansatz's Candidate-A (legible) /
  Candidate-B (illegible-until-atom) shapes.
- **R2c — the obstruction map.** (O1) a basis carrying a **hidden identity** (a fixed linear relation among
  the φ_k that holds on *all* phase space, not just orbits) produces a false null that the **rank guard G1**
  flags (M column-rank-deficient on generic scattered points, distinguishable from a true invariant, which
  is full-column-rank off-orbit). (O2) a **single** orbit aliases many functions as conserved; adding
  **diverse** orbits (G2) collapses the null space to the true invariant count. PASS = both guards behave as
  the theorem states.
- **R2d — cross-implementation agreement.** The bridge's independent scale-numbers match ansatz §123's
  order-of-magnitude: harmonic ~1e-15–1e-16, pendulum-poly ~1e-2–1e-3, pendulum+cos ~1e-8–1e-12. Not exact
  (different integrator, sampling, seeds); the **verdicts and scales** must agree. PASS = same physics, two
  implementations.

## Honest scope

- A **cross-implementation reproduction** of a sister's theorem + its adversaries; the theorem is ansatz's,
  the prior art is the SID literature's. Zero novelty. The payout is the family's standard independence
  check applied to its most valuable v2 result — plus a home-built demonstration of "what a linear-probe
  emit engine can and cannot read," the methods-section experimental core (M6).
- Exact/near-machine numeric with a symplectic integrator; finite bases; autonomous invariants; guards
  G1/G2 — the same scope §123 states. Legibility is basis-relative by construction (the point).
- Bridge-solo; no sister; no import of §123's code (a genuine second implementation).
