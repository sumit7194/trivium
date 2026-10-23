"""V16: independent replication of the TS δ=2 separatrix splitting (PREREGISTRATION.md). Bridge's own pipeline:
V11 compact field (exact Jacobian), DOP853 with the variational equations, Newton fixed point, manifold tracking,
primary symmetric homoclinic point on p_x = 0, angle θ and Lazutkin invariant Ω.
Usage: python v16_split.py <case: ts35|kerr35> <eps> <rtol> <s0>"""
import sys, os, json, math, time
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
V11 = os.path.join(HERE, '../../V11_chaos_reproduction/code')
sys.path.insert(0, V11)
_cwd = os.getcwd(); os.chdir(V11)                       # V11/V10 loaders use relative paths
import v11_chaos as V
os.chdir(_cwd)
E = 0.94

def field(case, L):
    os.chdir(V11)
    try:
        (FJ, _), _, fW, fGyy, fH = V.build(case, sp.Rational(47, 50), sp.nsimplify(L, rational=True, tolerance=1e-17))
    finally:
        os.chdir(_cwd)
    return FJ, fW, fH

def Wx(fW, x, h=1e-6):
    return (fW(x + h, 0.0) - fW(x - h, 0.0))/(2*h)

def saddle(fW, xlo, xhi):
    """Equatorial barrier top: maximum of W along y = 0 (saddle-centre of the 2-D potential)."""
    xs = np.linspace(xlo, xhi, 4000); w = np.array([fW(x, 0.0) for x in xs])
    i = int(np.nanargmax(w)); a, b = xs[max(i - 2, 0)], xs[min(i + 2, len(xs) - 1)]
    return brentq(lambda x: Wx(fW, x), a, b)

def lsep(case, xlo, xhi, Lguess):
    """|L| at which the equatorial saddle sits exactly on the shell, i.e. W(x_s) = -1 (H = W/2 = -1/2 at rest)."""
    def g(Labs):
        _, fW, _ = field(case, -Labs); xs = saddle(fW, xlo, xhi); return fW(xs, 0.0) + 1.0
    return brentq(g, Lguess*0.8, Lguess*1.25, xtol=1e-12)

def make_rhs(FJ):
    def rhs(t, s):
        F, J = FJ(s[0], s[1], s[2], s[3]); J = np.array(J); M = s[4:].reshape(4, 4)
        return np.concatenate([np.array(F), (J @ M).ravel()])
    return rhs

def py_from_H(fH, x, y, px):
    """p_y > 0 on the shell H = -1/2, from H = 1/2 (A px^2 + B py^2 + W)."""
    h0 = fH(x, y, px, 0.0); h1 = fH(x, y, px, 1.0) - h0     # B/2
    v = (-0.5 - h0)/h1
    return math.sqrt(v) if v > 0 else float('nan')

XPLUNGE = float(os.environ.get('V16_XPLUNGE', '1.25'))
def P(FJ, fH, z, rtol, tmax=float(os.environ.get("V16_TMAX", "4000"))):
    """Section map Σ: y = 0, p_y > 0 (upward), first return. Returns (image (x, px), 2x2 DP on Σ ∩ shell, time)."""
    x, px = z; py = py_from_H(fH, x, 0.0, px)
    if not np.isfinite(py): return None, None, None
    s0 = np.concatenate([[x, 0.0, px, py], np.eye(4).ravel()])
    def ev(t, s): return s[1] if t > 1e-6 else 1.0
    ev.direction = 1; ev.terminal = True
    def plunge(t, s): return s[0] - XPLUNGE
    plunge.terminal = True
    def escape(t, s): return 1000.0 - s[0]
    escape.terminal = True
    sol = solve_ivp(make_rhs(FJ), (0, tmax), s0, method='DOP853', rtol=rtol, atol=rtol*1e-3, events=[ev, plunge, escape], t_eval=[])
    if sol.t_events[0].size == 0:
        P.last = 'plunge' if sol.t_events[1].size else ('escape' if sol.t_events[2].size else 'tmax')
        return None, None, None
    P.last = 'ok'
    s = sol.y_events[0][0]; F, _ = FJ(s[0], s[1], s[2], s[3]); F = np.array(F); M = s[4:].reshape(4, 4)
    Fi, _ = FJ(x, 0.0, px, py); Fi = np.array(Fi)
    gH = np.array([-Fi[2], -Fi[3], Fi[0], Fi[1]])            # (dH/dx, dH/dy, dH/dpx, dH/dpy)
    D = np.zeros((2, 2))
    for k, (dx, dpx) in enumerate(((1.0, 0.0), (0.0, 1.0))):
        w = M @ np.array([dx, 0.0, dpx, -(gH[0]*dx + gH[2]*dpx)/gH[3]])   # start on the shell
        w = w - F*(w[1]/F[1])                                    # remove the time shift: land on y = 0
        D[:, k] = [w[0], w[2]]
    return np.array([s[0], s[2]]), D, sol.t_events[0][0]

