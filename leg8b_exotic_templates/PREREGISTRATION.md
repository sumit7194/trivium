# Leg 8b — Pre-Registration: Physics-Grounded Echo Templates

This document freezes our hypotheses, experimental setup, and success criteria for **Leg 8b: Physics-Grounded Echo Templates (Option E)**. We test the `deepstrain` echo-search pipeline's performance on physically motivated echo templates derived from the Damour-Solodukhin (DS) wormhole metric and a wave-scattering Fabry-Perot cavity model.

---

## 1. Physics & Template Formulation

We model the frequency-domain echo train $\Psi_{echo}(f)$ for $n_{echoes} = 6$ as:
$$\Psi_{echo}(f) = S_{ring}(f) \sum_{k=1}^{n_{echoes}} \left( \Gamma(f) e^{-i 2\pi f \Delta t} \right)^k$$
where:
*   $\Delta t = 0.2925$ s is the predicted echo spacing for GW150914.
*   $S_{ring}(f)$ is the Fourier transform of a damped sine-Gaussian starting at $t_{first} = 0.1$ s:
    $$S_{ring}(f) = e^{-i 2\pi f t_{first}} \frac{\omega_0}{\omega_0^2 + (1/\tau + i 2\pi f)^2}$$
    with $f_0 = 250$ Hz and $\tau = 0.02$ s.
*   $\Gamma(f)$ is the frequency-dependent reflection coefficient representing potential barrier transmission loss and a throat reflection phase flip:
    $$\Gamma(f) = - \frac{\gamma}{\sqrt{1 + e^{2\pi (f - f_0)/f_w}}}$$
    with low-frequency maximum reflectivity $\gamma = 0.7$ and roll-off width $f_w = 40$ Hz (corresponding to the $4$ ms damping time of the black hole photon sphere).

The time-domain template is:
$$\psi_{echo}(t) = \text{IFFT}[\Psi_{echo}(f)]$$
normalized such that the first echo peak amplitude matches the target injection amplitude.

---

## 2. Hypotheses & Success Criteria

### H1 (SymPy Metric Verification) — Exact Proof
*   **Hypothesis**: SymPy will symbolically verify that the photon sphere (light-ring orbit) $r_{ph}$ for the Damour-Solodukhin wormhole metric:
    $$ds^2 = -\left(1 - \frac{2M}{r} + \lambda^2\right) dt^2 + \left(1 - \frac{2M}{r}\right)^{-1} dr^2 + r^2 d\Omega^2$$
    is located at:
    $$r_{ph} = \frac{3M}{1+\lambda^2}$$
*   **Agreement Criterion**: SymPy's solver finds $r_{ph} = \frac{3M}{1+\lambda^2}$ as the unique root of the potential derivative $\frac{d}{dr}(V_{eff}(r)) = 0$.

### H2 (Pulse Redshifting & Broadening) — Morphological Verification
*   **Hypothesis**: The time-domain template $\psi_{echo}(t)$ will exhibit physical dispersion: subsequent echoes ($k > 1$) will be broader and have lower instantaneous frequency than the first echo due to the high-frequency filtering of the potential barrier.
*   **Agreement Criterion**: Plotting the templates visually confirms that the high-frequency components are filtered out, and the power spectrum of the $k$-th echo is redshifted relative to the $(k-1)$-th echo.

### H3 (Sensitivity Degradation) — Pipeline Robustness
*   **Hypothesis**: The physical filtering of high frequencies smooths the energy envelope, reducing the sharp transient features that both search statistics rely on. As a result, the 50% recovery threshold for the physics-grounded templates will be higher (less sensitive) than for the phenomenological templates.
*   **Agreement Criterion**: The amplitude at which the recovery rate reaches $50\%$ in the raw-strain injection sweeps increases compared to the phenomenological baseline.

### H4 (ML Scorer Advantage) — Representation Oracle Value
*   **Hypothesis**: The noise-trained ML scorer will maintain a sensitivity advantage of at least $1.2\times$ over the raw comb statistic on the physics-grounded templates, demonstrating its robustness to physical modifications of the echo shape.
*   **Agreement Criterion**: The 50% recovery threshold amplitude for the ML scorer is at least $1.2\times$ lower than the comb statistic's threshold.

### H5 (On-Source Search Null) — Physical Search
*   **Hypothesis**: Running the search on real GW150914 post-merger data with the physics-grounded templates will return a null result, consistent with detector noise.
*   **Agreement Criterion**: The empirical p-value of the on-source score at the predicted spacing $\Delta t = 0.2925$ s is $\ge 0.05$ (meaning it is not statistically significant).
