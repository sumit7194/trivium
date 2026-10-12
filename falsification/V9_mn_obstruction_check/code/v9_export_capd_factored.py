"""Export the MN equatorial NVE in FACTORED form for quantum's CAPD replay: A, B, X and the t-derivatives A_t, X_t
(same chart, branch, E_k = exp(w_k) basis and gcd reduction as v9_export_capd.py), from which
    p_t = -(A_t/A - X_t/(2X)) - x2/x1,    q_t = x1^2 A B / X,    x1 = dx/dt, x2 = d^2x/dt^2, x = (t + 1/t)/2,
exactly as v9_equatorial_monodromy.eq_coeffs_t builds them. Requested by quantum after the expanded p, q forms stalled
CAPD's step-size control on mneq row 0 (suspected interval dependency blow-up over the large expanded polynomials).
Self-checks at 40 digits: (1) each exported factor vs the original exp-containing one; (2) p, q rebuilt from the
exported factors vs the original eq_coeffs_t p, q. The exact identity against the expanded export is quantum's gate.
Usage: python v9_export_capd_factored.py ROW [basis.json]"""
import sys, os, json, time, random, subprocess
import sympy as sp, mpmath as M
import v9_equatorial_monodromy as V
from v9_equatorial_monodromy import eq_coeffs_t, ROWS, t
from v9_export_capd import guard, auto_basis, to_rational, monos, coeff_lists, OUT

def factors_t(M_, a_, beta, E, L, mu2):
    """A, B, X in the t-chart, built line for line as in eq_coeffs_t (no simplification beyond its substitutions)."""
    x, y, R0 = V.x, V.y, V.R0
    F = V.mn_functions_R0(M_, a_, beta); f, om, e2g, k = F['f'], F['om'], F['e2g'], F['k']
    gtt = -f; gtp = f*om; gpp = -f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2)
    gxx_dn = k**2/f*e2g*(x**2 - y**2)/(x**2 - 1); gyy_dn = k**2/f*e2g*(x**2 - y**2)/(1 - y**2)
    det = gtt*gpp - gtp**2
    Gtt, Gtp, Gpp, Gxx, Gyy = gpp/det, -gtp/det, gtt/det, 1/gxx_dn, 1/gyy_dn
    at0 = lambda e: e.subs(y, 0)
    d2 = lambda e: sp.diff(e, y, 2).subs(y, 0)
    E, L, mu2 = map(sp.Integer, (E, L, mu2))
    V0 = at0(Gtt)*E**2 - 2*at0(Gtp)*E*L + at0(Gpp)*L**2
    V2 = d2(Gtt)*E**2 - 2*d2(Gtp)*E*L + d2(Gpp)*L**2
    px2 = (-mu2 - V0)/at0(Gxx)
    A = at0(Gyy); X = at0(Gxx)*(-mu2 - V0); B = sp.Rational(1, 2)*(d2(Gxx)*px2 + V2)
    sub = {x: (t + 1/t)/2, R0: (t**2 - 1)/(2*t)}
    return [e.subs(sub) for e in (A, B, X)]

if __name__ == '__main__':
    guard(); row = int(sys.argv[1]); spec = ROWS[row]; t0 = time.time()
    A, B, X = factors_t(*spec['params']); At, Xt = sp.diff(A, t), sp.diff(X, t)
    pt, qt, x1, x2 = eq_coeffs_t(*spec['params'])
    fac = dict(A=A, B=B, X=X, A_t=At, X_t=Xt)
    args = set()
    for e in fac.values(): args |= {sp.cancel(sp.together(a.args[0])) for a in e.atoms(sp.exp)}
    if len(sys.argv) > 2:
        basis = [sp.sympify(s, locals={'t': t}) for s in json.load(open(sys.argv[2]))[str(row)]]; bsrc = sys.argv[2]
    else:
        basis = auto_basis(args); bsrc = 'auto (bridge)'
    Es = sp.symbols(f'E1:{len(basis) + 1}', positive=True); gens = (t,) + tuple(Es)
    print(f'row {row}: {len(args)} exp args, basis {len(basis)} ({bsrc})', flush=True)
    rat = {}
    for nm, e in fac.items():
        N, D, g = to_rational(e, basis, Es); rat[nm] = (N, D)
        print(f'  {nm} done {time.time() - t0:.0f}s terms {len(N.terms())}/{len(D.terms())} gcd deg {g}', flush=True)
    M.mp.dps = 40; rng = random.Random(23 + row)
    fw = [sp.lambdify(t, w, 'mpmath') for w in basis]
    fo = {nm: sp.lambdify(t, e, 'mpmath') for nm, e in fac.items()}
    fr = {nm: sp.lambdify(gens, N.as_expr()/D.as_expr(), 'mpmath') for nm, (N, D) in rat.items()}
    fpq = [sp.lambdify(t, e, 'mpmath') for e in (pt, qt)]
    fx = [sp.lambdify(t, e, 'mpmath') for e in (x1, x2)]
    wf = wpq = M.mpf(0)
    for _ in range(12):
        z = M.mpc(rng.uniform(0.4, 3), rng.uniform(-3, 3)); ev = [M.exp(f(z)) for f in fw]
        v = {nm: fr[nm](z, *ev) for nm in fr}
        for nm in fr: wf = max(wf, abs(v[nm]/fo[nm](z) - 1))
        X1, X2 = fx[0](z), fx[1](z)
        p_re = -(v['A_t']/v['A'] - v['X_t']/(2*v['X'])) - X2/X1; q_re = X1**2*v['A']*v['B']/v['X']
        wpq = max(wpq, abs(p_re/fpq[0](z) - 1), abs(q_re/fpq[1](z) - 1))
    wf, wpq = float(wf), float(wpq); assert wf < 1e-25 and wpq < 1e-25, (wf, wpq)
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    d = dict(family='mneq_factored', row=str(row),
             row_params=dict(zip(['M', 'a', 'beta', 'E', 'L', 'mu2'], map(str, spec['params']))),
             var='t', chart="x = (t + 1/t)/2, R0 = (t^2-1)/(2t) (positive-R0 branch); MN equatorial NVE, bridge V9-eq' derivation",
             form="y'' + p y' + q y = 0 with p = -(A_t/A - X_t/(2X)) - x2/x1, q = x1^2 A B / X, x1 = (1 - 1/t^2)/2, x2 = 1/t^3",
             exps=[coeff_lists(w) for w in basis], exps_basis_source=bsrc,
             factors={nm: dict(num=monos(N), den=monos(D)) for nm, (N, D) in rat.items()}, bad=[0, 1, -1],
             self_check=dict(points=12, factors_vs_original_max_rel_err=wf, pq_rebuilt_vs_eq_coeffs_t_max_rel_err=wpq,
                             vs='40-digit: exported rational factors (E_k = exp(w_k)) vs original exp-containing factors; '
                                'p, q rebuilt from exported factors vs eq_coeffs_t'),
             provenance=f'TheBridge falsification/V9_mn_obstruction_check/code/v9_export_capd_factored.py, commit {commit}')
    os.makedirs(OUT, exist_ok=True); json.dump(d, open(os.path.join(OUT, f'mneq_factored_row_{row}.json'), 'w'))
    print(f'row {row} exported, selfcheck factors {wf:.1e} pq {wpq:.1e}, {time.time() - t0:.0f}s', flush=True)
