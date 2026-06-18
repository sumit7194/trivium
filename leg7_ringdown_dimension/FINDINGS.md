# Leg 7 — Findings: ringdown intrinsic dimension (MDL / bottleneck count)

*Run 2026-06-17. Hypothesis verification criteria frozen in [PREREGISTRATION.md](PREREGISTRATION.md) before execution.*

## Result in one line

Adding **synthetic Gaussian noise at a LIGO-like SNR (~7)** collapses the autoencoder's
resolvable parameter count to **0**, while idealized (noise-free) waveforms appear **4D** to
a standard autoencoder even when they are physically 2D, because frequency-dependent
phase-shift curvature winds the waveform manifold. (Leg 7b shows an FFT-magnitude
preprocessing that undoes the curvature inflation.)

> **Two honest corrections (2026-06-18):**
> 1. **Not real LIGO noise.** PREREGISTRATION described Family 3 as injection into "real
>    LIGO O4 noise," but the committed `gen_ringdowns.py` adds **unit-variance Gaussian
>    noise** (`rng.normal(0, 1, ...)`), not real detector noise. Every "LIGO noise" claim
>    below should be read as "synthetic Gaussian noise at a comparable SNR." The
>    information-limited conclusion is still suggestive, but it was *not* demonstrated on
>    real noise — to honor the prereg one would inject into off-source real strain.
> 2. **"Two detectors" is cosmetic.** The 328-dim vector is one 164-sample waveform
>    duplicated (`x1` and `x2` are computed identically, with no per-detector noise or
>    projection). The doubling does not change the intrinsic dimension, but the
>    two-detector framing is not real.

---

## 1. The Outcome Table (Knee Dimension Counts)

| Configuration | Target Manifold | Resolved Count (Whitened) | Predicted Count | Verdict |
|---|---|---|---|---|
| **Kerr Locked (Family 1)** | 2D ($M, \chi$) | **4** | 2 | ❌ **H1: FALSE** (Manifold curvature) |
| **Kerr Free (Family 2)** | 4D ($M, \chi, A_{221}, \phi_{221}$) | **4** | 4 | ✅ **H2: TRUE** |
| **Synthetic Gaussian noise (Family 3)** | 1D/2D + Noise | **0** | 1 | ❌ **H3: FALSE** (Noise floor collapse; synthetic noise, not real LIGO) |

---

## 2. Hypothesis Verification

*   **H1 (Locked dim is 2): FALSE.** The autoencoder resolved 4 dimensions for the locked Kerr case.
*   **H2 (Free dim is 4): TRUE.** The autoencoder resolved 4 dimensions.
*   **H3 (Noise dim collapses to 1): FALSE.** The resolved dimension collapsed completely to **0** rather than 1.

---

## 3. Physical & Machine Learning Interpretation

This leg reveals two critical insights about representation learning on physical waveforms:

### The Phase-Shift Curvature Problem (H1)
Although the Kerr Locked waveform is topologically a 2-dimensional manifold ($M$ and $\chi$), the autoencoder resolves **4** dimensions. 
*   **The Cause:** Damped sinusoids are highly non-linear functions of frequency $f(M, \chi)$ and decay time $\tau(M, \chi)$. Varying the frequency causes the peaks of the wave to shift in time. In the high-dimensional vector space ($\mathbb{R}^{328}$), this phase shifting creates a highly curved, winding manifold.
*   **The MLP Limitation:** A standard bottleneck autoencoder requires extra coordinate capacity (4 dimensions instead of 2) to unfold and parameterize this curved manifold with high held-out $R^2$ ($> 90\%$). This explains why the "free" and "locked" cases both resolved to 4—the network spent its capacity on phase untangling rather than parameter counting.

### The Noise Floor Collapse (H3)
In the presence of **synthetic Gaussian noise** at a LIGO-like SNR ($\approx 7$; *not* real
detector noise — see the correction above), the whitened $R^2(d)$ curve remains negative or
zero for all bottleneck widths. The resolved dimension collapses to **0**.
*   **The Cause:** The signal variance is completely dominated by the random noise in whitened space (linear PCs kept = 328, with a flat spectrum).
*   **The Domain Gap Connection (suggestive, not proven on real data):** This is consistent
    with a representation-level explanation for `deepstrain`'s tone-counting failure (Leg 2):
    at this SNR the physical parameters are unresolvable by direct representation learning on
    raw waveforms, pointing to an information-limited rather than legibility-limited gap.
    Because the noise here is synthetic Gaussian, this corroborates rather than demonstrates
    the real-data conclusion — Leg 2 (which uses real O4 noise) is the load-bearing evidence
    for that claim.
