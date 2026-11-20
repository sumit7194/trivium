"""V26 addendum C (B8): the invisible family seen from below. Bridge code (independent of Fable's t5).
Lower-axis first-order NVE v'' = -(3/16)(P'/P)^2 v, P = E^2 - f0/(f0^2 + c0^2), with c0 continued by
c0''' = (S2)'/(2 c0''), S2 = (c0'')^2 rational. Monodromy of 4 loops from z_b = 4; statistic: non-abelian derived subgroup."""
import os, sys, json, math, cmath, numpy as np, sympy as sp, mpmath as mp
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
z, al = sp.symbols('z alpha')
A = sp.Rational(3, 5); I = sp.I

def kerr_family():
    f0 = 1 - 1/(z - I*A) - 1/(z + I*A)
    cK = -2*A/(z**2 + A**2); D = z**2 + A**2; v = (z + I*A)/(z - I*A)
    Q = v**3 + v**-3 - sp.Rational(3, 5)*(v + 1/v) - sp.Rational(4, 5)
    S2 = sp.diff(cK, z, 2)**2 + al*Q/D**3
    return f0, S2, sp.diff(cK, z, 2)

def control_family():
    f0 = 1 - 2/z; c0 = 1/z**2
    return f0, sp.diff(c0, z, 2)**2, c0

def lam(e): return sp.lambdify((z, al), e, 'numpy')

AN = 0.6
def kerr_funcs():
    """hand-coded (fast) Kerr-family functions; checked against sympy in self_test()."""
    ia = 1j*AN
    def f0(z_, a): return 1 - 1/(z_ - ia) - 1/(z_ + ia)
    def f0p(z_, a): return 1/(z_ - ia)**2 + 1/(z_ + ia)**2
    def S2(z_, a):
        D = z_*z_ + AN*AN; ck2 = 4*AN*(AN*AN - 3*z_*z_)/D**3; v = (z_ + ia)/(z_ - ia)
        Q = v**3 + v**-3 - 0.6*(v + 1/v) - 0.8
        return ck2*ck2 + a*Q/D**3
    def S2p(z_, a):
        D = z_*z_ + AN*AN; ck2 = 4*AN*(AN*AN - 3*z_*z_)/D**3; ck3 = 48*AN*z_*(z_*z_ - AN*AN)/D**4
        v = (z_ + ia)/(z_ - ia); vp = -2*ia/(z_ - ia)**2
        Q = v**3 + v**-3 - 0.6*(v + 1/v) - 0.8; Qv = 3*v**2 - 3*v**-4 - 0.6*(1 - v**-2)
        return 2*ck2*ck3 + a*(Qv*vp/D**3 - 6*z_*Q/D**4)
    return f0, f0p, S2, S2p

def control_funcs():
    return (lambda z_, a: 1 - 2/z_), (lambda z_, a: 2/z_**2), (lambda z_, a: 36/z_**8), (lambda z_, a: -288/z_**9)

def self_test():
    zs = [3.1 + 0.7j, -2.2 + 1.4j, 1.7 - 2.0j]
    f0, S2, _ = kerr_family(); refs = [lam(f0), lam(sp.diff(f0, z)), lam(S2), lam(sp.diff(S2, z))]
    worst = 0.0
    for fn, rf in zip(kerr_funcs(), refs):
        for zz in zs:
            for a in (0.0, 0.1): worst = max(worst, abs(fn(zz, a) - rf(zz, a))/max(1e-300, abs(rf(zz, a))))
    f0c, S2c, _ = control_family(); refc = [lam(f0c), lam(sp.diff(f0c, z)), lam(S2c), lam(sp.diff(S2c, z))]
    for fn, rf in zip(control_funcs(), refc):
        for zz in zs: worst = max(worst, abs(fn(zz, 0.0) - rf(zz, 0.0))/abs(rf(zz, 0.0)))
    return worst

class Model:
    def __init__(s, funcs, E):
        s.f0, s.f0p, s.S2, s.S2p = funcs; s.E = E
    def rhs(s, zz, Y, a):
        c0, c1, c2 = Y[0], Y[1], Y[2]
        c3 = s.S2p(zz, a)/(2*c2)
        f, fp = s.f0(zz, a), s.f0p(zz, a)
        g = f*f + c0*c0; gp = 2*f*fp + 2*c0*c1
        fm = f/g; fmp = (fp*g - f*gp)/(g*g)
        P = s.E*s.E - fm
        R = -(3/16)*(fmp/P)**2
        return [c1, c2, c3, Y[5], Y[6], R*Y[3], R*Y[4]]
    def crhs(s, zz, Y, a):
        return [Y[1], Y[2], s.S2p(zz, a)/(2*Y[2])]
    def Pval(s, zz, Y, a):
        f = s.f0(zz, a); return s.E**2 - f/(f*f + Y[0]**2)
    def gval(s, zz, Y, a):
        f = s.f0(zz, a); return f*f + Y[0]**2

