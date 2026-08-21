"""T1 — gain stability of a conserved-quantity readout along the alpha axis.

Gates frozen in ../PREREGISTRATION.md before this file was written.
Independent implementation from tabula's written spec; their code was not read.

H = 1/2(px^2+py^2) + 1/4(x^4+y^4) + (alpha/2) x^2 y^2
"""
import json, numpy as np, scipy.linalg as sla
from pathlib import Path

E0, DT, NSTEP, BURN, NTRAJ = 8.0, 0.02, 2500, 150, 70
ALPHAS = [0, 1, 2, 3, 4]
EPS = [0.0, 1e-4, 1e-3, 1e-2, 1e-1]
OUT = Path(__file__).resolve().parent.parent / "results"; OUT.mkdir(exist_ok=True)

def H(x, y, px, py, a):
    return 0.5*(px**2+py**2) + 0.25*(x**4+y**4) + 0.5*a*x**2*y**2

def force(x, y, a):
    return -(x**3 + a*x*y**2), -(y**3 + a*y*x**2)

def traj(x0, y0, px0, py0, a, n=NSTEP):
    """Velocity-Verlet; separable quartic potential."""
    X = np.empty((n, 4))
    x, y, px, py = x0, y0, px0, py0
    ax, ay = force(x, y, a)
    for i in range(n):
        px += 0.5*DT*ax; py += 0.5*DT*ay
        x += DT*px;      y += DT*py
        ax, ay = force(x, y, a)
        px += 0.5*DT*ax; py += 0.5*DT*ay
        X[i] = (x, y, px, py)
    return X

def sample_ic(a, rng, e0=E0):
    """Bounded IC on the shell H = e0."""
    for _ in range(4000):
        x, y = rng.uniform(-2.2, 2.2, 2)
        v = e0 - (0.25*(x**4+y**4) + 0.5*a*x**2*y**2)
        if v <= 1e-6: continue
        th = rng.uniform(0, 2*np.pi); p = np.sqrt(2*v)
        return x, y, p*np.cos(th), p*np.sin(th)
    return None

def features(X):
    """Polynomial basis, degree 2 in momenta -- the natural space for a quadratic invariant."""
    x, y, px, py = X.T
    return np.column_stack([px*px, py*py, px*py, x*px, y*py, x*py, y*px,
                            x*x, y*y, x*y, x**4, y**4, x*x*y*y, x*x*y, x*y*y])

def readout(F, tid, ntr, rng):
    """Conserved directions: min w'Cw_within / w'Cw_total, scored OUT-OF-SAMPLE on held-out
    trajectories. Split is over TRAJECTORIES, never over time within a trajectory."""
    ids = np.unique(tid); rng.shuffle(ids)
    tr, te = ids[:ntr], ids[ntr:]
    def cov_within(mask_ids):
        acc = np.zeros((F.shape[1], F.shape[1])); n = 0
        for t in mask_ids:
            S = F[tid == t]; S = S - S.mean(0)
            acc += S.T @ S; n += len(S)
        return acc/n
    def cov_total(mask_ids):
        S = F[np.isin(tid, mask_ids)]; S = S - S.mean(0)
        return (S.T @ S)/len(S)
    Cw, Ct = cov_within(tr), cov_total(tr)
    Ct = Ct + 1e-12*np.trace(Ct)/Ct.shape[0]*np.eye(Ct.shape[0])   # ridge for conditioning
    w, V = sla.eigh(Cw, Ct)
    Cw_te, Ct_te = cov_within(te), cov_total(te)
    ratios = np.array([ (v@Cw_te@v)/max(v@Ct_te@v, 1e-300) for v in V.T ])
    return V, ratios

def run():
    rng = np.random.default_rng(20260821)
    rep = {}
    for a in ALPHAS:
        Xs, tid, dH = [], [], []
        t = 0
        while len(Xs) < NTRAJ:
            ic = sample_ic(a, rng)
            if ic is None: continue
            X = traj(*ic, a)
            if not np.all(np.isfinite(X)) or np.abs(X).max() > 50: continue
            h = H(X[:,0], X[:,1], X[:,2], X[:,3], a)
            dH.append(float(np.ptp(h)/abs(np.mean(h))))
            Xs.append(X[BURN:]); tid.append(np.full(len(X)-BURN, t)); t += 1
        Xall = np.vstack(Xs); tidall = np.concatenate(tid)
        Fbase = features(Xall)
        Fbase = Fbase/Fbase.std(0)
        rep[str(a)] = {"dH_med": float(np.median(dH)), "dH_max": float(np.max(dH)), "eps": {}}
        for e in EPS:
            c = rng.standard_normal(NTRAJ)[tidall]                 # per-traj constant: EXACTLY conserved
            eta = rng.standard_normal(len(tidall))                 # within-traj noise
            P = c + e*eta
            true_ratio = e*e/(1.0+e*e) if e > 0 else 0.0
            F = np.column_stack([Fbase, P/P.std()])
            V, r = readout(F, tidall, 50, rng)
            k = int(np.argmin(r))
            ov = abs(V[-1, k])/np.linalg.norm(V[:, k])              # overlap of best dir on the plant
            # best direction that is actually ABOUT the plant
            ovs = np.abs(V[-1, :])/np.linalg.norm(V, axis=0)
            cand = np.where(ovs >= 0.9)[0]
            rp = float(r[cand].min()) if len(cand) else float('nan')
            rank = int(np.sum(r < (rp if np.isfinite(rp) else np.inf)))
            rep[str(a)]["eps"][str(e)] = {
                "true_ratio": true_ratio, "recovered_plant_ratio": rp,
                "best_overlap": float(ov), "max_overlap": float(ovs.max()),
                "plant_rank": rank, "best_ratio_any": float(r[k]),
                "gain": float(true_ratio/rp) if (np.isfinite(rp) and rp > 0 and true_ratio > 0) else None}
        print(f"alpha={a}: dH_med={rep[str(a)]['dH_med']:.2e} "
              f"best_any(eps=0)={rep[str(a)]['eps']['0.0']['best_ratio_any']:.2e}", flush=True)
    (OUT/"t1_gain.json").write_text(json.dumps(rep, indent=1))
    return rep

if __name__ == "__main__":
    run(); print("done")
