"""ansatz's one-shot test, plus the prior question they said to answer first.

PRIOR QUESTION: is my 4.5% residual in COEFFICIENT space or FUNCTION space?
Reading my own code: fit = M @ coef where M's columns are B@V2[k], i.e. FUNCTION
VALUES on the sample, and the residual is |H_values - fit_values|/|H_values|.
So it is FUNCTION SPACE. ansatz guessed coefficient space, which would have made
it gauge freedom in a degenerate basis and a non-issue. It is not that.

THEIR TEST: H's coefficient vector v is known in CLOSED FORM --
    H = 1/2( g11 px^2 + g22 py^2 + tt E^2 - 2 tp E L + pp L^2 )
so build v exactly, and compute ||P_discarded v|| / ||v||. If ~4.5%, the projection
is the culprit. If ~0, it is eliminated.
"""
import sys, itertools, numpy as np
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts"); sys.path.insert(0, ".")
from _zv_invariant import metric
from poincare import H_value
from shell_vary import integrate_c

f = metric(1.0); rng = np.random.default_rng(11)
Xs, ELs, tid, Hs = [], [], [], []; t = 0; tries = 0
while len(Xs) < 40 and tries < 6000:
    tries += 1
    E = rng.uniform(0.90, 0.97); L = rng.uniform(2.6, 3.6); x0 = rng.uniform(8.0, 16.0)
    c = rng.uniform(-0.62, -0.40)
    r = integrate_c(f, x0, E, L, c)
    if r is None: continue
    X, H0 = r; Xs.append(X); ELs.append((E, L)); Hs.append(H0)
    tid.append(np.full(len(X), t)); t += 1

MOM = [e for e in itertools.product(range(3), repeat=4) if sum(e) == 2]   # 10, ordered
NCO = 8                                                                   # coeff fns
def cols_for(X, EL):
    from kt_screen import basis
    return basis(X, EL, 2, 0, f)
cols = np.vstack([cols_for(X, el) for X, el in zip(Xs, ELs)]); tid = np.concatenate(tid)
step = max(1, len(cols)//(12*cols.shape[1])); cols, tid = cols[::step], tid[::step]
Hfull = np.concatenate([np.full(len(X), h) for X, h in zip(Xs, Hs)])[::step]

scale = np.maximum(np.abs(cols).max(0), 1e-300)
C = cols/scale

# H's EXACT coefficient vector in the RAW basis, then rescaled into C's basis
v = np.zeros(cols.shape[1])
idx = lambda mom, co: MOM.index(mom)*NCO + co        # column ordering: product(mom, coo)
v[idx((0,0,2,0), 3)] =  0.5      # px^2 * g11
v[idx((0,0,0,2), 4)] =  0.5      # py^2 * g22
v[idx((2,0,0,0), 5)] =  0.5      # E^2  * tt
v[idx((1,1,0,0), 7)] = -1.0      # E L  * tp   (from -2*tp/2)
v[idx((0,2,0,0), 6)] =  0.5      # L^2  * pp
print(f"H reconstructed from exact v: max|C@(v*scale) - H| = "
      f"{np.abs(cols@v - Hfull).max():.3e}   <- confirms v is right")
v_s = v*scale                                        # same function, C's coordinates
v_s = v_s/np.linalg.norm(v_s)

U, sv, Vt = np.linalg.svd(C, full_matrices=False)
for tol in [1e-6, 1e-8, 1e-10]:
    keep = sv/sv.max() >= tol
    Pk = Vt[keep]; Pd = Vt[~keep]
    frac = np.linalg.norm(Pd @ v_s)/np.linalg.norm(v_s)
    print(f"  tol={tol:.0e}  kept={int(keep.sum())}/{len(sv)}  "
          f"||P_discarded v|| / ||v|| = {frac:.4e}")
print("\n  ~4.5% => projection is the culprit.   ~0 => eliminated.")

# Projection eliminated. So is H's direction actually AMONG the 5 null directions?
keep = sv/sv.max() >= 1e-8; P = Vt[keep].T; B = C@P
Z = np.empty_like(B)
for k in np.unique(tid):
    m = tid == k; Z[m] = B[m]-B[m].mean(0)
Zs = Z/np.maximum(np.abs(B).max(0), 1e-300)
_, s2, V2 = np.linalg.svd(Zs, full_matrices=False); s2n = s2/s2.max()
nz = np.where(s2n < 1e-8)[0]
vp = P.T @ v_s; vp = vp/np.linalg.norm(vp)          # H's direction in projected coords
S = V2[nz]                                          # the 5 found null directions
ov = np.linalg.norm(S @ vp)                          # overlap of v_H with their span
print(f"\nnull directions found: {len(nz)}")
print(f"  overlap of H's EXACT direction with their span = {ov:.6f}   (1.0 = fully inside)")
print(f"  singular values at the cut: ...{s2n[nz[0]-2]:.2e} {s2n[nz[0]-1]:.2e} | "
      f"{'  '.join(f'{s2n[k]:.2e}' for k in nz)}")
# and how conserved is H's own direction, directly?
proj = B @ vp
wv = np.mean([np.var(proj[tid==k]) for k in np.unique(tid)])
print(f"  within-traj variance of H's own direction / total variance = "
      f"{wv/np.var(proj):.3e}   (0 = perfectly conserved)")

# ansatz's three-way discriminator. Zs = Z @ D with D = diag(1/max|B_j|).
# Right singular vectors of Zs live in the SCALED coords, and Zs u = 0 <=> Z (D u) = 0,
# so D^-1 vp is the object that belongs next to V2 -- which my original overlap ignored.
Dinv = np.maximum(np.abs(B).max(0), 1e-300)          # D^-1 as a diagonal
vp_scaled = vp*Dinv; vp_scaled /= np.linalg.norm(vp_scaled)
r_scaled   = np.linalg.norm(Zs @ vp_scaled)/np.linalg.norm(vp_scaled)
r_unscaled = np.linalg.norm(Zs @ vp)/np.linalg.norm(vp)
ov_scaled  = np.linalg.norm(S @ vp_scaled)
print(f"\n  r_scaled   = ||Zs @ (D^-1 v)|| / ||D^-1 v|| = {r_scaled:.4e}")
print(f"  r_unscaled = ||Zs @ v||        / ||v||      = {r_unscaled:.4e}")
print(f"  overlap(D^-1 v, span V2[nz])                = {ov_scaled:.6f}")
print(f"  overlap(v,      span V2[nz])  [original]    = {ov:.6f}")
if r_scaled < 1e-10 and ov_scaled > 0.99:
    print("  => BRANCH 1: column-scaling mismatch in MY overlap. v fine, subspace fine.")
elif r_scaled < 1e-10:
    print("  => BRANCH 2: v is null but V2[nz] is not the subspace I think -- slicing bug.")
else:
    print("  => BRANCH 3: v genuinely not null for Zs -- within/total and SVD disagree.")
# refit H using the correctly-scaled null block
M2 = np.column_stack([B @ (V2[k]/Dinv) for k in nz])   # DIVIDE: vp = vp_scaled/Dinv
c2,_,_,_ = np.linalg.lstsq(M2, Hfull, rcond=None)
print(f"  H residual using D-corrected null directions = "
      f"{np.linalg.norm(Hfull-M2@c2)/np.linalg.norm(Hfull):.4e}   (was 4.245e-02)")
