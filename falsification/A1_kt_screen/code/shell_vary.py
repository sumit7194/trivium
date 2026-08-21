"""ansatz's mass-shell trap, done properly.

My first null-vector check was VACUOUS: H = -1/2 identically on every orbit, so
"is H in the span" was answered by the constant column I had put in the fit.
Residual 2.8e-13 meant only that a constant fits a constant.

Fix: VARY THE NORMALISATION. p_on_shell solves H = -1/2; here p1 is solved from
    g11 p1^2 = 2c - W - g22 p2^2
with c drawn per orbit, so H varies ACROSS the ensemble while staying conserved
ALONG each. Then H has variance to detect and the question is no longer degenerate.
"""
import sys, itertools, numpy as np
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
sys.path.insert(0, ".")
from _zv_invariant import metric
from poincare import _rk4, H_value
from kt_screen import basis

HSTEP, NSTEP, BURN = 0.02, 6000, 500

def p1_at(f, x0, py, E, L, c):
    W = f["W"](x0, 0.0, E, L); g11 = f["g11"](x0,0.0,E,L); g22 = f["g22"](x0,0.0,E,L)
    val = (2*c - W - g22*py*py)/g11
    return np.sqrt(val) if val > 0 else None

def integrate_c(f, x0, E, L, c):
    a,b = 0.0, 3.0
    if p1_at(f,x0,0.0,E,L,c) is None: return None
    for _ in range(60):
        m = 0.5*(a+b)
        if p1_at(f,x0,m,E,L,c) is None: b=m
        else: a=m
    py=a; p1=p1_at(f,x0,py,E,L,c)
    if p1 is None: return None
    s=[x0,0.0,p1,py]; H0=H_value(f,s,E,L); X=np.empty((NSTEP,4))
    for i in range(NSTEP):
        try: s=_rk4(f,s,HSTEP,E,L)
        except (OverflowError,ZeroDivisionError,ValueError): return None
        if s[0]<1.3 or s[0]>120 or abs(s[1])>0.999: return None
        X[i]=s
    if abs(H_value(f,s,E,L)-H0)/max(abs(H0),1e-300) > 1e-6: return None
    return X[BURN:], H0

if __name__=="__main__":
    import sys
    CLO=float(sys.argv[1]); CHI=float(sys.argv[2])
    PTOL=float(sys.argv[3]) if len(sys.argv)>3 else 1e-8
    f=metric(1.0); rng=np.random.default_rng(11)
    Xs,ELs,tid,Hs=[],[],[],[]; t=0; tries=0
    while len(Xs)<40 and tries<6000:
        tries+=1
        E=rng.uniform(0.90,0.97); L=rng.uniform(2.6,3.6); x0=rng.uniform(8.0,16.0)
        c=rng.uniform(CLO,CHI)                           # VARIED mass shell
        r=integrate_c(f,x0,E,L,c)
        if r is None: continue
        X,H0=r; Xs.append(X); ELs.append((E,L)); Hs.append(H0)
        tid.append(np.full(len(X),t)); t+=1
    Hs=np.array(Hs)
    print(f"orbits={len(Xs)}   H across ensemble: [{Hs.min():.4f}, {Hs.max():.4f}]  "
          f"sd={Hs.std():.4f}   <- NOT constant now", flush=True)
    cols=np.vstack([basis(X,el,2,0,f) for X,el in zip(Xs,ELs)]); tid=np.concatenate(tid)
    step=max(1,len(cols)//(12*cols.shape[1])); cols,tid=cols[::step],tid[::step]
    Hfull=np.concatenate([np.full(len(X),h) for X,h in zip(Xs,Hs)])[::step]
    C=cols/np.maximum(np.abs(cols).max(0),1e-300)
    U,sv,Vt=np.linalg.svd(C,full_matrices=False); keep=sv/sv.max()>=1e-8
    P=Vt[keep].T; B=C@P
    Z=np.empty_like(B)
    for k in np.unique(tid):
        m=tid==k; Z[m]=B[m]-B[m].mean(0)
    Z=Z/np.maximum(np.abs(B).max(0),1e-300)
    _,s2,V2=np.linalg.svd(Z,full_matrices=False); s2n=s2/s2.max()
    nz=np.where(s2n<PTOL)[0]
    print(f"ptol={PTOL:.0e}  kept={int(keep.sum())}/{C.shape[1]}  conserved={len(nz)}", flush=True)
    M=np.column_stack([B@V2[k] for k in nz])
    # NO constant column this time -- H now varies, so the fit is a real test
    coef,_,_,_=np.linalg.lstsq(M,Hfull,rcond=None); fit=M@coef
    print(f"H recovered from the {len(nz)} directions WITHOUT a constant column:")
    print(f"   residual |H-fit|/|H| = {np.linalg.norm(Hfull-fit)/np.linalg.norm(Hfull):.3e}")
    # and the control: can 4 random directions do it?
    rr=np.random.default_rng(3); R=B[:, rr.choice(B.shape[1], len(nz), replace=False)]
    cf,_,_,_=np.linalg.lstsq(R,Hfull,rcond=None)
    print(f"   same fit from {len(nz)} RANDOM basis directions (control): "
          f"{np.linalg.norm(Hfull-R@cf)/np.linalg.norm(Hfull):.3e}")
