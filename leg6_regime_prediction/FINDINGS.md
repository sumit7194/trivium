# Leg 6 — Findings: leg-3 regime prediction (direct vs. indirect observation)

*Run 2026-06-17. Hypothesis verification criteria frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before execution.*

## Result in one line

We confirmed that **representation scrambling occurs ONLY under indirect observation**, and that enforcing orthogonal symmetries (representing conservation laws or Killing vectors) successfully restores representation legibility.

---

## 1. The Outcome Table (Linear vs. Nonlinear $R^2$)

| Configuration | Observation $R^2$ | Linear $R^2$ (Legible) | kNN $R^2$ (Info) | Scramble Gap | Verdict |
|---|---|---|---|---|---|
| **Direct, Orthogonal** | 0.9993 | 0.9996 | 0.9990 | -0.0006 | **Legible** (H1: Pass) |
| **Direct, Generic** | 0.9958 | 0.9915 | 0.9957 | 0.0042 | **Legible** (H1: Pass) |
| **Indirect, Orthogonal** | 0.9373 | 0.8786 | 0.9268 | 0.0482 | **Legible** (H2: Pass) |
| **Indirect, Generic** | 0.6087 | 0.0524 | 0.3640 | **0.3116** | **SCRAMBLED** (H2: Pass) |

---

## 2. Hypothesis Verification

*   **H1 (Direct Legibility): TRUE.** In the Direct observation regime, both models maintain excellent linear legibility ($R^2_{linear} > 0.99$) and negligible scramble gaps ($< 0.01$).
*   **H2 (Indirect Scrambling): TRUE.** In the Indirect observation regime, the Generic model scrambles ($R^2_{linear} = 0.0524$, scramble gap = $0.3116$), while the Orthogonal model remains highly legible ($R^2_{linear} = 0.8786$, scramble gap = $0.0482$).
*   **H3 (Erosion $\ge 0.15$): FALSE.** The erosion in the Indirect-Generic model was $0.0807$. This is because the linear legibility dropped to near-zero ($0.0524$) almost immediately, leaving no room for a gradual $0.15$ erosion over the evaluation window.

---

## 3. Physical & Machine Learning Interpretation

This result validates tabula's refined Leg-3 thesis on the limits of the legibility law:
1.  **The Direct Anchor:** When physical variables are directly observable at each step (e.g. measuring both position and velocity), the data itself acts as a strong linear anchor. The network's latent representation aligns linearly with the coordinates, even without structural constraints.
2.  **The Indirect Scramble:** When observations are indirect (e.g. measuring only a single projection, requiring time-series state reconstruction), the direct anchor is lost. The network is free to scramble the coordinates to minimize loss, destroying linear legibility.
3.  **Structure as a Safeguard:** Enforcing orthogonal updates (which represent Killing symmetries or conservation laws) constrains the latent dynamics. This structural constraint resists coordinate deformation, keeping the representation legible and stable over time.

This has major implications for gravitational wave ML (like `deepstrain`): models reconstructing parameters from 1D strain data are highly susceptible to representation scrambling unless they are explicitly equipped with conservation or symmetry structures.
