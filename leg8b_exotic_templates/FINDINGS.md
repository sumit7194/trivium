# Leg 8b — Findings: Physics-Grounded Echo Templates (Option E)

Symbolic verification, template generation, injection-recovery sensitivity sweeps, and
on-source searches for **Leg 8b** (Physics-Grounded Echo Templates) — testing how a physical
wave-scattering model of a Damour-Solodukhin (DS) wormhole cavity affects search sensitivity
in real LIGO noise versus toy phenomenological models.

## Result in one line (with the power caveat up front)

The physics-grounded (dispersion-filtered) template **degrades the ML scorer's sensitivity
and, suggestively, lets the shape-agnostic Comb baseline overtake it** for amplitudes
≥ 1.0σ; the on-source GW150914 search is a clean null. **Important caveat: the recovery
efficiencies are each measured from only N = 25 injections per amplitude** (binomial 95% CI
≈ ±0.18), so the "sensitivity reversal" — e.g. 0.68 vs 0.84 at 1.5σ — has **heavily
overlapping error bars and is suggestive, not established**. Read it as a plausible,
underpowered effect with a clean mechanism (§3), not a confirmed discovery. The 50%
thresholds are interpolated off a coarse 5-point amplitude grid.

---

## 1. Quantitative Results

### Injection-Recovery Efficiencies (p-value < 0.05 against background)

| Target Template | Search Statistic | 0.5σ | 1.0σ | 1.5σ | 2.0σ | 3.0σ | 50% Threshold |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Toy Phenomenological** | ML Scorer | **0.12** | **0.76** | **1.00** | **1.00** | **1.00** | **~0.85σ** |
| (Constant Decay) | Comb Baseline | 0.04 | 0.48 | **1.00** | **1.00** | **1.00** | **~1.02σ** |
| **Physics-Grounded** | ML Scorer | 0.08 | 0.28 | 0.68 | 0.68 | 0.80 | **~1.25σ** |
| (Wormhole Filtered) | Comb Baseline | **0.08** | **0.48** | **0.84** | **1.00** | **1.00** | **~1.02σ** |

### On-Source Search (GW150914 post-merger)
*   **ML Scorer**: Anomaly Score $= -0.157$, $p\text{-value} = 0.903$ (Null result)
*   **Comb Baseline**: Comb Statistic $= -0.371$, $p\text{-value} = 1.000$ (Null result)

---

## 2. Hypothesis & Success Criteria Evaluation

### H1 (SymPy Metric Verification) — TRUE (Exact Proof)
*   **Hypothesis**: SymPy will symbolically verify that the photon sphere (light-ring orbit) $r_{ph}$ for the Damour-Solodukhin wormhole metric:
    $$ds^2 = -\left(1 - \frac{2M}{r} + \lambda^2\right) dt^2 + \left(1 - \frac{2M}{r}\right)^{-1} dr^2 + r^2 d\Omega^2$$
    is located at $r_{ph} = \frac{3M}{1+\lambda^2}$.
*   **Result**: **Verified successfully ✅.** The effective potential for radial null geodesics is $V_{eff}(r) = \frac{1 - 2M/r + \lambda^2}{r^2}$. Solving $\frac{d}{dr}(V_{eff}(r)) = 0$ symbolically yields $r_{ph} = \frac{3M}{1+\lambda^2}$ as the unique physical root.

### H2 (Pulse Redshifting & Broadening) — TRUE (Morphological Verification)
*   **Hypothesis**: The time-domain template $\psi_{echo}(t)$ will exhibit physical dispersion: subsequent echoes ($k > 1$) will be broader and have lower instantaneous frequency than the first echo due to the high-frequency filtering of the potential barrier.
*   **Result**: **Verified successfully ✅.** As seen in the waveform comparison plot, subsequent reflections are visibly smoothed out and redshifted, filtering out high-frequency oscillations and causing the wave envelope to broaden in the time domain.

### H3 (Sensitivity Degradation) — TRUE (Pipeline Robustness)
*   **Hypothesis**: The physical filtering of high frequencies smooths the energy envelope, reducing the sharp transient features that both search statistics rely on. As a result, the 50% recovery threshold for the physics-grounded templates will be higher (less sensitive) than for the phenomenological templates.
*   **Result**: **Verified successfully ✅.** For the ML Scorer, the 50% threshold degraded from $\approx 0.85\sigma$ to $\approx 1.25\sigma$ ($1.47\times$ sensitivity loss). For the Comb statistic, while the 50% threshold remained stable at $\approx 1.02\sigma$, its recovery at $1.5\sigma$ dropped from $100\%$ to $84\%$, showing overall sensitivity degradation.

