"""V22 T4f + controls, run separately (the first run's 900-s shell timeout cut it after TS T-a). Same code (v22.py)."""
import sys, json, math, itertools, numpy as np, sympy as sp
from v22 import *
f0ts = sp.factor(-metric('ts45')['g_TT'].subs(Y, 1)); f0k = sp.factor(-metric('kerr45')['g_TT'].subs(Y, 1)); f0zv = ((X - 1)/(X + 1))**2
rows = {'T-a': sp.Rational(8, 15), 'T-d': sp.Rational(8, 3)}
out = {}
for label, f0, rn in [('TS', f0ts, 'T-a'), ('TS', f0ts, 'T-d'), ('Kerr', f0k, 'T-a'), ('ZV', f0zv, 'T-a')]:
    lam = float(rows[rn]); ms = monodromies(f0, math.sqrt(lam), 1.0, 1e-12); ms2 = monodromies(f0, math.sqrt(lam), 1.0, 1e-13)
    pairs = [ms[i][1] @ ms[j][1] for i, j in itertools.combinations(range(len(ms)), 2)]
    comms = [abs(comm_tr(G, H) - 2) for G, H in itertools.combinations(pairs, 2)]
    lox = [abs(np.trace(G)) for G in pairs]
    rec = dict(points=[[c.real, c.imag] for c, _ in ms], single_tr=[[np.trace(M).real, np.trace(M).imag] for _, M in ms],
               rtol_agree=max(abs(np.trace(a[1]) - np.trace(b[1])) for a, b in zip(ms, ms2)),
               pair_abs_tr=lox, comm_minus2_max=max(comms) if comms else None, comm_minus2_min=min(comms) if comms else None,
               n_lox_noncomm=sum(1 for (i, G), (j, H) in itertools.combinations(list(enumerate(pairs)), 2)
                                 if abs(np.trace(G)) > 2 + 1e-6 and abs(np.trace(H)) > 2 + 1e-6 and abs(comm_tr(G, H) - 2) > 1e-3))
    out[f'{label}_{rn}'] = rec; print(label, rn, json.dumps({k: v for k, v in rec.items() if k not in ('points', 'pair_abs_tr')}), flush=True)
    json.dump(out, open('../results/v22_t4.json', 'w'), indent=1)
