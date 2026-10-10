"""V12 reference integrator for gate G3: scipy solve_ivp DOP853 on the same reduced flow (sympy-lambdified, no numba
in the right-hand side's construction path beyond the shared metric), outcome rules as in v12_orbit."""
import math, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from v12_lsep import get_metric, X, Y

def make_ref(case, E, L):
    g = get_metric(case); E, L = sp.nsimplify(E), sp.nsimplify(L)
    det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    Gtt, Gtp, Gpp = g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det
    Aa, Bb = 1/g['g_xx'], 1/g['g_yy']; W = Gtt*E**2 - 2*Gtp*E*L + Gpp*L**2
    px, py = sp.symbols('px py')
    H = (Aa*px**2 + Bb*py**2 + W)/2
    F = sp.lambdify([X, Y, px, py], [sp.diff(H, px), sp.diff(H, py), -sp.diff(H, X), -sp.diff(H, Y)], 'math', cse=True)
    Wf = sp.lambdify([X, Y], W, 'math'); Bf = sp.lambdify([X, Y], Bb, 'math'); Af = sp.lambdify([X, Y], Aa, 'math')

    def run(x0, px0, N, rtol, atol, tau_max=5e6, chunk=50.0, record=20):
        rest = -1.0 - Wf(x0, 0.0) - Af(x0, 0.0)*px0**2
        if rest <= 0: return dict(outcome=4, crossings=0, secx=[])
        z = np.array([x0, 0.0, px0, math.sqrt(rest/Bf(x0, 0.0))]); t = 0.0
        def up(t, z): return z[1]
        up.direction = 1
        def pl(t, z): return z[0] - 1.5
        pl.terminal = True; pl.direction = -1
        def es(t, z): return z[0] - 2000.0
        es.terminal = True; es.direction = 1
        def ey(t, z): return abs(z[1]) - 0.999999
        ey.terminal = True; ey.direction = 1
        cross = []
        while t < tau_max:
            sol = solve_ivp(lambda t, z: F(*z), (t, min(t + chunk, tau_max)), z, method='DOP853', rtol=rtol, atol=atol,
                            events=[up, pl, es, ey])
            cr = [(te, ze[0]) for te, ze in zip(sol.t_events[0], sol.y_events[0]) if te > 1e-9]
            term = [(te[0], k) for k, te in ((1, sol.t_events[1]), (2, sol.t_events[2]), (2, sol.t_events[3])) if len(te)]
            tt = min(term)[0] if term else np.inf
            for te, xe in cr:
                if te < tt:
                    cross.append(xe)
                    if len(cross) >= N: return dict(outcome=0, crossings=len(cross), secx=cross[:record])
            if term: return dict(outcome=min(term)[1], crossings=len(cross), secx=cross[:record])
            z = sol.y[:, -1]; t = sol.t[-1]
        return dict(outcome=0, crossings=len(cross), secx=cross[:record])
    return run
