"""Does a LONGER RECORD flatten the drift estimator's gain?

FINDINGS item 1 asserts it should: the FFT interpolation bias is set by the bin
width ~1/N, so more crossings shrink the floor AND flatten the gain variation,
with no estimator change. Never tested. Everything expensive downstream depends
on it, so it is tested first and cheaply.

PRE-REGISTERED before running (frozen in this docstring):
  PASS  = gain spread (max-min over bin offsets) falls monotonically with N, and
          reaches < 0.20 by N=2000 -- i.e. <20% residual against 0.839 at N=200.
  FAIL  = spread flat or non-monotonic => longer records do NOT fix the gain, the
          ladder rerun would buy power over a distorted quantity, and item 1 is dead.
"""
import numpy as np
from gain_test import series_with_known_drift
from naff_drift import drift_fft

def spread_at(N, true_d=1e-3, reps=120, n_off=24):
    """Gain vs fractional bin offset of the HALF-series, at record length N."""
    import gain_test as G
    G.N, G.M = N, N//2
    M = N//2
    base = max(8, int(0.17*M))                       # keep absolute frequency ~constant
    rng = np.random.default_rng(31337 + N)
    gains = []
    for off in np.linspace(0, 1, n_off, endpoint=False):
        fa = (base + off)/M
        g = []
        for _ in range(reps):
            x, true = G.series_with_known_drift(fa, true_d, rng)
            v = drift_fft(x)
            if v is not None: g.append(v/true)
        gains.append(np.median(g))
    a = np.array(gains)
    return a.min(), a.max(), a.max()-a.min(), np.median(a)

print("Gain vs bin offset at increasing record length. true drift = 1e-3.\n")
print(f"{'N':>6} | {'gain min':>9} | {'gain max':>9} | {'SPREAD':>9} | {'median':>8}")
prev=None; rows=[]
for N in [200, 400, 800, 1600, 3200]:
    lo,hi,sp,med = spread_at(N)
    rows.append((N,sp))
    flag = '' if prev is None else ('  v' if sp < prev else '  ^ NOT falling')
    print(f"{N:6d} | {lo:9.3f} | {hi:9.3f} | {sp:9.3f} | {med:8.3f}{flag}")
    prev = sp
sp0, spN = rows[0][1], rows[-1][1]
mono = all(rows[i+1][1] < rows[i][1] for i in range(len(rows)-1))
print(f"\n  spread at N=200 : {sp0:.3f}   (the ladder's setting)")
print(f"  spread at N=3200: {spN:.3f}   improvement {sp0/spN:.1f}x")
print(f"  monotonic decrease: {mono}")
print(f"\n  PRE-REGISTERED PASS = monotonic AND spread < 0.20 by N=2000-3200")
print(f"  VERDICT: {'PASS' if (mono and spN < 0.20) else 'FAIL'}")
