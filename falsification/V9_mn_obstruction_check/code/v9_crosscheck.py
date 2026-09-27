"""Cross-check the bridge's MN transcription against ansatz's srepr components at random points (catches the
bridge's own transcription errors), and check omega = 0 on the axis (quantum's G1, re-done independently)."""
import sympy as sp, mpmath as mp, random
from sympy import Symbol, Integer, Rational, Mul, Add, Pow, exp, sqrt, Float
from v9_nve import mn_functions, axial_r, x, y
mp.mp.dps = 30
D = '/Users/sumit/Github/conjecture_machine/data/MN_for_quantum/'
def load(fn):
    out = {}
    for line in open(D + fn):
        if '=' in line and not line.startswith('#'):
            kk, v = line.split('=', 1)
            out[kk.strip()] = eval(v.strip(), {'Mul': Mul, 'Add': Add, 'Pow': Pow, 'Integer': Integer, 'Rational': Rational,
                                              'Symbol': Symbol, 'Float': Float, 'exp': exp, 'sqrt': sqrt, 'Half': sp.S.Half})
    return out
for fn, (M, a_, beta) in [('mn_metric_components_p1.txt', (5, 3, sp.Rational(1, 5))), ('mn_metric_components_p2.txt', (13, 5, sp.Rational(-1, 3)))]:
    comp = load(fn); keys = list(comp)
    F = mn_functions(M, a_, beta); k = F['k']
    mine = dict(g_tt=-F['f'], g_tphi=F['f']*F['om'], g_xx=k**2/F['f']*F['e2g']*(x**2 - y**2)/(x**2 - 1),
                g_yy=k**2/F['f']*F['e2g']*(x**2 - y**2)/(1 - y**2), g_phiphi=-F['f']*F['om']**2 + k**2/F['f']*(x**2 - 1)*(1 - y**2))
    random.seed(5); worst = {}
    for _ in range(3):
        X, Y = random.uniform(1.3, 4), random.uniform(-0.9, 0.9)
        for key in comp:
            sx = [s for s in comp[key].free_symbols if s.name == 'x'][0]; sy = [s for s in comp[key].free_symbols if s.name == 'y'][0]
            theirs = complex(sp.N(comp[key].subs({sx: X, sy: Y}), 25))
            mk = {'g_TT': 'g_tt', 'g_Tphi': 'g_tphi', 'g_tt': 'g_tt', 'g_tphi': 'g_tphi', 'g_xx': 'g_xx', 'g_yy': 'g_yy', 'g_phiphi': 'g_phiphi'}.get(key)
            if mk is None: continue
            ours = complex(sp.N(mine[mk].subs({x: X, y: Y}), 25))
            worst[key] = max(worst.get(key, 0), abs(ours - theirs)/max(1e-30, abs(theirs)))
    ax = axial_r(M, a_, beta, 1, 4)
    om_ax = [complex(sp.N(ax['omega_on_axis'].subs(x, X), 20)) for X in (1.7, 2.9, 0.6 + 0.3j)]
    print(fn, 'keys', keys, '\n  max rel diff (bridge vs ansatz srepr):', {k2: f'{v:.1e}' for k2, v in worst.items()}, '\n  omega on axis:', [f'{abs(v):.1e}' for v in om_ax])
