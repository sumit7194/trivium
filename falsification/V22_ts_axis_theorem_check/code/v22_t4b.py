"""V22 T4f + controls, third attempt (2026-11-20). The 11-19 run stalled for 12 h inside one lollipop transport
(90 MB, no output). Changes: progress logged per loop; single-point traces from plain circles (trace is base-free);
products from lollipops whose base is far away (|base| = 60) so the stems don't graze other points; t_eval=[] already."""
import sys, json, math, cmath, itertools, time, numpy as np, sympy as sp
from v22 import metric, make_r, transport, lollipop, singular_points, comm_tr, X, Y
f0ts = sp.factor(-metric('ts45')['g_TT'].subs(Y, 1)); f0k = sp.factor(-metric('kerr45')['g_TT'].subs(Y, 1)); f0zv = ((X - 1)/(X + 1))**2
rows = {'T-a': sp.Rational(8, 15), 'T-d': sp.Rational(8, 3)}
out = {}
def circle(c, rho):
    return [(lambda t: c + rho*cmath.exp(1j*t), lambda t: 1j*rho*cmath.exp(1j*t), 0.0, 2*math.pi)]
for label, f0, rn in [('TS', f0ts, 'T-d'), ('Kerr', f0k, 'T-a'), ('ZV', f0zv, 'T-a')]:
    lam = float(rows[rn]); rf = make_r(f0, math.sqrt(lam), 1.0)
    zs, ps, _, _ = singular_points(f0, math.sqrt(lam), 1.0)
    pts = []
    for z in zs + ps:
        if not any(abs(z - w) < 1e-5 for w in pts): pts.append(z)   # 1e-5: numerical double roots split by ~1e-8 (root cause of the 11-19/20 stalls)
    rec = dict(points=[[c.real, c.imag] for c in pts], single=[])
    for c in pts:
        dmin = min(abs(c - w) for w in pts if w is not c); t0 = time.time()
        M = transport(rf, circle(c, 0.3*dmin), 1e-12); M2 = transport(rf, circle(c, 0.3*dmin), 1e-13)
        rec['single'].append(dict(c=[c.real, c.imag], tr=[np.trace(M).real, np.trace(M).imag], rtol_agree=abs(np.trace(M) - np.trace(M2)), s=round(time.time() - t0, 1)))
        print(label, rn, 'single', c, np.trace(M), round(time.time() - t0, 1), 's', flush=True)
    base = complex(0.37, 60.0); Ms = []
    for c in pts:
        dmin = min(abs(c - w) for w in pts if w is not c); t0 = time.time()
        Ms.append(transport(rf, lollipop(base, c, 0.3*dmin), 1e-12)); print(label, rn, 'lollipop', c, round(time.time() - t0, 1), 's', flush=True)
    pairs = [Ms[i] @ Ms[j] for i, j in itertools.combinations(range(len(Ms)), 2)]
    comms = [abs(comm_tr(G, H) - 2) for G, H in itertools.combinations(pairs, 2)]
    rec['n_lox_noncomm'] = sum(1 for G, H in itertools.combinations(pairs, 2) if abs(np.trace(G)) > 2 + 1e-6 and abs(np.trace(H)) > 2 + 1e-6 and abs(comm_tr(G, H) - 2) > 1e-3)
    rec['comm_minus2_max'] = max(comms); rec['comm_minus2_min'] = min(comms)
    out[f'{label}_{rn}'] = rec; print(label, rn, 'n_lox_noncomm', rec['n_lox_noncomm'], 'max|tr[G,H]-2| %.3e' % rec['comm_minus2_max'], flush=True)
    json.dump(out, open('../results/v22_t4b.json', 'w'), indent=1)
