import time, numpy as np, os
os.environ['V16_XLO']='1.3'
import v16_split as M
ls=4.429699616905074; L=-ls*0.99
FJ,fW,fH=M.field('kerr35',L); xs,Ws=M.wmax(fW)
print('saddle', xs, Ws)
from scipy.integrate import solve_ivp
x=xs; px=0.0; py=M.py_from_H(fH,x,0.0,px); print('py',py)
s0=np.array([x,0.0,px,py]); 
def rhs(t,s): F,J=FJ(*s); return np.array(F)
def ev(t,s): return s[1] if t>1e-6 else 1.0
ev.direction=1; ev.terminal=True
t=time.time(); sol=solve_ivp(rhs,(0,400),s0,method='DOP853',rtol=1e-12,atol=1e-15,events=ev,t_eval=[])
print('no-var: t_event',sol.t_events, 'nfev',sol.nfev, 'sec',round(time.time()-t,2), 'status',sol.status)
t=time.time(); Pz,D,T=M.P(FJ,fH,np.array([xs,0.0]),1e-12); print('P var:',Pz,T,'sec',round(time.time()-t,2)); print(D, np.linalg.eigvals(D))
