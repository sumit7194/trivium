"""V24 (PREREGISTRATION.md): flat-plane reduction R1 (exact) and interval checks I1, I2 with negative controls.
Bridge TS2 metric (V11 loader, ts45); mpmath interval arithmetic with recursive bisection in (x, s = y^2)."""
import sys, os, json, time
import sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
V11 = os.path.join(HERE, '../../V11_chaos_reproduction/code'); sys.path.insert(0, V11)
_c = os.getcwd(); os.chdir(V11); import v11_chaos as V; os.chdir(_c)
X, Y = V.X, V.Y; s = sp.symbols('s', nonnegative=True)
E, L = sp.Rational(97, 100), sp.Rational(41, 8)
os.chdir(V11); g = V.get_metric('ts45'); os.chdir(_c)
det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
Gtt, Gtp, Gpp = g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det
W = sp.cancel(Gtt*E**2 - 2*Gtp*E*L + Gpp*L**2)
F = sp.cancel(g['g_xx']*(X**2 - 1))
out = {}

# ---- R1: conformal flatness and the Hamiltonian identity
pxs, pys, pu, pv = sp.symbols('p_x p_y p_u p_v')
conf = sp.cancel(g['g_xx']*(X**2 - 1) - g['g_yy']*(1 - Y**2))
H = sp.Rational(1, 2)*(pxs**2/g['g_xx'] + pys**2/g['g_yy'] + W)
Hflat = (sp.Rational(1, 2)*(pu**2 + pv**2) + sp.Rational(1, 2)*F*(W + 1))/F - sp.Rational(1, 2)
sub = {pu: pxs*sp.sqrt(X**2 - 1), pv: -pys*sp.sqrt(1 - Y**2)}
R1 = sp.cancel(sp.together(H - Hflat.subs(sub)))
out['R1'] = dict(conformal=str(conf), identity=str(R1)); print('R1 conformal', conf, '| identity', R1, flush=True)

# ---- V in (x, s): V = F (W + 1) / 2, even in y
Vxy = sp.cancel(F*(W + 1)/2)
Vs = sp.cancel(Vxy.subs(Y, sp.sqrt(s)))
assert not Vs.has(sp.sqrt(s)), 'not even in y'
nV, dV = sp.fraction(sp.together(Vs))
def strip(den):
    """A1: remove known-sign factors (s-1)^k, (x^2-s)^k, (x-1)^k, (x+1)^k; return (reduced_den, sign_of_removed)."""
    c, facs = sp.factor_list(den); keep = c; sgn = 1
    for f, k in facs:
        fe = sp.expand(f)
        if fe in (sp.expand(s - 1), sp.expand(1 - s)):
            sgn *= (-1 if fe == sp.expand(s - 1) else 1)**k
        elif fe in (sp.expand(X**2 - s), sp.expand(s - X**2)):
            sgn *= (1 if fe == sp.expand(X**2 - s) else -1)**k
        elif fe in (sp.expand(X - 1), sp.expand(X + 1), sp.expand(1 - X)):
            sgn *= (-1 if fe == sp.expand(1 - X) else 1)**k
        else: keep *= f**k
    return keep, sgn
dVx = sp.cancel(sp.diff(Vs, X)); n1, d1 = sp.fraction(sp.together(dVx))
dVs = sp.cancel(sp.diff(Vs, s)); n2, d2 = sp.fraction(sp.together(dVs))
fac = lambda e: sp.factor(e)
print('den V', fac(dV), '\nden dVx', fac(d1), '\nden dVs', fac(d2), flush=True)
mp.mp.dps = 30
lam = lambda e: sp.lambdify((X, s), sp.horner(sp.expand(e), wrt=X), 'mpmath')
dV, sV0 = strip(dV); d1, s10 = strip(d1); d2, s20 = strip(d2)
print('A1 stripped signs', sV0, s10, s20, '| reduced dens', dV, d1, d2, flush=True)
nVf, dVf, n1f, d1f, n2f, d2f = map(lam, (nV, dV, n1, d1, n2, d2))
iv = mp.iv

def sign_iv(a):  # +1, -1, or 0 (undecided)
    if not hasattr(a, 'a'): return 1 if a > 0 else (-1 if a < 0 else 0)
    return 1 if a.a > 0 else (-1 if a.b < 0 else 0)

def check(xlo, xhi, want, which, maxboxes=3_000_000, maxdepth=26):
    """want = +1 or -1: required sign of dV/dx (which='x') or dV/ds (which='s') on {V <= 0}."""
    nf, df, sg0 = (n1f, d1f, s10) if which == 'x' else (n2f, d2f, s20)
    stack = [(mp.mpf(xlo), mp.mpf(xhi), mp.mpf(0), mp.mpf(1), 0)]; nbox = 0; undecided = []; violations = []; minlb = None
    while stack:
        a, b, c, d, dep = stack.pop(); nbox += 1
        if nbox > maxboxes: return dict(status='BOX LIMIT', nbox=nbox, undecided=len(stack) + len(undecided), violations=len(violations))
        bx, bs = iv.mpf([a, b]), iv.mpf([c, d])
        sV = sign_iv(nVf(bx, bs))*sign_iv(dVf(bx, bs))*sV0
        if sV > 0: continue                                  # V > 0 on the whole box: outside Hill's region
        sd = sign_iv(nf(bx, bs))*sign_iv(df(bx, bs))*sg0
        if sd == want: continue
        if sd == -want and sV < 0:                          # proven wrong sign inside Hill's region
            violations.append((float(a), float(b), float(c), float(d))); continue
        if dep >= maxdepth: undecided.append((float(a), float(b), float(c), float(d))); continue
        mx, ms = (a + b)/2, (c + d)/2
        if (b - a)/max(abs(a), 1) >= (d - c): stack += [(a, mx, c, d, dep + 1), (mx, b, c, d, dep + 1)]
        else: stack += [(a, b, c, ms, dep + 1), (a, b, ms, d, dep + 1)]
    return dict(status='OK' if not undecided and not violations else 'FAIL', nbox=nbox, undecided=len(undecided),
                violations=len(violations), first_undecided=undecided[:3], first_violation=violations[:3])

for name, args in (('NEG_I1_ext_to_9.6', (1.5, 9.6, +1, 'x')), ('I1', (1.5, 9.49, +1, 'x')),
                   ('I2', (9.3, 77.1, +1, 's')), ('NEG_I2_reversed', (9.3, 77.1, -1, 's'))):
    t0 = time.time(); r = check(*args); r['seconds'] = round(time.time() - t0, 1); out[name] = r
    print(name, r, flush=True)
    json.dump(out, open(os.path.join(HERE, '../results/v24_A1.json'), 'w'), indent=1, default=str)
