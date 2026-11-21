"""V28 addendum B: per-slice shape test of the T25 BIE Delta C(w,a) against the per-slice bilinear B_X(u=w)."""
import numpy as np
def B(a, u, legs, P=30.0, Np=480):
    lam = np.sin(np.pi*a)/np.pi
    x, w = np.polynomial.legendre.leggauss(Np); p, wp = P*x, P*w
    d = p[:, None] - p[None, :]; e = np.exp(-(u/2)*np.cosh(p))
    R = e[:, None]*np.exp((a - .5)*d)/(2*np.cosh(d/2))*e[None, :]
    Rop, RTop = R*wp[None, :], R.T*wp[None, :]
    vl, vr = (e, e) if legs == 'v0' else (np.exp(-a*p)*e, np.exp(a*p)*e)
    xx = np.linalg.solve(np.eye(Np) - lam**2*(RTop @ Rop), RTop @ vr)
    return np.sum(vl*xx*wp)
bie = {0.3: [(1.00, -0.006392, 1.0e-5), (0.30, -0.064878, 2.2e-5), (0.10, -0.207750, 4.3e-5), (0.03, -0.510839, 8.9e-5), (0.01, -1.00630, 1.7e-4)],
       0.2: [(0.30, -0.045439, 7.6e-6), (0.10, -0.136563, 1.2e-5), (0.03, -0.304101, 2.0e-5), (0.01, -0.535003, 3.0e-5)],
       0.4: [(0.30, -0.085564, 5.5e-5), (0.10, -0.30115, 1.3e-4), (0.03, -0.84638, 3.5e-4), (0.01, -1.92856, 8.4e-4)]}
verdict = {}
for a, rows in bie.items():
    lam = np.sin(np.pi*a)/np.pi; tol = max(3*max(e/abs(v) for _, v, e in rows), 1e-3)
    for legs in ('RL', 'v0'):
        k = [v/B(a, w, legs) for w, v, _ in rows]
        spread = max(k)/min(k) - 1 if min(k) > 0 else max(k)/min(k) - 1
        ok = abs(max(k)/min(k)) <= 1 + tol
        verdict[(a, legs)] = ok
        print('a=%.1f legs=%s: k(w) = %s | spread %.2e (tol %.1e) %s | k*4pi/lam = %.6f' % (
            a, legs, ' '.join('%.6f' % x for x in k), abs(max(k)/min(k) - 1), tol, 'PASS' if ok else 'FAIL', np.mean(k)*4*np.pi/lam))
rl = all(verdict[(a, 'RL')] for a in bie); v0 = all(verdict[(a, 'v0')] for a in bie); v0none = not any(verdict[(a, 'v0')] for a in bie); rlnone = not any(verdict[(a, 'RL')] for a in bie)
print('DECISION:', 'RL (T23) SUPPORTED' if rl and v0none else ('v0 SUPPORTED' if v0 and rlnone else 'INCONCLUSIVE'))
