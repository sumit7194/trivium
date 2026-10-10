"""V12: exact separatrix L_sep (bisection) and gates G1 (Kerr vs Bardeen-Press-Teukolsky) and G2 (vs ansatz's grid)."""
import sys, os, math, json
import numpy as np, sympy as sp
from scipy.optimize import brentq, minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V11_chaos_reproduction/code'))
_cwd = os.getcwd(); os.chdir(os.path.join(HERE, '../../V11_chaos_reproduction/code'))
from v11_chaos import get_metric, X, Y
os.chdir(_cwd)

P = {'ts45': sp.Rational(4, 5), 'ts35': sp.Rational(3, 5), 'kerr45': sp.Rational(4, 5), 'kerr35': sp.Rational(3, 5)}
def mass(case): return float(2 / P[case]) if case.startswith('ts') else float(1 / P[case])

def x_ring(case):
    if not case.startswith('ts'): return None
    den = sp.denom(sp.together(get_metric(case)['g_TT'].subs(Y, 0)))
    return max(float(sp.re(r)) for r in sp.Poly(den, X).nroots() if abs(sp.im(r)) < 1e-12 and sp.re(r) > 0.9)

def x_in(case): return x_ring(case) + 0.01 if case.startswith('ts') else 1.0005

def equatorial_inverse(case):
    """g^tt, g^tphi, g^phiphi on y = 0 as fast numpy functions of x."""
    g = get_metric(case); det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    G = [g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det]
    return [sp.lambdify(X, sp.simplify(e.subs(Y, 0)), 'numpy') for e in G]

def Wfun(Ginv, E, L):
    a, b, c = Ginv
    return lambda x: a(x)*E*E - 2*b(x)*E*L + c(x)*L*L

def J_sign(case):
    """J from the asymptotic g_tphi ~ -2 J / r (sin^2 theta = 1 on the equator), in this chart's (t, phi) orientation."""
    g = get_metric(case); xv = 1e5
    return -np.sign(float(g['g_Tphi'].subs({X: xv, Y: 0})))

def has_closed(Wx, xi, xo=400.0, n=40000):
    """True if {x in (xi, xo): W(x) <= -1} has a component touching neither xi nor xo. Grid in log(x - 1) plus local
    refinement of every interior local minimum, so a tiny pocket near threshold is not missed."""
    xs = 1 + np.exp(np.linspace(math.log(xi - 1), math.log(xo - 1), n)); w = Wx(xs) + 1
    # refine every interior local minimum of w
    idx = np.where((w[1:-1] <= w[:-2]) & (w[1:-1] <= w[2:]))[0] + 1
    for i in idx:
        r = minimize_scalar(lambda t: Wx(t) + 1, bounds=(xs[i-1], xs[i+1]), method='bounded', options={'xatol': 1e-14})
        wmin = min(r.fun, w[i])
        # the component holding this minimum is closed iff forbidden points (W > -1) lie on both sides of it
        if wmin <= 0 and np.any(w[:i] > 0) and np.any(w[i+1:] > 0): return True
    return False

def _bisect(Ginv, E, sense, xi, lo, hi, want_true_at_hi, tol):
    while hi - lo > tol:
        mid = 0.5*(lo + hi)
        if has_closed(Wfun(Ginv, E, sense*mid), xi) == want_true_at_hi: hi = mid
        else: lo = mid
    return 0.5*(lo + hi)

def L_sep(case, E, sense, lo_m=1.5, hi_m=7.99, step_m=0.01, tol=1e-10):
    """Addendum 1: L_sep = lower edge of the closed-pocket |L| range (unstable circular orbit); also the upper edge
    (stable circular orbit), each by bisection between neighbouring grid points."""
    Ginv = equatorial_inverse(case); m = mass(case); xi = x_in(case)
    grid = np.round(np.arange(lo_m, hi_m + 1e-9, step_m), 10)
    flags = [has_closed(Wfun(Ginv, E, sense*g*m), xi) for g in grid]
    trans = [i for i in range(1, len(flags)) if flags[i] != flags[i-1]]
    assert len(trans) in (1, 2) and flags[trans[0]], f'unexpected predicate pattern, transitions at {[grid[i] for i in trans]}'
    k = trans[0]
    lower = _bisect(Ginv, E, sense, xi, grid[k-1]*m, grid[k]*m, True, tol)
    upper = None
    if len(trans) == 2:
        j = trans[1]; upper = _bisect(Ginv, E, sense, xi, grid[j-1]*m, grid[j]*m, False, tol)
    return dict(case=case, E=E, sense=sense, m=m, L_grid=float(grid[k]*m), L_sep=lower, L_upper=upper)

