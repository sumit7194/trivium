"""V13 transition graph between hyperbolic periodic orbits on Σ (prereg §5, A7).
Reversing symmetry: H is even in the momenta and W, g^xx, g^yy are even in y (checked to 1e-30). So
G(x, p_x) = (x, -p_x) conjugates P to its inverse, P^{-1} = G P G. The stable manifold of a periodic point z is
therefore G(W^u(G z)), and G z is a periodic point of the same period and type.
Unstable manifolds are grown by iterating P^m (B9 domain at rtol 1e-13) from a fundamental segment
z + s v_u, s in [delta, delta*|lambda_u|] (P^{2m} if lambda_u < 0), with adaptive refinement: a midpoint preimage is
inserted wherever consecutive images are more than DMAX apart in the scaled section metric. Points whose orbit leaves
D are dropped and counted, so every retained manifold point has stayed inside D.
A connection i -> j is a transversal crossing between a segment of W^u(i) (after a iterates) and a segment of
W^s(j) = G W^u(G j) (after b iterates). Recorded: the first such (a, b) by a + b, the crossing point, and the angle.
Usage: python v13_manifolds.py <upo json> <kmax> <delta>"""
import sys, os, json, math
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_upo import SectionMap
from v13_screen import POINTS, RES
DMAX, NSEG0, NMAX_PTS = 0.01, 200, 40000

def grow(S, z, m, lam, v, kmax, delta, xscale, pscale, cap=6000):
    """Incremental growth: each retained point's image at iterate k is P applied once to its image at k-1. Only
    points INSERTED by refinement are traced from the fundamental segment (k applications). Returns the polylines for
    iterates 0..kmax inside D, and the number of dropped points."""
    pow_ = m if lam > 0 else 2*m
    span = abs(lam) if lam > 0 else lam*lam
    ss = list(np.geomspace(delta, delta*span, NSEG0))
    cur = [z + si*v for si in ss]
    curves = [np.array(cur)]; dropped = 0
    def trace(si, k):
        w = z + si*v
        for _ in range(k):
            w2, _, _ = S.P(*w, pow_, b9=True)
            if w2 is None: return None
            w = w2
        return w
    for k in range(1, kmax + 1):
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
        curves.append(np.array([p if p is not None else [np.nan, np.nan] for p in cur]))
    return curves, dropped

def seg_cross(P1, P2):
    """Crossings between polylines P1 and P2 (NaN breaks segments). Returns a list of (point, angle in rad)."""
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
            out.append(((p + t[j]*r).tolist(), ang))
    return out

if __name__ == '__main__':
    f, kmax, delta = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    U = json.load(open(f)); pt = U['point']; M, a_, beta = POINTS[pt]
    E = sp.nsimplify(U['E']); ell = sp.nsimplify(U['ell']); S = SectionMap(M, a_, beta, E, ell*sp.nsimplify(M))
    hyp = [u for u in U['upos'] if u['type'] == 'hyperbolic' and u['whole_orbit_in_D'] and u['area_ok']]
    xs = [p[0] for u in U['upos'] for p in u['points']]; ps = [p[1] for u in U['upos'] for p in u['points']]
    xscale = max(1e-3, max(xs) - min(xs)); pscale = max(1e-3, max(abs(v) for v in ps)*2)
    Wu = {}
    for idx, u in enumerate(hyp):
        z = np.array(u['points'][0]); m = u['period']
        J = S.jac(z, m); ev, V = np.linalg.eig(J); k = int(np.argmax(abs(ev.real)))
        lam, v = float(ev[k].real), V[:, k].real; v = v/np.linalg.norm(v)
        branches = []
        for sgn in (+1, -1):
            curves, dropped = grow(S, z, m, lam, sgn*v, kmax, delta, xscale, pscale)
            branches.append(dict(curves=curves, dropped=dropped))
        Wu[idx] = dict(z=z, m=m, lam=lam, branches=branches)
        print('W^u grown for UPO', idx, 'period', m, 'lambda', round(lam, 3), 'dropped', [b['dropped'] for b in branches], flush=True)
    G = lambda arr: arr*np.array([1.0, -1.0])
    def find_G(idx):
        z = G(Wu[idx]['z'])
        for j, w in Wu.items():
            if w['m'] == Wu[idx]['m'] and np.hypot(*(w['z'] - z)) < 1e-6: return j
            # also match any point of j's orbit
            for p in hyp[j]['points']:
                if np.hypot(*(np.array(p) - z)) < 1e-6: return j
        return None
    edges = []
    for i in Wu:
        for j in Wu:
            gj = find_G(j)
            if gj is None: continue
            best = None
            for bi in Wu[i]['branches']:
                for a, Ca in enumerate(bi['curves']):
                    for bj in Wu[gj]['branches']:
                        for b, Cb in enumerate(bj['curves']):
                            if best is not None and a + b >= best[0]: continue
                            if a + b == 0: continue
                            hits = seg_cross(Ca, G(Cb))
                            if hits:
                                pt_, ang = max(hits, key=lambda h: h[1]); best = (a + b, a, b, pt_, ang)
            if best: edges.append(dict(src=i, dst=j, n_total=best[0], a=best[1], b=best[2], point=best[3], angle=best[4]))
            print('edge', i, '->', j, best[:3] if best else None, round(best[4], 4) if best else '', flush=True)
    out = dict(source=os.path.basename(f), kmax=kmax, delta=delta, DMAX=DMAX, upos=[dict(idx=i, period=w['m'], lam=w['lam'],
               z=w['z'].tolist(), dropped=[b['dropped'] for b in w['branches']]) for i, w in Wu.items()], edges=edges)
    json.dump(out, open(os.path.join(RES, os.path.basename(f).replace('v13_upo_', 'v13_graph_')), 'w'), indent=1)
