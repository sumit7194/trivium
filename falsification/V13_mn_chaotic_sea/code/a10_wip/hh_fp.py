import sys, time, math, numpy as np
sys.path.insert(0, '/Users/sumit/Github/TheBridge/falsification/V13_mn_chaotic_sea/code')
import v13_a10_multishoot as M
E=float(sys.argv[1]); sy=M.HHSys(E); print('sc', sy.sc, sy.yrange)
found=[]
for y0 in np.linspace(sy.yrange[0]+0.02, sy.yrange[1]-0.02, 30):
    pr=2*E-y0*y0+2*y0**3/3
    if pr<=0: continue
    for p0 in np.linspace(-0.9*math.sqrt(pr),0.9*math.sqrt(pr),15):
        z=np.array([y0,p0]); okz=False
        for _ in range(40):
            Pz=sy.P(z,1,1e-13)
            if Pz is None: break
            F=Pz-z
            if np.max(np.abs(F))<1e-12: okz=True; break
            J=sy.J(z,1,1e-13)
            if J is None: break
            dz=np.linalg.solve(J-np.eye(2),-F); lam=1.0
            while lam>1e-3:
                zn=z+lam*dz; Pn=sy.P(zn,1,1e-13)
                if Pn is not None and np.max(np.abs(Pn-zn))<np.max(np.abs(F)): break
                lam*=0.5
            z=zn
        if okz and not any(np.hypot(*(z-f))<1e-8 for f in found):
            found.append(z); J=sy.J(z,1,1e-13); ev=np.linalg.eigvals(J); print(z, 'tr', np.trace(J), 'ev', ev)
