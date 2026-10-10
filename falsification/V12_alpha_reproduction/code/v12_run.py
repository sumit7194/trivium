"""V12 driver: systems (3 TS levels + bridge-computed Kerr partners), window scan, nested-epsilon sampling with per-batch
checkpoints, multiprocessing; gate G3 (numba vs scipy) and G5 (H drift, Carter drift).
Usage: python v12_run.py systems | windows | G3 | primary [workers] | E1 [workers] | E2 [workers] | fit"""
import sys, os, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, '../results')
sys.path.insert(0, HERE)

EPS = [3e-3, 1e-3, 3e-4, 1e-4, 3e-5]
EPS_E1 = EPS + [1e-5, 3e-6, 1e-6]
TS_LEVELS = [('L1', 'ts45', 'kerr45', 0.97, 5.125), ('L2', 'ts45', 'kerr45', 0.97, 5.875), ('L3', 'ts35', 'kerr35', 0.95, -16/3)]
RTOL, ATOL_F = 1e-11, 1e-2          # atol = rtol * 1e-2, as V11
N_CROSS, TAU_MAX, MAX_STEPS = 300, 5e6, 3_000_000

def systems():
    """6 systems with exact L. Kerr |L| = L_sep,K (1 + eps_sep,TS); sign = TS chart sign (both charts have J < 0 in their
    own (t, phi) orientation -- checked in v12_lsep -- so equal chart sign = equal sign(L J))."""
    lsep = {(d['case'], d['sense']): d for d in json.load(open(os.path.join(RES, 'v12_lsep.json')))}
    out = []
    for i, (lev, ts, kr, E, L) in enumerate(TS_LEVELS):
        s = 1 if L > 0 else -1
        dT, dK = lsep[(ts, s)], lsep[(kr, s)]
        assert dT['J_sign'] == dK['J_sign']
        eps_sep = (abs(L) - dT['L_sep'])/dT['L_sep']
        LK = s*dK['L_sep']*(1 + eps_sep)
        out.append(dict(idx=2*i, level=lev, case=ts, E=E, L=L, eps_sep=eps_sep, sense=dT['physical_sense']))
        out.append(dict(idx=2*i + 1, level=lev, case=kr, E=E, L=LK, eps_sep=eps_sep, sense=dK['physical_sense']))
    return out

_W = {}
def _integ(sysd):
    key = (sysd['case'], sysd['E'], sysd['L'])
    if key not in _W:
        from v12_orbit import make
        _W[key] = make(*key)[0]
    return _W[key]

def outcome(sysd, x0, px0=0.0, N=N_CROSS, rtol=RTOL, record=0):
    r = _integ(sysd)(x0, px0, N, rtol, rtol*ATOL_F, TAU_MAX, MAX_STEPS, record)
    return int(r[0]), r

def allowed_interval(sysd):
    from v12_lsep import equatorial_inverse, Wfun, x_in
    W = Wfun(equatorial_inverse(sysd['case']), sysd['E'], sysd['L'])
    lo = max(x_in(sysd['case']), 1.5)
    xs = np.linspace(lo, 400, 400001); ok = W(xs) + 1 < 0
    assert ok[0], 'start region does not touch the inner boundary'
    hi = xs[np.argmax(~ok)] if not ok.all() else 400.0
    from scipy.optimize import brentq
    if hi < 400: hi = brentq(lambda x: W(x) + 1, xs[np.argmax(~ok) - 1], hi, xtol=1e-13)
    return lo, hi

def _changes(sysd, xs):
    oc = np.array([outcome(sysd, x)[0] for x in xs]); return oc, np.flatnonzero(oc[1:] != oc[:-1])

def window(sysd, n=400):
    """Addendum 5: two-stage window on the INNER transition (primary) and the OUTER transition (secondary)."""
    lo, hi = allowed_interval(sysd)
    xs = np.linspace(lo, hi, n + 2)[1:-1]; oc, ch = _changes(sysd, xs); step = xs[1] - xs[0]
    res = dict(lo=lo, hi=hi, n_changes=int(len(ch)), scan_outcomes=np.bincount(oc, minlength=5).tolist())
    if len(ch) == 0: res['W'] = None; return res
    for name, c in (('W', ch[0]), ('W_outer', ch[-1])):
        a0, b0 = max(lo, xs[c] - 3*step), min(hi, xs[c + 1] + 3*step)
        xd = np.linspace(a0, b0, n); ocd, chd = _changes(sysd, xd); sd = xd[1] - xd[0]
        a, b = xd[chd[0]] - 3*sd, xd[chd[-1] + 1] + 3*sd
        if b - a < 10*max(EPS):
            cc = 0.5*(a + b); a, b = cc - 5*max(EPS), cc + 5*max(EPS)
        a, b = max(a, lo + max(EPS)*1.0001), min(b, hi - max(EPS)*1.0001)
        res[name] = [float(a), float(b)]; res[name + '_dense_changes'] = int(len(chd))
        res[name + '_dense_outcomes'] = np.bincount(ocd, minlength=5).tolist()
    return res

