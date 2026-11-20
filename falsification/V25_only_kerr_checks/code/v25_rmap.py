"""V25 addendum A machinery (Bridge code): system R along a z-loop around an axis puncture, X+- basis, cubic return map.
U(r2, z) supplied by the caller (R-full: exact metric; R-trunc: own series through rho^4)."""
import math, cmath, numpy as np, sympy as sp
from scipy.integrate import solve_ivp

# ---------- own U through rho^4 from (f0, (c0'')^2), via the own static-Weyl series of V25 P1 + confirmed twist terms
def trunc_U_series():
    z = sp.symbols('z'); t = sp.symbols('t'); E, mu = sp.symbols('E mu'); C2 = sp.symbols('C2')
    f0 = sp.Function('f0')(z)
    a0 = sp.log(f0)/2; a1 = -sp.diff(a0, z, 2)/4; a2 = sp.diff(a0, z, 4)/64
    g1 = -sp.diff(a0, z)**2/2; g2 = (4*a1**2 - 2*sp.diff(a0, z)*sp.diff(a1, z))/4
    psi = a0 + a1*t + a2*t**2; gam = g1*t + g2*t**2
    F1 = sp.series(sp.exp(2*psi - 2*gam), t, 0, 3).removeO() - C2/(64*f0)*t**2
    F2 = sp.series(sp.exp(-2*psi), t, 0, 3).removeO() - C2/(64*f0**3)*t**2
    U = sp.series((E**2*F2 - mu**2)/(2*F1), t, 0, 3).removeO()
    return z, t, E, mu, C2, f0, [sp.simplify(U.coeff(t, n)) for n in range(3)]
_ZS = trunc_U_series()

def make_trunc(f0_expr, c2sq_expr, zsym, EE, MU=1):
    """f0_expr, c2sq_expr: sympy expressions in zsym. Returns Ufun(r2, z), dUfun(r2, z) (d/d r2), numpy complex."""
    z, t, E, mu, C2, f0, Uc = _ZS
    sub = {sp.Derivative(f0, (z, n)): sp.diff(f0_expr, zsym, n).subs(zsym, z) for n in range(4, 0, -1)}
    cs = []
    for c in Uc:
        e = c.subs(sub).subs(f0, f0_expr.subs(zsym, z)).subs({C2: c2sq_expr.subs(zsym, z), E: EE, mu: MU})
        cs.append(sp.lambdify(z, e, 'numpy'))
    U0, U2, U4 = cs
    return (lambda r2, zz: U0(zz) + U2(zz)*r2 + U4(zz)*r2*r2), (lambda r2, zz: U2(zz) + 2*U4(zz)*r2), U0, U2

class Axis:
    """two-simple-pole axis data f0 = 1 - m1/(z-z1) - m2/(z-z2) (for the X+- basis and kappa)."""
    def __init__(s, z1, z2, m1, m2, E, mu=1):
        s.z1, s.z2, s.m1, s.m2, s.E, s.mu = z1, z2, m1, m2, E, mu
        s.Dc = np.array([1, -(z1 + z2), z1*z2], complex)                       # high -> low
        s.Dlc = np.array([1, -(z1 + z2) - m1 - m2, z1*z2 + m1*z2 + m2*z1], complex)
        s.Nc = E**2*s.Dc - mu**2*s.Dlc; s.Y2c = np.polymul(s.Nc, s.Dc); s.dY2c = np.polyder(s.Y2c)
        dl = z1 - z2; s.kappa = cmath.sqrt(dl*((E**2 - mu**2)*dl - mu**2*(m1 - m2))/4)
    Delta = lambda s, z: np.polyval(s.Dlc, z)
    dDelta = lambda s, z: np.polyval(np.polyder(s.Dlc), z)
    Y2 = lambda s, z: np.polyval(s.Y2c, z)

def loop_run(ax, Ufun, dUfun, U0fun, zc, r, rho0, p0, branch_y=1, turns=2, rtol=1e-13, atol=1e-16, th_end=None):
    """integrate system R once around the loop z = zc + r e^{i th}, th in [0, 2 pi turns]; returns end state."""
    zs = zc + r
    y0 = branch_y*cmath.sqrt(ax.Y2(zs))
    def rhs(th, Z):
        rho, p, y, u = Z; z = zc + r*np.exp(1j*th); dz = 1j*r*np.exp(1j*th)
        Dl = ax.Delta(z); q0 = y/Dl; r2 = rho*rho
        pz = q0*np.sqrt(1 + (2*(Ufun(r2, z) - U0fun(z)) - p*p)/(q0*q0))
        return [dz*p/pz, dz*2*rho*dUfun(r2, z)/pz, dz*np.polyval(ax.dY2c, z)/(2*y), dz/y]
    T = 2*math.pi*turns if th_end is None else th_end
    sol = solve_ivp(rhs, (0, T), np.array([rho0, p0, y0, 0], complex), method='DOP853', rtol=rtol, atol=atol, t_eval=[T])
    return sol.y[:, -1], y0, zs

