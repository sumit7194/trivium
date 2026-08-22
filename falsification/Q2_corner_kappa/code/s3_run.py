"""s=3: L=480, m=0.00333, l=12,18,...,60. quantum confirmed s=1 and s=2 are the
whole of their refinement axis, so this point is NEW INFORMATION FOR BOTH OF US
and cannot have been anchored by anything they disclosed."""
import numpy as np, time
from regulators import REG
from entropy import run
from extract import fit, spread
L, m, ls = 480, 0.00333, list(range(12,61,6))
S={}
for reg in REG:
    t0=time.time(); S[reg]=run(L,m,ls,reg)
    print(f"  {reg:>14} done [{time.time()-t0:.0f}s]", flush=True)
for model in ("3p","4p"):
    A=[];B=[]
    for reg in REG:
        a,b=fit(ls,S[reg],model); A.append(a); B.append(b)
    print(f"  s=3 {model}: area spread {spread(A):.2f}%   corner spread {spread(B):.2f}%", flush=True)
