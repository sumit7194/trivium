# K4 — Pre-registration: ad-hoc metric surgery essentially never preserves vacuum

*Frozen 2026-07-23, before `code/k4_bumpy.py` is written or run (the symbolic structure was scouted to state
the obstruction precisely; the production script re-derives and re-verifies everything under the gates).
Ledger item K4 (Tier K — expected kill). Formalises what [leg Y](../../legY_ck_adjudication)'s
`verify_bumpy_vacuum.py` established for one metric (ansatz §119's bumpy entry) into a general statement.*

## The postulate under attack (Ledger K4)

> **"Every deformation of a vacuum metric that keeps the vacuum character of its invariants is itself
> vacuum."**

Leg Y already showed our own "bumpy" entry (Kerr × a bump) has R_ab ≠ 0. K4 asks the general question and
aims to **extract the obstruction** rather than accumulate examples — the ledger's stated payout: *a warning
theorem for every "bumpy BH" paper that skips the check.*

## The deformation family (frozen)

The surgery bumpy-black-hole constructions actually perform — **multiply g_tt by a radial profile and leave
g_rr alone**:

    ds² = −f(r)·(1 + ε h(r)) dt² + dr²/f(r) + r²dΩ²,    f = 1 − 2M/r

with h(r) an arbitrary radial profile and ε the deformation amplitude. Ricci computed exactly from the
metric (Christoffels → Riemann → Ricci) in sympy — no sampling, no finite differences.

## Frozen gates

- **K4d — controls (run first).** ε = 0 reproduces Schwarzschild with **R_ab ≡ 0 exactly**, and h = const
  (a pure rescaling of t) also gives **R_ab ≡ 0 exactly**. If either fails the machinery is wrong and the
  rest is void.

- **K4a — the KILL (by construction).** For a sample of ad-hoc profiles
  h ∈ {1/r, 1/r², e^(−r), a localized Gaussian bump, a §119-style bump}, the exact Ricci tensor is
  **nonzero** (≥ 1 nonvanishing component each). → **KILLED**: ad-hoc surgery does not preserve vacuum.

- **K4b — the OBSTRUCTION (the payout; a theorem, not a sample).** Computed exactly (all orders in ε, no
  linearisation), the combination

      R_tt/A + R_rr/B  =  ε (r − 2M) h′(r) / ( r² (1 + ε h) )

  vanishes **iff h′(r) = 0**. Therefore the deformed metric is vacuum **iff h is constant**, i.e. iff the
  "deformation" is a pure rescaling of the time coordinate — **pure gauge**. Frozen claim: *no nontrivial
  g_tt-multiplier deformation with g_rr untouched is ever Ricci-flat.* The gate is that the production run
  reproduces this identity symbolically and that solving it returns h = const.

- **K4c — the invariant trap (kills the postulate *as stated*).** The postulate's hypothesis is that the
  deformation "keeps the vacuum character of its **invariants**". Test the simplest such invariant, the Ricci
  **scalar**: at O(ε) the condition R = 0 is a linear ODE whose general solution is

      h(r) = C₁ + C₂ · √( r / (r − 2M) )

  The C₁ branch is the gauge/vacuum one; the **C₂ branch has R ≡ 0 but R_ab ≠ 0**. Gate: exhibit that
  solution, **verify it by substitution** (not by trusting a solver — scouting found sympy's `dsolve`
  returns a *bogus* closed form here, with an r-dependent exponent and spurious logs), and confirm the Ricci
  tensor is nonzero on it. This is the sharpest form of the warning: **a scalar invariant vanishing does not
  certify vacuum.**

## Honest limits (fixed in advance)

- The theorem is proved **for this deformation family** (static, spherically symmetric, g_tt-multiplier with
  g_rr untouched) — precisely the family ad-hoc "bumpy" constructions use. It is *not* a claim about all
  possible deformations of all vacuum metrics; a deformation that also adjusts g_rr to keep the product
  fixed lands back on Schwarzschild with a shifted mass (Birkhoff), which is the other half of the same
  lesson and is noted, not re-proved here.
- Toy/symbolic result, no novelty claimed: that Birkhoff's theorem forbids new static spherical vacua is
  textbook. The payout is the *explicit obstruction* (the h′ identity) and the *explicit counterexample* to
  "invariants look vacuum ⇒ vacuum", stated in the form a bumpy-BH practitioner would actually need.
- Exact symbolic computation throughout; the only approximation is the O(ε) linearisation used **for K4c
  only** (K4b is exact in ε).

## Anchors (read-only)

Birkhoff's theorem · [leg Y](../../legY_ck_adjudication) `verify_bumpy_vacuum.py` (ansatz §119's bumpy entry,
independently recomputed by the bridge) · leg O/Q's bumpy catalogue entry. Interpreter: conjecture_machine
`.venv` (sympy 1.14.0).
