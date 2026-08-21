"""Item 1 failed for FFT. Does NAFF at longer record dominate on BOTH properties?

NAFF's gain was already flat (spread 0.025 at N=200) but its FLOOR was 2.4x worse
than FFT's, and at n~22 the floor decided discrimination (E4). If NAFF's floor
falls fast with N while its gain stays flat, NAFF-at-longer-record beats FFT on
both and the dilemma dissolves.

PRE-REGISTERED before running:
  PASS = NAFF floor falls monotonically with N AND drops below FFT's floor by
         N<=3200, while NAFF gain spread stays < 0.10.
  FAIL = NAFF floor plateaus above FFT's, or its gain degrades with N. Then
         neither estimator dominates and the cross-delta comparison stays broken.
"""
import numpy as np
import gain_test as G
from naff_drift import drift_fft, drift_naff

def floor_and_gain(N, reps=250, n_off=16):
    G.N, G.M = N, N//2
    M = N//2; base = max(8, int(0.17*M))
    rng = np.random.default_rng(777 + N)
    out = {}
    for lab, fn in [("fft", drift_fft), ("naff", drift_naff)]:
        # FLOOR: true drift = 0, offsets varied (as real orbits are)
        f = []
        for _ in range(reps):
            fa = (base + rng.uniform(0,1))/M
            x,_ = G.series_with_known_drift(fa, 0.0, rng)
            v = fn(x)
            if v is not None: f.append(max(v,1e-18))
        f = np.array(f)
        # GAIN spread over offsets, true drift 1e-3
        g = []
        for off in np.linspace(0,1,n_off,endpoint=False):
            fa = (base+off)/M; gg=[]
            for _ in range(80):
                x,true = G.series_with_known_drift(fa, 1e-3, rng)
                v = fn(x)
                if v is not None: gg.append(v/true)
            g.append(np.median(gg))
        g = np.array(g)
        out[lab] = (float(np.median(f)), float(g.max()-g.min()), float(np.median(g)))
    return out

print("FLOOR (true drift 0, offsets varied) and GAIN SPREAD, both estimators vs N\n")
print(f"{'N':>6} | {'FFT floor':>11} {'FFTspread':>10} | {'NAFF floor':>11} {'NAFFspread':>11} | {'floor ratio':>11}")
rows=[]
for N in [200, 400, 800, 1600, 3200]:
    o = floor_and_gain(N)
    ff,fs,_ = o["fft"]; nf,ns,_ = o["naff"]
    rows.append((N,ff,fs,nf,ns))
    print(f"{N:6d} | {ff:11.3e} {fs:10.3f} | {nf:11.3e} {ns:11.3f} | {nf/ff:11.2f}")
mono = all(rows[i+1][3] < rows[i][3] for i in range(len(rows)-1))
final = rows[-1]
print(f"\n  NAFF floor monotonically falling: {mono}")
print(f"  NAFF floor at N=3200: {final[3]:.3e}  vs FFT {final[1]:.3e}  (ratio {final[3]/final[1]:.2f})")
print(f"  NAFF gain spread at N=3200: {final[4]:.3f}  (FFT {final[2]:.3f})")
ok = mono and final[3] < final[1] and final[4] < 0.10
print(f"\n  PRE-REGISTERED PASS = NAFF floor monotonic AND below FFT by N<=3200 AND spread < 0.10")
print(f"  VERDICT: {'PASS' if ok else 'FAIL'}")
