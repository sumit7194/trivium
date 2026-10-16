"""V13 A8: re-apply the registered p2 fallback with the 2-D bound-inside-D criterion (geometry only)."""
import sys, os, json
import sympy as sp
from fractions import Fraction as Fr
from v13_geometry import Point
from v13_geom2d import bound2d
R = sp.Rational; par = (13, 5, R(-1, 3)); Q = Point('p2')
grid = [(Fr(900 + 5*i, 1000), Fr(10 + j, 10)) for i in range(20) for j in range(36)]
grid.sort(key=lambda g: (abs(float(g[0]) - 0.5)/0.005 + abs(float(g[1]) - 0.0)/0.1, g[0], g[1]))
tried = []
for g in grid:
    b = [c for c in Q.bounded(float(g[0]), float(g[1]), 1.05) if c['hi'] - c['lo'] >= 0.05 and not c['nan_edge']]
    if not b: continue
    c = max(b, key=lambda c: c['hi'] - c['lo']); xe = 0.5*(c['lo'] + c['hi'])
    r = bound2d(*par, R(g[0].numerator, g[0].denominator), R(g[1].numerator, g[1].denominator), xe, nx=300, ny=240)
    tried.append(dict(E=str(g[0]), ell=str(g[1]), eq=(c['lo'], c['hi']), **{k: v for k, v in r.items() if k != 'x_range'}))
    print(g, r['ok'], round(r.get('frac_cells_outside_D', -1), 3), flush=True)
    if r['ok']:
        r2 = bound2d(*par, R(g[0].numerator, g[0].denominator), R(g[1].numerator, g[1].denominator), xe)  # full-resolution confirm
        if r2['ok']: tried[-1]['confirmed_500x400'] = True; break
json.dump(tried, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/v13_p2_fallback_2d.json'), 'w'), indent=1)
print('chosen', tried[-1]['E'], tried[-1]['ell'], tried[-1]['eq'])
