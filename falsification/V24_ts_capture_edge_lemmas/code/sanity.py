exec(open('v24.py').read().split('# ---- R1')[0])
import random
random.seed(1)
Vs = sp.cancel(sp.cancel(F*(W + 1)/2).subs(Y, sp.sqrt(s)))
dVs = sp.lambdify((X, s), sp.diff(Vs, s)); Vf = sp.lambdify((X, s), Vs); dVx = sp.lambdify((X, s), sp.diff(Vs, X))
mn = 1e9; cnt = 0
for _ in range(20000):
    x = random.uniform(9.3, 77.1); ss = random.uniform(0, 0.999999); v = dVs(x, ss); mn = min(mn, v); cnt += (v <= 0)
print('I2 float sample: min dV/ds', mn, 'nonpositive count', cnt)
mn = 1e9; cnt = 0; nh = 0
for _ in range(20000):
    x = random.uniform(1.5, 9.49); ss = random.uniform(0, 0.999999)
    if Vf(x, ss) <= 0:
        nh += 1; v = dVx(x, ss); mn = min(mn, v); cnt += (v <= 0)
print('I1 float sample in Hill:', nh, 'min dV/dx', mn, 'nonpositive', cnt)
