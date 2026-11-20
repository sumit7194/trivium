"""V23 (PREREGISTRATION.md): independent recomputation of the MN Melnikov potential harmonics L_n along Kerr's inclined
homoclinic orbit, in Mino time. Bridge code only: V17 g0_and_h (metric + d/dparam), own homoclinic and theta motion."""
import sys, os, json, math, time
import numpy as np, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V17_mn_first_order/code'))
import v17 as V17
X, Y = V17.X, V17.Y
mp.mp.dps = 30

def pieces(M, a, kind):
    """numpy callables (x, y) -> dicts of G0 (inverse Kerr metric) and G1 (first-order inverse-metric perturbation)."""
    if kind == 'sabotage':
        g0, _ = V17.g0_and_h(M, a, 'beta'); h = None
    else:
        g0, h = V17.g0_and_h(M, a, kind)
    K = V17.KEYS
    g0f = sp.lambdify((X, Y), [g0[k] for k in K], 'numpy')
    hf = sp.lambdify((X, Y), [h[k] for k in K], 'numpy') if h is not None else None
    def G0(x, y):
        tt, tp, pp, xx, yy = [np.broadcast_to(np.asarray(v, float), np.broadcast(x, y).shape) for v in g0f(x, y)]
        det = tt*pp - tp*tp
        return dict(tt=pp/det, tp=-tp/det, pp=tt/det, xx=1/xx, yy=1/yy)
    def G1(x, y):
        G = G0(x, y)
        if kind == 'sabotage':
            z = np.zeros(np.broadcast(x, y).shape); return dict(tt=x*y + z, tp=z, pp=z, xx=z, yy=z)
        htt, htp, hpp, hxx, hyy = [np.broadcast_to(np.asarray(v, float), np.broadcast(x, y).shape) for v in hf(x, y)]
        # -(G h G) on the (t, phi) block; diagonal (x, y) blocks
        a11, a12, a22 = G['tt'], G['tp'], G['pp']
        P11 = -(a11*(htt*a11 + htp*a12) + a12*(htp*a11 + hpp*a12))
        P12 = -(a11*(htt*a12 + htp*a22) + a12*(htp*a12 + hpp*a22))
        P22 = -(a12*(htt*a12 + htp*a22) + a22*(htp*a12 + hpp*a22))
        return dict(tt=P11, tp=P12, pp=P22, xx=-G['xx']**2*hxx, yy=-G['yy']**2*hyy)
    return G0, G1

def quad(G, E, L, px2, py2):   # H = 1/2 G^{ab} p_a p_b with p_t = -E, p_phi = L
    return 0.5*(G['tt']*E*E - 2*G['tp']*E*L + G['pp']*L*L + G['xx']*px2 + G['yy']*py2)

class Level:
    """Kerr (BL, +a, mu = 1) level with an unstable spherical orbit at r_u and theta libration amplitude z_m."""
    def __init__(self, M, a, ru, zm, guess):
        self.M, self.a, self.ru, self.zm = map(mp.mpf, (M, a, ru, zm))
        M, a, ru, zm = self.M, self.a, self.ru, self.zm
        def R(r, E, L, Q):
            D = r*r - 2*M*r + a*a; return (E*(r*r + a*a) - a*L)**2 - D*(r*r + (L - a*E)**2 + Q)
        def eqs(E, L, Q):
            return [R(ru, E, L, Q), mp.diff(lambda r: R(r, E, L, Q), ru),
                    Q - (Q + a*a*(1 - E*E) + L*L)*zm**2 + a*a*(1 - E*E)*zm**4]
        self.E, self.L, self.Q = mp.findroot(eqs, guess)
        E, L, Q = self.E, self.L, self.Q
        self.Rf = lambda r: R(r, E, L, Q)
        c = [E*E - 1, 2*M, a*a*(E*E - 1) - L*L - Q, 2*M*((a*E - L)**2 + Q), -a*a*Q]   # R polynomial, highest first
        q, rem = np.polydiv([float(v) for v in c], np.poly([float(ru), float(ru)]))
        # do it in mpmath for accuracy: synthetic division by (r - ru)^2
        cc = list(c)
        for _ in range(2):
            out = [cc[0]]
            for v in cc[1:-1]: out.append(v + out[-1]*ru)
            rem_ = cc[-1] + out[-1]*ru; cc = out
        self.rem = rem_
        roots = sorted([mp.re(z) for z in mp.polyroots(cc)])
        self.r4, self.rt = roots[0], roots[1]
        self.R2 = mp.diff(self.Rf, ru, 2); self.kap = mp.sqrt(self.R2/2)
        A, B = self.rt - ru, ru - self.r4; self.A, self.B = A, B
        self.k = mp.sqrt(M*M - a*a)
        self.zp2 = Q/(a*a*(1 - E*E)*zm*zm)
    def rh(self, lam):
        A, B, k = float(self.A), float(self.B), float(self.kap)
        return float(self.ru) + 2*A*B/((B - A) + (A + B)*np.cosh(k*lam))

