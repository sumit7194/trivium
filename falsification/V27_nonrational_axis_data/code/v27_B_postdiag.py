"""V27-B POST-RUN DIAGNOSTIC (labelled, not the registered verdict): B1 simplicity with a division-free derivative.
The registered harness used f0' = f0 * sum 1/(z - c_k), which is 0*inf at the Newton start points 2, 16, 512 (zeros of f0)."""
import numpy as np
c = np.array([2.0**(k*k) for k in range(1, 9)])
f0 = lambda z: np.prod(1 - z/c)
df0 = lambda z: sum(-1/c[k]*np.prod(np.delete(1 - z/c, k)) for k in range(len(c)))
a = 0.7; R = 2**12.5; roots = []
for z in (2.0+0j, 16.0+0j, 512.0+0j):
    for _ in range(100): z = z - (f0(z) - a)/df0(z)
    roots.append(z)
print('a-points', [complex(r) for r in roots]); print('|f0-a|', ['%.1e' % abs(f0(r)-a) for r in roots], '|f0\'|', ['%.3g' % abs(df0(r)) for r in roots])
okB1p = all(abs(r) < R and abs(f0(r)-a) < 1e-8 and abs(df0(r)) > 1e-6 for r in roots) and min(abs(roots[i]-roots[j]) for i in range(3) for j in range(i+1, 3)) > 1e-3
print('B1-prime (diagnostic) simplicity + distinctness:', okB1p, '| registered winding 3.000000 unchanged')
