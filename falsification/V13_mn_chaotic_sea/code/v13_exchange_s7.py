"""V13 §7 exchange (bridge side): from the SEALED counted screens (c365279), per shared level compute the CHAOTIC
fraction with a Clopper-Pearson 95% CI, the return-time median, and the occupied cells of the 200 x 200 Jaccard grid
(geometry-defined box: the x-range of the shared level's bound-in-D equatorial component, and p_x in +-sqrt(max p_x^2)
over that range on y = 0, p_y = 0) for CHAOTIC orbits and for all READ orbits. Read-only on the sealed JSONs."""
import sys, os, json, math
import numpy as np, sympy as sp
from scipy.stats import beta as Beta
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_screen import POINTS, SHARED, RES
from v13_field import build, W_reg, ginv_reg
from v9_nve import x as X, y as Y

def cp(k, n):
    lo = 0.0 if k == 0 else Beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else Beta.ppf(0.975, k + 1, n - k)
    return [float(lo), float(hi)]

out = {}
for key in ('p1', 'p2', 'F5R'):
    d = json.load(open(os.path.join(RES, f'v13_counted_{key}.json')))
    (x0, x1), = d['comps']
    M, a_, beta = POINTS[key]; E, ell = SHARED[key]
    S = build(M, a_, beta); gxx, _ = ginv_reg(S); W = W_reg(S, E, ell*sp.nsimplify(M))
    f = sp.lambdify([X], ((-1 - W)/gxx).subs(Y, 0), 'mpmath')
    xs = np.linspace(x0, x1, 4001)
    p2max = max(float(f(v)) for v in xs); pmax = math.sqrt(max(p2max, 0.0))
    nx = ny = 200
    def cells(orbs):
        s = set()
        for o in orbs:
            for row in o.get('sec', []):
                xv, pv = row[0], row[1]
                i = int((xv - x0)/(x1 - x0)*nx); j = int((pv + pmax)/(2*pmax)*ny)
                if 0 <= i < nx and 0 <= j < ny: s.add(i*ny + j)
        return sorted(s)
    read = [o for o in d['orbits'] if o.get('status') == 'READ']
    ch = [o for o in read if o.get('verdict') == 'CHAOTIC']
    rt = [o['ret_time_median'] for o in read if o.get('ret_time_median') is not None]
    rt_ch = [o['ret_time_median'] for o in ch if o.get('ret_time_median') is not None]
    out[key] = dict(level=dict(E=str(E), ell=str(ell)), n=d['n'], n_read=len(read), n_chaotic=len(ch),
                    chaotic_fraction=len(ch)/len(read) if read else None, cp95=cp(len(ch), len(read)),
                    ret_time_median_all=float(np.median(rt)) if rt else None,
                    ret_time_median_chaotic=float(np.median(rt_ch)) if rt_ch else None,
                    grid=dict(x=[x0, x1], px=[-pmax, pmax], nx=nx, ny=ny, cell_index='i*ny + j'),
                    cells_chaotic=cells(ch), n_cells_chaotic=len(cells(ch)), n_cells_read=len(cells(read)),
                    chaotic_orbits=[dict(i=o['i'], x0=o['x0'], A1=o['A1'], A2=o['A2']) for o in ch],
                    source=f'results/v13_counted_{key}.json (sealed c365279)')
json.dump(out, open(os.path.join(RES, 'v13_s7_exchange_bridge.json'), 'w'), indent=1)
for k, v in out.items():
    print(k, v['level'], f"{v['n_chaotic']}/{v['n_read']}", v['cp95'], 'rt_all', round(v['ret_time_median_all'], 3), 'rt_ch', v['ret_time_median_chaotic'], 'grid px', round(v['grid']['px'][1], 5), 'cells_ch', v['n_cells_chaotic'], 'cells_read', v['n_cells_read'])
