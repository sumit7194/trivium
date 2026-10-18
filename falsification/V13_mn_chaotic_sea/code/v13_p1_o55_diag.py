"""V13 p1 orbit 55: LABELLED POST-HOC diagnostic (no registered verdict changes). Prereg note at the top of
results/v13_p1_o55_diag.md (written before any computation here).

Question: is p1 counted orbit 55 (x0 = 6.870002791181163, p_x0 = 0, level (37/40, 29/10), B9; CHAOTIC under the
registered AND rule with A1 = -6.41, A2 = +0.0275) genuinely chaotic, or a regular orbit misclassified?

1. Maximal Lyapunov exponent: numba DOP853 (same tableau / step control as v13_orbit, v13_var) on the 8-dim system
   (z, w), w' = Df(z) w, Df from the EXACT second derivatives of the regularised field (as v13_var). w is renormalised
   to unit norm at the step end after each section crossing; lambda(t) = sum ln|w| / t. Domain (B9 or base) and
   |H + 1/2| are checked at every accepted step.
2. Section geometry: correlation dimension D2 (kd-tree pair counts), NAFF on successive 2000-return windows.
3. A2 calibration on the sealed counted file and the p1 Kerr null (read only).
4. Integrator check: v13_orbit.integrate at rtol 1e-11 / 1e-12 / 1e-13.
Usage: python v13_p1_o55_diag.py timing | lyap <label> <N> [rtol] | integ | analyze
Intermediate .npz go to $V13_DIAG_WORK (default: the session scratchpad); the summary goes to results/."""
import sys, os, json, math, time, subprocess, platform, hashlib
import numpy as np, sympy as sp, numba, scipy
import scipy.integrate._ivp.dop853_coefficients as DC
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_field import build, W_reg, ginv_reg, gpp_reg, x as X, y as Y
from v13_indicators import fma_diffusion, zero_one_K, naff_freq

R = sp.Rational
RES = os.path.join(HERE, '../results')
WORK = os.environ.get('V13_DIAG_WORK', '/private/tmp/claude-501/-Users-sumit-Github-TheBridge/'
                      '47a59676-296b-437c-9016-f6549751084c/scratchpad/o55')
os.makedirs(WORK, exist_ok=True)
SEAL_P1 = 'b2f3b3c9f705b5da476ad90aa130baefd5bb023525660301022cd3e3b66b5c9c'
SEAL_C0 = '6a705e2bd53443e8755387d68913857d99658f25a09053be21266e41cfbd74d1'
P1 = (5, 3, R(1, 5)); P1_LEVEL = (R(37, 40), R(29, 10)*5)          # (E, L_z = ell M)
C0 = (1, R(9, 10), R(19, 20)/(R(19, 100))**R(3, 2)); C0_LEVEL = (R(19, 20), R(3))

NS = DC.N_STAGES
A = np.ascontiguousarray(DC.A[:NS, :NS]); B = DC.B.copy(); E3 = DC.E3.copy(); E5 = DC.E5.copy(); D = DC.D.copy()
AX = np.ascontiguousarray(DC.A[NS + 1:])
ND = 8
SURVIVE, LEFT_D, ESCAPE, CAPPED, FORBIDDEN = 0, 1, 2, 3, 4
BOX = 0.025


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load_sealed():
    p1f, c0f = os.path.join(RES, 'v13_counted_p1.json'), os.path.join(RES, 'v13_c0_gate.json')
    assert sha(p1f) == SEAL_P1 and sha(c0f) == SEAL_C0, 'sealed file hash mismatch'
    return json.load(open(p1f)), json.load(open(c0f))


