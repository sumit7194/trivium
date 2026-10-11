"""V12: fit alpha (binomial MLE, bootstrap CI) per system and apply the pre-registered verdicts.
Usage: python v12_fitall.py [tag]   (tag = primary | outer | E2_px; E1 handled separately)"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, '../results')
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from v12_fit import uncertain_matrix, alpha
import envstamp

COVERAGE = dict(smooth=0.96, fractal=0.93)   # addendum 3, measured on synthetic data

def fit(tag, idx):
    d = np.load(os.path.join(RES, f'v12_{tag}_s{idx}.npz'), allow_pickle=False)
    base, minus, plus, eps = d['base'], d['minus'], d['plus'], d['eps']
    bad = np.isin(base, (3, 4)) | np.isin(minus, (3, 4)).any(1) | np.isin(plus, (3, 4)).any(1)
    U = uncertain_matrix(base, minus, plus, valid=~bad)
    r = alpha(U, eps, nboot=1000, seed=idx)
    r.update(excluded=int(bad.sum()), outcome_counts=np.bincount(base, minlength=5).tolist(),
             H_drift_max=float(d['H_drift_max']), sysd=json.loads(str(d['sysd'])))
    return r

def verdict(ts, kr):
    if 'ci' not in kr or 'ci' not in ts: return 'INCONCLUSIVE (insufficient)'
    k_ok = 0.85 <= kr['alpha_mle'] <= 1.15 and kr['ci'][0] <= 1 <= kr['ci'][1]
    if not k_ok: return 'VOID (Kerr control failed)'
    if ts['ci'][1] < 0.5 and ts['ci'][1] < kr['ci'][0]: return 'CONTRAST REPRODUCED'
    if ts['alpha_mle'] >= 0.85 and ts['ci'][0] <= 1 <= ts['ci'][1]: return 'NOT REPRODUCED'
    return 'INCONCLUSIVE'

if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'primary'
    out = dict(tag=tag, env=envstamp.stamp(os.path.join(HERE, '../../..')), coverage_note=COVERAGE, pairs={})
    present = [i for i in range(6) if os.path.exists(os.path.join(RES, f'v12_{tag}_s{i}.npz'))]
    fits = {i: fit(tag, i) for i in present}
    for i, f in fits.items():
        s = f['sysd']
        print(f"s{i} {s['level']} {s['case']:7s} L={s['L']:+.5f} K={f['K']} excl={f['excluded']} outcomes={f['outcome_counts']} "
              f"hits={f['hits']} alpha={f.get('alpha_mle', float('nan')):.4f} CI={f.get('ci')} wls={f.get('alpha_wls', float('nan')):.4f} "
              f"maxdH={f['H_drift_max']:.1e}", flush=True)
    nrep = nnot = 0
    for lev, (a, b) in (('L1', (0, 1)), ('L2', (2, 3)), ('L3', (4, 5))):
        if a in fits and b in fits:
            v = verdict(fits[a], fits[b]); out['pairs'][lev] = dict(ts=fits[a], kerr=fits[b], verdict=v)
            nrep += v == 'CONTRAST REPRODUCED'; nnot += v == 'NOT REPRODUCED'; print(lev, v)
    if len(out['pairs']) == 3 and tag == 'primary':
        out['overall'] = 'REPRODUCED' if (nrep >= 2 and nnot == 0) else ('NOT REPRODUCED' if nnot else 'INCONCLUSIVE')
        print('OVERALL', out['overall'])
    json.dump(out, open(os.path.join(RES, f'v12_fit_{tag}.json'), 'w'), indent=1, default=float)
