"""V7c -- the bridge's own LPs for the constants given CC at n = 1, plus the analytic bound (V7c2).
Constraint list as frozen by cuspis (a938baa); code written by the bridge without reading cuspis's.
  CC : F = tan(theta/4) a(theta) convex in u = tan^2(theta/4), with the node F(0) = kappa/4
  C2 : a >= 0, nonincreasing, convex in theta
  C3 : g = b tan(theta/2) nonincreasing, b = -a' at midpoints      (<=> a'' + a'/sin(theta) >= 0)
  C5 : a(pi) = 0
LP1: min kappa s.t. a(pi/2) = 1.      LP2: min kappa s.t. g(last midpoint) = 4 (sigma = 1); kappa/C_T = LP2 pi^2/24.
"""
import numpy as np, json, sympy as sp
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

def build(N, thmin, use_cc=True, use_c3=True):
    h = N//2
    th = np.concatenate([np.linspace(thmin, np.pi/2, h, endpoint=False), np.linspace(np.pi/2, np.pi, N - h)])
    i90 = h; assert abs(th[i90] - np.pi/2) < 1e-15
    nv = N + 1; K = N                       # a_0..a_{N-1}, kappa
    rows = []                               # each row: dict col->coef, meaning sum <= 0
    # C2
    for i in range(N): rows.append({i: -1.0})                                    # a >= 0
    for i in range(N-1): rows.append({i+1: 1.0, i: -1.0})                        # a_{i+1} <= a_i
    for i in range(1, N-1):                                                      # convex in theta
        d1 = th[i]-th[i-1]; d2 = th[i+1]-th[i]
        rows.append({i+1: -1/d2, i: 1/d2 + 1/d1, i-1: -1/d1})
    # C3
    mid = (th[1:] + th[:-1])/2; dth = np.diff(th); tq = np.tan(mid/2)
    # g_j = -(a_{j+1}-a_j)/dth_j * tq_j ;  g_{j+1} - g_j <= 0
    if use_c3:
        for j in range(N-2):
            # g_j = (a_j - a_{j+1}) tq_j/dth_j ;  g_{j+1} - g_j <= 0
            r = {j+2: -tq[j+1]/dth[j+1], j+1: tq[j+1]/dth[j+1] + tq[j]/dth[j], j: -tq[j]/dth[j]}
            rows.append(r)
    # CC
    if use_cc:
        uu = np.concatenate([[0.0], np.tan(th/4)**2]); t4 = np.tan(th/4)
        def Fcoef(k):   # node k: 0 -> kappa/4 ; k>=1 -> tan(th/4) a_{k-1}
            return {K: 0.25} if k == 0 else {k-1: t4[k-1]}
        for k in range(1, len(uu)-1):
            x0, x1, x2 = uu[k-1], uu[k], uu[k+1]
            r = {}
            for node, w in [(k+1, -1/(x2-x1)), (k, 1/(x2-x1) + 1/(x1-x0)), (k-1, -1/(x1-x0))]:
                for col, c in Fcoef(node).items(): r[col] = r.get(col, 0) + w*c
            rows.append(r)
    A = lil_matrix((len(rows), nv))
    for m, r in enumerate(rows):
        for col, c in r.items(): A[m, col] = c
    return th, i90, mid, dth, tq, A.tocsr(), nv, K

def solve(N, thmin, which, use_cc=True):
    th, i90, mid, dth, tq, A, nv, K = build(N, thmin, use_cc)
    c = np.zeros(nv); c[K] = 1.0
    Aeq = lil_matrix((2, nv)); beq = np.zeros(2)
    Aeq[0, N-1] = 1.0                                        # C5: a(pi) = 0
    if which == 1: Aeq[1, i90] = 1.0; beq[1] = 1.0
    else:           Aeq[1, N-1] = -tq[-1]/dth[-1]; Aeq[1, N-2] = tq[-1]/dth[-1]; beq[1] = 4.0
    bounds = [(None, None)]*N + [(0, None)]
    r = linprog(c, A_ub=A, b_ub=np.zeros(A.shape[0]), A_eq=Aeq.tocsr(), b_eq=beq, bounds=bounds, method='highs')
    return r.fun if r.status == 0 else ('status', r.status, r.message)

