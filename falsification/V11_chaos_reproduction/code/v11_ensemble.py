"""V11 addendum 3: neighbourhood ensembles with the late-escape criterion, TS orbit vs matched Kerr level.
usage: v11_ensemble.py <ts_case> <E> <L_ts> <x0> <m_ts> <kerr_case> <m_kerr> <label>"""
import sys, json, math, os, numpy as np
from v11_chaos import build, run_orbit, carter, KERR
OFFS = [0.0, -0.001, 0.001, -0.002, 0.002, -0.004, 0.004, -0.008, 0.008]

def quick(fns, x0, n=30, tag=''):
    return ck_get(f'quick|{tag}|{x0!r}|{n}', lambda: _quick(fns, x0, n))

def _quick(fns, x0, n=30):
    try:
        r = run_orbit(*fns, x0, 1e-11, ncross=n)
    except (ValueError, ZeroDivisionError):
        return 'forbidden'
    return 'plunge' if r['status'] == 'plunge' else ('survive' if r['crossings'] >= n else r['status'])   # 'capped' stays its own class

def allowed(fns, x0):
    fW, fGyy = fns[2], fns[3]
    v = (-1 - fW(x0, 0.0)) / fGyy(x0, 0.0)
    return v == v and v > 0

def bisect(fns, a, b, ca, tol=1e-4, tag=''):
    while b - a > tol:
        m = 0.5 * (a + b); cm = quick(fns, m, tag=tag)
        if cm == ca: a = m
        else: b = m
    return 0.5 * (a + b)

def late_escape(r):
    return r['status'] == 'plunge' and r['crossings'] >= 50

CK = None   # per-label checkpoint file (power-loss safe); one JSON line per finished computation

def ck_load():
    d = {}
    if CK and os.path.exists(CK):
        for l in open(CK):
            e = json.loads(l); d[e['key']] = e['val']
    return d

def ck_get(key, fn):
    d = ck_load()
    if key in d: return d[key]
    v = fn()
    with open(CK, 'a') as f: f.write(json.dumps({'key': key, 'val': v}, default=str) + '\n'); f.flush(); os.fsync(f.fileno())
    return v

def member(fns, x0, Qf=None, tag=''):
    return ck_get(f'member|{tag}|{x0!r}', lambda: _member(fns, x0, Qf))

def _member(fns, x0, Qf=None):
    r = run_orbit(*fns, x0, 1e-13, Qf=Qf)
    return dict(x0=x0, status=r['status'], n=r['crossings'], late_escape=late_escape(r), R=r['R'], fd=r['fd'],
                S_trunc=r['S_ex_trunc'], H=r['H_drift'], carter=r['carter_rel_dev'])

def basin_score(members):
    """Addendum 4: order by x0; S = survived the 300-crossing budget, P(n) = plunged after n crossings.
    T = number of S/P status changes; V = strict reversals of n along each P run, oriented toward the adjacent S block
    (or toward the larger-n end if there is no adjacent S block / S on both sides)."""
    capped = [m['x0'] for m in members if m['status'] in ('capped', 'stalled')]
    ms = sorted([m for m in members if m['status'] not in ('capped', 'stalled')], key=lambda m: m['x0'])
    st = ['P' if m['status'] == 'plunge' else 'S' for m in ms]
    T = sum(1 for i in range(len(st) - 1) if st[i] != st[i + 1])
    V = 0; i = 0
    while i < len(st):
        if st[i] != 'P': i += 1; continue
        j = i
        while j + 1 < len(st) and st[j + 1] == 'P': j += 1
        ns = [ms[k]['n'] for k in range(i, j + 1)]
        leftS, rightS = i > 0 and st[i - 1] == 'S', j < len(st) - 1 and st[j + 1] == 'S'
        toward_right = rightS and not leftS or (not (leftS ^ rightS) and ns[-1] >= ns[0])
        seq = ns if toward_right else ns[::-1]
        V += sum(1 for a, b in zip(seq[:-1], seq[1:]) if b < a)
        i = j + 1
    return dict(order=[(m['x0'], s_, m['n']) for m, s_ in zip(ms, st)], T=T, V=V, budget=300, capped=capped)

