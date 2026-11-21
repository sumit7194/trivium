"""V26-K4: end-to-end zero count of G1(z; a, k, E) = E^2 (f0^2 + c0^2) - f0 in Re z > c (argument principle on a
D-contour), with c0 from the ray representation (validated against the independent B8 ODE continuation in V26-I1)."""
import sys, numpy as np
xg, wg = np.polynomial.legendre.leggauss(240); xg = (xg + 1)/2; wg = wg/2
def c0(z, a, k):
    u = np.asarray(z, dtype=complex)[..., None]/a
    c4, c2, cc0 = 90 - 21*k, -(60 - 18*k), 10 - k
    t = xg**2/u**2
    f = xg*(1 - xg)/u**2/(1 + t)**3*np.sqrt(c4 + c2*t + cc0*t*t + 0j)
    return -np.sqrt(8/5)/a*(f*wg).sum(-1)
def G1(z, a, k, E):
    f0 = 1 - 2*z/(z*z + a*a); return E*E*(f0*f0 + c0(z, a, k)**2) - f0
def count(a, k, E, c, n=6000):
    """winding of G1 on the D-contour; the sample count is doubled until every angle step is < 0.3 rad"""
    Y = max(60.0, 40/(E*E - 1))
    while True:
        y = np.linspace(Y, -Y, n); th = np.linspace(-np.pi/2, np.pi/2, n)   # counter-clockwise around Re z > c
        z = np.concatenate([c + 1j*y, c + Y*np.exp(1j*th)])
        g = G1(z, a, k, E); d = np.diff(np.angle(g)); d = (d + np.pi) % (2*np.pi) - np.pi
        if np.max(np.abs(d)) < 0.3: break
        n *= 2
        assert n <= 800000, 'contour under-resolved'
    return d.sum()/(2*np.pi), np.min(np.abs(G1(c + 1j*y, a, k, E)))

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'precheck':
        for (E, c, exp) in ((1.5, 2.5, 1), (1.63, 2.5, 2), (2.0, 2.5, 0), (1.5, 1.0, 2)):  # exact r+- at k=0
            w, m = count(0.6, 0.0, E, c)
            print('K4 control k=0 a=0.6 E=%.2f Re z>%.1f: winding %.4f expected %d | min|G1| on line %.3e' % (E, c, w, exp, m))
        sys.exit()
    rng = np.random.default_rng(2026_11_21); bad = 0
    cases = [(rng.uniform(0.05, 0.95), rng.uniform(-30, 30/7 - 0.02), np.exp(rng.uniform(np.log(1.02), np.log(6)))) for _ in range(24)]
    cases += [(0.95, 4.27, 1.02), (0.05, 4.27, 6.0), (0.95, -30, 1.02), (0.5, 4.2857, 1.3)]
    for a, k, E in cases:
        w, m = count(a, k, E, 1.0)
        ok = abs(w - 2) < 0.01; bad += not ok
        print('K4 a=%.3f k=%8.4f E=%.3f : winding %.4f | min|G1| on Re z=1: %.3e %s' % (a, k, E, w, m, '' if ok else '<-- FAIL'))
    print('VERDICT K4', 'PASS' if bad == 0 else 'FAIL (%d)' % bad)
