"""V9 (for quantum's iahub v2 rung 5b, AXIAL): the bridge's own axial MN NVE pieces (v9_nve.axial_r, symbolic sympy),
non-reduced xi1 coefficients p = -(A'/A - X'/(2X)), q = A*B/X, plus A, B, X, at 50 digits.
A = g^thth|0, B = -d_y H|_{y=1} (= d^2_theta H at theta=0; omega^2/(1-y^2) limit taken analytically), X = g^xx(-mu2 - V)|_{y=1},
H = 1/2 g^{ab}p_a p_b, p_t = -E, L = 0, H = -mu2/2.  On the axis R = x (branch x*sqrt(1+(y^2-1)/x^2))."""
import sympy as sp, json
from v9_nve import axial_r, x
pts = [sp.Rational(5, 4), sp.Rational(5, 3), sp.Integer(2), sp.Rational(13, 4)]
out = {}
for tag, (M, a_, beta) in [('p1', (5, 3, sp.Rational(1, 5))), ('p2', (13, 5, sp.Rational(-1, 3)))]:
    for (E, mu2) in [(1, 4), (1, 9)]:
        ax = axial_r(M, a_, beta, sp.Integer(E), sp.Integer(mu2)); A, B, X = ax['A'], ax['B'], ax['xdot2']
        p = -(sp.diff(A, x)/A - sp.diff(X, x)/(2*X)); q = A*B/X
        vals = {str(X0): dict(x=str(sp.N(X0, 50)), p=str(sp.N(p.subs(x, X0), 50)), q=str(sp.N(q.subs(x, X0), 50)),
                              A=str(sp.N(A.subs(x, X0), 50)), B=str(sp.N(B.subs(x, X0), 50)), X=str(sp.N(X.subs(x, X0), 50))) for X0 in pts}
        out[f'{tag}|E={E},L=0,mu2={mu2}'] = vals
        print(tag, (E, 0, mu2), 'p(5/4)=', vals['5/4']['p'][:22], ' q(5/4)=', vals['5/4']['q'][:22], flush=True)
json.dump(out, open('../results/v9_axial_provenance.json', 'w'), indent=1); print('written')
