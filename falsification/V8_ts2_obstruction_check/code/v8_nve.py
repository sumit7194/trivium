"""V8 -- the bridge's own derivation of the equatorial NVE for TS delta=2 and its Kovacic/log analysis.
Imports nothing from quantum. Metric = ansatz's component files (shared data); ZV built here from its standard form.
H = 1/2 g^{ab} p_a p_b, p_T = -E, p_phi = L, mass shell g^{ab}p_a p_b = -mu2.  Gamma: y = 0, p_y = 0.
NVE in (dy, dp_y), independent variable x:  dy'' + a dy' + b dy = 0,
   a = (v^2)'/(2 v^2) - G'/G,  b = c G / v^2,  v = g^{xx} p_x (=dx/dt),  G = g^{yy}|_{y=0},
   c = 1/2 [ d_y^2 g^{xx} p_x^2 + d_y^2 U ]_{y=0},  U = g^{TT}E^2 - 2 g^{Tphi} E L + g^{phiphi} L^2.
Normal form z'' = r z,  r = a^2/4 + a'/2 - b.
"""
import sympy as sp, json, sys, random
from sympy import Symbol, Integer, Rational, Mul, Add, Pow
x = Symbol('x', real=True); y = Symbol('y', real=True); sigma = Symbol('sigma', real=True)
D = '/Users/sumit/Github/conjecture_machine/data/sealed/TS2_for_quantum/'

def load(fn):
    comps = {}
    for line in open(D + fn):
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            comps[k.strip()] = sp.sympify(eval(v.strip(), {'Mul': Mul, 'Add': Add, 'Pow': Pow, 'Integer': Integer,
                'Rational': Rational, 'Symbol': Symbol, 'Float': sp.Float})).subs(sigma, 1)
    return comps

def zv():
    f = ((x - 1)/(x + 1))**2; e2g = ((x**2 - 1)/(x**2 - y**2))**4
    return dict(g_TT=-f, g_Tphi=Integer(0), g_phiphi=(x**2 - 1)*(1 - y**2)/f,
                g_xx=e2g*(x**2 - y**2)/(f*(x**2 - 1)), g_yy=e2g*(x**2 - y**2)/(f*(1 - y**2)))

