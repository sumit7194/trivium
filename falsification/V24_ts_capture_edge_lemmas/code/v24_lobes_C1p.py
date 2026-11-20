"""V24 amendment C1' (PREREGISTRATION.md): interpolation floor measured first, then exact-U reclassification and re-check."""
import sys, os, json, math, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V20_ts_capture_edge_tangle/code')); import v20
FJ, fW, fH = v20.field('ts45', 0.97, 41/8); RT = 1e-12
z, Dm, T, clos = v20.polish(FJ, fH, 9.8045591682, RT)
ev, Vv = np.linalg.eig(Dm); k = int(np.argmax(np.abs(ev))); lam = float(np.real(ev[k])); eu = np.real(Vv[:, k]); eu /= np.linalg.norm(eu)
xs = z[0]; sgn = 1.0 if v20.P(FJ, fH, z + 1e-6*lam**2*eu, RT)[0][0] > xs else -1.0
s0 = 1e-6; S = np.geomspace(s0, s0*lam, 400, endpoint=False)
def it(s, n):
    q = z + sgn*s*eu
    for _ in range(n):
        q = v20.P(FJ, fH, q, RT)[0]
        if q is None: return None
    return q
meta = []; first = {}           # U points (x, px, seed index, n); first image below the line per seed
for i, s in enumerate(S):
    q = z + sgn*s*eu; n = 0; meta.append((q[0], q[1], i, 0))
    while n < 14:
        q2 = v20.P(FJ, fH, q, RT)[0]
        if q2 is None: break
        n += 1; q = q2
        if q[1] <= 0: first[i] = (q, n); break
        meta.append((q[0], q[1], i, n))
meta.sort(); MX = np.array([m[0] for m in meta]); MP = np.array([m[1] for m in meta]); xh = float(MX.max())
Ui = lambda x: float(np.interp(x, MX, MP))
SE = np.append(S, s0*lam)                     # seed s0*lam at iterate n == seed s0 at iterate n+1
def Ue(x):
    """exact U(x): curve parameter t = i + 400 n; root-find the seed between two curve-adjacent U points bracketing x;
    fallback: scan the whole curve for a bracketing adjacent pair."""
    j = int(np.searchsorted(MX, x)); tt = lambda m: m[2] + 400*m[3]
    pairs = [(meta[j-1], meta[j])] if 1 <= j < len(meta) else []
    for a, b in pairs:
        if abs(tt(a) - tt(b)) != 1: continue
        a, b = (a, b) if tt(a) < tt(b) else (b, a); n = a[3]; sa = S[a[2]]; sb = SE[a[2] + 1]
        r = brentq(lambda ss: it(ss, n)[0] - x, sa, sb, xtol=1e-18, rtol=1e-15); return float(it(r, n)[1])
    byt = sorted(meta, key=tt)
    for a, b in zip(byt, byt[1:]):
        if tt(b) - tt(a) != 1 or (a[0] - x)*(b[0] - x) > 0: continue
        n = a[3]; sa = S[a[2]]; sb = SE[a[2] + 1]
        r = brentq(lambda ss: it(ss, n)[0] - x, sa, sb, xtol=1e-18, rtol=1e-15); return float(it(r, n)[1])
    raise RuntimeError(f'no exact U at x={x}')
# 1. floor
fx = np.linspace(xs + 0.05, xh - 0.05, 30); errs = [abs(Ui(x) - Ue(x)) for x in fx]
floor = max(errs); delta = 10*floor
print('interp floor max %.3e (median %.3e) -> delta %.3e' % (floor, float(np.median(errs)), delta), flush=True)
# 2-3. classify with exact U where needed; iterate; re-check hits
def margin(q):   # U(x) - |p_x|, >0 means inside the open region |p| < U; exact when close
    if not (xs < q[0] < xh): return -math.inf
    m = Ui(q[0]) - abs(q[1])
    return Ue(q[0]) - abs(q[1]) if abs(m) < delta else m
rows = []
for i in sorted(first):
    p, n = first[i]
    gi = abs(p[1]) - Ui(p[0]) if p[0] < xh else math.inf
    ge = (abs(p[1]) - Ue(p[0])) if abs(gi) < delta else gi
    outside = (p[0] >= xh) or ge > 0
    q = p; went_in = False; hits = []
    for r in range(7):
        if q[0] < xs and q[1] < 0: went_in = True; break
        mg = margin(q)
        if mg > 0: hits.append((r, float(q[0]), float(q[1]), float(mg)))
        q2 = v20.P(FJ, fH, q, RT)[0]
        if q2 is None: went_in = (v20.P.last == 'plunge'); break
        q = q2
    rows.append(dict(i=i, n=n, x=float(p[0]), px=float(p[1]), gap_interp=float(gi), gap_used=float(ge),
                     outside=bool(outside), outside_interp=bool(p[0] >= xh or gi > 1e-9), went_in=went_in, hits=hits))
# pieces of the outside set in seed order (cyclic)
cls = [r['outside'] for r in rows]; changes = [rows[k]['i'] for k in range(len(rows)) if cls[k] != cls[k-1]]
out_rows = [r for r in rows if r['outside']]; rest = [r for r in rows if not r['outside']]
res = dict(floor=floor, delta=delta, floor_errs=errs, n_first=len(rows), class_changes_at_seed=changes,
           outside=len(out_rows), outside_with_exact_hit=sum(bool(r['hits']) for r in out_rows),
           outside_went_in=sum(r['went_in'] for r in out_rows),
           rest=len(rest), rest_reenter=sum(bool(r['hits']) for r in rest),
           reclassified=[(r['i'], r['outside_interp'], r['outside'], r['gap_interp'], r['gap_used']) for r in rows if r['outside'] != r['outside_interp']],
           min_outside_gap=min(r['gap_used'] for r in out_rows))
for k_, v in res.items():
    if k_ != 'floor_errs': print(k_, v, flush=True)
json.dump(dict(res, rows=rows), open(os.path.join(HERE, '../results/v24_lobes_C1p.json'), 'w'), indent=1, default=str)
