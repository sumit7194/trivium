# Leg 7b — Pre-Registration: Resolving Phase-Shift Curvature (Option A)

This document pre-registers our hypotheses, experimental setup, and success criteria for **Leg 7b: Resolving Phase-Shift Curvature** in ringdown dimension counting.

---

## 1. Experimental Setup

*   **Database/Model**: Simulated Kerr ringdown waveforms generated using deepstrain's `rdlib` library.
*   **Dataset**: Family 1 (Kerr Locked: 2D manifold parameterizing mass $M$ and spin $\chi$).
*   **Sample size**: 8000 training samples, 800 test samples.
*   **Waveform Representation Modifications**:
    1.  **Baseline**: Raw time-domain waveforms (length 328).
    2.  **FFT Magnitude**: Real Fast Fourier Transform magnitude of the waveforms (length 166).
    3.  **Hilbert Envelope**: Analytic envelope of the waveforms calculated via the Hilbert transform (length 328).
*   **Autoencoder sweeps**: Bottleneck dimensions $d \in \{0, 1, 2, 3, 4, 5\}$, trained for 4000 steps with Adam optimizer, batch size 512.
*   **Metrics**: $R^2$ reconstruction score on whitened representations, knee detection using the marginal gain threshold of $2\%$ (same as Leg 7).

---

## 2. Hypotheses & Success Criteria

### H1 (Baseline Replication)
*   **Hypothesis**: The baseline time-domain autoencoder will resolve $d_{knee} = 4$, replicating the phase-shift curvature manifold inflation found in Leg 7.
*   **Success Criterion**: The resolved dimension for the raw time-domain representation is exactly $4$.

### H2 (FFT Magnitude Dimension Recovery)
*   **Hypothesis**: Transforming the waveforms to their real FFT magnitude spectra removes the time-translation and oscillatory phase shifts, flattening the manifold and allowing the autoencoder to resolve the true $2$-parameter physical dimensionality.
*   **Success Criterion**: The resolved dimension for the FFT magnitude representation is exactly $2$.

### H3 (Hilbert Envelope Dimension Recovery)
*   **Hypothesis**: The Hilbert envelope removes the oscillatory frequency components, leaving only the exponential decay curves. This simplified manifold will resolve to exactly $2$ dimensions (or $1$ if the decay times collapse into a single dominant degree of freedom).
*   **Success Criterion**: The resolved dimension for the Hilbert envelope is $\le 2$.
