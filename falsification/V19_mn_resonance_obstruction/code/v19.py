"""V19 (PREREGISTRATION.md): Poincare resonance obstruction for a first-order deformation of Kerr, in Mino time.
F(q_r, q_th) = Sigma * H1 on a Kerr torus; resonant Fourier coefficient F_k (k . Upsilon = 0) nonzero => no smooth
first-order integral F0(J) + beta F1 with F0 depending on Carter's Q.  Metric pieces from the bridge's V9 MN
transcription via V17's symbolic g0 / h (MN chart x, y: r = M + k x, y = cos theta)."""
import sys, os, json, time
import mpmath as mp
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V17_mn_first_order/code'))
import v17 as V17
mp.mp.dps = 40
X, Y = V17.X, V17.Y

# ---------------------------------------------------------------- metric pieces as mpmath callables
def pieces(M, a, case):
    """Returns (G0f, G1f): callables (x, y) -> dict of inverse-metric components (tt, tp, pp, xx, yy)."""
    if case in ('mn', 'dM', 'da'):
        kind = {'mn': 'beta', 'dM': 'M', 'da': 'a'}[case]
        g0, h = V17.g0_and_h(M, a, kind)
    else:
        g0, _ = V17.g0_and_h(M, a, 'beta'); h = None
    keys = V17.KEYS
    g0f = sp.lambdify((X, Y), [g0[k] for k in keys], 'mpmath')
    if case == 'null':   # G1 = -L_xi G0 exactly, xi = (x^3/3) d_x + y^2 d_y (V17's field); computed symbolically
        tt, tp, pp, xx, yy = (g0[k] for k in keys)
        det = tt*pp - tp**2
        G0s = {'tt': pp/det, 'tp': -tp/det, 'pp': tt/det, 'xx': 1/xx, 'yy': 1/yy}
        xix, xiy = X**3/3, Y**2
        lie = {k: xix*sp.diff(v, X) + xiy*sp.diff(v, Y) for k, v in G0s.items()}
        lie['xx'] -= 2*G0s['xx']*sp.diff(xix, X); lie['yy'] -= 2*G0s['yy']*sp.diff(xiy, Y)
        g1f = sp.lambdify((X, Y), [-lie[k] for k in ('tt', 'tp', 'pp', 'xx', 'yy')], 'mpmath')
        def G1f(x, y): return dict(zip(('tt', 'tp', 'pp', 'xx', 'yy'), g1f(x, y)))
    elif case == 'sabotage':
        def G1f(x, y): return dict(tt=x*y, tp=mp.mpf(0), pp=mp.mpf(0), xx=mp.mpf(0), yy=mp.mpf(0))
    else:
        hf = sp.lambdify((X, Y), [h[k] for k in keys], 'mpmath')
        def G1f(x, y):
            G = G0f(x, y); htt, htp, hpp, hxx, hyy = hf(x, y)
            Hm = mp.matrix([[htt, htp], [htp, hpp]]); Gm = mp.matrix([[G['tt'], G['tp']], [G['tp'], G['pp']]])
            P = -(Gm * Hm * Gm)
            return dict(tt=P[0, 0], tp=P[0, 1], pp=P[1, 1], xx=-G['xx']**2*hxx, yy=-G['yy']**2*hyy)
    def G0f(x, y):
        tt, tp, pp, xx, yy = g0f(x, y); det = tt*pp - tp**2
        return dict(tt=pp/det, tp=-tp/det, pp=tt/det, xx=1/xx, yy=1/yy)
    return G0f, G1f

def quad_form(G, E, Lz, px2, py2):
    # p_t = -E, p_phi = Lz;  H = 1/2 G^{ab} p_a p_b  (diagonal x, y block)
    return (G['tt']*E**2 - 2*G['tp']*E*Lz + G['pp']*Lz**2 + G['xx']*px2 + G['yy']*py2) / 2

