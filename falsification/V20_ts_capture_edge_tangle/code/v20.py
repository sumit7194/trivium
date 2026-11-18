"""V20 (PREREGISTRATION.md): blind replication of ansatz §154. Bridge pipeline (V11 compact field, exact Jacobian,
scipy DOP853 + variational equations, symmetric fixed-point scan, both W^u branches, theta and Lazutkin Omega).
Usage: python v20.py <case ts45|kerr45|ts35> <E> <L> <rtol> <s0> <x_lo> <x_hi> <x_target>   -> JSON on stdout."""
import sys, os, json, math, time
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
V11 = os.path.join(HERE, '../../V11_chaos_reproduction/code')
sys.path.insert(0, V11)
_cwd = os.getcwd(); os.chdir(V11)
import v11_chaos as V
os.chdir(_cwd)
XPLUNGE = 1.5

def field(case, E, L):
    os.chdir(V11)
    try:
        (FJ, _), _, fW, fGyy, fH = V.build(case, sp.nsimplify(E, rational=True), sp.nsimplify(L, rational=True, tolerance=1e-17))
    finally:
        os.chdir(_cwd)
    return FJ, fW, fH

def symmetry_exact(case):
    """B0: every metric component even in y (exact)."""
    os.chdir(V11)
    try: g = V.get_metric(case)
    finally: os.chdir(_cwd)
    return all(sp.simplify(v - v.subs(V.Y, -V.Y)) == 0 for v in g.values())

def make_rhs(FJ):
    def rhs(t, s):
        F, J = FJ(s[0], s[1], s[2], s[3]); J = np.array(J); M = s[4:].reshape(4, 4)
        return np.concatenate([np.array(F), (J @ M).ravel()])
    return rhs

def py_from_H(fH, x, y, px):
    h0 = fH(x, y, px, 0.0); h1 = fH(x, y, px, 1.0) - h0
    v = (-0.5 - h0)/h1
    return math.sqrt(v) if v > 0 else float('nan')

def P(FJ, fH, z, rtol, tmax=4000.0):
    """Section y = 0 upward, first return. Returns (image, 2x2 DP on the section, time) or Nones (P.last says why)."""
    x, px = z; py = py_from_H(fH, x, 0.0, px)
    if not np.isfinite(py): P.last = 'forbidden'; return None, None, None
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
    gH = np.array([-Fi[2], -Fi[3], Fi[0], Fi[1]])
    D = np.zeros((2, 2))
    for k, (dx, dpx) in enumerate(((1.0, 0.0), (0.0, 1.0))):
        w = M @ np.array([dx, 0.0, dpx, -(gH[0]*dx + gH[2]*dpx)/gH[3]])
        w = w - F*(w[1]/F[1])
        D[:, k] = [w[0], w[2]]
    return np.array([s[0], s[2]]), D, sol.t_events[0][0]

def scan_fixed_points(FJ, fH, rtol, xlo, xhi, n):
    """All symmetric fixed points on p_x = 0 in [xlo, xhi]: sign changes of g(x0) = x(P(x0,0)) - x0 with BOTH ends
    returning (no plunge/escape surrogate), refined by brentq."""
    def g(x0):
        q = P(FJ, fH, np.array([x0, 0.0]), rtol)[0]
        return None if q is None else q[0] - x0
    xs = np.linspace(xlo, xhi, n); gs = [g(x) for x in xs]
    out = []
    for i in range(n - 1):
        if gs[i] is None or gs[i+1] is None or gs[i]*gs[i+1] >= 0: continue
        try: x0 = brentq(lambda x: g(x), xs[i], xs[i+1], xtol=1e-14)
        except Exception: continue
        Pz, D, T = P(FJ, fH, np.array([x0, 0.0]), rtol)
        if Pz is None: continue
        out.append(dict(x=x0, trace=float(np.trace(D)), det=float(np.linalg.det(D)), period=T))
    return out, [(float(a), None if b is None else float(b)) for a, b in zip(xs, gs)]

def polish(FJ, fH, x0, rtol, it=30):
    z = np.array([x0, 0.0])
    for _ in range(it):
        Pz, D, T = P(FJ, fH, z, rtol)
        r = Pz - z
        if np.max(np.abs(r)) < 1e-13: break
        dz = np.linalg.solve(D - np.eye(2), r)
        if np.max(np.abs(dz)) > 1e-4: dz *= 1e-4/np.max(np.abs(dz))
        z = z - dz
    Pz, D, T = P(FJ, fH, z, rtol)
    return z, D, T, float(np.max(np.abs(Pz - z)))

def reversor_check(FJ, fH, z, rtol):
    Sm = np.diag([1.0, -1.0]); worst = 0.0; nv = 0
    for d in ((1e-4, 0.0), (0.0, 1e-4), (2e-4, -1e-4), (-1e-4, 2e-4), (5e-5, 5e-5)):
        q = z + np.array(d); q1 = P(FJ, fH, q, rtol)[0]
        if q1 is None: continue
        q2 = P(FJ, fH, Sm @ q1, rtol)[0]
        if q2 is None: continue
        nv += 1; worst = max(worst, float(np.max(np.abs(Sm @ q2 - q))))
    return worst if nv == 5 else float('nan')

