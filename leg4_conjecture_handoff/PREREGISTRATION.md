# Leg 4 — Pre-registration: the conjecture handoff (physics geometrization)

*Frozen 2026-06-17, before any proof code is written. Discipline: THE_BRIDGE.md §2, §4A.*

This leg implements the **Conjecture Handoff**: we take the empirical discovery made by `tabula-geometrica` (via neural simulations of trajectories) and translate it into exact symbolic theorems using `ansatz`'s GR engine structure.

---

## 1. The Conjecture

> **A force geometrizes if and only if it is universal and conservative.**

We translate "geometrizes" to mean: the equations of motion can be written as the geodesic equations of a spacetime metric $\mathbf{g}$:
$$\ddot{x}^a + \Gamma^a_{bc} \dot{x}^b \dot{x}^c = 0$$

We will prove the **necessity** of both conditions symbolically:

1. **Universality is necessary:** If the force depends on a per-body coupling or species charge $q$ (independent of mass $m$), no single set of Christoffel symbols $\Gamma^a_{bc}$ (and thus no single metric $\mathbf{g}$) can describe the trajectories of all bodies.
2. **Conservativeness is necessary:** If the force has a velocity-dependent dissipative term (like friction $-\gamma v^i$), it breaks time-reversal symmetry. No stationary/static metric can produce such a dissipative term in its geodesic equations without breaking stationarity (time-independence) or requiring unphysical stress-energy that violates the Weak Energy Condition (WEC).

---

## 2. Symbolic Proving Plan

We will write `leg4_conjecture_handoff/code/prove_geometrization.py` using SymPy:

### Part 1: Universality Proof
- Let the force be species-dependent: $a^i = F^i(x, v, \lambda)$, where $\lambda = q/m$ is the charge-to-mass ratio.
- Attempt to map the equations of motion to a geodesic equation:
  $$\ddot{x}^i + \Gamma^i_{jk}(\lambda) \dot{x}^j \dot{x}^k = 0$$
- Show that the Christoffel symbols $\Gamma^i_{jk}$ must explicitly depend on the species parameter $\lambda$ if $\partial F^i / \partial \lambda \neq 0$.
- Conclude that a single, species-independent metric $\mathbf{g}$ cannot exist to geometrize the trajectories of different species. This is the symbolic formulation of the Weak Equivalence Principle.

### Part 2: Conservativeness (Dissipation) Proof
- Let the force be dissipative: $a^i = -x^i - \gamma v^i$ (a central restoring force with linear velocity-dependent friction).
- Examine time-reversal symmetry: under $t \to -t$, positions are invariant ($x \to x$), velocities flip sign ($v \to -v$), and accelerations are invariant ($a \to a$).
- The friction force term $- \gamma v^i$ flips sign, breaking time-reversal symmetry.
- Compare with the geodesic equation terms quadratic in velocity: $\Gamma^i_{jk} \dot{x}^j \dot{x}^k$. Under time-reversal, the velocity product $\dot{x}^j \dot{x}^k = (-v^j)(-v^k) = v^j v^k$ is invariant.
- Show that a velocity-dependent drag term $F(v) \propto v^i$ cannot be represented by the symmetric Christoffel symbols of a static, stationary metric because of this sign mismatch.
- Show that any attempt to force-geometrize friction into a stationary metric (by introducing velocity-dependent metric components or similar) leads to an unphysical stress-energy tensor $T^a_b$ that violates the Weak Energy Condition ($\rho < 0$).

---

## 3. Frozen Agreement Criteria

- **C1: Universality necessity verified.** The symbolic check confirms that $\partial \Gamma^i_{jk} / \partial \lambda \neq 0$ is required for non-universal forces.
- **C2: Conservativeness necessity verified.** The symbolic check confirms that a static/stationary geodesic equation cannot represent a time-reversal symmetry-breaking linear velocity drag term, or that doing so requires violating the WEC ($\rho < 0$).
- **No changes to other repos.** The three core repos remain untouched.
