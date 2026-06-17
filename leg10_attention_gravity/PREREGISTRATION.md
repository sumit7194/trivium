# Leg 10 — Pre-registration: Attention as Gravity in Qwen3-4B

*Frozen 2026-06-18, before running the attention extraction script. Discipline: THE_BRIDGE.md §2, §6.*

This leg tests three physical gravity hypotheses on the attention matrices of Qwen3-4B using a set of 50 text sentences.

---

## 1. Hypotheses & Predictions

*   **H1 (Newtonian Falloff)**: The attention weight $A(r)$ decays as a function of word distance $r = |i - j|$ following a power law:
    $$A(r) \propto r^{-\alpha}$$
    with $\alpha > 0$ and a goodness-of-fit $R^2 \ge 0.50$ in the mid-to-late layers of the model.
*   **H2 (Schwarzschild Horizon)**: The attention event horizon radius $R_s$ (the maximum distance from which $A(i, j) \ge 0.05$) scales positively with the token's mass $M_j = \sum_i A(i, j)$, showing a correlation coefficient $r \ge 0.60$.
*   **H3 (Gravitational Shielding)**: The presence of a high-mass intermediate token $j$ (where $M_j > \text{median}$ of the sentence) between $i$ and $k$ ($i < j < k$) will decrease the direct attention $A(i, k)$ by at least 20% compared to cases with a low-mass intermediate token.

---

## 2. Agreement & Success Criteria

*   **H1 is verified** if the fitted power-law exponent $\alpha > 0$ with $R^2 \ge 0.50$ in at least half of the layers.
*   **H2 is verified** if the Pearson or Spearman correlation coefficient between $R_s$ and $M$ is $\ge 0.60$ with $p < 0.01$.
*   **H3 is verified** if the mean ratio of $A(i, k)$ under high-mass intermediate tokens vs. low-mass intermediate tokens is $\le 0.80$ (a 20% reduction or greater).
