"""V21 C1 + C2 (PREREGISTRATION.md): Bridge's V9 MN transcription vs Fable's Lemma 3 (axis f0) and Lemmas 1+2 (axis NVE)."""
import sys, os, json
import sympy as sp, mpmath as mp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../V9_mn_obstruction_check/code'))
from v9_nve import mn_functions, axial_r, x, y
mp.mp.dps = 40
PTS = [mp.mpf('1.2'), mp.mpf('1.84145'), mp.mpf('3.3'), mp.mpf('7.5'), mp.mpf('30'),
       mp.mpc('0.6', '0.2'), mp.mpc('0.31', '-0.45'), mp.mpc('-0.5', '0.7'), mp.mpc('0.9', '0.05')]
out = {}
for name, (M, a, b) in {'p1': (5, 3, sp.Rational(1, 5)), 'p2': (13, 5, sp.Rational(-1, 3))}.items():
    F = mn_functions(M, a, b); k = F['k']
    W = sp.exp(2*b/x**3); r = k*x + M
    f0 = W*(r**2 - 2*M*r + a**2)/(r**2 + a**2*W**2)
    fV9 = F['f'].subs(y, 1); omV9 = F['om'].subs(y, 1)
    fl = sp.lambdify(x, fV9, 'mpmath'); f0l = sp.lambdify(x, f0, 'mpmath'); oml = sp.lambdify(x, omV9, 'mpmath')
    c1 = max(abs(fl(p)/f0l(p) - 1) for p in PTS); om = max(abs(oml(p)) for p in PTS)
    rows = {'C1_f_maxrel': float(c1), 'C1_omega_max': float(om)}
    for (E, mu2) in [(1, 4), (1, 9), (sp.Rational(97, 100), 1)]:
        rr = axial_r(M, a, b, E, mu2)['r']
        P = E**2 - mu2*f0
        target = -sp.Rational(3, 16)*(sp.diff(P, x)/P)**2
        rl = sp.lambdify(x, rr, 'mpmath'); tl = sp.lambdify(x, target, 'mpmath')
        d = max(abs(rl(p)/tl(p) - 1) for p in PTS)
        rows[f'C2_E{E}_mu2{mu2}_maxrel'] = float(d)
    out[name] = rows; print(name, rows, flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../results/c12.json'), 'w'), indent=1)
