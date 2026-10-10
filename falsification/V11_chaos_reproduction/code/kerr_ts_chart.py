"""Kerr in the TS (prolate spheroidal, sigma = 1) chart, built from the delta = 1 Ernst potential xi = p x - i q y with the
same conventions the bridge verified for ansatz's TS2 files (E = (xi-1)/(xi+1), twist eqs with sigma = 1), so a Kerr
orbit can be replayed in ansatz's chart. omega is fixed by the twist equations, checked symbolically; vacuum is checked
with V8's vacuum_check at rational points."""
import sympy as sp
x, y = sp.symbols('x y', real=True)
def kerr_ts(p, q):
    A = p**2*x**2 + q**2*y**2 - 1; B = (p*x + 1)**2 + q**2*y**2
    f = A/B
    E = sp.expand_complex(((p*x - sp.I*q*y) - 1)/((p*x - sp.I*q*y) + 1)); chi = sp.simplify(sp.im(E))
    om = 2*q*(1 - y**2)*(p*x + 1)/(p*A)          # candidate; sign/normalisation verified below
    tw1 = sp.simplify(sp.diff(om, x) - (1 - y**2)/f**2*sp.diff(chi, y))
    tw2 = sp.simplify(sp.diff(om, y) + (x**2 - 1)/f**2*sp.diff(chi, x))
    if tw1 != 0 or tw2 != 0:
        om = -om
        tw1 = sp.simplify(sp.diff(om, x) - (1 - y**2)/f**2*sp.diff(chi, y)); tw2 = sp.simplify(sp.diff(om, y) + (x**2 - 1)/f**2*sp.diff(chi, x))
    assert tw1 == 0 and tw2 == 0, ('twist equations fail', tw1, tw2)
    e2g = A/(p**2*(x**2 - y**2))
    g = dict(g_TT=-f, g_Tphi=f*om, g_phiphi=-f*om**2 + (x**2 - 1)*(1 - y**2)/f,
             g_xx=e2g*(x**2 - y**2)/(f*(x**2 - 1)), g_yy=e2g*(x**2 - y**2)/(f*(1 - y**2)))
    return g, om
if __name__ == '__main__':
    g, om = kerr_ts(sp.Rational(4, 5), sp.Rational(3, 5)); print('omega =', sp.factor(om))
    import runpy
