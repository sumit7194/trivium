"""V26 exact controls: closed-form Ernst potentials xi(x, y) in prolate coordinates (rho = s sqrt((x^2-1)(1-y^2)),
z = s x y). Upper axis: y = 1, x = z/s (z > s). Lower axis: y = -1, x = -z/s (z < -s). Rule L: xi_l(z) = -xi_u(z)."""
import sympy as sp
x, y, z, s, p, q, al = sp.symbols('x y z s p q alpha', real=True)
cases = {
  'Schwarzschild (xi = x)': x,
  'Kerr (xi = p x + i q y)': p*x + sp.I*q*y,
  'Kerr-NUT (xi = e^{i alpha}(p x + i q y))': sp.exp(sp.I*al)*(p*x + sp.I*q*y),
  'Tomimatsu-Sato delta=2': (p**2*x**4 + q**2*y**4 - 1 - 2*sp.I*p*q*x*y*(x**2 - y**2))/(2*p*x*(x**2 - 1) - 2*sp.I*q*y*(1 - y**2)),
}
for name, xi in cases.items():
    xu = xi.subs({x: z/s, y: 1}); xl = xi.subs({x: -z/s, y: -1})
    ruleL = sp.simplify(xl + xu) == 0
    mirror = sp.simplify(xl - xi.subs({x: -z/s, y: 1})) == 0          # e_-(z) = e_+(-z)
    print('%-45s rule L: %s | mirror guess: %s' % (name, ruleL, mirror))
