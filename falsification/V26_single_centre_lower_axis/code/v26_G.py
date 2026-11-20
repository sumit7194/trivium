"""V26 addendum G: check Neon T11 general-a claims. G1 exact identities; G2 independent I+(a) quadrature."""
import sympy as sp, mpmath as mp
z, A, k, u = sp.symbols('z a k u', positive=True); I = sp.I
def fam(a):
    D = z**2 + a**2; cK = -2*a/D; cK2 = sp.diff(cK, z, 2); v = (z + I*a)/(z - I*a)
    Q = v**3 + v**-3 - sp.Rational(3, 5)*(v + 1/v) - sp.Rational(4, 5)
    return D, cK, cK2, Q, sp.cancel(Q/(2*D**3*cK2))
def neon_dc0(a, wrong=False):
    b = a/sp.sqrt(3); s = -1 if wrong else 1
    return a/(4*(z**2 + a**2)) + s*3*I/(80*a**2)*z*sp.log((z + I*a)/(z - I*a)) + 3*sp.sqrt(3)/(80*a**2)*z*sp.log((z + b)/(z - b)) \
           + 3/(80*a)*sp.log((z**2 - b**2)/(z**2 + a**2))
def G1():
    ok = True; worst = 0; worst_wrong = 0
    for a in (sp.Rational(1, 10), sp.Rational(3, 5), sp.Integer(1), sp.Integer(2)):
        D, cK, cK2, Q, dc2 = fam(a)
        r = sp.diff(neon_dc0(a), z, 2) - dc2; rw = sp.diff(neon_dc0(a, True), z, 2) - dc2
        for pt in (sp.Rational(7, 3)*a, 3*a + 1, 2*a + sp.I*5*a):
            worst = max(worst, abs(complex(sp.N(r.subs(z, pt), 40)))); worst_wrong = max(worst_wrong, abs(complex(sp.N(rw.subs(z, pt), 20))))
        lead = sp.limit(neon_dc0(a)*z**2, z, sp.oo)
        ok &= sp.simplify(lead - 7*a/30) == 0 and sp.limit(neon_dc0(a), z, sp.oo) == 0
    # scaling form of (c0'')^2 with symbolic a, k
    D, cK, cK2, Q, _ = fam(A)
    S2 = cK2**2 + k*Q/D**3
    B = (90 - 21*k)*u**4 - (60 - 18*k)*u**2 + (10 - k)
    scal = sp.simplify(sp.cancel(S2.subs(z, A*u) - 8*B/(5*A**6*(u**2 + 1)**6))) == 0
    w = sp.symbols('w'); disc = sp.factor(sp.discriminant((90 - 21*k)*w**2 - (60 - 18*k)*w + (10 - k), w))
    print('G1: max |dc0_neon\'\' - target| = %.1e ; wrong-sign control %.2e ; limits ok %s ; scaling identity %s ; disc = %s'
          % (worst, worst_wrong, ok, scal, disc))
    return ok and worst < 1e-30 and worst_wrong > 1e-6 and scal and sp.simplify(disc - 240*k*(k - 4)) == 0
def Iplus(a, R=None):
    mp.mp.dps = 20
    D, cK, cK2, Q, dc2 = fam(sp.nsimplify(a))
    f0 = 1 - 1/(z - I*sp.nsimplify(a)) - 1/(z + I*sp.nsimplify(a))
    g = sp.cancel(2*f0*cK/(f0**2 + cK**2)**2); fm = sp.cancel(f0/(f0**2 + cK**2))
    f2, gl, gpl, fmp = [sp.lambdify(z, e, 'mpmath') for e in (dc2, g, sp.diff(g, z), sp.diff(fm, z))]
    ray0 = lambda zz: zz**2*mp.quad(lambda s: (s - 1)*f2(zz*s), [1, 2, 10, mp.inf])
    ray1 = lambda zz: -zz*mp.quad(lambda s: f2(zz*s), [1, 2, 10, mp.inf])
    R = R if R is not None else mp.sqrt(1 + mp.mpf(a)**2)
    aa = mp.mpf(a)
    def integ(th):
        zz = R*mp.expj(th); dz = 1j*zz
        return fmp(zz)*(gpl(zz)*ray0(zz) + gl(zz)*ray1(zz))*(zz - 2 - 1j*aa)**2*dz
    return mp.quad(integ, [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])
def G2():
    vals = {a: Iplus(a) for a in ('0.1', '0.6', '1.0', '2.0')}
    for a, v in vals.items(): print('G2 I+(%s) = %s  |I+| = %s' % (a, mp.nstr(v, 12), mp.nstr(abs(v), 6)))
    t8 = mp.mpc('-0.02433618209447682', '0.02323006896108698')
    c1 = abs(vals['0.6'] - t8)
    c2 = mp.nstr(abs(vals['0.1']), 3) == '0.000689' or abs(abs(vals['0.1'])/mp.mpf('6.89e-4') - 1) < 0.005
    c3 = abs(abs(vals['1.0'])/mp.mpf('0.275') - 1) < 0.0019
    c4 = all(mp.re(v) < 0 for v in vals.values())
    small = Iplus('0.01'); ratio = small/(-7*mp.pi/30*mp.mpf('0.01')**3); wrongr = small/(-7*mp.pi/15*mp.mpf('0.01')**3)
    print('G2 contour independence |I+(0.6) - T8| = %.1e ; |I+(0.1)|~6.89e-4 %s ; |I+(1)|~0.275 %s ; Re<0 all %s'
          % (c1, c2, c3, c4))
    print('G2 a=0.01: I+/(-7 pi a^3/30) = %s ; control (7pi/15) ratio = %s' % (mp.nstr(ratio, 8), mp.nstr(wrongr, 6)))
    return c1 <= 1e-12 and c2 and c3 and c4 and abs(ratio - 1) < 0.01 and abs(wrongr - 1) > 0.4
if __name__ == '__main__':
    ok1 = G1(); ok2 = G2()
    print('VERDICT G1', 'PASS' if ok1 else 'FAIL', '| G2', 'PASS' if ok2 else 'FAIL')