def bpt_L(M, a, E, prograde):
    """Equatorial circular orbits in Kerr (Bardeen-Press-Teukolsky 1972). Returns |L| of the unstable (r_mb < r < r_isco)
    and stable (r > r_isco) circular orbits with energy E < 1."""
    s = 1 if prograde else -1
    def EL(r):
        d = r**0.75*math.sqrt(r**1.5 - 3*M*r**0.5 + s*2*a*M**0.5)
        return (r**1.5 - 2*M*r**0.5 + s*a*M**0.5)/d, M**0.5*(r*r - s*2*a*M**0.5*r**0.5 + a*a)/d
    Z1 = 1 + (1 - (a/M)**2)**(1/3)*((1 + a/M)**(1/3) + (1 - a/M)**(1/3)); Z2 = math.sqrt(3*(a/M)**2 + Z1**2)
    risco = M*(3 + Z2 - s*math.sqrt((3 - Z1)*(3 + Z1 + 2*Z2)))
    rmb = 2*M - s*a + 2*math.sqrt(M)*math.sqrt(M - s*a)
    ru = brentq(lambda r: EL(r)[0] - E, rmb*(1 + 1e-12), risco*(1 - 1e-12), xtol=1e-14, rtol=1e-15)
    rs = brentq(lambda r: EL(r)[0] - E, risco*(1 + 1e-12), 1e6*M, xtol=1e-14, rtol=1e-15)
    return dict(L_unstable=EL(ru)[1], r_unstable=ru, L_stable=EL(rs)[1], r_stable=rs, r_isco=risco, r_mb=rmb)

if __name__ == '__main__':
    out = []
    ANS = {('ts45', +1): 10.475, ('kerr45', +1): 5.2125, ('ts35', -1): 9.2667, ('kerr35', -1): 4.500}
    for case, E, sense in (('ts45', 0.97, +1), ('kerr45', 0.97, +1), ('ts35', 0.95, -1), ('kerr35', 0.95, -1)):
        d = L_sep(case, E, sense); d['J_sign'] = int(J_sign(case)); d['x_in'] = x_in(case)
        d['physical_sense'] = 'prograde' if sense*d['J_sign'] > 0 else 'retrograde'
        A = ANS[(case, sense)]; d['ansatz_L_sep'] = A
        d['G2_diff'] = A - d['L_sep']; d['G2_pass'] = bool(-1e-4 <= A - d['L_sep'] < 0.01*d['m'] + 1e-4)
        if case.startswith('kerr'):
            M = d['m']; a = float(sp.Rational(3, 5)/P[case]) if case == 'kerr45' else float(sp.Rational(4, 5)/P[case])
            for pro in (True, False):
                try: d['BPT_' + ('pro' if pro else 'retro')] = bpt_L(M, a, E, pro)
                except ValueError: d['BPT_' + ('pro' if pro else 'retro')] = 'no circular orbit with this E in this sense'
            B = d['BPT_' + ('pro' if d['physical_sense'] == 'prograde' else 'retro')]
            d['G1_rel'] = abs(B['L_unstable'] - d['L_sep'])/B['L_unstable']; d['G1_pass'] = bool(d['G1_rel'] < 1e-8)
            d['G1b_rel'] = abs(B['L_stable'] - d['L_upper'])/B['L_stable'] if d['L_upper'] else None
            d['G1b_pass'] = bool(d['G1b_rel'] is not None and d['G1b_rel'] < 1e-8)
        print(json.dumps(d), flush=True); out.append(d)
    json.dump(out, open(os.path.join(HERE, '../results/v12_lsep.json'), 'w'), indent=1)
