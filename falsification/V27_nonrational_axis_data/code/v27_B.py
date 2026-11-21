"""V27-B target: Neon T21 Theorem 1 on the lacunary example (prereg addendum B)."""
import numpy as np, sys; sys.path.insert(0, __file__.rsplit('/', 1)[0])
from v27_B_lib import monodromy, eta_max, winding, floquet_product_winding
c = np.array([2.0**(k*k) for k in range(1, 9)])
f0 = lambda z: np.prod(1 - np.asarray(z)[..., None]/c, axis=-1)
df0 = lambda z: f0(z)*np.sum(1/(np.asarray(z)[..., None] - c), axis=-1)
a = 0.7; R = 2**12.5
dlP = lambda z: df0(z)/(f0(z) - a)
ok = {}; out = []
wraw = winding(lambda z, th: a - f0(z), R); m = round(wraw)
roots = []
for z in (2.0+0j, 16.0+0j, 512.0+0j):
    for _ in range(100): z = z - (f0(z) - a)/df0(z)
    roots.append(complex(z))
roots_ok = all(abs(r) < R and abs(f0(r) - a) < 1e-8*max(1, abs(a)) and abs(df0(r)) > 1e-6 for r in roots) \
    and min(abs(roots[i] - roots[j]) for i in range(3) for j in range(i+1, 3)) > 1e-3
ok['B1'] = abs(wraw - 3) < 1e-3 and roots_ok
out.append('B1: winding %.6f | a-points %s | |f0\'| %s' % (wraw, ['%.6g' % r.real if abs(r.imag) < 1e-9 else str(r) for r in roots],
           ['%.3g' % abs(df0(r)) for r in roots]))
e16 = eta_max(dlP, R, m, n=2**16); e14 = eta_max(dlP, R, m, n=2**14)
ok['B2'] = e16 < 1/15 and abs(e16 - e14) < 1e-6 and abs(e16 - 0.06045) <= 1e-4
out.append('B2: max|eta| %.6f (2^14: %.6f) vs 1/15 = %.6f; Neon 0.06045' % (e16, e14, 1/15))
M, s = monodromy(dlP, R)
tr = M.trace(); det = np.linalg.det(M)
ok['B3'] = abs(tr - (-1869.187)) <= 0.01 and abs(tr) > 27
ok['B4'] = abs(det - 1) <= 1e-6
out.append('B3: tr %.6f%+.2ei (Neon -1869.187) | B4: |det-1| %.2e' % (tr.real, tr.imag, abs(det - 1)))
wy, lam = floquet_product_winding(M, s, R)
ok['B5'] = abs(wy - 1) < 0.01
out.append('B5: winding(v+ v-) %.5f | multipliers %s' % (wy, ['%.4g' % abs(l) for l in lam]))
out.append(str(ok)); out.append('VERDICT V27-B ' + ('PASS' if all(ok.values()) else 'FAIL'))
print('\n'.join(out))
