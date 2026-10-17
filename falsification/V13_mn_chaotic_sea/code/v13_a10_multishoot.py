"""V13 amendment A10: multiple-shooting confirmation of the A9-scoped transition-graph edges (pre-registered in
PREREGISTRATION.md, A10, before any rerun). New additive script; nothing existing is edited. It imports SectionMap / RT
(v13_upo), POINTS / RES (v13_screen), DMAX / NSEG0 (v13_manifolds) and make_margin / seg_cross_idx / tarjan
(v13_a9_confirm) unchanged.

GENERIC CORE (the same functions serve MN and the Henon-Heiles positive control): a "system" object offers
P(w, n, rtol) -> section point after n returns (or None), J(w, n, rtol) -> exact variational 2x2 Jacobian of P^n,
sc = (xscale, pscale) for the scaled section metric, and the reversor G(x, p) = (x, -p).
An edge is (z_i, v_i, pow_i, a ; z_g, v_g, pow_g, b): W^u(i) = z_i + s v_i pushed forward a segments of P^{pow_i};
W^s(j) = G W^u(gj), gj = G-partner of j, = G of z_g + s' v_g pushed forward b segments of P^{pow_g}.
  unknowns  X = [s, w_1 .. w_a, s', u_1 .. u_b]   (2 + 2a + 2b reals)
  equations P^{pow_i}(w_{k-1}) - w_k = 0 (k = 1..a, w_0 = z_i + s v_i), P^{pow_g}(u_{k-1}) - u_k = 0 (k = 1..b,
            u_0 = z_g + s' v_g), and the final match w_a - G u_b = 0.                    (2a + 2b + 2 equations)
Newton: per-segment Jacobians from J (exact variational), d w_0/ds = v_i, d u_0/ds' = v_g; the bordered system is
row-scaled by 1/sc and column-scaled (points by sc, s by 1/|v/sc|) and solved by numpy lstsq (SVD) on the full
system; damped by step halving on the 2-norm of the scaled residual; iterated until no further decrease.

CHECKS (A10): 1 inherited from A9;  2 max per-equation scaled residual (every segment AND the final match) <= 1e-10;
3 angle between t_u = J_a..J_1 v_i and t_s = G J'_b..J'_1 v_g at the crossing >= 0.01 rad (raw (x, p_x) metric as
A9/the graph; scaled-metric angle reported); 4 every segment orbit (w_{k-1} over pow_i returns, u_{k-1} over pow_g
returns) completes in D_B9 (SectionMap.P(..., b9=True) not None), margins from v13_a9_confirm.make_margin;
5 the refined crossing point w_a agrees to <= 1e-6 (scaled) between independent solves at rtol 1e-13 and 1e-12 (map
and variational integrators both at that rtol, atol = 1e-3 rtol, from the same initial guess; z, v unchanged);
6 condition number of the scaled MS Jacobian reported; final Newton step (computed at the solution) scaled 2-norm
<= 1e-8.  CONFIRMED_MS iff 1-6 all hold.

rtol: SectionMap.P hard-codes RT = 1e-13 (atol 1e-16). It is not called for the solves; instead the SAME integrator
objects SectionMap builds with v13_orbit.make (S.base[0], and S.b9[0] for check 4) are called with rtol and atol =
1e-3 rtol, exactly as SectionMap.P does at 1e-13, and the variational map S.sj is called with rtol= (its own
argument; atol = 1e-3 rtol inside). This is what A9 did too.

CONTROLS (run first; A10 is void if either fails): Henon-Heiles H = (px^2+py^2+x^2+y^2)/2 + x^2 y - y^3/3, section
x = 0, px > 0, coordinates (y, py), with an own numba DOP853 section integrator (same tableau, step control and
dense-output bisection as v13_orbit, 4-dim map and 20-dim variational system); MN negative controls.
Usage: python v13_a10_multishoot.py controls | C0 | F5R   [--workers 2] [--edges i-j,...] [--tag suffix]"""
import sys, os, json, math, time, platform, subprocess, argparse
import numpy as np, sympy as sp, numba
import scipy.integrate._ivp.dop853_coefficients as DC
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_upo import SectionMap, RT
from v13_screen import POINTS, RES
from v13_manifolds import DMAX, NSEG0
from v13_a9_confirm import make_margin, seg_cross_idx, tarjan

RT2 = 1e-12
RES_MAX, ANG_MIN, PT_TOL, STEP_MAX = 1e-10, 0.01, 1e-6, 1e-8
GM = np.diag([1.0, -1.0]); GV = np.array([1.0, -1.0])
G = lambda a: np.asarray(a)*GV
A9F = {'C0': 'v13_a9_confirm_C0.json', 'F5R': 'v13_a9_confirm_F5R.json'}

# =============================================================== generic DOP853 section integrator (HH control)
NS = DC.N_STAGES
A_ = np.ascontiguousarray(DC.A[:NS, :NS]); B_ = DC.B.copy(); E3_ = DC.E3.copy(); E5_ = DC.E5.copy(); D_ = DC.D.copy()
AX_ = np.ascontiguousarray(DC.A[NS + 1:])