def make_lyap(M, a_, beta, E, Lz, domain):
    BASE = (domain == 'base')
    S = build(M, a_, beta); E, Lz = sp.nsimplify(E), sp.nsimplify(Lz)
    gxx, gyy = ginv_reg(S); W = W_reg(S, E, Lz)
    flat = []
    for f in (gxx, gyy, W):
        fx, fy = sp.diff(f, X), sp.diff(f, Y)
        flat += [f, fx, fy, sp.diff(fx, X), sp.diff(fx, Y), sp.diff(fy, Y)]
    pc = numba.njit(sp.lambdify([X, Y], flat, 'math', cse=True))
    gpp = numba.njit(sp.lambdify([X, Y], gpp_reg(S), 'math', cse=True))

    @numba.njit
    def rhs(z, out):
        q = pc(z[0], z[1]); px, py = z[2], z[3]
        out[0] = q[0]*px; out[1] = q[6]*py
        out[2] = -0.5*(q[1]*px*px + q[7]*py*py + q[13]); out[3] = -0.5*(q[2]*px*px + q[8]*py*py + q[14])
        J = np.empty((4, 4))
        J[0, 0] = q[1]*px; J[0, 1] = q[2]*px; J[0, 2] = q[0]; J[0, 3] = 0.0
        J[1, 0] = q[7]*py; J[1, 1] = q[8]*py; J[1, 2] = 0.0; J[1, 3] = q[6]
        J[2, 0] = -0.5*(q[3]*px*px + q[9]*py*py + q[15]); J[2, 1] = -0.5*(q[4]*px*px + q[10]*py*py + q[16])
        J[2, 2] = -q[1]*px; J[2, 3] = -q[7]*py
        J[3, 0] = -0.5*(q[4]*px*px + q[10]*py*py + q[16]); J[3, 1] = -0.5*(q[5]*px*px + q[11]*py*py + q[17])
        J[3, 2] = -q[2]*px; J[3, 3] = -q[8]*py
        for i in range(4):
            acc = 0.0
            for k in range(4): acc += J[i, k]*z[4 + k]
            out[4 + i] = acc

    @numba.njit
    def ham(z):
        q = pc(z[0], z[1]); return 0.5*(q[0]*z[2]*z[2] + q[6]*z[3]*z[3] + q[12])

    @numba.njit
    def in_D(xv, yv):
        if BASE:
            if not (xv > 1.0) or not (abs(yv) < 1.0): return False
            g = gpp(xv, yv)
            return g > 0.0 and math.isfinite(g)
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
    def dense_eval(F, y_old, s, out):
        for k in range(ND): out[k] = 0.0
        for i in range(7):
            f = F[6 - i]
            for k in range(ND): out[k] += f[k]
            fac = s if i % 2 == 0 else 1.0 - s
            for k in range(ND): out[k] *= fac
        for k in range(ND): out[k] += y_old[k]

    @numba.njit
    def root(F, y_old, comp, level, s_lo, s_hi):
        tmp = np.empty(ND)
        dense_eval(F, y_old, s_lo, tmp); flo = tmp[comp] - level
        for _ in range(60):
            sm = 0.5*(s_lo + s_hi); dense_eval(F, y_old, sm, tmp); fm = tmp[comp] - level
            if (fm < 0) == (flo < 0): s_lo = sm; flo = fm
            else: s_hi = sm
        return 0.5*(s_lo + s_hi)

    @numba.njit
    def run(x0, px0, w0, N, rtol, atol, tau_max, max_steps):
        """Returns (outcome, ncross, t, drift, steps, sec[N, 6]); sec rows
        (x, p_x, tau_cross, S = cumulative ln-stretch at the renormalisation, t at the renormalisation, drift)."""
        sec = np.zeros((max(N, 1), 6))
        q = pc(x0, 0.0); rest = -1.0 - q[12] - q[0]*px0*px0
        if not (rest > 0.0) or not (q[6] > 0.0) or not in_D(x0, 0.0): return FORBIDDEN, 0, 0.0, 0.0, 0, sec
        y = np.zeros(ND); y[0] = x0; y[2] = px0; y[3] = math.sqrt(rest/q[6])
        nw = 0.0
        for k in range(4): nw += w0[k]*w0[k]
        nw = math.sqrt(nw)
        for k in range(4): y[4 + k] = w0[k]/nw
        f = np.empty(ND); rhs(y, f)
        K = np.zeros((16, ND)); ynew = np.empty(ND); fnew = np.empty(ND); tmp = np.empty(ND); F = np.zeros((7, ND))
        h = 1e-3; t = 0.0; ncross = 0; steps = 0; drift = 0.0; Ssum = 0.0
        while True:
            if t >= tau_max: return SURVIVE, ncross, t, drift, steps, sec
            if steps >= max_steps: return CAPPED, ncross, t, drift, steps, sec
            rejected = False
            while True:
                hh = h
                K[0] = f
                for s in range(1, NS):
                    for k in range(ND):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*A[s, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(ND):
                    acc = 0.0
                    for j in range(NS): acc += K[j, k]*B[j]
                    ynew[k] = y[k] + hh*acc
                rhs(ynew, fnew); K[NS] = fnew
                e5 = 0.0; e3 = 0.0
                for k in range(ND):
                    sck = atol + max(abs(y[k]), abs(ynew[k]))*rtol
                    a5 = 0.0; a3 = 0.0
                    for j in range(NS + 1): a5 += K[j, k]*E5[j]; a3 += K[j, k]*E3[j]
                    e5 += (a5/sck)**2; e3 += (a3/sck)**2
                en = 0.0 if (e5 == 0.0 and e3 == 0.0) else hh*e5/math.sqrt((e5 + 0.01*e3)*ND)
                if not math.isfinite(en): en = 1e300
                if en < 1.0:
                    fac = 10.0 if en == 0.0 else min(10.0, 0.9*en**(-1.0/8.0))
                    if rejected: fac = min(1.0, fac)
                    h = hh*fac; break
                h = hh*max(0.2, 0.9*en**(-1.0/8.0)); rejected = True
                if h < 1e-14: return CAPPED, ncross, t, drift, steps, sec
            steps += 1
            dH = abs(ham(ynew) + 0.5)
            if dH > drift: drift = dH
            if not in_D(ynew[0], ynew[1]): return LEFT_D, ncross, t + hh, drift, steps, sec
            if ynew[0] > 1000.0: return ESCAPE, ncross, t + hh, drift, steps, sec
            crossed = y[1] < 0.0 and ynew[1] >= 0.0
            if crossed:
                for s in range(NS + 1, 16):
                    for k in range(ND):
                        acc = 0.0
                        for j in range(s): acc += K[j, k]*AX[s - NS - 1, j]
                        tmp[k] = y[k] + acc*hh
                    rhs(tmp, K[s])
                for k in range(ND):
                    dy = ynew[k] - y[k]
                    F[0, k] = dy; F[1, k] = hh*f[k] - dy; F[2, k] = 2*dy - hh*(fnew[k] + f[k])
                    for r in range(4):
                        acc = 0.0
                        for j in range(16): acc += D[r, j]*K[j, k]
                        F[3 + r, k] = hh*acc
                su = root(F, y, 1, 0.0, 0.0, 1.0); dense_eval(F, y, su, tmp)
            t += hh
            for k in range(ND): y[k] = ynew[k]; f[k] = fnew[k]
            nw = 0.0
            for k in range(4): nw += y[4 + k]*y[4 + k]
            nw = math.sqrt(nw)
            if crossed or nw > 1e8:
                Ssum += math.log(nw)
                for k in range(4): y[4 + k] /= nw; f[4 + k] /= nw
            if crossed:
                sec[ncross, 0] = tmp[0]; sec[ncross, 1] = tmp[2]; sec[ncross, 2] = t - hh + su*hh
                sec[ncross, 3] = Ssum; sec[ncross, 4] = t; sec[ncross, 5] = drift
                ncross += 1
                if ncross >= N: return SURVIVE, ncross, t, drift, steps, sec

    return run


TARGETS = {   # label: (params, level, domain, which sealed orbit)
    'o55': (P1, P1_LEVEL, 'B9', ('p1', 55)),
    'o14': (P1, P1_LEVEL, 'B9', ('p1', 14)),
    'c0o20': (C0, C0_LEVEL, 'base', ('c0', 20)),
}
W0 = {'a': np.array([1.0, 0.7, -0.3, 0.5]), 'b': np.array([-0.2, 1.0, 0.9, -0.6])}


def x0px0(label):
    p1, c0 = load_sealed()
    src, i = TARGETS[label][3]
    r = p1['orbits'][i] if src == 'p1' else c0['regions'][0]['base'][i]
    assert r['i'] == i
    return r['x0'], r['px0'], r


def cmd_lyap(label, N, rtol=1e-12, wkey='a'):
    (M, a_, beta), (E, Lz), dom, _ = TARGETS[label]
    x0, px0, rec = x0px0(label)
    t0 = time.time(); run = make_lyap(M, a_, beta, E, Lz, dom); tb = time.time() - t0
    run(x0, px0, W0[wkey], 2, rtol, rtol*1e-3, 1e9*float(M), 10**10)      # compile
    tc = time.time() - t0
    oc, nc, t, drift, steps, sec = run(x0, px0, W0[wkey], N, rtol, rtol*1e-3, 1e9*float(M), 10**10)
    el = time.time() - t0 - tc
    fn = os.path.join(WORK, f'lyap_{label}_{wkey}_{N}_{rtol:.0e}.npz')
    np.savez(fn, sec=sec[:nc], outcome=oc, ncross=nc, t=t, drift=drift, steps=steps, x0=x0, px0=px0, rtol=rtol,
             w0=W0[wkey], seconds=el, build_s=tb, compile_s=tc)
    lam = sec[nc - 1, 3]/sec[nc - 1, 4] if nc else float('nan')
    print(label, wkey, 'N', N, 'outcome', oc, 'returns', nc, 'drift %.2e' % drift, 'lambda_tau %.3e' % lam,
          'per_return %.3e' % (sec[nc - 1, 3]/nc if nc else float('nan')), 'run %.0f s' % el, 'build+compile %.0f s' % tc,
          flush=True)
    return fn


def cmd_integ():
    """Registered integrator (v13_orbit) on orbit 55 at three tolerances; A1/A2 as v13_screen.run_orbits."""
    from v13_orbit import make
    (M, a_, beta), (E, Lz), dom, _ = TARGETS['o55']
    x0, px0, rec = x0px0('o55')
    integ = make(M, a_, beta, E, Lz, domain=dom)[0]
    out = {}
    for rtol in (1e-11, 1e-12, 1e-13):
        t0 = time.time()
        oc, nc, tau, drift, steps, sec = integ(x0, px0, 2000, rtol, rtol*1e-3, 1e9*float(M), 400_000_000)
        d, n1, n2 = fma_diffusion(sec[:, 0], sec[:, 1])
        out[f'{rtol:.0e}'] = dict(outcome=int(oc), returns=int(nc), drift=float(drift), A1=d, nu1=n1, nu2=n2,
                                  A2=zero_one_K(sec[:, 0]), seconds=round(time.time() - t0, 1))
        np.save(os.path.join(WORK, f'integ_o55_{rtol:.0e}.npy'), sec[:nc])
        print(rtol, out[f'{rtol:.0e}'], flush=True)
    json.dump(out, open(os.path.join(WORK, 'integ_o55.json'), 'w'), indent=1)


# ---------------------------------------------------------------- analysis helpers
def zero_one_K_fast(phi, nc=100, seed=7):
    """The same statistic as v13_indicators.zero_one_K (same c draws, same ncut = N/10), with the mean-square
    displacement M_c(n) computed through FFT cross-correlation instead of an explicit loop (checked equal below)."""
    phi = np.asarray(phi, float); N = len(phi); ncut = N//10; rng = np.random.default_rng(seed)
    js = np.arange(1, N + 1); ns = np.arange(1, ncut + 1); Ks = []
    L = 1 << int(math.ceil(math.log2(2*N)))
    for c in rng.uniform(math.pi/5, 4*math.pi/5, nc):
        P = np.cumsum(phi*np.cos(js*c)) + 1j*np.cumsum(phi*np.sin(js*c))
        a2 = np.abs(P)**2; cs = np.concatenate([[0.0], np.cumsum(a2)])
        Fp = np.fft.fft(P, L); cc = np.fft.ifft(Fp*np.conj(Fp))[:ncut + 1]   # cc[n] = sum_j P[j+n] conj(P[j])
        cnt = N - ns
        s_hi = cs[N] - cs[ns]; s_lo = cs[N - ns]
        Mn = (s_hi + s_lo - 2*cc[ns].real)/cnt
        Vosc = (phi.mean())**2*(1 - np.cos(ns*c))/(1 - math.cos(c))
        Ks.append(np.corrcoef(ns, Mn - Vosc)[0, 1])
    return float(np.median(Ks))


def corr_dim(xs, ps, lo=-2.5, hi=-1.5, nr=11):
    from scipy.spatial import cKDTree
    u = np.c_[(xs - xs.min())/(xs.max() - xs.min()), (ps - ps.min())/(ps.max() - ps.min())]
    T = cKDTree(u); rs = np.logspace(lo, hi, nr)
    C = (T.count_neighbors(T, rs).astype(float) - len(u))/(len(u)*(len(u) - 1))
    ok = C > 0
    sl = np.polyfit(np.log10(rs[ok]), np.log10(C[ok]), 1)[0] if ok.sum() >= 3 else float('nan')
    return float(sl), [float(v) for v in C]


def lam_summary(fn):
    z = np.load(fn); sec = z['sec']; nc = int(z['ncross'])
    S, t = sec[:, 3], sec[:, 4]; n = np.arange(1, nc + 1)
    lt = S/t; lr = S/n
    chk = sorted(set([c for c in (10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000) if c <= nc] + [nc]))
    curve = [dict(n=int(c), tau=float(t[c - 1]), lam_tau=float(lt[c - 1]), lam_ret=float(lr[c - 1]),
                  lnt_over_t_ret=float(math.log(c)/c)) for c in chk]
    def slope(a, b):
        m = (n >= a) & (n <= b)
        return float(np.polyfit(np.log10(n[m]), np.log10(np.abs(lr[m])), 1)[0])
    last = (max(1, nc//10), nc)
    return dict(outcome=int(z['outcome']), returns=nc, drift=float(z['drift']), rtol=float(z['rtol']),
                seconds=float(z['seconds']), lam_tau_final=float(lt[-1]), lam_ret_final=float(lr[-1]),
                slope_last_decade=slope(*last), last_decade=list(map(int, last)),
                slope_first_decades=slope(max(1, nc//100), max(2, nc//10)) if nc >= 200 else None,
                curve=curve), sec


def geometry(sec, win=2000):
    xs, ps = sec[:, 0], sec[:, 1]; N = len(xs)
    d2, C = corr_dim(xs, ps); d2s, Cs = corr_dim(xs, ps, -3.5, -2.5)
    nus, Kw = [], []
    for k in range(N//win):
        s = slice(k*win, (k + 1)*win)
        z = (xs[s] - xs[s].mean()) + 1j*(ps[s] - ps[s].mean())
        nus.append(naff_freq(z)); Kw.append(zero_one_K_fast(xs[s]))
    A1w = [fma_diffusion(xs[k*win:(k + 1)*win], ps[k*win:(k + 1)*win])[0] for k in range(N//win)]
    return dict(N=N, x_range=[float(xs.min()), float(xs.max())], px_range=[float(ps.min()), float(ps.max())],
                D2=d2, D2_r=[-2.5, -1.5], D2_small=d2s, D2_small_r=[-3.5, -2.5], C=C, C_small=Cs,
                window=win, nu_windows=[float(v) for v in nus], nu_spread=float(max(nus) - min(nus)),
                K_windows=Kw, A1_windows=A1w, K_full=zero_one_K_fast(xs), A1_full=fma_diffusion(xs, ps)[0])


def phase_roughness(sec, nu):
    """Extra, NOT pre-registered: sort the section points by the phase frac(n nu) of the measured rotation number;
    on an invariant curve x(theta) is smooth and successive sorted differences are ~ |x'| / N; in a chaotic layer they
    are of order the layer width. Reported as the median |dx| relative to the x-range."""
    xs = sec[:, 0]; n = np.arange(len(xs)); th = np.mod(n*nu, 1.0); o = np.argsort(th)
    return float(np.median(np.abs(np.diff(xs[o])))/(xs.max() - xs.min()))


def extras(sec, g, thr):
    """Extra, NOT pre-registered (labelled): (a) phase roughness with the full-series NAFF frequency; (b) the strongest
    spectral lines of the centred section signal (are they all integer combinations of one frequency?); (c) how often
    the registered AND rule would fire on successive 2000-return windows of this single orbit; (d) the beat between the
    window length and the near-1/2 rotation number, 2000 (1 - 2|nu|) mod 1 cycles per window."""
    xs, ps = sec[:, 0], sec[:, 1]; z = (xs - xs.mean()) + 1j*(ps - ps.mean()); nu = naff_freq(z)
    w = 0.5*(1 - np.cos(2*math.pi*np.arange(len(z))/len(z))); Fz = np.abs(np.fft.fft(w*z)); f = np.fft.fftfreq(len(z))
    lines = []
    for i in np.argsort(Fz)[::-1]:
        if all(abs(f[i] - l[0]) > 2e-4 for l in lines): lines.append((float(f[i]), float(Fz[i]/Fz.max())))
        if len(lines) >= 8: break
    fires = [bool(a > thr['A1'] and k > thr['A2']) for a, k in zip(g['A1_windows'], g['K_windows'])]
    beat = (g['window']*(1 - 2*abs(nu))) % 1.0
    return dict(extra_label='NOT pre-registered', nu_full=float(nu), phase_roughness_extra=phase_roughness(sec, nu),
                spectral_lines=lines, and_rule_fires_windows=int(sum(fires)), n_windows=len(fires),
                A2_arm_fires_windows=int(sum(k > thr['A2'] for k in g['K_windows'])),
                A1_arm_fires_windows=int(sum(a > thr['A1'] for a in g['A1_windows'])),
                window_beat_cycles=float(beat), window_beat_period_windows=float(1/min(beat, 1 - beat)))


def cmd_analyze():
    p1, c0 = load_sealed()
    vers = dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, sympy=sp.__version__,
                numba=numba.__version__, machine=platform.platform(),
                head=subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=HERE).stdout.strip())
    out = dict(label='POST-HOC LABELLED DIAGNOSTIC; registered p1 verdict (1/60 CHAOTIC) and §7 Jaccard FAIL unchanged',
               versions=vers, sealed=dict(v13_counted_p1=SEAL_P1, v13_c0_gate=SEAL_C0), thresholds=p1['thresholds'])
    # self-check of the FFT 0-1 test against the registered implementation
    o55 = p1['orbits'][55]; sec55 = np.array(o55['sec'])
    out['K_fast_check'] = dict(registered=zero_one_K(sec55[:, 0]), fast=zero_one_K_fast(sec55[:, 0]),
                               sealed=o55['A2'])
    # 3. A2/A1 calibration
    rd = [r for r in p1['orbits'] if r['status'] == 'READ' and r['i'] != 55]
    K = np.array([r['A2'] for r in rd]); A1 = np.array([r['A1'] for r in rd])
    kn = json.load(open(os.path.join(RES, 'v13_kerr_null_p1.json')))
    kK = np.array([r['A2'] for L in kn['levels'] for r in L.get('orbits', []) if r.get('status') == 'READ'])
    kA1 = np.array([r['A1'] for L in kn['levels'] for r in L.get('orbits', []) if r.get('status') == 'READ'])
    out['calibration'] = dict(
        n_other_read=len(rd), A2_mean=float(K.mean()), A2_sd=float(K.std(ddof=1)), A2_min=float(K.min()),
        A2_max=float(K.max()), A2_absmax=float(np.abs(K).max()), z_o55=float((o55['A2'] - K.mean())/K.std(ddof=1)),
        rank_o55=int((K < o55['A2']).sum()) + 1, n_A2_positive=int((K > 0).sum()),
        n_A2_above_thr=int((K > p1['thresholds']['A2']).sum()),
        A1_n_above_thr=int((A1 > p1['thresholds']['A1']).sum()), A1_max=float(A1.max()),
        A1_rank_o55=int((A1 < o55['A1']).sum()) + 1,
        kerr_null_p1=dict(n=len(kK), A2_mean=float(kK.mean()), A2_sd=float(kK.std(ddof=1)), A2_min=float(kK.min()),
                          A2_max=float(kK.max()), A1_max=float(kA1.max())),
        others=[dict(i=r['i'], A1=r['A1'], A2=r['A2']) for r in rd])
    # 1-2. Lyapunov and geometry
    out['lyapunov'] = {}; out['geometry'] = {}
    for fn in sorted(os.listdir(WORK)):
        if not fn.startswith('lyap_'): continue
        key = fn[5:-4]; s, sec = lam_summary(os.path.join(WORK, fn)); out['lyapunov'][key] = s
        if s['returns'] >= 4000 and not key.startswith('c0'):
            g = geometry(sec); g.update(extras(sec, g, p1['thresholds']))
            out['geometry'][key] = g
        elif s['returns'] >= 2000:
            out['geometry'][key] = dict(N=s['returns'], D2=corr_dim(sec[:, 0], sec[:, 1])[0],
                                        K_full=zero_one_K_fast(sec[:, 0]))
    # 4. integrator check
    ij = os.path.join(WORK, 'integ_o55.json')
    if os.path.exists(ij):
        ic = json.load(open(ij)); out['integrator'] = ic
        s1, s2, s3 = [np.load(os.path.join(WORK, f'integ_o55_{r}.npy')) for r in ('1e-11', '1e-12', '1e-13')]
        sep = np.hypot(s2[:, 0] - s3[:, 0], s2[:, 1] - s3[:, 1])
        out['integrator']['sep_12_13'] = {str(n): float(sep[n - 1]) for n in (1, 10, 100, 500, 1000, 2000)}
        out['integrator']['sealed_reproduced'] = dict(dA1=abs(ic['1e-11']['A1'] - o55['A1']),
                                                      dA2=abs(ic['1e-11']['A2'] - o55['A2']),
                                                      max_point_diff=float(np.abs(s1[:, :2] - sec55[:, :2]).max()))
    json.dump(out, open(os.path.join(RES, 'v13_p1_o55_diag.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('calibration',)}, indent=1, default=str)[:6000])
    print(json.dumps({k: v for k, v in out['calibration'].items() if k != 'others'}, indent=1))


if __name__ == '__main__':
    for v in ('NUMBA_NUM_THREADS', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        assert os.environ.get(v) == '1', f'{v} must be 1'
    m = sys.argv[1]
    if m == 'timing': cmd_lyap(sys.argv[2] if len(sys.argv) > 2 else 'o55', 200)
    elif m == 'lyap': cmd_lyap(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 1e-12,
                               sys.argv[5] if len(sys.argv) > 5 else 'a')
    elif m == 'integ': cmd_integ()
    elif m == 'analyze': cmd_analyze()
