"""V22 ZV control only (v22_t4b's nroots failed on ZV's double pole). Singular points from exact sympy roots."""
import json, math, cmath, itertools, numpy as np, sympy as sp
from v22 import make_r, transport, lollipop, comm_tr, X
f0 = ((X - 1)/(X + 1))**2; lam = sp.Rational(8, 15); Ev = sp.sqrt(lam)
n, d = sp.fraction(sp.together(Ev**2 - f0))
pts = [complex(r) for r in sp.roots(sp.Poly(n, X)).keys()] + [complex(r) for r in sp.roots(sp.Poly(d, X)).keys()]
rf = make_r(f0, float(Ev), 1.0); rec = dict(points=[[c.real, c.imag] for c in pts], single=[])
for c in pts:
    dmin = min(abs(c - w) for w in pts if w is not c)
    M = transport(rf, [(lambda t, c=c, r=0.3*dmin: c + r*cmath.exp(1j*t), lambda t, r=0.3*dmin: 1j*r*cmath.exp(1j*t), 0.0, 2*math.pi)], 1e-12)
    rec['single'].append([c.real, c.imag, np.trace(M).real, np.trace(M).imag]); print('ZV single', c, np.trace(M), flush=True)
base = complex(0.37, 60.0); Ms = [transport(rf, lollipop(base, c, 0.3*min(abs(c - w) for w in pts if w is not c)), 1e-12) for c in pts]
pairs = [Ms[i] @ Ms[j] for i, j in itertools.combinations(range(len(Ms)), 2)]
comms = [abs(comm_tr(G, H) - 2) for G, H in itertools.combinations(pairs, 2)]
rec['n_lox_noncomm'] = sum(1 for G, H in itertools.combinations(pairs, 2) if abs(np.trace(G)) > 2 + 1e-6 and abs(np.trace(H)) > 2 + 1e-6 and abs(comm_tr(G, H) - 2) > 1e-3)
rec['comm_minus2_max'] = max(comms) if comms else None
print('ZV n_lox_noncomm', rec['n_lox_noncomm'], 'max|tr[G,H]-2|', rec['comm_minus2_max'], flush=True)
json.dump(rec, open('../results/v22_zv.json', 'w'), indent=1)
