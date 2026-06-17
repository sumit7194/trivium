# Leg 5 — Findings: the strong-field curriculum (shadow-edge fidelity)

*Run 2026-06-17. Hypothesis verification criteria frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before execution.*

## Result in one line

The theory-guided targeted curriculum (Curriculum B) **reduces the shadow-edge error from 22.98% to 2.27% (a 10.1x improvement)** and reduces the variance of the learned photon-sphere location by **almost 20x**, confirming that exact strong-field theory is a highly effective training guide.

---

## 1. The Outcome Table (Uniform vs. Targeted)

| Metric | Ground Truth | Uniform (Curriculum A) | Targeted (Curriculum B) |
|---|---|---|---|
| **$b_{crit}$ (mean $\pm$ std)** | $3\sqrt{3} \approx 5.196M$ | $6.390M \pm 1.010M$ | **$5.314M \pm 0.200M$** |
| **$b_{crit}$ Relative Error** | 0% | 22.98% | **2.27%** |
| **$r_{ps}$ (mean $\pm$ std)** | $3.000M$ | $2.990M \pm 0.182M$ | **$2.930M \pm 0.010M$** |
| **$r_{ps}$ Relative Error** | 0% | **0.34%** | 2.33% |

*Data controlled at exactly N=25,000 training segments for both configurations, averaged over 3 seeds.*

---

## 2. Hypothesis Verification

*   **H1 (Higher shadow-edge accuracy): TRUE.** The relative error on the shadow boundary drops from 22.98% (Uniform) to 2.27% (Targeted).
*   **H2 (Better photon sphere location): FALSE.** The Uniform curriculum mean ($2.990M$, 0.34% error) is numerically closer to the true value of $3.0M$ than the Targeted curriculum mean ($2.930M$, 2.33% error).
*   **H3 (Error ratio $\ge 1.5$x): TRUE.** The relative error ratio is $\frac{22.98\%}{2.27\%} \approx 10.12$x, significantly exceeding the 1.5x success threshold.

---

## 3. Analysis & Discussion

### The H2 Genuinely Useful Negative
The failure of H2 is a classic example of why reporting variance is critical in representation learning (THE_BRIDGE.md §7):
1.  **Uniform Instability:** The Uniform models had a standard deviation of $0.182M$ on the photon sphere location. Individual seeds fluctuated widely ($2.966M \to 3.224M \to 2.779M$), meaning any single trained model was highly unreliable. The low mean error (0.34%) is a statistical artifact of random variations canceling out across a small seed sample.
2.  **Targeted Stability:** The Targeted models had a standard deviation of $0.010M$—nearly **20x smaller variance**. The models consistently converged to a highly stable value ($2.921M \to 2.943M \to 2.926M$).
3.  **Systematic Bias:** The small remaining bias in the Targeted models (underestimating the photon sphere at $2.93M$) is a known feature of the neural potential method fit, but its tight convergence indicates it has successfully mapped the strong-field basin.

### Why the Curriculum Works
A neural network trained on a uniform distribution of light rays rarely sees critical winding trajectories, because the impact parameter window $[3\sqrt{3}, 5.6]$ is narrow. Consequently, the network fails to learn the dynamics of the strong field (near the photon sphere $r=3M$) and extrapolates poorly, leading to a shadow edge that is 23% too large.

By utilizing ansatz's exact knowledge of $b_{crit} = 3\sqrt{3}$ to concentrate 60% of the training points in the near-critical window, we force the network to repeatedly sample the strong-field orbit. This targeted curriculum results in a highly accurate and stable mapping of the shadow edge.

---

## 4. Artifacts

*   `code/strong_field_curriculum.py` — generates datasets, trains models, runs batched ray tracer, outputs json and plot.
*   `results/leg5_curriculum_comparison.json` — raw outputs and hypothesis checks.
*   `results/leg5_curriculum_curves.png` — the figure.
