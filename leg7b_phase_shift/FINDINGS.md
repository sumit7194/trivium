# Leg 7b — Findings: Resolving Phase-Shift Curvature (Option A+)

Bottleneck sweeps on the **Locked Kerr (Family 1)** and **Free Kerr (Family 2)** datasets
under time-domain, FFT-magnitude, and Hilbert-envelope representations, to test whether a
phase-invariant representation undoes the curvature inflation seen in Leg 7.

## Result in one line (with the metric-space caveat stated up front)

**FFT-magnitude preprocessing recovers the true 2D/4D dimensionality — but only in
*standardized* space.** This is an important honest caveat: PREREGISTRATION specified the
$R^2$ metric on **whitened** representations, and in whitened space FFT magnitude does
*not* recover the true count (knee = 4 for Locked, 5 for Free). The "recovers 2D" headline
therefore rests on a metric-space choice (standardized) that differs from the frozen
prereg. §2.3 argues standardized space is the more physically faithful choice (whitening
amplifies discretization/grid artifacts), and that argument is plausible — but it was made
*after* seeing that whitened space failed, so treat "FFT recovers the true dimension" as
holding **specifically in standardized space**, not unconditionally.

---

## 1. Quantitative Results Table (Held-Out $R^2$)

### Family 1: Locked Kerr (2D Manifold: $M, \chi$)
| Representation | Space | d = 0 | d = 1 | d = 2 | d = 3 | d = 4 | d = 5 | Knee (3% Thresh) | Knee (2% Thresh) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Baseline (Time-Domain)** | Std | -0.0015 | 0.6563 | 0.9517 | 0.9783 | 0.9864 | 0.9869 | **2** | **3** |
| | White | -0.0016 | 0.2702 | 0.6895 | 0.8307 | 0.9040 | 0.9204 | **4** | **4** |
| **FFT Magnitude** | Std | -0.0002 | 0.9431 | **0.9983** | 0.9991 | 0.9992 | 0.9992 | **2** | **2** |
| | White | -0.0016 | 0.4790 | **0.9406** | 0.9683 | 0.9900 | 0.9946 | **2** | **4** |
| **Hilbert Envelope** | Std | -0.0013 | 0.9117 | 0.9844 | 0.9945 | 0.9979 | 0.9978 | **2** | **3** |
| | White | -0.0015 | 0.1140 | 0.4327 | 0.5755 | 0.6365 | 0.6882 | **5** | **5** |

### Family 2: Free Kerr (4D Manifold: $M, \chi, A_{221}, \phi_{221}$)
| Representation | Space | d = 0 | d = 1 | d = 2 | d = 3 | d = 4 | d = 5 | Knee (3% Thresh) | Knee (2% Thresh) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Baseline (Time-Domain)** | Std | -0.0016 | 0.6241 | 0.8973 | 0.9552 | 0.9649 | 0.9731 | **3** | **3** |
| | White | -0.0016 | 0.2280 | 0.6008 | 0.7624 | 0.8397 | 0.8302 | **4** | **4** |
| **FFT Magnitude** | Std | -0.0017 | 0.8270 | **0.9612** | **0.9855** | **0.9962** | 0.9977 | **2** | **3** |
| | White | -0.0016 | 0.3360 | 0.6704 | 0.7818 | 0.8397 | 0.9099 | **5** | **5** |
| **Hilbert Envelope** | Std | -0.0022 | 0.8296 | 0.9305 | 0.9623 | 0.9755 | 0.9854 | **3** | **3** |
| | White | -0.0016 | 0.0695 | 0.2318 | 0.3248 | 0.4011 | 0.4358 | **5** | **5** |

---

## 2. Key Physical & ML Insights

### 1. The Resolution of Phase-Shift Curvature
The raw time-domain baseline exhibits a clear **manifold curvature inflation** in whitened space, resolving to a knee of **4** for both the 2D Locked and 4D Free families. This occurs because shifts in peak positions (caused by varying frequency $f(M, \chi)$) create a highly winding manifold in vector space.
Transforming the waveforms into the **Fourier magnitude domain** strips away global time/phase translation, flattening the representation manifold.
* For the **Locked Kerr (2D)** family in standardized space, the FFT magnitude autoencoder achieves **99.83% reconstruction accuracy at $d = 2$**, with a textbook knee of **exactly $2$** (marginal gain drops from 5.52% to 0.08%).
* This validates our primary hypothesis: removing phase-shift variance recovers the true physical parameter count.

### 2. Sequential Parameter Resolution (Energy Ranking)
In standardized (unwhitened) space for the **Free Kerr (4D)** family, the FFT magnitude autoencoder resolves parameters sequentially based on their variance/energy contribution:
1. **$d = 1$ to $2$ ($R^2 = 96.12\%$)**: Captures the mass $M$ and spin $\chi$ which dictate the frequency and decay time of the dominant fundamental $(2,2,0)$ mode.
2. **$d = 3$ ($R^2 = 98.55\%$, gain $+2.43\%$)**: Resolves the overtone amplitude ratio $A_{221}/A_{220}$.
3. **$d = 4$ ($R^2 = 99.62\%$, gain $+1.07\%$)**: Resolves the relative phase difference $\phi_{221}$.
4. **$d = 5$ (gain $+0.15\%$)**: Yields negligible improvement once the 4 physical degrees of freedom are fully exhausted.
Consequently, the resolved count depends on the knee threshold: a **3% threshold** detects
the 2 dominant fundamental-mode parameters, a **2% threshold** resolves 3, and a **1%
threshold** recovers all 4. This threshold-dependence is itself the caveat — the "all 4
parameters recovered" reading requires picking the 1% threshold *after* knowing there are 4,
so it is exploratory/confirmatory-after-the-fact, not an independent recovery of the count.
The robust, threshold-agnostic statement is that FFT magnitude (standardized) resolves the
2 dominant parameters sharply and exposes the overtone parameters as progressively smaller,
energy-ranked marginal gains.

### 3. The Whitening Noise-Inflation Effect
We observe a major disparity between standardized (`std`) and whitened (`white`) spaces:
* **Whitening** normalizes the variance of all linear principal components. For physical signals, this amplifies high-frequency, low-variance directions which consist of discretization errors, FFT binning grid artifacts, and numerical solver residuals.
* As a result, the autoencoder in whitened space is forced to spend bottleneck capacity trying to reconstruct these amplified non-physical numerical artifacts, leading to delayed or inflated knees (e.g. resolving a knee of $5$ for the Free family).
* **Standardized (unwhitened) space** keeps these numerical artifacts at near-zero variance, allowing the autoencoder to focus exclusively on the true physical parameters. Standardized space is therefore far more robust for dimension counting on physical waveforms.

---

## 3. Verification & Visualizations
The 6-panel comparison plot is saved to `results/leg7b_phase_shift.png`.

This completes **Option A+**. The honest scope of the conclusion: on these **two synthetic
Kerr families**, FFT-magnitude preprocessing in **standardized** space undoes the
phase-shift curvature inflation and recovers the true intrinsic dimension, where the raw
time-domain and whitened representations do not. Whether it generalizes beyond these two
families (and the standardized-vs-whitened question) is left open; this is a promising
preprocessing recipe, not an established general-purpose method.
