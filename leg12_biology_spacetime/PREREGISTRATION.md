# Leg 12 — Pre-Registration: Geometry of Cellular Stress Response Networks

This document pre-registers our hypotheses, experimental setup, and success criteria for **Leg 12: Biology Spacetime & Stress Response Network Curvature** on the STRING protein-protein interaction (PPI) network.

---

## 1. Experimental Setup

*   **Database**: STRING database.
*   **Species**: Yeast (*Saccharomyces cerevisiae*, Taxon ID `4932`) or Human (Taxon ID `9606`).
*   **Target Proteins (Yeast)**:
    *   *Stress/Chaperone Hubs*: `HSP82`, `SSA1`, `HSF1`, `SLT2`, `YAP1`
    *   *Housekeeping Controls*: `TDH3`, `ACT1`, `TUB1`
*   **Target Proteins (Human)**:
    *   *Stress/Chaperone Hubs*: `HSP90AA1`, `HSPA1A`, `HSF1`, `MAPK1`, `TP53`
    *   *Housekeeping Controls*: `GAPDH`, `ACTB`, `TUBB`
*   **Network Parameters**:
    *   Add up to 15 closely interacting partner nodes to form a full functional community.
    *   Medium confidence score threshold (400) for edge inclusion.
*   **Stress Perturbation Sweep**:
    *   Scale the vertex weights $w_v$ of the Stress/Chaperone Hubs by $\gamma \in [1.0, 10.0]$ in steps of $1.0$.
    *   Keep baseline housekeeping controls and added neighbor vertex weights at $w_v = 1.0$.
*   **Curvature Metric**: Weighted Forman-Ricci Curvature (FRC) for each edge:
    $$\text{Ric}(e) = w_e \left( \frac{w_{v_1}}{w_e} + \frac{w_{v_2}}{w_e} - \sum_{e_{v_1} \sim e} \frac{w_{v_1}}{\sqrt{w_e w(e_{v_1})}} - \sum_{e_{v_2} \sim e} \frac{w_{v_2}}{\sqrt{w_e w(e_{v_2})}} \right)$$

---

## 2. Hypotheses & Success Criteria

### H1 (Local Curvature Warping / Gravitational Shielding)
*   **Hypothesis**: Chaperone-connected edges will warp their curvature in the positive direction as their abundance (vertex weight) scales up under stress, while housekeeping-connected edges remain flat.
*   **Success Criteria**: Chaperone-connected edges must show an average FRC increase of $\ge 5.0$ FRC units at $\gamma = 10.0$ compared to baseline ($\gamma = 1.0$). Housekeeping-only edges must change by $< 1.0$ FRC unit.

### H2 (Topological Polarization / Extremal Curvature Shift)
*   **Hypothesis**: Under stress, the network will polarize, concentrating positive curvature around the stress hub and leaving the rest of the network connected by highly negative-curvature bottleneck edges.
*   **Success Criteria**: The variance of edge curvatures across the entire network must increase by $\ge 30\%$ at $\gamma = 10.0$ compared to baseline.
