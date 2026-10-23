import time, numpy as np, os
os.environ['V16_XLO']='1.3'
import v16_split as M
L=-4.429699616905074*0.99
FJ,fW,fH=M.field('kerr35',L); xs,Ws=M.wmax(fW)
t=time.time(); z,D,T,clos=M.newton_fp(FJ,fH,(xs,0.0),1e-12); print('fp',z,'closure',clos,'T',T,'sec',round(time.time()-t,1)); print('eig',np.linalg.eigvals(D))
print('R0', M.reversor_check(FJ,fH,z,1e-12))
