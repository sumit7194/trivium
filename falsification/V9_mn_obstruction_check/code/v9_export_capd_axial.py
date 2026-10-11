"""Export the bridge's own exact MN AXIAL NVE coefficients (V9 axial derivation, v9_nve.axial_r) for quantum's CAPD third
replay. Variable x on the axis (y = 1, L = 0). Form: non-reduced xi1, y'' + p y' + q y = 0 with
p = -(A'/A - (xdot2)'/(2 xdot2)), q = A B / xdot2 (exactly v9_nve.axial_r's p and q). The single exponential basis
E1 = exp(w1), w1 = 2 beta / x^3 (quantum's basis); every exp atom must be an integer multiple of w1 (checked exactly).
Usage: python v9_export_capd_axial.py   (exports p1/p2 x mu2 = 4, 9 at E = 1)"""
import os, json, time, random, subprocess
import sympy as sp, mpmath as M
from v9_nve import axial_r, x

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../export_capd')
CASES = [('p1', 5, 3, sp.Rational(1, 5), 1, 4), ('p1', 5, 3, sp.Rational(1, 5), 1, 9),
         ('p2', 13, 5, sp.Rational(-1, 3), 1, 4), ('p2', 13, 5, sp.Rational(-1, 3), 1, 9)]

def to_rational(e, w, E1):
    m = {}
    for a in e.atoms(sp.exp):
        r = sp.cancel(sp.together(a.args[0])/w)
        assert r.is_Integer, f'exp argument not an integer multiple of w1: {a.args[0]}'
        m[a] = E1**int(r)
    n, d = sp.fraction(sp.together(e.xreplace(m)))
    N = sp.Poly(sp.expand(n), x, E1); D = sp.Poly(sp.expand(d), x, E1)
    g = sp.gcd(N, D); return sp.div(N, g)[0], sp.div(D, g)[0], int(g.total_degree())

monos = lambda P: [[list(map(int, m)), f'{sp.Rational(c).p}/{sp.Rational(c).q}'] for m, c in zip(P.monoms(), P.coeffs())]

if __name__ == '__main__':
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    E1 = sp.Symbol('E1', positive=True); os.makedirs(OUT, exist_ok=True)
    for tag, Mm, a_, beta, E, mu2 in CASES:
        t0 = time.time(); ax = axial_r(Mm, a_, beta, sp.Integer(E), sp.Integer(mu2))
        A, B, xd2 = ax['A'], ax['B'], ax['xdot2']
        p = -(sp.diff(A, x)/A - sp.diff(xd2, x)/(2*xd2)); q = A*B/xd2
        half = [s for s in (p + q).atoms(sp.Pow) if s.exp.is_Rational and s.exp.q == 2 and s.base.has(x)]
        assert not half, f'square roots survive: {half[:2]}'
        w = 2*beta/x**3
        Pn, Pd, gp = to_rational(p, w, E1); Qn, Qd, gq = to_rational(q, w, E1)
        M.mp.dps = 40; rng = random.Random(29); worst = M.mpf(0)
        fo = [sp.lambdify(x, e, 'mpmath') for e in (p, q)]
        fr = [sp.lambdify((x, E1), N.as_expr()/D.as_expr(), 'mpmath') for N, D in ((Pn, Pd), (Qn, Qd))]
        for _ in range(12):
            z = M.mpc(rng.uniform(1.2, 4), rng.uniform(-2, 2)); e1 = M.exp(2*M.mpf(beta.p)/beta.q/z**3)
            for o, r in zip(fo, fr): worst = max(worst, abs(r(z, e1)/o(z) - 1))
        worst = float(worst); assert worst < 1e-25, worst
        nd = sp.fraction(sp.cancel(w))
        d = dict(family='mnaxial', row=f'{tag}_E{E}_mu2{mu2}',
                 row_params=dict(tag=tag, M=str(Mm), a=str(a_), beta=str(beta), E=str(E), L='0', mu2=str(mu2)),
                 var='x', chart='MN axis y = 1 (theta = 0), L = 0; bridge V9 axial derivation (v9_nve.axial_r), R = x on the axis',
                 form="Y' = [[0,1],[-q,-p]] Y, i.e. y'' + p y' + q y = 0 (non-reduced xi1 form; V9 reproduced v2's traces from its normal form r)",
                 exps=[dict(num=[f'{sp.Rational(c).p}/{sp.Rational(c).q}' for c in reversed(sp.Poly(nd[0], x).all_coeffs())],
                            den=[f'{sp.Rational(c).p}/{sp.Rational(c).q}' for c in reversed(sp.Poly(nd[1], x).all_coeffs())])],
                 p=dict(num=monos(Pn), den=monos(Pd)), q=dict(num=monos(Qn), den=monos(Qd)), bad=[0],
                 self_check=dict(vs='40-digit original exp-containing axial_r p, q vs exported rational form with E1 = exp(2 beta/x^3)', points=12, max_rel_err=worst),
                 provenance=f'TheBridge falsification/V9_mn_obstruction_check/code/v9_export_capd_axial.py via v9_nve.axial_r, commit {commit}')
        fn = f'mnaxial_{tag}_E{E}_mu2{mu2}.json'; json.dump(d, open(os.path.join(OUT, fn), 'w'))
        print(fn, f'gcd {gp}/{gq}', f'terms p {len(Pn.terms())}/{len(Pd.terms())} q {len(Qn.terms())}/{len(Qd.terms())}',
              f'selfcheck {worst:.1e}', f'{time.time() - t0:.0f}s', flush=True)
