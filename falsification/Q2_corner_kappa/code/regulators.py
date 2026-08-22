"""Q2a — the four regulators must agree with m^2 + k^2 to O(k^4) as k->0.
quantum: if one does not, that disagreement is the first finding and we stop there.
Gate frozen in ../PREREGISTRATION.md before this file was written.
"""
import numpy as np

def K2(kx, ky):  return (2-2*np.cos(kx)) + (2-2*np.cos(ky))

def K4(kx, ky):
    f = lambda k: (4/3)*(2-2*np.cos(k)) - (1/12)*(2-2*np.cos(2*k))
    return f(kx) + f(ky)

REG = {
    "nn":           lambda kx,ky,m2: m2 + K2(kx,ky),
    "improved":     lambda kx,ky,m2: m2 + K4(kx,ky),
    "higher_deriv": lambda kx,ky,m2: m2 + K2(kx,ky) + 0.25*K2(kx,ky)**2,
    "smeared":      lambda kx,ky,m2: m2 + K2(kx,ky)*np.exp(0.15*K2(kx,ky)),
}

if __name__ == "__main__":
    print("Q2a — small-k agreement with m^2 + k^2.  m=0 so the test is on k alone.")
    print("Reporting  (omega^2 - k^2)/k^4  as k->0 along the diagonal: finite => O(k^4) agreement,")
    print("diverging => the regulator differs at O(k^2) and the gate FAILS.\n")
    print(f"{'k':>10} | " + " | ".join(f"{n:>14}" for n in REG))
    rows={n:[] for n in REG}
    for k in [0.2, 0.1, 0.05, 0.025, 0.0125]:
        kx=ky=k/np.sqrt(2); k2=kx*kx+ky*ky
        vals=[]
        for n,f in REG.items():
            w2=f(kx,ky,0.0); r=(w2-k2)/k2**2; rows[n].append(r); vals.append(r)
        print(f"{k:10.4f} | " + " | ".join(f"{v:14.6f}" for v in vals))
    print()
    ok=True
    for n,v in rows.items():
        conv = abs(v[-1]-v[-2]) < 0.05*max(abs(v[-1]),1e-30) or abs(v[-1])<1e-8
        # also check O(k^2) coefficient vanishes: (w2-k2)/k2 -> 0
        kx=ky=0.0125/np.sqrt(2); k2=kx*kx+ky*ky
        o2=(REG[n](kx,ky,0.0)-k2)/k2
        print(f"  {n:>14}:  (w2-k2)/k4 -> {v[-1]:+.6f}   (w2-k2)/k2 -> {o2:+.3e}")
        if abs(o2) > 1e-3: ok=False
    print(f"\n  Q2a: {'PASS — all four agree to O(k^4)' if ok else 'FAIL — a regulator differs at O(k^2)'}")
