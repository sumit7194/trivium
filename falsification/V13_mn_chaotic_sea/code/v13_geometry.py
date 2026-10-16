"""V13 geometry only (no orbits): equatorial CZV components, gate G-q at C0, D's delta_x per point, shared levels.
Metric from the bridge's V9 transcription (v9_nve.mn_functions), gated exactly against quantum's fields in V8/V9.
Reduced H = 1/2[g^xx px^2 + g^yy py^2 + W] = -1/2, W = g^tt E^2 - 2 g^tphi E Lz + g^phiphi Lz^2; allowed: -1 - W >= 0.
Usage: python v13_geometry.py [gate|levels]"""
import sys, os, json, math
import numpy as np, sympy as sp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V9_mn_obstruction_check/code'))
from v9_nve import mn_functions, x, y

R = sp.Rational
POINTS = {
    'p1': (5, 3, R(1, 5)),
    'p2': (13, 5, R(-1, 3)),
    'F5R': (89, 80, R(13394411, 1186380)),
    'C0': (1, R(9, 10), R(19, 20)/(R(19, 100))**R(3, 2)),
}
MR_LEVELS = {  # V9 row order, (E, L, mu2) -> (E/mu, L/(mu M))
    'p1': [(1, 0, 4), (1, 0, 9), (1, 1, 4)],
    'p2': [(1, 0, 4), (1, 0, 9), (1, 1, 4)],
}
XMAX = 1000.0

class Point:
    def __init__(self, name, params=None):
        M, a, beta = params if params is not None else POINTS[name]; self.name, self.M = name, sp.nsimplify(M)
        F = mn_functions(M, a, beta); f, om, k = F['f'], F['om'], F['k']; self.k = float(k)
        gtt = -f; gtp = f*om; gpp = -f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2)
        self.g_full = sp.lambdify((x, y), [gtt, gtp, gpp], 'numpy')
        self.g_eq = sp.lambdify(x, [e.subs(y, 0) for e in (gtt, gtp, gpp)], 'numpy')
        self.gpp_full = sp.lambdify((x, y), gpp, 'numpy')
        self.f_full = sp.lambdify((x, y), f, 'numpy')
    def allowed_eq(self, xs, E, L):
        """-1 - W(x, 0); L in units of M (Lz = L*M), x prolate."""
        gtt, gtp, gpp = [np.asarray(v, dtype=float) for v in self.g_eq(xs)]
        Lz = L*float(self.M); det = gtt*gpp - gtp**2
        W = (gpp*E**2 + 2*gtp*E*Lz + gtt*Lz**2)/det  # g^tt=gpp/det, g^tp=-gtp/det, g^pp=gtt/det
        return -1.0 - W
    def components(self, E, L, x_lo=1 + 1e-7, n=40000):
        xs = 1 + np.logspace(math.log10(x_lo - 1), math.log10(XMAX - 1), n)
        F = self.allowed_eq(xs, E, L); ok = np.isfinite(F) & (F >= 0)
        comps, i = [], 0
        while i < n:
            if ok[i]:
                j = i
                while j + 1 < n and ok[j + 1]: j += 1
                lo, nan_lo = (xs[i], False) if i == 0 else self._edge(F, xs, i - 1, i, E, L)
                hi, nan_hi = (xs[j], False) if j == n - 1 else self._edge(F, xs, j, j + 1, E, L)
                comps.append(dict(lo=float(lo), hi=float(hi), touches_inner=(i == 0), touches_outer=(j == n - 1),
                                  nan_edge=bool(nan_lo or nan_hi)))
                i = j + 1
            else: i += 1
        return comps
    def _edge(self, F, xs, a, b, E, L):
        """Root of -1-W between grid points a, b; if either side is non-finite, return the finite grid point (flagged)."""
        if not (np.isfinite(F[a]) and np.isfinite(F[b])):
            return (xs[b] if np.isfinite(F[b]) else xs[a]), True
        return brentq(lambda t: self.allowed_eq(np.array([t]), E, L)[0], xs[a], xs[b], xtol=1e-14), False
    def bounded(self, E, L, x_min=None):
        out = [c for c in self.components(E, L) if not c['touches_inner'] and not c['touches_outer']]
        if x_min is not None: out = [c for c in out if c['lo'] >= x_min]
        return out
    def ctc_extent(self, nx=400, ny=200):
        """Outer x-extent of {g_phiphi < 0} over |y| < 1 (grid, then bisection along each y line)."""
        ys = np.linspace(-0.995, 0.995, ny); xs = 1 + np.logspace(-6, math.log10(20), nx); xc = 1.0
        for yy in ys:
            v = np.asarray(self.gpp_full(xs, yy), dtype=float); neg = np.where(np.isfinite(v) & (v < 0))[0]
            if len(neg) == 0: continue
            j = neg.max()
            if j + 1 < nx:
                xr = brentq(lambda t: float(self.gpp_full(t, yy)), xs[j], xs[j + 1], xtol=1e-12)
            else: xr = xs[j]
            xc = max(xc, xr)
        return xc
    def delta_x(self):
        xc = self.ctc_extent(); d = (xc - 1) + 0.025
        return xc, math.ceil(d/0.05 - 1e-12)*0.05

def gate_Gq():
    P = Point('C0'); res = {}
    def nb(E, L): return len(P.bounded(E, L))
    def ncomp_away(E, L):  # components not touching the inner end (bound or outer-escaping), for join test
        return [c for c in P.components(E, L) if not c['touches_inner']]
    # join threshold at E=0.95: number of bounded components drops from 2 to 1 below L_join
    f_join = lambda L: len(P.bounded(0.95, L)) - 1.5
    Ls = np.linspace(2.9, 3.5, 121); counts = [len(P.bounded(0.95, L)) for L in Ls]
    res['counts_E095'] = dict(zip([round(v, 4) for v in Ls], counts))
    return res

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'gate'
    if mode == 'gate':
        print(json.dumps(gate_Gq(), indent=0)[:3000])
