"""V13 orbit integrator: numba DOP853 (same coefficients and step control as V12/scipy) on the regularised MN field
(v13_field, gate A2 passed). Records every up-crossing of y = 0 (the section, p_y > 0): (x, p_x, tau, |H + 1/2|).
Domain D (A1 = quantum B9) is checked at every accepted step end:
  (a) g_phiphi > 0 at the point and at the 4 corners and 4 edge midpoints of the box (x, y) +/- 0.025;
  (a') x - 1 >= 0.05;  (c) R = sqrt(x^2 + y^2 - 1) >= 0.5;  every field value finite.
Outcomes: 0 SURVIVE (N returns), 1 LEFT_D, 2 ESCAPE (x > 1000), 3 CAPPED, 4 FORBIDDEN start."""
import sys, os, math
import numpy as np, sympy as sp, numba
import scipy.integrate._ivp.dop853_coefficients as DC
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v13_field import build, W_reg, ginv_reg, gpp_reg, x as X, y as Y

NS = DC.N_STAGES
A = np.ascontiguousarray(DC.A[:NS, :NS]); B = DC.B.copy(); C = DC.C[:NS].copy()
E3 = DC.E3.copy(); E5 = DC.E5.copy(); D = DC.D.copy()
AX = np.ascontiguousarray(DC.A[NS + 1:]); CX = DC.C[NS + 1:].copy()
SURVIVE, LEFT_D, ESCAPE, CAPPED, FORBIDDEN = 0, 1, 2, 3, 4
X_ES, BOX = 1000.0, 0.025

