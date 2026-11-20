"""V26 addendum B: jump of omega between the two outer axis segments along a semicircle of radius R,
Delta omega(R) = int_0^pi R^2 sin(theta) d_r chi / f^2 dtheta, from the Bridge's own Ernst series (v26_L.solve)."""
import os, sys, json, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v26_L import solve, u
N = 10; Z = sp.symbols('Z')                      # Z = 1/z
def moments(e_axis):
    xi = sp.series(((1 - e_axis)/(1 + e_axis)).subs(sp.Symbol('z'), 1/Z), Z, 0, N + 2).removeO()
    return [sp.nsimplify(sp.expand(xi).coeff(Z, k + 1)) for k in range(N + 1)]
zs = sp.Symbol('z'); I = sp.I
out = {}
for label, e_ax in (('AF twisted: 1 - 2/z + i/z^2', 1 - 2/zs + I/zs**2), ('CONTROL NUT: 1 - 2/z + i/(2z) + i/z^2', 1 - 2/zs + I/(2*zs) + I/zs**2)):
    mx = moments(e_ax); my = [sp.conjugate(m) for m in mx]
    Fx, Fy = solve(mx, my, N)
    r = sp.symbols('r', positive=True)
    X = sum(r**-(k + 1)*Fx[k] for k in range(N + 1)); Y = sum(r**-(k + 1)*Fy[k] for k in range(N + 1))
    e = (1 - X)/(1 + X); eb = (1 - Y)/(1 + Y)
    chi = (e - eb)/(2*I); f = (e + eb)/2
    integrand = sp.lambdify((r, u), r**2*sp.diff(chi, r)/f**2, 'mpmath')
    rows = []
    for R in (20, 40, 80):
        val = mp.quad(lambda th: mp.sin(th)*integrand(R, mp.cos(th)), [0, mp.pi])
        rows.append((R, complex(val)))
        print(label, '| R', R, '| Delta omega', mp.nstr(val, 10), flush=True)
    out[label] = rows
json.dump(out, open(os.path.join(HERE, '../results/v26_omega.json'), 'w'), indent=1, default=str)
