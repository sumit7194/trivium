# Leg 4 — Findings: the conjecture handoff (physics geometrization)

*Run 2026-06-17. Verification criteria frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before execution.*

## Result in one line

On a **1+1D stationary metric**, a SymPy derivation confirms that a pure linear-velocity
friction force cannot be written as geodesic motion (the *conservativeness* half of
tabula's "geometrizes ⟺ universal ∧ conservative" heuristic). The *universality* half is
recorded here as the equivalence-principle argument it is — **not** an independently
discovered theorem. This is a worked 1+1D special case of the handoff, not a general proof
of the conjecture (see Honest limits).

---

## 1. Universality — what the code actually shows (and what it does not)

The verbal argument is standard and correct: if a force law `a = F(x, v, λ)` depends on a
per-body species parameter `λ = q/m`, then writing it as a 1D geodesic
`ẍ + Γ(x,λ) v² = 0` forces `Γ = −F/v²` to inherit the `λ`-dependence, so the metric could
not be a single universal background. That is just the **Weak Equivalence Principle**
stated in reverse.

**Honest note on the code.** `prove_geometrization.py` computes `∂/∂λ(−F/v²)` and checks it
equals `−(∂F/∂λ)/v²`. Because `v` does not depend on `λ`, that equality is the **linearity
of the derivative** — it is true for *any* `F` and proves nothing physical on its own. So
Part 1 is a *consistency check that the reduction is self-consistent*, plus the WEP
argument above — it is **not** a SymPy-discovered result, and it should not be cited as a
"proof" of universality. (C1 is therefore best read as "restated, consistent," not
"proven.")

---

## 2. Conservativeness (dissipation) — a genuine 1+1D derivation

This part is a real symbolic result, within its stated scope. For a general stationary
1+1D metric
$$ds^2 = -A(x)\,dt^2 + B(x)\,dx^2 + 2C(x)\,dt\,dx,$$
the coordinate-time geodesic equation is `ẍ = A₀ + A₁v + A₂v² + A₃v³`, with SymPy-derived
coefficients (`D = AB + C²`):

* **v⁰ (potential, A₀):** $-\frac{A A'}{2D}$
* **v¹ (friction/Coriolis, A₁):** $\frac{-A C' + \frac{3}{2} C A'}{D}$
* **v² (A₂):** $\frac{-\frac{1}{2} A B' + B A'}{D}$
* **v³ (A₃):** $\frac{-B C' + \frac{1}{2} C B'}{D}$

To represent *pure* linear friction `ẍ = −γv`, the other coefficients must vanish:
`A₀ = 0 ⟹ A′ = 0`; then `A₂ = 0 ⟹ B′ = 0`; then `A₃ = 0 ⟹ C′ = 0`; substituting
`A′ = B′ = C′ = 0` into `A₁` gives `A₁ = 0` identically (`sp.simplify(A1_final) == 0`,
verified). So a metric with no potential gradient and no quadratic/cubic velocity terms
**cannot** carry a non-zero linear-velocity term either — pure linear friction is not the
geodesic motion of a stationary 1+1D metric. This matches the FINDINGS coefficient table
and is the substantive content of the leg.

---

## 3. Physical reading

Stripped to what is established: geodesic motion of a stationary metric is conservative and
time-reversible, and the 1+1D algebra above shows there is no room in it for a
time-reversal-breaking linear drag term once the conservative structure is imposed. This is
the exact-side echo of tabula's neural observation that dissipative forces resist
geometrization. The "universality" leg is the equivalence principle, restated.

This is the discovery→check direction of the falsifiability pipeline run on **one worked
special case** — a cheap neural heuristic handed to the symbolic engine and confirmed where
the engine can reach. It is a demonstration of the pipeline, not a closed general theorem.

## Honest limits

- **1+1D and one drag model only.** The derivation is for a stationary 1+1D metric and a
  pure linear-velocity friction `−γv`. The general 3+1D case, and non-conservative forces
  like the electromagnetic Lorentz force or non-linear drag, are **not** covered — that is
  exactly the still-open generalization flagged as "Leg 4b" in THE_BRIDGE.md §10 (Option C).
- **Universality is not proven by the code.** As noted in §1, the SymPy step there is a
  tautology; the content is the WEP argument. Do not cite Part 1 as a discovered proof.
- **The energy-condition / WEC angle is asserted, not computed.** PREREGISTRATION raised a
  WEC-violation (ρ < 0) route for the dissipative case; this leg does **not** compute any
  energy-condition quantity, so that clause is unsupported here.
- **No saved artifact.** The script prints to stdout; there is no `results/` transcript.
  The conservativeness algebra is deterministic and re-derivable by running the script.

## Artifacts
- `code/prove_geometrization.py` — SymPy: the 1+1D geodesic-coefficient derivation
  (substantive) and the universality consistency check (tautological — see §1).
