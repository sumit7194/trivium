"""Q2 — entanglement entropy of a square region, free scalar ground state on a
periodic LxL lattice. MY extraction; quantum's code not read.

Route chosen (Peschel / Casini-Huerta correlator method):
  ground state is Gaussian, so it is fixed by
      X(r) = <q_0 q_r> = (1/L^2) sum_k  1/(2 w(k))  e^{ik.r}
      P(r) = <p_0 p_r> = (1/L^2) sum_k  w(k)/2      e^{ik.r}
  both computed ONCE per (L, m, regulator) by FFT over the k-lattice, then the
  region blocks X_A, P_A are lookups on r = i - j.
  Symplectic eigenvalues nu = sqrt(eig(X_A P_A)), taken via the symmetric form
  sqrt(X_A) P_A sqrt(X_A) so the spectrum is real by construction.
      S = sum [ (nu+1/2) ln(nu+1/2) - (nu-1/2) ln(nu-1/2) ]
"""
import numpy as np, scipy.linalg as sla
from regulators import REG

def correlators(L, m, reg):
    k = 2*np.pi*np.fft.fftfreq(L)
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.sqrt(REG[reg](KX, KY, m*m))
    X = np.fft.ifft2(1.0/(2.0*w)).real          # X(r), shape (L,L)
    P = np.fft.ifft2(w/2.0).real                # P(r)
    return X, P

def entropy(X, P, l, L):
    idx = np.arange(l)
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    flat_x = IX.ravel(); flat_y = IY.ravel()
    dx = (flat_x[:,None] - flat_x[None,:]) % L
    dy = (flat_y[:,None] - flat_y[None,:]) % L
    XA = X[dx, dy]; PA = P[dx, dy]
    XA = (XA+XA.T)/2; PA = (PA+PA.T)/2
    sX = sla.sqrtm(XA).real
    M = sX @ PA @ sX
    M = (M+M.T)/2
    ev = np.linalg.eigvalsh(M)
    nu = np.sqrt(np.clip(ev, 0.25, None))       # nu >= 1/2 exactly at purity
    a, b = nu+0.5, nu-0.5
    return float(np.sum(a*np.log(a) - np.where(b>0, b*np.log(np.maximum(b,1e-300)), 0.0)))

def run(L, m, ls, reg):
    X, P = correlators(L, m, reg)
    return np.array([entropy(X, P, l, L) for l in ls])

if __name__ == "__main__":
    import sys, time
    L, m = 160, 0.01
    ls = list(range(4, 21, 2))
    print(f"s=1: L={L} m={m} l={ls}\n")
    print(f"{'regulator':>14} | " + " | ".join(f"l={l:<2d}" for l in ls))
    out={}
    for reg in REG:
        t0=time.time(); S = run(L, m, ls, reg); out[reg]=S
        print(f"{reg:>14} | " + " | ".join(f"{v:6.3f}" for v in S) + f"   [{time.time()-t0:.0f}s]", flush=True)
    np.save("s1_entropies.npy", np.array([out[r] for r in REG]))
    print("\n  saved s1_entropies.npy")
