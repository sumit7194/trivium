# Leg 10c — Pre-registration: Stress-Testing Attention Gravity

*Frozen 2026-06-18, before running the stress-test battery. Discipline: THE_BRIDGE.md §2, §6.*

This leg runs a rigorous control battery to validate or disprove our claims of attention as gravity.

---

## 1. Stress-Test Hypotheses & Predictions

*   **T1 (Sample Size Expansion)**: Running on 300 diverse sentences (instead of 50) will yield baseline metrics ($r \approx 0.88$, $A_{high}/A_{low} > 1.0$) with very narrow error margins, confirming statistical robustness.
*   **T2 (Random Vector Steering)**: Steering with a random direction vector of equivalent norm will show no monotonic relationship with the epistemic mass ratio (H4) and will lead to erratic, non-monotonic trends in other metrics.
*   **T3 (Random Weights Model)**: In a randomly initialized weights version of Qwen3-4B:
    *   The event horizon correlation $r$ will drop significantly (to $\le 0.30$) or be non-existent.
    *   The lensing ratio $A_{high}/A_{low}$ will collapse toward 1.0 (no magnification).
    This will prove that attention gravity is a learned property of semantic representation, not an architectural artifact of Softmax and causal masking.
*   **T4 (Early Layer Control)**: Since steering is applied at Layer 14, attention metrics in upstream layers 0–13 will exhibit exactly $0.0$ variance across all steering scales $\alpha_{steer}$, proving no backward leaks.

---

## 2. Agreement & Success/Failure Criteria

*   **T1 is verified** if the baseline ($\alpha_{steer}=0$) Pearson correlation remains $\ge 0.80$ and the lensing ratio remains $\ge 5.0$ over 300 sentences.
*   **T2 is verified** if the epistemic mass ratio curve under random vector steering is non-monotonic or flat, and fails the monotonic trend.
*   **T3 is verified** if the random model's average Pearson correlation is $\le 0.30$ and the average lensing ratio is $\le 1.5$ (collapsed).
*   **T4 is verified** if the variance of all attention metrics in layers 0–13 across all $\alpha_{steer}$ values is exactly $0.0$.
