"""V8' poison controls (added after the solver bug; labelled as such): equations WITH a log point at x = 0
(exponents -1/2, 3/2, as in TS) where case 1 HOLDS by construction. The route must NOT say OBSTRUCTION.
Guards against a case-1 solver that silently never finds P (which would make every log point look obstructed).
r = w' + w^2 with w = sum rho_c/(x-c) + P'/P, residues chosen so ord_inf(r) > 2 and all poles of r are double."""
import sys, sympy as sp
ns = {}
exec(open('v8_nve.py').read().split("rows = [(1, 0, 4)")[0], ns)
exec('import itertools, json\n' + open('v8p_case1.py').read().split('def case1_search')[1].join(['def case1_search', '']).split('def grade(')[0], ns)
x, analyse, log_at_zero, case1_search = ns['x'], ns['analyse'], ns['log_at_zero'], ns['case1_search']
R = sp.Rational
def make(rhos, P):
    w = sum(rh/(x - c) for c, rh in rhos.items()) + sp.diff(P, x)/P
    return sp.cancel(sp.together(sp.diff(w, x) + w**2))
# poison 1: d = 0 (P = 1); residues 3/2 at 0, 1/4 at 3, -3/4 at -2 (sum 1)
r1 = make({0: R(3, 2), 3: R(1, 4), -2: R(-3, 4)}, sp.Integer(1))
# poison 2: d = 1 (P = x - 7); residues at 0, 3 fixed; rho_a at -2, rho_b at 5 chosen so r has no pole at 7 and sum+1 = 1
ra, rb = sp.symbols('ra rb')
sol = sp.solve([R(3, 2) + R(1, 4) + ra + rb + 1 - 1, R(3, 2)/7 + R(1, 4)/4 + ra/9 + rb/2], [ra, rb])
r2 = make({0: R(3, 2), 3: R(1, 4), -2: sol[ra], 5: sol[rb]}, x - 7)
for name, r in [('poison_d0', r1), ('poison_d1', r2)]:
    an = analyse(r); lz = log_at_zero(r); tried, c1 = case1_search(r, an)
    v = 'OBSTRUCTION' if (lz.get('log_present') and c1 == 'no case-1 solution') else ('NOT OBSTRUCTION' if lz.get('log_present') is not None else 'no log point')
    print(f'{name}: log0={lz.get("log_present")}  N={lz.get("N")}  poles={[ (p["factor"], p.get("beta")) for p in an["poles"]]}  ord_inf={an["order_at_inf"]}')
    print(f'   case1: {c1};  P={[t["P"] for t in (tried or []) if t["P_found"]]}  ->  {v}  ({"OK" if v != "OBSTRUCTION" and lz.get("log_present") else "POISON MISBEHAVES"})')
