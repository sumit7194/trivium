"""V26 addendum A (B6): static class C seen from below, f0^- = z^2/(z^2 - 2Mz + q), via the Bridge's V25 return map."""
import os, sys, json, sympy as sp
V25 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../V25_only_kerr_checks/code'); sys.path.insert(0, V25)
_src = open(os.path.join(V25, 'v25_p3.py')).read().split('out = {}')[0]
_cwd = os.getcwd(); os.chdir(V25); exec(_src); os.chdir(_cwd)
HERE = os.path.dirname(os.path.abspath(__file__))
z = sp.symbols('z')
# exact check of the decomposition and of the ZV control
M, q = sp.symbols('M q')
fm = z**2/(z**2 - 2*M*z + q)
zv = sp.factor(fm.subs(q, M**2))
print('ZV delta=2 from below:', zv, flush=True)
out = dict(ZV_control=str(zv))
for label, z1, z2 in (('real roots q=3/4', 1.5, 0.5), ('complex roots q=5/4', 1 + 0.5j, 1 - 0.5j)):
    m1 = -z1**2/(z1 - z2); m2 = -z2**2/(z2 - z1)
    # exact identity check: 1 - m1/(z-z1) - m2/(z-z2) == z^2/(z^2-2z+q)
    qq = z1*z2; chk = sp.simplify((1 - sp.nsimplify(m1)/(z - sp.nsimplify(z1)) - sp.nsimplify(m2)/(z - sp.nsimplify(z2))) - z**2/(z**2 - 2*z + sp.nsimplify(qq)))
    print(label, 'm1, m2 =', m1, m2, '| decomposition exact:', chk == 0, flush=True)
    for E in (0.8, 0.6):
        out[f'{label} E={E}'] = case(z1, z2, m1, m2, E, sp.Integer(0), (0.3, 0.45), pred_F=1, label=f'{label} E={E} static')
    c2 = sp.diff(cref(z1, z2, m1, m2), z, 2)**2
    out[f'{label} E=0.8 CONTROL c_ref'] = case(z1, z2, m1, m2, 0.8, c2, (0.3, 0.45), pred_F=0, label=f'{label} E=0.8 CONTROL c_ref (F=0)')
json.dump(out, open(os.path.join(HERE, '../results/v26_B6.json'), 'w'), indent=1, default=str)