def u_offset(ax, zs, y0):
    """u(zs) - u_P, P = z1 branch point: z = z1 + s^2 d, du = 2 d ds / G(s), G^2 = d N(z)(z - z2), G(1) = y0."""
    d = zs - ax.z1
    def rhs(s_, Z):
        G, uu = Z; zz = ax.z1 + s_*s_*d
        G2p = d*(np.polyval(np.polyder(ax.Nc), zz)*(zz - ax.z2) + np.polyval(ax.Nc, zz))*2*s_*d
        return [G2p/(2*G), 2*d/G]
    sol = solve_ivp(rhs, (1, 0), np.array([y0, 0], complex), method='DOP853', rtol=1e-13, atol=1e-16, t_eval=[0])
    return -sol.y[1, -1]           # integral from 0 to 1 = -(integral from 1 to 0)

def basis(ax, z, y, uu):
    k = ax.kappa; sD = cmath.sqrt(ax.Delta(z)); eta = ax.dDelta(z)*y/(2*ax.Delta(z))
    Xp = cmath.exp(k*uu)*np.array([sD, (eta + k)/sD]); Xm = cmath.exp(-k*uu)*np.array([sD, (eta - k)/sD])
    return Xp, Xm

def ve1_selfcheck(ax, Ufun, dUfun, U0fun, U2fun, zc, r, du0, thetas=(0, 0.8, 1.6, 2.4, 3.2)):
    """A1: X+- satisfy VE_1 (d/ds = (y/Delta) d/dz) at points on the loop; y, u from the rho = p = 0 flow."""
    worst = 0.0
    for th in thetas:
        th = th*math.pi
        if th == 0: zz = zc + r; yy = cmath.sqrt(ax.Y2(zz)); uu = du0
        else:
            Z, _, _ = loop_run(ax, Ufun, dUfun, U0fun, zc, r, 0j, 0j, th_end=th); zz = zc + r*cmath.exp(1j*th); yy = Z[2]; uu = du0 + Z[3]
        h = 1e-5*r; vals = []
        for sgn in (+1, -1):
            z2 = zz + sgn*h; y2 = cmath.sqrt(ax.Y2(z2)); y2 = y2 if abs(y2 - yy) < abs(y2 + yy) else -y2
            vals.append(basis(ax, z2, y2, uu + sgn*h*(1/yy + 1/y2)/2))
        X = basis(ax, zz, yy, uu)
        for idx in (0, 1):
            dX = (vals[0][idx] - vals[1][idx])/(2*h)*yy/ax.Delta(zz)
            worst = max(worst, abs(dX[0] - X[idx][1])/abs(X[idx][1]), abs(dX[1] - 2*U2fun(zz)*X[idx][0])/abs(2*U2fun(zz)*X[idx][0]))
    return worst

def return_map(ax, Ufun, dUfun, U0fun, zc, radii, eps_list=(0.02, 0.01, 0.005, 0.0025), starts=((1, 0),), U2fun=None):
    """cubic return-map coefficient A for each start, with floor diagnostics (amendment A1: two-level Richardson)."""
    res = {}
    for r in radii:
        zs = zc + r; y0 = cmath.sqrt(ax.Y2(zs)); du = u_offset(ax, zs, y0)
        Xp, Xm = basis(ax, zs, y0, du); B = np.column_stack([Xp, Xm]); Bi = np.linalg.inv(B)
        chk = ve1_selfcheck(ax, Ufun, dUfun, U0fun, U2fun, zc, r, du) if U2fun is not None else None
        for st in starts:
            c = np.array(st, complex); As = []
            e0 = 1e-7; Zend, _, _ = loop_run(ax, Ufun, dUfun, U0fun, zc, r, *(e0*(B @ c)))
            lin = float(np.max(np.abs(Bi @ Zend[:2]/e0 - c)))
            yret = abs(Zend[2] - y0)/abs(y0); uret = abs(Zend[3])
            for e in eps_list:
                Zend, _, _ = loop_run(ax, Ufun, dUfun, U0fun, zc, r, *(e*(B @ c)))
                As.append((Bi @ Zend[:2]/e - c)/e**2)
            R = [(4*As[i + 1] - As[i])/3 for i in range(len(As) - 1)]
            RR = [(16*R[i + 1] - R[i])/15 for i in range(len(R) - 1)]
            res[(r, st)] = dict(A=RR[-1], rich_diff=float(np.max(np.abs(RR[-1] - RR[-2]))), lin_dev=lin, y_return=yret, u_return=uret, ve1_check=chk,
                                A_level1=R[-1])
    out = {}
    for st in starts:
        rs = [res[(r, st)] for r in radii]
        rad_diff = float(np.max(np.abs(rs[0]['A'] - rs[-1]['A'])))
        floor = max([rad_diff] + [x['rich_diff'] for x in rs] + [x['lin_dev'] for x in rs])
        out[st] = dict(A=[complex(a) for a in rs[-1]['A']], floor=floor, rad_diff=rad_diff,
                       rich_diff=[x['rich_diff'] for x in rs], lin_dev=[x['lin_dev'] for x in rs],
                       y_return=[x['y_return'] for x in rs], u_return=[x['u_return'] for x in rs], ve1_check=[x['ve1_check'] for x in rs])
    return out
