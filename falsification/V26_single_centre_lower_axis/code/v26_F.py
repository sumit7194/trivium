"""V26 addendum F: check Neon T8's first-order proof. F1: delta-c0 closed form and I+ (independent ray integrals);
F2: first-order prediction of tr(g_in)-2 = c k^2 on |z|=1.35, E=0.8, vs the V26-D ODE value."""
import sympy as sp, mpmath as mp, numpy as np, cmath, math
from scipy.integrate import solve_ivp
z = sp.symbols('z'); I = sp.I
a = sp.Rational(3, 5); b = sp.sqrt(3)/5
D = z**2 + a**2; cK = -2*a/D; cK2 = sp.diff(cK, z, 2); v = (z + I*a)/(z - I*a)
Q = v**3 + v**-3 - sp.Rational(3, 5)*(v + 1/v) - sp.Rational(4, 5)
dc2 = sp.cancel(Q/(2*D**3*cK2))                                   # delta c0''
neon_dc0 = 15/(4*(25*z**2 + 9)) + 5*sp.sqrt(3)/48*z*sp.log((z + b)/(z - b)) + 5/(48*I)*z*sp.log((z + I*a)/(z - I*a)) \
           + sp.Rational(1, 16)*sp.log((z**2 - b**2)/(z**2 + a**2))
# F2 per prereg uses the independently verified delta-c0 (ray integrals). Implemented via the sign-corrected closed form
# (5i/48 in place of Neon's 5/(48i)), shown identical to the ray integrals to 1e-32 and exactly satisfying dc0'' (results/v26_F_diagnosis.txt).
true_dc0 = 15/(4*(25*z**2 + 9)) + 5*sp.sqrt(3)/48*z*sp.log((z + b)/(z - b)) + 5*I/48*z*sp.log((z + I*a)/(z - I*a)) \
           + sp.Rational(1, 16)*sp.log((z**2 - b**2)/(z**2 + a**2))
neon_nolog = 15/(4*(25*z**2 + 9)) + sp.Rational(1, 16)*sp.log((z**2 - b**2)/(z**2 + a**2))

def F1():
    mp.mp.dps = 30
    f2 = sp.lambdify(z, dc2, 'mpmath')
    ray0 = lambda zz: zz**2*mp.quad(lambda s: (s - 1)*f2(zz*s), [1, 2, 10, mp.inf])
    ray1 = lambda zz: -zz*mp.quad(lambda s: f2(zz*s), [1, 2, 10, mp.inf])
    nf = sp.lambdify(z, neon_dc0, 'mpmath'); nl = sp.lambdify(z, neon_nolog, 'mpmath')
    worst = 0; worst_nolog = 0
    for j in range(8):
        zz = mp.mpf(1.35)*mp.expj(2*mp.pi*j/8 + 0.1)
        r = ray0(zz); worst = max(worst, abs(r - nf(zz))); worst_nolog = max(worst_nolog, abs(r - nl(zz)))
    print('F1 delta-c0: max |ray - Neon closed form| on circle = %.2e ; no-log control = %.2e' % (worst, worst_nolog))
    # I+ and I- by quadrature, delta-c0 and its derivative by rays (independent of Neon's closed form)
    f0 = 1 - 1/(z - I*a) - 1/(z + I*a); g = sp.cancel(2*f0*cK/(f0**2 + cK**2)**2); fm = sp.cancel(f0/(f0**2 + cK**2))
    gl, gpl, fmp = [sp.lambdify(z, e, 'mpmath') for e in (g, sp.diff(g, z), sp.diff(fm, z))]
    def integrand(th, sgn):
        zz = mp.mpf(1.35)*mp.expj(th); dz = 1j*zz
        dP1 = gpl(zz)*ray0(zz) + gl(zz)*ray1(zz)
        return fmp(zz)*dP1*(zz - 2 - sgn*1j*a)**2*dz
    mp.mp.dps = 20
    Ip = mp.quad(lambda th: integrand(th, 1), [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])
    Im = mp.quad(lambda th: integrand(th, -1), [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])
    neonI = mp.mpc('-0.0243361820944768', '0.0232300689610870')
    rel = abs(Ip - neonI)/abs(neonI); sym = abs(Im + mp.conj(Ip))
    print('F1 I+ (Bridge) =', mp.nstr(Ip, 16), '| rel diff to Neon %.2e | |I- + conj(I+)| = %.2e' % (rel, sym))
    return worst <= 1e-15 and worst_nolog > 1e-3 and rel <= 1e-10 and sym <= 1e-12

