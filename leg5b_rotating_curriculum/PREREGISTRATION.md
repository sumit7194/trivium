# Leg 5b — Pre-Registration: Rotating Strong-Field Curriculum

This document pre-registers our hypotheses, experimental design, and success criteria for **Leg 5b: Rotating Strong-Field Curriculum**. We extend the static Schwarzschild curriculum (Leg 5) to rotating Kerr spacetimes, where frame-dragging creates asymmetric shadow boundaries.

---

## 1. Physical & Mathematical Formulation

We restrict null geodesics to the equatorial plane ($\theta = \pi/2$, $p_\theta = 0$) in Boyer-Lindquist coordinates. The radial geodesic equations for a photon in Kerr spacetime (with $M=1$ and spin $a \in [0, 1)$) are governed by the critical impact parameter $\xi = L/E$:

$$\begin{aligned}
\frac{dr}{d\lambda} &= \frac{p_r}{r^2} \\
\frac{dp_r}{d\lambda} &= \frac{2(r^2 + a^2 - a\xi)r - (r - 1)(\xi - a)^2}{r^2}
\end{aligned}$$

where $p_r = r^2 \frac{dr}{d\lambda}$ is the radial momentum conjugate.

### Exact Critical Boundaries (Theory Oracle)
The prograde and retrograde circular photon orbits correspond to unstable orbits where $p_r = 0$ and $dp_r/d\lambda = 0$. For a given spin $a$, these occur at Boyer-Lindquist radii $r_{pro}$ and $r_{ret}$:

$$r_{pro} = 2 \left(1 + \cos\left(\frac{2}{3} \arccos(-a)\right)\right), \quad r_{ret} = 2 \left(1 + \cos\left(\frac{2}{3} \arccos(a)\right)\right)$$

The exact critical impact parameters associated with these orbits are:

$$\xi_{pro} = -\frac{r_{pro}^3 - 3 r_{pro}^2 + a^2 r_{pro} + a^2}{a(r_{pro} - 1)}, \quad \xi_{ret} = -\frac{r_{ret}^3 - 3 r_{ret}^2 + a^2 r_{ret} + a^2}{a(r_{ret} - 1)}$$

For $a=0$, these limits converge symmetrically to $\xi_{crit} = \pm 3\sqrt{3} \approx \pm 5.196$. For $a > 0$, the shadow boundary becomes asymmetric (e.g., for $a=0.5$, $\xi_{pro} \approx 4.10$ and $\xi_{ret} \approx -6.14$).

---

## 2. Experimental Design

We compare two training distributions with the **exact same number of total training segments** to control for capacity:

### Curriculum A (Uniform)
* **Sampling**: Spin $a$ is sampled uniformly from $[0.0, 0.9]$.
* **Impact Parameter**: $\xi$ is sampled uniformly from $[-9.0, 9.0]$.
* **Rays**: Integrated from $r_0 = 15.0$ inward.

### Curriculum B (Targeted)
* **Sampling**: Spin $a$ is sampled uniformly from $[0.0, 0.9]$.
* **Impact Parameter**: Concentrated around the spin-dependent critical winding regions:
  * **60% near-critical rays**: $\xi$ sampled uniformly from $[\xi_{ret} - 0.4, \xi_{ret} + 0.2] \cup $[\xi_{pro} - 0.2, \xi_{pro} + 0.4]$.
  * **40% background rays**: $\xi$ sampled from the rest of the $[-9.0, 9.0]$ domain.

### Model & Training
* **State Representation**: $X = [u, p_r, a, \xi]$ where $u = 1/r$.
* **Target Output**: $Y = [u', p_r']$ after a step of $\Delta\lambda = 0.05$.
* **Model**: Multi-layer perceptron with residual connections (size $4 \rightarrow 128 \rightarrow 128 \rightarrow 128 \rightarrow 2$).
* **Training**: 8000 steps with Adam optimizer, batch size 256. Evaluated over 3 independent seeds.

---

## 3. Hypotheses & Success Criteria

* **H1 (Asymmetric Shadow Recovery)**: The learned simulator trained on Curriculum B will reconstruct the asymmetric shadow boundaries $\xi_{pro}$ and $\xi_{ret}$ across the spin range $a \in [0.1, 0.8]$ with lower error than the simulator trained on Curriculum A.
* **H2 (Error Reduction at High Spin)**: At high spin $a = 0.8$, the relative error in the prograde shadow boundary $\xi_{pro}$ for Curriculum B will be at least **2.0x smaller** than that of Curriculum A.
* **H3 (High Fidelity Simulator)**: The one-step prediction $R^2$ on held-out test trajectories will exceed $0.995$ for both networks, but the boundary resolution (using batched ray-tracing) will expose the training set representation differences.
