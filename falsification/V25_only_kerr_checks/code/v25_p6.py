"""V25 P6: negative claims. (a) ZV delta=2 exact metric (R-full): return maps around z=1 (zero of f0), around infinity
(identity through eps^3 predicted) and around the double pole (linear multipliers, secondary). (b) f0 = 1 - 2/z with a
twist dipole (R-trunc, E = 4/5): linear return maps around z = 0, +-3 predicted identity. (rho, p) coordinates."""
import os, json, math, cmath, numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'v25_full.py')).read().split('# ===== P2')[0])
class AxisPoly:
    def __init__(s, Dc, Dlc, E, mu=1):
        s.Dc, s.Dlc = np.array(Dc, complex), np.array(Dlc, complex); s.Nc = np.polysub(E**2*s.Dc, mu**2*s.Dlc)
        s.Y2c = np.polymul(s.Nc, s.Dc); s.dY2c = np.polyder(s.Y2c)
    Delta = lambda s, z: np.polyval(s.Dlc, z)
    Y2 = lambda s, z: np.polyval(s.Y2c, z)
def rp_map(ax, U, dU, zc, r, turns, eps_list=(0.02, 0.01, 0.005, 0.0025), rtol=1e-13, linear_only=False):
    U0 = lambda z: ax.Y2(z)/(2*ax.Delta(z)**2)
    e0 = 1e-7; Ml = np.zeros((2, 2), complex)
    for j, st in enumerate(((1, 0), (0, 1))):
        Z, y0, _ = loop_run(ax, U, dU, U0, zc, r, e0*st[0], e0*st[1], turns=turns, rtol=rtol); Ml[:, j] = Z[:2]/e0
    yret = abs(Z[2] - y0)/abs(y0)
    cub = {}
    if linear_only: return Ml, {(1, 0): (np.zeros(2), 0.0), (0, 1): (np.zeros(2), 0.0)}, yret
    for st in ((1, 0), (0, 1)):
        s = np.array(st, complex); As = []
        for e in eps_list:
            Z, _, _ = loop_run(ax, U, dU, U0, zc, r, e*st[0], e*st[1], turns=turns, rtol=rtol); As.append((Z[:2]/e - Ml @ s)/e**2)
        R = [(4*As[i + 1] - As[i])/3 for i in range(3)]; RR = [(16*R[i + 1] - R[i])/15 for i in range(2)]
        cub[st] = (RR[-1], float(np.max(np.abs(RR[-1] - RR[-2]))))
    return Ml, cub, yret
def loop_case(label, ax, U, dU, zc, radii, turns, expect_identity=True, **kw):
    res = [rp_map(ax, U, dU, zc, r, turns, **kw) for r in radii]
    (M1, c1, y1), (M2, c2, y2) = res
    lin_floor = max(y1, y2, float(np.max(np.abs(M1 - M2))), 1e-12)
    lin_dev = float(np.max(np.abs(M2 - np.eye(2))))
    cub_floor = max([float(np.max(np.abs(c1[s][0] - c2[s][0]))) for s in c1] + [c2[s][1] for s in c2] + [c1[s][1] for s in c1])
    cub_max = max(float(np.max(np.abs(c2[s][0]))) for s in c2)
    ev = np.linalg.eigvals(M2)
    rec = dict(label=label, M_lin=[[str(x) for x in row] for row in M2], lin_dev_from_I=lin_dev, lin_floor=lin_floor,
               eig=[str(e) for e in ev], cubic=[[str(x) for x in c2[s][0]] for s in c2], cubic_max=cub_max, cubic_floor=cub_floor)
    if expect_identity:
        lin_ok = lin_dev <= 100*lin_floor; cub_ok = cub_max <= 100*cub_floor
        rec['verdict'] = 'VOID' if cub_floor > 1e-4 else ('IDENTITY (pred holds)' if lin_ok and cub_ok else ('LINEAR NOT I' if not lin_ok else 'CUBIC NONZERO'))
    print(label, '| lin dev %.2e (floor %.1e) | eig' % (lin_dev, lin_floor), [complex(round(e.real, 6), round(e.imag, 6)) for e in ev],
          '| cubic max %.2e (floor %.1e)' % (cub_max, cub_floor), rec.get('verdict', ''), flush=True)
    return rec
out = {}
E = 0.8
# (a) ZV delta = 2, exact metric, sigma = 1: f0 = ((z-1)/(z+1))^2, D = (z+1)^2, Delta = (z-1)^2
axz = AxisPoly([1, 2, 1], [1, -2, 1], E)
Uz, dUz, _ = prolate_U('zv', sp.Rational(4, 5))
out['zv_z1'] = loop_case('ZV exact: loop around z=1 (zero of f0) [A2]', axz, Uz, dUz, 1.0, (0.4, 0.6), 1, eps_list=(0.08, 0.04, 0.02, 0.01), rtol=1e-14)
out['zv_inf'] = loop_case('ZV exact: loop around infinity (|z| = 15, 25)', axz, Uz, dUz, 0.0, (15.0, 25.0), 1)
rec = loop_case('ZV exact: loop around double pole z=-1 (secondary)', axz, Uz, dUz, -1.0, (0.3, 0.5), 1, expect_identity=False, linear_only=True)
rec['pred_multipliers_secondary'] = [math.exp(math.sqrt(2)*math.pi), math.exp(-math.sqrt(2)*math.pi)]; out['zv_dpole'] = rec
print('   secondary prediction e^{+-sqrt2 pi} =', rec['pred_multipliers_secondary'], flush=True)
# (b) f0 = 1 - 2/z (Fable coordinates), c0 = 0.3/(z-3) - 0.3/(z+3), R-trunc
z = sp.symbols('z'); f0S = 1 - 2/z; c0 = sp.Rational(3, 10)/(z - 3) - sp.Rational(3, 10)/(z + 3)
Us, dUs, U0s, _ = make_trunc(f0S, sp.diff(c0, z, 2)**2, z, sp.Rational(4, 5))
axs = AxisPoly([1, 0], [1, -2], E)
out['schw_z0'] = loop_case('Schw f0 + twist dipole: loop around z=0 (pole of f0, branch, 2 turns)', axs, Us, dUs, 0.0, (0.5, 1.0), 2)
out['schw_z3'] = loop_case('Schw f0 + twist dipole: loop around z=+3 (twist pole)', axs, Us, dUs, 3.0, (0.3, 0.6), 1)
out['schw_zm3'] = loop_case('Schw f0 + twist dipole: loop around z=-3 (twist pole)', axs, Us, dUs, -3.0, (0.3, 0.6), 1)
json.dump(out, open(os.path.join(HERE, '../results/v25_p6.json'), 'w'), indent=1, default=str)
