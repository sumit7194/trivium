# Leg 11 — Pre-Registration: Fine-Grained Lensing and Qualitative Collapse

This document pre-registers our hypotheses, experimental setup, and success criteria for **Leg 11: Lensing Dynamics and qualitative collapse sweeps** on Qwen3-4B.

---

## 1. Experimental Setup

*   **Model**: Qwen3-4B (HuggingFace cached).
*   **Vector**: Intellectual humility virtue vector at Layer 14.
*   **Hook**: Additive steering hook at Layer 14: $h' = h + \alpha \cdot v_{normalized}$.
*   **Data for Lensing Sweeps**: The 50 sentences used in Leg 10/10d.
*   **Alphas for Lensing Sweeps**: $\alpha \in [0.0, 50.0]$ in steps of $2.0$ (26 points).
*   **Prompts for Generation Collapse Sweeps**:
    1. "The primary goal of science is"
    2. "When faced with a hard mathematical problem, a researcher should"
    3. "Artificial intelligence will shape the future by"
    4. "In history, the most successful societies were those that"
    5. "To understand the universe, one must first study"
*   **Alphas for Generation Collapse**: $\alpha \in \{0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0\}$.
*   **Generation Parameters**: Max new tokens = 50, temperature = 0.7, top_p = 0.9.

---

## 2. Hypotheses & Success Criteria

### H1 (Lensing Transition Curve)
*   **Hypothesis**: The lensing magnification ratio $A_{high}/A_{low}$ will exhibit a smooth concave shape. It will peak at a moderate steering value ($10.0 \le \alpha \le 20.0$) where the humility feature is amplified without completely drowning out sequence structure, and then decline smoothly as the representation becomes saturated and noisy.
*   **Verification Metric**: Plot the lensing ratio vs. $\alpha$ and find the peak. The decline must be continuous without chaotic fluctuations (orderly transition).

### H2 (Qualitative Coherence Collapse / Semantic Event Horizon)
*   **Hypothesis**: Model generation outputs will exhibit a sharp phase transition from semantically coherent (concept-steered) to incoherent (syntax breakdown, loops) at a critical steering scale $\alpha_{crit}$. We predict $\alpha_{crit}$ will lie in the range $[20.0, 30.0]$.
*   **Verification Metric**:
    *   Measure average token entropy of generated sequences as a proxy for coherence.
    *   Inspect text quality qualitatively across different $\alpha$ levels.
    *   Identify the exact range where coherence drops and mark it as the model's "semantic event horizon."
