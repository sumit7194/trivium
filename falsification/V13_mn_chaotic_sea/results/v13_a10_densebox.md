# V13 A10 strict-box check (LABELLED POST-HOC, prompted by tabula; no registered verdict changes)

**Code:** `code/v13_a10_densebox.py`, `code/v13_a10_densebox_hstar.py`.
**Results:** `results/v13_a10_densebox.json`, `results/v13_a10_densebox_hstar_{C0,F5R}.json`.
**Run:** one process each at nice 10; peak RSS ≤ 434 MB.

## Method
- **Orbits.** Every A10 CONFIRMED_MS edge, plus the A9-only edges (labelled), is re-integrated from its stored
  multiple-shooting solution, together with every in-D hyperbolic UPO over one period.
  - Integration is in the base domain, using the same DOP853 step sequence as v13_orbit. The section end points
    equal SectionMap's map bitwise.
  - Samples are taken at every step plus dense output; the maximum sample gap is ≤ 0.0028.
- **Strict test.** At every sample, take the minimum of g_φφ over a 21 × 21 grid on the ±0.025 box, then refine it
  with scipy L-BFGS-B (bounded) for the 300 worst samples per orbit. Non-finite values fail. The other B9 conditions
  are applied exactly.
- **Supplementary margin.**
  - *Distance to the CTC set.* The L∞ distance to {g_φφ ≤ 0 or non-finite} (boundary of a 5e−4 grid), at every
    sample.
  - *Exact h\*.* At the tightest samples, the half-width h at which the box minimum crosses 0, found by bisection
    to 1e−8.
  - The strict box passes iff h\* > 0.025.

## Controls (both points: PASS)
| control | strict test | box-min g_φφ (C0 / F5-R) |
|---|---|---|
| (3.6, 0) | passes | 10.4 / 8.3e4 |
| (x_s + 0.015, 0) | fails | −4e8 / −4e12 |

## Results
- **All edges survive the strict test.**
  - C0: 16/16 confirmed edges.
  - F5-R: 35/35 confirmed edges.
- **All 11 UPOs at each point are strictly in D.** The box-min distance test agrees with the box test everywhere.
- **The confirmed graph is unchanged.**
  - C0: SCC {1, 3, 4, 6}, self-loops 1, 3, 6.
  - F5-R: SCC {2, …, 8}, self-loops 2–7.
- **Smallest box-min g_φφ over confirmed edges:** C0 0.180 (8→6), F5-R 29.2 (9→7).
- **Where the orbits come closest to the CTC region.**
  - min x is not on the axis. It occurs at y ≈ ±0.095 (C0 x = 1.9474, F5-R x = 1.9392), at Euclidean distance
    ≈ 0.096 from the ring point.
  - The nearest CTC point lies diagonally off the lower-left box corner, at about (x − 0.025, y − 0.025).
  - In every case the box minimum sits at a box corner, which is one of B9's own 9 samples.

## Exact margins (h\* − 0.025)
| point | orbit | margin |
|---|---|---|
| F5-R | UPO 9 | +5.1e−5 |
| F5-R | 9→7 | +7.0e−6 |
| F5-R | 9→6 | +2.7e−5 |
| F5-R | 9→3 | +2.9e−5 |
| F5-R | 9→8 | +4.0e−5 |
| F5-R | 9→2 (A9 only) | +4.1e−5 |
| F5-R | smallest within the SCC (4→2) | +7.2e−4 |
| C0 | smallest overall (8→4, A9 only) | +3.2e−4 |
| C0 | UPOs 5, 7, 9, 10 | +3.4e−4 |
| C0 | 8→6 | +3.5e−4 |
| C0 | SCC members | > 1e−2 |

## Reading of tabula's UPO 9 verdict
- Our UPO 9 is tabula's orbit, z = (3.69828, 5.13182), and it stays strictly in D_B9 by 5e−5 in distance.
- That margin is ten times smaller than tabula's stated mask accuracy (≤ 5e−4), so their "leaves D" result is within
  their resolution and is not a contradiction.
- UPO 9 has no incoming edges, so it belongs to no SCC. Whatever its status, the SCCs and self-loops are unaffected.
- **Caveat:** UPO 9's four outgoing confirmed edges are marginal (≤ 4e−5). They depend on the exact box definition
  of B9.
