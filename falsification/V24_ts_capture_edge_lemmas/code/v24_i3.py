"""V24 addendum B: sample check of Fable's I3 on gamma-adapted leaves, in the flat (u, v) plane. Bridge code only."""
import json, os, math, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v24.py')).read().split('# ---- R1')[0])
HERE = os.path.dirname(os.path.abspath(__file__))
Vxy = sp.cancel(F*(W + 1)/2)
Vf = sp.lambdify((X, Y), Vxy, 'numpy'); Vxf = sp.lambdify((X, Y), sp.diff(Vxy, X), 'numpy'); Vyf = sp.lambdify((X, Y), sp.diff(Vxy, Y), 'numpy')
def Vuv(u, v):
    x, y = np.cosh(u), np.cos(v)
    return Vf(x, y), Vxf(x, y)*np.sinh(u), -Vyf(x, y)*np.sin(v)        # V, V_u, V_v

def rhs(t, z):
    u, v, pu, pv = z; _, Vu, Vv = Vuv(u, v); return [pu, pv, -Vu, -Vv]
def brake_ev(t, z): return z[3]
brake_ev.terminal = True; brake_ev.direction = 1                     # p_v rises through 0 (p_v starts negative)

def shoot(xs, dense=False):
    u0 = math.acosh(xs); V0, _, _ = Vuv(u0, math.pi/2)
    z0 = [u0, math.pi/2, 0.0, -math.sqrt(-2*V0)]
    sol = solve_ivp(rhs, (0, 5), z0, method='DOP853', rtol=1e-12, atol=1e-14, events=brake_ev, dense_output=dense,
                    t_eval=[] if not dense else None)
    zb = sol.y_events[0][0]; return sol, zb

f = lambda xs: shoot(xs)[1][2]                                          # p_u at the brake point
xs = brentq(f, 9.80, 9.81, xtol=1e-15)
sol, zb = shoot(xs, dense=True)
Vb = Vuv(zb[0], zb[1])[0]
out = dict(x_star=xs, brake_x=math.cosh(zb[0]), brake_y=math.cos(zb[1]), brake_pu=zb[2], brake_V=float(Vb), t_brake=sol.t_events[0][0])
print('gamma: x*', xs, 'brake (x, y)', out['brake_x'], out['brake_y'], 'p_u', zb[2], 'V', Vb, flush=True)

tb = sol.t_events[0][0]
vb = float(sol.sol(tb)[1])
def at_v(vq):
    """exact orbit quantities at latitude vq: (u, g', g'') with g' = p_u/p_v, g'' = (p_v(-V_u) - p_u(-V_v))/p_v^3."""
    t = brentq(lambda tt: float(sol.sol(tt)[1]) - vq, 0, tb, xtol=1e-15)
    u, v, pu, pv = sol.sol(t); _, Vu, Vv = Vuv(u, v)
    return u, pu/pv, (pv*(-Vu) - pu*(-Vv))/pv**3
class G:  # vectorised wrapper
    def __init__(s, k): s.k = k
    def __call__(s, vv): return np.array([at_v(float(x))[s.k] for x in np.atleast_1d(vv)])
g, g1, g2 = G(0), G(1), G(2)
out['gamma_method'] = 'B1 exact orbit derivatives'
u1 = math.acosh(9.3)
vgrid = np.linspace(vb + 1e-3, math.pi/2, 400)
taus = list(np.arange(0, 1.0, 0.01)) + [0.999, 0.9999, 1.0]
worst_ratio = math.inf; maxC = -math.inf; outside = 0; tau1_max = 0.0; worst_at = None
for tau in taus:
    gu = u1 + tau*(g(vgrid) - u1); gp = tau*g1(vgrid); gpp = tau*g2(vgrid)
    V, Vu, Vv = Vuv(gu, vgrid)
    C = -Vu + gp*Vv + 2*V*gpp/(1 + gp*gp)
    inside = V <= 0; outside += int(np.sum(~inside))
    if tau == 1.0:
        tau1_max = float(np.max(np.abs(C))); continue
    Ci = C[inside]
    if Ci.size:
        maxC = max(maxC, float(Ci.max()))
        r = float(np.min(-Ci/(1 - tau)))
        if r < worst_ratio: worst_ratio = r; worst_at = (tau, float(vgrid[inside][np.argmin(-Ci/(1 - tau))]))
out.update(I3_maxC=maxC, I3_min_ratio=worst_ratio, I3_worst_at=worst_at, points_outside_hill=outside, C_at_tau1_max=tau1_max)
print('I3: max C (inside Hill) %.3e  min -C/(1-tau) %.4f at %s  outside-Hill pts %d  |C| at tau=1: %.2e' %
      (maxC, worst_ratio, worst_at, outside, tau1_max), flush=True)
# equator / brake values of -C/(1-tau) as tau -> 1
for vlab, vv0 in (('equator', math.pi/2), ('near brake', vb + 1e-3)):
    tau = 0.9999; gu = u1 + tau*(g(vv0) - u1); gp = tau*g1(vv0); gpp = tau*g2(vv0); V, Vu, Vv = Vuv(gu, vv0)
    out[f'ratio_{vlab}'] = float(np.ravel(-(-Vu + gp*Vv + 2*V*gpp/(1 + gp*gp))/(1 - tau))[0]); print(vlab, out[f'ratio_{vlab}'])
# negative control: straight leaves u = const, x in [9.50, 9.80]: C = -V_u must be >= 0 somewhere inside Hill
cnt = 0; mx = -math.inf
for x in np.linspace(9.50, 9.80, 61):
    u = math.acosh(x); vv2 = np.linspace(vb, math.pi/2, 400); V, Vu, Vv = Vuv(np.full_like(vv2, u), vv2)
    m = V <= 0
    if m.any(): mx = max(mx, float((-Vu[m]).max())); cnt += int(np.sum(-Vu[m] >= 0))
out['NEG_straight_leaves_maxC'] = mx; out['NEG_count_C_ge_0'] = cnt
print('NEG straight leaves: max C', mx, 'count C>=0', cnt, flush=True)
json.dump(out, open(os.path.join(HERE, '../results/v24_i3_B1.json'), 'w'), indent=1, default=str)
