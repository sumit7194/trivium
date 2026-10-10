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
    lam = lambda e, args: sp.lambdify(args, e, 'numpy', cse=True)
    return lam(F, s), lam(J, s), lam(W, [X, Y]), lam(Gyy, [X, Y]), lam(H, s)

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

def run_orbit(fF, fJ, fW, fGyy, fH, x0, tol, ncross=300, tau_max=5e6, dtau=10.0, Qf=None):
    py0 = math.sqrt((-1 - fW(x0, 0.0)) / fGyy(x0, 0.0))
    s = np.array([x0, 0.0, 0.0, py0]); v = np.array([1, 0.7, -0.4, 0.3]); v = v / np.linalg.norm(v)
    def rhs(t, z):
        return np.concatenate([np.array(fF(*z[:4]), float), np.array(fJ(*z[:4]), float) @ z[4:]])
    def ev(t, z): return z[1]
    ev.direction = 1
    tau = 0.0; S = 0.0; xs = []; status = 'max_tau'; tau_last = 0.0
    Q0 = Qf(s) if Qf else None; Qdev = 0.0; S_cross = None; tau_cross = None
    while tau < tau_max:
        sol = solve_ivp(rhs, (tau, tau + dtau), np.concatenate([s, v]), method='DOP853', rtol=tol, atol=tol * 1e-2, events=ev)
        for ze in sol.y_events[0]:
            if ze[3] > 0: xs.append(ze[0])
        z = sol.y[:, -1]; s = z[:4]; v = z[4:]; tau = sol.t[-1]
        nv = np.linalg.norm(v); S += math.log(nv); v = v / nv; tau_last = tau
        if len(sol.t_events[0]): S_cross, tau_cross = S, tau          # score truncated at the last crossing (amendment-4 style)
        if Qf and s[0] >= 1.5: Qdev = max(Qdev, abs(Qf(s) - Q0) / abs(Q0))
        if s[0] < 1.5: status = 'plunge'; break
        if s[0] > 2000: status = 'escape'; break
        if len(xs) >= ncross: status = 'crossings'; break
    Sex = S - math.log(tau_last) if tau_last > 0 else float('nan')
    Sex_trunc = (S_cross - math.log(tau_cross)) if tau_cross else float('nan')
    return dict(x0=x0, tol=tol, status=status, crossings=len(xs), tau=tau, S_ex=Sex, S_ex_trunc=Sex_trunc, carter_rel_dev=Qdev if Qf else None,
                fd=frequency_drift(xs[:ncross]),
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
        for r, c in zip(rs, cls): print(json.dumps({**r, 'case': case, 'E': E, 'L': L, 'class': c}), flush=True)
        print(f'== {case} E={E} L={L} x0={x0}: {verdict}', flush=True)
        with open('../results/v11_runs.jsonl', 'a') as f:
            for r, c in zip(rs, cls): f.write(json.dumps({**r, 'case': case, 'E': E, 'L': L, 'class': c, 'verdict': verdict}) + '\n')