### H4 (ML Scorer Advantage) — NOT SUPPORTED (suggestive reversal, underpowered)
*   **Hypothesis**: The noise-trained ML scorer will maintain a sensitivity advantage of at least $1.2\times$ over the raw comb statistic on the physics-grounded templates, demonstrating its robustness to physical modifications of the echo shape.
*   **Result**: **Not supported.** The point estimates run the *other* way — the Comb baseline matches or beats the ML Scorer for amplitudes $\ge 1.0\sigma$ (50% recovery at $\approx 1.02\sigma$ vs $\approx 1.25\sigma$). But with **N = 25 injections per amplitude**, the deciding points (e.g. 1.5σ: ML 17/25 = 0.68 vs Comb 21/25 = 0.84) have binomial 95% CIs of roughly ±0.18 that **overlap substantially**, so this is a *suggestive* reversal, not a statistically established one. The honest claim is: the hypothesized ML advantage did not appear, and the data lean toward a reversal that a higher-N rerun (≥ ~200 injections) would be needed to confirm.

### H5 (On-Source Search Null) — TRUE (Physical Search)
*   **Hypothesis**: Running the search on real GW150914 post-merger data with the physics-grounded templates will return a null result, consistent with detector noise.
*   **Result**: **Verified successfully ✅.** The on-source search returned $p_{ML} = 0.903$ and $p_{comb} = 1.000$. Neither statistic showed any evidence of echoes at the predicted spacing $\Delta t = 0.2925$ s.

---

## 3. Proposed mechanism for the (suggestive) sensitivity reversal

*This is the hypothesized explanation for the leaning-reversal in §2 — internally consistent
and physically motivated, but resting on the same underpowered (N = 25) measurement, so it
is a mechanism proposal, not an established finding.* The story: physical wave-dispersion
interacts with the learned neural representation as follows:

1.  **Low-Pass Filtering of the Potential Barrier**:
    The potential barrier surrounding the wormhole throat acts as a frequency-dependent mirror. The reflection coefficient $\Gamma(f) \propto - 1/\sqrt{1 + e^{2\pi(f-f_0)/f_w}}$ acts as a low-pass filter, reflecting low frequencies while letting high-frequency components escape.
2.  **Smoothing and Redshifting of subsequent echoes**:
    Each bounce off the potential barrier filters out high frequencies. As $k$ increases, the echoes lose their sharp high-frequency edges and are redshifted into smooth, low-frequency oscillations.
3.  **Autoencoder Reconstruction Anomaly Deficit**:
    *   The ML scorer uses a Convolutional Autoencoder (ConvAE) trained on detector noise to evaluate anomaly scores. Real detector noise is dominated by low-frequency power (red noise).
    *   Under toy phenomenological templates, subsequent echoes retain their high-frequency features ($250$ Hz). These sharp high-frequency transients are highly anomalous to the ConvAE, resulting in large reconstruction errors $e(t)$ and a strong detection statistic.
    *   Under physics-grounded templates, the subsequent echoes are smoothed and redshifted. Because these smoothed, low-frequency waveforms closely resemble the low-frequency fluctuations of standard detector noise, the ConvAE reconstructs them with high fidelity.
    *   This reconstruction success reduces the reconstruction-error envelope $e(t)$, starving the downstream Comb scorer of its input signal and degrading the ML scorer's recovery rate.
4.  **Robustness of the Comb Baseline**:
    The Comb baseline is shape-agnostic. It computes the envelope autocorrelation of the whiten-filtered strain data. Because the envelope peaks still occur at exact intervals of $\Delta t$, the Comb baseline remains highly robust to the loss of high-frequency signal, maintaining its 50% recovery threshold at $\approx 1.02\sigma$.

---

## 4. Visualizations

The waveform comparison plot (showing dispersion and redshifting) and the sensitivity comparison plot (showing the sensitivity reversal) have been successfully compiled:
*   Waveform comparison plot: [leg8b_waveform_comparison.png](file:///Users/sumit/Github/TheBridge/results/leg8b_waveform_comparison.png)
*   Sensitivity curves plot: [leg8b_sensitivity_comparison.png](file:///Users/sumit/Github/TheBridge/results/leg8b_sensitivity_comparison.png)

This completes the analysis for **Leg 8b (Option E)**. The defensible takeaways: the
physics-grounded template is verified symbolically (H1) and shows the expected dispersion
(H2); it measurably degrades the ML scorer (H3); the on-source search is null (H5); and the
data *suggest*, without statistically establishing (N = 25), that physical smoothing can
erase the learned scorer's advantage over a shape-agnostic baseline by reconstructing the
dispersed echoes as ordinary red noise. A higher-N injection campaign is the natural
follow-up to confirm or retire the reversal.
