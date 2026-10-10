"""V11 -- the bridge's independent chaos-candidate checker (PREREGISTRATION.md). Own metric transcription (reused from
V10/V8), exact symbolic Jacobian, scipy DOP853 with exact y=0 section events, own S_ex and fd implementations."""
import sys, json, math, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
sys.path.insert(0, '../../V10_ts2_jet_bound/code')
from v10_jet import metric, X, Y          # V10's loader: ZV from V8's zv(), TS from the sealed component files

from kerr_ts_chart import kerr_ts, x as KX, y as KY
KERR = {'kerr45': (sp.Rational(4, 5), sp.Rational(3, 5)), 'kerr35': (sp.Rational(3, 5), sp.Rational(4, 5))}

def get_metric(case):
    if case in KERR:
        g, _ = kerr_ts(*KERR[case]); return {k: v.subs({KX: X, KY: Y}) for k, v in g.items()}
    return metric(case)

def carter(case, E, L):
    """Carter constant for Kerr in the TS chart: r = x + 1/p, cos(theta) = y, a = q/p (sigma = 1, m = 1/p), mu^2 = 1.
    Q = (1 - y^2) p_y^2 + y^2 (a^2 (1 - E^2) + L^2/(1 - y^2))."""
    p_, q_ = KERR[case]; a = float(q_/p_)
    return lambda s: (1 - s[1]**2)*s[3]**2 + s[1]**2*(a*a*(1 - E*E) + L*L/(1 - s[1]**2))

def build(case, E, L):
    """Compact fast build (V11 implementation note, 2026-10-10): only the scalar pieces A = g^xx, B = g^yy and W, with
    their first and second derivatives, are generated (common-subexpression eliminated) and compiled with numba; the
    vector field F and exact Jacobian J are assembled analytically from them. Same mathematics as the original build."""
    import numba
    g = get_metric(case); E, L = sp.nsimplify(E), sp.nsimplify(L)
    det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    Gtt, Gtp, Gpp = g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det
    A, B = 1/g['g_xx'], 1/g['g_yy']
    W = Gtt*E**2 - 2*Gtp*E*L + Gpp*L**2
    flat = []
    for f in (A, B, W):
        fx, fy = sp.diff(f, X), sp.diff(f, Y)
        flat += [f, fx, fy, sp.diff(fx, X), sp.diff(fx, Y), sp.diff(fy, Y)]
    pieces = numba.njit(sp.lambdify([X, Y], flat, 'math', cse=True))

    @numba.njit
    def FJ(x, y, px, py):
        q = pieces(x, y)
        a, ax, ay, axx, axy, ayy = q[0], q[1], q[2], q[3], q[4], q[5]
        b, bx, by, bxx, bxy, byy = q[6], q[7], q[8], q[9], q[10], q[11]
        w, wx, wy, wxx, wxy, wyy = q[12], q[13], q[14], q[15], q[16], q[17]
        px2, py2 = px*px, py*py
        F = (a*px, b*py, -0.5*(ax*px2 + bx*py2 + wx), -0.5*(ay*px2 + by*py2 + wy))
        J = ((ax*px, ay*px, a, 0.0), (bx*py, by*py, 0.0, b),
             (-0.5*(axx*px2 + bxx*py2 + wxx), -0.5*(axy*px2 + bxy*py2 + wxy), -ax*px, -bx*py),
             (-0.5*(axy*px2 + bxy*py2 + wxy), -0.5*(ayy*px2 + byy*py2 + wyy), -ay*px, -by*py))
        return F, J

    def fW(x, y): return pieces(x, y)[12]
    def fGyy(x, y): return pieces(x, y)[6]
    def fH(x, y, px, py):
        q = pieces(x, y); return 0.5*(q[0]*px*px + q[6]*py*py + q[12])
    return (FJ, None), None, fW, fGyy, fH

def build_reference(case, E, L):
    """The original (slow) build, kept only to validate the compact build."""
    g = get_metric(case); E, L = sp.nsimplify(E), sp.nsimplify(L)
    det = g['g_TT']*g['g_phiphi'] - g['g_Tphi']**2
    Gtt, Gtp, Gpp = g['g_phiphi']/det, -g['g_Tphi']/det, g['g_TT']/det
    Gxx, Gyy = 1/g['g_xx'], 1/g['g_yy']
    W = Gtt*E**2 - 2*Gtp*E*L + Gpp*L**2
    px, py = sp.symbols('px py', real=True)
    H = (Gxx*px**2 + Gyy*py**2 + W)/2
    s = [X, Y, px, py]
    F = [sp.diff(H, px), sp.diff(H, py), -sp.diff(H, X), -sp.diff(H, Y)]
    J = [[sp.diff(f, v) for v in s] for f in F]
    return sp.lambdify(s, [F, J], 'numpy')

def frequency_drift(xs):
    n = len(xs)
    if n < 100: return None
    def peak(a):
        a = np.asarray(a, float); a = (a - a.mean()) * np.hanning(len(a)); P = np.abs(np.fft.rfft(a)); P[0] = 0
        k = int(np.argmax(P))
        if 0 < k < len(P) - 1:
            al, b, c = P[k - 1], P[k], P[k + 1]; den = al - 2 * b + c; d = 0.5 * (al - c) / den if den != 0 else 0.0
        else: d = 0.0
        return (k + d) / len(a)
    h = n // 2; f1, f2 = peak(xs[:h]), peak(xs[h:2 * h])
    return abs(f1 - f2) / (0.5 * (f1 + f2))

def _std(xs, ps):
    a = np.array([xs, ps], float).T; return (a - a.mean(0)) / a.std(0)

