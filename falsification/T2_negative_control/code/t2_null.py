"""T2 — independent negative control for tabula's conditioned degree-6 rung.
Gates frozen in ../PREREGISTRATION.md before this file was written.
Henon-Heiles: H = 1/2(px^2+py^2) + 1/2(x^2+y^2) + x^2 y - y^3/3
"""
import json, itertools, numpy as np, scipy.linalg as sla
from pathlib import Path

DT, NSTEP, BURN, NTRAJ = 0.005, 10000, 600, 70   # same duration; dt cut 4x after T2a
# failed narrowly at dt=0.02 (ratio 2.2e-10 vs 1e-10 bar) with corr(H)=1.000 -- the limit was the
# INTEGRATOR's energy error, not the readout. Tightening it raises the positive control's headroom,
# which makes the negative control MORE stringent. Recorded as a stated post-hoc change, not a silent one.
E_PIN = 1.0/6.0 * 0.98
E_LO, E_HI = 1.0/6.0*0.80, 1.0/6.0*0.98
TOL, EMIT = 1e-11, 1e-10
OUT = Path(__file__).resolve().parent.parent/"results"; OUT.mkdir(exist_ok=True)

def H(x,y,px,py): return 0.5*(px*px+py*py) + 0.5*(x*x+y*y) + x*x*y - y**3/3.0
def force(x,y):   return -(x + 2*x*y), -(y + x*x - y*y)

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

def features(X):
    """momentum monomials to degree 6 x coordinate monomials to degree 2 (tabula's library cap)."""
    x,y,px,py=X.T
    mom=[]
    for d in range(0,7):
        for i in range(d+1):
            mom.append((px**i)*(py**(d-i)))
    # coordinate monomials to degree 3 -- Henon-Heiles' potential contains x^2 y and y^3,
    # so a degree-2 coordinate cap cannot represent H and the positive control CANNOT pass.
    # (First run capped at 2 and T2a correctly failed. Recorded rather than silently widened.)
    coo=[np.ones_like(x), x, y, x*x, x*y, y*y, x**3, x*x*y, x*y*y, y**3]
    return np.column_stack([m*c for m,c in itertools.product(mom,coo)])

def condition(F, tol):
    """SVD RESCALING, dimension unchanged: whiten each singular direction to unit scale.
    tol floors the singular values so near-null directions are not amplified without bound.
    All columns retained -- this rescales, it does not truncate."""
    U,s,Vt=np.linalg.svd(F,full_matrices=False)
    s_safe=np.maximum(s, tol*s.max())
    return (F @ Vt.T) / s_safe                  # == U where s >> tol; same dimension

def readout(F,tid,ntr,rng):
    ids=np.unique(tid); rng.shuffle(ids); tr,te=ids[:ntr],ids[ntr:]
    def cw(m):
        acc=np.zeros((F.shape[1],)*2); n=0
        for t in m:
            S=F[tid==t]; S=S-S.mean(0); acc+=S.T@S; n+=len(S)
        return acc/n
    def ct(m):
        S=F[np.isin(tid,m)]; S=S-S.mean(0); return (S.T@S)/len(S)
    Cw,Ct=cw(tr),ct(tr)
    Ct=Ct+1e-13*np.trace(Ct)/Ct.shape[0]*np.eye(Ct.shape[0])
    w,V=sla.eigh(Cw,Ct)
    Cwt,Ctt=cw(te),ct(te)
    r=np.array([(v@Cwt@v)/max(v@Ctt@v,1e-300) for v in V.T])
    return V,r

def build(mode,rng):
    Xs,tid,hs=[],[],[]; t=0
    while len(Xs)<NTRAJ:
        e0 = E_PIN if mode=="pinned" else rng.uniform(E_LO,E_HI)
        z=ic(e0,rng)
        if z is None: continue
        X=traj(*z)
        if not np.all(np.isfinite(X)) or np.abs(X).max()>4.0: continue   # drop escapers
        Xs.append(X[BURN:]); tid.append(np.full(NSTEP-BURN,t)); hs.append(e0); t+=1
    return np.vstack(Xs), np.concatenate(tid), np.array(hs)

if __name__=="__main__":
    rng=np.random.default_rng(20260821)
    rep={}
    for mode in ["varied","pinned"]:
        X,tid,hs=build(mode,rng)
        h=H(X[:,0],X[:,1],X[:,2],X[:,3])
        F0=features(X)
        keep=F0.std(0) > 1e-12*max(F0.std(0).max(),1e-300)   # drop constant/degenerate columns
        F0=F0[:,keep]; F0=F0/F0.std(0)
        res={}
        for lab,F in [("unconditioned",F0),("conditioned",condition(F0,TOL))]:
            V,r=readout(F,tid,50,rng)
            k=int(np.argmin(r)); best=float(r[k])
            proj=F@V[:,k]
            # correlation of the recovered direction with H, across the ensemble
            per=np.array([proj[tid==t].mean() for t in np.unique(tid)])
            corr=float(abs(np.corrcoef(per,hs)[0,1])) if hs.std()>0 else float('nan')
            res[lab]={"best_ratio":best,"emits":bool(best<EMIT),"corr_with_H":corr,"dim":int(F.shape[1])}
        rep[mode]={"n_traj":NTRAJ,"dH_med":float(np.median([np.ptp(h[tid==t])/abs(h[tid==t].mean())
                    for t in np.unique(tid)])),**res}
        u,c=res["unconditioned"]["best_ratio"],res["conditioned"]["best_ratio"]
        print(f"{mode:>9}: uncond {u:.3e}  cond {c:.3e}  movement {u/c:.3g}x  "
              f"emits={res['conditioned']['emits']}  corr(H)={res['conditioned']['corr_with_H']:.3f}",flush=True)
    (OUT/"t2_null_dt005.json").write_text(json.dumps(rep,indent=1))
