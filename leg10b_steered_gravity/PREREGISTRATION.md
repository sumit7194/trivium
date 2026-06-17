# Leg 10b — Pre-registration: Steered Attention as Gravity in Qwen3-4B

*Frozen 2026-06-18, before running the steering sweep script. Discipline: THE_BRIDGE.md §2, §6.*

This leg tests the effects of activation steering along the intellectual humility virtue vector on the attention gravity metrics of Qwen3-4B using a set of 50 text sentences.

---

## 1. Hypotheses & Predictions

*   **H1 (Steered Decay)**: Positive steering along the virtue vector increases the power-law decay exponent $\alpha$ (making attention more localized), while negative steering decreases $\alpha$ (making attention more diffuse).
*   **H2 (Horizon Warping)**: The event horizon radius $R_s$ retains a strong linear correlation with token mass $M$ (Pearson $r \ge 0.60$), but the slope of the mass-horizon relation (effective gravity $G_{eff}$) increases with positive steering and decreases with negative steering.
*   **H3 (Lensing Modulation)**: The lensing magnification ratio $A_{high}/A_{low}$ is modulated by steering: positive steering increases the ratio, and negative steering decreases it.
*   **H4 (Token Mass Redirection)**: Steering along the intellectual humility vector redirects attention mass toward epistemic uncertainty/hedging tokens. The ratio of the mean attention mass of hedging tokens to control tokens increases monotonically with positive steering.

---

## 2. Agreement & Success Criteria

*   **H1 is verified** if the average fitted power-law decay exponent $\alpha$ over steered layers (layers 15–35) is higher for $\alpha_{steer} > 0$ than for $\alpha_{steer} = 0$, and lower for $\alpha_{steer} < 0$.
*   **H2 is verified** if the Pearson correlation coefficient between $R_s$ and $M$ remains $\ge 0.60$ for all sweep values, and the fitted slope of $R_s(M)$ is monotonic with respect to $\alpha_{steer}$.
*   **H3 is verified** if the average lensing ratio over steered layers is monotonic with respect to $\alpha_{steer}$.
*   **H4 is verified** if the ratio of mean attention mass of hedging tokens ("currently", "incompatible", "requires", "exotic", "limits", "candidates", "hypothetical") to control tokens ("theory", "mass", "star", "space", "light", "field", "core") is monotonic with respect to $\alpha_{steer}$.