# ---------------------------------------------------------------- Kerr geodesics (BL, mu = 1), Mino time
class Torus:
    def __init__(self, M, a, rp, ra, zm, s=+1):
        self.M, self.a, self.rp, self.ra, self.zm = map(mp.mpf, (M, a, rp, ra, zm)); self.s = s
        self.solve_ELQ(); self.roots(); self.freqs()
    def R(self, r):
        M, a, E, L, Q = self.M, self.a, self.E, self.L, self.Q
        D = r*r - 2*M*r + a*a
        return (E*(r*r + a*a) - a*L)**2 - D*(r*r + (L - a*E)**2 + Q)
    def Zf(self, z):
        a, E, L, Q = self.a, self.E, self.L, self.Q
        return Q - (Q + a*a*(1 - E*E) + L*L)*z*z + a*a*(1 - E*E)*z**4
    def solve_ELQ(self):
        M, a, zm = self.M, self.a, self.zm
        p = 2*self.ra*self.rp/(self.ra + self.rp); e = (self.ra - self.rp)/(self.ra + self.rp)
        E0 = mp.sqrt(((p - 2*M)**2 - 4*M*M*e*e)/(p*(p - 3*M - e*e*M))); Lt = mp.sqrt(p*p*M/(p - 3*M - e*e*M))
        def eqs(E, L):
            Q = zm*zm*(a*a*(1 - E*E) + L*L/(1 - zm*zm))
            self.E, self.L, self.Q = E, L, Q
            return [self.R(self.rp), self.R(self.ra)]
        E, L = mp.findroot(eqs, (E0, self.s*Lt*mp.sqrt(1 - zm*zm)))
        self.E, self.L = E, L; self.Q = zm*zm*(a*a*(1 - E*E) + L*L/(1 - zm*zm))
        assert abs(self.Zf(zm)) < mp.mpf(10)**(-30)
    def roots(self):
        M, a, E, L, Q = self.M, self.a, self.E, self.L, self.Q
        c4 = E*E - 1; c3 = 2*M; c2 = a*a*(E*E - 1) - L*L - Q; c1 = 2*M*((a*E - L)**2 + Q); c0 = -a*a*Q
        rts = sorted([mp.re(x) for x in mp.polyroots([c4, c3, c2, c1, c0], maxsteps=200, extraprec=200)], reverse=True)
        self.r1, self.r2, self.r3, self.r4 = rts
        assert abs(self.r1 - self.ra) < mp.mpf(10)**(-25) and abs(self.r2 - self.rp) < mp.mpf(10)**(-25), (rts, self.ra, self.rp)
        A = a*a*(1 - E*E); self.zp2 = (Q + A + L*L)/A - self.zm**2 if A != 0 else mp.inf   # z_+^2 (product root)
    def r_of(self, chi): return (self.ra + self.rp)/2 - (self.ra - self.rp)/2*mp.cos(chi)
    def dlam_dchi(self, chi):
        r = self.r_of(chi); return 1/mp.sqrt((1 - self.E**2)*(r - self.r3)*(r - self.r4))
    def z_of(self, psi): return self.zm*mp.cos(psi)
    def dlam_dpsi(self, psi):
        z = self.z_of(psi); return 1/mp.sqrt(self.a**2*(1 - self.E**2)*(self.zp2 - z*z))
    def freqs(self):
        self.Lr = mp.quad(self.dlam_dchi, [0, mp.pi]); self.Lt = mp.quad(self.dlam_dpsi, [0, mp.pi])
        self.Ur = mp.pi/self.Lr; self.Ut = mp.pi/self.Lt
    def ratio(self): return self.Ur/self.Ut
    def angle_grid(self, N, which):
        """chi_j (or psi_j) at uniform Mino angle q_j = 2 pi j / N: solve Upsilon * lambda(chi) = q."""
        f, U = (self.dlam_dchi, self.Ur) if which == 'r' else (self.dlam_dpsi, self.Ut)
        out = []; prev = mp.mpf(0); lam_prev = mp.mpf(0)
        for j in range(N):
            q = 2*mp.pi*j/N
            if j == 0: out.append(mp.mpf(0)); continue
            g = lambda c: U*(lam_prev + mp.quad(f, [prev, c])) - q
            c = mp.findroot(g, prev + 2*mp.pi/N)
            lam_prev = lam_prev + mp.quad(f, [prev, c]); prev = c; out.append(c)
        return out

def tune(M, a, rp, zm, target, ra0, s=+1):
    f = lambda ra: Torus(M, a, rp, ra, zm, s).ratio() - target
    ra = mp.findroot(f, mp.mpf(ra0), tol=mp.mpf(10)**(-30))
    return Torus(M, a, rp, ra, zm, s)

# ---------------------------------------------------------------- the obstruction statistic
def evaluate(T, G0f, G1f, N, k, check_shell=True):
    M, a, E, L = T.M, T.a, T.E, T.L
    kk = mp.sqrt(M*M - a*a)
    chis = T.angle_grid(N, 'r'); psis = T.angle_grid(N, 't')
    rs = [T.r_of(c) for c in chis]; zs = [T.z_of(p) for p in psis]
    F = [[None]*N for _ in range(N)]; shell = mp.mpf(0)
    for i, r in enumerate(rs):
        D = r*r - 2*M*r + a*a; Rv = T.R(r); x = (r - M)/kk
        px2 = kk*kk*max(Rv, mp.mpf(0))/D**2
        for j, z in enumerate(zs):
            Zv = T.Zf(z); py2 = max(Zv, mp.mpf(0))/(1 - z*z)**2
            G0 = G0f(x, z); G1 = G1f(x, z)
            if check_shell: shell = max(shell, abs(quad_form(G0, E, L, px2, py2) + mp.mpf(1)/2))
            F[i][j] = (r*r + a*a*z*z)*quad_form(G1, E, L, px2, py2)
    def coef(kr, kt):
        s = mp.mpf(0)
        for i in range(N):
            for j in range(N):
                s += F[i][j]*mp.cos(2*mp.pi*(kr*i + kt*j)/N)   # F even in each angle -> cosine coefficients
        return s/N**2
    Fk = coef(*k); norm = max(abs(coef(0, 0)), abs(coef(1, 0)), abs(coef(0, 1)))
    return dict(Fk=Fk, norm=norm, rho=(abs(Fk)/norm if norm != 0 else mp.mpf(0)), shell=shell)

TORI = {  # name: (r_p in units of M, z_max, resonance p/q, k)
    'T1_12': (4, mp.mpf('0.5'), mp.mpf(1)/2, (2, -1)),
    'T2_12': (6, mp.mpf('0.3'), mp.mpf(1)/2, (2, -1)),
    'T1_23': (4, mp.mpf('0.5'), mp.mpf(2)/3, (3, -2)),
    'T2_23': (6, mp.mpf('0.3'), mp.mpf(2)/3, (3, -2)),
}