def F2(E=0.8, wrong=False):
    # symbolic: check closed-form identities, then numerics in double precision
    f0 = 1 - 1/(z - I*a) - 1/(z + I*a); fm = sp.cancel(f0/(f0**2 + cK**2))
    Dm = (z - 2)**2 + a**2; Nm = (E**2 - 1)*Dm - 2*(z - 2)
    P0 = sp.nsimplify(E)**2 - fm
    ok_P0 = sp.simplify(P0 - sp.nsimplify(Nm/Dm)) == 0
    ND = sp.expand(sp.nsimplify(Nm*Dm)); k2 = -a**2*(sp.nsimplify(E)**2 - 1)
    q0 = sp.Rational(3, 16)*(sp.diff(P0, z)/P0)**2
    ident = sp.diff(sp.diff(ND, z)/ND, z)/4 + (sp.diff(ND, z)/ND)**2/16 + k2/ND + q0
    ok_v = sp.simplify(sp.cancel(ident)) == 0
    print('F2 symbolic: P0 == N-/D- : %s ; v+- = (ND)^(1/4) e^(+-kappa u) solves NVE with kappa^2=-a^2(E^2-1): %s' % (ok_P0, ok_v))
    dP = sp.cancel(2*f0*cK/(f0**2 + cK**2)**2)*true_dc0
    if wrong: q1 = sp.Rational(3, 16)*sp.diff(dP/P0, z)**2
    else: q1 = sp.Rational(3, 8)*(sp.diff(P0, z)/P0)*sp.diff(dP/P0, z)
    q1f = sp.lambdify(z, q1, 'numpy')
    coeffs = [complex(c) for c in sp.Poly(ND, z).all_coeffs()]
    roots = np.roots(coeffs); s0 = np.sqrt(complex(np.polyval(coeffs, 0)))
    sfun = lambda zz: s0*np.prod([np.sqrt(1 - zz/r) for r in roots])
    kap = np.sqrt(complex(k2)); r0 = 1.35
    def rhs(th, Y):
        zz = r0*np.exp(1j*th); dz = 1j*zz; s = sfun(zz); u = Y[0]
        vp2 = s*np.exp(2*kap*u); vm2 = s*np.exp(-2*kap*u); vpm = s
        q = q1f(zz)
        return [dz/s, q*vpm*dz, q*vm2*dz, q*vp2*dz]
    sol = solve_ivp(rhs, (0, 2*np.pi), np.zeros(4, dtype=complex), method='DOP853', rtol=1e-12, atol=1e-15)
    u, J0, Jm, Jp = sol.y[:, -1]
    c_pred = -(Jp*Jm - J0**2)/(4*kap**2)
    print('F2 %s: min|root| %.4f, u returns %.1e, J0 %s, J+ %s, J- %s, c_pred = %s'
          % ('WRONG-q1 control' if wrong else 'Neon q1', min(abs(roots)), abs(u), J0, Jp, Jm, c_pred))
    return ok_P0 and ok_v, c_pred

if __name__ == '__main__':
    ok1 = F1()
    okS, c = F2(); _, cw = F2(wrong=True)
    target = -4.78447e-3
    rel = abs(c/target - 1); relw = abs(cw/target - 1)
    print('F2 c_pred/target - 1 = %.2e (PASS <= 1e-3) | control miss %.2e (must be > 1e-2)' % (rel, relw))
    ok2 = okS and rel <= 1e-3 and relw > 1e-2
    print('VERDICT F1', 'PASS' if ok1 else 'FAIL', '| F2', 'PASS' if ok2 else 'FAIL')
