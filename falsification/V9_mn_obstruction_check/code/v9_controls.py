"""V9 controls. (1) Integrator test: z'' = (beta/x^2) z around x = 0 has trace -2 cos(pi sqrt(1+4 beta)) exactly.
(2) Kerr (beta=0) axial at the same levels: generator traces around every located singular point, from the bridge's
own root-finding, must all lie in [-2, 2] (Kerr is integrable; quantum reports trace ~ 0 at elliptic turning points)."""
import numpy as np, sympy as sp
from v9_nve import axial_r, x
from v9_fast import monodromy, loop_pts
print('(1) integrator test, z\'\' = beta z / x^2, loop around 0 from base 1+1i, radius 0.3:')
for beta in (0.1, -3/16, 1.7):
    rf = lambda z, b=beta: b/z**2
    M = monodromy(rf, loop_pts(1 + 1j, 0, 0.3), 1e-13)
    exact = -2*np.cos(np.pi*np.sqrt(1 + 4*beta)); print(f'   beta={beta}: trace {np.trace(M):.12g}  exact {exact:.12g}  |diff| {abs(np.trace(M) - exact):.1e}', flush=True)
print('(2) Kerr axial controls:')
for tag, (M_, a_) in [('p1', (5, 3)), ('p2', (13, 5))]:
    for mu2 in (4, 9):
        ax = axial_r(M_, a_, 0, 1, mu2); r = ax['r']
        # candidate singular points of r: zeros and poles of A and xdot^2, poles of B (cheap piecewise)
        roots = []
        for e in (ax['A'], ax['xdot2'], ax['B']):
            n_, d_ = sp.fraction(sp.together(sp.simplify(e)))
            for poly in ((n_, d_) if e is not ax['B'] else (d_,)):
                P_ = sp.Poly(sp.expand(poly), x)
                if P_.degree() > 0: roots += [complex(z) for z in np.roots([complex(c) for c in P_.all_coeffs()])]
        uniq = []
        for z in roots:
            if all(abs(z - u) > 1e-6 for u in uniq): uniq.append(z)
        rf = sp.lambdify(x, r, 'numpy'); base = 2.7 + 2.8j
        trs = []
        for c in uniq:
            sep = min([abs(c - d) for d in uniq if d != c] + [abs(c)] if abs(c) > 1e-9 else [abs(c - d) for d in uniq if d != c])
            trs.append(np.trace(monodromy(rf, loop_pts(base, c, 0.3*sep), 1e-12)))
        inside = all(abs(t.imag) < 1e-6 and -2 - 1e-6 <= t.real <= 2 + 1e-6 for t in trs)
        print(f'   Kerr {tag} mu2={mu2}: {len(uniq)} singular points; traces {[f"{t.real:+.4f}{t.imag:+.1e}j" for t in trs]}; all in [-2,2]: {inside}', flush=True)
