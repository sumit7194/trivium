# Leg 6 — Pre-registration: leg-3 regime prediction (direct vs. indirect observation)

*Frozen 2026-06-17, before running the regime comparison. Discipline: THE_BRIDGE.md §2, §4A.*

This leg implements the **Regime Prediction** test: we verify the hypothesis that representation scrambling occurs under generic updates *only when the system requires state reconstruction from a time series (indirect observation)*. When the state is observed directly, no scrambling occurs.

---

## 1. The Core Idea

We simulate a conserved 3D state rotating under a sequence of controls (SO(3) rotations). We compare two observation regimes:
1.  **Direct Regime**: The full 3D state vector is observed directly at each step (plus noise).
2.  **Indirect Regime**: Only a single fixed projection $y(t) = \mathbf{P} \cdot \mathbf{x}(t)$ is observed at each step, requiring the model to reconstruct the 3D state from the time series.

We train two models in both regimes:
*   **Generic Model**: Free addition-based state updates (no structural constraints).
*   **Orthogonal Model**: Enforced SO(3) rotation-based updates (symmetry-preserving).

We define the **scramble gap** as:
$$\text{Gap} = R^2_{kNN} - R^2_{linear}$$
A large gap ($\ge 0.20$) indicates that information is present in the latent representation but stored in a scrambled, non-linear way (illegible). A small gap ($< 0.15$) with high linear $R^2$ indicates the state is legible.

---

## 2. Frozen Hypotheses & Success Criteria

*   **H1 (Direct Legibility)**: In the Direct observation regime, both the Generic model and the Orthogonal model will maintain high linear legibility of the conserved state ($R^2_{linear} \ge 0.8$, and scramble gap $< 0.15$). No scrambling occurs.
*   **H2 (Indirect Scrambling)**: In the Indirect observation regime, the Generic model will scramble the representation (scramble gap $\ge 0.20$ and $R^2_{linear} < 0.70$), while the Orthogonal model will remain legible (scramble gap $< 0.15$ and $R^2_{linear} \ge 0.75$).
*   **H3 (Erosion)**: In the Indirect regime, the Generic model's linear legibility will decrease significantly from the early part of the path to the late part of the path (erosion $\ge 0.15$), whereas the Orthogonal model will resist this erosion (erosion $< 0.10$).

---

## 3. Implementation Checklist

-   [ ] Implement `leg6_regime_prediction/code/regime_prediction.py` simulating both direct and indirect observation regimes.
-   [ ] Train Generic and Orthogonal models for both regimes.
-   [ ] Measure Ridge vs. kNN $R^2$ of the decoded conserved state.
-   [ ] Verify the scramble signature is isolated to the Generic-Indirect configuration.
-   [ ] Write findings in `leg6_regime_prediction/FINDINGS.md`.
