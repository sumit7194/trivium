"""quantum's check: is the 1.4x improvement real, or an artifact of the offset SWEEP?

If the interpolation bias is a fixed function of the FRACTIONAL bin offset, then at
FIXED fractional offset the gain should not improve with N at all. If it is flat,
my reported 1.4x was averaging over a changing offset distribution, and the true
answer is "longer records do nothing", which is stronger than what I claimed.

Also: report NAFF's spread at full precision. "exactly 0.000" is a rounding, and
after a day cataloguing quantities that cannot fail, a displayed zero should never
be mistaken for a measured one.
"""
import numpy as np, gain_test as G
from naff_drift import drift_fft, drift_naff

def gain_at(N, off, fn, true_d=1e-3, reps=300):
    G.N, G.M = N, N//2
    M = N//2; base = max(8, int(0.17*M))
    rng = np.random.default_rng(4242)
    fa = (base + off)/M                       # fractional offset held EXACTLY fixed
    g = []
    for _ in range(reps):
        x, true = G.series_with_known_drift(fa, true_d, rng)
        v = fn(x)
        if v is not None: g.append(v/true)
    return float(np.median(g))

print("GAIN AT FIXED FRACTIONAL BIN OFFSET, varying N (quantum's killing check)\n")
print(f"{'offset':>8} | " + " | ".join(f"N={N:<6}" for N in [200,400,800,1600,3200]) + " |  max/min")
for off in [0.0, 0.25, 0.5, 0.75]:
    gs = [gain_at(N, off, drift_fft) for N in [200,400,800,1600,3200]]
    a = np.array(gs)
    print(f"{off:8.2f} | " + " | ".join(f"{g:8.4f}" for g in gs) + f" | {a.max()/a.min():8.4f}")
print("\n  If these rows are FLAT, the bias is fixed in fractional offset and longer")
print("  records do NOTHING -- the 1.4x in the sweep was averaging over offsets.\n")

print("NAFF spread at FULL PRECISION (not rounded):")
print(f"{'N':>6} | {'min gain':>12} | {'max gain':>12} | {'max-min':>12}")
for N in [200,400,800,1600,3200]:
    gs = np.array([gain_at(N, o, drift_naff, reps=120) for o in np.linspace(0,1,16,endpoint=False)])
    print(f"{N:6d} | {gs.min():12.9f} | {gs.max():12.9f} | {gs.max()-gs.min():12.3e}")
