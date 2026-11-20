"""V24 C1 diagnostic (post-result, not a registered test): exact U(x) at the classification points of the 5 flagged
arc points, by root-finding on the seed parameter (no interpolation), and the exact margin at their first D-hit."""
import sys, os, json, math, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V20_ts_capture_edge_tangle/code')); import v20
FJ, fW, fH = v20.field('ts45', 0.97, 41/8); RT = 1e-12
z, Dm, T, clos = v20.polish(FJ, fH, 9.8045591682, RT)
ev, Vv = np.linalg.eig(Dm); k = int(np.argmax(np.abs(ev))); lam = float(np.real(ev[k])); eu = np.real(Vv[:, k]); eu /= np.linalg.norm(eu)
xs = z[0]; sgn = 1.0 if v20.P(FJ, fH, z + 1e-6*lam**2*eu, RT)[0][0] > xs else -1.0
s0 = 1e-6; S = np.geomspace(s0, s0*lam, 400, endpoint=False)
def it(s, n):
    q = z + sgn*s*eu
    for _ in range(n):
        q = v20.P(FJ, fH, q, RT)[0]
        if q is None: return None
    return q
# U points with provenance (seed s, iterate n), pre-crossing only
meta = []
for s in S:
    q = z + sgn*s*eu; n = 0; meta.append((q[0], q[1], s, 0))
    while n < 12:
        q2 = v20.P(FJ, fH, q, RT)[0]
        if q2 is None or q2[1] <= 0: break
        n += 1; q = q2; meta.append((q[0], q[1], s, n))
meta.sort()
def U_exact(x):
    """find a W^u_out point with abscissa x: bracket in (s, n) between consecutive U points with the same n."""
    xsrt = [m[0] for m in meta]; j = int(np.searchsorted(xsrt, x))
    for a, b in ((meta[j-1], meta[j]),):
        cands = []
        for n in {a[3], b[3]}:
            # seeds whose n-th iterate brackets x: scan the seed grid for a sign change of x_n(s) - x
            vals = [(s, it(s, n)) for s in S]
            for (sa, qa), (sb, qb) in zip(vals, vals[1:]):
                if qa is None or qb is None or qa[1] <= 0 or qb[1] <= 0: continue
                if (qa[0] - x)*(qb[0] - x) <= 0 and abs(sb - sa) < 0.1*s0*lam:
                    r = brentq(lambda ss: it(ss, n)[0] - x, sa, sb, xtol=1e-17, rtol=1e-15)
                    cands.append((n, r, float(it(r, n)[1])))
        return cands
rows = json.load(open(os.path.join(HERE, '../results/v24_lobes_C1diag.json')))['rows']
bad = [r for r in rows if r['on_arc'] and r['inD_hits']]
interp = lambda x: np.interp(x, [m[0] for m in meta], [m[1] for m in meta])
out = []
for b in bad:
    c0 = U_exact(b['x']); h1 = b['inD_hits'][0]; c1 = U_exact(h1[1])
    rec = dict(seed=b['i'], x=b['x'], px=b['px'], gap_interp=b['gap'],
               U_interp=float(interp(b['x'])), U_exact_candidates=c0,
               gap_exact=[abs(b['px']) - c[2] for c in c0],
               firsthit_x=h1[1], firsthit_px=h1[2], firsthit_margin_interp=h1[3],
               firsthit_margin_exact=[c[2] - abs(h1[2]) for c in c1])
    out.append(rec); print(rec, flush=True)
json.dump(out, open(os.path.join(HERE, '../results/v24_lobes_C1diag2.json'), 'w'), indent=1, default=str)
