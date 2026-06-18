# Leg 5c — Findings: Integrability Fingerprints

**Leg 5c (Option D):** can the representation oracle (`tabula` autoencoder) detect a hidden
symmetry — the Carter constant — from raw coordinate trajectories of an integrable (Kerr)
vs a deformed non-integrable spacetime?

## Result in one line (the honest headline)

**No — the bottleneck count did not fingerprint integrability.** It returned **2 for both**
the exact-Kerr and the deformed orbit, i.e. it failed to distinguish the integrable from the
non-integrable case, which was the thing the leg set out to detect (H2 and H3 both
REJECTED). There is a plausible physical reason it *should* fail for a *bound* orbit (KAM
tori keep a stable orbit on a 2-torus whether or not the global symmetry is exactly intact —
see §2), and the Carter constant itself does cleanly track the deformation
($\sigma(K)$ jumps ~$5.7\times10^5$). But the representational fingerprint claimed by the
hypothesis was **not** observed; the KAM story is an *explanation of a negative result*, not
a positive detection.

> **Logged deviations (recorded 2026-06-18, predictions were frozen in PREREGISTRATION).**
> (a) The launch parameters used here differ from the frozen prereg §2 (which specified
> **5 geodesics**, $v_u \in \{0.001\ldots0.005\}$, $v_\phi = 0.035$, **6000 steps**); the
> run used **1 trajectory**, $v_u = 0.05$, $v_\phi = 0.04$, **30000 steps**. This change
> was not flagged at the time and is logged now.
> (b) **Single-trajectory leakage:** one long orbit was shuffled before the train/test
> split, so adjacent integrator steps straddle both splits — the $R^2 > 0.999$ values are
> optimistic for that reason. The *dimension count* (2) is plausibly still right (a regular
> bound orbit lies on a 2-torus), but the high $R^2$ magnitudes should not be read as
> out-of-sample fidelity. A clean redo would split by trajectory / use the prereg's
> multiple independent orbits.

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

### H1 (Carter Constant Conservation & Drifting) — ⚠️ CONFIRMED IN SUBSTANCE, frozen Kerr threshold narrowly missed
*   **Hypothesis (frozen)**: In exact Kerr, $\sigma(K) < 10^{-8}$, while in deformed Kerr, $\sigma(K) > 10^{-4}$.
*   **Result**: $\sigma(K)_{Kerr} = 1.58 \times 10^{-8}$ and $\sigma(K)_{Deformed} = 9.07 \times 10^{-3}$.
    The substantive claim — that the deformation strongly breaks Carter-constant
    conservation — holds decisively ($\sigma(K)$ increases $5.74 \times 10^5\times$, and the
    deformed value clears the $10^{-4}$ bar). **But the frozen Kerr sub-criterion
    $\sigma(K) < 10^{-8}$ was NOT met**: $1.58 \times 10^{-8}$ sits just *above* it, at the
    float64 integration-error floor. Reporting this honestly: H1 passes in substance, fails
    the literal frozen Kerr threshold by a factor of ~1.6. (Previously this was marked a
    clean ✅; corrected 2026-06-18.)

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
3.  **Shuffling traded an OOD failure for a leakage artifact (correction 2026-06-18)**:
    The first run split one trajectory chronologically and failed to generalize; shuffling
    the coordinate matrix before the split fixed that, but shuffling a *single* orbit puts
    adjacent integrator steps in both train and test — which is precisely why the $R^2$ then
    reached $>99.9\%$. So the high accuracy is partly leakage, not pure intrinsic-dimension
    recovery. The intrinsic-dimension *count* (2) is still defensible (a regular bound orbit
    is 2-toroidal), but a methodologically clean run would split by trajectory or use
    multiple independent orbits (as the prereg originally specified).

---

## 4. Verification Visualizations

The reconstruction curves comparison plot is saved to:
- `results/leg5c_integrability_curves.png`
