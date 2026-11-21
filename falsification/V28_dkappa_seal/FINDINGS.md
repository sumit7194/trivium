# V28 findings (2026-11-21, ~12:20 real clock). Seal commit b93cb63.
Environment: CPython 3.14.5 (conjecture_machine/.venv), numpy/scipy as in ENVIRONMENT.

| Check | Result |
|---|---|
| S1 v0 m = 0 term vs the Born closed form | alpha = 0.3: 3.9e-8 and 0.45: 1.2e-9, PASS. alpha = 0.05: 2.8e-5, **FAIL as registered** (tolerance 1e-6) |
| S2 (v_R, v_L) m = 0 term vs T23's closed form, Gamma(3a+1/2)Gamma(3/2-a) | alpha = 0.3: 3.3e-8 and 0.45: 3.9e-9, PASS. alpha = 0.05: 1.9e-5, **FAIL as registered**. Orientation: v_R = e^{-ap} on the left leg (as T23 wrote); the swapped orientation misses by 10-33% |
| S3 grid convergence | < 1e-5 relative at every sealed value, PASS |

**Labelled post-run diagnostic (results/v28_postdiag_a005.txt).** The alpha = 0.05 misses come from the p-range
(P = 12), not the q-range: at small u the legs extend to |p| ~ log(4/u). With P = 24 or 40, both closed forms are
reproduced to 6e-11 and then 1.4e-14. The tolerance was registered without pre-running the alpha = 0.05 floor, which
is the same slip as before.

**So T23's claim (b) is confirmed independently.** With its derived legs, the exact m = 0 term is T23's
Gamma(3a+1/2)Gamma(3/2-a) form, not the "Born" form. Whether those legs are physically RIGHT is a separate question,
for the direct referee.

**SEALED values (absolute C+resum, and the ratio to each formula's own m = 0 term):**
| twist | T20-v0 C+ | ratio | T23 (v_R, v_L) C+ | ratio |
|---|---|---|---|---|
| 0.2 | -0.00807417 | 1.118040 | -0.00732118 | 1.124486 |
| 0.3 | -0.00738607 | 1.140946 | -0.00727308 | 1.162740 |
| 0.4 | -0.00599607 | 1.136208 | -0.00674452 | 1.175918 |

**First comparison (after sealing).** Cuspis's CH05-route ratio at 0.3 is 1.162 (reported before T23 existed for
Cuspis), which matches T23's 1.16274. Cuspis's own T20-v0 re-implementation gave 1.141, which matches the Bridge's
1.140946. So the CH05 route and T23's leg structure appear to be the SAME resummation. The ratios at 0.2 and 0.4
stay sealed, for a blind comparison with Cuspis's CH05 values.