def homoclinic(FJ, fH, z, eu, lam, rtol, s0, sign, nmax=40, ngrid=160):
    """Grow branch sign*eu of W^u from [s0, s0*lam]; first p_x sign change (both points returning) is the primary
    symmetric homoclinic point of that branch. Returns dict or None."""
    ss = np.geomspace(s0, s0*lam, ngrid)
    pts = [z + sign*s*eu for s in ss]
    for n in range(1, nmax + 1):
        pts = [None if q is None else P(FJ, fH, q, rtol)[0] for q in pts]
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i+1]
            if a is None or b is None: continue
            if abs(a[0] - z[0]) < 1e-3 and abs(b[0] - z[0]) < 1e-3: continue   # amendment 1: fixed distance (was 10*s0*lam^n, a bug)
            if a[1]*b[1] < 0:
                def fpx(s):
                    q = z + sign*s*eu
                    for _ in range(n): q = P(FJ, fH, q, rtol)[0]
                    return q[1]
                sh = brentq(fpx, ss[i], ss[i+1], xtol=s0*1e-12)
                q = z + sign*sh*eu; Dn = np.eye(2)
                for _ in range(n):
                    q2, D, _ = P(FJ, fH, q, rtol); Dn = D @ Dn; q = q2
                tu = (Dn @ (sign*eu))*lam**(-n)
                ta, tb = tu
                return dict(n=n, s_h=float(sh), z_h=q.tolist(), t_u=tu.tolist(),
                            theta=float(2*math.atan(abs(ta)/abs(tb))), Omega=float((ta*tb)/(eu[0]*eu[1])))
        if all(q is None for q in pts): return dict(n=None, fail='all seeds lost at iterate %d' % n)
    return None

def run(case, E, L, rtol, s0, xlo, xhi, xtarget, nscan=241):
    t0 = time.time()
    FJ, fW, fH = field(case, E, L)
    fps, grid = scan_fixed_points(FJ, fH, rtol, xlo, xhi, nscan)
    hyp = [f for f in fps if abs(f['trace']) > 2 + 1e-6]
    out = dict(case=case, E=E, L=L, rtol=rtol, s0=s0, scan=[xlo, xhi, nscan], fixed_points=fps)
    if not hyp:
        out.update(verdict_gate='no hyperbolic symmetric fixed point', seconds=round(time.time() - t0, 1)); return out
    tgt = min(hyp, key=lambda f: abs(f['x'] - xtarget))
    z, D, T, clos = polish(FJ, fH, tgt['x'], rtol)
    ev, Vv = np.linalg.eig(D); k = int(np.argmax(np.abs(ev))); lam = float(np.real(ev[k]))
    eu = np.real(Vv[:, k]); eu = eu/np.linalg.norm(eu)
    out.update(fixed_point=z.tolist(), closure=clos, period=T, trace=float(np.trace(D)), det=float(np.linalg.det(D)),
               lambda_u=lam, e_u=eu.tolist(), R0=reversor_check(FJ, fH, z, rtol))
    br = {}
    for sign in (1.0, -1.0):
        q = P(FJ, fH, z + sign*s0*lam**3*eu, rtol)[0]
        label = ('outward' if q[0] > z[0] else 'inward') if q is not None else 'lost'
        br[label if label not in br else label + '2'] = dict(sign=sign, **(homoclinic(FJ, fH, z, eu, lam, rtol, s0, sign) or {}))
    out['branches'] = br; out['seconds'] = round(time.time() - t0, 1)
    return out

def kerr_spherical(p, q, E, L):
    """B3: Kerr unstable spherical orbits at (E, L): double roots of R(r) with Q free, BL, m = 1/p, a = q/p, mu = 1.
    Returns the list of (r, Q) for BOTH signs of a*L (the chart sense is decided by matching)."""
    import mpmath as mp
    mp.mp.dps = 40
    m, a = mp.mpf(1)/p, mp.mpf(q)/p; E = mp.mpf(E); res = []
    for La in (L, -L):
        La = mp.mpf(La)
        def R(r, Q): D = r*r - 2*m*r + a*a; return (E*(r*r + a*a) - a*La)**2 - D*(r*r + (La - a*E)**2 + Q)
        def Qof(r):   # R = 0 -> Q
            D = r*r - 2*m*r + a*a; return ((E*(r*r + a*a) - a*La)**2)/D - r*r - (La - a*E)**2
        f = lambda r: mp.diff(lambda rr: R(rr, Qof(r)), r)
        rs = mp.linspace(m + mp.sqrt(m*m - a*a) + mp.mpf('0.01'), 40*m, 4000); vals = [f(r) for r in rs]
        for i in range(len(rs) - 1):
            if vals[i]*vals[i+1] < 0:
                r0 = mp.findroot(f, (rs[i], rs[i+1]), solver='anderson'); Q0 = Qof(r0)
                d2 = mp.diff(lambda rr: R(rr, Q0), r0, 2)
                res.append(dict(sense='L*a>0' if La*a > 0 else 'L*a<0', r=float(r0), x=float(r0 - m), Q=float(Q0), R2=float(d2)))
    return res

if __name__ == '__main__':
    a = sys.argv
    r = run(a[1], float(sp.Rational(a[2])), float(sp.Rational(a[3])), float(a[4]), float(a[5]), float(a[6]), float(a[7]), float(a[8]))
    print(json.dumps(r))
