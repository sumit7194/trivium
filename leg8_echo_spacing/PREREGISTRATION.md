# Leg 8 — Pre-registration: Exact Echo Spacing for Echo Search (ansatz ↔ deepstrain)

*Frozen 2026-06-17, before running the physical spacing search. Discipline: THE_BRIDGE.md §2, §4C, §5.*

This leg bridges the exact wormhole metric from ansatz with deepstrain's search for echoes on real LIGO GW150914 post-merger data. By integrating radial null geodesics, we translate the abstract time spacing $\Delta t$ into a physical wormhole deviation parameter $\lambda$.

---

## 1. Physics & Numerical Integration

We model a Damour-Solodukhin (DS) wormhole with:
$$A(r) = 1 - \frac{2M}{r} + \lambda^2, \quad B(r) = 1 - \frac{2M}{r}$$
We evaluate the echo spacing:
$$\Delta t(\lambda) = 2 \int_{2M(1+\epsilon)}^{r_{ph}} \frac{dr}{\sqrt{A(r) B(r)}}$$
for $M = 68.0 M_\odot$ (detector frame) using two cutoff regimes:
1.  **Planckian cutoff**: $\epsilon = \ell_P / 2M \approx 10^{-38}$.
2.  **Macroscopic cutoff**: $\epsilon = 10^{-10}$.

---

## 2. Frozen Predictions & Hypotheses

*   **H1 (SymPy Verification)**: SymPy will find the photon sphere $r_{ph}$ by solving $\frac{d}{dr}(r^2 / A(r)) = 0$, verifying it matches:
    $$r_{ph} = \frac{3M}{1+\lambda^2}$$
*   **H2 (Logarithmic scaling)**: At small $\lambda \ll 1$, the echo spacing $\Delta t$ scales logarithmically with $\lambda$:
    $$\Delta t \approx -4M \ln(\lambda) + C(\epsilon)$$
    where $M$ is in units of seconds ($M \approx 68.0 \times 4.9255 \times 10^{-6}\text{ s} \approx 3.35 \times 10^{-4}\text{ s}$).
*   **H3 (Physical Search Null)**: The coherent network comb search on GW150914 post-merger strain will return a null result (no p-value $< 0.05$ at the spacings corresponding to physical $\lambda$). This will establish an exclusion limit on the wormhole parameter $\lambda$.

---

## 3. Agreement Criteria

*   **H1 is verified** if SymPy returns $r_{ph} = \frac{3M}{1+\lambda^2}$.
*   **H2 is verified** if the computed $\Delta t(\lambda)$ shows a linear relationship when plotted against $\log_{10}(\lambda)$ for small $\lambda$ with a slope matching $-4M \ln(10) \approx -9.21 M \approx -0.0031$ s/decade.
*   **H3 is verified** if the minimum p-value over the physical $\log_{10}(\lambda) \in [-15, -1]$ sweep is $\ge 0.05$.
