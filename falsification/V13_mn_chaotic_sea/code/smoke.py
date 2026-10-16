import time, numpy as np, sympy as sp
from v13_orbit import make
R=sp.Rational
t0=time.time()
integ,start,ham,inD,pieces = make(1, R(9,10), R(19,20)/(R(19,100))**R(3,2), R(19,20), 3, domain='base')
print('build', round(time.time()-t0,1),'s')
for x0 in (2.6, 3.0, 4.0, 8.0, 20.0):
    t1=time.time(); out=integ(x0, 0.0, 200, 1e-13, 1e-15, 1e7, 20_000_000)
    print(x0, 'outcome',out[0],'ncross',out[1],'tau',round(out[2],1),'drift',out[3],'steps',out[4],'time',round(time.time()-t1,2),'s')
