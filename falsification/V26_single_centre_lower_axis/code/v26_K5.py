"""V26-K0: symbolic check of T19's E-elimination identity. V26-K5: dense float sanity grid of the analytic tails
(NOT rigorous; the tails were read by hand)."""
import sys, numpy as np, sympy as sp
xg, wg = np.polynomial.legendre.leggauss(400); xg = (xg + 1)/2; wg = wg/2
def Hn(theta, u):
    u = np.asarray(u, dtype=complex)[..., None]
    a, b, g = 21*(1 - theta), 120/7*theta - 18*(1 - theta), 1 + 33/7*theta
    t = xg**2/u**2
    f = xg*(1 - xg)*(1 + u**-2)/(1 + t)**3*np.sqrt(a + b*t + g*t*t + 0j)
    return np.sqrt(8/5)*(f*wg).sum(-1)
def K0():
    y, a, t, H = sp.symbols('y a t H'); z = 1 + sp.I*y; E2 = 1/t
    D = z**2 + a**2; S = y**2 + 1 - a**2
    f0 = (z**2 - 2*z + a**2)/D; c0 = -H/D
    G1 = E2*(f0**2 + c0**2) - f0
    return sp.simplify(sp.expand(D**2*G1/E2 - ((1 - t)*S**2 + 2*t*S + H**2 + 2*sp.I*y*t*S))) == 0
def K5(shift=0.0):
    out = {}; eta = np.concatenate([np.linspace(10, 50, 801), np.geomspace(50, 300, 200)])
    th1 = np.linspace(0, 7/37, 41); v = min((Hn(t, 1 + 1j*eta)**2).real.min() for t in th1); out['K1 tail Re H^2 (eta>=10)'] = v
    eta2 = np.concatenate([np.linspace(5, 50, 901), np.geomspace(50, 300, 200)]); th2 = np.linspace(7/37, 1, 81)
    v = min(1 - np.abs(Hn(t, 1 + 1j*eta2).imag).max()/np.sqrt(t) for t in th2); out['K2 tail 1 - th^-1/2|Im H| (eta>=5)'] = v
    x0 = np.concatenate([np.linspace(5, 50, 901), np.geomspace(50, 300, 200)])
    v = min((lambda H: (H.real - np.abs(H.imag)).min())(Hn(t, x0 + 1j)) for t in th2); out['K3 top-edge tail Re H - |Im H| (x0>=5)'] = v
    return {k: v - shift for k, v in out.items()}
if __name__ == '__main__':
    if sys.argv[1] == 'precheck':
        import mpmath as mp, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from v26_K_lib import H_float
        d = max(abs(complex(H_float(t, X, E)) - Hn(t, X + 1j*E)) for t, X, E in ((0.1, 1, 12.0), (0.5, 1, 7.0), (0.9, 6.0, 1.0), (1.0, 1, 30.0), (0.3, 40.0, 1.0)))
        print('K5 precheck: numpy GL vs mpmath quad max |diff| = %.2e (must be < 1e-9)' % d)
        print('K5 precheck must-fail (shift 10 -> every tail value must go negative; target-independent):', {k: bool(v < 0) for k, v in K5(10).items()})
        sys.exit()
    k0 = K0(); print('K0 identity holds exactly:', k0)
    r = K5(); [print('K5 %s: grid min %.4e' % kv) for kv in r.items()]
    print('VERDICT K0', 'PASS' if k0 else 'FAIL', '| K5', 'PASS' if all(v > 0 for v in r.values()) else 'FAIL')
