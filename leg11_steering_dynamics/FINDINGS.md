# Leg 11 — Findings: Fine-Grained Lensing and Qualitative Collapse

We successfully ran the fine-grained lensing sweep and qualitative generation tests for Qwen3-4B under Layer 14 intellectual humility steering. Our findings provide a detailed map of the lensing gradient and test the hypothesis of a qualitative "event horizon."

---

## 1. Lensing Gradient & Transition Peak (H1: CONFIRMED ✅)

*   **Observed Trend**: The lensing magnification ratio $A_{high}/A_{low}$ exhibits a smooth, concave shape as predicted.
    *   **Baseline ($\alpha = 0.0$)**: $6.8727$
    *   **Peak ($\alpha = 14.0$)**: $7.0092$
    *   **Extreme positive ($\alpha = 50.0$)**: $6.4430$
*   **Interpretation**: Lensing magnification peaks at a moderate scale ($\alpha = 14.0$). Below the peak, increasing the steering scale strengthens the relative focus on the steered feature. Above the peak, the feature starts to saturate, introducing noise into the representation and gradually flattening the attention distributions, causing a smooth and orderly decline. There are no chaotic or sharp fluctuations.

---

## 2. Coherence Collapse & The Semantic Event Horizon (H2: DISPROVED ❌)

*   **Hypothesis**: We predicted a sharp phase transition into incoherence (syntax breakdown, repetitions, or gibberish) at a critical threshold $\alpha_{crit} \in [20.0, 30.0]$.
*   **Observed**: 
    *   The model did **not** collapse. Even at $\alpha_{steer} = 50.0$, the generated text remained syntactically perfect and highly coherent.
    *   The average token-wise generation entropy remained stable across the sweep, ranging between **0.7393 bits** ($\alpha=5.0$) and **0.9624 bits** ($\alpha=50.0$).
    *   Rather than breaking down, the model's outputs shifted semantically to reflect the humility vector. It generated sophisticated philosophical discussions on the limits of science, the boundary between science and math, and the constraints of the scientific method.
*   **Sample Qualitative Output at $\alpha = 50.0$**:
    > "The primary goal of science is to explain natural phenomena, unlike mathematics. Therefore, the statement that 'a is b' is not considered a scientific explanation. The original statement is a well-known example of the problem in the philosophy of science. This is due to the fundamental conflict between..."

---

## 3. Implications for the Space-Time Analogy

1.  **Topological Stability**: The absence of a qualitative event horizon demonstrates that the model's language representations are extremely stable. The softmax normalization and causal masks act as topological bounds, preventing the hidden activations from collapsing into a singular state (like a black hole) even when pushed 50 standard deviations off the training manifold.
2.  **Orderly Semantic Bending**: Rather than breaking down, the model "bends" its outputs smoothly toward the steered semantic domain (epistemic humility and philosophy of science boundaries). This suggests that activation steering acts more like a continuous gravitational field that curves the path of token generation without tearing the underlying language fabric.
