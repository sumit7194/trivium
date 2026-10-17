"""V13 amendment A9: confirm each raw transition-graph edge of v13_manifolds.py (pre-registered before any crossing was
used). New additive script; nothing existing is edited. It imports SectionMap (v13_upo), make (v13_orbit), POINTS/RES
(v13_screen) and DMAX/NSEG0 (v13_manifolds) unchanged.

For each edge i -> j (a, b) of results/v13_graph_<pt>_19o20_3.json:
  0. Rebuild the hyperbolic in-D UPO list exactly as v13_manifolds.py does (same filter, order, eigen-direction v,
     lambda, xscale/pscale, find_G); assert z and lambda equal the graph file's.
  1. Re-grow the two branches of W^u(i) up to iterate a and of W^u(G j) up to iterate b with the SAME algorithm
     (copied from v13_manifolds.grow, which does not expose s), keeping each sample's fundamental-segment parameter s.
     Re-find the polyline crossing, require it to reproduce the recorded point, and take its two chords.
     CHECK 1: both chords <= DMAX (scaled metric).
  2. 2-D Newton in signed (s, s') on F = P^{a pow_i}(z_i + s v_i) - G P^{b pow_gj}(z_gj + s' v_gj), pow = m (lam > 0)
     or 2m (lam < 0), G(x, p) = (x, -p). F from the v13_orbit integrator (base domain, as SectionMap.P); derivatives
     from the exact variational Jacobian (v13_var, the function behind SectionMap.jac) applied to v.
     CHECK 2: scaled residual <= 1e-9.  CHECK 3: angle between DP v_i and G DP v_gj >= 0.01 rad (raw (x, p_x) metric,
     as the recorded graph angles; the scaled-metric angle is reported too).
  4. CHECK 4: the connecting orbit stays in D_B9 at every accepted step: w_i = z_i + s v_i over a pow_i maps, and (by
     reversibility) w_gj = z_gj + s' v_gj over b pow_gj maps, both with SectionMap.P(..., b9=True) (must not be None).
     Margins along every accepted step come from a copy of the v13_orbit integrator with margin tracking, which is
     asserted to reproduce v13_orbit's section points. Supplementary (not a registered check): the two infinite tails,
     G w_i and G w_gj integrated forward one fundamental period in B9 (they lie on stable manifolds and approach the
     UPO orbits, whose own in-D status is from v13_upo).
  5. CHECK 5: the Newton solve repeated with rtol 1e-12 (atol 1e-15) in BOTH the map and the variational Jacobian,
     from the same chord seed; (s, s') must agree to <= 1e-6 relative.
  CONFIRMED iff checks 1-5 all pass.
Usage: python v13_a9_confirm.py <C0|F5R> [--edges i-j,i-j,...] [--tag suffix] [--workers 2]"""
import sys, os, json, math, time, platform, subprocess, argparse
import numpy as np, sympy as sp, numba
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_upo import SectionMap, RT
from v13_screen import POINTS, RES
from v13_manifolds import DMAX, NSEG0
from v13_field import build, gpp_reg, x as X, y as Y
import scipy.integrate._ivp.dop853_coefficients as DC

GRAPH = {'C0': 'v13_graph_C0_19o20_3.json', 'F5R': 'v13_graph_F5R_19o20_3.json'}
UPOF = {'C0': 'v13_upo_C0_19o20_3.json', 'F5R': 'v13_upo_F5R_19o20_3.json'}
RES_TOL, ANG_MIN, S_REL, RT2 = 1e-9, 0.01, 1e-6, 1e-12
GV = np.array([1.0, -1.0])
G = lambda arr: np.asarray(arr)*GV

# ---------------------------------------------------------------- margin-tracking copy of the v13_orbit integrator
NS = DC.N_STAGES
A_ = np.ascontiguousarray(DC.A[:NS, :NS]); B_ = DC.B.copy()
E3 = DC.E3.copy(); E5 = DC.E5.copy(); D_ = DC.D.copy()
AX = np.ascontiguousarray(DC.A[NS + 1:])
BOX = 0.025

