"""V12 outcome integrator: numba-compiled DOP853 (Hairer-Norsett-Wanner coefficients as shipped in scipy; same error
norm and step control as scipy's DOP853), 4-dim reduced geodesic flow, events located on the 7th-order dense output.
Outcome codes: 0 SURVIVE (N up-crossings of y = 0 or tau_max), 1 PLUNGE (x < 1.5), 2 ESCAPE (x > 2000 or |y| > 0.999999),
3 CAPPED (step cap), 4 FORBIDDEN start."""
import sys, os, math
import numpy as np, sympy as sp, numba
import scipy.integrate._ivp.dop853_coefficients as DC
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v12_lsep import get_metric, X, Y

NS = DC.N_STAGES
A = np.ascontiguousarray(DC.A[:NS, :NS]); B = DC.B.copy(); C = DC.C[:NS].copy()
E3 = DC.E3.copy(); E5 = DC.E5.copy(); D = DC.D.copy()
AX = np.ascontiguousarray(DC.A[NS + 1:]); CX = DC.C[NS + 1:].copy()
SURVIVE, PLUNGE, ESCAPE, CAPPED, FORBIDDEN = 0, 1, 2, 3, 4
X_PL, X_ES, Y_ES = 1.5, 2000.0, 0.999999

def make(case, E, L):
    g = get_metric(case); E, L = sp.nsimplify(E), sp.nsimplify(L)
    det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    Gtt, Gtp, Gpp = g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det
    Aa, Bb = 1/g['g_xx'], 1/g['g_yy']; W = Gtt*E**2 - 2*Gtp*E*L + Gpp*L**2
    flat = []
    for f in (Aa, Bb, W): flat += [f, sp.diff(f, X), sp.diff(f, Y)]
    pieces = numba.njit(sp.lambdify([X, Y], flat, 'math', cse=True))

    @numba.njit
    def rhs(z, out):
        q = pieces(z[0], z[1]); px, py = z[2], z[3]
        out[0] = q[0]*px; out[1] = q[3]*py
        out[2] = -0.5*(q[1]*px*px + q[4]*py*py + q[7]); out[3] = -0.5*(q[2]*px*px + q[5]*py*py + q[8])

    @numba.njit
    def ham(z):
        q = pieces(z[0], z[1]); return 0.5*(q[0]*z[2]*z[2] + q[3]*z[3]*z[3] + q[6])

    @numba.njit
    def start(x0, px0):
        """y = 0, p_x = px0, p_y > 0 from the mass shell H = -1/2. Returns (ok, py0)."""
        q = pieces(x0, 0.0); rest = -1.0 - q[6] - q[0]*px0*px0
        if rest <= 0.0 or q[3] <= 0.0: return False, 0.0
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
    def integrate(x0, px0, N, rtol, atol, tau_max, max_steps, record):
        """Returns (outcome, crossings, tau, H_drift, steps, section_x[record])."""
        secx = np.zeros(max(record, 1))
        ok, py0 = start(x0, px0)
        if not ok: return FORBIDDEN, 0, 0.0, 0.0, 0, secx
        y = np.array([x0, 0.0, px0, py0]); f = np.empty(4); rhs(y, f)
        K = np.zeros((16, 4)); ynew = np.empty(4); fnew = np.empty(4); tmp = np.empty(4); F = np.zeros((7, 4))
        # initial step (Hairer-Norsett-Wanner II.4, as scipy)
        sc = atol + np.abs(y)*rtol
        d0 = math.sqrt(np.mean((y/sc)**2)); d1 = math.sqrt(np.mean((f/sc)**2))
        h0 = 1e-6 if (d0 < 1e-5 or d1 < 1e-5) else 0.01*d0/d1
        y1 = y + h0*f; f1 = np.empty(4); rhs(y1, f1)
        d2 = math.sqrt(np.mean(((f1 - f)/sc)**2))/h0
        h1 = max(1e-6, h0*1e-3) if (d1 <= 1e-15 and d2 <= 1e-15) else (0.01/max(d1, d2))**(1.0/8.0)
        h = min(100*h0, h1)
        t = 0.0; ncross = 0; steps = 0; H0 = ham(y)
        while True:
            if t >= tau_max: return SURVIVE, ncross, t, abs(ham(y) - H0), steps, secx
            if steps >= max_steps: return CAPPED, ncross, t, abs(ham(y) - H0), steps, secx
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
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return CAPPED, ncross, t, abs(ham(y) - H0), steps, secx
            steps += 1
            # events in (t, t+hh]: up-crossing of y = 0, x < 1.5, x > 2000, |y| > 0.999999
            up = y[1] < 0.0 and ynew[1] >= 0.0
            pl = ynew[0] < X_PL; es = ynew[0] > X_ES or abs(ynew[1]) > Y_ES
            if up or pl or es:
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
                s_up = root(F, y, 1, 0.0, 0.0, 1.0) if up else 2.0
                s_pl = root(F, y, 0, X_PL, 0.0, 1.0) if pl else 2.0
                s_es = 2.0
                if ynew[0] > X_ES: s_es = root(F, y, 0, X_ES, 0.0, 1.0)
                if ynew[1] > Y_ES: s_es = min(s_es, root(F, y, 1, Y_ES, 0.0, 1.0))
                if ynew[1] < -Y_ES: s_es = min(s_es, root(F, y, 1, -Y_ES, 0.0, 1.0))
                s_term = min(s_pl, s_es)
                if up and s_up < s_term:
                    if ncross < record:
                        dense_eval(F, y, s_up, tmp); secx[ncross] = tmp[0]
                    ncross += 1
                    if ncross >= N: return SURVIVE, ncross, t + s_up*hh, abs(ham(ynew) - H0), steps, secx
                if s_term <= 1.0:
                    return (PLUNGE if s_pl <= s_es else ESCAPE), ncross, t + s_term*hh, abs(ham(ynew) - H0), steps, secx
            t += hh
            for k in range(4): y[k] = ynew[k]; f[k] = fnew[k]

    return integrate, start, ham, rhs, pieces
