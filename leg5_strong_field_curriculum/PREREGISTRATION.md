# Leg 5 — Pre-registration: the strong-field curriculum (shadow-edge fidelity)

*Frozen 2026-06-17, before running the curriculum sweep. Discipline: THE_BRIDGE.md §2, §5.*

This leg implements the **Strong-field Curriculum**. We study how exact theory-guided sampling (concentrating training rays around the critical winding region) shapes the accuracy of a neural network's strong-field representation of gravity.

---

## 1. The Core Idea

In general relativity, the Schwarzschild photon sphere $r_{ps} = 3M$ and the shadow boundary $b_{crit} = 3\sqrt{3} \approx 5.196M$ are exact critical features. When training a neural network (`tabula`'s `Photon` model) on simulated null geodesic segments:
*   A **uniform/naive** training set contains very few rays in the near-critical winding region, since the critical impact parameter window is extremely narrow.
*   A **targeted curriculum** uses the exact location of the critical orbit $b_{crit} = 3\sqrt{3}$ (known from theory) to focus sampling in the critical winding window $[5.2, 5.6]$ where light winds around the hole.

We compare two datasets with the **exact same number of total training points** to control for capacity/data size:
*   **Curriculum A (Uniform)**: Impact parameters sampled uniformly from $[4.8, 14.0]$.
*   **Curriculum B (Targeted)**: Impact parameters consisting of a sparse background + extra near-critical winding rays in $[5.2, 5.6]$.

---

## 2. Frozen Hypotheses & Success Criteria

-   **H1 (Higher shadow-edge accuracy)**: The predicted shadow boundary $b_{crit}$ from Curriculum B (targeted) will be closer to the exact value $3\sqrt{3} \approx 5.196$ than Curriculum A.
-   **H2 (Better photon sphere location)**: The predicted photon sphere radius $r_{ps}$ from Curriculum B will be closer to the exact value $3.000$ than Curriculum A.
-   **H3 (Quantifiable benefit)**: The relative error in $b_{crit}$ for Curriculum B will be at least **1.5x smaller** than the relative error for Curriculum A.

---

## 3. Implementation Checklist

-   [ ] Implement `leg5_strong_field_curriculum/code/strong_field_curriculum.py` based on `SpaceTime`'s `78_photon_shadow.py` and `83_fidelity_curve.py`.
-   [ ] Generate datasets for both curricula with identical point counts.
-   [ ] Train both networks (averaging over multiple seeds).
-   [ ] Measure $b_{crit}$ (using batched ray capture) and $r_{ps}$ (from zero of learned force).
-   [ ] Write findings in `leg5_strong_field_curriculum/FINDINGS.md`.