out = {'LP1': {}, 'LP2_kappa_over_CT': {}, 'noCC': {}}
for thmin in [1e-3, 1e-4]:
    for N in [200, 400, 800, 1600, 3200]:
        v1 = solve(N, thmin, 1); v2 = solve(N, thmin, 2)
        out['LP1'][f'{thmin:g}/{N}'] = v1
        out['LP2_kappa_over_CT'][f'{thmin:g}/{N}'] = v2*np.pi**2/24 if not isinstance(v2, tuple) else v2
        print(f'thmin={thmin:g} N={N:5d}  LP1={v1:.6f}  LP2 kappa/C_T={v2*np.pi**2/24:.6f}')
for N in [400, 1600]:
    out['noCC'][N] = (solve(N, 1e-3, 1, use_cc=False), solve(N, 1e-3, 2, use_cc=False))
print('no-CC control (LP1, LP2):', out['noCC'])

# V7c2: analytic bound, bridge's derivation.  tau = tan(theta/4) = sqrt(u).
tau, a, g, Cp = sp.symbols('tau a g Cp', positive=True)
A_ = sp.Function('A')
# F - u F'(u) = tau a/2 - tau^2 a_tau/2 ; a_tau = -b dtheta/dtau, dtheta/dtau = 4/(1+tau^2), b = g cot(theta/2) = g (1-tau^2)/(2 tau)
b_ = g*(1 - tau**2)/(2*tau)
intercept = tau*a/2 + tau**2*(b_*4/(1 + tau**2))/2
print('intercept - [tau a/2 + g tau(1-tau^2)/(1+tau^2)] =', sp.simplify(intercept - (tau*a/2 + g*tau*(1-tau**2)/(1+tau**2))))
# with g >= g_inf = 4 sigma and a >= 8 sigma log(1/sin(theta/2)) = 8 sigma log((1+tau^2)/(2 tau)):
phi = tau*(sp.log((1 + tau**2)/(2*tau)) + (1 - tau**2)/(1 + tau**2))
lower = sp.simplify(intercept.subs({g: 4, a: 8*sp.log((1 + tau**2)/(2*tau))}) - 4*phi)
print('lower-bound intercept (sigma = 1) - 4 phi =', lower)
tstar = sp.nsolve(sp.diff(phi, tau), tau, 0.37); phistar = phi.subs(tau, tstar)
print('tau* =', sp.N(tstar, 12), ' theta* (deg) =', sp.N(4*sp.atan(tstar)*180/sp.pi, 8), ' phi* =', sp.N(phistar, 12))
print('kappa >= 16 sigma phi*  ->  kappa/C_T >=', sp.N(16*phistar*sp.pi**2/24, 10),
      ';  kappa/a(pi/2) >= 4 phi*/ln 2 =', sp.N(4*phistar/sp.log(2), 10), ' (needs theta* <= pi/2:', bool(tstar < sp.tan(sp.pi/8)), ')')
out['analytic'] = dict(tau_star=float(tstar), phi_star=float(phistar), kappa_over_CT=float(16*phistar*sp.pi**2/24),
                       kappa_over_a90=float(4*phistar/sp.log(2)))
json.dump(out, open('../results/v7c_lp.json', 'w'), indent=1, default=str)

# Control added before looking at it: CC on, C3 off -> LP1 must fall to the chord floor 2 (cuspis EXP-025b H4).
def solve_noc3(N, thmin):
    th, i90, mid, dth, tq, A, nv, K = build(N, thmin, True, use_c3=False)
    c = np.zeros(nv); c[K] = 1.0
    Aeq = lil_matrix((2, nv)); Aeq[0, N-1] = 1.0; Aeq[1, i90] = 1.0
    r = linprog(c, A_ub=A, b_ub=np.zeros(A.shape[0]), A_eq=Aeq.tocsr(), b_eq=[0, 1], bounds=[(None, None)]*N + [(0, None)], method='highs')
    return r.fun
out['CC_without_C3_LP1'] = {N: solve_noc3(N, 1e-3) for N in [400, 1600]}
print('control CC without C3, LP1 (expect chord 2):', out['CC_without_C3_LP1'])
json.dump(out, open('../results/v7c_lp.json', 'w'), indent=1, default=str)
