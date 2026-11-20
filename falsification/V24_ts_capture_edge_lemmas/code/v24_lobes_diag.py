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
# DIAGNOSTIC (post-result, not a registered test): per-point record in seed order
rows = []
for i, p in enumerate(cur):
    if p is None or not crossed[i]: continue
    gap = abs(p[1]) - Uf(p[0]); on_arc = (p[0] >= xh) or (gap > 1e-9)
    j = int(np.searchsorted(U[:, 0], p[0])); hloc = float(U[min(j, len(U)-1), 0] - U[max(j-1, 0), 0])
    q = p; hits = []
    for r in range(7):
        if q[0] < xs and q[1] < 0: break
        if inside_D(q): hits.append((r, float(q[0]), float(q[1]), float(Uf(q[0]) - abs(q[1]))))
        q2 = v20.P(FJ, fH, q, RT)[0]
        if q2 is None: break
        q = q2
    rows.append(dict(i=i, x=float(p[0]), px=float(p[1]), gap=float(gap), on_arc=bool(on_arc), U_spacing=hloc, inD_hits=hits))
for k, rw in enumerate(rows):
    prev = rows[k-1]['on_arc'] if k else None; nxt = rows[k+1]['on_arc'] if k+1 < len(rows) else None
    rw['class_change_adjacent'] = (prev is not None and prev != rw['on_arc']) or (nxt is not None and nxt != rw['on_arc'])
bad = [r for r in rows if r['on_arc'] and r['inD_hits']]
print('bad', len(bad)); [print(b) for b in bad]
print('transitions in seed order:', [(rows[k]['i'], rows[k]['on_arc']) for k in range(1, len(rows)) if rows[k]['on_arc'] != rows[k-1]['on_arc']])
json.dump(dict(rows=rows, xs=xs, xh=xh), open(os.path.join(HERE, '../results/v24_lobes_C1diag.json'), 'w'), indent=1, default=str)
