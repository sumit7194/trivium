"""V11 addendum 3: neighbourhood ensembles with the late-escape criterion, TS orbit vs matched Kerr level.
usage: v11_ensemble.py <ts_case> <E> <L_ts> <x0> <m_ts> <kerr_case> <m_kerr> <label>"""
import sys, json, math, numpy as np
from v11_chaos import build, run_orbit, carter, KERR
OFFS = [0.0, -0.001, 0.001, -0.002, 0.002, -0.004, 0.004, -0.008, 0.008]

def quick(fns, x0, n=30):
    try:
        r = run_orbit(*fns, x0, 1e-11, ncross=n)
    except (ValueError, ZeroDivisionError):
        return 'forbidden'
    return 'plunge' if r['status'] == 'plunge' else ('survive' if r['crossings'] >= n else r['status'])

def allowed(fns, x0):
    fW, fGyy = fns[2], fns[3]
    v = (-1 - fW(x0, 0.0)) / fGyy(x0, 0.0)
    return v == v and v > 0

def bisect(fns, a, b, ca, tol=1e-4):
    while b - a > tol:
        m = 0.5 * (a + b); cm = quick(fns, m)
        if cm == ca: a = m
        else: b = m
    return 0.5 * (a + b)

def late_escape(r):
    return r['status'] == 'plunge' and r['crossings'] >= 50

def member(fns, x0, Qf=None):
    r = run_orbit(*fns, x0, 1e-13, Qf=Qf)
    return dict(x0=x0, status=r['status'], n=r['crossings'], late_escape=late_escape(r), R=r['R'], fd=r['fd'],
                S_trunc=r['S_ex_trunc'], H=r['H_drift'], carter=r['carter_rel_dev'])

if __name__ == '__main__':
    ts, E, Lts, x0, m_ts, kc, m_k, label = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6], float(sys.argv[7]), sys.argv[8]
    out = dict(label=label, ts=ts, E=E, L_ts=Lts, x0=x0)
    fT = build(ts, E, Lts)
    # TS boundary nearest x0 (for relative position)
    cl, cr = quick(fT, x0 - 0.05), quick(fT, x0 + 0.05)
    xb_ts = bisect(fT, x0 - 0.05, x0 + 0.05, cl) if cl != cr else None
    out['ts_boundary'] = xb_ts; out['ts_sides'] = [cl, cr]
    out['ts_members'] = [member(fT, x0 + d) for d in OFFS]
    print(label, 'TS done', json.dumps([(m['x0'], m['status'], m['n'], m['late_escape']) for m in out['ts_members']]), flush=True)
    # matched Kerr level: same E and L/m; boundary with the same orientation, same offset from it
    Lk = Lts / m_ts * m_k; fK = build(kc, E, Lk); Qf = carter(kc, E, Lk)
    grid = [1.6 + 0.1 * i for i in range(300)]
    cls = [(xg, quick(fK, xg) if allowed(fK, xg) else 'forbidden') for xg in grid]
    trans = [(cls[i][0], cls[i + 1][0], cls[i][1]) for i in range(len(cls) - 1)
             if {cls[i][1], cls[i + 1][1]} == {'plunge', 'survive'}]
    want = cl if xb_ts else None
    pick = next((t for t in trans if t[2] == want), trans[0] if trans else None)
    out['kerr_L'] = Lk; out['kerr_transitions'] = trans
    if pick and xb_ts is not None:
        xb_k = bisect(fK, pick[0], pick[1], pick[2]); xk0 = xb_k + (x0 - xb_ts)
        out['kerr_boundary'] = xb_k; out['kerr_x0'] = xk0
        out['kerr_members'] = [member(fK, xk0 + d, Qf) for d in OFFS]
    else:
        out['kerr_members'] = None; out['kerr_note'] = 'no matching survive/plunge transition at this Kerr level'
    fts = sum(m['late_escape'] for m in out['ts_members']) / 9
    fk = None if out['kerr_members'] is None else sum(m['late_escape'] for m in out['kerr_members']) / 9
    out['ts_frac'] = fts; out['kerr_frac'] = fk
    out['verdict'] = ('CONFIRMED' if fts >= 3 / 9 and fk == 0 else 'NOT CONFIRMED' if fts == 0 else 'INCONCLUSIVE')
    print(label, 'VERDICT', out['verdict'], 'TS frac', round(fts, 3), 'Kerr frac', fk, flush=True)
    json.dump(out, open(f'../results/ens_{label}.json', 'w'), indent=1, default=str)
