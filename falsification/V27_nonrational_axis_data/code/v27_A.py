"""V27 A1-A3: exact checks of Neon T16 claims (Curzon hypergeometric reduction, trace identities, barrier examples)."""
import sympy as sp, mpmath as mp, random
z, w, x, at, u, tau, M = sp.symbols('z w x atilde u tau M')
ok = {}
# A1: NVE v'' + (3/16)(P'/P)^2 v = 0 with P = at - e^w, w -> x = e^w
q_w = sp.Rational(3, 16)*(sp.diff(at - sp.exp(w), w)/(at - sp.exp(w)))**2
q_w_x = sp.simplify(q_w.subs(sp.exp(w), x))
# v_ww = x^2 v_xx + x v_x  =>  v_xx + v_x/x + q_w/x^2 v = 0 ; claim q_w/x^2 = (3/16)/(x-at)^2
ok['A1_eq'] = sp.simplify(q_w_x/x**2 - sp.Rational(3, 16)/(x - at)**2) == 0
r = sp.symbols('r')
ok['A1_exp_inf'] = set(sp.solve(r*(r - 1) + r + sp.Rational(3, 16), r)) == {sp.I*sp.sqrt(3)/4, -sp.I*sp.sqrt(3)/4}
ok['A1_exp_at'] = set(sp.solve(r*(r - 1) + sp.Rational(3, 16), r)) == {sp.Rational(1, 4), sp.Rational(3, 4)}
# Curzon map: f0 = exp(-2M/z), w = -2M/z  -> exp(w)
ok['A1_curzon'] = sp.simplify(sp.exp(-2*M/z).subs(z, -2*M/w) - sp.exp(w)) == 0
# A2: trace identities
M0 = sp.Matrix([[1, 1], [0, 1]]); Ma = sp.Matrix([[u, -(1 + u**2)/tau], [tau, -u]])
ok['A2_param'] = sp.simplify(Ma.trace()) == 0 and sp.simplify(Ma.det() - 1) == 0 and sp.simplify((M0*Ma).trace() - tau) == 0
g = lambda k: M0**k*Ma*(M0**-k)
h1 = g(0)*g(1); h2 = g(0)*g(2)
comm = lambda A, B: A*B*A.inv()*B.inv()
t1 = sp.simplify(h1.trace()); t2 = sp.simplify(h2.trace()); tc = sp.simplify(comm(h1, h2).trace())
print('A2: tr h1 =', sp.factor(t1), '| tr h2 =', sp.factor(t2), '| tr[h1,h2]-2 =', sp.factor(tc - 2))
ok['A2_traces'] = sp.simplify(t1 + 2 + tau**2) == 0 and sp.simplify(t2 + 2 + 4*tau**2) == 0 and sp.simplify(tc - 2 + 4*tau**6) == 0
lam = sp.symbols('lam'); D = sp.diag(lam, 1/lam)
gd = lambda k: D**k*Ma*(D**-k); hd1 = gd(0)*gd(1); hd2 = gd(0)*gd(2)
ok['A2_control_diag_gives_2_FIRES_if_False'] = sp.simplify(comm(hd1, hd2).trace() - 2) == 0
print('A2 control (diag M0): tr[h1,h2]-2 =', sp.factor(sp.simplify(comm(hd1, hd2).trace() - 2)))
# A3: barrier examples (numeric at random complex points, 30 digits)
mp.mp.dps = 30
s3 = sp.sqrt(3)
P1 = sp.exp(z/s3)*sp.cot(z/2); Y = sp.sin(z); C = s3/2
res1 = sp.diff(Y, z, 2) - sp.Rational(3, 4)*sp.diff(Y, z)**2/Y + C + sp.Rational(3, 4)*(sp.diff(P1, z)/P1)**2*Y
def res2f(b):
    P2 = sp.sin(b*z)/sp.cosh(z); uu = b/4*sp.cot(b*z) + sp.Rational(3, 4)*sp.tanh(z)
    return sp.diff(uu, z) + uu**2 + sp.Rational(3, 16)*(sp.diff(P2, z)/P2)**2
f1 = sp.lambdify(z, res1, 'mpmath'); f2 = sp.lambdify(z, res2f(s3), 'mpmath'); f2c = sp.lambdify(z, res2f(sp.Rational(17, 10)), 'mpmath')
random.seed(1); pts = [mp.mpc(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(5)]
m1 = max(abs(f1(p)) for p in pts); m2 = max(abs(f2(p)) for p in pts); m2c = min(abs(f2c(p)) for p in pts)
print('A3: max residual D_inf example %.1e ; reducible example %.1e ; control (sqrt3 -> 1.7) min residual %.2e' % (m1, m2, m2c))
ok['A3_Dinf'] = m1 < 1e-25; ok['A3_red'] = m2 < 1e-25; ok['A3_control_fires'] = m2c > 1e-6
print(ok)
passed = all(v for k, v in ok.items() if 'control_diag' not in k) and ok['A2_control_diag_gives_2_FIRES_if_False'] is True
print('VERDICT V27-A', 'PASS' if passed else 'FAIL')
