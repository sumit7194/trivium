"""V12 G3'''' (addendum 9): D_cross <= 10 max(D_self, 1e-12) on every tolerance-invariant survivor."""
import json, os, sys, numpy as np
from v12_run import systems, outcome, RES
sysl = {s['idx']: s for s in systems()}; out = {}
for idx in [int(a) for a in sys.argv[1:]]:
    f = 'v12_G3p_1_5.json' if idx in (1, 5) else f'v12_G3p_{idx}.json'
    rows = json.load(open(os.path.join(RES, f)))[str(idx)]['rows']; s = sysl[idx]; res = []
    for r in rows:
        if not (r['survivor'] and r['invariant']): continue
        a = np.array(outcome(s, r['x0'], rtol=1e-11, record=20)[1][5]); b = np.array(outcome(s, r['x0'], rtol=1e-12, record=20)[1][5])
        dself = float(np.max(abs(a - b))); dcross = r['dx20']
        res.append(dict(x0=r['x0'], D_cross=dcross, D_self=dself, ratio=dcross/max(dself, 1e-12), ok=dcross <= 10*max(dself, 1e-12)))
    ratios = [x['ratio'] for x in res]
    out[idx] = dict(n=len(res), max_ratio=float(max(ratios or [0])), median_ratio=float(np.median(ratios)) if ratios else None,
                    n_fail=sum(not x['ok'] for x in res), pass_=all(x['ok'] for x in res), rows=res)
    print(idx, s['case'], {k: v for k, v in out[idx].items() if k != 'rows'}, flush=True)
json.dump(out, open(os.path.join(RES, 'v12_G3q_' + '_'.join(sys.argv[1:]) + '.json'), 'w'), indent=1)
