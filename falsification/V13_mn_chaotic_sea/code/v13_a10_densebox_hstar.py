"""V13 A10 LABELLED POST-HOC supplement to v13_a10_densebox.py: the EXACT L-infinity distance h* from the orbits to the
CTC set {g_phiphi <= 0 or non-finite}, at the samples where the 5e-4 CTC grid puts it below 0.0265. h* is found by
bisection on the box half-width h (to 1e-8): box-min of g_phiphi over [x +/- h] x [y +/- h] (41 x 41 grid, then
scipy L-BFGS-B from the 3 lowest grid points) changes sign at h = h*. The strict B9 box (h = 0.025) passes iff
h* > 0.025; margin = h* - 0.025. Also reports where the box minimum sits (a corner of the box or not) and g_phiphi at
the four corners for the tightest sample. Writes results/v13_a10_densebox_hstar_<pt>.json. Usage: python v13_a10_densebox_hstar.py C0|F5R (one process each)."""
import sys, os, json, math, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v13_a10_densebox as DB
import v13_a10_multishoot as M

def boxmin(g, x, y, h):
    xs = np.linspace(x - h, x + h, 41); ys = np.linspace(max(y - h, -1 + 1e-15), min(y + h, 1 - 1e-15), 41)
    G = np.array([[g(a, b) for b in ys] for a in xs])
    if not np.isfinite(G).all(): return -np.inf, None
    best = (float(G.min()), (float(xs[np.unravel_index(G.argmin(), G.shape)[0]]), float(ys[np.unravel_index(G.argmin(), G.shape)[1]])))
    for k in np.argsort(G, axis=None)[:3]:
        i, j = np.unravel_index(k, G.shape)
        r = minimize(lambda p: g(p[0], p[1]), np.array([xs[i], ys[j]]), method='L-BFGS-B',
                     bounds=[(x - h, x + h), (max(y - h, -1 + 1e-15), min(y + h, 1 - 1e-15))])
        if not math.isfinite(r.fun): return -np.inf, None
        if r.fun < best[0]: best = (float(r.fun), (float(r.x[0]), float(r.x[1])))
    return best

def hstar(g, x, y):
    lo, hi = 0.015, 0.035
    if boxmin(g, x, y, lo)[0] <= 0: return lo, 'h* below 0.015'
    if boxmin(g, x, y, hi)[0] > 0: return hi, 'h* above 0.035'
    while hi - lo > 1e-8:
        m = 0.5*(lo + hi)
        if boxmin(g, x, y, m)[0] > 0: lo = m
        else: hi = m
    return 0.5*(lo + hi), 'ok'

def run_point(pt, log):
    R = json.load(open(os.path.join(M.RES, f'v13_a10_{pt}.json'))); sc = [R['scaling']['xscale'], R['scaling']['pscale']]
    DB.setup(pt, sc); DB.ctc_setup(log); g = DB.W['gpp']
    A9 = json.load(open(os.path.join(M.RES, M.A9F[pt])))
    def orbits():
      for u in A9['upos']:
        smp, _, _ = DB.orbit_samples([np.array(u['z'])], u['period'], [False]); yield (f"UPO {u['idx']}", smp)
      for e in R['edges']:
        if not (e['CONFIRMED_MS'] or e['A9_CONFIRMED']): continue
        j = M.edge_jobs(pt, {(e['src'], e['dst'])})[3][0]
        Ed = M.Edge(j['zi'], j['vi'], j['pi'], j['a'], j['zg'], j['vg'], j['pg'], j['b'])
        s, w, sp_, u = Ed.unpack(np.array(e['ms_13']['X']))
        su = DB.orbit_samples(w[:Ed.a], Ed.pi, [False]*Ed.a)[0] if Ed.a else np.array([[w[0][0], 0.0]])
        ss = DB.orbit_samples(u[:Ed.b], Ed.pg, [True]*Ed.b)[0] if Ed.b else np.array([[u[0][0], 0.0]])
        yield (f"{e['src']}->{e['dst']}" + ('' if e['CONFIRMED_MS'] else ' (A9 only)'), np.concatenate([su, ss]))
    out = []
    for name, smp in orbits():
        d, _ = DB.W['tree'].query(smp, k=1, p=np.inf)
        cand = np.argsort(d)[:20]; cand = [k for k in cand if d[k] < 0.0265] or [int(np.argmin(d))]
        best = None
        for k in cand:
            h, st = hstar(g, *smp[k])
            if best is None or h < best[0]: best = (h, st, k)
        h, st, k = best; x, y = smp[k]
        bm, loc = boxmin(g, x, y, DB.BOX)
        corners = {f'{sx:+d}{sy:+d}': float(g(x + sx*DB.BOX, y + sy*DB.BOX)) for sx in (-1, 1) for sy in (-1, 1)}
        rec = dict(orbit=name, h_star=h, margin=h - DB.BOX, status=st, strict_in_D_exact=bool(h > DB.BOX), sample=dict(x=float(x), y=float(y)),
                   boxmin_at_0025=bm, boxmin_location=loc, boxmin_at_corner=bool(loc is not None and abs(abs(loc[0] - x) - DB.BOX) < 1e-9 and abs(abs(loc[1] - y) - DB.BOX) < 1e-9),
                   gpp_corners=corners, grid_Linf_dist=float(d[k]), n_candidates=len(cand))
        del smp; out.append(rec); log(pt, name, 'h* %.7f margin %+.2e' % (h, h - DB.BOX), st, 'boxmin %.4g at corner %s' % (bm, rec['boxmin_at_corner']), 'sample', (round(x, 6), round(y, 6)))
    return out

if __name__ == '__main__':
    pt = sys.argv[1]; T0 = time.time(); env, commit = M.env_commit()
    log = lambda *a: print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)
    res = dict(label='LABELLED POST-HOC supplement (exact L-inf distance to the CTC set)', point=pt, commit=commit, env=env)
    res['orbits'] = run_point(pt, log); M.rss_guard(log)
    res['min_margin'] = min(r['margin'] for r in res['orbits'])
    res['runtime_s'] = time.time() - T0; res['peak_rss_mb'] = M.rss_mb()
    json.dump(res, open(os.path.join(M.RES, f'v13_a10_densebox_hstar_{pt}.json'), 'w'), indent=1)
    log(f'wrote results/v13_a10_densebox_hstar_{pt}.json; min margin', res['min_margin'], 'peak RSS', res['peak_rss_mb'])
