"""V24 amendment E1: symmetry of W^u-S crossings w.r.t. Fix(R) and Fix(HR), H = half-return (equatorial reflection)."""
import os, json, math, numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
rec_prev = json.load(open(os.path.join(HERE, '../results/v24_symE.json')))['records']
import sys; sys.path.insert(0, os.path.join(HERE, '../../V20_ts_capture_edge_tangle/code')); import v20
FJ, fW, fH = v20.field('ts45', 0.97, 41/8); RT = 1e-12
z, Dm, T, clos = v20.polish(FJ, fH, 9.8045591682, RT); xs = z[0]
def H(zz, tmax=4000.0):
    x, px = zz; py = v20.py_from_H(fH, x, 0.0, px)
    if not np.isfinite(py): return None
    s0 = np.concatenate([[x, 0.0, px, py], np.eye(4).ravel()])
    def ev(t, s): return s[1] if t > 1e-6 else -1.0
    ev.direction = -1; ev.terminal = True
    def plunge(t, s): return s[0] - v20.XPLUNGE
    plunge.terminal = True
    sol = solve_ivp(v20.make_rhs(FJ), (0, tmax), s0, method='DOP853', rtol=RT, atol=RT*1e-3, events=[ev, plunge], t_eval=[])
    if sol.t_events[0].size == 0: return None
    s = sol.y_events[0][0]; return np.array([s[0], s[2]])     # reflect y -> -y: (x, p_x) unchanged, p_y -> -p_y
Pm = lambda q: v20.P(FJ, fH, q, RT)[0]
Rf = lambda q: np.array([q[0], -q[1]])
Hinv = lambda q: (lambda w: None if w is None else Rf(w))(H(Rf(q)))
out = {}
# control H^2 = P on points near U
ctrl = []
for q in ([12.0, 0.12], [20.0, 0.15], [30.0, 0.14], [45.0, 0.10], [9.9, 0.01]):
    q = np.array(q); a = H(q); b = H(a) if a is not None else None; c = Pm(q)
    if b is not None and c is not None: ctrl.append(float(np.max(np.abs(b - c))))
out['CTRL_H2_eq_P'] = ctrl; print('control |H(H(z)) - P(z)|:', ['%.1e' % c for c in ctrl], flush=True)
recs = []
for r in rec_prev:
    c = np.array(r['point']); label = r['kind'] + (' %s' % (r.get('seed_pair'),) if 'seed_pair' in r else '')
    ws = {0: c}; q = c
    for k in (1, 2):
        q = H(q) if q is not None else None; ws[k] = q
    q = c
    for k in (1, 2):
        q = Hinv(q) if q is not None else None; ws[-k] = q
    dR, dHR = {}, {}
    for k, w in ws.items():
        if w is None or abs(w[0] - xs) < 0.5: continue
        dR[k] = float(abs(w[1])); hw = H(Rf(w)); dHR[k] = float(np.linalg.norm(hw - w)) if hw is not None else None
    mR = min(dR.values()) if dR else None; vHR = [v for v in dHR.values() if v is not None]; mHR = min(vHR) if vHR else None
    m = min(x for x in (mR, mHR) if x is not None)
    which = 'Fix(R)' if mR is not None and mR == m else 'Fix(HR)'
    verdict = 'SYMMETRIC' if m <= 1e-8 else ('NON-SYMMETRIC' if m >= 1e-4 else 'UNRESOLVED')
    rr = dict(label=label, point=c.tolist(), min_dR=mR, min_dHR=mHR, best=which, verdict=verdict, dR=dR, dHR=dHR)
    recs.append(rr); print('%-24s c=%s  min dR %s  min dHR %s  -> %s (%s)' % (label, np.round(c, 6), '%.2e' % mR if mR is not None else '-', '%.2e' % mHR if mHR is not None else '-', verdict, which), flush=True)
out['records'] = recs
json.dump(out, open(os.path.join(HERE, '../results/v24_symE1.json'), 'w'), indent=1, default=str)
