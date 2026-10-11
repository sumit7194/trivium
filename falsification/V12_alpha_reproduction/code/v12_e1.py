"""V12 E1 analysis (addendum 12): realisation sensitivity r(N), noise exclusion f < 3r, local slopes, crossover eps_c(N),
readings; alpha (MLE) over retained eps. Needs v12_E1_N300_s{0,1}.npz and v12_E1_N600_s{0,1}.npz."""
import os, sys, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, '../results')
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from v12_fit import uncertain_matrix, alpha
from v12_run import systems, outcome
import envstamp

def realisation_r(sysd, x0, N):
    a = np.array([outcome(sysd, x, N=N, rtol=1e-11)[0] for x in x0]); b = np.array([outcome(sysd, x, N=N, rtol=1e-13)[0] for x in x0])
    return float(np.mean(a != b)), int(np.sum(a != b))

def analyse(tag, idx, N):
    d = np.load(os.path.join(RES, f'v12_{tag}_s{idx}.npz')); s = json.loads(str(d['sysd']))
    base, minus, plus, eps, x0 = d['base'], d['minus'], d['plus'], d['eps'], d['x0']
    bad = np.isin(base, (3, 4)) | np.isin(minus, (3, 4)).any(1) | np.isin(plus, (3, 4)).any(1)
    U = uncertain_matrix(base, minus, plus, valid=~bad); n = U.shape[0]; k = U.sum(0); f = k/n
    r, nr = realisation_r(s, x0[~bad], N)
    keep = f >= 3*r
    slopes = []
    idxs = [i for i in range(len(eps)) if keep[i]]
    for a_, b_ in zip(idxs[:-1], idxs[1:]):
        if k[a_] >= 10 and k[b_] >= 10:
            slopes.append(dict(eps_hi=float(eps[a_]), eps_lo=float(eps[b_]), s=float(math.log(f[a_]/f[b_])/math.log(eps[a_]/eps[b_]))))
    cross = next((sl['eps_hi'] for sl in slopes if sl['s'] > 0.5), None)
    fitU = U[:, keep]; fe = eps[keep]
    al = alpha(fitU, fe, nboot=1000, seed=100 + idx) if keep.sum() >= 3 else dict(verdict='INSUFFICIENT')
    return dict(system=s, N=N, K=int(n), excluded=int(bad.sum()), hits=k.tolist(), f=f.tolist(), eps=eps.tolist(),
                r=r, r_count=nr, retained=keep.tolist(), slopes=slopes, eps_c=cross, alpha=al)

if __name__ == '__main__':
    out = dict(env=envstamp.stamp(os.path.join(HERE, '../../..')), runs={})
    for N, tag in ((300, 'E1_N300'), (600, 'E1_N600')):
        for idx in (0, 1):
            r = analyse(tag, idx, N); out['runs'][f'{tag}_s{idx}'] = r
            print(f"{tag} s{idx} {r['system']['case']}: r={r['r']:.3f} ({r['r_count']}) hits={r['hits']} retained={sum(r['retained'])}/8 "
                  f"eps_c={r['eps_c']} alpha={r['alpha'].get('alpha_mle')} CI={r['alpha'].get('ci')}", flush=True)
            for sl in r['slopes']: print(f"     s[{sl['eps_hi']:.0e}->{sl['eps_lo']:.0e}] = {sl['s']:.3f}")
    ts300, ts600 = out['runs']['E1_N300_s0']['eps_c'], out['runs']['E1_N600_s0']['eps_c']
    if ts300 is not None and ts600 is not None:
        reading = 'SUPPORTS GENUINE FRACTAL' if ts600 < ts300 else ('FINITE-TIME ARTEFACT SUSPECTED' if ts600 == ts300 else 'UNEXPECTED')
    elif ts300 is None and ts600 is None:
        reading = 'FLAT TO EPS_MIN (no crossover at either N)'
    else:
        reading = 'UNEXPECTED (' + ('crossover at 300 only' if ts600 is None else 'crossover at 600 only') + ')'
    out['TS_reading'] = reading; print('TS reading:', reading)
    json.dump(out, open(os.path.join(RES, 'v12_E1_analysis.json'), 'w'), indent=1, default=float)
