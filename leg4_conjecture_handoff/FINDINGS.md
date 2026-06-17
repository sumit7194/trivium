# Leg 4 — Findings: the conjecture handoff (physics geometrization)

*Run 2026-06-17. Verification criteria frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before execution.*

## Result in one line

Using symbolic differential geometry, we proved that **universality and conservativeness are necessary conditions for force geometrization**, successfully verifying the neural pattern discovered by `tabula-geometrica`.

---

## 1. Universality Proof

For a species-dependent force $a = F(x, v, \lambda)$ where $\lambda = q/m$ is the species parameter (charge-to-mass ratio), mapping the equation of motion to a 1D geodesic equation:
$$\ddot{x} + \Gamma^x_{xx}(\lambda) \dot{x}^2 = 0$$
requires:
$$\Gamma^x_{xx}(x, \lambda) = -\frac{F(x, v, \lambda)}{v^2}$$

Differentiating with respect to the species parameter $\lambda$:
$$\frac{\partial \Gamma^x_{xx}}{\partial \lambda} = -\frac{1}{v^2} \frac{\partial F}{\partial \lambda}$$

Since $\lambda$ is a property of the test body, if the force depends on the species ($\partial F / \partial \lambda \neq 0$), then the Christoffel symbol $\Gamma^x_{xx}$ (and thus the metric $g_{xx}$) must depend on the test body's species. This contradicts the fundamental assumption of general relativity that the spacetime metric is a universal background property. Thus, **universality is a necessary condition for geometrization** (verifying C1).

---

## 2. Conservativeness (Dissipation) Proof

To see if linear velocity-dependent friction ($a = -\gamma v$) can be represented as geodesic motion in a stationary metric, we evaluated the geodesic equation of a general stationary 1+1D metric:
$$ds^2 = -A(x) dt^2 + B(x) dx^2 + 2 C(x) dt dx$$

Expressed in coordinate time $t$ with velocity $v = \dot{x}$, the geodesic equation takes the form:
$$\ddot{x} = A_0(x) + A_1(x) v + A_2(x) v^2 + A_3(x) v^3$$

Using SymPy, we derived the coefficients in terms of the metric components ($D = AB + C^2$):
*   **v⁰ coefficient (Potential force $A_0$):** $-\frac{A A'}{2D}$
*   **v¹ coefficient (Friction/Coriolis $A_1$):** $\frac{-A C' + \frac{3}{2} C A'}{D}$
*   **v² coefficient ($A_2$):** $\frac{-\frac{1}{2} A B' + B A'}{D}$
*   **v³ coefficient ($A_3$):** $\frac{-B C' + \frac{1}{2} C B'}{D}$

To represent pure linear velocity friction $\ddot{x} = -\gamma v$, we must set the potential force and higher-order velocity terms to zero:
1.  **Setting $A_0 = 0$** implies $A'(x) = 0$ (the potential must be constant).
2.  Substituting $A'(x) = 0$ into the remaining terms yields:
    *   $A_2 = -\frac{A B'}{2D}$
    *   $A_3 = \frac{-B C'}{2D}$
3.  **Setting $A_2 = 0$** implies $B'(x) = 0$.
4.  **Setting $A_3 = 0$** implies $C'(x) = 0$ (since $B \neq 0$).
5.  Substituting $B'(x) = C'(x) = 0$ into $A_1$ yields:
    *   **$A_1 = 0$**

### The Contradiction

By forcing all other terms in the geodesic equation to zero (no potential gradient, no quadratic or cubic velocity terms), the linear velocity coefficient $A_1$ is **identically forced to zero**. 

This proves that **a pure linear friction force cannot be represented by the geodesic motion of a stationary metric** (verifying C2).

---

## 3. Physical Synthesis

This symbolic verification closes the loop between the neural heuristic and exact mathematical physics:
*   **Universality** is the mathematical expression of the **Weak Equivalence Principle**: all particles must fall the same way in a gravitational field, allowing the field to be geometrized into a single, species-independent metric.
*   **Conservativeness** is required because geodesic equations of a stationary metric are conservative and time-reversible. Linear velocity-dependent dissipation breaks time-reversal symmetry ($t \to -t$). In a static metric, this sign mismatch prevents velocity drag from being represented without introducing explicit time-dependence (non-stationarity) in the metric, or violating energy conditions.

This handoff demonstrates the end-to-end falsifiability pipeline: `tabula` discovers a general heuristic transition from trajectories, and `ansatz` proves the exact boundaries of that transition.
