"""V24 addendum D: C^1 leaf continuation in the brake cap (float sample). Bridge code."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); __file__ = os.path.join(HERE, 'v24_i3.py')
exec(open(os.path.join(HERE, 'v24_i3.py')).read().split('vgrid = np.linspace')[0])
ub = float(sol.sol(tb)[0]); gb = ub
gp_orbit = float(g1(np.array([vb + 1e-7]))[0])
_, Vu_b, Vv_b = Vuv(ub, vb); gp_jet = float(Vu_b/Vv_b)
out = dict(v_b=vb, u_b=ub, gprime_orbit=gp_orbit, gprime_jet=gp_jet, D0_rel=abs(gp_orbit/gp_jet - 1))
print('D0: g\'(v_b) orbit %.8f  jet V_u/V_v %.8f  rel %.2e' % (gp_orbit, gp_jet, out['D0_rel']), flush=True)
def cap_scan(slope, n=2001):
    vv = np.linspace(vb - 2e-3, vb, n, endpoint=False); uu = np.linspace(u1, ub + 1e-3, n)
    U_, V_ = np.meshgrid(uu, vv); Vp, Vu, Vv = Vuv(U_, V_); hill = Vp <= 0
    den = (gb - u1) + slope*(V_ - vb); tau = (U_ - u1)/den
    inZ = hill & (tau >= 0) & (tau <= 1)
    C = -Vu + tau*slope*Vv
    r = np.hypot(U_ - ub, V_ - vb)
    res = dict(points=int(inZ.sum()), hill_beyond_tau1=int((hill & (tau > 1)).sum()))
    if inZ.any():
        Ci = C[inZ]; res['maxC'] = float(Ci.max()); k = np.argmax(Ci)
        res['maxC_at'] = (float(tau[inZ][k]), float(V_[inZ][k]), float(U_[inZ][k])); res['min_negC_over_r'] = float(np.min(-Ci/r[inZ]))
    return res
D = cap_scan(gp_orbit); out['D1_D2'] = D
print('D1/D2 (slope g\'(v_b)):', D, flush=True)
NEG = cap_scan(2*gp_orbit); out['NEG_slope2x'] = NEG
print('must-fail (slope 2g\'(v_b)):', NEG, flush=True)
# corner sanity for Fable's straight continuation: tau_v^+ - tau_v^- at v = v_b
cs = []
for uq in np.linspace(u1 + 0.01, ub - 0.005, 5):
    tau = (uq - u1)/(gb - u1); cs.append(float(-tau*gp_orbit/(gb - u1) - 0.0))
out['corner_jump_straight'] = cs; print('straight-continuation corner jump tau_v+ - tau_v- at 5 points:', ['%.4f' % c for c in cs], flush=True)
out['D_verdict'] = dict(D0=out['D0_rel'] <= 1e-6, D1=D.get('maxC', 1) < 0, D2=D.get('min_negC_over_r', -1) > 0,
                        NEG_fires=NEG.get('maxC', -1) > 0, corner_positive=all(c > 0 for c in cs))
print('verdicts:', out['D_verdict'], flush=True)
json.dump(out, open(os.path.join(HERE, '../results/v24_capD.json'), 'w'), indent=1, default=str)
