"""V24 amendment E2: symmetric points on W^u found directly in the flow (Fix(R)-type: p_x = 0 at an equator event;
brake-type: p_x = 0 at a latitude-turning event p_y = 0). Compare with the W^u-S crossings of addendum E."""
import os, sys, json, math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V20_ts_capture_edge_tangle/code')); import v20
FJ, fW, fH = v20.field('ts45', 0.97, 41/8); RT = 1e-12
z, Dm, T, clos = v20.polish(FJ, fH, 9.8045591682, RT)
ev_, Vv_ = np.linalg.eig(Dm); k = int(np.argmax(np.abs(ev_))); lam = float(np.real(ev_[k])); eu = np.real(Vv_[:, k]); eu /= np.linalg.norm(eu)
xs = z[0]; sgn = 1.0 if v20.P(FJ, fH, z + 1e-6*lam**2*eu, RT)[0][0] > xs else -1.0
s0 = 1e-6; S = np.geomspace(s0, s0*lam, 400, endpoint=False)
prevE = json.load(open(os.path.join(HERE, '../results/v24_symE.json')))['records']
cross_logs = [r['log_s'] for r in prevE if r['kind'] == 'crossing']
rowsC = json.load(open(os.path.join(HERE, '../results/v24_lobes_C1p.json')))['rows']; nmax = max(r['n'] for r in rowsC)
TMAX = 80*T     # E2 fix: excursion returns take far longer than T; orbits end at the plunge event
def rhs(t, s): return np.array(FJ(s[0], s[1], s[2], s[3])[0])
def events_of(sv):
    q = z + sgn*sv*eu; py = v20.py_from_H(fH, q[0], 0.0, q[1])
    def eq(t, s): return s[1] if t > 1e-6 else 1.0
    def tp(t, s): return s[3]
    def pl(t, s): return s[0] - v20.XPLUNGE
    pl.terminal = True
    sol = solve_ivp(rhs, (0, TMAX), [q[0], 0.0, q[1], py], method='DOP853', rtol=RT, atol=RT*1e-3, events=[eq, tp, pl], t_eval=[TMAX])
    evs = [(t, 'E', y[2]) for t, y in zip(sol.t_events[0], sol.y_events[0])] + [(t, 'B', y[2]) for t, y in zip(sol.t_events[1], sol.y_events[1])]
    evs.sort(key=lambda e: e[0]); return [(e[1], e[2]) for e in evs]
print('T %.6f  nmax %d  TMAX %.3f' % (T, nmax, TMAX), flush=True)
ev_list = [events_of(sv) for sv in S]
roots = []
for i in range(len(S) - 1):
    a, b = ev_list[i], ev_list[i + 1]; K = 0
    while K < min(len(a), len(b)) and a[K][0] == b[K][0]: K += 1
    for e in range(K):
        if a[e][1]*b[e][1] < 0:
            typ = a[e][0]
            def f(sv, e=e, typ=typ):
                L = events_of(sv); return L[e][1] if len(L) > e and L[e][0] == typ else float('nan')
            try:
                r = brentq(f, S[i], S[i + 1], xtol=1e-22, rtol=1e-15); roots.append(dict(type='Fix(R)' if typ == 'E' else 'brake', event=e, seed=i, log_s=math.log(r)))
            except Exception as ex: roots.append(dict(type=typ, event=e, seed=i, error=str(ex)))
per = math.log(lam)
print('roots found:', len(roots), flush=True)
for r in roots:
    if 'log_s' in r:
        dmin = min(abs(((r['log_s'] - c + per/2) % per) - per/2) for c in cross_logs)   # distance modulo the period
        r['dist_to_nearest_crossing_logs'] = dmin
        print('  %-7s event %2d seed %3d  log s %.8f  |dlog s| to nearest E-crossing %.2e' % (r['type'], r['event'], r['seed'], r['log_s'], dmin), flush=True)
    else: print('  ', r, flush=True)
matched = []
for c in cross_logs:
    best = min((abs(((r['log_s'] - c + per/2) % per) - per/2), r['type']) for r in roots if 'log_s' in r)
    matched.append(dict(cross_log_s=c, best_dlog=best[0], type=best[1])); print('crossing log s %.8f: nearest symmetric root |dlog s| %.2e (%s)' % (c, best[0], best[1]), flush=True)
json.dump(dict(roots=roots, matched=matched, period=per), open(os.path.join(HERE, '../results/v24_symE2.json'), 'w'), indent=1, default=str)
