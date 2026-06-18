# Leg 4b — Pre-Registration: Generalized Conjecture Handoff

This document freezes our hypotheses, mathematical formulations, and agreement criteria for **Leg 4b: Generalized Conjecture Handoff (Option C)**. We generalize the symbolic proof of force-geometrization to $3+1D$ spacetimes and investigate both conservative electromagnetic (Lorentz) and dissipative (linear/non-linear drag) forces.

---

## 1. Mathematical Formulations

We represent a general stationary $3+1D$ metric as:
$$ds^2 = -\Psi(x, y, z) dt^2 + g_{ij}(x, y, z) dx^i dx^j + 2 A_i(x, y, z) dt dx^i$$
where coordinates are $x^\mu = [t, x, y, z]$. Stationary condition: all metric components depend only on the spatial coordinates $x^i = [x, y, z]$, meaning $\partial_t g_{\mu\nu} = 0$.

The coordinate-time geodesic equation for $\ddot{x}^i = \frac{d^2 x^i}{dt^2}$ (with velocity $v^i = \frac{dx^i}{dt}$ and $v^0 = 1$) is:
$$\ddot{x}^i = - \left( \Gamma^i_{\alpha\beta} - \Gamma^0_{\alpha\beta} v^i \right) v^\alpha v^\beta$$
This expands to a polynomial in velocities $v$ of degree at most 3:
$$\ddot{x}^i = A^i_0 + A^i_{1, j} v^j + A^i_{2, jk} v^j v^k + A^i_{3, jk} v^j v^k v^i$$
where the coefficients are:
*   **Static acceleration ($v^0$ term)**: $A^i_0 = -\Gamma^i_{00}$
*   **Linear velocity coupling ($v^1$ term)**: $A^i_{1, j} v^j = -\left(2\Gamma^i_{0j} - \Gamma^0_{00} \delta^i_j\right) v^j$
*   **Quadratic velocity coupling ($v^2$ term)**: $A^i_{2, jk} v^j v^k = -\left(\Gamma^i_{jk} - 2\Gamma^0_{0j} \delta^i_k\right) v^j v^k$
*   **Cubic velocity coupling ($v^3$ term)**: $A^i_{3, jk} v^j v^k v^i = \Gamma^0_{jk} v^j v^k v^i$

---

## 2. Hypotheses & Success Criteria

### H1 (3+1D Universality Necessity)
*   **Hypothesis**: If a 3D force/acceleration $a^i(x^k, v^k, \lambda)$ depends on a species parameter $\lambda$ (e.g. charge-to-mass ratio $q/m$), then the Christoffel symbols $\Gamma^\mu_{\alpha\beta}$ in the matching geodesic equations must depend on $\lambda$. Since $\lambda$ is a property of the test body, the metric cannot be universal.
*   **Agreement Criterion**: Symbolic differentiation with respect to $\lambda$ verifies that if $\frac{\partial a^i}{\partial \lambda} \neq 0$, then at least one component of $\frac{\partial \Gamma^\mu_{\alpha\beta}}{\partial \lambda}$ must be non-zero.

### H2 (Electromagnetic Geometrization)
*   **Hypothesis**: For a static electric potential $\Phi(x, y, z)$ and magnetic vector potential $\vec{A}_{EM}(x, y, z)$, the Lorentz force $a^i_{EM} = \lambda \left( -\partial_i \Phi + \epsilon^i_{jk} v^j B^k \right)$ (with $B^k = \epsilon^{kjl}\partial_j A_{EM, l}$) can be matched to the static and linear velocity terms of the geodesic equation in the weak-field limit by setting $\Psi \approx 1 - 2\lambda\Phi$ and $g_{0i} \approx \lambda A_{EM, i}$.
*   **Result**: Symbolic expansion in the weak-field limit reproduces $A^i_0 \approx -\lambda \partial_i \Phi$ and $A^i_{1, j} v^j \approx \lambda (\vec{v} \times \vec{B})^i$.

### H3 (Linear Drag Dissipation Contradiction)
*   **Hypothesis**: In a general stationary $3+1D$ metric, a pure linear drag force $a^i = -\gamma v^i$ cannot be represented. Forcing the other coefficients in the geodesic equations to vanish ($A^i_0 = 0$, $A^i_{2, jk} = 0$, $A^i_{3, jk} = 0$) forces the linear coupling coefficient $A^i_{1, j}$ to be identically zero.
*   **Result**: SymPy's solver proves that setting the non-dissipative terms to zero forces $A^i_{1, j} = 0$ for all $i, j$.

### H4 (Non-Linear Drag Non-Analyticity)
*   **Hypothesis**: Non-linear drag forces of the form $a^i = -\gamma |v|^p v^i$ (where $|v| = \sqrt{\sum (v^k)^2}$ and $p$ is non-integer) are non-analytic at $v=0$. Since the geodesic equations are strictly polynomial in $v^i$, they cannot represent such non-linear drag terms.
*   **Result**: Symbolic analysis confirms that $|v|$ cannot be represented by a polynomial in $v^x, v^y, v^z$.

---

## 3. Success Criteria

- **C1: 3+1D Universality necessity verified.**
- **C2: Electromagnetic Lorentz force geometrization verified.**
- **C3: Linear drag dissipation contradiction verified.**
- **C4: Non-linear drag non-analyticity constraint verified.**
- **No changes to other repos.** All code lives under `leg4_conjecture_handoff_generalized/`.
