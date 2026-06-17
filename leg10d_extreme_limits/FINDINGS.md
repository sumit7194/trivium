# Leg 10d — Findings: Extreme Steering Limits (The Black Hole Collapse)

We successfully ran the extreme steering sweep for Qwen3-4B up to $\alpha_{steer} = \pm 50.0$ along the Layer 14 intellectual humility virtue vector. Our goals were to test whether activation steering could force the attention geometry into a "singularity collapse" (black hole formation).

---

## 1. Quantitative Results Table

| Steering Scale ($\alpha_{steer}$) | H1: Attention Entropy ($H$) | H2: Normalized Horizon ($R_s / N$) | H3: Correlation ($r$) | H3: Horizon Slope ($G_{eff}$) | H4: Lensing Ratio ($A_{high}/A_{low}$) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **-50.0** (Extreme Negative) | 1.3291 | 0.1631 | 0.8917 | 1.2652 | 5.4973 |
| **-20.0** | 1.1987 | 0.1465 | 0.8838 | 1.1555 | 6.2171 |
| **-10.0** | 1.1764 | 0.1443 | 0.8809 | 1.1431 | 6.5075 |
| **-5.0** | 1.1696 | 0.1439 | 0.8792 | 1.1394 | 6.6863 |
| **0.0** (Baseline) | 1.1653 | 0.1437 | 0.8781 | 1.1368 | 6.8727 |
| **+5.0** | 1.1633 | 0.1439 | 0.8757 | 1.1352 | 6.9091 |
| **+10.0** | 1.1636 | 0.1434 | 0.8760 | 1.1360 | 6.9166 |
| **+20.0** (Peak Lensing) | 1.1704 | 0.1428 | 0.8768 | 1.1403 | 6.9959 |
| **+50.0** (Extreme Positive) | 1.2326 | 0.1434 | 0.8871 | 1.1754 | 6.4430 |

---

## 2. Hypothesis Evaluation

### H1 (Entropy Collapse / Singularity): DISPROVED ❌
*   **Preregistered Criterion**: Average attention entropy drops by $\ge 50\%$ at $\alpha_{steer} = 50.0$ compared to baseline.
*   **Observed**: Baseline entropy is $1.1653$. At $\alpha = +50.0$, entropy actually *increased* slightly to $1.2326$. Under extreme negative steering ($\alpha = -50.0$), it increased to $1.3291$.
*   **Implication**: The attention map does not collapse to a single coordinate (singularity). Instead, extreme steering acts as a disruptive, destabilizing noise field that spreads attention out, increasing overall entropy.

### H2 (Horizon Expansion / Gravitational Pull): DISPROVED ❌
*   **Preregistered Criterion**: Normalized event horizon radius ($R_s / N$) exceeds $0.80$ at $\alpha_{steer} = 50.0$.
*   **Observed**: Normalized horizon remained nearly flat, at $0.1437$ (baseline), $0.1434$ ($\alpha = +50.0$), and $0.1631$ ($\alpha = -50.0$).
*   **Implication**: Even under extreme semantic force, the model does not form an inescapable "black hole" token that captures long-range attention from across the entire sequence. Causal masking and query-key formatting preserve the localizing attention decay structure.

### H3 (Horizon-Mass Correlation Breakdown): DISPROVED ❌
*   **Preregistered Criterion**: Pearson correlation coefficient between token mass and event horizon drops below $0.50$ at $\alpha_{steer} = 50.0$.
*   **Observed**: The correlation remains exceptionally high and stable across the entire sweep ($r \approx 0.878$ to $0.892$).
*   **Implication**: The linear Schwarzschild-like spacing structure is extremely robust and does not break down under extreme steering. This confirms that the linear correlation is a structural invariant of causally masked attention.

### H4 (Lensing Magnification Collapse): DISPROVED / PARTIALLY SUPPORTED ❌
*   **Preregistered Criterion**: Lensing magnification ratio $A_{high}/A_{low}$ drops by $\ge 30\%$ from its peak at moderate steering.
*   **Observed**: Lensing ratio peaked at $\alpha = +20.0$ ($6.9959$) and decreased to $6.4430$ at $\alpha = +50.0$ (a drop of $7.9\%$). Under negative steering, it dropped from the baseline to $5.4973$ at $\alpha = -50.0$ (a drop of $20.0\%$).
*   **Implication**: While lensing magnification does indeed peak at moderate-to-high steering scales ($\alpha \approx 20.0$) and starts to degrade as steering goes to extreme ranges, the drop does not meet the preregistered $30\%$ threshold. The lensing mechanism is resilient to extreme saturation.

---

## 3. Physical Analogy & Interpretation

These results provide crucial evidence on the nature of the "attention as gravity" analogy:
1.  **Resilience over Collapse**: Standard transformer attention has built-in stabilizers (softmax normalization and causal masks) that prevent mathematical singularities or "black hole collapses." Softmax scales inputs to probability coordinates between 0 and 1, ensuring that the total mass is conserved ($\sum A(i, j) = 1.0$) and bounds the maximum size of event horizons.
2.  **Destabilization via Noise**: At extreme steering amplitudes ($\pm 50.0$), the model's activations are pushed far outside their typical training manifold. Rather than collapsing into a singular state, the attention matrices become noisier and flatter (as seen by the rise in entropy).
3.  **Stability of the Space-Time Invariant**: The linear correlation between mass and horizon is a structural invariant ($r \approx 0.88-0.89$) that is unaffected by extreme semantic steering.