def make_margin(M, a_, beta, pieces):
    """Same DOP853 step control, section detection and B9 domain test as v13_orbit.make(domain='B9'); additionally
    tracks, over every accepted step end, min(x - 1), min R, min of g_phiphi over the 9-point box, and
    min(1 - |y| - 0.025)."""
    S = build(M, a_, beta)
    gpp = numba.njit(sp.lambdify([X, Y], gpp_reg(S), 'math', cse=True))

    @numba.njit
    def rhs(z, out):
        q = pieces(z[0], z[1]); px, py = z[2], z[3]
        out[0] = q[0]*px; out[1] = q[3]*py
        out[2] = -0.5*(q[1]*px*px + q[4]*py*py + q[7]); out[3] = -0.5*(q[2]*px*px + q[5]*py*py + q[8])

    @numba.njit
    def ham(z):
        q = pieces(z[0], z[1]); return 0.5*(q[0]*z[2]*z[2] + q[3]*z[3]*z[3] + q[6])

    @numba.njit
    def in_D(xv, yv):
        if not (xv - 1.0 >= 0.05): return False
        if xv*xv + yv*yv - 1.0 < 0.25: return False
        for dx in (-BOX, 0.0, BOX):
            for dy in (-BOX, 0.0, BOX):
                yy = yv + dy
                if yy >= 1.0 or yy <= -1.0: return False
                g = gpp(xv + dx, yy)
                if not (g > 0.0) or not math.isfinite(g): return False
        return True

    @numba.njit
    def track(xv, yv, mg):
        if xv - 1.0 < mg[0]: mg[0] = xv - 1.0
        r2 = xv*xv + yv*yv - 1.0
        r = math.sqrt(r2) if r2 > 0 else -1.0
        if r < mg[1]: mg[1] = r
        gm = 1e300
        for dx in (-BOX, 0.0, BOX):
            for dy in (-BOX, 0.0, BOX):
                yy = yv + dy
                if yy < 1.0 and yy > -1.0:
                    g = gpp(xv + dx, yy)
                    if not math.isfinite(g): g = -1e300
                    if g < gm: gm = g
        if gm < mg[2]: mg[2] = gm
        ym = 1.0 - abs(yv) - BOX
        if ym < mg[3]: mg[3] = ym

    @numba.njit
    def start(x0, px0):
        q = pieces(x0, 0.0); rest = -1.0 - q[6] - q[0]*px0*px0
        if not (rest > 0.0) or not (q[3] > 0.0): return False, 0.0
        return True, math.sqrt(rest/q[3])

    @numba.njit
    def dense_eval(F, y_old, s, out):
        for k in range(4): out[k] = 0.0
        for i in range(7):
            f = F[6 - i]
            for k in range(4): out[k] += f[k]
            fac = s if i % 2 == 0 else 1.0 - s
            for k in range(4): out[k] *= fac
        for k in range(4): out[k] += y_old[k]

    @numba.njit
    def root(F, y_old, comp, level, s_lo, s_hi):
        tmp = np.empty(4)
        dense_eval(F, y_old, s_lo, tmp); flo = tmp[comp] - level
        for _ in range(60):
            sm = 0.5*(s_lo + s_hi); dense_eval(F, y_old, sm, tmp); fm = tmp[comp] - level
            if (fm < 0) == (flo < 0): s_lo = sm; flo = fm
            else: s_hi = sm
        return 0.5*(s_lo + s_hi)

    @numba.njit
    def integrate(x0, px0, N, rtol, atol, tau_max, max_steps, dom=True):
        sec = np.zeros((max(N, 1), 4)); mg = np.array([1e300, 1e300, 1e300, 1e300])
        hs = np.empty(4096)
        ok, py0 = start(x0, px0)
        if not ok or (dom and not in_D(x0, 0.0)): return 4, 0, 0.0, 0.0, 0, sec, mg, hs[:0]
        track(x0, 0.0, mg)
        y = np.array([x0, 0.0, px0, py0]); f = np.empty(4); rhs(y, f)
        K = np.zeros((16, 4)); ynew = np.empty(4); fnew = np.empty(4); tmp = np.empty(4); F = np.zeros((7, 4))
        sc = atol + np.abs(y)*rtol
        d0 = math.sqrt(np.mean((y/sc)**2)); d1 = math.sqrt(np.mean((f/sc)**2))
        h0 = 1e-6 if (d0 < 1e-5 or d1 < 1e-5) else 0.01*d0/d1
        y1 = y + h0*f; f1 = np.empty(4); rhs(y1, f1)
        d2 = math.sqrt(np.mean(((f1 - f)/sc)**2))/h0
        h1 = max(1e-6, h0*1e-3) if (d1 <= 1e-15 and d2 <= 1e-15) else (0.01/max(d1, d2))**(1.0/8.0)
        h = min(100*h0, h1)
        t = 0.0; ncross = 0; steps = 0; drift = 0.0
        while True:
            if t >= tau_max: return 0, ncross, t, drift, steps, sec, mg, hs[:steps]
            if steps >= max_steps: return 3, ncross, t, drift, steps, sec, mg, hs[:steps]
            rejected = False
            while True:
                hh = min(h, tau_max - t)
                K[0] = f
                for s in range(1, NS):
                    for k in range(4):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*A_[s, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(4):
                    acc = 0.0
                    for j in range(NS): acc += K[j, k]*B_[j]
                    ynew[k] = y[k] + hh*acc
                rhs(ynew, fnew); K[NS] = fnew
                e5 = 0.0; e3 = 0.0
                for k in range(4):
                    sck = atol + max(abs(y[k]), abs(ynew[k]))*rtol
                    a5 = 0.0; a3 = 0.0
                    for j in range(NS + 1): a5 += K[j, k]*E5[j]; a3 += K[j, k]*E3[j]
                    e5 += (a5/sck)**2; e3 += (a3/sck)**2
                if e5 == 0.0 and e3 == 0.0: en = 0.0
                else: en = hh*e5/math.sqrt((e5 + 0.01*e3)*4)
                if not math.isfinite(en): en = 1e300
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return 3, ncross, t, drift, steps, sec, mg, hs[:steps]
            if steps >= hs.shape[0]:
                hs2 = np.empty(2*hs.shape[0]); hs2[:steps] = hs[:steps]; hs = hs2
            hs[steps] = hh
            steps += 1
            dH = abs(ham(ynew) + 0.5)
            if dH > drift: drift = dH
            track(ynew[0], ynew[1], mg)
            if dom and not in_D(ynew[0], ynew[1]): return 1, ncross, t + hh, drift, steps, sec, mg, hs[:steps]
            if ynew[0] > 1000.0: return 2, ncross, t + hh, drift, steps, sec, mg, hs[:steps]
            if y[1] < 0.0 and ynew[1] >= 0.0:
                for s in range(NS + 1, 16):
                    for k in range(4):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*AX[s - NS - 1, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(4):
                    dy = ynew[k] - y[k]
                    F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                    for r in range(4):
                        acc = 0.0
                        for j in range(16): acc += D_[r, j]*K[j, k]
                        F[3 + r, k] = hh*acc
                su = root(F, y, 1, 0.0, 0.0, 1.0); dense_eval(F, y, su, tmp)
                sec[ncross, 0] = tmp[0]; sec[ncross, 1] = tmp[2]; sec[ncross, 2] = t + su*hh; sec[ncross, 3] = drift
                ncross += 1
                if ncross >= N: return 0, ncross, t + su*hh, drift, steps, sec, mg, hs[:steps]
            t += hh
            for k in range(4): y[k] = ynew[k]; f[k] = fnew[k]

    @numba.njit
    def frozen(x0, px0, N, hs):
        """DIAGNOSTIC ONLY: the same DOP853 stages and section detection, replaying a fixed step-size sequence hs (the
        last entry repeated if more steps are needed), no error control. A smooth function of (x0, px0); identical to the
        adaptive map at the point where hs was recorded."""
        ok, py0 = start(x0, px0)
        out = np.zeros(2)
        if not ok: return False, out
        y = np.array([x0, 0.0, px0, py0]); f = np.empty(4); rhs(y, f)
        K = np.zeros((16, 4)); ynew = np.empty(4); fnew = np.empty(4); tmp = np.empty(4); F = np.zeros((7, 4))
        nh = hs.shape[0]; ncross = 0
        for st in range(nh + 200000):
            hh = hs[st] if st < nh else hs[nh - 1]
            K[0] = f
            for s in range(1, NS):
                for k in range(4):
                    acc = 0.0
                    for j in range(s): acc += K[j, k]*A_[s, j]
                    tmp[k] = y[k] + acc*hh
                rhs(tmp, K[s])
            for k in range(4):
                acc = 0.0
                for j in range(NS): acc += K[j, k]*B_[j]
                ynew[k] = y[k] + hh*acc
            rhs(ynew, fnew); K[NS] = fnew
            if not math.isfinite(ynew[0]): return False, out
            if y[1] < 0.0 and ynew[1] >= 0.0:
                ncross += 1
                if ncross >= N:
                    for s in range(NS + 1, 16):
                        for k in range(4):
                            acc = 0.0
                            for j in range(s): acc += K[j, k]*AX[s - NS - 1, j]
                            tmp[k] = y[k] + acc*hh
                        rhs(tmp, K[s])
                    for k in range(4):
                        dy = ynew[k] - y[k]
                        F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                        for r in range(4):
                            acc = 0.0
                            for j in range(16): acc += D_[r, j]*K[j, k]
                            F[3 + r, k] = hh*acc
                    su = root(F, y, 1, 0.0, 0.0, 1.0); dense_eval(F, y, su, tmp)
                    out[0] = tmp[0]; out[1] = tmp[2]
                    return True, out
            for k in range(4): y[k] = ynew[k]; f[k] = fnew[k]
        return False, out
    return integrate, frozen

# ---------------------------------------------------------------- worker state
W = {}

def init_worker(pt, E, ell):
    M, a_, beta = POINTS[pt]
    S = SectionMap(M, a_, beta, sp.nsimplify(E), sp.nsimplify(ell)*sp.nsimplify(M))
    W['S'] = S; W['pt'] = pt
    W['marg'], W['frozen'] = make_margin(M, a_, beta, S.b9[4])

def Pn(w, n, rtol):
    """P^n on the base domain at rtol (identical to SectionMap.P(..., b9=False) when rtol = RT)."""
    if n == 0: return np.array(w, float)
    oc, nc, tau, drift, steps, sec = W['S'].base[0](float(w[0]), float(w[1]), n, rtol, rtol*1e-3, 1e12, 50_000_000)
    if nc < n: return None
    return np.array([sec[n - 1, 0], sec[n - 1, 1]])

def Jn(w, n, rtol):
    if n == 0: return np.eye(2)
    _, J = W['S'].sj(float(w[0]), float(w[1]), n, rtol=rtol)
    return J

def task_eig(args):
    idx, z, m = args
    S = W['S']; z = np.array(z)
    J = S.jac(z, m); ev, V = np.linalg.eig(J); k = int(np.argmax(abs(ev.real)))
    lam, v = float(ev[k].real), V[:, k].real; v = v/np.linalg.norm(v)
    return idx, lam, v.tolist(), J.tolist()

def task_grow(args):
    """Copy of v13_manifolds.grow, additionally returning the parameter list ss at every iterate."""
    idx, sgn, z, m, lam, v, kneed, delta, xscale, pscale = args
    t0 = time.time(); S = W['S']; z = np.array(z); v = sgn*np.array(v); cap = 6000
    pow_ = m if lam > 0 else 2*m
    span = abs(lam) if lam > 0 else lam*lam
    ss = list(np.geomspace(delta, delta*span, NSEG0))
    cur = [z + si*v for si in ss]
    curves = [np.array(cur)]; sss = [np.array(ss)]; dropped = 0
    def trace(si, k):
        w = z + si*v
        for _ in range(k):
            w2, _, _ = S.P(*w, pow_, b9=True)
            if w2 is None: return None
            w = w2
        return w
    for k in range(1, kneed + 1):
        nxt = []
        for w in cur:
            if w is None: nxt.append(None); continue
            w2, _, _ = S.P(*w, pow_, b9=True); nxt.append(w2)
        i = 0
        while i < len(ss) - 1 and len(ss) < cap:
            a, b = nxt[i], nxt[i + 1]
            if a is not None and b is not None and math.hypot((a[0] - b[0])/xscale, (a[1] - b[1])/pscale) > DMAX:
                sm = math.sqrt(ss[i]*ss[i + 1])
                ss.insert(i + 1, sm); nxt.insert(i + 1, trace(sm, k))
            else: i += 1
        dropped = sum(1 for p in nxt if p is None)
        cur = nxt
        curves.append(np.array([p if p is not None else [np.nan, np.nan] for p in cur])); sss.append(np.array(ss))
    return idx, sgn, curves, sss, dropped, len(ss) >= cap, time.time() - t0

def seg_cross_idx(P1, P2):
    """Same arithmetic as v13_manifolds.seg_cross, also returning chord indices and the chord parameters (t, u)."""
    out = []
    A0, A1 = P1[:-1], P1[1:]; B0, B1 = P2[:-1], P2[1:]
    for i in range(len(A0)):
        p, r = A0[i], A1[i] - A0[i]
        if np.isnan(p).any() or np.isnan(r).any(): continue
        q = B0; s = B1 - B0
        den = r[0]*s[:, 1] - r[1]*s[:, 0]
        with np.errstate(all='ignore'):
            t = ((q[:, 0] - p[0])*s[:, 1] - (q[:, 1] - p[1])*s[:, 0])/den
            u = ((q[:, 0] - p[0])*r[1] - (q[:, 1] - p[1])*r[0])/den
        hit = np.where((t >= 0) & (t <= 1) & (u >= 0) & (u <= 1) & np.isfinite(den) & (den != 0))[0]
        for j in hit:
            ang = math.acos(min(1.0, abs(r @ s[j])/(np.linalg.norm(r)*np.linalg.norm(s[j]))))
            out.append(dict(i=int(i), j=int(j), t=float(t[j]), u=float(u[j]), point=(p + t[j]*r).tolist(), angle=ang))
    return out

def angle(t1, t2):
    c = abs(t1[0]*t2[1] - t1[1]*t2[0]); d = abs(t1 @ t2)
    return math.atan2(c, d)

def newton(zi, vi, Ai, zg, vg, Bg, s0, sp0, rtol, sc, it_max=25, maps=None, jrtol=None):
    """2-D damped Newton on F(s, s') = P^Ai(zi + s vi) - G P^Bg(zg + s' vg). Returns a dict with the history.
    maps=None: the registered adaptive map at rtol (Jacobian at rtol). maps=(Mi, Mg): diagnostic maps w -> point."""
    nrm = lambda F: math.hypot(F[0]/sc[0], F[1]/sc[1])
    Mi = (lambda w: Pn(w, Ai, rtol)) if maps is None else maps[0]
    Mg = (lambda w: Pn(w, Bg, rtol)) if maps is None else maps[1]
    jr = rtol if jrtol is None else jrtol
    def Fonly(u):
        a = Mi(zi + u[0]*vi); b = Mg(zg + u[1]*vg)
        if a is None or b is None: return None, a, b
        return a - G(b), a, b
    u = np.array([s0, sp0], float); F, pa, pb = Fonly(u)
    if F is None: return dict(ok=False, why='map undefined at seed', hist=[])
    r = nrm(F); hist = [r]; stall = 0
    for it in range(it_max):
        if r < 1e-15: break
        Ji = Jn(zi + u[0]*vi, Ai, jr); Jg = Jn(zg + u[1]*vg, Bg, jr)
        if Ji is None or Jg is None: return dict(ok=False, why='variational failed', hist=hist)
        Jm = np.column_stack([Ji @ vi, -G(Jg @ vg)])
        try: du = -np.linalg.solve(Jm, F)
        except np.linalg.LinAlgError: return dict(ok=False, why='singular Jacobian', hist=hist)
        lam = 1.0; acc = False
        while lam > 1e-4:
            un = u + lam*du; Fn, pan, pbn = Fonly(un)
            if Fn is not None and nrm(Fn) < r: acc = True; break
            lam *= 0.5
        if not acc: break
        rn = nrm(Fn)
        stall = stall + 1 if rn > 0.5*r else 0
        u, F, pa, pb, r = un, Fn, pan, pbn, rn; hist.append(r)
        if stall >= 3: break
    Ji = Jn(zi + u[0]*vi, Ai, jr); Jg = Jn(zg + u[1]*vg, Bg, jr)
    ti = Ji @ vi; tg = G(Jg @ vg)
    return dict(ok=True, s=float(u[0]), sp=float(u[1]), F=F.tolist(), res=r, hist=hist, point=pa.tolist(),
                point_other=G(pb).tolist(), t_u=ti.tolist(), t_s=tg.tolist(),
                ang_raw=angle(ti, tg), ang_scaled=angle(ti/sc, tg/sc))

def b9_piece(w, n):
    """Registered check: SectionMap.P(w, n, b9=True) is not None. Margins from the margin-tracking copy, which must
    reproduce v13_orbit's section points exactly."""
    S = W['S']
    if n == 0:
        ok = bool(S.b9[3](float(w[0]), 0.0))
        return dict(n=0, in_D=ok, note='zero maps: point itself checked with in_D', copy_matches=True)
    Pw, sec, oc = S.P(float(w[0]), float(w[1]), n, b9=True)
    oc2, nc2, tau2, drift2, st2, sec2, mg, _ = W['marg'](float(w[0]), float(w[1]), n, RT, RT*1e-3, 1e12, 50_000_000)
    k = min(len(sec), nc2)
    same = (len(sec) == nc2) and (int(oc) == int(oc2)) and bool(np.array_equal(np.asarray(sec)[:k, :3], sec2[:k, :3]))
    xs = sec2[:nc2, 0]
    return dict(n=n, in_D=Pw is not None, outcome=int(oc), returns=int(len(sec)), copy_matches=same,
                min_xm1=float(mg[0]), min_R=float(mg[1]), min_gpp_box=float(mg[2]), min_1my=float(mg[3]),
                min_xm1_sec=float(xs.min() - 1) if nc2 else None,
                min_R_sec=float(np.sqrt(xs**2 - 1).min()) if nc2 else None, drift=float(drift2), steps=int(st2))

def tail(w, n, zref):
    """Supplementary: G w forward n maps in B9 (the infinite backward/forward tail, on a stable manifold)."""
    Gw = G(w); r = b9_piece(Gw, n)
    Pw, _, _ = W['S'].P(float(Gw[0]), float(Gw[1]), n, b9=True)
    r['dist_to_upo_after'] = float(np.hypot(*(Pw - zref))) if Pw is not None else None
    r['dist_to_upo_before'] = float(np.hypot(*(Gw - zref)))
    return r

def noise_floor(zi, vi, Ai, zg, vg, Bg, n13, sc):
    """DIAGNOSTIC ONLY (not a registered check): roughness of the adaptive numerical map at the refined point. Six
    perturbations of s (and s') by k*8 ulp(|z|), k = 1..6; noise = rms deviation from the linear prediction, scaled."""
    out = {}
    for nm, z, v, n, s0, t in (('u', zi, vi, Ai, n13['s'], np.array(n13['t_u'])), ('s', zg, vg, Bg, n13['sp'], G(np.array(n13['t_s'])))):
        if n == 0: out[nm] = 0.0; continue
        ds = 8*np.spacing(np.max(np.abs(z)))
        p0 = Pn(z + s0*v, n, RT); dev = []
        for k in range(1, 7):
            pk = Pn(z + (s0 + k*ds)*v, n, RT)
            if pk is None or p0 is None: continue
            dk = pk - p0 - t*k*ds; dev.append((dk[0]/sc[0])**2 + (dk[1]/sc[1])**2)
        out[nm] = float(math.sqrt(np.mean(dev))) if dev else None
    out['combined'] = float(math.hypot(out['u'] or 0.0, out['s'] or 0.0))
    out['res_over_noise'] = float(n13['res']/out['combined']) if out['combined'] > 0 else None
    return out

def frozen_diag(zi, vi, Ai, zg, vg, Bg, s0, sp0, sc):
    """DIAGNOSTIC ONLY (not a registered check): the registered equation solved on a SMOOTH realisation of the same
    numerical map: the step-size sequence of the adaptive integrator is recorded at the chord seed (at rtol 1e-13, and
    separately at 1e-12) and replayed without error control. Reports the residual reached, (s, s') agreement between
    the two step sequences, and that the replayed map equals the adaptive map bitwise at the seed."""
    out = {}
    for tag, rt in (('13', RT), ('12', RT2)):
        maps, same = [], True
        for z, v, n, s in ((zi, vi, Ai, s0), (zg, vg, Bg, sp0)):
            if n == 0: maps.append(lambda w: np.array(w, float)); continue
            w = z + s*v
            oc, nc, _, _, st, sec, _, hs = W['marg'](float(w[0]), float(w[1]), n, rt, rt*1e-3, 1e12, 50_000_000, False)
            if nc < n: return dict(ok=False, why='seed orbit did not complete')
            hs = hs.copy()
            ok, pt = W['frozen'](float(w[0]), float(w[1]), n, hs)
            same = same and ok and pt[0] == sec[n - 1, 0] and pt[1] == sec[n - 1, 1]
            def mp(ww, n=n, hs=hs):
                ok, p = W['frozen'](float(ww[0]), float(ww[1]), n, hs)
                return p.copy() if ok else None
            maps.append(mp)
        r = newton(zi, vi, Ai, zg, vg, Bg, s0, sp0, rt, sc, it_max=30, maps=maps, jrtol=RT)
        r['replay_equals_adaptive_at_seed'] = bool(same)
        for k in ('t_u', 't_s', 'point_other'): r.pop(k, None)
        out[tag] = r
    if out['13'].get('ok') and out['12'].get('ok'):
        out['s_rel'] = abs(out['13']['s'] - out['12']['s'])/abs(out['13']['s'])
        out['sp_rel'] = abs(out['13']['sp'] - out['12']['sp'])/abs(out['13']['sp'])
    return out

def task_edge(args):
    e = args['edge']; t0 = time.time()
    zi, vi, Ai = np.array(args['zi']), np.array(args['vi']), args['Ai']
    zg, vg, Bg = np.array(args['zg']), np.array(args['vg']), args['Bg']
    sc = np.array(args['sc'])
    rec = dict(src=e['src'], dst=e['dst'], a=e['a'], b=e['b'], gj=args['gj'], Ai=Ai, Bg=Bg)
    n13 = newton(zi, vi, Ai, zg, vg, Bg, args['s0'], args['sp0'], RT, sc); t1 = time.time()
    rec['newton_13'] = n13; rec['t_newton_13'] = t1 - t0
    n12 = newton(zi, vi, Ai, zg, vg, Bg, args['s0'], args['sp0'], RT2, sc); t2 = time.time()
    rec['newton_12'] = n12; rec['t_newton_12'] = t2 - t1
    if n13['ok']:
        wi = zi + n13['s']*vi; wg = zg + n13['sp']*vg
        rec['piece_back'] = b9_piece(wi, Ai); rec['piece_fwd'] = b9_piece(wg, Bg)
        rec['tail_back'] = tail(wi, args['pow_i'], G(zi)); rec['tail_fwd'] = tail(wg, args['pow_g'], G(zg))
        # Jacobian cross-check by central differences in s (exact variational vs difference quotient)
        rec['fd_check'] = {}
        for hr in (1e-3, 1e-4):
            hs = hr*abs(n13['s']); hp = hr*abs(n13['sp'])
            a1, a2 = Pn(zi + (n13['s'] + hs)*vi, Ai, RT), Pn(zi + (n13['s'] - hs)*vi, Ai, RT)
            b1, b2 = Pn(zg + (n13['sp'] + hp)*vg, Bg, RT), Pn(zg + (n13['sp'] - hp)*vg, Bg, RT)
            if all(q is not None for q in (a1, a2, b1, b2)) and Ai > 0 and Bg > 0:
                di = (a1 - a2)/(2*hs); dg = G(b1 - b2)/(2*hp)
                rec['fd_check'][f'h={hr:g}|s|'] = dict(
                    rel_u=float(np.linalg.norm(di - np.array(n13['t_u']))/np.linalg.norm(n13['t_u'])),
                    rel_s=float(np.linalg.norm(dg - np.array(n13['t_s']))/np.linalg.norm(n13['t_s'])))
        rec['diag_noise'] = noise_floor(zi, vi, Ai, zg, vg, Bg, n13, sc)
        rec['diag_frozen'] = frozen_diag(zi, vi, Ai, zg, vg, Bg, args['s0'], args['sp0'], sc)
    rec['t_total'] = time.time() - t0
    return rec

# ---------------------------------------------------------------- driver
def tarjan(nodes, adj):
    idx, low, on, st, out, c = {}, {}, set(), [], [], [0]
    def sc(v):
        idx[v] = low[v] = c[0]; c[0] += 1; st.append(v); on.add(v)
        for w in adj.get(v, ()):
            if w not in idx: sc(w); low[v] = min(low[v], low[w])
            elif w in on: low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop(); on.discard(w); comp.append(w)
                if w == v: break
            out.append(sorted(comp))
    for v in nodes:
        if v not in idx: sc(v)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('pt'); ap.add_argument('--edges', default='')
    ap.add_argument('--tag', default=''); ap.add_argument('--workers', type=int, default=2)
    A = ap.parse_args(); pt = A.pt; T0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    Gr = json.load(open(os.path.join(RES, GRAPH[pt]))); U = json.load(open(os.path.join(RES, UPOF[pt])))
    assert Gr['source'] == UPOF[pt]
    kmax, delta = Gr['kmax'], Gr['delta']
    hyp = [u for u in U['upos'] if u['type'] == 'hyperbolic' and u['whole_orbit_in_D'] and u['area_ok']]
    xs = [p[0] for u in U['upos'] for p in u['points']]; ps = [p[1] for u in U['upos'] for p in u['points']]
    xscale = max(1e-3, max(xs) - min(xs)); pscale = max(1e-3, max(abs(v) for v in ps)*2)
    edges = Gr['edges']
    if A.edges:
        want = {tuple(map(int, s.split('-'))) for s in A.edges.split(',')}
        edges = [e for e in edges if (e['src'], e['dst']) in want]
    log = lambda *a: print(f'[{time.time() - T0:8.1f}s]', *a, flush=True)
    log(pt, 'hyp in-D UPOs', len(hyp), 'edges', len(edges), 'xscale', xscale, 'pscale', pscale)
    with ProcessPoolExecutor(A.workers, initializer=init_worker, initargs=(pt, U['E'], U['ell'])) as ex:
        eig = {r[0]: r for r in ex.map(task_eig, [(i, u['points'][0], u['period']) for i, u in enumerate(hyp)])}
        Wu = {}
        for i, u in enumerate(hyp):
            _, lam, v, J = eig[i]; g = Gr['upos'][i]
            assert g['idx'] == i and np.allclose(g['z'], u['points'][0], rtol=0, atol=0), ('z mismatch', i)
            assert lam == g['lam'], ('lambda mismatch', i, lam, g['lam'])
            Wu[i] = dict(z=np.array(u['points'][0]), m=u['period'], lam=lam, v=np.array(v), pts=u['points'],
                         min_xm1=u['min_xm1'], min_R=u['min_R'])
        log('eigen data reproduced exactly for all', len(Wu), 'UPOs (z, lambda bitwise equal to the graph file)')
        def find_G(idx):   # copy of v13_manifolds.find_G
            z = G(Wu[idx]['z'])
            for j, w in Wu.items():
                if w['m'] == Wu[idx]['m'] and np.hypot(*(w['z'] - z)) < 1e-6: return j
                for p in hyp[j]['points']:
                    if np.hypot(*(np.array(p) - z)) < 1e-6: return j
            return None
        need = {}
        for e in edges:
            need[e['src']] = max(need.get(e['src'], 0), e['a'])
            gj = find_G(e['dst']); e['_gj'] = gj
            need[gj] = max(need.get(gj, 0), e['b'])
        tasks = [(i, sgn, Wu[i]['z'].tolist(), Wu[i]['m'], Wu[i]['lam'], Wu[i]['v'].tolist(), k, delta, xscale, pscale)
                 for i, k in sorted(need.items(), key=lambda t: -t[1]) for sgn in (+1, -1)]
        br = {}; grow_t = {}
        for idx, sgn, curves, sss, dropped, capped, dt in ex.map(task_grow, tasks):
            br[(idx, sgn)] = dict(curves=curves, ss=sss, dropped=dropped, capped=capped); grow_t[f'{idx},{sgn}'] = dt
            log('regrown W^u', idx, 'branch', sgn, 'to iterate', len(curves) - 1, 'points', len(sss[-1]), 'dropped',
                dropped, 'cap hit' if capped else '', f'{dt:.1f}s')
        # match each edge's recorded crossing and build the Newton seeds (check 1)
        recs0, jobs = {}, []
        for e in edges:
            i, j, a, b, gj = e['src'], e['dst'], e['a'], e['b'], e['_gj']
            best = None
            for si in (+1, -1):
                for sg in (+1, -1):
                    Ca = br[(i, si)]['curves'][a]; Cb = br[(gj, sg)]['curves'][b]
                    for h in seg_cross_idx(Ca, G(Cb)):
                        d = math.hypot(h['point'][0] - e['point'][0], h['point'][1] - e['point'][1])
                        if best is None or d < best[0]: best = (d, si, sg, h)
            key = (i, j)
            r0 = dict(src=i, dst=j, a=a, b=b, gj=gj, recorded_point=e['point'], recorded_angle=e['angle'])
            if best is None:
                r0['match'] = None; recs0[key] = r0; log('edge', i, '->', j, 'NO CROSSING REPRODUCED'); continue
            d, si, sg, h = best
            ssa, ssb = br[(i, si)]['ss'][a], br[(gj, sg)]['ss'][b]
            Ca, Cb = br[(i, si)]['curves'][a], br[(gj, sg)]['curves'][b]
            ch_a = math.hypot(*((Ca[h['i'] + 1] - Ca[h['i']])/[xscale, pscale]))
            ch_b = math.hypot(*((Cb[h['j'] + 1] - Cb[h['j']])/[xscale, pscale]))
            s0 = si*(ssa[h['i']] + h['t']*(ssa[h['i'] + 1] - ssa[h['i']]))
            sp0 = sg*(ssb[h['j']] + h['u']*(ssb[h['j'] + 1] - ssb[h['j']]))
            r0.update(match=dict(dist=d, branch_i=si, branch_gj=sg, chord_i=h['i'], chord_gj=h['j'], t=h['t'], u=h['u'],
                                 angle_chord=h['angle'], s_chord_i=[si*ssa[h['i']], si*ssa[h['i'] + 1]],
                                 s_chord_gj=[sg*ssb[h['j']], sg*ssb[h['j'] + 1]]),
                      chord_i=ch_a, chord_gj=ch_b, check1=bool(ch_a <= DMAX and ch_b <= DMAX), s_seed=s0, sp_seed=sp0,
                      cap_hit_i=br[(i, si)]['capped'], cap_hit_gj=br[(gj, sg)]['capped'])
            recs0[key] = r0
            pi = Wu[i]['m'] if Wu[i]['lam'] > 0 else 2*Wu[i]['m']; pg = Wu[gj]['m'] if Wu[gj]['lam'] > 0 else 2*Wu[gj]['m']
            jobs.append(dict(edge=e, gj=gj, zi=Wu[i]['z'].tolist(), vi=(Wu[i]['v']).tolist(), Ai=a*pi, pow_i=pi,
                             zg=Wu[gj]['z'].tolist(), vg=(Wu[gj]['v']).tolist(), Bg=b*pg, pow_g=pg,
                             s0=s0, sp0=sp0, sc=[xscale, pscale]))
            log('edge', i, '->', j, f'(a,b)=({a},{b}) gj={gj} match {d:.1e} chords {ch_a:.2e} {ch_b:.2e} seed s={s0:.6e} s\'={sp0:.6e}')
        out_recs = []
        for rec in ex.map(task_edge, jobs):
            r = recs0[(rec['src'], rec['dst'])]; r.update(rec)
            n13, n12 = r['newton_13'], r['newton_12']
            r['check2'] = bool(n13['ok'] and n13['res'] <= RES_TOL)
            r['check3'] = bool(n13['ok'] and n13['ang_raw'] >= ANG_MIN)
            r['check3_scaled_metric'] = bool(n13['ok'] and n13['ang_scaled'] >= ANG_MIN)
            r['check4'] = bool(n13['ok'] and r['piece_back']['in_D'] and r['piece_fwd']['in_D'])
            if n13['ok'] and n12['ok']:
                r['s_rel'] = abs(n13['s'] - n12['s'])/abs(n13['s']); r['sp_rel'] = abs(n13['sp'] - n12['sp'])/abs(n13['sp'])
                # guard: a solve that accepted no Newton step returns its seed, so equal seeds would pass vacuously
                r['newton_steps'] = [len(n13['hist']) - 1, len(n12['hist']) - 1]
                r['check5'] = bool(r['s_rel'] <= S_REL and r['sp_rel'] <= S_REL and min(r['newton_steps']) >= 1)
                r['point_13_vs_12_scaled'] = math.hypot((n13['point'][0] - n12['point'][0])/xscale, (n13['point'][1] - n12['point'][1])/pscale)
            else: r['check5'] = False
            if n13['ok']:
                r['refined_vs_seed'] = dict(dist_scaled=math.hypot((n13['point'][0] - r['recorded_point'][0])/xscale,
                                                                   (n13['point'][1] - r['recorded_point'][1])/pscale),
                                            s_in_chord=bool(min(r['match']['s_chord_i']) <= n13['s'] <= max(r['match']['s_chord_i'])),
                                            sp_in_chord=bool(min(r['match']['s_chord_gj']) <= n13['sp'] <= max(r['match']['s_chord_gj'])))
                r['tails_in_D'] = bool(r['tail_back']['in_D'] and r['tail_fwd']['in_D'])
            r['CONFIRMED'] = bool(r['check1'] and r['check2'] and r['check3'] and r['check4'] and r['check5'])
            out_recs.append(r)
            log('edge', r['src'], '->', r['dst'], 'CONFIRMED' if r['CONFIRMED'] else 'not confirmed',
                'c1..5', [r['check1'], r['check2'], r['check3'], r['check4'], r['check5']],
                'res', f"{n13.get('res', float('nan')):.1e}", 'ang', f"{n13.get('ang_raw', float('nan')):.4f}",
                's_rel', f"{r.get('s_rel', float('nan')):.1e}/{r.get('sp_rel', float('nan')):.1e}", f"{r['t_total']:.0f}s")
    for key, r0 in recs0.items():
        if r0.get('match') is None: r0.update(check1=False, check2=False, check3=False, check4=False, check5=False, CONFIRMED=False); out_recs.append(r0)
    out_recs.sort(key=lambda r: (r['src'], r['dst']))
    conf = [r for r in out_recs if r['CONFIRMED']]
    adj = {}
    for r in conf: adj.setdefault(r['src'], []).append(r['dst'])
    nodes = sorted(set(Wu))
    sccs = [c for c in tarjan(nodes, adj) if len(c) > 1 or any(r['src'] == r['dst'] == c[0] for r in conf)]
    first_fail = {}
    for r in out_recs:
        if r['CONFIRMED']: continue
        k = next(c for c in ('check1', 'check2', 'check3', 'check4', 'check5') if not r[c]); first_fail[k] = first_fail.get(k, 0) + 1
    fails_any = {c: sum(1 for r in out_recs if not r[c]) for c in ('check1', 'check2', 'check3', 'check4', 'check5')}
    ok13 = [r for r in out_recs if r.get('newton_13', {}).get('ok')]
    mins = dict(
        min_angle_confirmed=min((r['newton_13']['ang_raw'] for r in conf), default=None),
        max_res_confirmed=max((r['newton_13']['res'] for r in conf), default=None),
        max_srel_confirmed=max((max(r['s_rel'], r['sp_rel']) for r in conf), default=None),
        max_chord_confirmed=max((max(r['chord_i'], r['chord_gj']) for r in conf), default=None),
        min_xm1_confirmed=min((min(r['piece_back'].get('min_xm1', 1e9), r['piece_fwd'].get('min_xm1', 1e9)) for r in conf), default=None),
        min_R_confirmed=min((min(r['piece_back'].get('min_R', 1e9), r['piece_fwd'].get('min_R', 1e9)) for r in conf), default=None),
        min_gpp_box_confirmed=min((min(r['piece_back'].get('min_gpp_box', 1e9), r['piece_fwd'].get('min_gpp_box', 1e9)) for r in conf), default=None))
    anomalies = []
    for r in out_recs:
        if r.get('match') and r['match']['dist'] > 1e-12: anomalies.append(f"{r['src']}->{r['dst']}: recorded crossing reproduced only to {r['match']['dist']:.1e}")
        for pc in ('piece_back', 'piece_fwd', 'tail_back', 'tail_fwd'):
            if pc in r and not r[pc].get('copy_matches', True): anomalies.append(f"{r['src']}->{r['dst']}: margin integrator copy differs from v13_orbit on {pc}")
        if r.get('check3') != r.get('check3_scaled_metric') and r.get('newton_13', {}).get('ok'):
            anomalies.append(f"{r['src']}->{r['dst']}: check 3 differs between raw ({r['newton_13']['ang_raw']:.4f}) and scaled ({r['newton_13']['ang_scaled']:.4f}) metric")
        if r.get('CONFIRMED') and not r.get('tails_in_D', True): anomalies.append(f"{r['src']}->{r['dst']}: confirmed but a supplementary tail leaves D")
        if r.get('refined_vs_seed') and r['refined_vs_seed']['dist_scaled'] > max(r['chord_i'], r['chord_gj']):
            anomalies.append(f"{r['src']}->{r['dst']}: refined point {r['refined_vs_seed']['dist_scaled']:.1e} (scaled) from the recorded crossing, farther than its longer chord")
    commit = subprocess.run(['git', '-C', '/Users/sumit/Github/TheBridge', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    env = dict(python=sys.version, numpy=np.__version__, numba=numba.__version__, sympy=sp.__version__,
               scipy=__import__('scipy').__version__, platform=platform.platform(), machine=platform.machine())
    summary = dict(n_edges=len(out_recs), n_confirmed=len(conf), confirmed=[(r['src'], r['dst']) for r in conf],
                   self_loops_confirmed=sorted(r['src'] for r in conf if r['src'] == r['dst']),
                   sccs_confirmed=sccs, first_failing_check=first_fail, failing_each_check=fails_any,
                   check3_scaled_metric_failures=sum(1 for r in ok13 if not r['check3_scaled_metric']),
                   margins=mins, anomalies=anomalies, runtime_s=time.time() - T0)
    out = dict(amendment='A9', point=pt, graph=GRAPH[pt], upo_file=UPOF[pt], commit=commit, env=env,
               thresholds=dict(DMAX=DMAX, residual=RES_TOL, angle=ANG_MIN, s_rel=S_REL, rtol_primary=RT, rtol_check5=RT2,
                               atol='1e-3*rtol'),
               scaling=dict(xscale=xscale, pscale=pscale), kmax=kmax, delta=delta, grow_seconds=grow_t,
               upos=[dict(idx=i, period=w['m'], lam=w['lam'], z=w['z'].tolist(), v=w['v'].tolist(), gi=find_G(i),
                          min_xm1_sec=w['min_xm1'], min_R_sec=w['min_R']) for i, w in Wu.items()],
               summary=summary, edges=out_recs)
    fn = os.path.join(RES, f'v13_a9_confirm_{pt}{A.tag}.json')
    json.dump(out, open(fn, 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    log('wrote', fn); log('SUMMARY', json.dumps(summary, default=str))

if __name__ == '__main__':
    main()
