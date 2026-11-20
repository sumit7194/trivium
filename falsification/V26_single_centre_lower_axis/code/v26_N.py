"""V26 N-count and N-search (PREREGISTRATION.md, ccafd13). Bridge code.
f0^- = f0/(f0^2 + c0^2) (from e_- = 1/e_+). Lemma N: single-centre, asymptotically flat (c0 = O(z^-2)), c0 != 0
=> deg f0^- >= 4."""
import os, json, random, itertools, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
z = sp.symbols('z')

def fminus(f0, c0): return sp.cancel(f0/(f0**2 + c0**2))
def deg(R):
    n, d = sp.fraction(sp.cancel(R)); return max(sp.degree(n, z), sp.degree(d, z))
def sing_count(R, E2=sp.Rational(7, 10), mu=1):
    """singular points of the axis NVE for P = E^2 - mu^2 R at a (fixed) energy: s simple, h heavy (|order| >= 2)."""
    n, d = sp.fraction(sp.cancel(R)); P = sp.cancel(E2 - mu**2*R); pn, pd = sp.fraction(P)
    s = h = 0; info = []
    for poly, kind in ((pn, 'zero'), (pd, 'pole')):
        for fac, k in sp.factor_list(poly, extension=None)[1]:
            r = sp.degree(fac, z)
            if r == 0: continue
            if k == 1: s += r
            else: h += r
            info.append((kind, str(fac), k))
    # infinity: ordinary iff P -> nonzero constant with no 1/z term issue (P' / P = O(z^-2)); report order of P at infinity
    ordinf = sp.degree(pd, z) - sp.degree(pn, z)
    return dict(s=s, h=h, s_plus_2h=s + 2*h, P_order_at_infinity=int(ordinf), factors=info)

out = {}
# ---------- N-count
cnt = {}
for b in (sp.Rational(1, 2), 1, 3):
    f0 = 1 - 2/z
    R = fminus(f0, b/z**2); cnt['b/z^2, b=%s' % b] = dict(fminus=str(sp.factor(R)), deg=deg(R), **sing_count(R))
    Rc = fminus(f0, b/z); cnt['CONTROL b/z, b=%s' % b] = dict(fminus=str(sp.factor(Rc)), deg=deg(Rc), **sing_count(Rc))
out['N_count'] = cnt
for k, v in cnt.items(): print('N-count', k, '| deg', v['deg'], '| s+2h', v['s_plus_2h'], '| s,h', v['s'], v['h'], flush=True)

# ---------- N-search
def families():
    M = 1
    fD = 1 - 2*M/z                                 # class D (centre at 0, M = 1 by scaling)
    fC = lambda q: (z**2 - 2*M*z + q)/z**2         # class C (double pole at 0), q != 0
    f1 = sp.Integer(1)                             # f0 = 1
    return fD, fC, f1

def rand_rat(rng, lo=-6, hi=6): return sp.Rational(rng.randint(lo, hi), rng.randint(1, 4))

def random_twist(rng, d, flat=True):
    """c0 = N/D, deg D = d, deg N <= d - 2 if flat (c0 = O(z^-2)), else deg N <= d - 1. Structured choices:
    roots of D sometimes at 0 (the centre) or at zeros of f0 (z = 2 for class D), N sometimes vanishing there."""
    roots = []
    for _ in range(d):
        c = rng.random()
        roots.append(0 if c < 0.3 else (2 if c < 0.45 else rand_rat(rng)))
    D = sp.prod([z - r for r in roots]) if rng.random() < 0.8 else sp.expand(sp.prod([z - r for r in roots[:-2]])*(z**2 + abs(rand_rat(rng)) + 1)) if d >= 2 else sp.prod([z - r for r in roots])
    top = d - 2 if flat else d - 1
    if top < 0: return None
    N = sum(rand_rat(rng)*z**k for k in range(top + 1))
    if rng.random() < 0.3 and top >= 1: N = sp.expand(N*(z - 2)/z) if False else sp.expand((z - 2)*sum(rand_rat(rng)*z**k for k in range(top)))
    if N == 0: return None
    return sp.cancel(N/D)

rng = random.Random(20261120)
fD, fC, f1 = families()
search = dict(trials=0, min_deg={}, hits=[], control_hits=[])
for trial in range(6000):
    cls = rng.choice(['D', 'C', 'one'])
    f0 = fD if cls == 'D' else (fC(rand_rat(rng) or 1) if cls == 'C' else f1)
    d = rng.randint(1, 4)
    for flat in (True, False):
        c0 = random_twist(rng, d, flat)
        if c0 is None or c0 == 0: continue
        R = fminus(f0, c0); dg = deg(R)
        key = '%s flat=%s' % (cls, flat)
        search['min_deg'][key] = min(search['min_deg'].get(key, 99), dg)
        if dg <= 2:
            (search['hits'] if flat else search['control_hits']).append(dict(cls=cls, f0=str(f0), c0=str(c0), deg=dg))
    search['trials'] += 1
# symbolic d <= 2 families with parameter cancellations (resultant descent, two levels)
a, b, p, q = sp.symbols('a b p q')
sym = {}
for name, f0, c0 in (('D, a/z^2', fD, a/z**2), ('D, a/(z-p)^2', fD, a/(z - p)**2), ('D, a/((z-p)(z-q))', fD, a/((z - p)*(z - q))),
                     ('D, a/(z^2+b z+q)', fD, a/(z**2 + b*z + q)), ('C(q), a/z^2', fC(q), a/z**2), ('C(q), a/(z-p)^2', fC(q), a/(z - p)**2),
                     ('one, a/(z-p)^2', f1, a/(z - p)**2), ('one, a/(z^2+b z+q)', f1, a/(z**2 + b*z + q))):
    R = fminus(f0, c0); n, dd = sp.fraction(sp.together(R))
    g = deg(R); best = g; trail = []
    res = sp.factor(sp.resultant(sp.expand(n), sp.expand(dd), z))
    for fac, _ in sp.factor_list(res)[1]:
        if not (fac.free_symbols & {p, q, b}): continue
        var = sorted(fac.free_symbols & {p, q, b}, key=str)[0]
        for solv in sp.solve(fac, var):
            if solv.has(sp.I) and not solv.is_real: pass
            R2 = sp.cancel(R.subs(var, solv)); g2 = deg(R2); best = min(best, g2); trail.append((str(var), str(solv), g2))
    sym[name] = dict(generic_deg=g, min_deg_after_one_cancellation=best, trail=trail[:8])
    print('N-search symbolic', name, '| generic deg', g, '| min after a parameter cancellation', best, flush=True)
search['symbolic'] = sym
out['N_search'] = search
print('N-search random: trials', search['trials'], '| min deg', search['min_deg'], '| flat hits (deg<=2)', len(search['hits']),
      '| non-flat control hits', len(search['control_hits']), flush=True)
print('control hit examples', search['control_hits'][:3], flush=True)
json.dump(out, open(os.path.join(HERE, '../results/v26_N.json'), 'w'), indent=1, default=str)
