"""V25 addendum B (PREREGISTRATION.md, b2c57b0): Lemma X critical case (gap G2). Bridge code.
B1: exact identity kappa^2(E*) = mu^2 f0''(p) D(p)^2 / 4 at critical points (sympy).
B2: scaling of the residue coefficient h_{m-1} at p as eps = E^2 - E*^2 -> 0 (mpmath power series, 60 digits),
with the generic-p control and the integer-exponent must-show-vanishing control."""
import os, json, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

# ---------------- B1
z, p, m1, m2, z1, z2, mu, b, c = sp.symbols('z p m1 m2 z1 z2 mu b c')
f0 = 1 - m1/(z - z1) - m2/(z - z2); D = (z - z1)*(z - z2)
fp, fpp = sp.diff(f0, z), sp.diff(f0, z, 2)
n1 = sp.factor(sp.numer(sp.together(fp))).subs(z, p)
Es2 = mu**2*f0.subs(z, p)
kap2 = (z1 - z2)*((Es2 - mu**2)*(z1 - z2) - mu**2*(m1 - m2))/4
diff = sp.together(kap2 - mu**2*fpp.subs(z, p)*D.subs(z, p)**2/4)
num = sp.expand(sp.numer(diff))
remA = sp.simplify(sp.rem(sp.Poly(num, p), sp.Poly(sp.expand(n1), p)).as_expr())
out['B1a_remainder'] = str(remA)
# (b) double pole
Del = z**2 + b*z + c; f0d = Del/(z - z1)**2
n1d = sp.numer(sp.together(sp.diff(f0d, z))).subs(z, p)
kap2d = mu**2*Del.subs(z, z1)/2
diffd = sp.together(kap2d - mu**2*sp.diff(f0d, z, 2).subs(z, p)*((p - z1)**2)**2/4)
remB = sp.simplify(sp.rem(sp.Poly(sp.expand(sp.numer(diffd)), p), sp.Poly(sp.expand(n1d), p)).as_expr())
out['B1b_remainder'] = str(remB)
# (c) nondegeneracy: resultant of num f0' and num f0'' in p
n2 = sp.numer(sp.together(fpp)).subs(z, p)
res = sp.factor(sp.resultant(sp.expand(n1), sp.expand(n2), p))
n2d = sp.numer(sp.together(sp.diff(f0d, z, 2))).subs(z, p)
resd = sp.factor(sp.resultant(sp.expand(n1d), sp.expand(n2d), p))
out['B1c_resultant_two_poles'] = str(res); out['B1c_resultant_double_pole'] = str(resd)
out['B1_pass'] = bool(remA == 0 and remB == 0 and res != 0 and resd != 0)
print('B1a rem', remA, '| B1b rem', remB, '\nB1c res', res, '\nB1c res (double)', resd, '\nB1 pass', out['B1_pass'], flush=True)

# ---------------- B2
mp.mp.dps = 60
NT = 8   # series length (need up to index m-1 = 5)

def ser_mul(a, b): return [mp.fsum(a[i]*b[k - i] for i in range(k + 1)) for k in range(NT)]
def ser_inv(a):
    r = [1/a[0]] + [mp.mpc(0)]*(NT - 1)
    for k in range(1, NT): r[k] = -mp.fsum(a[i]*r[k - i] for i in range(1, k + 1))/a[0]
    return r
def ser_sqrt(a, s0):
    r = [s0] + [mp.mpc(0)]*(NT - 1)
    for k in range(1, NT): r[k] = (a[k] - mp.fsum(r[i]*r[k - i] for i in range(1, k)))/(2*s0)
    return r
def ser_exp(a):   # a[0] = 0
    r = [mp.mpc(1)] + [mp.mpc(0)]*(NT - 1)
    for k in range(1, NT): r[k] = mp.fsum(i*a[i]*r[k - i] for i in range(1, k + 1))/k
    return r
def taylor_at(f, p0): return [mp.taylor(f, p0, NT - 1)[k] for k in range(NT)]

def case_data(name):
    if name == 'kerr':
        M, A = mp.mpf(1), mp.mpf(3)/5; Z1, Z2, M1, M2 = 1j*A, -1j*A, M, M
    else:
        Z1, Z2, M1, M2 = mp.mpf(1), mp.mpf(-1), mp.mpf(3)/10, mp.mpf(1)/2
    return mp.mpc(Z1), mp.mpc(Z2), mp.mpf(M1), mp.mpf(M2)

def h_coeffs(Z1, Z2, M1, M2, p0, E2, kappa, w, mu=mp.mpf(1)):
    """Taylor coefficients at p0 of h = exp(w kappa (u - u_p)) / y, y = D sqrt(phi), phi = E^2 - mu^2 f0, du = dz/y."""
    d1, d2 = p0 - Z1, p0 - Z2                                   # exact series in t = z - p0 (no numerical differentiation)
    inv = lambda d: [(-1)**k/d**(k + 1) for k in range(NT)]
    phi = [mu**2*(M1*x1 + M2*x2) for x1, x2 in zip(inv(d1), inv(d2))]; phi[0] += E2 - mu**2
    Dser = [d1*d2, d1 + d2, mp.mpc(1)] + [mp.mpc(0)]*(NT - 3)
    y = ser_mul(Dser, ser_sqrt(phi, mp.sqrt(phi[0])))
    iy = ser_inv(y)
    U = [mp.mpc(0)] + [iy[k - 1]/k for k in range(1, NT)]
    return ser_mul(ser_exp([w*kappa*x for x in U]), iy)

