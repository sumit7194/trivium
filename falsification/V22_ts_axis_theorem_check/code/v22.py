"""V22 (PREREGISTRATION.md): independent check of Fable's TS delta=2 axis theorem with the Bridge's own TS2/Kerr metrics."""
import sys, os, json, math, cmath, itertools
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
V11 = os.path.join(HERE, '../../V11_chaos_reproduction/code'); sys.path.insert(0, V11)
_cwd = os.getcwd(); os.chdir(V11); import v11_chaos as V; os.chdir(_cwd)
X, Y = V.X, V.Y; E, mu2 = sp.symbols('E mu2', positive=True)
OUT = {}

def metric(case):
    os.chdir(V11)
    try: return V.get_metric(case)
    finally: os.chdir(_cwd)

def axial_r(case):
    """theta-linearised normal form r(x) of H = 1/2(g^xx px^2 + g^thth pth^2 + g^tt E^2), L = 0, y = cos(theta)."""
    g = metric(case)
    det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    gtt = sp.cancel(sp.together(g['g_phiphi']/det))
    a = sp.cancel(1/g['g_xx']); b = sp.cancel(1/(g['g_yy']*(1 - Y**2)))
    at1 = lambda e: sp.cancel(e.subs(Y, 1))
    a0, b0, W0 = at1(a), at1(b), at1(gtt*E**2)
    ay, Wy = at1(sp.diff(a, Y)), at1(sp.diff(gtt, Y)*E**2)
    px2 = (-mu2 - W0)/a0
    A = b0; B = -sp.Rational(1, 2)*(ay*px2 + Wy)          # theta'' - (A'/A)theta' + A B theta = 0 (affine)
    X2 = a0*(-mu2 - W0)
    a1 = sp.diff(X2, X)/(2*X2) - sp.diff(A, X)/A
    q = A*B/X2
    r = a1**2/4 + sp.diff(a1, X)/2 - q
    f0 = sp.factor(-g['g_TT'].subs(Y, 1))
    return r, f0

def T1(case):
    r, f0 = axial_r(case)
    P = E**2 - mu2*f0
    target = -sp.Rational(3, 16)*(sp.diff(P, X)/P)**2
    d = sp.cancel(sp.together(r - target))
    return d == 0, f0

# ------------------------------------------------------------------ monodromy (float) of y'' = r y, r = -(3/16)(P'/P)^2
def make_r(f0, Ev, m2):
    P = Ev**2 - m2*f0
    L = sp.lambdify(X, sp.cancel(sp.diff(P, X)/P), 'numpy')
    return lambda x: -(3/16)*complex(L(x))**2

def transport(rf, path, rtol):
    """Fundamental matrix along a piecewise path given as list of (z(t), dz(t), t0, t1)."""
    Mt = np.eye(2, dtype=complex)
    for z, dz, t0, t1 in path:
        def rhs(t, Yv):
            x = z(t); d = dz(t); return [d*Yv[1], d*rf(x)*Yv[0]]
        cols = []
        for k in range(2):
            sol = solve_ivp(rhs, (t0, t1), list(Mt[:, k]), method='DOP853', rtol=rtol, atol=rtol*1e-8, t_eval=[])  # t_eval=[]: no dense history (09:57 leak)
            cols.append(sol.y[:, -1])
        Mt = np.array(cols).T
    return Mt

def lollipop(base, c, rho):
    d = c - base; u = d/abs(d); s = c - rho*u          # stem end on the circle, facing the base
    th0 = cmath.phase(s - c)
    seg1 = (lambda t: base + t*(s - base), lambda t: (s - base), 0.0, 1.0)
    circ = (lambda t: c + rho*cmath.exp(1j*(th0 + t)), lambda t: 1j*rho*cmath.exp(1j*(th0 + t)), 0.0, 2*math.pi)
    seg2 = (lambda t: s + t*(base - s), lambda t: (base - s), 0.0, 1.0)
    return [seg1, circ, seg2]

def singular_points(f0, Ev, m2):
    n, d = sp.fraction(sp.together(Ev**2 - m2*f0))
    zs = [complex(z) for z in sp.Poly(n, X).nroots(n=30)]; ps = [complex(z) for z in sp.Poly(d, X).nroots(n=30)]
    return zs, ps, sp.degree(n, X), sp.degree(d, X)