def roughness(xs, ps, K=12):
    if len(xs) < 100: return None
    a = _std(xs, ps); th = np.arctan2(a[:, 1], a[:, 0]); r = np.hypot(a[:, 0], a[:, 1])
    A = np.column_stack([np.ones_like(th)] + [f(k * th) for k in range(1, K + 1) for f in (np.cos, np.sin)])
    coef, *_ = np.linalg.lstsq(A, r, rcond=None); res = r - A @ coef
    return float(np.sqrt(np.mean(res**2)) / np.sqrt(np.mean((r - r.mean())**2)))

def nn_dimension(xs, ps):
    if len(xs) < 100: return None
    a = _std(xs, ps)
    def med_nn(b):
        d = np.sqrt(((b[:, None, :] - b[None, :, :])**2).sum(-1)); np.fill_diagonal(d, np.inf); return np.median(d.min(1))
    d1, dh = med_nn(a), med_nn(a[:len(a) // 2])
    return float(np.log(2) / np.log(dh / d1)) if dh > d1 else float('inf')

class StepCap(Exception): pass

def run_orbit(fF, fJ, fW, fGyy, fH, x0, tol, ncross=300, tau_max=5e6, dtau=10.0, Qf=None, max_evals=2_000_000):
    """max_evals is now a PER-CHUNK stall guard (addendum 6); plunge (x = 1.5) and escape (x = 2000) are terminal
    integrator events, so a plunge inside a chunk is caught at the crossing instead of at the chunk end."""
    py0 = math.sqrt((-1 - fW(x0, 0.0)) / fGyy(x0, 0.0))
    s = np.array([x0, 0.0, 0.0, py0]); v = np.array([1, 0.7, -0.4, 0.3]); v = v / np.linalg.norm(v)
    FJ = fF[0]; nev = [0]
    def rhs(t, z):
        nev[0] += 1
        if nev[0] > max_evals: raise StepCap()   # per-chunk counter, reset before every chunk
        Fv, Jv = FJ(*z[:4])
        return np.concatenate([np.array(Fv, float), np.array(Jv, float) @ z[4:]])
    def ev(t, z): return z[1]
    ev.direction = 1
    def pl(t, z): return z[0] - 1.5
    pl.terminal = True; pl.direction = -1
    def es(t, z): return z[0] - 2000.0
    es.terminal = True; es.direction = 1
    tau = 0.0; S = 0.0; xs = []; pxs = []; status = 'max_tau'; tau_last = 0.0
    Q0 = Qf(s) if Qf else None; Qdev = 0.0; S_cross = None; tau_cross = None; prev_cross = (None, None)
    while tau < tau_max:
        nev[0] = 0
        try:
            sol = solve_ivp(rhs, (tau, tau + dtau), np.concatenate([s, v]), method='DOP853', rtol=tol, atol=tol * 1e-2, events=[ev, pl, es])
        except StepCap:
            status = 'stalled'; break
        for ze in sol.y_events[0]:
            if ze[3] > 0: xs.append(ze[0]); pxs.append(ze[2])
        z = sol.y[:, -1]; s = z[:4]; v = z[4:]; tau = sol.t[-1]
        nv = np.linalg.norm(v); S += math.log(nv); v = v / nv; tau_last = tau
        if len(sol.t_events[0]): prev_cross = (S_cross, tau_cross); S_cross, tau_cross = S, tau   # truncated at the last crossing
        if Qf and s[0] >= 1.5: Qdev = max(Qdev, abs(Qf(s) - Q0) / abs(Q0))
        if len(sol.t_events[1]) or s[0] < 1.5:
            status = 'plunge'
            if len(sol.t_events[0]) and prev_cross[1]: S_cross, tau_cross = prev_cross   # chunk with the last crossing also holds the plunge
            break
        if len(sol.t_events[2]) or s[0] > 2000: status = 'escape'; break
        if len(xs) >= ncross: status = 'crossings'; break
    Sex = S - math.log(tau_last) if tau_last > 0 else float('nan')
    Sex_trunc = (S_cross - math.log(tau_cross)) if tau_cross else float('nan')
    return dict(x0=x0, tol=tol, status=status, crossings=len(xs), tau=tau, S_ex=Sex, S_ex_trunc=Sex_trunc, carter_rel_dev=Qdev if Qf else None,
                fd=frequency_drift(xs[:ncross]), R=roughness(xs[:ncross], pxs[:ncross]), D=nn_dimension(xs[:ncross], pxs[:ncross]),
                section=[list(map(float, xs[:ncross])), list(map(float, pxs[:ncross]))],
                H_drift=float(abs(2 * fH(*s) + 1)))

def classify(r):
    S = r['S_ex_trunc'] if r['S_ex_trunc'] == r['S_ex_trunc'] else r['S_ex']
    return 'CHAOTIC' if (S >= 10 or (r['fd'] is not None and r['fd'] >= 0.0115)) else 'REGULAR'

if __name__ == '__main__':
    case, E, L = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); x0s = [float(a) for a in sys.argv[4:]]
    fns = build(case, E, L); Qf = carter(case, E, L) if case in KERR else None
    for x0 in x0s:
        rs = [run_orbit(*fns, x0, tol, Qf=Qf) for tol in (1e-11, 1e-13)]
        cls = [classify(r) for r in rs]; verdict = cls[0] if cls[0] == cls[1] else 'INCONCLUSIVE'
        for r, c in zip(rs, cls): print(json.dumps({k: v for k, v in {**r, 'case': case, 'E': E, 'L': L, 'class': c}.items() if k != 'section'}), flush=True)
        print(f'== {case} E={E} L={L} x0={x0}: {verdict}', flush=True)
        with open('../results/v11_runs.jsonl', 'a') as f:
            for r, c in zip(rs, cls): f.write(json.dumps({**r, 'case': case, 'E': E, 'L': L, 'class': c, 'verdict': verdict}) + '\n')
