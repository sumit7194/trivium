import sys, time, math, json, numpy as np
sys.path.insert(0, '/Users/sumit/Github/TheBridge/falsification/V13_mn_chaotic_sea/code')
import v13_a10_multishoot as M
pt=sys.argv[1]; want={tuple(map(int,e.split('-'))) for e in sys.argv[2].split(',')}
A9, sc, scope, jobs = M.edge_jobs(pt, want)
M.init_worker(pt, *M.level(A9), sc); sy=M.W['sy']
def noise(w, n, t, rtol=M.RT):
    """rms deviation from linear prediction over 12 perturbations of size k*8ulp along t (scaled)."""
    p0=sy.P(w,n,rtol); J=sy.J(w,n,rtol); dev=[]
    tt=t/np.linalg.norm(t)
    for k in range(1,13):
        d=tt*k*8*np.spacing(np.max(np.abs(w)))*1e2
        pk=sy.P(w+d,n,rtol); dk=(pk-p0-J@d)/sy.sc; dev.append(np.hypot(*dk))
    return float(np.sqrt(np.mean(np.square(dev)))), float(np.max(dev))
for j in jobs:
    E=M.Edge(j['zi'],j['vi'],j['pi'],j['a'],j['zg'],j['vg'],j['pg'],j['b']); E.lam_i,E.lam_g=j['lam_i'],j['lam_g']
    X0=M.ms_initial(sy,E,j['s0'],j['sp0'],M.RT); r=M.ms_solve(sy,E,X0,M.RT)
    print(j['src'],'->',j['dst'],'a,b',E.a,E.b,'pow',E.pi,E.pg,'why',r['why_stop'],'iters',r['iters_accepted'])
    print('  seg_res', ['%.1e'%x for x in r['seg_res']]); print('  hist', [('%.1e'%h['norm2'],'%.1e'%h['maxseg'],h.get('lam')) for h in r['hist']])
    s,w,sp_,u=E.unpack(np.array(r['X']))
    for k in range(E.a): print('  Wu seg',k+1,'noise rms/max (scaled)', noise(w[k],E.pi,E.vi if k==0 else np.array([1.0,0.3])))
    for k in range(E.b): print('  Ws seg',k+1,'noise rms/max (scaled)', noise(u[k],E.pg,E.vg if k==0 else np.array([1.0,0.3])))
