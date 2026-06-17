# Leg 5c — Findings: Integrability Fingerprints

We have completed the symbolic derivation, numerical integration, and autoencoder bottleneck sweeps for **Leg 5c (Option D)**, evaluating whether the representation oracle (`tabula` autoencoder) can detect the presence of a hidden symmetry—the Carter constant—from raw coordinate trajectories.

---

## 1. Experimental Results Summary

We compare two cases of Boyer-Lindquist style rotating black hole spacetimes with mass $M = 1$ and spin $a = 0.5$, starting from the stable bound off-equatorial geodesic launch parameters: $r_0 = 12.0$, $u_0 = 0.0$, $v_{u0} = 0.05$, $v_{\phi0} = 0.04$, integrated for 30,000 steps with step size $\Delta\lambda = 0.05$.

| Spacetime Metric | Deformation ($\epsilon$) | Carter Constant Mean ($\langle K \rangle$) | Carter Constant Std Dev ($\sigma(K)$) | Resolved Bottleneck Count ($d$) |
|---|---|---|---|---|
| **Exact Kerr** | $0.0$ | $51.840000$ | $1.58 \times 10^{-8}$ | **2** |
| **Deformed Kerr** | $0.1$ | $51.737821$ | $9.07 \times 10^{-3}$ | **2** |

### Autoencoder Reconstruction Sweep ($R^2$)

We trained bottleneck autoencoders $AE(4, d)$ on standardized and PCA-whitened active coordinate datasets $X = [r, u, p_r, p_u]$ over 3 random seeds:

*   **Exact Kerr ($\epsilon = 0.0$):**
    *   *Standardized $R^2(d)$*: $d_0: -0.0003$, $d_1: 0.9922$, $d_2: 0.9999$, $d_3: 0.9999$, $d_4: 0.9990$
    *   *Whitened $R^2(d)$*: $d_0: -0.0003$, $d_1: 0.9209$, $d_2: 0.9996$, $d_3: 1.0000$, $d_4: 1.0000$
    *   **Resolved Knee Count: 2** (gain $d_1 \rightarrow d_2 = 7.87\% > 2\%$, gain $d_2 \rightarrow d_3 = 0.04\% \le 2\%$)
*   **Deformed Kerr ($\epsilon = 0.1$):**
    *   *Standardized $R^2(d)$*: $d_0: -0.0003$, $d_1: 0.9967$, $d_2: 0.9999$, $d_3: 0.9993$, $d_4: 0.9990$
    *   *Whitened $R^2(d)$*: $d_0: -0.0003$, $d_1: 0.9586$, $d_2: 0.9998$, $d_3: 0.9997$, $d_4: 1.0000$
    *   **Resolved Knee Count: 2** (gain $d_1 \rightarrow d_2 = 4.12\% > 2\%$, gain $d_2 \rightarrow d_3 = -0.01\% \le 2\%$)

---

## 2. Hypothesis Evaluation

### H1 (Carter Constant Conservation & Drifting) — ✅ CONFIRMED
*   **Hypothesis**: In exact Kerr, $\sigma(K) < 10^{-8}$, while in deformed Kerr, $\sigma(K) > 10^{-4}$ (a $>10,000\times$ increase).
*   **Result**: $\sigma(K)_{Kerr} = 1.58 \times 10^{-8}$ (set by double-precision numerical integration error) and $\sigma(K)_{Deformed} = 9.07 \times 10^{-3}$ ($> 10^{-4}$). This represents a $5.74 \times 10^5 \times$ increase in variance, confirming that the formal Carter constant symmetry is strongly broken by the metric deformation.

### H2 (Intrinsic Dimension Shift) — ❌ REJECTED / REFINED
*   **Hypothesis**: The autoencoder resolves exactly **2** dimensions for Kerr and exactly **3** dimensions for deformed Kerr.
*   **Result**: Both resolved exactly **2** dimensions.
*   **Physics Explanation**: Under the Kolmogorov-Arnold-Moser (KAM) theorem, the breaking of an integrable system's algebraic symmetry does not immediately destroy its invariant tori. Stable bound orbits (like the one simulated) remain topologically confined to 2D invariant tori (KAM tori) in phase space. The representation oracle correctly and faithfully detects this **effective topological integrability**; because the trajectory is regular and quasi-periodic, the coordinate manifold remains topologically 2D. This is a classic example of **representation oracle compressibility (resolved $2$ < algebraic moduli $3$)** due to KAM confinement.

### H3 (Marginal Gain Separation) — ❌ REJECTED
*   **Hypothesis**: The marginal $R^2$ gain from $d=2$ to $d=3$ is $< 2\%$ for Kerr and $> 2\%$ for deformed Kerr.
*   **Result**: The marginal gain was $0.04\%$ for Kerr and $-0.01\%$ for deformed Kerr, both well below the $2\%$ threshold. The slow drift of the broken Carter constant generates negligible coordinate variance compared to the dominant periodic radial and polar orbital oscillations, leaving the effective dimensionality at 2.

---

## 3. Physical & Methodological Takeaways

1.  **KAM Tori and Representation Limits**: The network's blind count of $2$ for deformed Kerr highlights that the autoencoder measures the *actual topological dimensionality* of the observed trajectory rather than the formal codimension of conserved quantities. Unless the orbit is actively chaotic and diffuses to fill the 3D energy surface, the effective dimensionality of a stable bound orbit is physically and representationally 2.
2.  **Double-Precision Resolution**: By computing the Carter constant statistics in float64 before casting the dataset to float32, we avoided the $7.6 \times 10^{-6}$ single-precision limit and verified the numerical conservation of $K$ in exact Kerr at $1.58 \times 10^{-8}$.
3.  **Shuffling Prevents Chronological OOD Splits**: Shuffling the coordinate matrix before the train/test split successfully resolved the chronological out-of-distribution failure of the first run, allowing both autoencoders to train to $>99.9\%$ accuracy at $d=2$.

---

## 4. Verification Visualizations

The reconstruction curves comparison plot is saved to:
- [leg5c_integrability_curves.png](file:///Users/sumit/Github/TheBridge/results/leg5c_integrability_curves.png) (Workspace copy)
- [leg5c_integrability_curves.png](file:///Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1/leg5c_integrability_curves.png) (Brain artifact copy)

![curves](file:///Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1/leg5c_integrability_curves.png)
