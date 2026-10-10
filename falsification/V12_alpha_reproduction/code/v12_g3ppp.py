"""V12 G3''' (addendum 8): 4-tolerance numba-vs-scipy convergence on the 10 Kerr orbits of G3''(c)."""
import json, os, numpy as np
from v12_run import systems, outcome, RES, N_CROSS, ATOL_F
from v12_ref import make_ref
d = json.load(open(os.path.join(RES, 'v12_G3p_1_5.json'))); sysl = {s['idx']: s for s in systems()}; out = []
for idx in (1, 5):
    s = sysl[idx]; ref = make_ref(s['case'], s['E'], s['L'])
    for c in d[str(idx)]['summary']['convergence']:
        seq = []
        for t in (1e-11, 1e-12, 1e-13, 3e-14):
            a = np.array(outcome(s, c['x0'], rtol=t, record=20)[1][5]); b = np.array(ref(c['x0'], 0.0, N_CROSS, t, t*ATOL_F, record=20)['secx'])
            seq.append(float(np.max(abs(a - b))))
        dec = all(seq[i + 1] < seq[i] for i in range(3)); below = any(all(v < 1e-6 for v in seq[i:]) for i in range(4))
        out.append(dict(idx=idx, x0=c['x0'], seq=seq, strictly_decreasing=dec, below_1e6_and_stays=below, ok=bool(dec or below)))
        print(json.dumps(out[-1]), flush=True)
res = dict(rows=out, pass_=all(r['ok'] for r in out)); json.dump(res, open(os.path.join(RES, 'v12_G3ppp.json'), 'w'), indent=1)
print('G3ppp', 'PASS' if res['pass_'] else 'FAIL')
