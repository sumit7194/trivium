# Leg 8 — Findings: Exact Echo Spacing for Echo Search (ansatz ↔ deepstrain)

## 1. Symbolic & Numerical Results

*   **H1 (SymPy Verification) is VERIFIED ✅**: SymPy successfully verified that the photon sphere (light ring) for the Damour-Solodukhin (DS) wormhole metric:
    $$ds^2 = -\left(1 - \frac{2M}{r} + \lambda^2\right) dt^2 + \left(1 - \frac{2M}{r}\right)^{-1} dr^2 + r^2 d\Omega^2$$
    is located at:
    $$r_{ph} = \frac{3M}{1+\lambda^2}$$
*   **H2 (Logarithmic scaling) is VERIFIED ✅**: The exact analytical integration of the round-trip travel time of light from the throat $2M(1+\epsilon)$ to $r_{ph}$ confirmed the logarithmic scaling with the wormhole parameter $\lambda$ for small values:
    $$\Delta t \approx -8M_{sec} \ln(\lambda) + C(\epsilon)$$
    For the Planckian cutoff ($\epsilon = 10^{-38}$), $\Delta t$ ranges from $0.117$ s (static) / $0.139$ s (rotating) at $\lambda = 10^{-21}$ down to $0.0077$ s (static) / $0.0091$ s (rotating) at $\lambda = 10^{-1}$.
    For the macroscopic cutoff ($\epsilon = 10^{-10}$), the spacing is independent of $\lambda$ for $\lambda \le 10^{-6}$ (saturating at $0.0306$ s static / $0.0364$ s rotating) and drops at larger $\lambda$.

---

## 2. On-Source Search on GW150914

We ran the coherent network comb statistic on real LIGO GW150914 post-merger data at the exact spacings corresponding to the physical $\lambda$ sweeps, comparing to the noise background of 159 off-source segment pairs.

### The Significance Peak

In the **Planckian Rotating** sweep, we observed a localized dip in the empirical p-value at:
$$\lambda = 1.0 \times 10^{-17} \implies \Delta t = 0.1267\text{ s} \implies p = 0.00625$$
This means only 1 out of 159 noise-only background segments achieved a network comb score higher than the on-source score at this spacing.

### Trials Factor (Look-Elsewhere Effect) Analysis

To evaluate whether this $p \approx 0.006$ peak constitutes a real detection, we must apply the trials factor. Since we swept a grid of $N_{trials} = 41$ spacings in the Planckian rotating model:
$$p_{trials} = 1 - (1 - p_{local})^{N_{trials}} = 1 - (1 - 0.00625)^{41} \approx 22.7\%$$
A trials-corrected p-value of $22.7\%$ is well above the standard $5\%$ significance threshold ($p > 0.05$). Thus, **H3 (Physical Search Null) is VERIFIED ✅**. The peak is statistically consistent with a random noise fluctuation, establishing a null result.

---

## 3. What this does and does not establish (non-detection, not an exclusion limit)

Mapping the comb search directly onto the physical $\lambda$-spacing grid, the result is a
clean **non-detection**: across both the Planckian ($\epsilon = 10^{-38}$) and macroscopic
($\epsilon = 10^{-10}$) cutoffs, every physical spacing is consistent with detector noise
(the one $p\approx0.006$ dip washes out to ~23% after the 41-trial correction).

**Honest scope (corrected 2026-06-18):** this is *not* an exclusion limit on $\lambda$. An
exclusion would require a sensitivity/efficiency curve — showing what echo amplitude we
*would have detected* at each spacing — which this leg does not compute. So the correct
statement is "no significant echo found at the searched physical spacings in GW150914," not
"$\lambda$ is constrained / horizon-scale quantum corrections are constrained." Turning this
into an upper limit on $\lambda$ is left as future work (it needs the injection-efficiency
curve that Leg 8b begins to build).
