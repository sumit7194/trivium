"""Pre-check for addendum K' (tight enclosure): containment at the same 11 P1 boxes, WIDTH at the theta ~ 1 corners
(the failure mode of K2), and the P2 known-false must-fail controls, all on the tight code path."""
import sys, os, random, mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v26_K_lib import iv, lo, hi, H_enclose_tight, H_float
from v26_K import certify
random.seed(11); bad = 0
pts = [(random.uniform(0, 1), 1.0, random.uniform(0, 10)) for _ in range(5)] + \
      [(random.uniform(0.2, 1), random.uniform(1, 5), 1.0) for _ in range(3)] + [(1.0, 1.0, 0.7), (1.0, 3.0, 1.0), (0.0, 1.0, 0.0)]
for th, X, E in pts:
    h = 1e-7
    T = iv.mpf([th, min(th + h, 1.0)]) if th < 1 else iv.mpf([1 - h, 1]); Hc = H_enclose_tight(T, iv.mpf([X, X]), iv.mpf([E, E + h]), 64)
    mp.mp.dps = 25; Hf = H_float(float(lo(T)), X, E)
    ok = lo(Hc.re) <= Hf.real <= hi(Hc.re) and lo(Hc.im) <= Hf.imag <= hi(Hc.im); bad += not ok
    print("P1' contain theta=%.4f x0=%.2f eta=%.3f : %s (width %.1e)" % (float(lo(T)), X, E, ok, float(hi(Hc.re) - lo(Hc.re))))
for (T, X, E) in (((0.9999938, 1.0), (1, 1), (4.99992, 5.0)), ((0.999, 1.0), (1, 1), (0.99, 1.0)), ((0.999, 1.0), (4.99, 5.0), (1, 1))):
    for M in (128, 512):
        Hc = H_enclose_tight(iv.mpf(list(T)), iv.mpf(list(X)), iv.mpf(list(E)), M)
        w = max(float(hi(Hc.re) - lo(Hc.re)), float(hi(Hc.im) - lo(Hc.im))); ok = w < 0.05; bad += not ok
        print("P1w' width at theta-corner box %s M=%d: %.3e (must be < 0.05 and must not grow with M) : %s" % ((T, X, E), M, w, ok))
probe = {'K1': (0.1, 1, 5.0), 'K2': (0.5, 1, 2.0), 'K3A': (0.6, 1, 0.5), 'K3B': (0.6, 2.0, 1.0)}
for name, (th, X, E) in probe.items():
    mp.mp.dps = 25; Hf = H_float(th, X, E)
    v = Hf.real**2 - Hf.imag**2 if name == 'K1' else (1 - abs(Hf.imag)/mp.sqrt(th) if name == 'K2' else Hf.real - abs(Hf.imag))
    r = certify(name, shift=v + mp.mpf('1e-3'), max_boxes=3000, minw=1e-3, tight=True); bad += r['ok']
    print("P2' must-fail %s (tight): certified = %s (must be False)" % (name, r['ok']))
print("PRECHECK K'", 'OK' if bad == 0 else 'PROBLEMS %d' % bad)
