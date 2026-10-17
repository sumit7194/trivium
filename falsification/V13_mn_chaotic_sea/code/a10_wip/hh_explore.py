import sys, time, math, numpy as np
sys.path.insert(0, '/Users/sumit/Github/TheBridge/falsification/V13_mn_chaotic_sea/code')
import v13_a10_multishoot as M
t=time.time(); sy=M.HHSys(1/6); print('sc', sy.sc, sy.yrange)
w=np.array([0.1,0.05]); print(sy.P(w,1,1e-13), time.time()-t)
t=time.time(); J=sy.J(w,1,1e-13); print(J, np.linalg.det(J)-1, time.time()-t)
h=1e-6; fd=np.column_stack([(sy.P(w+h*e,1,1e-13)-sy.P(w-h*e,1,1e-13))/(2*h) for e in np.eye(2)]); print('fd rel', np.linalg.norm(fd-J)/np.linalg.norm(J))
t=time.time()
for _ in range(100): sy.P(w,1,1e-13)
print('per P', (time.time()-t)/100)
t=time.time()
for _ in range(20): sy.J(w,1,1e-13)
print('per J', (time.time()-t)/20)
