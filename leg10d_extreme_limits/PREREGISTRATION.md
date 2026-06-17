# Leg 10d — Pre-registration: Extreme Steering Limits (The Black Hole Collapse)

*Frozen 2026-06-18, before running the extreme steering sweep. Discipline: THE_BRIDGE.md §2, §6.*

This leg tests the behavior of Qwen3-4B's attention maps under extreme steering scales ($\alpha_{steer} \le \pm 50.0$) using the intellectual humility vector at Layer 14. We aim to identify if and when the attention geometry collapses into a "black hole" singularity.

---

## 1. Hypotheses & Predictions

*   **H1 (Entropy Collapse / Singularity)**: As steering scale $\alpha_{steer}$ grows to extreme positive values ($+50.0$), the average attention entropy $H$ of steered layers will collapse toward $0.0$, indicating that attention is focused entirely on a single coordinate (the steered feature's "singularity").
*   **H2 (Horizon Expansion / Gravitational Pull)**: For extreme positive steering, the average event horizon radius $R_s$ will expand to fill the entire sequence length ($R_s \to N - 1$), showing that the black hole token exerts an inescapable long-range gravitational pull.
*   **H3 (Horizon-Mass Correlation Breakdown)**: At extreme steering scales, the tight linear relation between token mass $M$ and horizon $R_s$ will break down (correlation coefficient $r$ drops below $0.50$), because the black-hole token will dominate all event horizons, saturating them at $R_s \approx N - 1$ regardless of individual token masses.
*   **H4 (Lensing Magnification Collapse)**: The lensing magnification ratio $A_{high}/A_{low}$ will peak at moderate steering scales, but will collapse back toward $1.0$ at extreme scales ($\pm 50.0$), as the singular black-hole token captures all attention, silencing the direct path $A(i+2, i)$ and rendering lensing calculations undefined or collapsed.

---

## 2. Agreement & Success/Collapse Criteria

*   **Entropy Collapse (H1) is verified** if the average attention entropy across steered layers drops by at least 50% at $\alpha_{steer} = 50.0$ compared to the baseline ($\alpha_{steer} = 0.0$).
*   **Horizon Expansion (H2) is verified** if the average event horizon radius normalized by sequence length ($R_s / N$) exceeds $0.80$ at $\alpha_{steer} = 50.0$.
*   **Correlation Breakdown (H3) is verified** if the Pearson correlation coefficient between mass and horizon drops below $0.50$ at $\alpha_{steer} = 50.0$.
*   **Lensing Collapse (H4) is verified** if the lensing ratio $A_{high}/A_{low}$ at $\alpha_{steer} = 50.0$ is significantly lower than its peak value at moderate steering (e.g. drops by $\ge 30\%$ from the peak).