def _batch(args):
    sysd, x0s, eps, px_mode, N, rtol = args
    base, minus, plus, hd, cap = [], [], [], 0.0, 0
    for x0 in x0s:
        if px_mode:
            ob, r = outcome(sysd, x0, 0.0, N, rtol)
            om = [outcome(sysd, x0, -e, N, rtol)[0] for e in eps]; op = [outcome(sysd, x0, e, N, rtol)[0] for e in eps]
        else:
            ob, r = outcome(sysd, x0, 0.0, N, rtol)
            om = [outcome(sysd, x0 - e, 0.0, N, rtol)[0] for e in eps]; op = [outcome(sysd, x0 + e, 0.0, N, rtol)[0] for e in eps]
        if ob == 0: hd = max(hd, r[3])
        base.append(ob); minus.append(om); plus.append(op)
    return np.array(base), np.array(minus), np.array(plus), hd

def run(tag, sysl, eps, K=2000, workers=6, batch=50, px_mode=False, N=N_CROSS, rtol=RTOL, seed_base=12000, wkey='W'):
    from multiprocessing import get_context
    wins = json.load(open(os.path.join(RES, 'v12_windows.json')))
    for sysd in sysl:
        out = os.path.join(RES, f'v12_{tag}_s{sysd["idx"]}.npz')
        if os.path.exists(out): print('done already', out); continue
        a, b = wins[str(sysd['idx'])][wkey]
        x0 = np.random.default_rng(seed_base + sysd['idx']).uniform(a, b, K)
        ckdir = os.path.join(RES, f'ck_{tag}_s{sysd["idx"]}'); os.makedirs(ckdir, exist_ok=True)
        jobs = [(i, (sysd, x0[i:i + batch], eps, px_mode, N, rtol)) for i in range(0, K, batch)
                if not os.path.exists(os.path.join(ckdir, f'{i:05d}.npz'))]
        t0 = time.time()
        with get_context('fork').Pool(workers) as pool:
            for (i, _), res in zip(jobs, pool.imap(_batch, [j for _, j in jobs])):
                np.savez(os.path.join(ckdir, f'{i:05d}.npz'), base=res[0], minus=res[1], plus=res[2], hd=res[3])
                print(f'{tag} s{sysd["idx"]} batch {i} done ({time.time() - t0:.0f}s)', flush=True)
        parts = [np.load(os.path.join(ckdir, f'{i:05d}.npz')) for i in range(0, K, batch)]
        np.savez(out, x0=x0, eps=np.array(eps), base=np.concatenate([p['base'] for p in parts]),
                 minus=np.concatenate([p['minus'] for p in parts]), plus=np.concatenate([p['plus'] for p in parts]),
                 H_drift_max=max(float(p['hd']) for p in parts), sysd=json.dumps(sysd))
        print('wrote', out, flush=True)

def G3(n_per=75, only=None):
    from v12_ref import make_ref
    wins = json.load(open(os.path.join(RES, 'v12_windows.json'))); sysl = systems(); rows = []
    for sysd in [s for s in sysl if s['level'] in ('L1', 'L3') and (only is None or s['idx'] == only)]:
        ref = make_ref(sysd['case'], sysd['E'], sysd['L']); a, b = wins[str(sysd['idx'])]['W']
        for x0 in np.random.default_rng(3000 + sysd['idx']).uniform(a, b, n_per):
            o, r = outcome(sysd, x0, record=20); q = ref(x0, 0.0, N_CROSS, RTOL, RTOL*ATOL_F)
            n = min(r[1], len(q['secx']), 20)
            dx = max([abs(u - v) for u, v in zip(r[5][:n], q['secx'][:n])] or [0.0])
            rows.append(dict(idx=sysd['idx'], x0=float(x0), numba=o, scipy=q['outcome'], same=o == q['outcome'],
                             survivor=(o == 0 and q['outcome'] == 0), dx20=float(dx)))
            print(json.dumps(rows[-1]), flush=True)
    same = np.mean([r['same'] for r in rows]); dxs = [r['dx20'] for r in rows if r['survivor']]
    summ = dict(n=len(rows), same_frac=float(same), survivors=len(dxs), max_dx20=float(max(dxs) if dxs else 0),
                n_dx_over_1e7=int(sum(d > 1e-7 for d in dxs)), pass_=bool(same >= 0.99 and all(d <= 1e-7 for d in dxs)))
    json.dump(dict(summary=summ, rows=rows), open(os.path.join(RES, f'v12_G3{"" if only is None else "_s%d" % only}.json'), 'w'), indent=1)
    print(json.dumps(summ))

if __name__ == '__main__':
    mode = sys.argv[1]; workers = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    if mode == 'systems':
        for s in systems(): print(json.dumps(s))
    elif mode == 'windows':
        w = {}
        for s in systems():
            w[str(s['idx'])] = {**window(s), **s}; print(json.dumps(w[str(s['idx'])]), flush=True)
        json.dump(w, open(os.path.join(RES, 'v12_windows.json'), 'w'), indent=1)
    elif mode == 'G3': G3(only=int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif mode == 'primary': run('primary', systems(), EPS, workers=workers)
    elif mode == 'outer': run('outer', systems(), EPS, workers=workers, seed_base=15000, wkey='W_outer')
    elif mode == 'E1':
        L1 = [s for s in systems() if s['level'] == 'L1']
        run('E1_N300', L1, EPS_E1, workers=workers, rtol=1e-13, seed_base=13000)
        run('E1_N600', L1, EPS_E1, workers=workers, rtol=1e-13, N=600, seed_base=13000)
    elif mode == 'E2':
        run('E2_px', [s for s in systems() if s['level'] == 'L1'], EPS, workers=workers, px_mode=True, seed_base=14000)
