"""V13 Kerr-null analysis (A4, A6): training (even-index) per-arm p99 per level, class-wise max over levels gives
the χ's thresholds; held-out (odd-index) READ orbits give the C1 binomial test (CHAOTIC rate vs 1%, CP95).
CHAOTIC = A1 > thr_A1 AND A2 > thr_A2. Fates of ABSTAIN orbits are tabulated.
Usage: python v13_null_analysis.py <chi_key>"""
import sys, os, json
import numpy as np
from scipy.stats import beta as Beta, binom
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, '../results')
FATE = {0: 'SURVIVE', 1: 'LEFT_D', 2: 'ESCAPE', 3: 'CAPPED', 4: 'FORBIDDEN'}

def cp_upper(k, n, conf=0.95):
    return 1.0 if k == n else float(Beta.ppf(conf, k + 1, n - k))

if __name__ == '__main__':
    key = sys.argv[1]; d = json.load(open(os.path.join(RES, f'v13_kerr_null_{key}.json')))
    per, thrA1, thrA2 = [], -np.inf, -np.inf
    for L in d['levels']:
        if 'orbits' not in L: per.append(dict(kind=L['kind'], note=L.get('note'))); continue
        tr = [o for o in L['orbits'] if o['i'] % 2 == 0 and o['status'] == 'READ']
        fates = {}
        for o in L['orbits']:
            if o['status'] != 'READ':
                f = FATE[o['outcome']] if o['returns'] < 2000 else 'DRIFT>1e-9'; fates[f] = fates.get(f, 0) + 1
        row = dict(kind=L['kind'], E=L['E'], ell=L['ell'], rtol=L['rtol'], n_read=sum(o['status'] == 'READ' for o in L['orbits']),
                   n=len(L['orbits']), abstain_fates=fates)
        if len(tr) >= 5:
            a1 = float(np.percentile([o['A1'] for o in tr], 99)); a2 = float(np.percentile([o['A2'] for o in tr], 99))
            row.update(p99_A1=a1, p99_A2=a2, n_train=len(tr)); thrA1 = max(thrA1, a1); thrA2 = max(thrA2, a2)
        per.append(row)
    held = [o for L in d['levels'] if 'orbits' in L for o in L['orbits'] if o['i'] % 2 == 1 and o['status'] == 'READ']
    k = sum(1 for o in held if o['A1'] > thrA1 and o['A2'] > thrA2); n = len(held)
    out = dict(key=key, thresholds=dict(A1=thrA1, A2=thrA2), levels=per,
               C1=dict(held_out_read=n, chaotic=k, cp95_upper=cp_upper(k, n) if n else None,
                       p_binom=float(binom.sf(k - 1, n, 0.01)) if n else None,
                       PASS=bool(n and binom.sf(k - 1, n, 0.01) >= 0.05),
                       rule='FAIL iff P(X >= k | n, p = 0.01) < 0.05 (one-sided binomial test of rate <= 1%); CP95 reported'))
    json.dump(out, open(os.path.join(RES, f'v13_kerr_null_{key}_analysis.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))
