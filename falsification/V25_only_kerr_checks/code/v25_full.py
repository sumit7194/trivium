"""V25 addendum A: R-full (exact metrics, complex continuation) for P2 (Kerr, static twin), P5 (two-rod static),
P6 (ZV delta=2 exact; Schwarzschild f0 + twist dipole, R-trunc). Bridge code only."""
import sys, os, json, math, cmath, numpy as np, sympy as sp
from v25_rmap import Axis, make_trunc, return_map, loop_run, ve1_selfcheck, _ZS
HERE = os.path.dirname(os.path.abspath(__file__))
V11 = os.path.join(HERE, '../../V11_chaos_reproduction/code'); sys.path.insert(0, V11)
_c = os.getcwd(); os.chdir(V11); import v11_chaos as V; os.chdir(_c)
X, Y = V.X, V.Y
r2s, zs_ = sp.symbols('r2 z')
out = {}

# ---------- prolate-metric route (Kerr, ZV): U(x, y) with stable x, y from (r2, z), sigma = 1
def prolate_U(case, E, mu=1):
    os.chdir(V11); g = V.get_metric(case); os.chdir(_c)
    F1 = sp.cancel((X**2 - Y**2)/(g['g_xx']*(X**2 - 1)))
    F2 = sp.cancel(g['g_phiphi']/((X**2 - 1)*(1 - Y**2)))
    U = (E**2*F2 - mu**2)/(2*F1)
    Uf = sp.lambdify((X, Y), U, 'numpy'); Uxf = sp.lambdify((X, Y), sp.diff(U, X), 'numpy'); Uyf = sp.lambdify((X, Y), sp.diff(U, Y), 'numpy')
    def xy(r2, z):
        Rp = (z + 1)*np.sqrt(1 + r2/(z + 1)**2); Rm = (z - 1)*np.sqrt(1 + r2/(z - 1)**2); P = Rp*Rm
        B = 2*r2/(P*(1 + np.sqrt(1 - 4*r2/(P*P))))          # 1 - y^2, small root
        x = (Rp + Rm)/2; y = 1 - B/(1 + np.sqrt(1 - B))
        return x, y, Rp, Rm
    def Ufun(r2, z): x, y, _, _ = xy(r2, z); return Uf(x, y)
    def dUfun(r2, z):
        x, y, Rp, Rm = xy(r2, z)
        dx = (1/(2*Rp) + 1/(2*Rm))/2; dy = (1/(2*Rp) - 1/(2*Rm))/2
        return Uxf(x, y)*dx + Uyf(x, y)*dy
    return Ufun, dUfun, g

# ---------- static Weyl sums (twin, two-rod): f = prod (R_i + z - b_i)^eps_i ; e^{-2 gamma} = prod (1 + mu_i mu_j / rho^2)^{eps_i eps_j}
def weyl_sum(bs, es, E, mu=1):
    z, r2 = zs_, r2s
    R = [(z - b)*sp.sqrt(1 + r2/(z - b)**2) for b in bs]; A = [R[i] + z - bs[i] for i in range(len(bs))]
    f = sp.Mul(*[A[i]**es[i] for i in range(len(bs))])
    em2g = sp.Mul(*[(1 + r2/(A[i]*A[j]))**(es[i]*es[j]) for i in range(len(bs)) for j in range(len(bs))])
    F1 = f*em2g; F2 = 1/f; U = (E**2*F2 - mu**2)/(2*F1)
    psi = sp.Rational(1, 2)*sum(es[i]*sp.log(A[i]) for i in range(len(bs)))
    gam = -sp.Rational(1, 2)*sum(es[i]*es[j]*sp.log(1 + r2/(A[i]*A[j])) for i in range(len(bs)) for j in range(len(bs)))
    return U, F1, F2, psi, gam

