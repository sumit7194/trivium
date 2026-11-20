"""V24 addendum E: symmetry of the W^u-S crossings (float). Bridge code; reuses the C1' exact-U machinery."""
import os, json, math, numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); __file__ = os.path.join(HERE, 'v24_lobes_C1p.py')
exec(open(os.path.join(HERE, 'v24_lobes_C1p.py')).read().split('# 1. floor')[0])
rows = json.load(open(os.path.join(HERE, '../results/v24_lobes_C1p.json')))['rows']
Rf = lambda z: np.array([z[0], -z[1]])
Pm = lambda z: v20.P(FJ, fH, z, RT)[0]
Pinv = lambda z: Rf(Pm(Rf(z)))
def orbit_test(c):
    pts = {0: c}; q = c
    for k in range(1, 4): q = Pm(q); pts[k] = q
    q = c
    for k in range(1, 4): q = Pinv(q); pts[-k] = q
    dR = {k: float(abs(p[1])) for k, p in pts.items() if p is not None}
    dPR = {}
    for k, p in pts.items():
        if p is None: continue
        w = Pm(Rf(p)); dPR[k] = float(np.linalg.norm(w - p)) if w is not None else None
    return pts, dR, dPR
out = {}
# control: h, where the first crossing iterate n changes along the seeds
ns = {r['i']: r['n'] for r in rows}
hc = [i for i in range(1, 400) if i in ns and i - 1 in ns and ns[i] != ns[i - 1]]
print('n changes at seeds', hc, flush=True)
recs = []
for i in hc[:1]:
    n = ns[i - 1]                      # seed i-1 crosses at iterate n; seed i crosses later -> h between, at iterate n... use p_x of iterate n
    f = lambda sp_: it(sp_, n)[1]
    a, b = S[i - 1], S[i]
    if f(a)*f(b) < 0:
        s_h = brentq(f, a, b, xtol=1e-20, rtol=1e-15); hpt = it(s_h, n)
    else:
        n2 = n - 1; f2 = lambda sp_: it(sp_, n2)[1]; s_h = brentq(f2, a, b, xtol=1e-20, rtol=1e-15); hpt = it(s_h, n2)
    _, dR, dPR = orbit_test(hpt)
    rec = dict(kind='CONTROL h', point=hpt.tolist(), min_dR=min(dR.values()), min_dPR=min(v for v in dPR.values() if v is not None), dR=dR, dPR=dPR)
    recs.append(rec); print('h control:', hpt, 'min dR %.2e  min dPR %.2e' % (rec['min_dR'], rec['min_dPR']), flush=True)
# the 4 crossings
cls = {r['i']: r['outside'] for r in rows}
chg = [i for i in range(400) if i in cls and (i - 1) % 400 in cls and cls[i] != cls[(i - 1) % 400]]
print('class changes at seeds', chg, flush=True)
for i in chg:
    j = (i - 1) % 400; n_i, n_j = ns[i], ns[j]
    if i == 0 or n_i != n_j:
        print('  seed pair', j, i, 'spans an n change; skipped', flush=True); continue
    n = n_i
    def gap(sp_):
        q = it(sp_, n); return abs(q[1]) - Ue(q[0])
    s_c = brentq(gap, S[j], S[i], xtol=1e-20, rtol=1e-14); c = it(s_c, n)
    _, dR, dPR = orbit_test(c)
    mR = min(dR.values()); mPR = min(v for v in dPR.values() if v is not None)
    verdict = 'SYMMETRIC' if min(mR, mPR) <= 1e-8 else ('NON-SYMMETRIC' if min(mR, mPR) >= 1e-4 else 'UNRESOLVED')
    rec = dict(kind='crossing', seed_pair=(j, i), log_s=float(math.log(s_c)), point=c.tolist(), min_dR=mR, argmin_dR=min(dR, key=dR.get),
               min_dPR=mPR, argmin_dPR=min((k for k in dPR if dPR[k] is not None), key=lambda k: dPR[k]), verdict=verdict, dR=dR, dPR=dPR)
    recs.append(rec); print('crossing seeds %d/%d: c = %s  min dR %.2e (k=%s)  min dPR %.2e (k=%s)  -> %s' %
                            (j, i, c, mR, rec['argmin_dR'], mPR, rec['argmin_dPR'], verdict), flush=True)
cr = [r for r in recs if r['kind'] == 'crossing']
if len(cr) >= 2:
    ls = sorted(r['log_s'] for r in cr); per = math.log(lam)
    print('log-s spacing / log(lambda):', [round((ls[k + 1] - ls[k])/per, 6) for k in range(len(ls) - 1)], flush=True)
    out['spacing_over_period'] = [(ls[k + 1] - ls[k])/per for k in range(len(ls) - 1)]
out['records'] = recs
json.dump(out, open(os.path.join(HERE, '../results/v24_symE.json'), 'w'), indent=1, default=str)
