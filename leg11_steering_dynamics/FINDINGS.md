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

## 3. Honest Methodological Reflection

1.  **Lensing is a Tiny Modulation**: Although the lensing ratio curve (H1) is concave and peaks at $\alpha = 14.0$, the absolute variance is very small ($6.87 \to 7.00$, a $1.8\%$ relative change). This indicates that the "lensing magnification" is a minor modulation of baseline attention routing rather than a major geometric distortion.
2.  **Fluency does not equal correctness**: The model's syntactic coherence remains completely intact at $\alpha = 50.0$ (H2). However, we did not evaluate whether the generated statements are calibrated or correct. High fluency at extreme steering scales may simply mask confident confabulations.
3.  **Metaphor Limits**: The lack of a qualitative collapse confirms that the "event horizon" framing does not hold. Softmax bounds ensure representation stability, causing the model to bend its outputs semantically rather than collapse structurally.

