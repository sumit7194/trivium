"""V7b -- geometry and set algebra behind 'SSA => concavity in flow time', checked by the bridge's own code.

Complex coordinate z on the t = 0 plane (LMW's Euclidean 'time' axis is Re z).
  V_u = (P - u K)/2  <->  holomorphic field (1 - u z^2)/2          fixed points z = +-1/sqrt(u)
  zeta = (1 + sqrt(u) z)/(1 - sqrt(u) z),  w = log zeta             V_u acts as w -> w + sqrt(u) tau
Eye E(u'): the lens through z = +-i with cusps at +-1/sqrt(u').  U = E n {Re z > 0},  L = E n {Re z < 0}.
Flowed family (T = sqrt(u) tau, in w units):  R(T) = L  u  {0 <= Re w <= T, |Im w| < theta(u)/2}  u  (U + T).
Claim checked here (b2/b3):
  u < u' :  R(Tm) u (R(Tm)+D) = R(T2)   and   R(Tm) n (R(Tm)+D) = R(T1)+D        (D = Tm - T1 = T2 - Tm)
  u > u' :  the same with u and n swapped (complements have the interval structure; purity makes SSA symmetric)
Either way SSA gives  2 S(R(Tm)) >= S(R(T1)) + S(R(T2))  once S(X + D) = S(X) up to the local terms that cancel.
"""
import numpy as np, sympy as sp, json, sys

out = {}
# ---------------- b1: symbolic facts ----------------
z, u, up, th = sp.symbols('z u uprime theta', positive=True)
V = (1 - u*z**2)/2
zeta = (1 + sp.sqrt(u)*z)/(1 - sp.sqrt(u)*z)
b1_translation = sp.simplify(V*sp.diff(zeta, z) - sp.sqrt(u)*zeta)          # must be 0
zi = zeta.subs(z, sp.I)
b1_mod = sp.simplify(sp.Abs(sp.expand_complex(zi))**2)                      # |zeta(i)|^2 must be 1
# arg zeta(i) = 2 arctan sqrt(u) = theta(u)/2 with tan(theta/4) = sqrt(u)
uv = 0.37
argzi = complex(zi.subs(u, uv).evalf())
b1_arg = abs(np.angle(argzi) - 2*np.arctan(np.sqrt(uv)))
# eye through +-i with cusps +-1/sqrt(u'): circle centre (0,c), c = (1 - 1/u')/2, radius 1 - c
def eye_angle(uprime):
    c = (1 - 1/uprime)/2
    x0 = 1/np.sqrt(uprime)
    radial = np.array([x0, -c]); tang = np.array([radial[1], -radial[0]])     # perpendicular to radius
    alpha = np.arctan2(abs(tang[1]), abs(tang[0]))                             # angle of eyelid with real axis at cusp
    if c > 0: alpha = np.pi - alpha
    return 2*alpha                                                              # full cusp angle theta
b1_eye = max(abs(eye_angle(q) - 4*np.arctan(np.sqrt(q))) for q in [0.03, 0.1, 0.3, 0.6, 0.9, 1.0])
# attractor contraction rate: d/dz V at 1/sqrt(u) = -sqrt(u)
b1_rate = sp.simplify(sp.diff(V, z).subs(z, 1/sp.sqrt(u)) + sp.sqrt(u))
out['b1'] = dict(translation_residual=str(b1_translation), zeta_i_modulus_sq=str(b1_mod),
                 arg_error=float(b1_arg), eye_angle_max_error=float(b1_eye), attractor_rate_residual=str(b1_rate))
print('b1', out['b1'])