def integrate_path(model, pts, Y0, a, rtol, conly=False):
    """piecewise-linear path through pts (complex), plus circles given as ('circle', centre, radius)."""
    Y = np.array(Y0, dtype=complex); zc = pts[0]
    for seg in pts[1:]:
        if isinstance(seg, tuple):
            _, cen, rad = seg
            th0 = cmath.phase(zc - cen)
            fz = lambda t: cen + rad*cmath.exp(1j*(th0 + 2*math.pi*t)); dz = lambda t: 2j*math.pi*rad*cmath.exp(1j*(th0 + 2*math.pi*t))
            zend = zc
        else:
            z0_, z1_ = zc, seg
            fz = lambda t, z0_=z0_, z1_=z1_: z0_ + (z1_ - z0_)*t; dz = lambda t, z0_=z0_, z1_=z1_: (z1_ - z0_)
            zend = seg
        fr = (lambda t, y: dz(t)*np.asarray(model.crhs(fz(t), y, a))) if conly else (lambda t, y: dz(t)*np.asarray(model.rhs(fz(t), y, a)))
        sol = solve_ivp(fr, (0, 1), Y, method='DOP853', rtol=rtol, atol=rtol*1e-3)
        Y = sol.y[:, -1]; zc = zend
    return Y

def loop_matrix(model, Ybase, route, centre, rad, a, rtol):
    Y0 = np.concatenate([Ybase[:3], np.eye(2, dtype=complex).ravel()])
    path = [route[0]] + route[1:] + [('circle', centre, rad)] + list(reversed(route[:-1]))
    Y = integrate_path(model, path, Y0, a, rtol)
    return Y[3:].reshape(2, 2), Y[:3] - Ybase[:3]

def refine(model, Ybase, route, guess, a, rtol, which):
    """Newton for a zero of P ('P') or of g = f0^2 + c0^2 ('g'), continuing only c0 (not the NVE) along the route."""
    zt = guess
    F = (lambda zz, YY: model.Pval(zz, YY, a)) if which == 'P' else (lambda zz, YY: model.gval(zz, YY, a))
    for _ in range(5):
        Y = integrate_path(model, route[:-1] + [zt], np.array(Ybase[:3], dtype=complex), a, rtol, conly=True)
        h = 1e-6
        Yh = integrate_path(model, [zt, zt + h], Y, a, rtol, conly=True)
        d = (F(zt + h, Yh) - F(zt, Y))/h
        zt = zt - F(zt, Y)/d
    return zt

def stat(Ms, normalised=False):
    """registered statistic: max ||K K' - K' K|| over commutator pairs; normalised (extra, not registered): divided by ||K|| ||K'||."""
    K = [Ms[i] @ Ms[j] @ np.linalg.inv(Ms[i]) @ np.linalg.inv(Ms[j]) for i in range(4) for j in range(i + 1, 4)]
    nf = (lambda p, q: np.linalg.norm(K[p])*np.linalg.norm(K[q])) if normalised else (lambda p, q: 1.0)
    return max(np.linalg.norm(K[p] @ K[q] - K[q] @ K[p])/nf(p, q) for p in range(len(K)) for q in range(p + 1, len(K)))

def base_state_kerr(S2f, cKpp, a, zb=4.0):
    """c0, c0', c0'' at zb from asymptotic flatness, integrating c0'' from infinity along the real axis (mpmath)."""
    mp.mp.dps = 30
    s2 = sp.lambdify((z, al), S2f, 'mpmath'); ck = sp.lambdify(z, cKpp, 'mpmath')
    c2 = lambda t: mp.sign(ck(t))*mp.sqrt(s2(t, a))
    c1 = -mp.quad(c2, [zb, 10*zb, mp.inf]); c0 = mp.quad(lambda t: (t - zb)*c2(t), [zb, 10*zb, mp.inf])
    return np.array([complex(c0), complex(c1), complex(c2(zb))])

def kerr_targets(E):
    """Kerr-from-below singular points: poles 2 +- 0.6i, zeros of z^2-2z+a^2 = E^2((z-2)^2+a^2)."""
    a2 = 0.36; c = [1 - E**2, -2 + 4*E**2, a2*(1 - E**2) - 4*E**2]
    zr = sorted(np.roots(c).real)
    zneg, zpos = zr[0], zr[1]
    return [('g', 2 + 0.6j, [4.0, 4 + 3j, 2 + 3j, 2 + 0.6j]),
            ('g', 2 - 0.6j, [4.0, 4 - 3j, 2 - 3j, 2 - 0.6j]),
            ('P', complex(zpos), [4.0, complex(zpos)]),
            ('P', complex(zneg), [4.0, 4 + 3j, complex(zneg) + 3j, complex(zneg)])]

