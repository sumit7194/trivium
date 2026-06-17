# Leg 5c — Pre-Registration: Integrability Fingerprints

This document freezes our hypotheses, experimental design, and success criteria for **Leg 5c: Integrability Fingerprints (Option D)**. We test whether the neural bottleneck count (`tabula` autoencoder) can detect the presence of a hidden symmetry—the Carter constant—directly from geodesic trajectory coordinates.

---

## 1. Physical & Mathematical Formulation

Equatorial orbits in Kerr spacetime are always integrable but do not probe the Carter constant. By generalizing to 3D (off-equatorial) massive geodesics, the active phase subspace is 4-dimensional:
$$X = [r, u, p_r, p_u]$$
where $u = \cos\theta$ and $p_u = g_{uu} \frac{du}{d\lambda}$ is the conjugate momentum.

We compare two spacetimes using the Boyer-Lindquist style rotating metric structure:
$$\Sigma = r^2 + a^2 u^2, \quad \Delta = r^2 - 2Mr + a^2 + \epsilon M^2 u^2$$

1.  **Exact Kerr ($\epsilon = 0.0$)**: The Carter constant $K$ is conserved along the geodesic, providing a second independent algebraic constraint (in addition to the Hamiltonian constraint $g_{ab} v^a v^b = -1$) on $X$. The trajectory lies on a **2-dimensional manifold** (a 2D torus).
2.  **Deformed Kerr ($\epsilon = 0.1$)**: Symmetries are broken, and the Carter constant is lost. The trajectory is only restricted by the Hamiltonian constraint, filling a **3-dimensional volume** in $X$.

The Kerr Carter constant is calculated along the trajectory as:
$$K = (1 - u^2) p_u^2 + u^2 \left( a^2 (1 - E^2) + \frac{L_z^2}{1 - u^2} \right)$$
where $E = -p_t$ and $L_z = p_\phi$ are conserved conjugate momenta.

---

## 2. Experimental Design

### Geodesic Generation
*   **Parameters**: Mass $M = 1$, spin $a = 0.5$.
*   **Initial Conditions**: 5 bound massive geodesics are launched from $r_0 = 12.0$, $u_0 = 0.0$, $\phi_0 = 0.0$ with initial spatial velocities:
    *   $v_r = 0.0$
    *   $v_u \in \{0.001, 0.002, 0.003, 0.004, 0.005\}$
    *   $v_\phi = 0.035$
    The temporal velocity $v_t$ is determined by solving $g_{ab} v^a v^b = -1$ at launch.
*   **Integration**: Geodesics are integrated for 6,000 steps with affine step size $\Delta\lambda = 0.05$ using 4th-order Runge-Kutta.
*   **Outputs**: Phase space coordinates $[r, u, p_r, p_u]$ along the trajectories are collected and saved to `results/obs_integrability_kerr.npz` and `results/obs_integrability_deformed.npz`.

### Bottleneck Autoencoder Sweeps
*   **Features**: Standardized and whitened active coordinates $X = [r, u, p_r, p_u]$ ($m=4$ features).
*   **Architecture**: Bottleneck autoencoder with Tanh activations:
    `Linear(4 -> 64) -> Tanh -> Linear(64 -> 64) -> Tanh -> Linear(64 -> d) -> Linear(d -> 64) -> Tanh -> Linear(64 -> 64) -> Tanh -> Linear(64 -> 4)`
    where the bottleneck dimension $d$ is swept over $\{0, 1, 2, 3, 4\}$.
*   **Training**: Trained for 4000 steps with Adam (learning rate 1e-3, batch size 512) over 3 independent seeds.
*   **Dimension Rule**: Knee count = number of dimensions $d \ge 1$ where the whitened marginal $R^2$ gain exceeds 2% ($0.02$).

---

## 3. Hypotheses & Success Criteria

*   **H1 (Carter Constant Conservation & Drifting)**:
    Along geodesics in exact Kerr ($\epsilon = 0.0$), the Carter constant $K$ is conserved with a standard deviation $\sigma(K) < 10^{-8}$. In deformed Kerr ($\epsilon = 0.1$), the symmetry is broken, resulting in a standard deviation $\sigma(K) > 10^{-4}$ (showing a $> 10,000\times$ increase in variance).
*   **H2 (Intrinsic Dimension Shift)**:
    The neural bottleneck count will resolve exactly **2** dimensions for exact Kerr ($\epsilon = 0.0$) and exactly **3** dimensions for deformed Kerr ($\epsilon = 0.1$).
*   **H3 (Marginal Gain Separation)**:
    For exact Kerr, the marginal $R^2$ gain from $d=2$ to $d=3$ is less than $2\%$ ($0.02$), while for deformed Kerr, the marginal gain from $d=2$ to $d=3$ is greater than $2\%$.
