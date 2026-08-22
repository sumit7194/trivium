"""Q2 extraction. TWO fit models, per gate Q2e: if my conclusion depends on which
model I picked, I have reproduced the defect this exercise exists to avoid.

  model 3p:  S(l) = A*(4l) + B*ln(l) + C
  model 4p:  S(l) = A*(4l) + B*ln(l) + C + D/l      <- the term that moved quantum's number

A = area coefficient, B = corner coefficient. Spread = (max-min)/mean over the four
regulators, in percent.
"""
import numpy as np
from regulators import REG
from entropy import run

def fit(ls, S, model):
    l = np.asarray(ls, float)
    cols = [4*l, np.log(l), np.ones_like(l)]
    if model == "4p": cols.append(1.0/l)
    M = np.column_stack(cols)
    c, *_ = np.linalg.lstsq(M, S, rcond=None)
    return c[0], c[1]

def spread(v):
    v = np.asarray(v, float)
    return 100.0*(v.max()-v.min())/abs(v.mean())

if __name__ == "__main__":
    import sys, time
    CFG = {"s=1": (160, 0.01,  list(range(4,21,2))),
           "s=2": (320, 0.005, list(range(8,41,4)))}
    res = {}
    for tag,(L,m,ls) in CFG.items():
        S = {}
        for reg in REG:
            t0=time.time(); S[reg] = run(L,m,ls,reg)
            print(f"  {tag} {reg:>14} done [{time.time()-t0:.0f}s]", flush=True)
        res[tag] = (ls, S)
    print()
    print(f"{'':>6} | {'model':>5} | {'AREA spread %':>14} | {'CORNER spread %':>16}")
    summary={}
    for tag,(ls,S) in res.items():
        for model in ("3p","4p"):
            A=[]; B=[]
            for reg in REG:
                a,b = fit(ls, S[reg], model); A.append(a); B.append(b)
            sa, sb = spread(A), spread(B)
            summary[(tag,model)] = (sa, sb, A, B)
            print(f"{tag:>6} | {model:>5} | {sa:14.2f} | {sb:16.2f}")
    print()
    print("Q2b POSITIVE CONTROL — area coefficient must NOT be universal (>10%):")
    for model in ("3p","4p"):
        v = summary[("s=1",model)][0]
        print(f"   {model}: area spread at s=1 = {v:.2f}%   {'PASS (not universal)' if v>10 else 'FAIL — I am wrong'}")
    print()
    print("Q2c PRIMARY — corner spread must fall >=3x; area spread must change <10% relative:")
    for model in ("3p","4p"):
        a1,b1,_,_ = summary[("s=1",model)]; a2,b2,_,_ = summary[("s=2",model)]
        fall = b1/b2 if b2>0 else float('inf')
        arel = 100*abs(a2-a1)/a1
        print(f"   {model}: corner {b1:.2f}% -> {b2:.2f}%  = {fall:.2f}x fall   |   "
              f"area {a1:.2f}% -> {a2:.2f}%  = {arel:.1f}% relative change")
        print(f"        corner falls>=3x: {fall>=3}   area flat<10%: {arel<10}   "
              f"=> {'AGREE' if (fall>=3 and arel<10) else 'DISAGREE'}")
    np.save("q2_summary.npy", np.array([[summary[(t,m)][0],summary[(t,m)][1]]
                                        for t in CFG for m in ("3p","4p")]))