# ---------------------------------------------------------------------------------------------------------------
XLO = float(os.environ.get('V16_XLO', '1.3'))
def wmax(fW, xlo=None, xhi=30.0, n=2000):
    xlo = XLO if xlo is None else xlo
    """Outer barrier: the local maximum of W(x, 0) in [xlo, xhi] (None if absent)."""
    xs = np.linspace(xlo, xhi, n); w = np.array([fW(x, 0.0) for x in xs]); d = np.diff(w)
    idx = [i for i in range(1, len(d)) if d[i-1] > 0 and d[i] <= 0]
    if not idx: return None
    i = idx[-1]
    xs_ = brentq(lambda x: Wx(fW, x), xs[i-1], xs[i+1], xtol=1e-14)
    return xs_, fW(xs_, 0.0)

_GCACHE = {}
def wfun_L(case):
    """W(x, 0; L) for any L from the three inverse-metric pieces, built ONCE (W = Gtt E^2 - 2 Gtp E L + Gpp L^2)."""
    if case not in _GCACHE:
        os.chdir(V11)
        try:
            g = V.get_metric(case)
        finally:
            os.chdir(_cwd)
        X, Y = V.X, V.Y
        det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
        parts = [sp.lambdify(X, (e).subs(Y, 0), 'math') for e in (g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det)]
        _GCACHE[case] = parts
    Gtt, Gtp, Gpp = _GCACHE[case]
    return lambda L: (lambda x, y=0.0: Gtt(x)*E*E - 2*Gtp(x)*E*L + Gpp(x)*L*L)

def find_lsep(case, Llo, Lhi):
    WL = wfun_L(case)
    def g(Labs):
        m = wmax(WL(-Labs))
        return (m[1] + 1.0) if m else -1.0                    # no barrier (merged/absent at small |L|) -> open
    return brentq(g, Llo, Lhi, xtol=1e-13)

def newton_fp(FJ, fH, z0, rtol, it=30, w=float(os.environ.get("V16_FPW", "0.08"))):
    """Symmetric Lyapunov orbit: on Fix(S) = {p_x = 0}, find x0 with x(P(x0, 0)) = x0 by bracketing (falling in = -,
    escaping/falling out = +), then polish with a guarded 2-D Newton."""
    def g(x0):
        q = P(FJ, fH, np.array([x0, 0.0]), rtol)[0]
        if q is None: return -1.0 if P.last == 'plunge' else 1.0
        return q[0] - x0
    xs = np.linspace(z0[0] - w, z0[0] + w, 161); gs = [g(x) for x in xs]
    br = [(xs[i], xs[i+1]) for i in range(len(xs) - 1) if gs[i]*gs[i+1] < 0]
    if not br: raise RuntimeError('no symmetric fixed point bracket near the saddle')
    a, b = min(br, key=lambda ab: abs(0.5*(ab[0] + ab[1]) - z0[0]))
    x0 = brentq(g, a, b, xtol=1e-14)
    z = np.array([x0, 0.0])
    for _ in range(it):
        Pz, D, T = P(FJ, fH, z, rtol)
        if Pz is None: break
        r = Pz - z
        if np.max(np.abs(r)) < 1e-13: break
        dz = np.linalg.solve(D - np.eye(2), r)
        if np.max(np.abs(dz)) > 1e-4: dz *= 1e-4/np.max(np.abs(dz))
        z = z - dz
    Pz, D, T = P(FJ, fH, z, rtol)
    return z, D, T, float(np.max(np.abs(Pz - z)))