def validate_weyl(bs, es, zvals, f0expr):
    """series of F1, F2 in r2 vs own static series; Weyl equations for gamma (in r2 = rho^2 form)."""
    U, F1, F2, psi, gam = weyl_sum(bs, es, sp.Rational(4, 5))
    z, t, E_, mu_, C2, f0, Uc = _ZS
    zz = sp.symbols('zz')
    a0 = sp.log(f0)/2; a1 = -sp.diff(a0, z, 2)/4; a2 = sp.diff(a0, z, 4)/64
    g1 = -sp.diff(a0, z)**2/2; g2 = (4*a1**2 - 2*sp.diff(a0, z)*sp.diff(a1, z))/4
    F1s = sp.series(sp.exp(2*(a0 + a1*t + a2*t**2) - 2*(g1*t + g2*t**2)), t, 0, 3).removeO()
    F2s = sp.series(sp.exp(-2*(a0 + a1*t + a2*t**2)), t, 0, 3).removeO()
    sub = {sp.Derivative(f0, (z, n)): sp.diff(f0expr, zs_, n).subs(zs_, z) for n in range(4, 0, -1)}
    import mpmath as mp
    mp.mp.dps = 50; worst = 0.0; weq = 0.0
    F1m = sp.lambdify((r2s, zs_), F1, 'mpmath'); F2m = sp.lambdify((r2s, zs_), F2, 'mpmath')
    pr, pz = sp.diff(psi, r2s), sp.diff(psi, zs_); gr, gz = sp.diff(gam, r2s), sp.diff(gam, zs_)
    W1 = sp.lambdify((r2s, zs_), gz - 4*r2s*pr*pz, 'mpmath'); W2 = sp.lambdify((r2s, zs_), 2*gr - 4*r2s*pr**2 + pz**2, 'mpmath')
    for zv in zvals:
        for Fm, Fs in ((F1m, F1s), (F2m, F2s)):
            tc = mp.taylor(lambda rr: Fm(rr, mp.mpf(zv)), 0, 2)
            for n in (1, 2):
                c_s = complex(sp.N(Fs.coeff(t, n).subs(sub).subs(f0, f0expr.subs(zs_, z)).subs(z, sp.nsimplify(zv)), 40))
                worst = max(worst, abs(complex(tc[n])/c_s - 1))
        for rr in ('0.01', '0.05'):
            weq = max(weq, abs(complex(W1(mp.mpf(rr), mp.mpf(zv)))), abs(complex(W2(mp.mpf(rr), mp.mpf(zv)))))
    return worst, weq

def lam_weyl(bs, es, E):
    U = weyl_sum(bs, es, E)[0]
    return sp.lambdify((r2s, zs_), U, 'numpy'), sp.lambdify((r2s, zs_), sp.diff(U, r2s), 'numpy')

def U0_of(ax):
    return lambda z: ax.Y2(z)/(2*ax.Delta(z)**2)        # U0 = q0^2/2 = N D/(2 Delta^2)

def verdict(A, pred, floor):
    err = max(abs(A[i] - pred[i]) for i in range(2)); scale = max(abs(p) for p in pred)
    if floor > 1e-4: return 'VOID', err
    return ('MATCH' if err <= max(100*floor, 1e-6*scale) else 'MISMATCH'), err

def run_pole_case(label, ax, Ufun, dUfun, U2fun, zc, radii, preds):
    r = return_map(ax, Ufun, dUfun, U0_of(ax), zc, radii, starts=tuple(preds.keys()), U2fun=U2fun)
    rec = {}
    for st, pred in preds.items():
        v, err = verdict(r[st]['A'], pred, r[st]['floor'])
        if max(r[st]['ve1_check']) > 1e-8: v = 'VOID (VE1 self-check)'
        rec[str(st)] = dict(A=[str(a) for a in r[st]['A']], pred=[str(p) for p in pred], err=err, floor=r[st]['floor'], verdict=v,
                            diag={k: x for k, x in r[st].items() if k != 'A'})
        print(label, st, '| A', [complex(round(a.real, 8), round(a.imag, 8)) for a in r[st]['A']], '| pred', [complex(round(p.real, 8), round(p.imag, 8)) for p in pred],
              '| err %.2e floor %.2e ve1 %.1e' % (err, r[st]['floor'], max(r[st]['ve1_check'])), v, flush=True)
    return rec