def kappa2(Z1, Z2, M1, M2, E2, mu=1): return (Z1 - Z2)*((E2 - mu**2)*(Z1 - Z2) - mu**2*(M1 - M2))/4

def model_coeffs(cp, Dp, sa):
    """Taylor coefficients of M(xi) = exp(cp asinh xi)/(Dp sa sqrt(1+xi^2))."""
    return [x/(Dp*sa) for x in mp.taylor(lambda xi: mp.exp(cp*mp.asinh(xi))/mp.sqrt(1 + xi*xi), 0, NT - 1)]

EPS = [mp.mpf(10)**(-k) for k in range(2, 11)]
B2 = {}; allpass = True
for name in ('kerr', 'rods'):
    Z1, Z2, M1, M2 = case_data(name)
    f0 = lambda zz: 1 - M1/(zz - Z1) - M2/(zz - Z2)
    crit = mp.polyroots([M1 + M2, -2*(M1*Z2 + M2*Z1), M1*Z2**2 + M2*Z1**2], maxsteps=200, extraprec=200)   # num f0'
    p0 = mp.mpc(crit[0]); assert abs(mp.diff(f0, p0)) < mp.mpf(10)**-40
    Es2 = f0(p0); a = f0(p0)*0 + mp.diff(f0, p0, 2)/2; Dp = (p0 - Z1)*(p0 - Z2); sa = mp.sqrt(-a)
    k2s = kappa2(Z1, Z2, M1, M2, Es2)
    B2[name] = dict(p=str(mp.nstr(p0, 15)), identity_check=float(abs(k2s - mp.diff(f0, p0, 2)*Dp**2/4)))
    for w in (2, 4):
        cp = w*mp.sqrt(k2s)/(Dp*sa)
        Mc = model_coeffs(cp, Dp, sa)
        B2[name]['cprime^2_w%d' % w] = mp.nstr(cp**2, 12)
        for m in range(1, 7):
            devs = []
            for eps in EPS:
                E2 = Es2 + eps; kap = mp.sqrt(kappa2(Z1, Z2, M1, M2, E2))
                sig = mp.sqrt(eps)/sa
                h = h_coeffs(Z1, Z2, M1, M2, p0, E2, kap, w)
                devs.append(float(abs(h[m - 1]*sig**m/Mc[m - 1] - 1)))
            ok = devs[-1] <= 1e-3 and all(devs[i + 1] <= devs[i] for i in range(len(devs) - 4, len(devs) - 1))
            allpass &= ok
            B2[name]['w%d_m%d' % (w, m)] = dict(dev=['%.2e' % d for d in devs], ok=ok)
            print(name, 'w', w, 'm', m, 'dev', ['%.1e' % d for d in devs[-4:]], ok, flush=True)
    # generic control
    pg = mp.mpc('0.3', '0.2'); Eg2 = f0(pg); gen = {}
    for m in range(1, 7):
        lr = []
        for eps in EPS[-2:]:
            E2 = Eg2 + eps; kap = mp.sqrt(kappa2(Z1, Z2, M1, M2, E2))
            lr.append(mp.log(abs(h_coeffs(Z1, Z2, M1, M2, pg, E2, kap, 2)[m - 1])))
        slope = float((lr[1] - lr[0])/(mp.log(EPS[-1]) - mp.log(EPS[-2])))
        gen['m%d' % m] = dict(slope=slope, predicted=-(m - 0.5), ok=abs(slope + (m - 0.5)) <= 0.05)
    B2[name]['generic_control'] = gen; print(name, 'generic slopes', {k: round(v['slope'], 4) for k, v in gen.items()}, flush=True)
    # must-show-vanishing control: kappa chosen so that c' = 1 (w = 2)
    kint = Dp*sa/2
    vals = {}
    for m in (2, 3, 5):
        eps = EPS[-1]; sig = mp.sqrt(eps)/sa
        h = h_coeffs(Z1, Z2, M1, M2, p0, Es2 + eps, kint, 2)
        vals['m%d' % m] = float(abs(h[m - 1]*sig**m*Dp*sa))
    B2[name]['integer_control'] = dict(vals=vals, ok=vals['m3'] <= 1e-2 and vals['m5'] <= 1e-2 and vals['m2'] > 1e-1)
    print(name, 'integer control |h sigma^m Dp sa|', vals, flush=True)
out['B2'] = B2; out['B2_pass'] = bool(allpass)
out['controls_pass'] = all(all(v['ok'] for v in B2[n]['generic_control'].values()) and B2[n]['integer_control']['ok'] for n in B2)
print('B2 pass', out['B2_pass'], '| controls pass', out['controls_pass'], flush=True)
json.dump(out, open(os.path.join(HERE, '../results/v25_B.json'), 'w'), indent=1, default=str)
