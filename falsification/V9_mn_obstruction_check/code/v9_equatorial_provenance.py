"""V9 extension (for quantum's iahub v2 ladder rung 5b, equation provenance): the bridge's OWN equatorial NVE for MN,
non-reduced xi1 form in x:  xi1'' + p xi1' + q xi1 = 0,
  p = -(A'/A - X'/(2X)),  q = A*B/X,
  A = g^yy|_{y=0},  B = d^2_y H|_{y=0,p_y=0} with p_x^2 eliminated by H = -mu2/2,  X = g^xx (-mu2 - V)|_{y=0},
  V = g^tt E^2 - 2 g^tphi E L + g^phiphi L^2  (p_t = -E, p_phi = L),  H = 1/2 g^{ab} p_a p_b.
Method: sympy SYMBOLIC differentiation (quantum's Q2 reference used mpmath numerical differentiation, so the methods
differ), evaluated with evalf at 50 digits. Metric functions: the bridge's own transcription (v9_nve.mn_functions,
verified against ansatz's srepr to 1e-15). On y=0 the branch R = x*sqrt(1-1/x^2) = principal sqrt(x^2-1) for real x>1."""
import sympy as sp, json
from v9_nve import mn_functions, x, y
pts = [sp.Rational(5, 4), sp.Rational(5, 3), sp.Integer(2), sp.Rational(13, 4)]   # 1.6667 taken as 5/3 exactly
rows = [(1, 0, 4), (1, 0, 9), (1, 1, 4)]
out = {}
for tag, (M, a_, beta) in [('p1', (5, 3, sp.Rational(1, 5))), ('p2', (13, 5, sp.Rational(-1, 3)))]:
    F = mn_functions(M, a_, beta); f, om, e2g, k = F['f'], F['om'], F['e2g'], F['k']
    gtt = -f; gtp = f*om; gpp = -f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2)
    gxx_dn = k**2/f*e2g*(x**2 - y**2)/(x**2 - 1); gyy_dn = k**2/f*e2g*(x**2 - y**2)/(1 - y**2)
    det = gtt*gpp - gtp**2
    Gtt, Gtp, Gpp = gpp/det, -gtp/det, gtt/det
    Gxx, Gyy = 1/gxx_dn, 1/gyy_dn
    # evenness check (first y-derivatives vanish on y=0) at one point
    ev = max(abs(sp.N(sp.diff(e, y).subs(y, 0).subs(x, sp.Rational(9, 5)), 30)) for e in (Gxx, Gtt, Gtp, Gpp))
    d2 = lambda e: sp.diff(e, y, 2).subs(y, 0)
    Gxx0, Gyy0, Gtt0, Gtp0, Gpp0 = [e.subs(y, 0) for e in (Gxx, Gyy, Gtt, Gtp, Gpp)]
    Gxx2, Gtt2, Gtp2, Gpp2 = d2(Gxx), d2(Gtt), d2(Gtp), d2(Gpp)
    for (E, L, mu2) in rows:
        E, L, mu2 = map(sp.Integer, (E, L, mu2))
        V0 = Gtt0*E**2 - 2*Gtp0*E*L + Gpp0*L**2
        V2 = Gtt2*E**2 - 2*Gtp2*E*L + Gpp2*L**2
        px2 = (-mu2 - V0)/Gxx0
        A = Gyy0; X = Gxx0*(-mu2 - V0); B = sp.Rational(1, 2)*(Gxx2*px2 + V2)
        p = -(sp.diff(A, x)/A - sp.diff(X, x)/(2*X)); q = A*B/X
        vals = {}
        for X0 in pts:
            vals[str(X0)] = dict(x=str(sp.N(X0, 50)), p=str(sp.N(p.subs(x, X0), 50)), q=str(sp.N(q.subs(x, X0), 50)),
                                 A=str(sp.N(A.subs(x, X0), 50)), B=str(sp.N(B.subs(x, X0), 50)), X=str(sp.N(X.subs(x, X0), 50)))
        out[f'{tag}|E={E},L={L},mu2={mu2}'] = vals
        print(tag, (E, L, mu2), 'p(5/4)=', vals['5/4']['p'][:22], ' q(5/4)=', vals['5/4']['q'][:22], flush=True)
    out[f'{tag}|evenness_max_abs_dy'] = str(ev)
    print(tag, 'evenness check max|d_y g^..| at y=0:', ev, flush=True)
json.dump(out, open('../results/v9_equatorial_provenance.json', 'w'), indent=1)
print('written ../results/v9_equatorial_provenance.json')