if __name__ == '__main__':
    ts, E, Lts, x0, m_ts, kc, m_k, label = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6], float(sys.argv[7]), sys.argv[8]
    CK = f'../results/ens_{label}_checkpoint.jsonl'
    out = dict(label=label, ts=ts, E=E, L_ts=Lts, x0=x0)
    fT = build(ts, E, Lts)
    # TS boundary nearest x0 (for relative position)
    cl, cr = quick(fT, x0 - 0.05, tag='T'), quick(fT, x0 + 0.05, tag='T')
    xb_ts = bisect(fT, x0 - 0.05, x0 + 0.05, cl, tag='T') if cl != cr else None
    out['ts_boundary'] = xb_ts; out['ts_sides'] = [cl, cr]
    out['ts_members'] = [member(fT, x0 + d, tag='T') for d in OFFS]
    print(label, 'TS done', json.dumps([(m['x0'], m['status'], m['n'], m['late_escape']) for m in out['ts_members']]), flush=True)
    # matched Kerr level: same E and L/m; boundary with the same orientation, same offset from it
    Lk = Lts / m_ts * m_k; fK = build(kc, E, Lk); Qf = carter(kc, E, Lk)
    grid = [1.6 + 0.1 * i for i in range(300)]
    cls = [(xg, quick(fK, xg, tag='K') if allowed(fK, xg) else 'forbidden') for xg in grid]
    trans = [(cls[i][0], cls[i + 1][0], cls[i][1]) for i in range(len(cls) - 1)
             if {cls[i][1], cls[i + 1][1]} == {'plunge', 'survive'}]
    want = cl if xb_ts else None
    pick = next((t for t in trans if t[2] == want), trans[0] if trans else None)
    out['kerr_L'] = Lk; out['kerr_transitions'] = trans
    if pick and xb_ts is not None:
        xb_k = bisect(fK, pick[0], pick[1], pick[2], tag='K'); xk0 = xb_k + (x0 - xb_ts)
        out['kerr_boundary'] = xb_k; out['kerr_x0'] = xk0
        out['kerr_members'] = [member(fK, xk0 + d, Qf, tag='K') for d in OFFS]
    else:
        out['kerr_members'] = None; out['kerr_note'] = 'no matching survive/plunge transition at this Kerr level'
    fts = sum(m['late_escape'] for m in out['ts_members']) / 9
    fk = None if out['kerr_members'] is None else sum(m['late_escape'] for m in out['kerr_members']) / 9
    out['ts_frac'] = fts; out['kerr_frac'] = fk
    out['late_escape_descriptive'] = dict(ts_frac=fts, kerr_frac=fk)
    bt = basin_score(out['ts_members']); out['ts_basin'] = bt
    bk = basin_score(out['kerr_members']) if out['kerr_members'] else None; out['kerr_basin'] = bk
    kcarter = None if not out['kerr_members'] else max((m['carter'] or 0) for m in out['kerr_members'])
    out['kerr_carter_max'] = kcarter
    ts_ch = bt['T'] >= 2 or bt['V'] >= 2
    kerr_ok = bk is not None and bk['T'] <= 1 and bk['V'] == 0 and kcarter is not None and kcarter < 1e-8
    enough = len(bt['order']) >= 6 and (bk is None or len(bk['order']) >= 6)
    out['verdict'] = ('INCONCLUSIVE' if not enough else 'CONFIRMED' if ts_ch and kerr_ok else 'NOT CONFIRMED' if (bt['T'] <= 1 and bt['V'] == 0) else 'INCONCLUSIVE')
    print(label, 'VERDICT', out['verdict'], 'TS T/V', bt['T'], bt['V'], 'Kerr T/V', None if bk is None else (bk['T'], bk['V']),
          'Kerr Carter max', kcarter, '| late-escape (descriptive) TS', round(fts, 3), 'Kerr', fk, flush=True)
    json.dump(out, open(f'../results/ens_{label}.json', 'w'), indent=1, default=str)
