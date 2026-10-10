"""V12 gate G3'' (addenda 6-7) from the G3 rows: Kerr strict; TS disagreements must be realisation-sensitive, first-crossing
agreement to 1e-8, and the realisation-sensitive fraction r reported."""
import json, os, sys, numpy as np
from v12_run import systems, outcome, RES, N_CROSS, RTOL, ATOL_F
from v12_ref import make_ref

TOLS = (1e-11, 1e-12, 1e-13, 1e-14)
sysl = {s['idx']: s for s in systems()}; out = {}
IDX = [int(a) for a in sys.argv[1:]] or [0, 1, 4, 5]
for idx in IDX:
    rows = json.load(open(os.path.join(RES, f'v12_G3_s{idx}.json')))['rows']; s = sysl[idx]
    ref = make_ref(s['case'], s['E'], s['L']); kerr = s['case'].startswith('kerr')
    res = []
    for r in rows:
        outs = [outcome(s, r['x0'], rtol=t)[0] for t in TOLS]; invariant = len(set(outs)) == 1
        o1 = outcome(s, r['x0'], N=1, record=1)[1]; q1 = ref(r['x0'], 0.0, 1, RTOL, RTOL*ATOL_F, record=1)
        dx1 = abs(o1[5][0] - q1['secx'][0]) if (o1[1] >= 1 and len(q1['secx']) >= 1) else None
        res.append(dict(**r, tol_outcomes=outs, invariant=invariant, dx1=dx1))
    n = len(res); dis = [x for x in res if not x['same']]
    inv = [x for x in res if x['invariant']]; dx1s = [x['dx1'] for x in res if x['dx1'] is not None]
    if kerr:
        top = sorted([x for x in res if x['survivor']], key=lambda x: -x['dx20'])[:5]; conv = []
        for x in top:
            dd = {}
            for t in (1e-11, 1e-13):
                a = np.array(outcome(s, x['x0'], rtol=t, record=20)[1][5])
                b = np.array(ref(x['x0'], 0.0, N_CROSS, t, t*ATOL_F, record=20)['secx'])
                dd[t] = float(np.max(abs(a - b)))
            conv.append(dict(x0=x['x0'], dx20_1e11=dd[1e-11], dx20_1e13=dd[1e-13], ratio=dd[1e-13]/dd[1e-11]))
            print('   conv', conv[-1], flush=True)
        ca = np.mean([x['same'] for x in res]) >= 0.99; cb = all(d <= 1e-8 for d in dx1s)
        cc = all(c['ratio'] <= 0.1 for c in conv)
        summ = dict(kind='Kerr', n=n, same_frac=float(np.mean([x['same'] for x in res])), max_dx1=float(max(dx1s or [0])),
                    convergence=conv, a=bool(ca), b=bool(cb), c=bool(cc), pass_=bool(ca and cb and cc))
    else:
        c1 = all(not x['invariant'] for x in dis)
        c2 = (np.mean([x['same'] for x in inv]) >= 0.99) if inv else False
        c3 = all(d <= 1e-8 for d in dx1s)   # G3'' (b)
        summ = dict(kind='TS', n=n, disagreements=len(dis), disagreements_all_sensitive=bool(c1),
                    invariant_n=len(inv), invariant_same_frac=float(np.mean([x['same'] for x in inv])) if inv else None,
                    max_dx1=float(max(dx1s or [0])), r_sensitive=float(1 - len(inv)/n),
                    invariant_survivor_dx20_max=float(max([x['dx20'] for x in inv if x['survivor']] or [0])),
                    pass_=bool(c1 and c2 and c3))
    out[idx] = dict(summary=summ, rows=res); print(idx, s['case'], json.dumps(summ), flush=True)
out['pass'] = all(v['summary']['pass_'] for k, v in out.items() if k != 'pass')
json.dump(out, open(os.path.join(RES, 'v12_G3p_' + '_'.join(map(str, IDX)) + '.json'), 'w'), indent=1); print('G3p', 'PASS' if out['pass'] else 'FAIL')
