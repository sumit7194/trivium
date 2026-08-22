"""s=4: L=640, m=0.0025, l=16,24,...,80.

THE DISCRIMINATOR quantum could not run. Their two readings of the deceleration:
  A: converging to ZERO with varying effective exponent (regulators differ at
     O(k^4), so asymptotic rate ~s^-2, and 2.76 -> 1.81 brackets it).
     => corner coefficient EXACTLY universal, wobble is subleading terms.
  B: converging to a small NON-ZERO FLOOR near 0.1%. Local exponent falls
     monotonically toward zero as the floor is approached -- which 2.76 -> 1.81
     also looks like exactly.
     => corner coefficient universal TO ~0.1% AND NO FURTHER. A physical statement.

They could not separate them: fitting A*s^-2 + F to three points gives F = -0.23%,
an unphysical negative floor, and any 3-parameter form fits 3 points exactly.

s=4 separates them. Under A the spread keeps falling; under B it flattens near 0.1%.

m*L = 1.6 and l/L held identical to s=1,2,3 -- only the lattice spacing changes.
sqrtm replaced by eigendecomposition: 6400x6400 scipy.sqrtm is not affordable.
"""
import numpy as np, time
from pathlib import Path
from regulators import REG
from entropy import correlators
from extract import fit, spread

def entropy_big(X, P, l, L):
    idx = np.arange(l)
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    fx = IX.ravel(); fy = IY.ravel()
    dx = (fx[:,None]-fx[None,:]) % L; dy = (fy[:,None]-fy[None,:]) % L
    XA = X[dx,dy]; PA = P[dx,dy]
    XA = (XA+XA.T)/2; PA = (PA+PA.T)/2
    d, V = np.linalg.eigh(XA)                      # sqrt via eigendecomposition
    sX = (V*np.sqrt(np.clip(d,0,None))) @ V.T
    del d, V, XA
    M = sX @ PA @ sX; del sX, PA
    M = (M+M.T)/2
    ev = np.linalg.eigvalsh(M); del M
    return ev                                       # RETURN THE SPECTRUM, not S

def S_at(ev, floor):
    """Entropy with the symplectic-eigenvalue floor set explicitly.
    quantum's ask: sweeping this decades apart measures whether a flattening at
    s=4 is PHYSICAL or is my own numerical floor. Their scaling probe extrapolates
    a clip band of ~5e-06 at 6400 sites against a ~8e-06 requirement for a 0.1%
    corner claim -- a factor 1.5, not comfortably below."""
    nu = np.sqrt(np.clip(ev, 0.25, None))
    b  = np.maximum(nu - 0.5, floor)
    a  = nu + 0.5
    return float(np.sum(a*np.log(a) - b*np.log(b)))

if __name__=="__main__":
    L, m, ls = 960, 1/600., list(range(24,121,12))
    print(f"s=6: L={L} m={m} m*L={m*L} l={ls}", flush=True)
    # PER-REGULATOR CHECKPOINT. The first s=5 attempt lost 340s of completed work to
    # the fifth power cut in three days, because it held every spectrum in memory and
    # wrote nothing until all four regulators finished. G3's runs survive cuts because
    # they checkpoint per orbit; this one had no equivalent. Same lesson, not applied
    # here until it cost something.
    CK = Path(__file__).resolve().parent.parent / "s6_spectra.npz"
    S={}
    if CK.exists():
        z=np.load(CK, allow_pickle=True)
        S={k:list(v) for k,v in z.items()}
        print(f"  RESUMING — {len(S)} regulator(s) already banked: {sorted(S)}", flush=True)
    for reg in REG:
        if reg in S: 
            print(f"  {reg:>14} skipped (banked)", flush=True); continue
        t0=time.time(); X,P = correlators(L,m,reg)
        S[reg]=[entropy_big(X,P,l,L) for l in ls]
        np.savez(CK, **{k:np.array(v,dtype=object) for k,v in S.items()})
        print(f"  {reg:>14} done [{time.time()-t0:.0f}s]  banked", flush=True)
    print()
    for floor in (1e-14, 1e-9):
        for model in ("3p","4p"):
            A=[];B=[]
            for reg in REG:
                Sv = np.array([S_at(ev, floor) for ev in S[reg]])
                a,b = fit(ls, Sv, model); A.append(a); B.append(b)
            print(f"  s=6 floor={floor:.0e} {model}: area {spread(A):.4f}%   "
                  f"CORNER {spread(B):.5f}%", flush=True)
    print()
    print("  CLIP BAND = difference in corner spread between the two floors.")
    print("  band << spread  -> a flattening near 0.1% is PHYSICAL (Reading B)")
    print("  band ~  spread  -> the flattening is MY FLOOR, Reading B unsupported")
