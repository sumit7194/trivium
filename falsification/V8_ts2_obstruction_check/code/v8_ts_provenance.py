"""V8 extension (for quantum's iahub v2 TS rung 5b): independent TS delta=2 equatorial NVE values.
Independence: (1) the bridge re-derives f and e^{2gamma} from the delta=2 Ernst potential itself (TS2_METRIC.md formulas)
and checks ansatz's g_TT, g_xx, g_yy against them; checks ansatz's omega against the twist equations with the bridge's own
chi (exact rational points); (2) the NVE pieces are built by the bridge's own symbolic code (sympy differentiation),
not quantum's loader. Non-reduced xi1: p = -(A'/A - X'/(2X)), q = A B / X; A = g^yy|0, X = g^xx(-mu2 - V)|0,
B = 1/2 (d2_y g^xx p_x^2 + d2_y V)|0, V = g^tt E^2 - 2 g^tphi E L + g^phiphi L^2, p_t=-E, p_phi=L, H=1/2 g^ab p_a p_b."""
import sympy as sp, json, random
ns = {}; exec(open('v8_nve.py').read().split("def zv():")[0], ns)
x, y, sigma, load = ns['x'], ns['y'], ns['sigma'], ns['load']
def ernst(p, q):
    I = sp.I
    N = p**2*x**4 + q**2*y**4 - 1 - 2*I*p*q*x*y*(x**2 - y**2)
    D = 2*p*x*(x**2 - 1) - 2*I*q*y*(1 - y**2)
    E = (N - D)/(N + D)              # (xi-1)/(xi+1) with xi = N/D
    A = sp.expand(N*sp.conjugate(N) - D*sp.conjugate(D)); B = sp.expand((N + D)*sp.conjugate(N + D))
    f = sp.re(sp.expand_complex(E)); chi = sp.im(sp.expand_complex(E))
    e2g = A/(p**4*(x**2 - y**2)**4)
    return f, chi, e2g, A, B
pts = [sp.Rational(5, 4), sp.Rational(5, 3), sp.Integer(2), sp.Rational(13, 4)]
rows = [(1, 0, 4), (1, 0, 9), (1, 1, 4)]
out = {}; random.seed(42)
for tag, fn, (p_, q_) in [('P1', 'ts2_metric_components_t1o2.txt', (sp.Rational(3, 5), sp.Rational(4, 5))),
                          ('P2', 'ts2_metric_components_t1o3.txt', (sp.Rational(4, 5), sp.Rational(3, 5)))]:
    g = load(fn)
    f, chi, e2g, _, _ = ernst(p_, q_)
    om = g['omega']
    worst = 0
    for _ in range(3):
        pt = {x: sp.Rational(random.randint(1300, 4000), 1000), y: sp.Rational(random.randint(-800, 800), 1000)}
        chk = [g['g_TT'] + f,                                        # g_TT = -f
               g['g_xx'] - e2g*(x**2 - y**2)/(f*(x**2 - 1)),         # sigma = 1
               g['g_yy'] - e2g*(x**2 - y**2)/(f*(1 - y**2)),
               sp.diff(om, x) - (1 - y**2)/f**2*sp.diff(chi, y),     # twist equations, sigma = 1
               sp.diff(om, y) + (x**2 - 1)/f**2*sp.diff(chi, x)]
        worst = max([worst] + [abs(sp.N(c.subs(pt), 40)) for c in chk])
    out[f'{tag}|metric_and_twist_check_max_abs'] = str(worst)
    print(tag, 'metric/twist cross-check max |residual|:', sp.N(worst, 5), flush=True)
    gtt, gtp, gpp, gxx_dn, gyy_dn = g['g_TT'], g['g_Tphi'], g['g_phiphi'], g['g_xx'], g['g_yy']
    det = gtt*gpp - gtp**2
    Gtt, Gtp, Gpp, Gxx, Gyy = gpp/det, -gtp/det, gtt/det, 1/gxx_dn, 1/gyy_dn
    d2 = lambda e: sp.diff(e, y, 2).subs(y, 0)
    Gxx0, Gyy0, Gtt0, Gtp0, Gpp0 = [e.subs(y, 0) for e in (Gxx, Gyy, Gtt, Gtp, Gpp)]
    Gxx2, Gtt2, Gtp2, Gpp2 = d2(Gxx), d2(Gtt), d2(Gtp), d2(Gpp)
    for (E, L, mu2) in rows:
        E, L, mu2 = map(sp.Integer, (E, L, mu2))
        V0 = Gtt0*E**2 - 2*Gtp0*E*L + Gpp0*L**2; V2 = Gtt2*E**2 - 2*Gtp2*E*L + Gpp2*L**2
        px2 = (-mu2 - V0)/Gxx0
        A = Gyy0; X = Gxx0*(-mu2 - V0); B = sp.Rational(1, 2)*(Gxx2*px2 + V2)
        pc = -(sp.diff(A, x)/A - sp.diff(X, x)/(2*X)); qc = A*B/X
        vals = {str(X0): dict(x=str(sp.N(X0, 50)), p=str(sp.N(pc.subs(x, X0), 50)), q=str(sp.N(qc.subs(x, X0), 50)),
                              A=str(sp.N(A.subs(x, X0), 50)), B=str(sp.N(B.subs(x, X0), 50)), X=str(sp.N(X.subs(x, X0), 50))) for X0 in pts}
        out[f'{tag}|E={E},L={L},mu2={mu2}'] = vals
        print(tag, (E, L, mu2), 'p(5/4)=', vals['5/4']['p'][:22], ' q(5/4)=', vals['5/4']['q'][:22], flush=True)
json.dump(out, open('../results/v8_ts_provenance.json', 'w'), indent=1); print('written')
