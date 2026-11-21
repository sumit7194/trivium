"""V26 addendum I: check Neon T14 (U_a separation). I1: Neon's finite-interval ray representation of c0 vs the
independent B8 ODE continuation (a = 0.6). I2: dense float sampling of Re H_theta(1+i eta) > 0. Controls: x^2(1-x)
variant must disagree; the wall crossing at k = -22.5906090375 must give |f0^2 + c0^2| ~ 0 via B8 continuation."""
import sys, os, numpy as np, mpmath as mp, sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v26_B8 import Model, kerr_funcs, kerr_family, base_state_kerr, integrate_path
A = 0.6
def neon_c0(zz, k, wrong=False, M=None):
    mp.mp.dps = 30
    u = mp.mpc(zz)/A; c4, c2, c0c = 90 - 21*k, -(60 - 18*k), 10 - k
    def f(x):
        t = x*x/(u*u)
        w = x*x*(1 - x) if wrong else x*(1 - x)
        return w*(1/(u*u))/(1 + t)**3*mp.sqrt(c4 + c2*t + c0c*t*t)
    return complex(-mp.sqrt(mp.mpf(8)/5)/A*mp.quad(f, [0, 1]))
def b8_c0(zz, k):
    f0, S2, cKpp = kerr_family(); m = Model(kerr_funcs(), 0.8)
    Yb = base_state_kerr(S2, cKpp, k)
    path = [4.0, complex(4, zz.imag), complex(zz)]
    return integrate_path(m, path, Yb, k, 1e-12, conly=True)[0]
def Htheta(theta, eta, n=400):
    u = 1 + 1j*eta; a_, b_, g_ = 21*(1 - theta), 120/7*theta - 18*(1 - theta), 1 + 33/7*theta
    x = (np.arange(n) + 0.5)/n
    t = x*x/u**2; Phi = (1 + u**-2)/(1 + t)**3
    val = x*(1 - x)*Phi*np.sqrt(a_ + b_*t + g_*t*t + 0j)
    return np.sqrt(8/5)*val.mean()
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'run'
    if mode == 'precheck':
        z = 1 + 0.5j; k = 0.1
        print('PRECHECK control x^2(1-x) vs correct at z=1+0.5i,k=0.1: |diff| = %.3e' % abs(neon_c0(z, k, True) - neon_c0(z, k)))
        kw = -22.5906090375; zw = complex(-0.36260544, 1.10838499)
        c0w = b8_c0(zw, kw); f0w = 1 - 1/(zw - 0.6j) - 1/(zw + 0.6j)
        print('PRECHECK wall control via B8: |f0^2+c0^2| at z_wall,k_wall = %.3e (|f0|^2 = %.3f)' % (abs(f0w**2 + c0w**2), abs(f0w)**2))
        sys.exit()
    worst = 0
    for k in (-5.0, 0.1, 4.2):
        for z in (1 + 0.5j, 1 + 3j, 1 - 2j, 2.5 + 1j):
            d = abs(neon_c0(z, k) - b8_c0(z, k)); worst = max(worst, d)
            print('I1 k=%5.2f z=%s |ray - B8| = %.2e' % (k, z, d))
    wrong = abs(neon_c0(1 + 0.5j, 0.1, True) - neon_c0(1 + 0.5j, 0.1))
    ok1 = worst <= 1e-8 and wrong > 1e-3
    th = np.linspace(0, 1, 201); et = np.concatenate([np.linspace(0, 10, 401), np.linspace(10, 200, 191)])
    best = (np.inf, None)
    for t_ in th:
        for e_ in et:
            v = Htheta(t_, e_).real
            if v < best[0]: best = (v, (t_, e_))
    print('I2 grid min Re H_theta(1+i eta) = %.4e at (theta, eta) = %s ; Neon certified lower bound 7.006e-05' % best)
    ok2 = best[0] >= 7.006e-5
    print('VERDICT I1', 'PASS' if ok1 else 'FAIL', '| I2', 'PASS' if ok2 else 'FAIL')
