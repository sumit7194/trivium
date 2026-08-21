"""ansatz's degree-4 basis, emitted by them as scripts/_kt_emit_basis.py (e3172ac).

    COEFFICIENTS:  { x^i y^j / L^k : 0<=i<=dx, 0<=j<=dy }

Independent AS RATIONAL FUNCTIONS by construction -- distinct numerator monomials
over a common denominator. So there is no rank estimate, no tolerance, and no
orthogonalisation in the CONSTRUCTION, which is a direct answer to my bugs 2
(degenerate span read as conservation) and 3 (1008-1001, catastrophic cancellation
in a rank estimate).

They deliberately did NOT send the basis built from their own reducible products:
that one is exactly large enough to hold the reducibles, would calibrate
beautifully, and would prove nothing because an irreducible tensor would have no
room to appear.

k=2 IS THE POINT. k=1 reproduces their prover's scope. k=2 is where they are blind.

  delta=1: L=(x-1)(x+1)^2(y-1)(y+1),  box x<=6,  y<=8   -> 63 fns,  2205 cols, MUST return 14
  delta=2: L=(x-1)^2(x+1)^6(y-1)(y+1), box x<=16, y<=20 -> 357 fns, 12495 cols, must return 9
"""
import sys, itertools, numpy as np
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts"); sys.path.insert(0, ".")
from _zv_invariant import metric
from kt_screen import integrate

DEN = {1.0: (lambda x,y: (x-1)*(x+1)**2*(y-1)*(y+1), 6, 8),
       2.0: (lambda x,y: (x-1)**2*(x+1)**6*(y-1)*(y+1), 16, 20)}

def basis4(X, EL, delta, k=2):
    x,y,px,py = X[:,0],X[:,1],X[:,2],X[:,3]
    E=np.full(len(x),EL[0]); L=np.full(len(x),EL[1])
    mom=[(E**e[0])*(L**e[1])*(px**e[2])*(py**e[3])
         for e in itertools.product(range(5),repeat=4) if sum(e)==4]
    Lfn,dx,dy = DEN[delta]; den = Lfn(x,y)**k
    coo=[(x**i)*(y**j)/den for i in range(dx+1) for j in range(dy+1)]
    return np.column_stack([m*c for m,c in itertools.product(mom,coo)])

if __name__=="__main__":
    delta=float(sys.argv[1]); ntraj=int(sys.argv[2]) if len(sys.argv)>2 else 40
    ROWS_PER_ORBIT=int(sys.argv[5]) if len(sys.argv)>5 else 344
    f=metric(delta); rng=np.random.default_rng(11)
    Xs,ELs,tid=[],[],[]; t=0; tries=0
    while len(Xs)<ntraj and tries<4000:
        tries+=1
        E=rng.uniform(0.90,0.97); L=rng.uniform(2.6,3.6); x0=rng.uniform(float(sys.argv[3]) if len(sys.argv)>3 else 8.0, float(sys.argv[4]) if len(sys.argv)>4 else 16.0)
        X=integrate(f,x0,E,L)
        if X is None: continue
        Xs.append(X); ELs.append((E,L)); tid.append(np.full(len(X),t)); t+=1
        if t % 20 == 0:
            print(f"  collected {t}/{ntraj} orbits (tries={tries})", flush=True)
    # SUBSAMPLE PER ORBIT, BEFORE building the basis. The previous version vstacked
    # the full matrix and subsampled after: at 320 orbits that is 1.76M rows x 2205
    # cols x 8 B = 31 GB and the job died in the vstack. The progress line "building
    # basis for 320 orbits..." is the only reason the failure was locatable at all --
    # the run before it printed nothing and was indistinguishable from hung.
    NCOL = 35*((DEN[delta][1]+1)*(DEN[delta][2]+1))
    # ROWS PER ORBIT PINNED, not total rows. The original design pinned TOTAL rows at
    # ~12*ncols, so rows/orbit fell 1375 -> 687 -> 344 across n=20/40/80 -- meaning the
    # alpha trend conflated MORE ORBITS with FEWER ROWS PER ORBIT. Holding rows/orbit
    # fixed makes n the only thing that varies, which is what the trend is meant to measure.
    per = ROWS_PER_ORBIT
    print(f"  building basis: {len(Xs)} orbits x ~{per} samples, target ~{12*NCOL} rows "
          f"x {NCOL} cols (~{12*NCOL*NCOL*8/2**30:.2f} GB)", flush=True)
    sub=[]; subt=[]
    for X,el,ti in zip(Xs,ELs,tid):
        k=max(1,len(X)//per)
        sub.append(basis4(X[::k],el,delta)); subt.append(ti[::k])
    cols=np.vstack(sub); tid=np.concatenate(subt); del sub
    print(f"  basis built: {cols.shape}, {cols.nbytes/2**30:.2f} GB", flush=True)
    print(f"delta={delta}  degree 4  k=2  orbits={len(Xs)}  cols={cols.shape[1]}  "
          f"rows={len(cols)}", flush=True)
    NC=cols.shape[1]
    C=cols/np.maximum(np.abs(cols).max(0),1e-300)
    del cols
    print(f"  SVD of {C.shape} ...", flush=True)
    sv=np.linalg.svd(C,compute_uv=False); svn=sv/sv.max()
    print(f"  BASIS numerical rank: 1e-8 -> {(svn>=1e-8).sum()}, 1e-10 -> {(svn>=1e-10).sum()}, "
          f"1e-12 -> {(svn>=1e-12).sum()}   of {NC} "
          f"(independent as rational fns; this is the FINITE-SAMPLE rank)", flush=True)
    U,s,Vt=np.linalg.svd(C,full_matrices=False)
    for tol in [1e-8,1e-10,1e-12]:
        keep=s/s.max()>=tol; P=Vt[keep].T; B=C@P
        Z=np.empty_like(B)
        for kk in np.unique(tid):
            m=tid==kk; Z[m]=B[m]-B[m].mean(0)
        Z=Z/np.maximum(np.abs(B).max(0),1e-300)
        s2=np.linalg.svd(Z,compute_uv=False); s2/=s2.max()
        print(f"  tol={tol:.0e}  basis-rank={int(keep.sum()):5d}  "
              f"CONSERVED = {int((s2<tol).sum())}", flush=True)
