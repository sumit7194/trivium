"""V27-B controls, run ALONE before the prereg is committed (target not touched)."""
import numpy as np, sys; sys.path.insert(0, __file__.rsplit('/', 1)[0])
from v27_B_lib import monodromy, eta_max, winding, floquet_product_winding
out = []
# C3 integrator floor: P = z^3 (Euler); exact tr = -2 cosh(pi sqrt(23)/2)
M, s = monodromy(lambda z: 3/z, 5792.6)
ex = -2*np.cosh(np.pi*np.sqrt(23)/2)
out.append('C3 z^3: tr %.10f exact %.10f relerr %.2e | det-1 %.2e' % (M.trace().real, ex, abs(M.trace()-ex)/abs(ex), abs(np.linalg.det(M)-1)))
# C1 must-escape: P = (z-1)(z-2) on |z| = 20; exact tr = -2 cosh(pi sqrt 2); winding of v+v- expected 1 (Y=(v+v-)^2 has 2 zeros = N+P = 2)
dl = lambda z: 1/(z-1) + 1/(z-2)
M, s = monodromy(dl, 20.0)
ex = -2*np.cosh(np.pi*np.sqrt(2))
wy, lam = floquet_product_winding(M, s, 20.0)
out.append('C1 (z-1)(z-2): tr %.8f exact %.8f relerr %.2e | det-1 %.2e | winding(v+v-) %.4f | m %.4f | N+P = 2 < 3 -> Thm 1 not applicable' % (
    M.trace().real, ex, abs(M.trace()-ex)/abs(ex), abs(np.linalg.det(M)-1), wy, winding(lambda z, th: (z-1)*(z-2), 20.0)))
# C2 must-fail on the hypothesis: lacunary product at R = 2^9.3 (near the zero at 2^9); eta must exceed 1/15
c = np.array([2.0**(k*k) for k in range(1, 9)])
f0 = lambda z: np.prod(1 - z[..., None]/c, axis=-1)
df0 = lambda z: f0(z)*np.sum(1/(z[..., None] - c), axis=-1)
a = 0.7; dlP = lambda z: df0(np.atleast_1d(z))/(f0(np.atleast_1d(z)) - a)
R2 = 2**9.3; m2 = round(winding(lambda z, th: a - f0(z), R2))
out.append('C2 lacunary R=2^9.3: m %d | max|eta| %.4f (must be > 1/15 = %.4f)' % (m2, eta_max(dlP, R2, m2), 1/15))
print('\n'.join(out))
