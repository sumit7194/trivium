"""V26 addendum E: Bridge checks of Gemini Neon T3: E1 Class D degree classification; E2 ZV delta=2 equatorial NVE1."""
import random, itertools, sympy as sp
z, x, y, px, py = sp.symbols('z x y p_x p_y')

# ---------------- E1 ----------------
def rand_poly(deg, rng, monic=False):
    cs = [sp.Rational(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(deg + 1)]
    if monic: cs[0] = 1
    while cs[0] == 0: cs[0] = sp.Rational(rng.randint(1, 4))
    return sp.Poly(cs, z).as_expr()

def actual_degree(c0, M=1):
    f0 = 1 - 2*M/z
    fm = sp.cancel(sp.together(f0/(f0**2 + c0**2)))
    return sp.degree(sp.denom(fm), z)

def claimed(case, d, p2m, swap=False, nocorr=False):
    if case == 'schw': return 1
    if case == 'nut': return 2
    corr = 0 if nocorr else (1 if p2m else 0)
    if case == 'k0': return (2*d if swap else 2*(d + 1)) - corr
    return (2*(d + 1) if swap else 2*d) - corr

def E1(seed=7):
    rng = random.Random(seed); rows = []
    rows.append(('schw', 0, False, sp.Integer(0))); rows.append(('nut', 1, False, -sp.Rational(6, 5)/z))
    while len(rows) < 62:
        case = rng.choice(['k0', 'k1'])
        if case == 'k0':
            d = rng.randint(1, 3); Q = rand_poly(d, rng, True)
            if Q.subs(z, 0) == 0: continue
        else:
            k = rng.randint(1, 2); m = rng.randint(0, 2); d = k + m
            Q = z**k*(rand_poly(m, rng, True) if m else 1)
            if m and sp.Poly(sp.expand(Q/z**k), z).eval(0) == 0: continue
        p2m = rng.random() < 0.4 and d >= 2
        if p2m: P = (z - 2)*rand_poly(rng.randint(0, d - 2), rng)
        else:
            P = rand_poly(rng.randint(0, d - 1), rng)
            if P.subs(z, 2) == 0: continue
        if sp.gcd(sp.Poly(P, z), sp.Poly(Q, z)).degree() > 0: continue
        if case == 'k1' and P.subs(z, 0) == 0: continue
        rows.append((case, d, p2m, sp.expand(P)/sp.expand(Q)))
    ok = True; ctrl_mismatch = 0; mind = 99
    for case, d, p2m, c0 in rows:
        a = actual_degree(c0)
        good = a == claimed(case, d, p2m)
        ok &= good
        is_nut = sp.simplify(c0*z).is_constant() and c0 != 0      # amendment E-a: c0 = c/z IS Taub-NUT (prereg excludes it)
        if case not in ('schw', 'nut') and not is_nut: mind = min(mind, a)
        if a != claimed(case, d, p2m, swap=True) or a != claimed(case, d, p2m, nocorr=True): ctrl_mismatch += 1
        if not good: print('E1 MISMATCH', case, d, p2m, c0, a, claimed(case, d, p2m))
    print('E1: %d examples, all match claimed degrees: %s; min degree (non-Schw/NUT) = %d; control mismatches = %d'
          % (len(rows), ok, mind, ctrl_mismatch))
    print('E1 case counts:', {c: sum(1 for r in rows if r[0] == c and r[2] == p) for c in ('k0', 'k1') for p in (False, True)} if False else
          [(c, p, sum(1 for r in rows if r[0] == c and r[2] == p)) for c in ('k0', 'k1') for p in (False, True)])
    return ok and mind >= 3 and ctrl_mismatch > 0

# ---------------- E2 ----------------
def nve_r(delta, E=2, mu=1):
    f = ((x - 1)/(x + 1))**delta
    e2g = ((x**2 - 1)/(x**2 - y**2))**(delta**2)
    H = sp.Rational(1, 2)*(-E**2/f + f/e2g/(x**2 - y**2)*((x**2 - 1)*px**2 + (1 - y**2)*py**2))
    a = sp.diff(H, y, 2).subs({y: 0, py: 0}); b = sp.diff(H, py, 2).subs({y: 0, py: 0})
    H0 = H.subs({y: 0, py: 0})
    px2 = sp.solve(sp.Eq(H0, -sp.Rational(mu**2, 2)), px**2)[0]
    xdot2 = sp.cancel((sp.diff(H0, px)**2).subs(px**2, px2))
    a = sp.cancel(a.subs(px**2, px2))
    # Y' = (b/xdot) P, P' = -(a/xdot) Y  =>  Y'' - (g'/g) Y' + (a b / xdot^2) Y = 0, g = b/xdot
    glog = sp.cancel(sp.diff(b, x)/b - sp.diff(xdot2, x)/(2*xdot2))
    p = -glog; q = sp.cancel(a*b/xdot2)
    return sp.factor(sp.cancel(p**2/4 + sp.diff(p, x)/2 - q))

def kovacic_case1(r):
    num, den = sp.fraction(sp.cancel(r)); den_p = sp.Poly(den, x)
    poles = sp.roots(den_p)
    assert sum(poles.values()) == den_p.degree(), 'non-rational poles'
    exps = []
    for c, mult in poles.items():
        assert mult <= 2
        if mult == 1: exps.append((c, [sp.Integer(1)]))
        else:
            bc = sp.limit((x - c)**2*r, x, c)
            s = sp.sqrt(1 + 4*bc); exps.append((c, list({sp.Rational(1, 2) + s/2, sp.Rational(1, 2) - s/2})))
    ordinf = den_p.degree() - sp.Poly(num, x).degree()
    if ordinf > 2: einf = [sp.Integer(0), sp.Integer(1)]
    elif ordinf == 2:
        binf = sp.limit(x**2*r, x, sp.oo); s = sp.sqrt(1 + 4*binf); einf = list({sp.Rational(1, 2) + s/2, sp.Rational(1, 2) - s/2})
    else: raise ValueError('irregular at infinity')
    found = []; tried = 0
    for choice in itertools.product(*[e for _, e in exps]):
        for ei in einf:
            dd = sp.nsimplify(ei - sum(choice))
            if not (dd.is_integer and dd >= 0): continue
            tried += 1; dd = int(dd)
            th = sum(al/(x - c) for (c, _), al in zip(exps, choice))
            cs = sp.symbols('a0:%d' % (dd + 1)) if dd > 0 else ()
            P = x**dd + sum(cs[i]*x**i for i in range(dd))
            expr = sp.together(sp.diff(P, x, 2) + 2*th*sp.diff(P, x) + (sp.diff(th, x) + th**2 - r)*P)
            nm = sp.Poly(sp.expand(sp.numer(expr)), x)
            sol = sp.solve(nm.coeffs(), cs[:dd], dict=True) if dd > 0 else ([{}] if nm.is_zero else [])
            if dd == 0 and nm.is_zero: found.append((choice, ei, 0))
            elif dd > 0 and sol: found.append((choice, ei, dd))
    return tried, found

def frob_obstruction(r, c=0):
    s = sp.series(sp.cancel((x - c)**2*r), x, c, 4).removeO()
    cc = [sp.nsimplify(s.coeff(x - c, k) if c else s.coeff(x, k)) for k in range(4)]
    roots = sorted(sp.solve(sp.Symbol('t')*(sp.Symbol('t') - 1) - cc[0], sp.Symbol('t')))
    rho = roots[0]; diff = roots[1] - roots[0]
    return cc, roots, diff

def E2():
    neon = 3*(50*x**6 + 292*x**5 + 197*x**4 - 452*x**3 - 328*x**2 - 24*x + 9)/(4*x**2*(x - 1)**2*(x + 1)**2*(x + 3)**2*(3*x + 1)**2)
    r2 = nve_r(2)
    same = sp.simplify(r2 - neon) == 0
    print('E2 Bridge r(x) for ZV delta=2:', r2); print('E2 equals Neon r(x):', same)
    cc, roots, dfr = frob_obstruction(r2)
    obstruction = cc[1]*(-cc[1]) + cc[2] if dfr == 2 else None   # a1 = c1/((rho+1)rho - c0) = -c1 for rho=-1/2, c0=3/4
    # general: a1 = c1 / ((rho+1)*rho - c0)
    rho = roots[0]; a1 = cc[1]/((rho + 1)*rho - cc[0]); obs = sp.nsimplify(cc[1]*a1 + cc[2])
    print('E2 x=0: x^2 r = %s + %s x + %s x^2 ...; exponents %s; obstruction %s' % (cc[0], cc[1], cc[2], roots, obs))
    tried, found = kovacic_case1(r2)
    print('E2 Kovacic case 1 (ZV2): candidate exponent sets with integer d>=0:', tried, '| solutions:', found)
    r1 = nve_r(1)
    print('E2 control Schwarzschild delta=1 r(x):', r1)
    t1, f1 = kovacic_case1(r1) if r1 != 0 else (0, ['r=0 trivially reducible'])
    print('E2 control Kovacic case 1 (Schw): tried', t1, '| solutions:', f1)
    return same and obs != 0 and not found and bool(f1)

if __name__ == '__main__':
    ok1 = E1(); ok2 = E2()
    print('VERDICT E1', 'PASS' if ok1 else 'FAIL', '| E2', 'PASS' if ok2 else 'FAIL')