def vacuum_check(g, npts=3, seed=11):
    X = [Symbol('T'), x, y, Symbol('phi')]
    M = sp.Matrix([[g['g_TT'], 0, 0, g['g_Tphi']], [0, g['g_xx'], 0, 0], [0, 0, g['g_yy'], 0], [g['g_Tphi'], 0, 0, g['g_phiphi']]])
    Mi = M.inv()   # symbolic inverse, cheap: block structure
    dM = [[[sp.diff(M[i, j], X[k]) for k in range(4)] for j in range(4)] for i in range(4)]
    random.seed(seed); worst = 0
    for _ in range(npts):
        pt = {x: Rational(random.randint(1200, 4000), 1000), y: Rational(random.randint(-800, 800), 1000)}
        # Ricci via Christoffels evaluated exactly at the point (needs second derivatives): do it symbolically in x,y then substitute
        Gam = [[[sum(Mi[a, d]*(dM[d][b][c] + dM[d][c][b] - sp.diff(M[b, c], X[d])) for d in range(4))/2
                 for c in range(4)] for b in range(4)] for a in range(4)]
        Gp = [[[sp.nsimplify(Gam[a][b][c].subs(pt)) for c in range(4)] for b in range(4)] for a in range(4)]
        dG = [[[[sp.diff(Gam[a][b][c], X[k]).subs(pt) for k in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
        for b in range(4):
            for c in range(4):
                R = sum(dG[a][b][c][a] - dG[a][b][a][c] for a in range(4)) + \
                    sum(Gp[a][a][d]*Gp[d][b][c] - Gp[a][c][d]*Gp[d][b][a] for a in range(4) for d in range(4))
                worst = max(worst, abs(sp.nsimplify(R)))
    return worst

def nve_r(g, E, L, mu2):
    det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    gTT, gTp, gpp = g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det
    U = gTT*E**2 - 2*gTp*E*L + gpp*L**2
    gxx, gyy = 1/g['g_xx'], 1/g['g_yy']
    even = sp.simplify(sp.together((U - U.subs(y, -y)))) == 0 and sp.simplify(sp.together(gxx - gxx.subs(y, -y))) == 0
    px2 = sp.cancel(sp.together((-mu2 - U.subs(y, 0))/gxx.subs(y, 0)))
    v2 = sp.cancel(sp.together(gxx.subs(y, 0)**2*px2))
    G = sp.cancel(sp.together(gyy.subs(y, 0)))
    c = sp.cancel(sp.together((sp.diff(gxx, y, 2).subs(y, 0)*px2 + sp.diff(U, y, 2).subs(y, 0))/2))
    a = sp.cancel(sp.together(sp.diff(v2, x)/(2*v2) - sp.diff(G, x)/G))
    b = sp.cancel(sp.together(c*G/v2))
    r = sp.cancel(sp.together(a**2/4 + sp.diff(a, x)/2 - b))
    return r, even, v2

def analyse(r):
    num, den = sp.fraction(sp.together(r)); num = sp.Poly(num, x); den = sp.Poly(den, x)
    lc = den.LC(); num = num*(1/lc); den = den.monic()
    ordinf = den.degree() - num.degree()
    fac = sp.factor_list(den.as_expr())[1]
    out = []; alphas_min = 0; ok_all_rational = True
    for gfac, mult in fac:
        gp = sp.Poly(gfac, x); dg = gp.degree()
        entry = dict(factor=str(gfac), degree=dg, pole_order=mult)
        if mult == 2:
            # beta(c) = num(c) / (Q(c) * g'(c)^2), Q = den / g^2 ; test whether beta is one rational for all roots
            Q = sp.Poly(sp.quo(den.as_expr(), gfac**2, x), x)
            P = num; gd = gp.diff(x)
            # beta rational beta0 iff P - beta0*Q*gd^2 == 0 mod g ; find beta0 from one root numerically, verify exactly
            root = sp.Poly(gfac, x).nroots(n=40)[0]
            b0n = sp.N(P.as_expr().subs(x, root)/(Q.as_expr().subs(x, root)*gd.as_expr().subs(x, root)**2), 30)
            b0 = sp.nsimplify(sp.re(b0n), rational=True, tolerance=1e-20)
            exact = sp.rem((P - b0*Q*gd**2).as_expr(), gfac, x) == 0
            entry.update(beta=str(b0), beta_exact_all_roots=bool(exact))
            if not exact: ok_all_rational = False
            disc = 1 + 4*b0
            s = sp.sqrt(disc)
            entry['exponent_difference'] = str(s)
            alphas = (Rational(1, 2) - s/2, Rational(1, 2) + s/2)
            entry['alphas'] = [str(al) for al in alphas]
            alphas_min += dg*min(alphas)
        elif mult == 1:
            entry['alphas'] = ['1']; alphas_min += dg*1
        else:
            entry['note'] = 'pole order >2'; ok_all_rational = False
        out.append(entry)
    return dict(poles=out, order_at_inf=ordinf, sum_alpha_min=str(alphas_min), all_double_rational=ok_all_rational)

def log_at_zero(r, nterms=4):
    # Frobenius at x=0 for z'' = r z with a double pole: r = sum rk x^(k-2)
    ser = sp.series(r*x**2, x, 0, nterms).removeO()
    rk = [ser.coeff(x, k) for k in range(nterms)]
    r0 = rk[0]; s = sp.sqrt(1 + 4*r0); rho = Rational(1, 2) - s/2; N = s
    if not (N.is_integer and N > 0):
        return dict(r0=str(r0), N=str(N), log='no integer exponent difference')
    N = int(N); cfs = [Integer(1)]
    for n in range(1, N + 1):
        rhs = sum(rk[k]*cfs[n - k] for k in range(1, n + 1))
        lhs = (rho + n)*(rho + n - 1) - r0
        if n < N: cfs.append(sp.simplify(rhs/lhs))
        else: obstruction_term = sp.simplify(rhs)
    return dict(r0=str(r0), N=N, log_coefficient=str(obstruction_term), log_present=bool(obstruction_term != 0))

def verdict(an, logz, ordinf):
    alinf_max = 1 if ordinf > 2 else None
    if alinf_max is None: return 'INCONCLUSIVE (order at infinity <= 2: not handled here)'
    if not an['all_double_rational']: return 'INCONCLUSIVE (a factor with non-rational exponents or higher pole)'
    case1_possible = alinf_max - sp.Rational(an['sum_alpha_min']) >= 0
    if logz.get('log_present') and not case1_possible: return 'OBSTRUCTION (log point excludes cases 2,3; case 1 fails the exponent count)'
    if not logz.get('log_present'): return 'NO-OBSTRUCTION-FOUND (no log point at 0)'
    return 'NOT OBSTRUCTED BY THIS ROUTE (case-1 count survives)'

rows = [(1, 0, 4), (1, 0, 9), (1, 1, 4)]
targets = [('ZV_delta2_control', None), ('KERR_control_t1o2', 'ts2_KERR_metric_components_t1o2.txt'),
           ('TS2_P1_t1o2', 'ts2_metric_components_t1o2.txt'), ('TS2_P2_t1o3', 'ts2_metric_components_t1o3.txt')]
results = {}
for name, fn in targets:
    g = zv() if fn is None else load(fn)
    vac = vacuum_check(g) if '--vacuum' in sys.argv else 'skipped'
    for E, L, mu2 in rows:
        r, even, v2 = nve_r(g, Integer(E), Integer(L), Integer(mu2))
        an = analyse(r); lz = log_at_zero(r)
        v = verdict(an, lz, an['order_at_inf'])
        results[f'{name}|{E},{L},{mu2}'] = dict(even_in_y=even, vacuum_max_abs_R=str(vac), analysis=an, log_at_0=lz, verdict=v)
        print(f'{name:18s} (E,L,mu2)=({E},{L},{mu2})  even={even}  ord_inf={an["order_at_inf"]}  sum_alpha_min={an["sum_alpha_min"]}  '
              f'log0={lz.get("log_present", lz.get("log"))}  -> {v}')
        for p in an['poles']: print('     ', p)
json.dump(results, open('../results/v8_results.json', 'w'), indent=1, default=str)
