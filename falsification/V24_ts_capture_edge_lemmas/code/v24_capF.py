"""V24 addendum F (PREREGISTRATION.md, 2e1daf6): the brake cap in interval arithmetic. Bridge code.
F0 gates (containment, identity), F1 bisection away from the brake point, F2 mean-value jet lemma on the disc,
rho0 ladder {1e-5, 1e-4, 1e-3}, must-fail controls NEG-F1, NEG-F0b, NEG-F2.
Usage: python v24_capF.py [quick]   (quick = smoke test with tiny box budget; not a registered run)"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'v24.py')).read()
__file__ = os.path.join(HERE, 'v24.py')
exec(_src.split('# ---- R1')[0])                                              # metric, W, F, X, Y, s, E, L
exec('# ---- V in' + _src.split('# ---- V in')[1].split('for name, args in')[0])  # nVf, dVf, sV0, sign_iv, iv, lam
import sympy as sp, mpmath as mp
__file__ = os.path.join(HERE, 'v24_capF.py')
QUICK = len(sys.argv) > 1 and sys.argv[1] == 'quick'
NEGF2_ONLY = len(sys.argv) > 1 and sys.argv[1] == 'negF2'   # amendment F-a rerun of the last two controls
mp.mp.dps = 30; iv.dps = 30

# ---- exact polynomials: V = N/D in (x, y); derivatives by the quotient rule (F0a checks them against sympy diff)
Vxy_ = sp.cancel(F*(W + 1)/2)
Nx_, Dx_ = sp.fraction(sp.together(Vxy_))
Nx_, Dx_ = sp.expand(Nx_), sp.expand(Dx_)
def hl(e): return sp.lambdify((X, Y), sp.horner(sp.expand(e), wrt=X), 'mpmath')
P = {}
for nm, base in (('N', Nx_), ('D', Dx_)):
    P[nm] = hl(base); P[nm + 'x'] = hl(sp.diff(base, X)); P[nm + 'y'] = hl(sp.diff(base, Y))
    P[nm + 'xx'] = hl(sp.diff(base, X, 2)); P[nm + 'xy'] = hl(sp.diff(base, X, Y)); P[nm + 'yy'] = hl(sp.diff(base, Y, 2))

def derivs_uv(U, Vv_):
    """(V, V_u, V_v, V_uu, V_uv, V_vv) at (u, v); works for iv and mp scalars."""
    f = iv if hasattr(U, 'a') else mp
    eu, emu = f.exp(U), f.exp(-U)                                             # iv has no cosh/sinh: build from exp
    x, sh = (eu + emu)/2, (eu - emu)/2; y, sn = f.cos(Vv_), f.sin(Vv_); cy = y
    n = {k[1:]: P[k](x, y) for k in P if k[0] == 'N'}; d = {k[1:]: P[k](x, y) for k in P if k[0] == 'D'}
    V = n[''] / d['']
    Vx = (n['x'] - V*d['x'])/d['']; Vy = (n['y'] - V*d['y'])/d['']
    Vxx = (n['xx'] - 2*Vx*d['x'] - V*d['xx'])/d['']
    Vxy = (n['xy'] - Vx*d['y'] - Vy*d['x'] - V*d['xy'])/d['']
    Vyy = (n['yy'] - 2*Vy*d['y'] - V*d['yy'])/d['']
    Vu = Vx*sh; Vv = -Vy*sn
    Vuu = Vxx*sh*sh + Vx*x; Vuv = -Vxy*sh*sn; Vvv = Vyy*sn*sn - Vy*cy
    return V, Vu, Vv, Vuu, Vuv, Vvv

def hill_sign(U, Vv_):
    """V24 rule in (x, s = y^2): +1 V > 0 on box, -1 V < 0, 0 undecided."""
    x = (iv.exp(U) + iv.exp(-U))/2; y = iv.cos(Vv_); s2 = y*y
    s2 = iv.mpf([max(lo(s2), mp.mpf(0)), min(hi(s2), mp.mpf(1))])
    return sign_iv(nVf(x, s2))*sign_iv(dVf(x, s2))*sV0

# ---- fixed data
ub0, vb0, DEL = mp.mpf('2.9784812092869313'), mp.mpf('0.5410774904031077'), mp.mpf('1e-7')
UB, VB = iv.mpf([ub0 - DEL, ub0 + DEL]), iv.mpf([vb0 - DEL, vb0 + DEL])
def lo(t): return mp.mpf(t.a)      # ivmpf.a is a degenerate interval: convert to mpf
def hi(t): return mp.mpf(t.b)
x93 = iv.mpf('9.3'); U1 = iv.log(x93 + iv.sqrt(x93*x93 - 1))
_, VuB, VvB, _, _, _ = derivs_uv(UB, VB)
SL = VuB/VvB                                                                  # s := V_u/V_v over B (exact jet relation)
out = dict(addendum='F', prereg='2e1daf6', B=dict(u=[str(UB.a), str(UB.b)], v=[str(VB.a), str(VB.b)]),
           slope=[float(SL.a), float(SL.b)], u1=[float(U1.a), float(U1.b)], quick=QUICK)
print('slope s over B:', SL, flush=True)

def Cfun(U, Vv_, sl):
    V, Vu, Vv, _, _, _ = derivs_uv(U, Vv_)
    den = (UB - U1) + sl*(Vv_ - VB); tau = (U - U1)/den
    return V, tau, den, Vu, Vv

def clip01(t):
    l, h = max(lo(t), mp.mpf(0)), min(hi(t), mp.mpf(1))
    return None if l > h else iv.mpf([l, h])

# ---- F0 gates
def F0a():
    pts = [('2.9784', '0.5410'), ('2.9785', '0.5411'), ('2.97848', '0.54107'), ('2.95', '0.541'), ('2.93', '0.5410')]
    exprs = dict(V=Vxy_)
    exprs['Vx'] = sp.diff(Vxy_, X); exprs['Vy'] = sp.diff(Vxy_, Y)
    exprs['Vxx'] = sp.diff(Vxy_, X, 2); exprs['Vxy'] = sp.diff(Vxy_, X, Y); exprs['Vyy'] = sp.diff(Vxy_, Y, 2)
    fs = {k: sp.lambdify((X, Y), e, 'mpmath') for k, e in exprs.items()}
    worst = []; ok = True
    for us, vs in pts:
        with mp.workdps(50):
            u, v = mp.mpf(us), mp.mpf(vs); x, y = mp.cosh(u), mp.cos(v); sh, sn = mp.sinh(u), mp.sin(v)
            Vx, Vy = fs['Vx'](x, y), fs['Vy'](x, y)
            ref = [fs['V'](x, y), Vx*sh, -Vy*sn, fs['Vxx'](x, y)*sh**2 + Vx*x, -fs['Vxy'](x, y)*sh*sn, fs['Vyy'](x, y)*sn**2 - Vy*y]
        got = derivs_uv(iv.mpf(us), iv.mpf(vs))
        for nm, r, g in zip(('V', 'Vu', 'Vv', 'Vuu', 'Vuv', 'Vvv'), ref, got):
            inside = g.a <= r <= g.b; ok &= inside
            worst.append((us, vs, nm, float(r), float(g.b - g.a), bool(inside)))
    return dict(pass_=bool(ok), rows=worst)

def F0b(sl):
    _, tau, _, Vu, Vv = Cfun(UB, VB, sl)
    C = -Vu + tau*sl*Vv
    return dict(C_at_B=[float(C.a), float(C.b)], contains0=bool(C.a <= 0 <= C.b), tau_at_B=[float(tau.a), float(tau.b)])

# ---- F1
UDOM = (lo(U1), hi(UB) + mp.mpf('0.004')); VDOM = (mp.mpf(0), hi(VB))
def F1(rho0, sl, maxboxes=5_000_000, maxdepth=40):
    stack = [(UDOM[0], UDOM[1], VDOM[0], VDOM[1], 0)]
    nbox = 0; why = dict(above=0, notHill=0, tau=0, disc=0, C=0); undecided = []; viol = []; margin = None
    while stack:
        a, b, c, d, dep = stack.pop(); nbox += 1
        if nbox > maxboxes: return dict(status='BOX LIMIT', nbox=nbox, why=why, undecided=len(undecided) + len(stack), violations=len(viol))
        if c >= hi(VB): why['above'] += 1; continue
        du = max(abs(b - lo(UB)), abs(a - hi(UB))); dv = max(abs(d - lo(VB)), abs(c - hi(VB)))
        if mp.sqrt(du*du + dv*dv) < rho0: why['disc'] += 1; continue
        U, Vv_ = iv.mpf([a, b]), iv.mpf([c, d])
        hs = hill_sign(U, Vv_)
        if hs > 0: why['notHill'] += 1; continue
        V, tau, den, Vu, Vvv = Cfun(U, Vv_, sl)
        if den.a <= 0: tc = 'split'
        else:
            tc = clip01(tau)
            if tc is None: why['tau'] += 1; continue
        if tc != 'split':
            C = -Vu + tc*sl*Vvv
            if C.b < 0:
                why['C'] += 1; margin = C.b if margin is None else max(margin, C.b); continue
            if C.a > 0 and hs < 0 and tau.a >= 0 and tau.b <= 1:
                viol.append((float(a), float(b), float(c), float(d), float(C.a))); continue
        if dep >= maxdepth: undecided.append((float(a), float(b), float(c), float(d))); continue
        if (b - a) >= (d - c): m = (a + b)/2; stack += [(a, m, c, d, dep + 1), (m, b, c, d, dep + 1)]
        else: m = (c + d)/2; stack += [(a, b, c, m, dep + 1), (a, b, m, d, dep + 1)]
    return dict(status='OK' if not undecided and not viol else 'FAIL', nbox=nbox, why=why, undecided=len(undecided),
                violations=len(viol), first_undecided=undecided[:3], first_violation=viol[:3],
                margin_maxCupper=None if margin is None else float(margin))

# ---- F2
def F2(rho0, sl, hill=True, th=(mp.pi, 2*mp.pi), maxdepth=30, stop_early=False):
    """stop_early (amendment F-a, NEG-F2 only): return at the first proven-C>0 interval or after 1000 depth-limited ones."""
    DU = iv.mpf([lo(UB) - rho0, hi(UB) + rho0]); DV = iv.mpf([lo(VB) - rho0, hi(VB)])
    V, Vu, Vv, Vuu, Vuv, Vvv = derivs_uv(DU, DV)
    den = (UB - U1) + sl*(DV - VB)
    if den.a <= 0: return dict(status='FAIL', reason='den not positive on D')
    tau = clip01((DU - U1)/den)
    Cu = -Vuu + sl*Vv/den + tau*sl*Vuv
    Cv = -Vuv - tau*sl*sl*Vv/den + tau*sl*Vvv
    stack = [(mp.mpf(th[0]), mp.mpf(th[1]), 0)]; why = dict(tau=0, notHill=0, C=0); und = []; posC = []; rate = None; n = 0
    while stack:
        a, b, dep = stack.pop(); n += 1
        T = iv.mpf([a, b]); ec, es = iv.cos(T), iv.sin(T)
        if (ec - sl*es).a > 0: why['tau'] += 1; continue
        if hill and (Vu*ec + Vv*es).a > 0: why['notHill'] += 1; continue
        g = Cu*ec + Cv*es
        if g.b < 0: why['C'] += 1; rate = g.b if rate is None else max(rate, g.b); continue
        if g.a > 0:
            posC.append((float(a), float(b), float(g.a)))                    # proven C > 0 in this direction: stop
            if stop_early: break
            continue
        if dep >= maxdepth:
            und.append((float(a), float(b)))
            if stop_early and len(und) >= 1000: break
            continue
        m = (a + b)/2; stack += [(a, m, dep + 1), (m, b, dep + 1)]
    return dict(status='OK' if not und and not posC else 'FAIL', n=n, why=why, undischarged=len(und), first_undischarged=und[:3],
                provenCpos=len(posC), first_provenCpos=posC[:3], rate_maxupper=None if rate is None else float(rate),
                gradC=[[float(Cu.a), float(Cu.b)], [float(Cv.a), float(Cv.b)]], den_lo=float(den.a))

def save(): json.dump(out, open(os.path.join(HERE, '../results/v24_capF%s.json' % ('_quick' if QUICK else '')), 'w'), indent=1, default=str)

if NEGF2_ONLY:
    out = json.load(open(os.path.join(HERE, '../results/v24_capF.json'))); t0 = time.time(); rc = mp.mpf(out['F_verdict'].split('= ')[1])
    out['NEG_F0b'] = F0b(2*SL); print('NEG-F0b (slope 2s):', out['NEG_F0b'], flush=True)
    out['NEG_F2'] = F2(rc, SL, hill=False, th=(0, 2*mp.pi), stop_early=True); out['NEG_F2']['amendment'] = 'F-a stop_early'
    print('NEG-F2 (no Hill, theta in [0, 2pi]):', out['NEG_F2'], flush=True)
    out['controls'] = dict(NEG_F1_fires=out['NEG_F1'].get('violations', 0) > 0, NEG_F0b_excludes0=not out['NEG_F0b']['contains0'],
                           NEG_F2_fails=out['NEG_F2']['status'] != 'OK' or out['NEG_F2']['provenCpos'] > 0)
    out['seconds_negF2'] = round(time.time() - t0, 1); print('controls:', out['controls'], flush=True)
    json.dump(out, open(os.path.join(HERE, '../results/v24_capF.json'), 'w'), indent=1, default=str); sys.exit(0)
t0 = time.time()
out['F0a'] = F0a(); print('F0a containment:', out['F0a']['pass_'], flush=True)
out['F0b'] = F0b(SL); print('F0b identity:', out['F0b'], flush=True); save()
mb = 20000 if QUICK else 5_000_000
passed = None; out['ladder'] = []
for rho in ('1e-5', '1e-4', '1e-3'):
    r0 = mp.mpf(rho); t1 = time.time()
    f2 = F2(r0, SL); print('rho0', rho, 'F2:', f2, flush=True)
    f1 = F1(r0, SL, maxboxes=mb); print('rho0', rho, 'F1:', f1, round(time.time() - t1, 1), 's', flush=True)
    ok = out['F0a']['pass_'] and out['F0b']['contains0'] and f1['status'] == 'OK' and f2['status'] == 'OK'
    out['ladder'].append(dict(rho0=rho, F1=f1, F2=f2, pass_=bool(ok), seconds=round(time.time() - t1, 1))); save()
    if ok: passed = rho; break
out['F_verdict'] = 'PASS at rho0 = %s' % passed if passed else 'FAIL (no rho0 in the ladder passed)'
print('F verdict:', out['F_verdict'], flush=True)
rc = mp.mpf(passed or '1e-4')
out['NEG_F1'] = F1(rc, 2*SL, maxboxes=mb); print('NEG-F1 (slope 2s):', out['NEG_F1'], flush=True); save()
out['NEG_F0b'] = F0b(2*SL); print('NEG-F0b (slope 2s):', out['NEG_F0b'], flush=True)
out['NEG_F2'] = F2(rc, SL, hill=False, th=(0, 2*mp.pi)); print('NEG-F2 (no Hill, theta in [0, 2pi]):', out['NEG_F2'], flush=True)
out['controls'] = dict(NEG_F1_fires=out['NEG_F1'].get('violations', 0) > 0, NEG_F0b_excludes0=not out['NEG_F0b']['contains0'],
                       NEG_F2_fails=out['NEG_F2']['status'] != 'OK' or out['NEG_F2']['provenCpos'] > 0)
out['seconds'] = round(time.time() - t0, 1); print('controls:', out['controls'], 'total', out['seconds'], 's', flush=True); save()
