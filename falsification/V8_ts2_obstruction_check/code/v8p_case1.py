"""V8' (post-failure amendment) -- add the case-1 polynomial solve to V8's count route. Controls first; exits
before TS if a control misbehaves. Reuses the bridge's own v8_nve.py (nve_r, analyse, log_at_zero, zv, load)."""
import sys, itertools, json, sympy as sp
sys.argv = [sys.argv[0]]                       # keep v8_nve's module-level run quiet: import pieces only
src = open('v8_nve.py').read().split("rows = [(1, 0, 4)")[0]
ns = {}; exec(src, ns)
x = ns['x']; nve_r, analyse, log_at_zero, zv, load = ns['nve_r'], ns['analyse'], ns['log_at_zero'], ns['zv'], ns['load']

def case1_search(r, an):
    facs = []
    for p in an['poles']:
        if p['pole_order'] != 2 or not p.get('beta_exact_all_roots'): return None, 'out of scope (non-double pole or non-rational exponent)'
        a = [sp.Rational(s) for s in p['alphas']]
        if any(not al.is_rational for al in a): return None, 'out of scope (irrational exponent)'
        # BUG FIX (post-run, 2026-09-24): the first run parsed the factor string with a plain Symbol('x'), not the
        # real x of the NVE, so every degree came out 0 and theta came out 0. Its verdicts are void. Parse with x.
        fx = sp.sympify(p['factor'], locals={'x': x})
        facs.append((fx, sp.Poly(fx, x).degree(), a))
    assert sum(f[1] for f in facs) == sum(sp.Poly(sp.sympify(p['factor'], locals={'x': x}), x).degree() for p in an['poles']) > 0
    if an['order_at_inf'] <= 2: return None, 'out of scope (order at infinity <= 2)'
    tried = []
    for choice in itertools.product(*[f[2] for f in facs]):
        for ainf in (0, 1):
            d = ainf - sum(f[1]*al for f, al in zip(facs, choice))
            if not (d.is_integer and d >= 0): continue
            d = int(d)
            theta = sum(al*sp.diff(f[0], x)/f[0] for f, al in zip(facs, choice))
            cs = sp.symbols(f'c0:{d}') if d > 0 else ()
            P = x**d + sum(c*x**k for k, c in enumerate(cs))
            expr = sp.together(sp.diff(P, x, 2) + 2*theta*sp.diff(P, x) + (sp.diff(theta, x) + theta**2 - r)*P)
            num = sp.Poly(sp.numer(expr), x)
            eqs = num.coeffs()
            sol = sp.solve(eqs, cs, dict=True) if cs else ([{}] if all(sp.simplify(e) == 0 for e in eqs) else [])
            found = bool(sol) and (not cs or len(sol) > 0)
            tried.append(dict(choice=[str(c) for c in choice], a_inf=ainf, d=d, P_found=found,
                              P=str(P.subs(sol[0])) if found and sol else None))
            if found: return tried, 'CASE 1 HOLDS (P found)'
    return tried, 'no case-1 solution'

def grade(g, E, L, mu2):
    r, even, _ = nve_r(g, sp.Integer(E), sp.Integer(L), sp.Integer(mu2))
    an = analyse(r); lz = log_at_zero(r)
    tried, c1 = case1_search(r, an)
    if not lz.get('log_present'): v = 'NOT OBSTRUCTION (no log point at 0)'
    elif c1 == 'no case-1 solution': v = 'OBSTRUCTION'
    elif c1.startswith('CASE 1'): v = 'NOT OBSTRUCTION (case 1 holds)'
    else: v = 'INCONCLUSIVE (' + c1 + ')'
    return dict(even=even, log0=lz, case1=c1, tried=tried, verdict=v)

rows = [(1, 0, 4), (1, 0, 9), (1, 1, 4)]
out = {}
ctrl_ok = True
for name, g, want in [('ZV_delta2', zv(), 'OBSTRUCTION'), ('KERR_t1o2', load('ts2_KERR_metric_components_t1o2.txt'), 'NOT')]:
    for row in rows:
        res = grade(g, *row); out[f'{name}|{row}'] = res
        ok = res['verdict'] == 'OBSTRUCTION' if want == 'OBSTRUCTION' else not res['verdict'].startswith('OBSTRUCTION')
        ctrl_ok &= ok
        print(f'CONTROL {name:10s} {row}: {res["verdict"]:40s} case1={res["case1"]}  candidates tried={len(res["tried"] or [])}  {"OK" if ok else "MISBEHAVES"}')
if not ctrl_ok:
    print('A CONTROL MISBEHAVED -> V8\' REFUSED; TS rows not computed.'); json.dump(out, open('../results/v8p_results.json', 'w'), indent=1, default=str); sys.exit(0)
for name, fn in [('TS2_P1', 'ts2_metric_components_t1o2.txt'), ('TS2_P2', 'ts2_metric_components_t1o3.txt')]:
    g = load(fn)
    for row in rows:
        res = grade(g, *row); out[f'{name}|{row}'] = res
        print(f'TARGET  {name:10s} {row}: {res["verdict"]:40s} case1={res["case1"]}  candidates tried={len(res["tried"] or [])}')
json.dump(out, open('../results/v8p_results.json', 'w'), indent=1, default=str)
