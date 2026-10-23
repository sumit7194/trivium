import os, numpy as np
os.environ['V16_XLO']='1.6'; os.environ['V16_FPW']='0.5'
import v16_split as M
ls=9.110868547831844; L=-ls*0.99
FJ,fW,fH=M.field('ts35',L); xs,Ws=M.wmax(fW)
z,D,T,c=M.newton_fp(FJ,fH,(xs,0.0),1e-12)
ev,V=np.linalg.eig(D); k=int(np.argmax(abs(ev))); lam=float(ev[k].real); eu=V[:,k].real; eu/=np.linalg.norm(eu)
print('z',z,'lam',lam,'eu',eu)
for sign in (1.0,-1.0):
    ss=np.geomspace(1e-7,1e-7*lam,24); pts=[z+sign*s*eu for s in ss]
    for n in range(1,9):
        pts=[None if q is None else M.P(FJ,fH,q,1e-12)[0] for q in pts]
        ok=[q for q in pts if q is not None]
        if not ok: print(sign,n,'all lost', M.P.last); break
        xsv=[q[0] for q in ok]; pv=[q[1] for q in ok]
        print(sign,n,'alive',len(ok),'x[%.4f,%.4f] px[%.4g,%.4g]'%(min(xsv),max(xsv),min(pv),max(pv)), 'last',M.P.last)
