"""tabula's S3 audit: order ladder on chaotic Henon-Heiles.

Reimplemented blind from tabula's written spec; their `certify` was not read.

Their C5 refinement 1 says a positive control must match the certify in DEGREE.
S3 certifies CERTIFY-NO-INVARIANT-IN[poly(state), order 2]. My T2 positive control
recovered H -- but H carries x^2 y and y^3, so H is ORDER 3 and demonstrates the
instrument on a different family than the one certifying. Hence the ladder: one
ensemble, one instrument, ONLY the hypothesis class moves.

  N=2  expect ~0.58   CERTIFY   (the verdict under audit)
  N=3  expect ~1e-12  EMIT      (H becomes representable)
  N=4  expect ~1e-12  EMIT

PASS = N=2 certifies AND N=3 emits.
KNOWN-FAIL = N=3 does NOT reach the floor => instrument blind at every order on
this substrate => S3 is undemonstrated, a finding against tabula's certificate.

SHELL-VARIED ensemble per tabula: a pinned shell makes a per-realization nuisance
constant available which the engine finds at ~4e-17, more conserved than the real
invariant, and the ladder would inverts into a false pass.
"""
import itertools, numpy as np, scipy.linalg as sla

DT, NSTEP, BURN, NTRAJ = 0.005, 10000, 600, 70
E_LO, E_HI = 1.0/6.0*0.80, 1.0/6.0*0.98        # SHELL VARIED

def H(x,y,px,py): return 0.5*(px*px+py*py)+0.5*(x*x+y*y)+x*x*y-y**3/3.0
def force(x,y):   return -(x+2*x*y), -(y+x*x-y*y)

def traj(x0,y0,px0,py0,n=NSTEP):
    X=np.empty((n,4)); x,y,px,py=x0,y0,px0,py0; ax,ay=force(x,y)
    for i in range(n):
        px+=0.5*DT*ax; py+=0.5*DT*ay; x+=DT*px; y+=DT*py
        ax,ay=force(x,y); px+=0.5*DT*ax; py+=0.5*DT*ay
        X[i]=(x,y,px,py)
    return X

def ic(e0,rng):
    for _ in range(6000):
        x,y=rng.uniform(-0.7,0.7,2)
        v=e0-(0.5*(x*x+y*y)+x*x*y-y**3/3.0)
        if v<=1e-6: continue
        th=rng.uniform(0,2*np.pi); p=np.sqrt(2*v)
        return x,y,p*np.cos(th),p*np.sin(th)
    return None

def poly_basis(X, order):
    """ALL monomials in (x,y,px,py) of total degree 1..order. Degree-0 (constant)
    EXCLUDED: a constant is perfectly conserved and defeats the test outright."""
    cols=[]
    for d in range(1, order+1):
        for e in itertools.product(range(d+1), repeat=4):
            if sum(e)==d:
                cols.append(np.prod([X[:,i]**e[i] for i in range(4)], axis=0))
    return np.column_stack(cols)

def heldout_ratio(F, tid, rng, ntr=50):
    ids=np.unique(tid); rng.shuffle(ids); tr,te=ids[:ntr],ids[ntr:]
    def cw(m):
        a=np.zeros((F.shape[1],)*2); n=0
        for t in m:
            S=F[tid==t]; S=S-S.mean(0); a+=S.T@S; n+=len(S)
        return a/n
    def ct(m):
        S=F[np.isin(tid,m)]; S=S-S.mean(0); return (S.T@S)/len(S)
    Cw,Ct=cw(tr),ct(tr)
    Ct=Ct+1e-13*np.trace(Ct)/Ct.shape[0]*np.eye(Ct.shape[0])
    w,V=sla.eigh(Cw,Ct)
    Cwt,Ctt=cw(te),ct(te)
    r=np.array([(v@Cwt@v)/max(v@Ctt@v,1e-300) for v in V.T])
    k=int(np.argmin(r))
    return float(r[k]), V[:,k]

if __name__=="__main__":
    rng=np.random.default_rng(20260822)
    Xs,tid,es=[],[],[]; t=0
    while len(Xs)<NTRAJ:
        e0=rng.uniform(E_LO,E_HI); z=ic(e0,rng)
        if z is None: continue
        X=traj(*z)
        if not np.all(np.isfinite(X)) or np.abs(X).max()>4.0: continue
        Xs.append(X[BURN:]); tid.append(np.full(NSTEP-BURN,t)); es.append(e0); t+=1
    X=np.vstack(Xs); tid=np.concatenate(tid); es=np.array(es)
    print(f"ensemble: {NTRAJ} chaotic trajectories, SHELL VARIED E0 in "
          f"[{E_LO:.4f},{E_HI:.4f}], dt={DT}, {NSTEP-BURN} samples each\n", flush=True)
    print(f"{'order':>6} | {'dim':>4} | {'C3 heldout ratio':>17} | {'verdict':>8} | {'corr(dir,H)':>11}")
    h=H(X[:,0],X[:,1],X[:,2],X[:,3])
    for N in [2,3,4]:
        F=poly_basis(X,N); F=F/np.maximum(F.std(0),1e-300)
        r,v=heldout_ratio(F,tid,np.random.default_rng(7))
        proj=F@v
        per=np.array([proj[tid==k].mean() for k in np.unique(tid)])
        ph =np.array([h[tid==k].mean()    for k in np.unique(tid)])
        c=abs(np.corrcoef(per,ph)[0,1])
        print(f"{N:6d} | {F.shape[1]:4d} | {r:17.4e} | "
              f"{'EMIT' if r<1e-10 else 'CERTIFY':>8} | {c:11.4f}", flush=True)