def run_kerr(E, a, rtol, rad=0.2):
    f0, S2, cKpp = kerr_family(); m = Model(kerr_funcs(), E)
    Yb = base_state_kerr(S2, cKpp, a)
    Ms, gates = [], []
    for which, guess, route in kerr_targets(E):
        zt = refine(m, Yb, route, guess, a, rtol, which)
        r = route[:-1] + [zt + rad]                          # approach to a point on the circle
        if which == 'g' and guess.imag > 0: r = route[:-1] + [zt + 1j*rad]
        if which == 'g' and guess.imag < 0: r = route[:-1] + [zt - 1j*rad]
        if which == 'P' and guess.real < 0: r = route[:-1] + [zt + 1j*rad]
        M, dc = loop_matrix(m, Yb, r, zt, rad, a, rtol)
        Ms.append(M); gates.append(dict(target=str(zt), trace=abs(np.trace(M)), det=abs(np.linalg.det(M) - 1), c0_return=float(np.max(np.abs(dc)))))
    run_kerr.last_norm = stat(Ms, True)
    return stat(Ms), gates

def run_control(E, rtol, rad=0.15):
    f0, S2, c0 = control_family(); m = Model(control_funcs(), E)
    zb = 4.0; Yb = np.array([complex(c0.subs(z, zb)), complex(sp.diff(c0, z).subs(z, zb)), complex(sp.diff(c0, z, 2).subs(z, zb))])
    zz = np.roots([1, -2, 1j]); ww = np.roots([1, -2, -1j])           # zeros of e and of e-bar (poles of f0^-)
    pts = sorted([p for p in list(zz) + list(ww) if abs(p) > 1.0], key=lambda p: p.imag)
    # zeros of P = E^2 - f0^- : f0^- = z^3(z-2)/(z^2(z-2)^2+1); P=0 <=> z^3(z-2) = E^2 (z^2(z-2)^2+1)
    poly = np.poly1d([1, -2, 0, 0, 0]) - E**2*(np.poly1d([1, -4, 4, 0, 0]) + 1)
    zp = sorted([r for r in poly.r if abs(r) > 1.0 and abs(r.imag) < 1e-9], key=lambda r: r.real)
    targets = [(pts[0], [zb, zb - 3j, pts[0].real - 3j, pts[0]], -1j), (pts[-1], [zb, zb + 3j, pts[-1].real + 3j, pts[-1]], 1j)]
    for r_ in zp[:2]:
        targets.append((complex(r_), [zb, zb + 3j, complex(r_) + 3j, complex(r_)], 1j))
    Ms, gates = [], []
    for zt, route, off in targets[:4]:
        r = route[:-1] + [zt + off*rad]
        M, dc = loop_matrix(m, Yb, r, zt, rad, 0.0, rtol)
        Ms.append(M); gates.append(dict(target=str(zt), trace=abs(np.trace(M)), det=abs(np.linalg.det(M) - 1), c0_return=float(np.max(np.abs(dc)))))
    return stat(Ms), gates

if __name__ == '__main__':
    out = dict(grid={}, control={}, scaling={}, self_test=self_test()); print('hand-coded vs sympy max rel err', out['self_test'], flush=True)
    for E in (0.8, 0.7, 0.9):
        for a in (0.0, 0.01, 1/30, 0.1):
            S13, g13 = run_kerr(E, a, 1e-13); S11, _ = run_kerr(E, a, 1e-11)
            gok = all(g['trace'] <= 1e-9 and g['det'] <= 1e-10 and g['c0_return'] <= 1e-9 for g in g13)
            out['grid']['E=%s alpha=%.4g' % (E, a)] = dict(S_norm_extra=run_kerr.last_norm, S=S13, S_rtol11=S11, floor=abs(S13 - S11), gates_ok=gok, gates=g13)
            print('E', E, 'alpha %.4g' % a, '| S %.3e (rtol1e-11: %.3e, floor %.1e) gates %s | S_norm %.2e' % (S13, S11, abs(S13 - S11), gok, run_kerr.last_norm),
                  '| max trace %.1e c0ret %.1e' % (max(g['trace'] for g in g13), max(g['c0_return'] for g in g13)), flush=True)
        json.dump(out, open(os.path.join(HERE, '../results/v26_B8.json'), 'w'), indent=1, default=str)
    for a in (1e-3, 3e-3, 1e-2):
        S, _ = run_kerr(0.8, a, 1e-13); out['scaling'][a] = S; print('scaling alpha', a, 'S %.4e' % S, flush=True)
    xs = np.log(list(out['scaling'].keys())); ys = np.log(list(out['scaling'].values()))
    out['scaling_slope'] = float(np.polyfit(xs, ys, 1)[0]); print('log-log slope', out['scaling_slope'], flush=True)
    for E in (0.8, 0.7):
        S, g = run_control(E, 1e-13); out['control']['E=%s' % E] = dict(S=S, gates=g)
        print('CONTROL e=1-2/z+i/z^2 E', E, '| S %.3e' % S, '| traces', ['%.1e' % x['trace'] for x in g], flush=True)
    json.dump(out, open(os.path.join(HERE, '../results/v26_B8.json'), 'w'), indent=1, default=str)
