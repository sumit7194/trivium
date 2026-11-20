"""V25 P1: near-axis rho^2 / rho^4 coefficients of F1 = f e^{-2gamma}, F2 = 1/f - f omega^2/rho^2 for TS (twisting),
Kerr (twisting) and ZV (static), against (i) twist-free rho^2 formulas, (ii) own static-Weyl rho^4 series + the claimed
twist term -(c0'')^2/(64 f0) [F1] and -(c0'')^2/(64 f0^3) [F2]. Bridge metrics only."""
import sys, os, json
import sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
V11 = os.path.join(HERE, '../../V11_chaos_reproduction/code'); sys.path.insert(0, V11)
_c = os.getcwd(); os.chdir(V11); import v11_chaos as V; os.chdir(_c)
X, Y = V.X, V.Y; z = sp.symbols('z', real=True)
mp.mp.dps = 50

# ---- own static Weyl series, in terms of f0 and its derivatives
f0s = sp.Function('f0')(z); rho2 = sp.symbols('t')   # t = rho^2
a0 = sp.log(f0s)/2; a1 = -sp.diff(a0, z, 2)/4; a2 = sp.diff(a0, z, 4)/64
g1 = -sp.diff(a0, z)**2/2; g2 = (4*a1**2 - 2*sp.diff(a0, z)*sp.diff(a1, z))/4
psi = a0 + a1*rho2 + a2*rho2**2; gam = g1*rho2 + g2*rho2**2
F1s = sp.series(sp.exp(2*psi - 2*gam), rho2, 0, 3).removeO(); F2s = sp.series(sp.exp(-2*psi), rho2, 0, 3).removeO()
F1_2s, F1_4s = sp.simplify(F1s.coeff(rho2, 1)), sp.simplify(F1s.coeff(rho2, 2))
F2_2s, F2_4s = sp.simplify(F2s.coeff(rho2, 1)), sp.simplify(F2s.coeff(rho2, 2))
# sanity: rho^2 static coefficients vs the claimed twist-free formulas (symbolic)
d = lambda n: sp.diff(f0s, z, n)
chk2a = sp.simplify(F1_2s - (-d(2)/4 + d(1)**2/(2*f0s))); chk2b = sp.simplify(F2_2s - (f0s*d(2) - d(1)**2)/(4*f0s**3))
print('static rho^2 symbolic vs claimed:', chk2a, chk2b, flush=True)

def ernst(case):
    if case == 'ts45':
        p, q = sp.Rational(4, 5), sp.Rational(3, 5)
        xi = (p**2*X**4 + q**2*Y**4 - 1 - 2*sp.I*p*q*X*Y*(X**2 - Y**2))/(2*p*X*(X**2 - 1) - 2*sp.I*q*Y*(1 - Y**2))
    elif case == 'kerr45':
        p, q = sp.Rational(4, 5), sp.Rational(3, 5); xi = p*X - sp.I*q*Y
    elif case == 'zv':
        return ((z - 1)/(z + 1))**2, sp.Integer(0)
    Ez = sp.simplify(((xi - 1)/(xi + 1)).subs({X: z, Y: 1}))
    return sp.simplify(sp.re(sp.expand_complex(Ez))), sp.simplify(sp.im(sp.expand_complex(Ez)))

def run(case, zvals):
    os.chdir(V11); g = V.get_metric(case); os.chdir(_c)
    f0, c0 = ernst(case)
    f0m = -g['g_TT'].subs(Y, 1)
    axis_ok = sp.simplify(f0 - f0m) == 0
    G = sp.lambdify((X, Y), [g['g_TT'], g['g_Tphi'], g['g_xx']], 'mpmath')
    def F12(r, zz):
        Rp, Rm = mp.sqrt(r*r + (zz + 1)**2), mp.sqrt(r*r + (zz - 1)**2)
        x, y = (Rp + Rm)/2, (Rp - Rm)/2
        gtt, gtp, gxx = G(x, y); f = -gtt
        e2g = f*gxx*(x*x - 1)/(x*x - y*y)
        return f/e2g, 1/f - gtp**2/(f*r*r)
    res = {'axis_f0_matches_metric': bool(axis_ok)}
    for zz in zvals:
        zz = mp.mpf(zz)
        def coeffs(npts):
            rs = [mp.mpf('1e-3') + (mp.mpf('1e-2') - mp.mpf('1e-3'))*i/(npts - 1) for i in range(npts)]
            out = []
            for which in (0, 1):
                tm = mp.mpf('1e-4')   # scale t = rho^2 by its max to keep the Vandermonde well conditioned
                A = mp.matrix([[(r*r/tm)**j for j in range(7)] for r in rs]); b = mp.matrix([F12(r, zz)[which] for r in rs])
                sol = mp.qr_solve(A, b)[0]; out.append((sol[0], sol[1]/tm, sol[2]/tm**2))
            return out
        cA, cB = coeffs(12), coeffs(16)
        gate = max(abs(cA[w][k]/cB[w][k] - 1) for w in (0, 1) for k in (1, 2))
        sub = {sp.Derivative(f0s, (z, n)): sp.diff(f0, z, n) for n in range(1, 5)}
        ev = lambda e: mp.mpf(sp.N(e.subs(sub).subs(f0s, f0).subs(z, zz), 60))
        f0v = ev(f0s); c2 = mp.mpf(sp.N(sp.diff(c0, z, 2).subs(z, zz), 60))
        F1_2, F1_4 = cB[0][1], cB[0][2]; F2_2, F2_4 = cB[1][1], cB[1][2]
        r = dict(gate=float(gate), F1_0_rel=float(abs(cB[0][0]/f0v - 1)),
                 F1_2_rel=float(abs(F1_2/ev(F1_2s) - 1)), F2_2_rel=float(abs(F2_2/ev(F2_2s) - 1)))
        tw1 = -c2**2/(64*f0v); tw2 = -c2**2/(64*f0v**3)
        r['F1_4_minus_static'] = float(F1_4 - ev(F1_4s)); r['F2_4_minus_static'] = float(F2_4 - ev(F2_4s))
        r['pred_twist_F1'] = float(tw1); r['pred_twist_F2'] = float(tw2)
        if c2 != 0:
            r['ratio_F1'] = float((F1_4 - ev(F1_4s))/tw1); r['ratio_F2'] = float((F2_4 - ev(F2_4s))/tw2)
            r['NEG_ratio_F1_with_1.1c0pp'] = float((F1_4 - ev(F1_4s))/(tw1*mp.mpf('1.21')))
        res[str(zz)] = r; print(case, zz, r, flush=True)
    return res

out = {'static_rho2_symbolic_check': [str(chk2a), str(chk2b)]}
for case in ('ts45', 'kerr45', 'zv'):
    out[case] = run(case, ['2.5', '4', '7'])
json.dump(out, open(os.path.join(HERE, '../results/v25_p1.json'), 'w'), indent=1, default=str)
