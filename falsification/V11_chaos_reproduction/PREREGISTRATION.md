# V11 — Pre-registration: the bridge's independent reproduction of chaos candidates (ansatz's TS δ=2 chaos study)

*2026-10-10. Written and committed BEFORE any V11 code runs. Conventions come from ansatz's text message (y0 = 0,
p_x0 = 0, p_y0 > 0 from the mass shell, μ² = 1, up-crossings of y = 0, affine time = proper time, S_ex and fd as
defined there). The bridge has not read ansatz's code.*

## The bridge's own implementation (`code/v11_chaos.py`)
- **Metric:** the bridge's own transcription. ZV δ=2 comes from V8's `zv()`, TS from ansatz's sealed component files
  via V8's loader, and Kerr from V10's Boyer–Lindquist form.
- **Equations:** H = ½[g^xx p_x² + g^yy p_y² + W] with W = g^tt E² − 2g^tφ E L + g^φφ L². The vector field and its
  **exact Jacobian** come from sympy symbolic differentiation (ansatz uses central differences).
- **Integrator:** scipy **DOP853** (ansatz uses Dormand–Prince 5(4)), with exact section events at y = 0, direction +1.
- **Tangent vector:** v0 = (1, 0.7, −0.4, 0.3)/‖·‖, evolved by the exact variational equations. It is renormalised
  every Δτ = 10.
- **Detector:** S_ex = Σ ln‖v‖ − ln τ_last, with chaos declared at S_ex ≥ 10.
- **Frequency drift:** fd per the stated recipe (halves, Hanning window, rfft, parabolic peak), threshold 0.0115, used
  only when n ≥ 100.
- **Stops:** 300 crossings, τ = 5e6, plunge x < 1.5, or escape x > 2000.
- **Tolerances:** rtol 1e−11 and 1e−13. A classification counts only if both tolerances agree.

## Validation gate (ZV δ=2, E = 0.95), which must pass before any TS candidate is examined
| Orbit | Expected |
|---|---|
| L = 2.9, x0 = 7.56263 | CHAOTIC (S_ex ≥ 10 at both tolerances) |
| L = 3.0, x0 = 7.57274 | CHAOTIC |
| L = 3.0, x0 = 7.62 | REGULAR (S_ex < 10, fd < 0.0115 at both tolerances) |

The comparison is on classifications, not identical numbers, because layer orbits are sticky and depend on the exact
realisation. **If any orbit is misclassified, STOP and diagnose; the detector is not tuned on these orbits.**

## Use
Each TS candidate ansatz reports gets reproduced at both tolerances.
- **REPRODUCED:** CHAOTIC at both.
- **NOT REPRODUCED:** REGULAR at both.
- **INCONCLUSIVE:** the two tolerances disagree.

## Addendum 1 (before any Kerr replay): Kerr in ansatz's chart, a Carter diagnostic, and the truncated score
- **Kerr in the TS chart:** `kerr45` (p = 4/5) and `kerr35` (p = 3/5), built from the δ = 1 Ernst potential with the
  same conventions (`code/kerr_ts_chart.py`). The twist equations are satisfied exactly, and R_ab = 0 exactly at 3
  rational points.
- **Carter diagnostic:** Q = (1−y²)p_y² + y²(a²(1−E²) + L²/(1−y²)), with a = q/p, recorded as the maximum relative
  deviation along the orbit while x ≥ 1.5. A conserved Q together with a "chaotic" score marks a detector false positive.
- **Truncated score:** classification now uses S_ex truncated at the last section crossing, the same rule as ansatz's
  amendment 4. Untruncated S_ex is still reported. The ZV gate is re-checked under the truncated score before any Kerr
  replay.
