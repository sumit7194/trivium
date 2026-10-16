"""V13 variational section map: DOP853 (as v13_orbit) on the 20-dim system (z, Phi), Phi' = Df(z) Phi, Phi(0) = I,
with exact second derivatives of the regularised field. Returns the n-th up-crossing of y = 0 and the 2x2 Jacobian
DP^n on (x, p_x), via the energy-constrained initial variations and the return-time correction:
  d p_y0 = -(H_x dx + H_px dp_x)/H_py ;  w = Phi V ;  dt = -w_y/ydot ;  DP = rows (x, p_x) of (w + f dt).
Replaces the finite-difference Jacobian in v13_upo (which lost area preservation, det-1 up to 0.26, on strongly
hyperbolic orbits)."""
import sys, os, math
import numpy as np, sympy as sp, numba
import scipy.integrate._ivp.dop853_coefficients as DC
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_field import build, W_reg, ginv_reg, x as X, y as Y
NS = DC.N_STAGES
A = np.ascontiguousarray(DC.A[:NS, :NS]); B = DC.B.copy(); E3 = DC.E3.copy(); E5 = DC.E5.copy(); D = DC.D.copy()
AX = np.ascontiguousarray(DC.A[NS + 1:])
ND = 20

def make_var(M, a_, beta, E, Lz):
    S = build(M, a_, beta); E, Lz = sp.nsimplify(E), sp.nsimplify(Lz)
    gxx, gyy = ginv_reg(S); W = W_reg(S, E, Lz)
    flat = []
    for f in (gxx, gyy, W):
        fx, fy = sp.diff(f, X), sp.diff(f, Y)
        flat += [f, fx, fy, sp.diff(fx, X), sp.diff(fx, Y), sp.diff(fy, Y)]
    pc = numba.njit(sp.lambdify([X, Y], flat, 'math', cse=True))

    @numba.njit
    def rhs(z, out):
        q = pc(z[0], z[1]); px, py = z[2], z[3]
        # q: gxx 0..5, gyy 6..11, W 12..17 ; each (f, fx, fy, fxx, fxy, fyy)
        out[0] = q[0]*px; out[1] = q[6]*py
        out[2] = -0.5*(q[1]*px*px + q[7]*py*py + q[13]); out[3] = -0.5*(q[2]*px*px + q[8]*py*py + q[14])
        J = np.empty((4, 4))
        J[0, 0] = q[1]*px; J[0, 1] = q[2]*px; J[0, 2] = q[0]; J[0, 3] = 0.0
        J[1, 0] = q[7]*py; J[1, 1] = q[8]*py; J[1, 2] = 0.0; J[1, 3] = q[6]
        J[2, 0] = -0.5*(q[3]*px*px + q[9]*py*py + q[15]); J[2, 1] = -0.5*(q[4]*px*px + q[10]*py*py + q[16])
        J[2, 2] = -q[1]*px; J[2, 3] = -q[7]*py
        J[3, 0] = -0.5*(q[4]*px*px + q[10]*py*py + q[16]); J[3, 1] = -0.5*(q[5]*px*px + q[11]*py*py + q[17])
        J[3, 2] = -q[2]*px; J[3, 3] = -q[8]*py
        for i in range(4):
            for j in range(4):
                acc = 0.0
                for k in range(4): acc += J[i, k]*z[4 + 4*k + j]
                out[4 + 4*i + j] = acc

    @numba.njit
    def dense_eval(F, y_old, s, out):
        for k in range(ND): out[k] = 0.0
        for i in range(7):
            f = F[6 - i]
            for k in range(ND): out[k] += f[k]
            fac = s if i % 2 == 0 else 1.0 - s
            for k in range(ND): out[k] *= fac
        for k in range(ND): out[k] += y_old[k]

    @numba.njit
    def root(F, y_old, comp, level, s_lo, s_hi):
        """Bisection (60 halvings) for z[comp](s) = level on [s_lo, s_hi] of the dense output."""
        tmp = np.empty(ND)
        dense_eval(F, y_old, s_lo, tmp); flo = tmp[comp] - level
        for _ in range(60):
            sm = 0.5*(s_lo + s_hi); dense_eval(F, y_old, sm, tmp); fm = tmp[comp] - level
            if (fm < 0) == (flo < 0): s_lo = sm; flo = fm
            else: s_hi = sm
        return 0.5*(s_lo + s_hi)

    @numba.njit
    def run(x0, px0, n, rtol, atol, max_steps):
        """Returns (ok, z at n-th return (20), f at return (20))."""
        q = pc(x0, 0.0); rest = -1.0 - q[12] - q[0]*px0*px0
        zr = np.zeros(ND); fr = np.zeros(ND)
        if not (rest > 0.0) or not (q[6] > 0.0): return False, zr, fr
        y = np.zeros(ND); y[0] = x0; y[2] = px0; y[3] = math.sqrt(rest/q[6])
        for i in range(4): y[4 + 5*i] = 1.0
        f = np.empty(ND); rhs(y, f)
        K = np.zeros((16, ND)); ynew = np.empty(ND); fnew = np.empty(ND); tmp = np.empty(ND); F = np.zeros((7, ND))
        h = 1e-3; t = 0.0; ncross = 0; steps = 0
        while steps < max_steps:
            rejected = False
            while True:
                hh = h
                K[0] = f
                for s in range(1, NS):
                    for k in range(ND):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*A[s, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(ND):
                    acc = 0.0
                    for j in range(NS): acc += K[j, k]*B[j]
                    ynew[k] = y[k] + hh*acc
                rhs(ynew, fnew); K[NS] = fnew
                e5 = 0.0; e3 = 0.0
                for k in range(ND):
                    sck = atol + max(abs(y[k]), abs(ynew[k]))*rtol
                    a5 = 0.0; a3 = 0.0
                    for j in range(NS + 1): a5 += K[j, k]*E5[j]; a3 += K[j, k]*E3[j]
                    e5 += (a5/sck)**2; e3 += (a3/sck)**2
                en = 0.0 if (e5 == 0.0 and e3 == 0.0) else hh*e5/math.sqrt((e5 + 0.01*e3)*ND)
                if not math.isfinite(en): en = 1e300
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return False, zr, fr
            steps += 1
            if y[1] < 0.0 and ynew[1] >= 0.0:
                ncross += 1
                if ncross == n:
                    for s in range(NS + 1, 16):
                        for k in range(ND):
                            acc = 0.0
                            for j in range(s): acc += K[j, k]*AX[s - NS - 1, j]
                            tmp[k] = y[k] + acc*hh
                        rhs(tmp, K[s])
                    for k in range(ND):
                        dy = ynew[k] - y[k]
                        F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                        for r in range(4):
                            acc = 0.0
                            for j in range(16): acc += D[r, j]*K[j, k]
                            F[3 + r, k] = hh*acc
                    su = root(F, y, 1, 0.0, 0.0, 1.0); dense_eval(F, y, su, zr); rhs(zr, fr)
                    return True, zr, fr
            t += hh
            for k in range(ND): y[k] = ynew[k]; f[k] = fnew[k]
        return False, zr, fr

    def section_jac(x0, px0, n, rtol=1e-13):
        ok, zr, fr = run(x0, px0, n, rtol, rtol*1e-3, 200_000_000)
        if not ok: return None, None
        q = pc(x0, 0.0); py0 = math.sqrt((-1.0 - q[12] - q[0]*px0*px0)/q[6])
        Hx = 0.5*(q[1]*px0*px0 + q[7]*py0*py0 + q[13]); Hpx = q[0]*px0; Hpy = q[6]*py0
        V = np.zeros((4, 2)); V[0, 0] = 1.0; V[3, 0] = -Hx/Hpy; V[2, 1] = 1.0; V[3, 1] = -Hpx/Hpy
        Phi = zr[4:].reshape(4, 4); w = Phi @ V
        dt = -w[1]/fr[1]; dz = w + np.outer(fr[:4], dt)
        return np.array([zr[0], zr[2]]), dz[[0, 2], :]
    return section_jac
