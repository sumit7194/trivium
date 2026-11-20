"""V24 addendum C: sample check of the 1D lobe conditions with the Bridge's V20 section map (ts45, E=97/100, L=41/8)."""
import sys, os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V20_ts_capture_edge_tangle/code'))
import v20
FJ, fW, fH = v20.field('ts45', 0.97, 41/8)
RT = 1e-12
z, Dm, T, clos = v20.polish(FJ, fH, 9.8045591682, RT)
ev, Vv = np.linalg.eig(Dm); k = int(np.argmax(np.abs(ev))); lam = float(np.real(ev[k])); eu = np.real(Vv[:, k]); eu /= np.linalg.norm(eu)
xs = z[0]
# outward branch: first excursion to x > x*
sgn = 1.0 if v20.P(FJ, fH, z + 1e-6*lam**2*eu, RT)[0][0] > xs else -1.0
out = dict(x_star=xs, lam=lam, closure=clos, branch=sgn)
s0 = 1e-6; seeds = [z + sgn*s*eu for s in np.geomspace(s0, s0*lam, 400, endpoint=False)]
U_pts = [p.copy() for p in seeds]; cur = [p.copy() for p in seeds]; crossed = [False]*len(seeds); lost_before_h = 0
for it in range(12):
    nxt = []
    for i, p in enumerate(cur):
        if p is None or crossed[i]: nxt.append(p); continue
        q = v20.P(FJ, fH, p, RT)[0]
        if q is None: lost_before_h += 1; nxt.append(None); continue
        if q[1] <= 0: crossed[i] = True; nxt.append(q); continue
        U_pts.append(q.copy()); nxt.append(q)
    cur = nxt
    if all(crossed[i] or cur[i] is None for i in range(len(cur))): break
U = np.array(U_pts); order = np.argsort(U[:, 0]); U = U[order]
xh = float(np.max(U[:, 0])); out.update(U_points=len(U), x_h_est=xh, lost_before_h=lost_before_h,
                                       U_min_px_interior=float(np.min(U[(U[:, 0] > xs + 1e-3) & (U[:, 0] < xh - 1e-3), 1])),
                                       U_graph_monotone_x=bool(np.all(np.diff(U[:, 0]) >= 0)))
print('gamma x*', xs, 'lam', lam, '| U pts', len(U), 'x_h~', xh, 'min p_x (interior)', out['U_min_px_interior'], 'lost', lost_before_h, flush=True)
Uf = lambda x: np.interp(x, U[:, 0], U[:, 1])
def inside_D(p, margin=1e-7): return xs < p[0] < xh and abs(p[1]) < Uf(p[0]) - margin
# beyond h: the crossed points, 6 more returns
c1a = c1b = 0; gate_in = 0; plunged_after = 0; n = 0; records = []
for i, p in enumerate(cur):
    if p is None or not crossed[i]: continue
    n += 1; q = p; went_in = False; inD = False; ok = True
    for r in range(7):
        if q[0] < xs and q[1] < 0: went_in = True; break
        if r > 0 and inside_D(q): inD = True
        q2 = v20.P(FJ, fH, q, RT)[0]
        if q2 is None:
            ok = (v20.P.last == 'plunge'); went_in = ok; break
        q = q2
    if not ok: c1a += 1
    if inD: c1b += 1
    if went_in: gate_in += 1
    records.append(dict(went_in=went_in, entered_D=inD))
out.update(beyond_h_points=n, C1a_failures=c1a, C1b_entered_D=c1b, C2_went_in=gate_in)
print('beyond h: points', n, 'C1a fail', c1a, 'entered D', c1b, 'went in through gate', gate_in, flush=True)
# controls
inward = [z - sgn*s*eu for s in np.geomspace(s0, s0*lam, 30, endpoint=False)]
inw_plunge = 0
for p in inward:
    q = p
    for r in range(8):
        q2 = v20.P(FJ, fH, q, RT)[0]
        if q2 is None: inw_plunge += (v20.P.last == 'plunge'); break
        q = q2
out['CTRL_inward_plunge'] = f'{inw_plunge}/30'
interior_return = 0
for x in np.linspace(xs + 2, xh - 2, 10):
    q = np.array([x, 0.5*Uf(x)]); back = False
    for r in range(6):
        q = v20.P(FJ, fH, q, RT)[0]
        if q is None: break
        if inside_D(q): back = True; break
    interior_return += back
out['NEGCTRL_interior_returns_to_D'] = f'{interior_return}/10'
print('CTRL inward plunge', out['CTRL_inward_plunge'], '| NEG interior points returning to D', out['NEGCTRL_interior_returns_to_D'], flush=True)
json.dump(out, open(os.path.join(HERE, '../results/v24_lobes.json'), 'w'), indent=1, default=str)