def make(M, a_, beta, E, Lz, domain='B9'):
    """domain='B9' (counted screens) or 'base' (C0 instrument gate, A3: only g_phiphi > 0 and finite, |y| < 1, x > 1)."""
    BASE = (domain == 'base')
    S = build(M, a_, beta); E, Lz = sp.nsimplify(E), sp.nsimplify(Lz)
    gxx, gyy = ginv_reg(S); W = W_reg(S, E, Lz)
    flat = []
    for f in (gxx, gyy, W): flat += [f, sp.diff(f, X), sp.diff(f, Y)]
    pieces = numba.njit(sp.lambdify([X, Y], flat, 'math', cse=True))
    gpp = numba.njit(sp.lambdify([X, Y], gpp_reg(S), 'math', cse=True))

    @numba.njit
    def rhs(z, out):
        q = pieces(z[0], z[1]); px, py = z[2], z[3]
        out[0] = q[0]*px; out[1] = q[3]*py
        out[2] = -0.5*(q[1]*px*px + q[4]*py*py + q[7]); out[3] = -0.5*(q[2]*px*px + q[5]*py*py + q[8])

    @numba.njit
    def ham(z):
        q = pieces(z[0], z[1]); return 0.5*(q[0]*z[2]*z[2] + q[3]*z[3]*z[3] + q[6])

    @numba.njit
    def in_D(xv, yv):
        if BASE:
            if not (xv > 1.0) or not (abs(yv) < 1.0): return False
            g = gpp(xv, yv)
            return g > 0.0 and math.isfinite(g)
        if not (xv - 1.0 >= 0.05): return False
        if xv*xv + yv*yv - 1.0 < 0.25: return False
        for dx in (-BOX, 0.0, BOX):
            for dy in (-BOX, 0.0, BOX):
                yy = yv + dy
                if yy >= 1.0 or yy <= -1.0: return False
                g = gpp(xv + dx, yy)
                if not (g > 0.0) or not math.isfinite(g): return False
        return True

    @numba.njit
    def start(x0, px0):
        """y = 0, p_x = px0, p_y > 0 from H = -1/2. Returns (ok, py0)."""
        q = pieces(x0, 0.0); rest = -1.0 - q[6] - q[0]*px0*px0
        if not (rest > 0.0) or not (q[3] > 0.0): return False, 0.0
        return True, math.sqrt(rest/q[3])

    @numba.njit
    def dense_eval(F, y_old, s, out):
        for k in range(4): out[k] = 0.0
        for i in range(7):
            f = F[6 - i]
            for k in range(4): out[k] += f[k]
            fac = s if i % 2 == 0 else 1.0 - s
            for k in range(4): out[k] *= fac
        for k in range(4): out[k] += y_old[k]

    @numba.njit
    def root(F, y_old, comp, level, s_lo, s_hi):
        """Bisection (60 halvings) for z[comp](s) = level on [s_lo, s_hi] of the dense output."""
        tmp = np.empty(4)
        dense_eval(F, y_old, s_lo, tmp); flo = tmp[comp] - level
        for _ in range(60):
            sm = 0.5*(s_lo + s_hi); dense_eval(F, y_old, sm, tmp); fm = tmp[comp] - level
            if (fm < 0) == (flo < 0): s_lo = sm; flo = fm
            else: s_hi = sm
        return 0.5*(s_lo + s_hi)

    @numba.njit
    def integrate(x0, px0, N, rtol, atol, tau_max, max_steps):
        """Returns (outcome, ncross, tau, max_drift, steps, sec[N,4]) with sec rows (x, p_x, tau, |H+1/2| so far)."""
        sec = np.zeros((max(N, 1), 4))
        ok, py0 = start(x0, px0)
        if not ok or not in_D(x0, 0.0): return FORBIDDEN, 0, 0.0, 0.0, 0, sec
        y = np.array([x0, 0.0, px0, py0]); f = np.empty(4); rhs(y, f)
        K = np.zeros((16, 4)); ynew = np.empty(4); fnew = np.empty(4); tmp = np.empty(4); F = np.zeros((7, 4))
        sc = atol + np.abs(y)*rtol
        d0 = math.sqrt(np.mean((y/sc)**2)); d1 = math.sqrt(np.mean((f/sc)**2))
        h0 = 1e-6 if (d0 < 1e-5 or d1 < 1e-5) else 0.01*d0/d1
        y1 = y + h0*f; f1 = np.empty(4); rhs(y1, f1)
        d2 = math.sqrt(np.mean(((f1 - f)/sc)**2))/h0
        h1 = max(1e-6, h0*1e-3) if (d1 <= 1e-15 and d2 <= 1e-15) else (0.01/max(d1, d2))**(1.0/8.0)
        h = min(100*h0, h1)
        t = 0.0; ncross = 0; steps = 0; drift = 0.0
        while True:
            if t >= tau_max: return SURVIVE, ncross, t, drift, steps, sec
            if steps >= max_steps: return CAPPED, ncross, t, drift, steps, sec
            rejected = False
            while True:
                hh = min(h, tau_max - t)
                K[0] = f
                for s in range(1, NS):
                    for k in range(4):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*A[s, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(4):
                    acc = 0.0
                    for j in range(NS): acc += K[j, k]*B[j]
                    ynew[k] = y[k] + hh*acc
                rhs(ynew, fnew); K[NS] = fnew
                e5 = 0.0; e3 = 0.0
                for k in range(4):
                    sck = atol + max(abs(y[k]), abs(ynew[k]))*rtol
                    a5 = 0.0; a3 = 0.0
                    for j in range(NS + 1): a5 += K[j, k]*E5[j]; a3 += K[j, k]*E3[j]
                    e5 += (a5/sck)**2; e3 += (a3/sck)**2
                if e5 == 0.0 and e3 == 0.0: en = 0.0
                else: en = hh*e5/math.sqrt((e5 + 0.01*e3)*4)
                if not math.isfinite(en): en = 1e300
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return CAPPED, ncross, t, drift, steps, sec
            steps += 1
            dH = abs(ham(ynew) + 0.5)
            if dH > drift: drift = dH
            if not in_D(ynew[0], ynew[1]): return LEFT_D, ncross, t + hh, drift, steps, sec
            if ynew[0] > X_ES: return ESCAPE, ncross, t + hh, drift, steps, sec
            if y[1] < 0.0 and ynew[1] >= 0.0:
                for s in range(NS + 1, 16):
                    for k in range(4):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*AX[s - NS - 1, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(4):
                    dy = ynew[k] - y[k]
                    F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                    for r in range(4):
                        acc = 0.0
                        for j in range(16): acc += D[r, j]*K[j, k]
                        F[3 + r, k] = hh*acc
                su = root(F, y, 1, 0.0, 0.0, 1.0); dense_eval(F, y, su, tmp)
                sec[ncross, 0] = tmp[0]; sec[ncross, 1] = tmp[2]; sec[ncross, 2] = t + su*hh; sec[ncross, 3] = drift
                ncross += 1
                if ncross >= N: return SURVIVE, ncross, t + su*hh, drift, steps, sec
            t += hh
            for k in range(4): y[k] = ynew[k]; f[k] = fnew[k]

    return integrate, start, ham, in_D, pieces
