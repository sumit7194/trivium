"""Export the bridge's own exact MN equatorial NVE coefficients (V9-eq' derivation, positive-R0 branch fix) for quantum's
CAPD third replay. Form: y'' + p_t y' + q_t y = 0 in the t-chart x = (t + 1/t)/2, R0 = (t^2 - 1)/(2t)
(exactly v9_equatorial_monodromy.eq_coeffs_t). Every exp(.) atom is written as a product of E_k = exp(w_k(t)) with
integer powers (basis w_k supplied, or derived automatically); p_t, q_t become rational functions of (t, E_1..E_K),
reduced by an exact polynomial gcd. Negative E powers are cleared into the denominator.
Usage: python v9_export_capd.py ROW [basis.json]"""
import sys, os, json, time, random, subprocess, resource, threading
import sympy as sp, mpmath as M
from v9_equatorial_monodromy import eq_coeffs_t, ROWS, t

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../export_capd')

def guard(limit=8e9):
    def g():
        while True:
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > limit: print('MEM GUARD', flush=True); os._exit(3)
            time.sleep(2)
    threading.Thread(target=g, daemon=True).start()

def auto_basis(args):
    """Greedy: smallest-|degree| representatives such that every arg is an integer multiple of one basis element."""
    basis = []
    for a in sorted(args, key=lambda e: (sp.count_ops(e), sp.default_sort_key(e))):
        if any(sp.cancel(a/b).is_Integer for b in basis): continue
        for i, b in enumerate(basis):                 # replace b by a if b is an integer multiple of a
            if sp.cancel(b/a).is_Integer: basis[i] = a; break
        else: basis.append(a)
    # canonical sign: positive leading coefficient of the numerator
    out = []
    for b in basis:
        n, d = sp.fraction(sp.cancel(b)); out.append(-b if sp.Poly(n, t).LC() < 0 else b)
    return out

def to_rational(e, basis, Es):
    m = {}
    for a in e.atoms(sp.exp):
        arg = sp.cancel(sp.together(a.args[0])); hit = None
        for k, w in enumerate(basis):
            r = sp.cancel(arg/w)
            if r.is_Integer: hit = (k, int(r)); break
        assert hit, f'exp argument not an integer multiple of a basis element: {arg}'
        m[a] = Es[hit[0]]**hit[1]
    n, d = sp.fraction(sp.together(e.xreplace(m)))
    gens = (t,) + tuple(Es)
    N = sp.Poly(sp.expand(n), *gens); D = sp.Poly(sp.expand(d), *gens)
    g = sp.gcd(N, D); N = sp.div(N, g)[0]; D = sp.div(D, g)[0]
    return N, D, int(g.total_degree())

def monos(P):
    return [[list(map(int, m)), f'{sp.Rational(c).p}/{sp.Rational(c).q}'] for m, c in zip(P.monoms(), P.coeffs())]

def coeff_lists(w):
    n, d = sp.fraction(sp.cancel(w))
    asc = lambda e: [f'{sp.Rational(c).p}/{sp.Rational(c).q}' for c in reversed(sp.Poly(e, t).all_coeffs())]
    return dict(num=asc(n), den=asc(d))

if __name__ == '__main__':
    guard(); row = int(sys.argv[1]); spec = ROWS[row]; t0 = time.time()
    pt, qt, x1, x2 = eq_coeffs_t(*spec['params'])
    args = {sp.cancel(sp.together(a.args[0])) for a in (pt.atoms(sp.exp) | qt.atoms(sp.exp))}
    if len(sys.argv) > 2:
        basis = [sp.sympify(s, locals={'t': t}) for s in json.load(open(sys.argv[2]))[str(row)]]; bsrc = sys.argv[2]
    else:
        basis = auto_basis(args); bsrc = 'auto (bridge)'
    Es = sp.symbols(f'E1:{len(basis) + 1}', positive=True)
    print(f'row {row}: {len(args)} exp args, basis {len(basis)} ({bsrc})', flush=True)
    Pn, Pd, gp = to_rational(pt, basis, Es); print(f'  p done {time.time() - t0:.0f}s terms {len(Pn.terms())}/{len(Pd.terms())} gcd deg {gp}', flush=True)
    Qn, Qd, gq = to_rational(qt, basis, Es); print(f'  q done {time.time() - t0:.0f}s terms {len(Qn.terms())}/{len(Qd.terms())} gcd deg {gq}', flush=True)
    # self-check at 40 digits: original (exp-containing) pt, qt vs exported rational forms with E_k = exp(w_k(t))
    M.mp.dps = 40; rng = random.Random(11 + row)
    fo = [sp.lambdify(t, e, 'mpmath') for e in (pt, qt)]
    fw = [sp.lambdify(t, w, 'mpmath') for w in basis]
    gens = (t,) + tuple(Es)
    fr = [sp.lambdify(gens, N.as_expr()/D.as_expr(), 'mpmath') for N, D in ((Pn, Pd), (Qn, Qd))]
    worst = M.mpf(0)
    for _ in range(12):
        z = M.mpc(rng.uniform(0.4, 3), rng.uniform(-3, 3)); ev = [M.exp(f(z)) for f in fw]
        for o, r in zip(fo, fr): worst = max(worst, abs(r(z, *ev)/o(z) - 1))
    worst = float(worst); assert worst < 1e-25, worst
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    d = dict(family='mneq', row=str(row), row_params=dict(zip(['M', 'a', 'beta', 'E', 'L', 'mu2'], map(str, spec['params']))),
             var='t', chart='x = (t + 1/t)/2, R0 = (t^2-1)/(2t) (positive-R0 branch); MN equatorial NVE, bridge V9-eq\' derivation',
             form="Y' = [[0,1],[-q,-p]] Y, i.e. y'' + p y' + q y = 0 (non-reduced xi1 form, as V9-eq' used to reproduce v2's traces)",
             exps=[coeff_lists(w) for w in basis], exps_basis_source=bsrc,
             p=dict(num=monos(Pn), den=monos(Pd)), q=dict(num=monos(Qn), den=monos(Qd)), bad=[0, 1, -1],
             self_check=dict(vs='40-digit original exp-containing eq_coeffs_t vs exported rational form with E_k = exp(w_k)', points=12, max_rel_err=worst),
             provenance=f'TheBridge falsification/V9_mn_obstruction_check/code/v9_export_capd.py via eq_coeffs_t, commit {commit}')
    os.makedirs(OUT, exist_ok=True); json.dump(d, open(os.path.join(OUT, f'mneq_row_{row}.json'), 'w'))
    print(f'row {row} exported, selfcheck {worst:.1e}, {time.time() - t0:.0f}s', flush=True)