def theta_motion(lev, N):
    """chi grid, z(chi), psi(chi), dpsi/dchi, Upsilon_theta; spectral integration of dlam/dchi."""
    a, E, zm, zp2 = (float(v) for v in (lev.a, lev.E, lev.zm, lev.zp2))
    chi = 2*np.pi*np.arange(N)/N
    g = 1/np.sqrt(a*a*(1 - E*E)*(zp2 - zm*zm*np.cos(chi)**2))
    c = np.fft.fft(g)/N; c0 = c[0].real
    n = np.fft.fftfreq(N, d=1/N); per = np.zeros(N, complex); nz = n != 0
    per[nz] = c[nz]/(1j*n[nz])
    lam = c0*chi + np.real(np.fft.ifft(per*N)) - np.real(np.sum(per))   # lambda(0) = 0
    Ups = 1/c0
    return chi, zm*np.cos(chi), Ups*lam, Ups*g, Ups

def F_vals(lev, G0, G1, r, z):
    M, a, E, L, Q, k = (float(v) for v in (lev.M, lev.a, lev.E, lev.L, lev.Q, lev.k))
    D = r*r - 2*M*r + a*a
    Rv = (E*(r*r + a*a) - a*L)**2 - D*(r*r + (L - a*E)**2 + Q)
    Zv = Q - (Q + a*a*(1 - E*E) + L*L)*z*z + a*a*(1 - E*E)*z**4
    px2 = k*k*np.maximum(Rv, 0)/D**2; py2 = np.maximum(Zv, 0)/(1 - z*z)**2
    x = (r - M)/k
    g0 = G0(x, z); g1 = G1(x, z)
    shell = np.max(np.abs(quad(g0, E, L, px2, py2) + 0.5))
    return (r*r + a*a*z*z)*quad(g1, E, L, px2, py2), shell

def harmonics(lev, kind, nlist, Nchi=256, dlam=None, Tfac=40.0):
    G0, G1 = pieces(float(lev.M), float(lev.a), kind)
    chi, z, psi, dpsi, Ups = theta_motion(lev, Nchi)
    kap = float(lev.kap); T = Tfac/kap; dlam = dlam or (2*np.pi/(2*max(nlist + [1])*Ups))/24
    lam = np.arange(0, T + dlam/2, dlam)
    r = lev.rh(lam)
    RR, ZZ = np.meshgrid(r, z, indexing='ij')
    Fv, shell = F_vals(lev, G0, G1, RR, ZZ)
    Fu, shell_u = F_vals(lev, G0, G1, np.full_like(z, float(lev.ru)), z)
    out = {}
    for n in nlist:
        w = np.exp(-1j*n*psi)*dpsi/Nchi                    # (1/2pi) * dchi = 1/N
        vn = Fv @ w; vnu = Fu @ w
        integ = (vn - vnu)*np.cos(n*Ups*lam)
        trap = dlam*(integ[0]/2 + integ[1:].sum())*2      # even in lambda: 2 * int_0^T
        out[n] = complex(trap)
    return out, dict(Ups=Ups, kap=kap, T=T, dlam=dlam, Nchi=Nchi, shell=max(shell, shell_u), npts=len(lam))

def gate_H1(lev):
    worst = 0
    for lam in np.linspace(-3, 3, 20)/float(lev.kap):
        rr = mp.mpf(lev.rh(lam)); d = mp.diff(lambda l: mp.mpf(lev.ru) + 2*lev.A*lev.B/((lev.B - lev.A) + (lev.A + lev.B)*mp.cosh(lev.kap*l)), lam)
        worst = max(worst, abs(d*d/lev.Rf(rr) - 1))
    return float(worst)

if __name__ == '__main__':
    res = {}
    base = Level(5, 3, 16, mp.mpf(1)/2, (mp.mpf('0.94'), mp.mpf('13'), mp.mpf('56')))
    res['level_base'] = dict(E=str(base.E), L=str(base.L), Q=str(base.Q), rt=str(base.rt), r4=str(base.r4), kap=str(base.kap),
                             rem=str(base.rem), H1=gate_H1(base))
    print('base level', res['level_base'], flush=True)
    for kind, ns in (('beta', [0, 2, 4, 6]), ('M', [2]), ('a', [2]), ('sabotage', [1, 2])):
        for Nchi, df in ((256, 1.0), (512, 0.5)):
            t0 = time.time()
            h, meta = harmonics(base, kind, ns, Nchi=Nchi, dlam=None if df == 1.0 else None)
            if df == 0.5:
                h, meta = harmonics(base, kind, ns, Nchi=Nchi, dlam=meta['dlam']*0.5)
            res[f'base_{kind}_N{Nchi}'] = dict({f'L{n}': [v.real, v.imag] for n, v in h.items()}, **meta, s=round(time.time() - t0, 1))
            print(kind, Nchi, {n: f'{v.real:.9e}' for n, v in h.items()}, 'shell %.1e' % meta['shell'], flush=True)
    h, meta = harmonics(base, 'beta', [2], Tfac=60.0)
    res['base_beta_T60'] = dict(L2=[h[2].real, h[2].imag], **meta); print('T60 L2', h[2].real, flush=True)
    lev8 = Level(5, 3, 16, mp.mpf('0.8'), (mp.mpf('0.977'), mp.mpf('11'), mp.mpf('150')))
    res['level_zm08'] = dict(E=str(lev8.E), L=str(lev8.L), Q=str(lev8.Q), H1=gate_H1(lev8))
    for Nchi in (256, 512):
        h, meta = harmonics(lev8, 'beta', [2], Nchi=Nchi)
        res[f'zm08_beta_N{Nchi}'] = dict(L2=[h[2].real, h[2].imag], **meta); print('zm0.8', Nchi, h[2].real, 'E', float(lev8.E), flush=True)
    json.dump(res, open(os.path.join(HERE, '../results/v23.json'), 'w'), indent=1, default=str)
