"""V13 A8: 2-D bound-inside-D test for a level (geometry only). The allowed set {-1 - W(x, y) >= 0} is gridded on
x - 1 in log space [1e-4, 1e3] x y in [-0.999, 0.999]. The 4-connected component containing the equatorial interval
counts as BOUND-IN-D iff no cell of it touches the grid's inner edge (x -> 1), the outer edge, or |y| = 0.999, and every
cell satisfies D_B9 (x - 1 >= 0.05, R^2 >= 0.25, g_phiphi > 0 on the +/-0.025 box)."""
import sys, os, math
import numpy as np, sympy as sp
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_field import build, W_reg, gpp_reg, x as X, y as Y
def bound2d(M, a_, beta, E, ell, x_eq, nx=500, ny=400):
    S = build(M, a_, beta); E = sp.nsimplify(E); Lz = sp.nsimplify(ell)*sp.nsimplify(M)
    Wf = sp.lambdify((X, Y), W_reg(S, E, Lz), 'numpy'); gf = sp.lambdify((X, Y), gpp_reg(S), 'numpy')
    xs = 1 + np.logspace(-4, 3, nx); ys = np.linspace(-0.999, 0.999, ny); XX, YY = np.meshgrid(xs, ys, indexing='ij')
    with np.errstate(all='ignore'):
        allowed = np.nan_to_num(-1.0 - Wf(XX, YY), nan=-1.0) >= 0
        g0 = np.nan_to_num(gf(XX, YY), nan=-1.0)
        gbox = np.minimum.reduce([np.nan_to_num(gf(XX + dx, np.clip(YY + dy, -0.9999, 0.9999)), nan=-1.0)
                                  for dx in (-0.025, 0, 0.025) for dy in (-0.025, 0, 0.025)])
    inD = (XX - 1 >= 0.05) & (XX**2 + YY**2 - 1 >= 0.25) & (g0 > 0) & (gbox > 0)
    lab, _ = ndimage.label(allowed)
    i = int(np.argmin(abs(xs - x_eq))); j = int(np.argmin(abs(ys)))
    L = lab[i, j]
    if L == 0: return dict(ok=False, reason='equatorial point not allowed on grid')
    comp = lab == L
    touches = bool(comp[0, :].any() or comp[-1, :].any() or comp[:, 0].any() or comp[:, -1].any())
    frac_out = float((comp & ~inD).sum()/comp.sum())
    return dict(ok=(not touches and frac_out == 0.0), touches_edge=touches, frac_cells_outside_D=frac_out, n_cells=int(comp.sum()),
                x_range=(float(xs[comp.any(1)].min()), float(xs[comp.any(1)].max())), y_absmax=float(abs(ys[comp.any(0)]).max()))
if __name__ == '__main__':
    R = sp.Rational
    for nm, par, E, ell, xe in [('p1', (5, 3, R(1, 5)), R(37, 40), R(29, 10), 5.5), ('p2', (13, 5, R(-1, 3)), R(9, 10), R(13, 10), 5.0),
                                ('F5R', (89, 80, R(13394411, 1186380)), R(19, 20), R(3), 18.0)]:
        print(nm, E, ell, bound2d(*par, E, ell, xe), flush=True)
