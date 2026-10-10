"""V12 estimator: uncertainty fraction f(eps) from the nested design, alpha by binomial maximum likelihood
(log f = c + alpha log eps), 95% CI by bootstrap over x0; secondary weighted least squares as in ansatz's spec.
Gate G4: synthetic outcome functions (smooth, middle-thirds Cantor, i.i.d. random)."""
import math, numpy as np
from scipy.optimize import minimize

def uncertain_matrix(base, minus, plus, valid=None):
    """base: (K,), minus/plus: (K, nE) outcome codes. Returns boolean (K', nE) over valid rows."""
    U = (minus != base[:, None]) | (plus != base[:, None])
    return U if valid is None else U[valid]

def mle(k, n, eps):
    """Binomial MLE of p_i = min(exp(c) eps_i^alpha, 1 - 1e-12). k hits out of n at each eps."""
    le = np.log(eps); k = np.asarray(k, float)
    def nll(th):
        lp = np.minimum(th[0] + th[1]*le, math.log(1 - 1e-12))
        p = np.exp(lp)
        return -np.sum(k*lp + (n - k)*np.log1p(-p))
    a0, c0 = np.polyfit(le, np.log(np.maximum(k, 0.5)/n), 1)
    r = minimize(nll, [c0, a0], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 20000})
    return r.x[1]

def wls(k, n, eps):
    le = np.log(eps); lf = np.log(np.asarray(k, float)/n); w = np.asarray(k, float)
    W = np.sum(w); mx = np.sum(w*le)/W; my = np.sum(w*lf)/W
    return np.sum(w*(le - mx)*(lf - my))/np.sum(w*(le - mx)**2)

def alpha(U, eps, nboot=1000, seed=0, min_hits=10, min_eps=3):
    eps = np.asarray(eps, float); n = U.shape[0]; k = U.sum(0)
    use = k >= min_hits
    out = dict(K=int(n), hits=k.tolist(), f=(k/n).tolist(), eps=eps.tolist(), used=use.tolist())
    if use.sum() < min_eps:
        out['verdict'] = 'INSUFFICIENT'; return out
    a = mle(k[use], n, eps[use]); out['alpha_mle'] = float(a); out['alpha_wls'] = float(wls(k[use], n, eps[use]))
    rng = np.random.default_rng(seed); bs = []
    for _ in range(nboot):
        kb = U[rng.integers(0, n, n)].sum(0)[use]
        if np.all(kb > 0): bs.append(mle(kb, n, eps[use]))
    out['ci'] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]; out['nboot_ok'] = len(bs)
    return out

# ---------------- G4 synthetic outcome functions on a window of width w ----------------
def smooth_outcome(x, w): return (x > 0.5*w).astype(int)

def cantor_outcome(x, w, depth=40):
    """Parity of the depth at which x/w first falls into a removed middle third; boundary = middle-thirds Cantor set."""
    u = np.asarray(x, float)/w; out = np.zeros(u.shape, int); alive = (u >= 0) & (u <= 1)
    for d in range(1, depth + 1):
        t = u*3.0; digit = np.floor(t); mid = alive & (digit == 1)
        out[mid] = d % 2; alive &= ~mid; u = t - digit
    return out

def random_outcome(x, w):
    b = np.frombuffer(np.asarray(x, float).tobytes(), dtype=np.uint64)
    h = (b * np.uint64(0x9E3779B97F4A7C15)) ^ (b >> np.uint64(29))
    h = h * np.uint64(0xBF58476D1CE4E5B9)
    return ((h >> np.uint64(33)) & np.uint64(1)).astype(int)

def gate_G4(K=2000, w=0.03, eps=(3e-3, 1e-3, 3e-4, 1e-4, 3e-5), seed=4):
    rng = np.random.default_rng(seed); x = rng.uniform(0, w, K); eps = np.array(eps)
    res = {}
    for name, fn in (('smooth', smooth_outcome), ('cantor', cantor_outcome), ('random', random_outcome)):
        base = fn(x, w); minus = np.stack([fn(x - e, w) for e in eps], 1); plus = np.stack([fn(x + e, w) for e in eps], 1)
        res[name] = alpha(uncertain_matrix(base, minus, plus), eps, nboot=300)
    a = {k: v.get('alpha_mle') for k, v in res.items()}
    res['pass'] = dict(smooth=a['smooth'] is not None and 0.95 <= a['smooth'] <= 1.05,
                       cantor=a['cantor'] is not None and abs(a['cantor'] - (1 - math.log(2)/math.log(3))) <= 0.05,
                       random=a['random'] is not None and -0.05 <= a['random'] <= 0.05)
    return res

if __name__ == '__main__':
    import json, os
    r = gate_G4(); print(json.dumps(r, indent=1))
    json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/v12_G4.json'), 'w'), indent=1)

# ---------------- G4' (addendum 2): calibrated against the exact in-range target, over 20 seeds ----------------
def population_alpha(fn, w, eps, K=2000, ngrid=2_000_000):
    x = np.linspace(0, w, ngrid + 1)[:-1]; b = fn(x, w)
    f = np.array([np.mean((fn(x - e, w) != b) | (fn(x + e, w) != b)) for e in eps])
    use = f*K >= 10
    return float(mle(f[use]*K, K, np.asarray(eps)[use])), f.tolist()

def gate_G4p(K=2000, w=0.03, eps=(3e-3, 1e-3, 3e-4, 1e-4, 3e-5), seeds=range(400, 420)):
    eps = np.array(eps); res = {}
    for name, fn in (('smooth', smooth_outcome), ('cantor', cantor_outcome), ('random', random_outcome)):
        apop, fpop = population_alpha(fn, w, eps, K) if name != 'random' else (0.0, None)
        a, cover = [], 0
        for s in seeds:
            x = np.random.default_rng(s).uniform(0, w, K)
            U = uncertain_matrix(fn(x, w), np.stack([fn(x - e, w) for e in eps], 1), np.stack([fn(x + e, w) for e in eps], 1))
            r = alpha(U, eps, nboot=300, seed=s)
            if 'alpha_mle' in r:
                a.append(r['alpha_mle']); cover += int(r['ci'][0] <= apop <= r['ci'][1])
        m = float(np.mean(a))
        ok = (abs(m) <= 0.03) if name == 'random' else (abs(m - apop) <= 0.03 and cover >= 17)
        res[name] = dict(alpha_pop=apop, f_pop=fpop, mean=m, sd=float(np.std(a)), n=len(a), coverage=cover, pass_=bool(ok))
    res['pass'] = all(v['pass_'] for v in res.values() if isinstance(v, dict))
    return res
