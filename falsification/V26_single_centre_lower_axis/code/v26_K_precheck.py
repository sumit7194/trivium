"""V26-K pre-check: every code path the K clauses use, on known inputs (target margins NOT computed)."""
import sys, os, random, mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v26_K_lib import iv, lo, hi, H_enclose, H_float
from v26_K import certify, SPEC, m_K1, m_K2, m_K3, T737
random.seed(11); bad = 0
# P1 enclosure validity (incl. theta = 1 cut-fallback cells and the off-line u of K3B)
pts = [(random.uniform(0, 1), 1.0, random.uniform(0, 10)) for _ in range(5)] + \
      [(random.uniform(0.2, 1), random.uniform(1, 5), 1.0) for _ in range(3)] + [(1.0, 1.0, 0.7), (1.0, 3.0, 1.0), (0.0, 1.0, 0.0)]
for th, X, E in pts:
    h = 1e-7
    T = iv.mpf([th, min(th + h, 1.0)]) if th < 1 else iv.mpf([1 - h, 1]); Xi = iv.mpf([X, X]); Ei = iv.mpf([E, E + h])
    Hc = H_enclose(T, Xi, Ei, 64); Hf = H_float(float(lo(T)), X, E)
    mp.mp.dps = 25
    inside = lo(Hc.re) <= Hf.real <= hi(Hc.re) and lo(Hc.im) <= Hf.imag <= hi(Hc.im)
    bad += not inside
    print('P1 theta=%.4f x0=%.3f eta=%.3f float H=%s | encl re [%s,%s] im [%s,%s] width %.1e : %s' % (
        float(lo(T)), X, E, mp.nstr(Hf, 8), mp.nstr(lo(Hc.re), 8), mp.nstr(hi(Hc.re), 8), mp.nstr(lo(Hc.im), 8), mp.nstr(hi(Hc.im), 8),
        float(hi(Hc.re) - lo(Hc.re)), inside))
# P2 must-fail: shift each decision by (its float value at one fixed in-domain point) + 1e-3 -> known-false target
probe = {'K1': (0.1, 1, 5.0), 'K2': (0.5, 1, 2.0), 'K3A': (0.6, 1, 0.5), 'K3B': (0.6, 2.0, 1.0)}
for name, (th, X, E) in probe.items():
    mp.mp.dps = 25; Hf = H_float(th, X, E)
    if name == 'K1': v = Hf.real**2 - Hf.imag**2
    elif name == 'K2': v = 1 - abs(Hf.imag)/mp.sqrt(th)
    else: v = Hf.real - abs(Hf.imag)
    r = certify(name, shift=v + mp.mpf('1e-3'), max_boxes=3000, minw=1e-3)
    fires = not r['ok']; bad += not fires
    print('P2 must-fail %s: shift = value at %s (%.4e) + 1e-3 -> certified = %s (must be False) | stop %s' % (name, (th, X, E), float(v), r['ok'], r['stop']))
print('PRECHECK', 'OK' if bad == 0 else 'PROBLEMS %d' % bad)