# ---------------- b2/b3: set algebra on a jittered w-grid ----------------
rng = np.random.default_rng(7)
def members(uu, uprime, notch=False):
    su = np.sqrt(uu); thu = 4*np.arctan(su)
    c = (1 - 1/uprime)/2; R0 = 1 - c
    def zof(w):
        zt = np.exp(w); return (zt - 1)/(su*(zt + 1))
    def in_eye(zz):
        ok = (np.abs(zz - 1j*c) < R0) & (np.abs(zz + 1j*c) < R0)
        if notch:   # control: bite a disc out of the upper half-eye, breaking the interval structure
            ok &= ~(np.abs(zz - (0.45/np.sqrt(uprime) + 0.0j)) < 0.12/np.sqrt(uprime))
        return ok
    def L(w): zz = zof(w); return in_eye(zz) & (zz.real < 0)
    def U(w): zz = zof(w); return in_eye(zz) & (zz.real > 0)
    def band(w): return np.abs(w.imag) < thu/2
    def R(T):
        def f(w):
            out = np.zeros(w.shape, bool)
            m1 = w.real <= 0; m2 = (w.real > 0) & (w.real <= T); m3 = w.real > T
            out[m1] = L(w[m1]); out[m2] = band(w[m2]); out[m3] = U(w[m3] - T)
            return out
        return f
    return R, band

def check(uu, uprime, T1, T2, notch=False, n=(900, 700)):
    R, band = members(uu, uprime, notch)
    Tm = (T1 + T2)/2; D = Tm - T1
    lo, hi = -6.0, T2 + 6.0
    xr = np.linspace(lo, hi, n[0]); yr = np.linspace(-np.pi, np.pi, n[1], endpoint=False)
    X, Y = np.meshgrid(xr, yr)
    # Im-jitter is per ROW: a row of fixed Im w is one flow line of V_u.  (Post-run fix, 2026-09-24: the first
    # run jittered Im w per point, which moved points off their flow line and produced 1 spurious broken row.)
    W = (X + rng.uniform(-1e-4, 1e-4, X.shape)) + 1j*(Y + rng.uniform(-1e-4, 1e-4, (Y.shape[0], 1)))
    A = R(Tm)(W); B = R(Tm)(W - D); R2 = R(T2)(W); R1D = R(T1)(W - D)
    inner = uu < uprime
    uni, inter = (R2, R1D) if inner else (R1D, R2)
    bad_union = int(np.sum((A | B) != uni)); bad_inter = int(np.sum((A & B) != inter))
    # reversed control: the other branch's assignment must fail
    uni_r, inter_r = (R1D, R2) if inner else (R2, R1D)
    rev = int(np.sum((A | B) != uni_r) + np.sum((A & B) != inter_r))
    # interval structure: along each flow line (row of fixed Im w), R(T2) is one contiguous run (u<u') or
    # its complement is one contiguous run inside the window (u>u')
    runs_bad = 0
    Rrow = R2 if inner else ~R2
    for row in Rrow:
        d = np.diff(row.astype(int)); runs = int(np.sum(d == 1) + (row[0] == 1))
        if runs > 1: runs_bad += 1
    return dict(u=uu, uprime=uprime, T1=T1, T2=T2, notch=notch, inner=inner, bad_union=bad_union,
                bad_inter=bad_inter, reversed_control_mismatches=rev, rows_not_one_interval=runs_bad,
                area_R2=int(R2.sum()))

grid = [0.05, 0.15, 0.3, 0.5, 0.75, 0.95]
Ts = [(0.0, 1.2), (0.4, 1.0), (0.2, 2.6)]
res = []
for uu in grid:
    for uq in grid:
        if uu == uq: continue
        for T1, T2 in Ts:
            res.append(check(uu, uq, T1, T2))
ctrl = [check(uu, uq, 0.0, 1.2, notch=True) for uu, uq in [(0.15, 0.5), (0.3, 0.75), (0.05, 0.95)]]
out['b2b3'] = res; out['controls_notch'] = ctrl
tot = lambda k, L: sum(r[k] for r in L)
print('b2/b3 cases:', len(res), ' union mismatches:', tot('bad_union', res), ' intersection mismatches:', tot('bad_inter', res),
      ' rows not one interval:', tot('rows_not_one_interval', res))
print('reversed-assignment control: min mismatches over cases =', min(r['reversed_control_mismatches'] for r in res))
print('notch controls (must fail):', [(c['bad_union'] + c['bad_inter'], c['rows_not_one_interval']) for c in ctrl])
json.dump(out, open('../results/v7b_geometry.json', 'w'), indent=1, default=str)
