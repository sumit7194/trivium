# Leg 9 — Pre-registration: The Representation Horizon (Causal Structure of Neural Networks)

*Frozen 2026-06-18, before training the deep MLP and running the probe sweeps. Discipline: THE_BRIDGE.md §2, §6.*

This leg maps the information-theoretic causal structure of a deep neural network, treating layer depth as a time coordinate and feature decodability as the causal lapse. We identify "representation event horizons" where irrelevant features become unrecoverable, and construct the network's Penrose diagram.

---

## 1. Features & Network Architecture

We generate a synthetic dataset ($N = 10,000$ samples) with input $\mathbf{x} \in \mathbb{R}^{30}$ consisting of three features:
1.  **Target ($y$)**: A non-linear function of 10 input dimensions:
    $$y = \sin(x_1 x_2) + \cos(x_3 + x_4) + x_5^2 - x_6^3 + x_7 x_8 - \tanh(x_9 + x_{10})$$
2.  **Nontarget Invariant ($z_{inv}$)**: A continuous linear combination of another 10 dimensions, irrelevant to $y$.
3.  **Shortcut/Noise ($z_{noise}$)**: A high-frequency, easy-to-decode feature:
    $$z_{noise} = \text{sign}(x_{21} + x_{22} + x_{23}) \cdot \cos(5 \pi x_{24})$$
    which is also irrelevant to $y$.

We train a 6-layer MLP:
*   **Layers**: Input (30) $\to$ Layer 1 (64) $\to$ Layer 2 (64) $\to$ Layer 3 (64) $\to$ Layer 4 (64) $\to$ Layer 5 (64) $\to$ Output Layer 6 (1).
*   **Activations**: GELU on layers 1–5, Linear on layer 6.
*   **Loss**: Mean Squared Error (MSE) against the target $y$.

---

## 2. Frozen Predictions & Hypotheses

*   **H1 (Target Escape)**: The target feature $y$ will escape the representation horizon, maintaining high decodability at the final layer:
    $$R^2_{linear} \ge 0.80 \quad \text{and} \quad R^2_{kNN} \ge 0.80 \quad \text{at } l = 6$$
*   **H2 (Nontarget Horizon)**: The irrelevant invariant $z_{inv}$ will start with high decodability at the input ($l=0$) but will decay monotonically as it flows deeper, crossing the horizon ($R^2 < 0.05$) at a layer $l_{horizon} < 6$.
*   **H3 (Shortcut Decay)**: The network will discard the high-frequency shortcut $z_{noise}$ faster than $z_{inv}$, meaning its horizon layer will be shallower:
    $$l_{horizon}(z_{noise}) < l_{horizon}(z_{inv})$$

---

## 3. Agreement Criteria

*   **H1 is verified** if the output layer ($l=6$) can decode $y$ with $R^2 \ge 0.8$.
*   **H2 is verified** if $z_{inv}$'s $R^2_{kNN}$ falls below $0.05$ at some layer $l < 6$ and remains below $0.05$ for all subsequent layers.
*   **H3 is verified** if the layer at which $R^2_{kNN}(z_{noise}) < 0.05$ is strictly less than the layer at which $R^2_{kNN}(z_{inv}) < 0.05$.
