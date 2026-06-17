# Leg 7 — Pre-registration: ringdown intrinsic dimension (MDL / bottleneck count)

*Frozen 2026-06-17, before running the dimension sweeps. Discipline: THE_BRIDGE.md §2, §4B, §5.*

This leg applies tabula's bottleneck autoencoder instrument to deepstrain's ringdown waveforms to count their intrinsic degrees of freedom. We investigate how modeling assumptions and LIGO noise affect the resolvable physical parameter space.

---

## 1. Datasets & Configurations

We generate three datasets of 8,000 ringdown episodes each (2 detectors, 164 samples per detector, flattened to 328-dimensional vectors):

1.  **Family 1 (Kerr Locked)**: Idealized two-tone ringdowns where the overtone (221) is locked to the 220 parameters by Kerr equations (a 2-dimensional manifold in $M$ and $\chi$).
2.  **Family 2 (Kerr Free)**: Idealized two-tone ringdowns where the overtone has independent amplitude and phase offsets (a 4-dimensional manifold in $M$, $\chi$, $A_{ratio}$, $\phi_{diff}$).
3.  **Family 3 (LIGO Noise Injected)**: Family 1 injected into real LIGO O4 noise at an SNR level of ~7.

---

## 2. Bottleneck Sweep & Counting Instrument

We sweep autoencoder bottleneck widths $d \in \{0, 1, 2, 3, 4, 5\}$ (3 seeds, 4000 training steps, batch size 256).
The intrinsic dimension count is defined as:
$$\text{Count} = \text{number of widths } d \ge 1 \text{ whose whitened marginal } R^2 \text{ gain exceeds } \tau = 2\%$$

---

## 3. Frozen Predictions & Agreement Criteria

*   **Family 1 (Kerr Locked) count = 2.** The autoencoder will resolve exactly 2 dimensions ($M$ and $\chi$).
*   **Family 2 (Kerr Free) count = 4.** The autoencoder will resolve exactly 4 dimensions ($M$, $\chi$, and the 2 independent overtone degrees of freedom).
*   **Family 3 (LIGO Noise) count = 1.** At GW250114 SNR levels (~7), real noise will obscure the second dimension (spin), collapsing the resolvable dimension to exactly 1 (mass only).

This provides a direct representation-level proof of the domain gap: real LIGO noise collapses the physical degrees of freedom that are learnable from time-series data.

---

## 4. Deliverables

*   `code/gen_ringdowns.py` — generates the datasets.
*   `code/count_bottleneck_rd.py` — performs the sweeps.
*   `code/plot_curves_rd.py` — visualizes the curves and saves the figure.
*   `FINDINGS.md` — documents the results.