def homoclinic(FJ, fH, z, eu, lam, rtol, s0, nmax=40, ngrid=160, sign=1.0):
    """Grow W^u (branch sign*eu) from the fundamental segment [s0, s0*lam]; the first p_x sign change at x > x* is
    the primary symmetric homoclinic point. Returns n, s_h, z_h, t_u (= lam^-n DP^n e_u), or None."""
    ss = np.geomspace(s0, s0*lam, ngrid)
    pts = [z + sign*s*eu for s in ss]
    for n in range(1, nmax + 1):
        pts = [None if q is None else P(FJ, fH, q, rtol)[0] for q in pts]
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i+1]
            if a is None or b is None: continue
            if a[0] > z[0] and b[0] > z[0] and a[1]*b[1] < 0:
                def fpx(s):
                    q = z + sign*s*eu
                    for _ in range(n): q = P(FJ, fH, q, rtol)[0]
                    return q[1]
                sh = brentq(fpx, ss[i], ss[i+1], xtol=s0*1e-12)
                q = z + sign*sh*eu; Dn = np.eye(2)
                for _ in range(n):
                    q2, D, _ = P(FJ, fH, q, rtol); Dn = D @ Dn; q = q2
                tu = (Dn @ (sign*eu))*lam**(-n)
                return n, sh, q, tu
    return None

def reversor_check(FJ, fH, z, rtol):
    Sm = np.diag([1.0, -1.0]); worst = 0.0
    nvalid = 0
    for d in ((1e-4, 0.0), (0.0, 1e-4), (2e-4, -1e-4), (-1e-4, 2e-4), (5e-5, 5e-5)):
        q = z + np.array(d); q1 = P(FJ, fH, q, rtol)[0]
        if q1 is None: continue
        q2 = P(FJ, fH, Sm @ q1, rtol)[0]
        if q2 is None: continue
        nvalid += 1; worst = max(worst, float(np.max(np.abs(Sm @ q2 - q))))
    return worst if nvalid >= 5 else float('nan')

def run(case, eps, rtol, s0, Lbracket):
    t0 = time.time()
    ls = find_lsep(case, *Lbracket); print('l_sep', ls, round(time.time()-t0,1), file=sys.stderr, flush=True)
    L = -ls*(1 + eps)
    FJ, fW, fH = field(case, L)
    xs, Ws = wmax(fW)
    print('field built', round(time.time()-t0,1), file=sys.stderr, flush=True)
    z, D, T, clos = newton_fp(FJ, fH, (xs, 0.0), rtol)
    print('fixed point', z, clos, T, round(time.time()-t0,1), file=sys.stderr, flush=True)
    ev, V = np.linalg.eig(D); k = int(np.argmax(np.abs(ev))); lam = float(np.real(ev[k]))
    eu = np.real(V[:, k]); eu = eu/np.linalg.norm(eu)
    R0 = reversor_check(FJ, fH, z, rtol)
    best = None
    for sign in (1.0, -1.0):                                   # the pocket branch: the one whose first excursion goes to x > x*
        q = P(FJ, fH, z + sign*s0*lam**3*eu, rtol)[0]
        if q is not None and q[0] > z[0]: best = sign; break
    h = homoclinic(FJ, fH, z, eu, lam, rtol, s0, sign=best if best else 1.0)
    out = dict(case=case, eps=eps, rtol=rtol, s0=s0, l_sep=ls, L=L, x_saddle=xs, W_saddle=Ws, h=-0.5 - 0.5*Ws,
               fixed_point=z.tolist(), closure=clos, period=T, lambda_u=lam, e_u=eu.tolist(), R0=R0,
               branch_sign=best, seconds=None)
    if h:
        n, sh, zh, tu = h
        a, b = tu
        out.update(n=n, s_h=sh, z_h=zh.tolist(), t_u=tu.tolist(),
                   theta=float(2*math.atan(abs(a)/abs(b))), Omega=float((a*b)/(eu[0]*eu[1])))
    out['seconds'] = round(time.time() - t0, 1)
    return out

if __name__ == '__main__':
    case, eps, rtol, s0, Llo, Lhi = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
    r = run(case, eps, rtol, s0, (Llo, Lhi))
    print(json.dumps(r))
