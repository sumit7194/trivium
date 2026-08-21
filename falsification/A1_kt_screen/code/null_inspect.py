"""ansatz's one-line check: is H actually among the 5 at delta=1 degree 2,
or am I inferring it from the aggregate count? H = -1/2 identically on every
orbit -- constant ALONG and ACROSS -- which is the one signature a within/total
readout cannot distinguish on its own."""
import sys, numpy as np, itertools
sys.path.insert(0,'.')
from kt_screen import integrate, basis, count_conserved
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _zv_invariant import metric
from poincare import H_value

f = metric(1.0); rng = np.random.default_rng(11)
Xs, ELs, tid = [], [], []; t=0; tries=0
while len(Xs) < 40 and tries < 4000:
    tries += 1
    E = rng.uniform(0.90,0.97); L = rng.uniform(2.6,3.6); x0 = rng.uniform(8.0,16.0)
    X = integrate(f, x0, E, L)
    if X is None: continue
    Xs.append(X); ELs.append((E,L)); tid.append(np.full(len(X), t)); t+=1
cols = np.vstack([basis(X, el, 2, 0, f) for X, el in zip(Xs, ELs)])
tid = np.concatenate(tid)
step = max(1, len(cols)//(12*cols.shape[1])); cols, tid = cols[::step], tid[::step]

C = cols/np.maximum(np.abs(cols).max(0),1e-300)
U,sv,Vt = np.linalg.svd(C, full_matrices=False)
keep = sv/sv.max() >= 1e-8; P = Vt[keep].T
B = C@P
Z = np.empty_like(B)
for k in np.unique(tid):
    m = tid==k; Z[m] = B[m]-B[m].mean(0)
Z = Z/np.maximum(np.abs(B).max(0),1e-300)
_,s2,V2 = np.linalg.svd(Z, full_matrices=False)
s2n = s2/s2.max(); nz = np.where(s2n < 1e-8)[0]
print(f"conserved directions found: {len(nz)}")

# true H on the same rows
Hs = []
for X, el in zip(Xs, ELs):
    Hs.append(np.array([H_value(f,[a,b,c,d],el[0],el[1]) for a,b,c,d in X]))
H = np.concatenate(Hs)[::step]
print(f"H range over ensemble: [{H.min():.6f}, {H.max():.6f}]  (constant across => -0.5)")

print("\noverlap of each conserved direction with the TRUE H, and with E/L constants:")
Efull = np.concatenate([np.full(len(X), el[0]) for X,el in zip(Xs,ELs)])[::step]
Lfull = np.concatenate([np.full(len(X), el[1]) for X,el in zip(Xs,ELs)])[::step]
targets = {"H": H, "E^2": Efull**2, "E*L": Efull*Lfull, "L^2": Lfull**2}
for i,k in enumerate(nz):
    proj = B @ V2[k]
    row = []
    for name, tgt in targets.items():
        t_ = tgt - tgt.mean(); p_ = proj - proj.mean()
        c = abs(np.dot(t_,p_)/ (np.linalg.norm(t_)*np.linalg.norm(p_)+1e-300))
        row.append(f"{name}={c:.4f}")
    print(f"  dir {i+1}: " + "  ".join(row))
print("\nspan check: is TRUE H inside the span of the 5 conserved directions?")
M = np.column_stack([B@V2[k] for k in nz])
coef,res,rank,_ = np.linalg.lstsq(np.column_stack([M,np.ones(len(M))]), H, rcond=None)
fit = np.column_stack([M,np.ones(len(M))])@coef
print(f"  residual |H - fit|/|H| = {np.linalg.norm(H-fit)/np.linalg.norm(H):.3e}")
