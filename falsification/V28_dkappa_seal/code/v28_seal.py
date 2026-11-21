"""V28 seal: own re-implementation of the T20 (v0) and T23 (v_R, v_L) resummed same-tip coefficient at real alpha."""
import numpy as np, sys
from scipy.special import gamma as G, gammaln
def grid(L, N):
    x, w = np.polynomial.legendre.leggauss(N); return L*x, L*w
def Cplus(a, legs, P=12.0, Np=160, Q=(-16.0, 4.0), Nq=140, resum=True):
    lam = np.sin(np.pi*a)/np.pi
    p, wp = grid(P, Np); d = p[:, None] - p[None, :]
    core = np.exp((a - 0.5)*d)/(2*np.cosh(d/2))
    qx, qw = np.polynomial.legendre.leggauss(Nq); q = (Q[1] - Q[0])/2*qx + (Q[1] + Q[0])/2; wq = (Q[1] - Q[0])/2*qw
    tot = 0.0
    for qi, wqi in zip(q, wq):
        u = np.exp(qi); e = np.exp(-(u/2)*np.cosh(p))
        R = e[:, None]*core*e[None, :]                      # kernel R(p,p')
        RT = R.T
        Rop, RTop = R*wp[None, :], RT*wp[None, :]           # operators with quadrature weights
        if legs == 'v0': vl = e.copy(); vr = e.copy()
        elif legs == 'RL': vl = np.exp(-a*p)*e; vr = np.exp(a*p)*e      # v_R on the left leg, v_L on the right
        elif legs == 'LR': vl = np.exp(a*p)*e; vr = np.exp(-a*p)*e
        x = RTop @ vr
        if resum: x = np.linalg.solve(np.eye(Np) - lam**2*(RTop @ Rop), x)
        B = np.sum(vl*x*wp)
        tot += wqi*np.exp(qi)*(np.exp(qi)/2)**(2*a)*B
    return -lam/(4*np.pi**2*G(1 + a)**2)*tot
def born(a): return -(np.sin(np.pi*a)/(4*np.pi**3))*(G(a + .5)/G(a + 1))**2*G(2*a + .5)*G(1.5)/G(2*a + 2)
def t23m0(a): return -(np.sin(np.pi*a)/(4*np.pi**3))*(G(a + .5)/G(a + 1))**2*G(3*a + .5)*G(1.5 - a)/G(2*a + 2)
if __name__ == '__main__':
    out = []
    for a in (0.05, 0.3, 0.45):
        b0 = Cplus(a, 'v0', resum=False); rl = Cplus(a, 'RL', resum=False); lr = Cplus(a, 'LR', resum=False)
        out.append('S1/S2 a=%.2f: v0 m0 %.10f Born %.10f rel %.1e | RL m0 %.10f LR m0 %.10f T23-closed %.10f rel(RL) %.1e rel(LR) %.1e' % (
            a, b0, born(a), abs(b0/born(a) - 1), rl, lr, t23m0(a), abs(rl/t23m0(a) - 1), abs(lr/t23m0(a) - 1)))
    for a in (0.2, 0.3, 0.4):
        for legs in ('v0', 'RL'):
            v1 = Cplus(a, legs); v2 = Cplus(a, legs, Np=320); v3 = Cplus(a, legs, P=16.0, Np=320, Q=(-22.0, 5.0), Nq=200)
            m0 = Cplus(a, legs, P=16.0, Np=320, Q=(-22.0, 5.0), Nq=200, resum=False)
            out.append('SEAL a=%.1f legs=%s: C+resum %.10f (Np x2: %.10f, ext: %.10f; conv %.1e, %.1e) | m0 %.10f | ratio %.6f' % (
                a, legs, v3, v1, v2, abs(v2/v1 - 1), abs(v3/v2 - 1), m0, v3/m0))
    print('\n'.join(out))
