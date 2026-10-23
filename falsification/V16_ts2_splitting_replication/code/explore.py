import numpy as np
from v16_split import field
def maxima(case,L):
    FJ,fW,fH = field(case, L)
    xs=np.linspace(1.3,40,1600); w=np.array([fW(x,0.0) for x in xs]); d=np.diff(w)
    return [(round(xs[i],3), round(w[i],5)) for i in range(1,len(d)) if d[i-1]>0 and d[i]<=0]
for case,Ls in (('kerr35',np.arange(6.0,7.01,0.2)),('ts35',np.arange(7.0,11.01,0.5)),('ts35',np.arange(-11.0,-6.9,1.0))):
    for L in Ls: print(case, round(L,2), maxima(case,float(L))[:2])
