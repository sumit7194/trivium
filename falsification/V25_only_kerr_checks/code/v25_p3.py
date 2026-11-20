"""V25 P3 (closed-form residue sweep) and P4(iii) (invisible family) with R-trunc. Bridge code only."""
import os, json, math, cmath, numpy as np, sympy as sp
from v25_rmap import Axis, make_trunc, return_map
HERE = os.path.dirname(os.path.abspath(__file__)); z = sp.symbols('z')
def case(z1, z2, m1, m2, E, c2sq, radii, pred_F=None, predA=None, label=''):
    ax = Axis(z1, z2, m1, m2, E)
    f0 = 1 - sp.nsimplify(m1)/(z - sp.nsimplify(z1)) - sp.nsimplify(m2)/(z - sp.nsimplify(z2))
    U, dU, U0, U2 = make_trunc(f0, c2sq, z, sp.nsimplify(E))
    r = return_map(ax, U, dU, U0, z1, radii, U2fun=U2)[(1, 0)]
    dl = z1 - z2
    if predA is None: predA = [-3j*math.pi*m2*pred_F/(5*dl), 6j*math.pi*m2*pred_F/(5*dl)]
    A = r['A']; tol_zero = 100*r['floor']
    err = max(abs(A[i] - predA[i]) for i in (0, 1)); scale = max(abs(p) for p in predA)
    ok = err <= max(100*r['floor'], 1e-6*scale)
    void = r['floor'] > 1e-4 or max(r['ve1_check']) > 1e-8
    rec = dict(label=label, A=[str(complex(round(a.real, 9), round(a.imag, 9))) for a in A], pred=[str(complex(round(p.real, 9), round(p.imag, 9))) for p in predA],
               err=err, floor=r['floor'], verdict='VOID' if void else ('MATCH' if ok else 'MISMATCH'), diag={k: v for k, v in r.items() if k != 'A'})
    print(label, '| A', rec['A'], '| pred', rec['pred'], '| err %.2e floor %.2e ve1 %.1e' % (err, r['floor'], max(r['ve1_check'])), rec['verdict'], flush=True)
    return rec
I = sp.I
def cref(z1, z2, m1, m2): return I*(sp.nsimplify(m1)/(z - sp.nsimplify(z1)) - sp.nsimplify(m2)/(z - sp.nsimplify(z2)))
out = {}
# Kerr M=1 a=3/5, E=4/5, twist lambda c_ref
a = 0.6; K1 = (1j*a, -1j*a, 1.0, 1.0)
for lam in (0, 0.5, 1, 1.5):
    c2 = (sp.nsimplify(lam)*sp.diff(cref(*K1), z, 2))**2
    out[f'kerr_lam{lam}'] = case(*K1, 0.8, c2, (0.3, 0.45), pred_F=1 - lam**2, label=f'Kerr a=0.6 E=0.8 lambda={lam}')
out['kerr_E0.7'] = case(*K1, 0.7, sp.Integer(0), (0.3, 0.45), pred_F=1, label='Kerr a=0.6 E=0.7 static twin')
out['kerr_a0.8_E1.3'] = case(0.8j, -0.8j, 1.0, 1.0, 1.3, sp.Integer(0), (0.4, 0.6), pred_F=1, label='Kerr a=0.8 E=1.3 static twin (unbound)')
NUT = (0.5j, -0.5j, 1 - 0.4j, 1 + 0.4j)
for lam in (0, 0.7):
    c2 = (sp.nsimplify(lam)*sp.diff(cref(*NUT), z, 2))**2
    out[f'nut_lam{lam}'] = case(*NUT, 0.7, c2, (0.2, 0.35), pred_F=1 - lam**2, label=f'Kerr-NUT type E=0.7 lambda={lam}')
RP = (1.0, -0.5, 0.75, 0.5)
out['real_c0'] = case(*RP, 0.6, sp.Integer(0), (0.4, 0.6), pred_F=1, label='real poles static')
c0 = sp.Rational(1, 2)/(z - 1) - sp.Rational(1, 2)/(z + sp.Rational(1, 2))
out['real_twist'] = case(*RP, 0.6, sp.diff(c0, z, 2)**2, (0.4, 0.6), pred_F=1 + 0.25/0.5625, label='real poles, real twist (F=13/9)')
out['real_ref'] = case(*RP, 0.6, sp.diff(cref(*RP), z, 2)**2, (0.4, 0.6), pred_F=0, label='real poles, complexified reference twist (F=0)')
# P4(iii): Kerr f0 with (c0'')^2 = (cK'')^2 + Q/D^3
v = (z + I*sp.nsimplify(a))/(z - I*sp.nsimplify(a)); D = z**2 + sp.nsimplify(a)**2; cK2 = sp.diff(cref(*K1), z, 2)**2
Q1 = sp.Rational(1, 3)*(v**3 + v**-3 - sp.Rational(3, 5)*(v + 1/v) - sp.Rational(4, 5)); Q2 = sp.Rational(1, 3)*(v**3 + v**-3)
out['P4iii_Q1'] = case(*K1, 0.8, cK2 + Q1/D**3, (0.3, 0.45), predA=[0j, 0j], label='P4(iii) Q1 (invisible family member)')
out['P4iii_Q2'] = case(*K1, 0.8, cK2 + Q2/D**3, (0.3, 0.45), predA=[-math.pi/24 + 0j, math.pi/12 + 0j], label='P4(iii) Q2 (non-admissible)')
json.dump(out, open(os.path.join(HERE, '../results/v25_p3_A1.json'), 'w'), indent=1, default=str)
