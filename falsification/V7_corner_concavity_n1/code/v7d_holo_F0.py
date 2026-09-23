"""V7d addendum -- holographic CC check INCLUDING the F(0) = kappa/4 node, done in 30-digit arithmetic.
The first run (v7d_known.py 'holographic_with_F0') estimated kappa as Omega*a at the smallest angle. That forces the
first chord slope to ~0 and is not the pre-registered node; its failure is an estimator artefact (recorded, not hidden).
Here kappa is the closed form Gamma(3/4)^4/pi (units L^2/(2G) = 1), first checked against the bridge's own quadrature
by Richardson extrapolation of Omega*a(Omega) -> kappa.
"""
import mpmath as mp, json
mp.mp.dps = 40
def holo(h0):
    h0 = mp.mpf(h0); s = mp.sqrt(1 + h0**2); hh = lambda t: h0*mp.sin(t)
    Om = 2*mp.quad(lambda t: hh(t)**2*s/(mp.sqrt(1 + hh(t)**2)*mp.sqrt(h0**2 + (1 + h0**2)*hh(t)**2)), [0, mp.pi/2])
    def integ(t):
        h = hh(t); r = mp.sqrt((1 + h**2)*(h0**2 + (1 + h0**2)*h**2))
        return (1 + h**2)*(1 + h0**2)*h**2/(r*((1 + h**2)*h0**2 + r*h0*mp.cos(t)))
    return Om, 1/h0 - mp.quad(integ, [0, mp.pi/2])
kappa_exact = mp.gamma(mp.mpf(3)/4)**4/mp.pi
CT = 6/mp.pi**3
# Richardson: Omega*a = kappa + c1*Omega + c2*Omega^2 ...  from three small h0
sm = [holo(h) for h in ['0.001', '0.002', '0.004']]
Oa = [O*a for O, a in sm]; Os = [O for O, a in sm]
M = mp.matrix([[1, O, O**2] for O in Os]); coef = mp.lu_solve(M, mp.matrix(Oa))
print('kappa (extrapolated) =', mp.nstr(coef[0], 15), '  closed form Gamma(3/4)^4/pi =', mp.nstr(kappa_exact, 15))
print('kappa/C_T =', mp.nstr(kappa_exact/CT, 12), '   linear coefficient (a0) =', mp.nstr(coef[1], 6))
h0s = [mp.mpf(10)**(mp.mpf(k)/40) for k in range(-100, 101)]
pts = [holo(h) for h in h0s]
u = [mp.mpf(0)] + [mp.tan(O/4)**2 for O, a in pts] + [mp.mpf(1)]
F = [kappa_exact/4] + [mp.tan(O/4)*a for O, a in pts] + [mp.mpf(0)]
sl = [(F[i+1] - F[i])/(u[i+1] - u[i]) for i in range(len(u) - 1)]
sdd = [(sl[i+1] - sl[i])/((u[i+2] - u[i])/2) for i in range(len(sl) - 1)]
mn = min(sdd); maxF = max(abs(x) for x in F)
print('holographic CC incl. F(0) and F(1): min sdd =', mp.nstr(mn, 8), ' max F =', mp.nstr(maxF, 6), ' pass =', bool(mn >= -1e-8*maxF))
# control, as first written: kappa RAISED 1% -- it did NOT fire, and it can't: a higher endpoint keeps a convex F convex.
# That was a control designed in the wrong direction (CC bounds kappa from BELOW). Kept for the record; the live
# control is kappa LOWERED 1%, which must fail.
F2 = [F[0]*mp.mpf('1.01')] + F[1:]
F3 = [F[0]*mp.mpf('0.99')] + F[1:]
sl2 = [(F2[i+1] - F2[i])/(u[i+1] - u[i]) for i in range(len(u) - 1)]
mn2 = min((sl2[i+1] - sl2[i])/((u[i+2] - u[i])/2) for i in range(len(sl2) - 1))
print('control kappa*1.01 at the node (wrong-direction control): min sdd =', mp.nstr(mn2, 6), ' fails =', bool(mn2 < -1e-8*maxF))
sl3 = [(F3[i+1] - F3[i])/(u[i+1] - u[i]) for i in range(len(u) - 1)]
mn3 = min((sl3[i+1] - sl3[i])/((u[i+2] - u[i])/2) for i in range(len(sl3) - 1))
print('control kappa*0.99 at the node (live control): min sdd =', mp.nstr(mn3, 6), ' fails =', bool(mn3 < -1e-8*maxF))
json.dump(dict(kappa_extrap=str(coef[0]), kappa_exact=str(kappa_exact), a0_linear=str(coef[1]),
               min_sdd=str(mn), maxF=str(maxF), passes=bool(mn >= -1e-8*maxF), control_up_min_sdd=str(mn2), control_down_min_sdd=str(mn3)),
          open('../results/v7d_holo_F0.json', 'w'), indent=1)
