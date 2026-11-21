"""V26-K: Bridge's independent certificates for Neon T19 (G1 gap), checks K1, K2, K3A, K3B; K4 end-to-end count."""
import sys, os, time, mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v26_K_lib import iv, lo, hi, H_enclose, H_float, CutError
T737 = mp.mpf(7)/37
# decision functions: return a rigorous lower bound of the margin over the box (positive = certified)
def m_K1(H, th):            # Re(H^2) = Hr^2 - Hi^2 > 0  (needs Hr > 0)
    if not lo(H.re) > 0: return lo(H.re)
    ai = max(abs(lo(H.im)), abs(hi(H.im)))
    return lo(H.re)**2 - ai**2
def m_K2(H, th, thr=1):     # 1 - theta^-1/2 |Im H| > 0
    ai = max(abs(lo(H.im)), abs(hi(H.im)))
    return thr - ai/mp.sqrt(lo(th))
def m_K3(H, th):            # Re H - |Im H| > 0
    ai = max(abs(lo(H.im)), abs(hi(H.im)))
    return lo(H.re) - ai
SPEC = {  # name: (theta range, x0 range, eta range, decision, split-variable)
    'K1': ((0, T737), (1, 1), (0, 10), m_K1),
    'K2': ((T737, 1), (1, 1), (0, 5), m_K2),
    'K3A': ((T737, 1), (1, 1), (0, 1), m_K3),
    'K3B': ((T737, 1), (1, 5), (1, 1), m_K3),
}
def certify(name, shift=0, Ms=(16, 32, 64, 128), max_boxes=40000, minw=1e-5, decision=None, verbose=False):
    (t0, t1), (x0, x1), (e0, e1), dec = SPEC[name]; dec = decision or dec
    todo = [(mp.mpf(t0), mp.mpf(t1), mp.mpf(x0), mp.mpf(x1), mp.mpf(e0), mp.mpf(e1))]
    done = 0; minlb = mp.inf; evals = 0
    while todo:
        b = todo.pop(); a0, a1, X0, X1, E0, E1 = b
        th = iv.mpf([a0, a1]); X = iv.mpf([X0, X1]); E = iv.mpf([E0, E1])
        size = max(a1 - a0, (X1 - X0)/5, (E1 - E0)/10)
        M = Ms[0] if size > 1/32 else (Ms[1] if size > 1/256 else (Ms[2] if size > 1/2048 else Ms[3]))
        try: lb = dec(H_enclose(th, X, E, M), th) - shift
        except (ZeroDivisionError, CutError): lb = -mp.inf          # enclosure too wide: split
        evals += 1
        if lb > 0:
            done += 1; minlb = min(minlb, lb); continue
        if size < minw: return dict(ok=False, boxes=done, minlb=minlb, stop=('stuck', [float(v) for v in b]), evals=evals)
        # split the widest (normalised) dimension
        w = [(a1 - a0), (X1 - X0)/5, (E1 - E0)/10]; k = w.index(max(w))
        if k == 0: m = (a0 + a1)/2; todo += [(a0, m, X0, X1, E0, E1), (m, a1, X0, X1, E0, E1)]
        elif k == 1: m = (X0 + X1)/2; todo += [(a0, a1, X0, m, E0, E1), (a0, a1, m, X1, E0, E1)]
        else: m = (E0 + E1)/2; todo += [(a0, a1, X0, X1, E0, m), (a0, a1, X0, X1, m, E1)]
        if done + len(todo) > max_boxes: return dict(ok=False, boxes=done, minlb=minlb, stop='budget', evals=evals)
    return dict(ok=True, boxes=done, minlb=minlb, stop=None, evals=evals)
if __name__ == '__main__':
    name = sys.argv[1]; t = time.time()
    r = certify(name)
    print('%s: certified = %s | boxes %d | evals %d | min certified margin %s | stop %s | %.0f s' % (
        name, r['ok'], r['boxes'], r['evals'], mp.nstr(r['minlb'], 6), r['stop'], time.time() - t))
    print('VERDICT', name, 'PASS' if r['ok'] and r['minlb'] > 0 else 'FAIL')