# ===== P2: Kerr and the static twin, prolate units, M = 5/4, a = 3/4
M, a = 1.25, 0.75; z1, z2 = complex(-M, a), complex(-M, -a)
f0K = (zs_**2 - 1)/((zs_ + sp.Rational(5, 4))**2 + sp.Rational(9, 16))
bs_t = [1, -1, -sp.Rational(5, 4) + sp.I*sp.Rational(3, 4), -sp.Rational(5, 4) - sp.I*sp.Rational(3, 4)]; es_t = [1, 1, -1, -1]
w_series, w_eq = validate_weyl(bs_t, es_t, [3, 5], f0K)
print('twin validation: series rel err %.2e, Weyl eqs %.2e' % (w_series, w_eq), flush=True)
out['P2_twin_validation'] = dict(series_rel_err=w_series, weyl_eq_resid=w_eq, ok=bool(w_series <= 1e-12 and w_eq <= 1e-8))
for E in (0.8, 0.7):
    ax = Axis(z1, z2, M, M, E)
    U2t = make_trunc(f0K, sp.Integer(0), zs_, sp.nsimplify(E))[3]
    preds_twin = {(1, 0): [-math.pi/2 + 0j, math.pi + 0j], (0, 1): [math.pi + 0j, -math.pi/2 + 0j]}
    preds_kerr = {(1, 0): [0j, 0j], (0, 1): [0j, 0j]}
    Uk, dUk, _ = prolate_U('kerr45', sp.nsimplify(E))
    out[f'P2_kerr_E{E}'] = run_pole_case(f'P2 Kerr exact E={E}', ax, Uk, dUk, U2t, z1, (0.35, 0.5), preds_kerr)
    Ut, dUt = lam_weyl(bs_t, es_t, sp.nsimplify(E))
    out[f'P2_twin_E{E}'] = run_pole_case(f'P2 twin exact E={E}', ax, Ut, dUt, U2t, z1, (0.35, 0.5), preds_twin)
    if E == 0.8:   # must-pass cross-check: R-trunc on the twin data
        Utr, dUtr, U0tr, _ = make_trunc(f0K, sp.Integer(0), zs_, sp.nsimplify(E))
        out['P2_twin_trunc_cross'] = run_pole_case('P2 twin R-trunc cross-check', ax, Utr, dUtr, U2t, z1, (0.35, 0.5), preds_twin)
json.dump(out, open(os.path.join(HERE, '../results/v25_full.json'), 'w'), indent=1, default=str)

# ===== P5: real two-rod static (Fable coordinates), loop around z1 = 1, E = 3/5
bp = (sp.Rational(7, 4) + sp.sqrt(sp.Rational(49, 16) + sp.Rational(3, 2)))/2; bm = (sp.Rational(7, 4) - sp.sqrt(sp.Rational(49, 16) + sp.Rational(3, 2)))/2
bs_r = [bp, bm, 1, -sp.Rational(1, 2)]; es_r = [1, 1, -1, -1]
f0R = 1 - sp.Rational(3, 4)/(zs_ - 1) - sp.Rational(1, 2)/(zs_ + sp.Rational(1, 2))
w_series, w_eq = validate_weyl(bs_r, es_r, [3, 5], f0R)
print('two-rod validation: series rel err %.2e, Weyl eqs %.2e' % (w_series, w_eq), flush=True)
out['P5_validation'] = dict(series_rel_err=w_series, weyl_eq_resid=w_eq, ok=bool(w_series <= 1e-12 and w_eq <= 1e-8))
ax = Axis(1.0, -0.5, 0.75, 0.5, 0.6); U2t = make_trunc(f0R, sp.Integer(0), zs_, sp.Rational(3, 5))[3]
Ur, dUr = lam_weyl(bs_r, es_r, sp.Rational(3, 5))
out['P5_tworod'] = run_pole_case('P5 two-rod exact E=0.6', ax, Ur, dUr, U2t, 1.0, (0.4, 0.6), {(1, 0): [-0.2j*math.pi, 0.4j*math.pi]})
json.dump(out, open(os.path.join(HERE, '../results/v25_full.json'), 'w'), indent=1, default=str)