def monodromies(f0, Ev, m2, rtol, base=complex(0.37, 9.1)):
    rf = make_r(f0, Ev, m2); zs, ps, _, _ = singular_points(f0, Ev, m2)
    pts = []
    for z in zs + ps:
        if not any(abs(z - w) < 1e-9 for w in pts): pts.append(z)
    out = []
    for c in pts:
        dmin = min(abs(c - w) for w in pts if w is not c)
        M = transport(rf, lollipop(base, c, 0.3*dmin), rtol)
        out.append((c, M))
    return out

def comm_tr(G, H):
    return np.trace(G @ H @ np.linalg.inv(G) @ np.linalg.inv(H))

if __name__ == '__main__':
    # T1
    for case in ('ts45', 'ts35', 'kerr45'):
        ok, f0 = T1(case); OUT[f'T1_{case}'] = dict(identity_zero=bool(ok), f0=str(f0)); print('T1', case, ok, f0, flush=True)
    f0ts = sp.factor(-metric('ts45')['g_TT'].subs(Y, 1)); f0k = sp.factor(-metric('kerr45')['g_TT'].subs(Y, 1))
    f0zv = ((X - 1)/(X + 1))**2
    # T2
    rows = {'T-a': sp.Rational(8, 15), 'T-b': 2, 'T-c': 1, 'T-d': sp.Rational(8, 3), 'irr': sp.sqrt(2)}
    for name, lam in rows.items():
        P = sp.together(1 - f0ts/lam)                                    # E^2 = lam, mu^2 = 1, scaled by 1/lam
        n, d = sp.fraction(P)
        zr = sp.roots(sp.Poly(n, X)); pr = sp.roots(sp.Poly(d, X))
        mult_z = sorted(zr.values()); mult_p = sorted(pr.values()); deg_n, deg_d = sp.degree(n, X), sp.degree(d, X)
        at_inf = deg_d - deg_n                                         # order of zero (+) or pole (-) of P at infinity
        OUT[f'T2_{name}'] = dict(zero_mult=mult_z, pole_mult=mult_p, deg_num=deg_n, deg_den=deg_d, inf_order=at_inf)
        print('T2', name, 'zeros', mult_z, 'poles', mult_p, 'deg', deg_n, deg_d, 'inf', at_inf, flush=True)
    # T4f + controls
    for label, f0, lamrows in (('TS', f0ts, ['T-a', 'T-d']), ('Kerr', f0k, ['T-a']), ('ZV', f0zv, ['T-a'])):
        for rn in lamrows:
            lam = float(rows[rn]); res = {}
            for rtol in (1e-12, 1e-13):
                ms = monodromies(f0, math.sqrt(lam), 1.0, rtol)
                res[rtol] = ms
            ms = res[1e-12]; ms2 = res[1e-13]
            singles = [(c, np.trace(M)) for c, M in ms]
            pairs = [ms[i][1] @ ms[i + 1][1] for i in range(len(ms) - 1)]
            comms = [comm_tr(G, H) for G, H in itertools.combinations(pairs, 2)]
            rec = dict(points=[[c.real, c.imag] for c, _ in ms],
                       single_tr=[[t.real, t.imag] for _, t in singles],
                       single_tr_rtolagree=max(abs(np.trace(a[1]) - np.trace(b[1])) for a, b in zip(ms, ms2)),
                       pair_tr=[[np.trace(G).real, np.trace(G).imag] for G in pairs],
                       comm_minus2=[abs(c - 2) for c in comms])
            OUT[f'T4f_{label}_{rn}'] = rec
            print(label, rn, 'single |tr|', ['%.2e' % abs(t) if abs(t) < 1 else '%.6f%+.6fj' % (t.real, t.imag) for _, t in singles],
                  '| max |tr[G,H]-2| = %.3e' % (max(rec['comm_minus2']) if comms else 0), 'min = %.3e' % (min(rec['comm_minus2']) if comms else 0), flush=True)
    json.dump(OUT, open(os.path.join(HERE, '../results/v22.json'), 'w'), indent=1, default=str)