def make_section_run(rhs, ND, comp):
    """Same DOP853 stages, error norm, step control, initial step and dense-output bisection as v13_orbit.integrate,
    for an ND-dim system; the section is the up-crossing of state component `comp` through 0. Returns
    run(y0, n, rtol, atol, max_steps) -> (ok, state at n-th crossing, rhs there, steps)."""
    @numba.njit
    def dense_eval(F, y_old, s, out):
        for k in range(ND): out[k] = 0.0
        for i in range(7):
            f = F[6 - i]
            for k in range(ND): out[k] += f[k]
            fac = s if i % 2 == 0 else 1.0 - s
            for k in range(ND): out[k] *= fac
        for k in range(ND): out[k] += y_old[k]

    @numba.njit
    def root(F, y_old, s_lo, s_hi):
        tmp = np.empty(ND)
        dense_eval(F, y_old, s_lo, tmp); flo = tmp[comp]
        for _ in range(60):
            sm = 0.5*(s_lo + s_hi); dense_eval(F, y_old, sm, tmp); fm = tmp[comp]
            if (fm < 0) == (flo < 0): s_lo = sm; flo = fm
            else: s_hi = sm
        return 0.5*(s_lo + s_hi)

    @numba.njit
    def run(y0, n, rtol, atol, max_steps):
        zr = np.zeros(ND); fr = np.zeros(ND)
        y = y0.copy(); f = np.empty(ND); rhs(y, f)
        K = np.zeros((16, ND)); ynew = np.empty(ND); fnew = np.empty(ND); tmp = np.empty(ND); F = np.zeros((7, ND))
        sc = atol + np.abs(y)*rtol
        d0 = math.sqrt(np.mean((y/sc)**2)); d1 = math.sqrt(np.mean((f/sc)**2))
        h0 = 1e-6 if (d0 < 1e-5 or d1 < 1e-5) else 0.01*d0/d1
        y1 = y + h0*f; f1 = np.empty(ND); rhs(y1, f1)
        d2 = math.sqrt(np.mean(((f1 - f)/sc)**2))/h0
        h1 = max(1e-6, h0*1e-3) if (d1 <= 1e-15 and d2 <= 1e-15) else (0.01/max(d1, d2))**(1.0/8.0)
        h = min(100*h0, h1)
        ncross = 0; steps = 0
        while steps < max_steps:
            rejected = False
            while True:
                hh = h
                K[0] = f
                for s in range(1, NS):
                    for k in range(ND):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*A_[s, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(ND):
                    acc = 0.0
                    for j in range(NS): acc += K[j, k]*B_[j]
                    ynew[k] = y[k] + hh*acc
                rhs(ynew, fnew); K[NS] = fnew
                e5 = 0.0; e3 = 0.0
                for k in range(ND):
                    sck = atol + max(abs(y[k]), abs(ynew[k]))*rtol
                    a5 = 0.0; a3 = 0.0
                    for j in range(NS + 1): a5 += K[j, k]*E5_[j]; a3 += K[j, k]*E3_[j]
                    e5 += (a5/sck)**2; e3 += (a3/sck)**2
                en = 0.0 if (e5 == 0.0 and e3 == 0.0) else hh*e5/math.sqrt((e5 + 0.01*e3)*ND)
                if not math.isfinite(en): en = 1e300
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return False, zr, fr, steps
            steps += 1
            if not math.isfinite(ynew[0]) or abs(ynew[0]) > 1e6: return False, zr, fr, steps
            if y[comp] < 0.0 and ynew[comp] >= 0.0:
                ncross += 1
                if ncross == n:
                    for s in range(NS + 1, 16):
                        for k in range(ND):
                            acc = 0.0
                            for j in range(s): acc += K[j, k]*AX_[s - NS - 1, j]
                            tmp[k] = y[k] + acc*hh
                        rhs(tmp, K[s])
                    for k in range(ND):
                        dy = ynew[k] - y[k]
                        F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                        for r in range(4):
                            acc = 0.0
                            for j in range(16): acc += D_[r, j]*K[j, k]
                            F[3 + r, k] = hh*acc
                    su = root(F, y, 0.0, 1.0); dense_eval(F, y, su, zr); rhs(zr, fr)
                    return True, zr, fr, steps
            for k in range(ND): y[k] = ynew[k]; f[k] = fnew[k]
        return False, zr, fr, steps
    return run

@numba.njit
def hh4(z, out):
    x, y = z[0], z[1]
    out[0] = z[2]; out[1] = z[3]; out[2] = -x - 2.0*x*y; out[3] = -y - x*x + y*y

@numba.njit
def hh20(z, out):
    x, y = z[0], z[1]
    out[0] = z[2]; out[1] = z[3]; out[2] = -x - 2.0*x*y; out[3] = -y - x*x + y*y
    J = np.zeros((4, 4))
    J[0, 2] = 1.0; J[1, 3] = 1.0
    J[2, 0] = -1.0 - 2.0*y; J[2, 1] = -2.0*x; J[3, 0] = -2.0*x; J[3, 1] = -1.0 + 2.0*y
    for i in range(4):
        for j in range(4):
            acc = 0.0
            for k in range(4): acc += J[i, k]*z[4 + 4*k + j]
            out[4 + 4*i + j] = acc

class HHSys:
    """Henon-Heiles section map on x = 0, px > 0, coordinates (y, py). Reversor G(y, py) = (y, -py) (x -> -x composed
    with time reversal). P from the 4-dim integrator, J from the 20-dim variational one (as P/sj in MN)."""
    name = 'HH'
    def __init__(self, E):
        self.E = float(E)
        self.r4 = make_section_run(hh4, 4, 0); self.r20 = make_section_run(hh20, 20, 0)
        # bounded component of {y : V(0, y) <= E} containing y = 0 (for E = 1/6: [-1/2, 1], touching the saddle y = 1)
        ys = np.linspace(-0.6, 1.2, 180001); ok = (ys**2 - 2*ys**3/3) <= 2*self.E
        i0 = int(np.argmin(np.abs(ys))); lo = i0; hi = i0
        while lo > 0 and ok[lo - 1]: lo -= 1
        while hi < len(ys) - 1 and ok[hi + 1]: hi += 1
        ylo, yhi = ys[lo], ys[hi]; pmax = math.sqrt(2*self.E)
        self.sc = np.array([yhi - ylo, 2*pmax]); self.yrange = (float(ylo), float(yhi)); self.pmax = pmax
    def px0(self, y, py):
        r = 2*self.E - py*py - y*y + 2*y**3/3
        return math.sqrt(r) if r > 0 else None
    def ham(self, z):
        x, y, px, py = z[:4]; return 0.5*(px*px + py*py + x*x + y*y) + x*x*y - y**3/3
    def P(self, w, n, rtol):
        if n == 0: return np.array(w, float)
        p = self.px0(w[0], w[1])
        if p is None: return None
        ok, zr, fr, st = self.r4(np.array([0.0, w[0], p, w[1]]), n, rtol, rtol*1e-3, 50_000_000)
        return np.array([zr[1], zr[3]]) if ok else None
    def J(self, w, n, rtol):
        if n == 0: return np.eye(2)
        p = self.px0(w[0], w[1])
        if p is None: return None
        y0 = np.zeros(20); y0[:4] = [0.0, w[0], p, w[1]]
        for i in range(4): y0[4 + 5*i] = 1.0
        ok, zr, fr, st = self.r20(y0, n, rtol, rtol*1e-3, 200_000_000)
        if not ok: return None
        y, py = w; Hy = y - y*y; Hpy = py; Hpx = p
        V = np.zeros((4, 2)); V[1, 0] = 1.0; V[2, 0] = -Hy/Hpx; V[3, 1] = 1.0; V[2, 1] = -Hpy/Hpx
        Phi = zr[4:].reshape(4, 4); wv = Phi @ V
        dt = -wv[0]/fr[0]; dz = wv + np.outer(fr[:4], dt)
        return dz[[1, 3], :]
    def energy_drift(self, w, n, rtol):
        p = self.px0(w[0], w[1]); ok, zr, _, _ = self.r4(np.array([0.0, w[0], p, w[1]]), n, rtol, rtol*1e-3, 50_000_000)
        return abs(self.ham(zr) - self.E) if ok else None

class MNSys:
    """MN section map: S.base[0] (v13_orbit.make, base domain) at a given rtol, S.sj (v13_var) for J."""
    name = 'MN'
    def __init__(self, S, sc):
        self.S = S; self.sc = np.asarray(sc, float)
    def P(self, w, n, rtol):
        if n == 0: return np.array(w, float)
        oc, nc, tau, drift, steps, sec = self.S.base[0](float(w[0]), float(w[1]), n, rtol, rtol*1e-3, 1e12, 50_000_000)
        return np.array([sec[n - 1, 0], sec[n - 1, 1]]) if nc >= n else None
    def J(self, w, n, rtol):
        if n == 0: return np.eye(2)
        _, J = self.S.sj(float(w[0]), float(w[1]), n, rtol=rtol)
        return J

# =============================================================== generic multiple shooting
def angle(t1, t2):
    return math.atan2(abs(t1[0]*t2[1] - t1[1]*t2[0]), abs(t1 @ t2))

class Edge:
    def __init__(self, zi, vi, pi, a, zg, vg, pg, b):
        self.zi, self.vi, self.pi, self.a = np.asarray(zi, float), np.asarray(vi, float), int(pi), int(a)
        self.zg, self.vg, self.pg, self.b = np.asarray(zg, float), np.asarray(vg, float), int(pg), int(b)
        self.n = 2 + 2*self.a + 2*self.b
        self.iS, self.iSp = 0, 1 + 2*self.a          # positions of s and s' in X
    def unpack(self, X):
        a, b = self.a, self.b
        s = X[0]; w = [self.zi + s*self.vi] + [X[1 + 2*k:3 + 2*k] for k in range(a)]
        o = self.iSp; sp_ = X[o]; u = [self.zg + sp_*self.vg] + [X[o + 1 + 2*k:o + 3 + 2*k] for k in range(b)]
        return s, w, sp_, u
    def col_w(self, k): return 1 + 2*(k - 1)        # column of w_k (k >= 1)
    def col_u(self, k): return self.iSp + 1 + 2*(k - 1)

def ms_initial(sy, E, s, sp_, rtol):
    """Forward propagation from (s, s') (single-shooting trajectory) as the MS initial guess."""
    X = np.zeros(E.n); X[E.iS] = s; X[E.iSp] = sp_
    w = E.zi + s*E.vi
    for k in range(1, E.a + 1):
        w = sy.P(w, E.pi, rtol)
        if w is None: return None
        X[E.col_w(k):E.col_w(k) + 2] = w
    u = E.zg + sp_*E.vg
    for k in range(1, E.b + 1):
        u = sy.P(u, E.pg, rtol)
        if u is None: return None
        X[E.col_u(k):E.col_u(k) + 2] = u
    return X

def ms_residual(sy, E, X, rtol):
    """Scaled residual vector (2a + 2b + 2) and the per-equation scaled norms (segments W^u, W^s, then the match)."""
    s, w, sp_, u = E.unpack(X); sc = sy.sc; R = []; seg = []
    for k in range(1, E.a + 1):
        p = sy.P(w[k - 1], E.pi, rtol)
        if p is None: return None, None
        r = (p - w[k])/sc; R.append(r); seg.append(float(np.hypot(*r)))
    for k in range(1, E.b + 1):
        p = sy.P(u[k - 1], E.pg, rtol)
        if p is None: return None, None
        r = (p - u[k])/sc; R.append(r); seg.append(float(np.hypot(*r)))
    r = (w[E.a] - G(u[E.b]))/sc; R.append(r); seg.append(float(np.hypot(*r)))
    return np.concatenate(R), seg

def ms_jacobian(sy, E, X, rtol):
    """Raw Jacobian (rows: equations in raw units; columns: raw unknowns) and the segment-propagated tangents."""
    s, w, sp_, u = E.unpack(X); Jm = np.zeros((E.n, E.n)); r = 0
    tu = E.vi.copy()
    for k in range(1, E.a + 1):
        Jk = sy.J(w[k - 1], E.pi, rtol)
        if Jk is None: return None, None, None
        if k == 1: Jm[r:r + 2, E.iS] += Jk @ E.vi
        else: Jm[r:r + 2, E.col_w(k - 1):E.col_w(k - 1) + 2] += Jk
        Jm[r:r + 2, E.col_w(k):E.col_w(k) + 2] -= np.eye(2); tu = Jk @ tu; r += 2
    ts = E.vg.copy()
    for k in range(1, E.b + 1):
        Jk = sy.J(u[k - 1], E.pg, rtol)
        if Jk is None: return None, None, None
        if k == 1: Jm[r:r + 2, E.iSp] += Jk @ E.vg
        else: Jm[r:r + 2, E.col_u(k - 1):E.col_u(k - 1) + 2] += Jk
        Jm[r:r + 2, E.col_u(k):E.col_u(k) + 2] -= np.eye(2); ts = Jk @ ts; r += 2
    if E.a > 0: Jm[r:r + 2, E.col_w(E.a):E.col_w(E.a) + 2] += np.eye(2)
    else: Jm[r:r + 2, E.iS] += E.vi
    if E.b > 0: Jm[r:r + 2, E.col_u(E.b):E.col_u(E.b) + 2] -= GM
    else: Jm[r:r + 2, E.iSp] -= GM @ E.vg
    return Jm, tu, G(ts)

def scalings(sy, E):
    sc = sy.sc; Dr = np.tile(1.0/sc, E.n//2)
    Dc = np.tile(sc, E.n//2).astype(float)
    Dc[E.iS] = 1.0/np.linalg.norm(E.vi/sc); Dc[E.iSp] = 1.0/np.linalg.norm(E.vg/sc)
    return Dr, Dc

def ms_solve(sy, E, X0, rtol, fix_s=False, it_max=40):
    """Damped Newton (Gauss-Newton if fix_s: the s column is removed and s held at X0[0]) on the MS system.
    Returns the solution record, including the Newton step computed AT the final iterate (check 6)."""
    t0 = time.time()
    Dr, Dc = scalings(sy, E)
    keep = np.arange(E.n) if not fix_s else np.array([c for c in range(E.n) if c != E.iS])
    X = X0.copy(); R, seg = ms_residual(sy, E, X, rtol)
    if R is None: return dict(ok=False, why='map undefined at initial guess')
    hist = [dict(norm2=float(np.linalg.norm(R)), maxseg=max(seg))]; nacc = 0; stall = 0; why = 'it_max'
    def step_at(X, R):
        Jm, tu, ts = ms_jacobian(sy, E, X, rtol)
        if Jm is None: return None
        Jh = (Dr[:, None]*Jm*Dc[None, :])[:, keep]
        dh, _, rank, sv = np.linalg.lstsq(Jh, -R, rcond=None)
        dX = np.zeros(E.n); dX[keep] = Dc[keep]*dh
        Jraw = Jm[:, keep]; svr = np.linalg.svd(Jraw, compute_uv=False)
        return dict(dX=dX, dh=dh, rank=int(rank), sv=sv, cond=float(sv[0]/sv[-1]) if sv[-1] > 0 else float('inf'),
                    cond_raw=float(svr[0]/svr[-1]) if svr[-1] > 0 else float('inf'), tu=tu, ts=ts)
    for it in range(it_max):
        if np.linalg.norm(R) == 0.0: why = 'zero residual'; break
        st = step_at(X, R)
        if st is None: why = 'variational failed'; break
        lam = 1.0; acc = False; r0 = np.linalg.norm(R)
        while lam >= 1.0/1024:
            Xn = X + lam*st['dX']; Rn, segn = ms_residual(sy, E, Xn, rtol)
            if Rn is not None and np.linalg.norm(Rn) < r0: acc = True; break
            lam *= 0.5
        if not acc: why = 'no decrease (noise floor or stall)'; break
        nacc += 1
        stall = stall + 1 if np.linalg.norm(Rn) > 0.5*r0 else 0
        X, R, seg = Xn, Rn, segn
        hist.append(dict(norm2=float(np.linalg.norm(R)), maxseg=max(seg), lam=lam, step_scaled=float(np.linalg.norm(lam*st['dh']))))
        if stall >= 4: why = 'stalled (4 steps with < 2x decrease)'; break
    fin = step_at(X, R)
    if fin is None: return dict(ok=False, why='variational failed at solution', hist=hist)
    s, w, sp_, u = E.unpack(X)
    tu, ts = fin['tu'], fin['ts']; sc = sy.sc
    return dict(ok=True, why_stop=why, iters_accepted=nacc, hist=hist, s=float(s), sp=float(sp_),
                X=X.tolist(), point=w[E.a].tolist(), point_other=G(u[E.b]).tolist(),
                seg_res=seg, max_seg_res=float(max(seg)), res_norm2=float(np.linalg.norm(R)),
                final_step_scaled_2norm=float(np.linalg.norm(fin['dh'])), final_step_scaled_max=float(np.max(np.abs(fin['dh']))),
                final_step_raw_2norm=float(np.linalg.norm(fin['dX'])), final_step_ds=float(fin['dX'][E.iS]),
                final_step_dsp=float(fin['dX'][E.iSp]),
                cond_scaled=fin['cond'], cond_raw=fin['cond_raw'], rank=fin['rank'], sv_min=float(fin['sv'][-1]),
                sv_max=float(fin['sv'][0]), n_unknowns=int(len(keep)), n_equations=int(E.n),
                t_u=tu.tolist(), t_s=ts.tolist(), ang_raw=angle(tu, ts), ang_scaled=angle(tu/sc, ts/sc),
                seconds=time.time() - t0)

def scaled_dist(sy, p, q): return float(math.hypot((p[0] - q[0])/sy.sc[0], (p[1] - q[1])/sy.sc[1]))

def ms_confirm(sy, E, s0, sp0, reparam=True):
    """Registered checks 2, 3, 5, 6 for one edge (checks 1 and 4 are added by the caller). Supplementary (not
    registered): the same solve with one extra segment on each side, seeds s/Lambda_i, s'/Lambda_g (Lambda = the
    eigenvalue of P^pow), whose crossing point must agree if the local linear W^u approximation is adequate."""
    rec = {}
    X0 = ms_initial(sy, E, s0, sp0, RT)
    if X0 is None: rec.update(ok=False, why='initial propagation left the map domain'); return rec
    R0, seg0 = ms_residual(sy, E, X0, RT); rec['initial_max_seg_res'] = max(seg0)
    n13 = ms_solve(sy, E, X0, RT); rec['ms_13'] = n13
    X0b = ms_initial(sy, E, s0, sp0, RT2)
    n12 = ms_solve(sy, E, X0b, RT2) if X0b is not None else dict(ok=False, why='initial propagation failed at 1e-12')
    rec['ms_12'] = n12
    rec['ok'] = bool(n13['ok'])
    rec['check2'] = bool(n13['ok'] and n13['max_seg_res'] <= RES_MAX)
    rec['check3'] = bool(n13['ok'] and n13['ang_raw'] >= ANG_MIN)
    rec['check3_scaled_metric'] = bool(n13['ok'] and n13['ang_scaled'] >= ANG_MIN)
    if n13['ok'] and n12['ok']:
        rec['point_13_vs_12_scaled'] = scaled_dist(sy, n13['point'], n12['point'])
        rec['newton_steps'] = [n13['iters_accepted'], n12['iters_accepted']]
        rec['check5'] = bool(rec['point_13_vs_12_scaled'] <= PT_TOL and min(rec['newton_steps']) >= 1)
        rec['s_rel_13_12'] = abs(n13['s'] - n12['s'])/abs(n13['s']) if n13['s'] != 0 else None
        rec['sp_rel_13_12'] = abs(n13['sp'] - n12['sp'])/abs(n13['sp']) if n13['sp'] != 0 else None
        rec['max_seg_res_12'] = n12['max_seg_res']
    else: rec['check5'] = False
    rec['check6'] = bool(n13['ok'] and n13['final_step_scaled_2norm'] <= STEP_MAX)
    rec['check6_raw_norm_also'] = bool(n13['ok'] and n13['final_step_raw_2norm'] <= STEP_MAX)
    if n13['ok'] and reparam:
        lam_i = E.lam_i; lam_g = E.lam_g
        Li = lam_i if lam_i > 0 else lam_i*lam_i; Lg = lam_g if lam_g > 0 else lam_g*lam_g
        E2 = Edge(E.zi, E.vi, E.pi, E.a + 1, E.zg, E.vg, E.pg, E.b + 1)
        Xr = ms_initial(sy, E2, n13['s']/Li, n13['sp']/Lg, RT)
        if Xr is None: rec['diag_reparam'] = dict(ok=False, why='initial propagation failed')
        else:
            nr = ms_solve(sy, E2, Xr, RT)
            rec['diag_reparam'] = dict(ok=nr['ok'], max_seg_res=nr.get('max_seg_res'), iters=nr.get('iters_accepted'),
                                       point_vs_primary_scaled=scaled_dist(sy, nr['point'], n13['point']) if nr['ok'] else None,
                                       ang_raw=nr.get('ang_raw'), step=nr.get('final_step_scaled_2norm'), cond=nr.get('cond_scaled'))
    if n13['ok']:
        rec['diag_noise_floor'] = segment_noise(sy, E, n13)
        if E.pi > 1 or E.pg > 1:
            rec['diag_single_return'] = single_return_solve(sy, E, s0, sp0, n13)
    if n13['ok']:
        # supplementary: exact-variational vs central-difference derivative of the first segment on each side
        fd = {}
        for nm, z, v, p, s_ in (('u', E.zi, E.vi, E.pi, n13['s']), ('s', E.zg, E.vg, E.pg, n13['sp'])):
            w0 = z + s_*v; Jk = sy.J(w0, p, RT); h = 1e-6*float(np.max(sy.sc))
            errs = []
            for e in (np.array([1.0, 0.0]), np.array([0.0, 1.0])):
                d = e*h*sy.sc/np.max(sy.sc)
                a1, a2 = sy.P(w0 + d, p, RT), sy.P(w0 - d, p, RT)
                if a1 is None or a2 is None: continue
                fdv = (a1 - a2)/2; errs.append(float(np.linalg.norm(fdv - Jk @ d)/np.linalg.norm(Jk @ d)))
            fd[nm] = max(errs) if errs else None
        rec['diag_fd_first_segment_rel'] = fd
    return rec

def segment_noise(sy, E, sol):
    """DIAGNOSTIC (not registered): roughness of each segment map at the solution. For every segment start w_{k-1}
    (and u_{k-1}), 12 displacements d = k * 8e2 ulp(|w|) along the propagated manifold tangent; noise = deviation of
    P(w + d) - P(w) from J d, scaled. A residual below this floor cannot be produced by Newton on that segment."""
    s, w, sp_, u = E.unpack(np.array(sol['X'])); out = dict(Wu=[], Ws=[])
    for nm, pts, v, p, nseg in (('Wu', w, E.vi, E.pi, E.a), ('Ws', u, E.vg, E.pg, E.b)):
        t = v.copy()
        for k in range(nseg):
            Jk = sy.J(pts[k], p, RT); p0 = sy.P(pts[k], p, RT); dev = []
            if Jk is None or p0 is None: out[nm].append(None); continue
            tt = t/np.linalg.norm(t); base = 8e2*np.spacing(float(np.max(np.abs(pts[k]))))
            for m in range(1, 13):
                d = tt*m*base; pk = sy.P(pts[k] + d, p, RT)
                if pk is not None: dev.append(float(np.hypot(*((pk - p0 - Jk @ d)/sy.sc))))
            out[nm].append(dict(rms=float(np.sqrt(np.mean(np.square(dev)))) if dev else None, max=max(dev) if dev else None))
            t = Jk @ t
    allr = [q['rms'] for q in out['Wu'] + out['Ws'] if q and q['rms'] is not None]
    out['max_rms'] = max(allr) if allr else None
    out['floor_exceeds_check2'] = bool(out['max_rms'] is not None and out['max_rms'] > RES_MAX)
    return out

def single_return_solve(sy, E, s0, sp0, prim):
    """DIAGNOSTIC (NOT the registered A10 method): the same MS system with one segment per single return (pow = 1,
    a*pow_i and b*pow_g segments), from the same A9 seeds, at rtol 1e-13 and 1e-12. Shows what an amendment with finer
    segments would give."""
    E1 = Edge(E.zi, E.vi, 1, E.a*E.pi, E.zg, E.vg, 1, E.b*E.pg); out = dict(note='unregistered diagnostic: single-return segments')
    sols = {}
    for tag, rt in (('13', RT), ('12', RT2)):
        X0 = ms_initial(sy, E1, s0, sp0, rt)
        if X0 is None: out[tag] = dict(ok=False); continue
        r = ms_solve(sy, E1, X0, rt); sols[tag] = r
        out[tag] = dict(ok=r['ok'], max_seg_res=r.get('max_seg_res'), step=r.get('final_step_scaled_2norm'),
                        cond=r.get('cond_scaled'), ang_raw=r.get('ang_raw'), iters=r.get('iters_accepted'), why_stop=r.get('why_stop'),
                        point=r.get('point'))
    if sols.get('13', {}).get('ok'):
        out['point_vs_registered_scaled'] = scaled_dist(sy, sols['13']['point'], prim['point'])
        if sols.get('12', {}).get('ok'): out['point_13_vs_12_scaled'] = scaled_dist(sy, sols['13']['point'], sols['12']['point'])
        out['would_pass_2_3_5_6'] = bool(out['13']['max_seg_res'] <= RES_MAX and out['13']['ang_raw'] >= ANG_MIN and
                                         out.get('point_13_vs_12_scaled', 1.0) <= PT_TOL and out['13']['step'] <= STEP_MAX)
    return out

def grow_generic(P, z, pow_, lam, v, kneed, delta, sc, cap=6000):
    """Copy of v13_manifolds.grow (as v13_a9_confirm.task_grow) for a generic map P(w) = P^{pow}(w), returning the
    parameter list ss at every iterate."""
    span = abs(lam) if lam > 0 else lam*lam
    ss = list(np.geomspace(delta, delta*span, NSEG0)); cur = [z + si*v for si in ss]
    curves = [np.array(cur)]; sss = [np.array(ss)]
    def trace(si, k):
        w = z + si*v
        for _ in range(k):
            w = P(w)
            if w is None: return None
        return w
    for k in range(1, kneed + 1):
        nxt = [None if w is None else P(w) for w in cur]
        i = 0
        while i < len(ss) - 1 and len(ss) < cap:
            a, b = nxt[i], nxt[i + 1]
            if a is not None and b is not None and math.hypot((a[0] - b[0])/sc[0], (a[1] - b[1])/sc[1]) > DMAX:
                sm = math.sqrt(ss[i]*ss[i + 1]); ss.insert(i + 1, sm); nxt.insert(i + 1, trace(sm, k))
            else: i += 1
        cur = nxt
        curves.append(np.array([p if p is not None else [np.nan, np.nan] for p in cur])); sss.append(np.array(ss))
    return curves, sss, len(ss) >= cap

def negative_control(sy, E, sol, label):
    """Fake crossing: s offset so that the W^u-side endpoint moves 1e-3 (scaled) along W^u, s held fixed, rest solved
    by Gauss-Newton; also the variant s -> s (1 + 1e-3). Must fail check 2 (max scaled residual >> 1e-10)."""
    out = dict(label=label)
    tu = np.array(sol['t_u']); ds = 1e-3/np.linalg.norm(tu/sy.sc)
    for nm, sfake in (('along_Wu_1e-3_scaled', sol['s'] + ds), ('s_relative_1e-3', sol['s']*(1 + 1e-3))):
        X0 = ms_initial(sy, E, sfake, sol['sp'], RT)
        if X0 is None: out[nm] = dict(ok=False, why='propagation failed'); continue
        r = ms_solve(sy, E, X0, RT, fix_s=True)
        out[nm] = dict(s_fake=float(sfake), s_true=sol['s'], ok=r['ok'], max_seg_res=r.get('max_seg_res'),
                       seg_res=r.get('seg_res'), res_norm2=r.get('res_norm2'), iters=r.get('iters_accepted'),
                       why_stop=r.get('why_stop'), check2_passes=bool(r['ok'] and r['max_seg_res'] <= RES_MAX),
                       fails_check2=bool((not r['ok']) or r['max_seg_res'] > RES_MAX))
    out['control_passes'] = bool(all(out[k].get('fails_check2', False) for k in ('along_Wu_1e-3_scaled', 's_relative_1e-3')))
    return out

# =============================================================== MN worker side
W = {}
def init_worker(pt, E, ell, sc):
    M, a_, beta = POINTS[pt]
    S = SectionMap(M, a_, beta, sp.nsimplify(E), sp.nsimplify(ell)*sp.nsimplify(M))
    W['S'] = S; W['sy'] = MNSys(S, sc); W['marg'], _ = make_margin(M, a_, beta, S.b9[4])

def b9_piece(w, n):
    """Check 4 piece: SectionMap.P(w, n, b9=True) must not be None; margins over every accepted step from the
    margin-tracking copy (asserted to reproduce v13_orbit's section points); the B9 end point is compared with the
    base-domain map used by the solve."""
    S = W['S']
    if n == 0:
        return dict(n=0, in_D=bool(S.b9[3](float(w[0]), 0.0)), copy_matches=True, note='zero maps: point checked with in_D')
    Pw, sec, oc = S.P(float(w[0]), float(w[1]), n, b9=True)
    oc2, nc2, tau2, drift2, st2, sec2, mg, _ = W['marg'](float(w[0]), float(w[1]), n, RT, RT*1e-3, 1e12, 50_000_000)
    k = min(len(sec), nc2)
    same = (len(sec) == nc2) and (int(oc) == int(oc2)) and bool(np.array_equal(np.asarray(sec)[:k, :3], sec2[:k, :3]))
    Pb = W['sy'].P(w, n, RT)
    return dict(n=n, in_D=Pw is not None, outcome=int(oc), returns=int(len(sec)), copy_matches=same,
                b9_equals_base=bool(Pw is not None and Pb is not None and np.array_equal(Pw, Pb)),
                min_xm1=float(mg[0]), min_R=float(mg[1]), min_gpp_box=float(mg[2]), min_1my=float(mg[3]),
                drift=float(drift2), steps=int(st2))

def task_edge(args):
    t0 = time.time(); sy = W['sy']
    E = Edge(args['zi'], args['vi'], args['pi'], args['a'], args['zg'], args['vg'], args['pg'], args['b'])
    E.lam_i, E.lam_g = args['lam_i'], args['lam_g']
    rec = dict(src=args['src'], dst=args['dst'], gj=args['gj'], a=E.a, b=E.b, pow_i=E.pi, pow_g=E.pg,
               seed_from_A9=dict(s=args['s0'], sp=args['sp0']), check1=args['check1'], A9_CONFIRMED=args['A9_CONFIRMED'])
    rec.update(ms_confirm(sy, E, args['s0'], args['sp0']))
    n13 = rec.get('ms_13', {})
    if n13.get('ok'):
        s, w, sp_, u = E.unpack(np.array(n13['X']))
        rec['pieces_Wu'] = [b9_piece(w[k], E.pi) for k in range(E.a)] if E.a > 0 else [b9_piece(w[0], 0)]
        rec['pieces_Ws'] = [b9_piece(u[k], E.pg) for k in range(E.b)] if E.b > 0 else [b9_piece(u[0], 0)]
        pcs = rec['pieces_Wu'] + rec['pieces_Ws']
        rec['check4'] = bool(all(p['in_D'] for p in pcs))
        mm = lambda key: min((p[key] for p in pcs if key in p), default=None)
        rec['margins'] = dict(min_xm1=mm('min_xm1'), min_R=mm('min_R'), min_gpp_box=mm('min_gpp_box'), min_1my=mm('min_1my'))
        rec['copy_matches_all'] = bool(all(p.get('copy_matches', True) for p in pcs))
        rec['b9_equals_base_all'] = bool(all(p.get('b9_equals_base', True) for p in pcs if p['n'] > 0))
        # supplementary tails (as A9): G w_0 and G u_0 forward one fundamental period in B9
        rec['tail_Wu'] = b9_piece(G(w[0]), E.pi); rec['tail_Ws'] = b9_piece(G(u[0]), E.pg)
        rec['refined_vs_A9_point_scaled'] = scaled_dist(sy, n13['point'], args['A9_point'])
    else: rec['check4'] = False
    rec['CONFIRMED_MS'] = bool(rec['check1'] and rec.get('check2') and rec.get('check3') and rec['check4']
                               and rec.get('check5') and rec.get('check6'))
    rec['t_total'] = time.time() - t0; rec['worker_peak_rss_mb'] = rss_mb()
    if rec['worker_peak_rss_mb'] > RSS_MAX_MB: rec['RSS_WARNING'] = True
    return rec

def task_negative(args):
    sy = W['sy']
    E = Edge(args['zi'], args['vi'], args['pi'], args['a'], args['zg'], args['vg'], args['pg'], args['b'])
    E.lam_i, E.lam_g = args['lam_i'], args['lam_g']
    X0 = ms_initial(sy, E, args['s0'], args['sp0'], RT); sol = ms_solve(sy, E, X0, RT)
    out = dict(edge=f"{args['src']}->{args['dst']}", a=E.a, b=E.b, true_solve=dict(
        ok=sol['ok'], max_seg_res=sol.get('max_seg_res'), step=sol.get('final_step_scaled_2norm'), cond=sol.get('cond_scaled')))
    if sol['ok']: out.update(negative_control(sy, E, sol, out['edge']))
    else: out['control_passes'] = False
    return out

# =============================================================== resource guard
RSS_MAX_MB = 450.0
def rss_mb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6   # macOS: bytes
def rss_guard(log):
    r = rss_mb()
    if r > RSS_MAX_MB:
        log(f'RESOURCE GUARD: peak RSS {r:.0f} MB > {RSS_MAX_MB:.0f} MB; aborting'); sys.exit(3)

# =============================================================== HH control
def hh_control(log):
    t0 = time.time(); sy = HHSys(1.0/6.0); out = dict(system='Henon-Heiles', E='1/6', section='x = 0, px > 0; (y, py)',
                                                     sc=sy.sc.tolist(), yrange=sy.yrange)
    # Jacobian sanity at a generic point: det = 1 and central differences
    w = np.array([0.1, 0.05]); J = sy.J(w, 1, RT); h = 1e-6
    fd = np.column_stack([(sy.P(w + h*e, 1, RT) - sy.P(w - h*e, 1, RT))/(2*h) for e in np.eye(2)])
    out['jac_check'] = dict(det_minus_1=float(np.linalg.det(J) - 1), fd_rel=float(np.linalg.norm(fd - J)/np.linalg.norm(J)),
                            energy_drift_1_return=sy.energy_drift(w, 1, RT))
    log('HH jacobian check', out['jac_check'])
    # period-1 fixed points: Newton from a seed grid (as v13_upo.newton)
    found = []
    for y0 in np.linspace(sy.yrange[0] + 0.02, sy.yrange[1] - 0.02, 16):
        pr = 2*sy.E - y0*y0 + 2*y0**3/3
        if pr <= 0: continue
        for p0 in np.linspace(-0.9*math.sqrt(pr), 0.9*math.sqrt(pr), 9):
            z = np.array([y0, p0]); okz = False
            for _ in range(40):
                Pz = sy.P(z, 1, RT)
                if Pz is None: break
                F = Pz - z
                if np.max(np.abs(F)) < 1e-12: okz = True; break
                Jz = sy.J(z, 1, RT)
                if Jz is None: break
                try: dz = np.linalg.solve(Jz - np.eye(2), -F)
                except np.linalg.LinAlgError: break
                lam = 1.0
                while lam > 1e-3:
                    zn = z + lam*dz; Pn = sy.P(zn, 1, RT)
                    if Pn is not None and np.max(np.abs(Pn - zn)) < np.max(np.abs(F)): break
                    lam *= 0.5
                z = zn
            if not okz or any(np.hypot(*(z - f['z'])) < 1e-8 for f in found): continue
            Jz = sy.J(z, 1, RT); tr = float(np.trace(Jz))
            found.append(dict(z=z, tr=tr, det=float(np.linalg.det(Jz)), type='hyperbolic' if abs(tr) > 2 else 'elliptic'))
    out['fixed_points'] = [dict(z=f['z'].tolist(), trace=f['tr'], det=f['det'], type=f['type']) for f in found]
    log('HH fixed points', [(np.round(f['z'], 6).tolist(), round(f['tr'], 4), f['type']) for f in found])
    hyp = [f for f in found if f['type'] == 'hyperbolic']
    out['loops'] = []; out['negative'] = None
    for f in hyp:
        z = f['z']; Jz = sy.J(z, 1, RT); ev, V = np.linalg.eig(Jz); k = int(np.argmax(abs(ev.real)))
        lam, v = float(ev[k].real), V[:, k].real; v = v/np.linalg.norm(v); pow_ = 1 if lam > 0 else 2
        gz = G(z); partner = next((g for g in found if np.hypot(*(g['z'] - gz)) < 1e-8), None)
        if partner is None: log('HH fixed point', z, 'has no G partner among found points; skipped'); continue
        zg = partner['z']; Jg = sy.J(zg, 1, RT); evg, Vg = np.linalg.eig(Jg); kg = int(np.argmax(abs(evg.real)))
        lamg, vg = float(evg[kg].real), Vg[:, kg].real; vg = vg/np.linalg.norm(vg); pow_g = 1 if lamg > 0 else 2
        kmax, delta = 8, 1e-6   # lambda ~ 2.5-8 here: 1e-6 * Lambda^8 reaches the size of the section
        Pm = lambda w_, p=pow_: sy.P(w_, p, RT)
        br = {}
        for sgn in (+1, -1):
            br[('u', sgn)] = grow_generic(Pm, z, pow_, lam, sgn*v, kmax, delta, sy.sc)
            br[('g', sgn)] = grow_generic(lambda w_, p=pow_g: sy.P(w_, p, RT), zg, pow_g, lamg, sgn*vg, kmax, delta, sy.sc)
        out.setdefault('growth', []).append(dict(z=z.tolist(), lam=lam, kmax=kmax, delta=delta, DMAX=DMAX,
                                                 cap_hit={f'{k[0]}{k[1]:+d}': bool(v_[2]) for k, v_ in br.items()}))
        # Memory-bounded candidate search (resource guard): scan a + b upward, keep at most 3 short-chord crossings per
        # (a, b, branch pair) by chord angle, stop after the first level giving >= 6 candidates. The lowest a + b
        # representative of a homoclinic point is the one v13_manifolds would record.
        cands = []; n_raw = 0
        for tot in range(1, 2*kmax + 1):
            for a in range(max(0, tot - kmax), min(kmax, tot) + 1):
                b = tot - a
                for si in (+1, -1):
                    for sg in (+1, -1):
                        Cu, Su, capu = br[('u', si)]; Cg, Sg, capg = br[('g', sg)]
                        hits = seg_cross_idx(Cu[a], G(Cg[b])); n_raw += len(hits); keep_h = []
                        for h_ in hits:
                            ch_a = math.hypot(*((Cu[a][h_['i'] + 1] - Cu[a][h_['i']])/sy.sc))
                            ch_b = math.hypot(*((Cg[b][h_['j'] + 1] - Cg[b][h_['j']])/sy.sc))
                            if ch_a <= DMAX and ch_b <= DMAX: keep_h.append((h_, ch_a, ch_b))
                        keep_h.sort(key=lambda t: -t[0]['angle'])
                        for h_, ch_a, ch_b in keep_h[:3]:
                            s0 = si*(Su[a][h_['i']] + h_['t']*(Su[a][h_['i'] + 1] - Su[a][h_['i']]))
                            sp0 = sg*(Sg[b][h_['j']] + h_['u']*(Sg[b][h_['j'] + 1] - Sg[b][h_['j']]))
                            cands.append(dict(a=a, b=b, si=si, sg=sg, point=h_['point'], angle_chord=h_['angle'],
                                              chord_u=ch_a, chord_s=ch_b, check1=True, s0=s0, sp0=sp0))
                        del hits, keep_h
            rss_guard(log)
            if len(cands) >= 6: break
        cands.sort(key=lambda c: (c['a'] + c['b'], -c['angle_chord']))
        log('HH fixed point', np.round(z, 6).tolist(), 'lambda', round(lam, 4), 'G partner', np.round(zg, 6).tolist(),
            'raw crossings scanned', n_raw, 'kept short-chord candidates', len(cands), 'at a+b =', sorted({c['a'] + c['b'] for c in cands}))
        tried = 0
        for c in cands:
            if not c['check1'] or tried >= 6: continue
            if c['angle_chord'] < 0.01: continue
            tried += 1
            E = Edge(z, c['si']*v, pow_, c['a'], zg, c['sg']*vg, pow_g, c['b']); E.lam_i, E.lam_g = lam, lamg
            r = ms_confirm(sy, E, abs(c['s0']), abs(c['sp0']))
            n13 = r.get('ms_13', {})
            r.update(fixed_point=z.tolist(), partner=zg.tolist(), lam=lam, lam_partner=lamg, a=c['a'], b=c['b'],
                     branch_u=c['si'], branch_s=c['sg'], chord_u=c['chord_u'], chord_s=c['chord_s'], check1=c['check1'],
                     polyline_point=c['point'], check4='not applicable (no domain D in HH)',
                     self_loop=True)   # W^u(z) meets W^s(z) = G W^u(G z): a homoclinic point of z
            if n13.get('ok'):
                r['refined_vs_polyline_scaled'] = scaled_dist(sy, n13['point'], c['point'])
                # energy conservation along the solution segments
                s_, w_, sp_, u_ = E.unpack(np.array(n13['X']))
                r['max_energy_drift'] = max(sy.energy_drift(q, pow_, RT) for q in (w_[:-1] if E.a else []) + (u_[:-1] if E.b else []) + [w_[0], u_[0]])
            r['CONFIRMED_MS'] = bool(r['check1'] and r.get('check2') and r.get('check3') and r.get('check5') and r.get('check6'))
            out['loops'].append(r)
            log('HH loop (a,b)=', (c['a'], c['b']), 'CONFIRMED_MS' if r['CONFIRMED_MS'] else 'not confirmed',
                'c2,3,5,6', [r.get('check2'), r.get('check3'), r.get('check5'), r.get('check6')],
                'res', f"{n13.get('max_seg_res', float('nan')):.1e}", 'ang', f"{n13.get('ang_raw', float('nan')):.3f}",
                'pt13/12', f"{r.get('point_13_vs_12_scaled', float('nan')):.1e}", 'step', f"{n13.get('final_step_scaled_2norm', float('nan')):.1e}",
                'cond', f"{n13.get('cond_scaled', float('nan')):.1e}", 'reparam', r.get('diag_reparam', {}).get('point_vs_primary_scaled'))
            if r['CONFIRMED_MS'] and out['negative'] is None:
                out['negative'] = negative_control(sy, E, n13, f'HH (a,b)=({c["a"]},{c["b"]})')
                log('HH negative control', {k: (v_.get('max_seg_res') if isinstance(v_, dict) else v_) for k, v_ in out['negative'].items()})
    out['n_confirmed_self_loops'] = sum(1 for r in out['loops'] if r['CONFIRMED_MS'] and r['self_loop'])
    out['positive_control_passes'] = bool(out['n_confirmed_self_loops'] >= 1)
    out['negative_control_passes'] = bool(out['negative'] is not None and out['negative']['control_passes'])
    out['seconds'] = time.time() - t0
    return out

# =============================================================== driver
def env_commit():
    commit = subprocess.run(['git', '-C', '/Users/sumit/Github/TheBridge', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    env = dict(python=sys.version, numpy=np.__version__, numba=numba.__version__, sympy=sp.__version__,
               scipy=__import__('scipy').__version__, platform=platform.platform(), machine=platform.machine())
    return env, commit

def level(A9):
    U = json.load(open(os.path.join(RES, A9['upo_file']))); return U['E'], U['ell']

def edge_jobs(pt, want=None):
    A9 = json.load(open(os.path.join(RES, A9F[pt])))
    up = {u['idx']: u for u in A9['upos']}; sc = [A9['scaling']['xscale'], A9['scaling']['pscale']]
    scope = [r for r in A9['edges'] if r['check1'] and r['check3'] and r['check4']]
    jobs = []
    for r in scope:
        if want and (r['src'], r['dst']) not in want: continue
        ui, ug = up[r['src']], up[r['gj']]
        pi = ui['period'] if ui['lam'] > 0 else 2*ui['period']; pg = ug['period'] if ug['lam'] > 0 else 2*ug['period']
        assert r['Ai'] == r['a']*pi and r['Bg'] == r['b']*pg, ('pow mismatch', r['src'], r['dst'])
        jobs.append(dict(src=r['src'], dst=r['dst'], gj=r['gj'], a=r['a'], b=r['b'], pi=pi, pg=pg,
                         zi=ui['z'], vi=ui['v'], lam_i=ui['lam'], zg=ug['z'], vg=ug['v'], lam_g=ug['lam'],
                         s0=r['newton_13']['s'], sp0=r['newton_13']['sp'], A9_point=r['newton_13']['point'],
                         check1=bool(r['check1']), A9_CONFIRMED=bool(r['CONFIRMED'])))
    return A9, sc, scope, jobs

class InProcess:
    """--workers 1: no pool, a single process (resource guard: one numba/sympy footprint instead of three)."""
    def __init__(self, initializer, initargs): initializer(*initargs)
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def map(self, f, it):
        for x in it: yield f(x)

def pool(n, initializer, initargs):
    from concurrent.futures import ProcessPoolExecutor
    return InProcess(initializer, initargs) if n <= 1 else ProcessPoolExecutor(n, initializer=initializer, initargs=initargs)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--edges', default=''); ap.add_argument('--tag', default='')
    A = ap.parse_args(); T0 = time.time(); env, commit = env_commit()
    log = lambda *a: print(f'[{time.time() - T0:8.1f}s]', *a, flush=True)
    thresholds = dict(max_seg_res=RES_MAX, angle=ANG_MIN, point_13_vs_12_scaled=PT_TOL, final_step_scaled_2norm=STEP_MAX,
                      rtol_primary=RT, rtol_check5=RT2, atol='1e-3*rtol', DMAX=DMAX)
    if A.mode == 'controls':
        out = dict(amendment='A10', part='controls', commit=commit, env=env, thresholds=thresholds)
        out['HH'] = hh_control(log)
        log('HH positive control', 'PASS' if out['HH']['positive_control_passes'] else 'FAIL',
            '; negative', 'PASS' if out['HH']['negative_control_passes'] else 'FAIL')
        out['MN_negative'] = []
        for pt, edges in (('C0', {(8, 4), (1, 1)}), ('F5R', {(9, 2)})):
            A9, sc, scope, jobs = edge_jobs(pt, edges)
            with pool(min(A.workers, len(jobs)), init_worker, (pt, *level(A9), sc)) as ex:
                for r in ex.map(task_negative, jobs):
                    r['point'] = pt; out['MN_negative'].append(r)
                    log('MN negative', pt, r['edge'], 'true solve res', r['true_solve'].get('max_seg_res'),
                        'fake res', {k: r[k].get('max_seg_res') for k in ('along_Wu_1e-3_scaled', 's_relative_1e-3') if k in r},
                        'PASS' if r['control_passes'] else 'FAIL')
        out['MN_negative_control_passes'] = bool(all(r['control_passes'] for r in out['MN_negative']))
        out['A10_controls_pass'] = bool(out['HH']['positive_control_passes'] and out['HH']['negative_control_passes']
                                        and out['MN_negative_control_passes'])
        out['runtime_s'] = time.time() - T0; out['peak_rss_mb_main'] = rss_mb()
        fn = os.path.join(RES, f'v13_a10_controls{A.tag}.json')
        json.dump(out, open(fn, 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
        log('wrote', fn, 'A10 controls', 'PASS' if out['A10_controls_pass'] else 'FAIL'); return
    pt = A.mode
    ctl = os.path.join(RES, 'v13_a10_controls.json')
    if not os.path.exists(ctl) or not json.load(open(ctl)).get('A10_controls_pass'):
        log('controls missing or failed: A10 is void; not running', pt); sys.exit(2)
    want = {tuple(map(int, s.split('-'))) for s in A.edges.split(',')} if A.edges else None
    A9, sc, scope, jobs = edge_jobs(pt, want)
    n_scope = len(scope); expect = {'C0': 18, 'F5R': 42}[pt]
    log(pt, 'A9 edges', len(A9['edges']), 'in A10 scope (A9 checks 1, 3, 4 passed)', n_scope, 'expected', expect,
        'MISMATCH' if n_scope != expect else 'ok', 'running', len(jobs))
    recs = []
    with pool(A.workers, init_worker, (pt, *level(A9), sc)) as ex:
        for rec in ex.map(task_edge, jobs):
            recs.append(rec); n13 = rec.get('ms_13', {})
            log('edge', rec['src'], '->', rec['dst'], f"(a,b)=({rec['a']},{rec['b']})",
                'CONFIRMED_MS' if rec['CONFIRMED_MS'] else 'not confirmed',
                'c1..6', [rec['check1'], rec.get('check2'), rec.get('check3'), rec['check4'], rec.get('check5'), rec.get('check6')],
                'res', f"{n13.get('max_seg_res', float('nan')):.1e}", 'ang', f"{n13.get('ang_raw', float('nan')):.4f}",
                'pt13/12', f"{rec.get('point_13_vs_12_scaled', float('nan')):.1e}", 'step', f"{n13.get('final_step_scaled_2norm', float('nan')):.1e}",
                'cond', f"{n13.get('cond_scaled', float('nan')):.1e}",
                'reparam', f"{(rec.get('diag_reparam') or {}).get('point_vs_primary_scaled') or float('nan'):.1e}", f"{rec['t_total']:.0f}s")
    recs.sort(key=lambda r: (r['src'], r['dst']))
    checks = ('check1', 'check2', 'check3', 'check4', 'check5', 'check6')
    conf = [r for r in recs if r['CONFIRMED_MS']]
    a9conf = [(r['src'], r['dst']) for r in A9['edges'] if r['CONFIRMED']]
    lab = {}
    for r in conf: lab[(r['src'], r['dst'])] = 'A10'
    for e in a9conf: lab[tuple(e)] = 'A9+A10' if tuple(e) in lab else 'A9 only'
    adj = {}
    for (i, j) in lab: adj.setdefault(i, []).append(j)
    nodes = sorted(u['idx'] for u in A9['upos'])
    sccs = [c for c in tarjan(nodes, adj) if len(c) > 1 or (c[0], c[0]) in lab]
    adj10 = {}
    for r in conf: adj10.setdefault(r['src'], []).append(r['dst'])
    sccs10 = [c for c in tarjan(nodes, adj10) if len(c) > 1 or any(r['src'] == r['dst'] == c[0] for r in conf)]
    first_fail, fails_any = {}, {c: sum(1 for r in recs if not r.get(c)) for c in checks}
    for r in recs:
        if r['CONFIRMED_MS']: continue
        k = next(c for c in checks if not r.get(c)); first_fail[k] = first_fail.get(k, 0) + 1
    mg = lambda key: min((r['margins'][key] for r in conf), default=None)
    summary = dict(n_scope=n_scope, scope_expected=expect, scope_matches=(n_scope == expect), n_run=len(recs),
                   n_confirmed_ms=len(conf), confirmed_ms=[(r['src'], r['dst']) for r in conf],
                   self_loops_confirmed_ms=sorted(r['src'] for r in conf if r['src'] == r['dst']),
                   A9_confirmed=a9conf, graph_edges_labelled={f'{i}->{j}': l for (i, j), l in sorted(lab.items())},
                   sccs_A10_only=sccs10, sccs_A9_union_A10=sccs, first_failing_check=first_fail, failing_each_check=fails_any,
                   worst_residual_confirmed=max((r['ms_13']['max_seg_res'] for r in conf), default=None),
                   min_angle_confirmed=min((r['ms_13']['ang_raw'] for r in conf), default=None),
                   max_point_13_12_confirmed=max((r['point_13_vs_12_scaled'] for r in conf), default=None),
                   max_step_confirmed=max((r['ms_13']['final_step_scaled_2norm'] for r in conf), default=None),
                   max_cond_confirmed=max((r['ms_13']['cond_scaled'] for r in conf), default=None),
                   margins_confirmed=dict(min_xm1=mg('min_xm1'), min_R=mg('min_R'), min_gpp_box=mg('min_gpp_box'), min_1my=mg('min_1my')),
                   max_reparam_point_diff_confirmed=max(((r.get('diag_reparam') or {}).get('point_vs_primary_scaled') or 0 for r in conf), default=None),
                   check3_scaled_metric_failures=sum(1 for r in recs if r.get('ok') and not r.get('check3_scaled_metric')),
                   check6_raw_norm_disagreements=sum(1 for r in recs if r.get('check6') != r.get('check6_raw_norm_also')),
                   runtime_s=time.time() - T0, peak_rss_mb_main=rss_mb(),
                   peak_rss_mb_workers=max((r.get('worker_peak_rss_mb', 0) for r in recs), default=None))
    anomalies = []
    for r in recs:
        if r.get('ok') and not r.get('copy_matches_all', True): anomalies.append(f"{r['src']}->{r['dst']}: margin copy differs from v13_orbit")
        if r.get('ok') and not r.get('b9_equals_base_all', True): anomalies.append(f"{r['src']}->{r['dst']}: B9 end point differs from base map")
        dr = r.get('diag_reparam') or {}
        if r['CONFIRMED_MS'] and (not dr.get('ok') or (dr.get('point_vs_primary_scaled') or 0) > PT_TOL):
            anomalies.append(f"{r['src']}->{r['dst']}: confirmed, but the one-extra-segment reparametrisation moves the point by {dr.get('point_vs_primary_scaled')}")
        if r['CONFIRMED_MS'] and not (r['tail_Wu']['in_D'] and r['tail_Ws']['in_D']): anomalies.append(f"{r['src']}->{r['dst']}: confirmed but a supplementary tail leaves D")
        if r['a'] == 0 or r['b'] == 0: anomalies.append(f"{r['src']}->{r['dst']}: a or b = 0 (crossing point on the LINEAR local manifold z + s v, |s| = {abs(r.get('ms_13', {}).get('s', float('nan'))):.2e})")
    summary['anomalies'] = anomalies
    out = dict(amendment='A10', point=pt, a9_file=A9F[pt], commit=commit, env=env, thresholds=thresholds,
               scaling=dict(xscale=sc[0], pscale=sc[1]), method=dict(
                   solver='numpy.linalg.lstsq (SVD) on the full row/column-scaled bordered system', damping='step halving on the scaled residual 2-norm (to 1/1024)',
                   init='forward propagation from A9 newton_13 (s, s\') at the solve rtol', rtol_handling='S.base[0] / S.sj called with rtol, atol = 1e-3 rtol (SectionMap.P fixes 1e-13)'),
               summary=summary, edges=recs)
    fn = os.path.join(RES, f'v13_a10_{pt}{A.tag}.json')
    json.dump(out, open(fn, 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    log('wrote', fn); log('SUMMARY', json.dumps({k: v for k, v in summary.items() if k != 'anomalies'}, default=str))
    for a_ in anomalies: log('ANOMALY', a_)

if __name__ == '__main__':
    main()
