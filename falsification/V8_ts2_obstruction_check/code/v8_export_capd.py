"""Export the bridge's own exact TS delta=2 NVE coefficients (V8 derivation) for quantum's CAPD third replay.
Form: the non-reduced xi1 equation in the t-chart, y'' + p_t y' + q_t y = 0, x = (t + 1/t)/2,
      p_t = x' p(x(t)) - x''/x',  q_t = x'^2 q(x(t))   (exactly as v8_hp.make_stepper / v8_ts_monodromy.coeffs).
p(x), q(x) come from v8_hp.rational_parts (exact sympy cancel in x); the t-composition is exact (sympy cancel in t).
One JSON per row in ../export_capd/, monomial format agreed with quantum: [[i], "n/d"] means "n/d" * t^i."""
import sys, os, json, subprocess, random
import sympy as sp, numpy as np
from v8_hp import rational_parts
from v8_ts_monodromy import ROWS, coeffs, x, FILES

t = sp.Symbol('t')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../export_capd')

def poly_monos(expr):
    P = sp.Poly(sp.expand(expr), t)
    return [[[int(m[0])], f'{sp.Rational(c).p}/{sp.Rational(c).q}'] for m, c in zip(P.monoms(), P.coeffs())]

def t_form(parts):
    (pn, pd), (qn, qd) = parts
    P = sp.Poly(pn, x).as_expr()/sp.Poly(pd, x).as_expr(); Q = sp.Poly(qn, x).as_expr()/sp.Poly(qd, x).as_expr()
    xt = (t + 1/t)/2; x1 = sp.diff(xt, t); x2 = sp.diff(xt, t, 2)
    pt = sp.cancel(sp.together(x1*P.subs(x, xt) - x2/x1)); qt = sp.cancel(sp.together(x1**2*Q.subs(x, xt)))
    return [sp.fraction(e) for e in (pt, qt)]

def commit():
    return subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); rows = [(a if a.startswith('C') else int(a)) for a in sys.argv[1:]] or list(range(6)) + [f'C{i}' for i in range(1, 9)]
    rng = random.Random(7)
    for row in rows:
        tag, (E, L, mu2), *_ = ROWS[row]
        E, L, mu2 = map(sp.Rational, (E, L, mu2))
        (pn, pdn), (qn, qdn) = t_form(rational_parts(tag, E, L, mu2))
        # self-check: 40-digit evaluation of V8's ORIGINAL (unsimplified) pc, qc composed with x(t), vs the exact export
        import mpmath as M
        M.mp.dps = 40
        pc, qc, _, _ = coeffs(tag, E, L, mu2)
        pcf = sp.lambdify(x, pc, 'mpmath'); qcf = sp.lambdify(x, qc, 'mpmath')
        fp = sp.lambdify(t, pn/pdn, 'mpmath'); fq = sp.lambdify(t, qn/qdn, 'mpmath'); worst = M.mpf(0)
        for _ in range(20):
            z = M.mpc(M.mpf(rng.uniform(0.3, 3)), M.mpf(rng.uniform(-3, 3)))
            xz = (z + 1/z)/2; x1 = (1 - 1/z**2)/2; x2 = 1/z**3
            ref_p = x1*pcf(xz) - x2/x1; ref_q = x1**2*qcf(xz)
            worst = max(worst, abs(fp(z)/ref_p - 1), abs(fq(z)/ref_q - 1))
        worst = float(worst)
        assert worst < 1e-25, (row, worst)
        sing = sorted({complex(r) for e in (pdn, qdn) for r in sp.Poly(e, t).nroots(n=30, maxsteps=200)}, key=lambda c: (c.real, c.imag))
        d = dict(family='ts2', row=str(row),
                 row_params=dict(tag=tag, metric_file=FILES[tag], E=str(E), L=str(L), mu2=str(mu2)),
                 var='t', chart='x = (t + 1/t)/2; equatorial TS delta=2 NVE (bridge V8 derivation from the sealed component file)',
                 form="Y' = [[0,1],[-q,-p]] Y, i.e. y'' + p y' + q y = 0 (non-reduced xi1 form, as V8 used to reproduce v2's traces)",
                 exps=[], p=dict(num=poly_monos(pn), den=poly_monos(pdn)), q=dict(num=poly_monos(qn), den=poly_monos(qdn)),
                 bad=[], singular_points_float=[[s.real, s.imag] for s in sing],
                 self_check=dict(vs='40-digit evaluation of V8 coeffs() unsimplified pc, qc composed with x(t)', points=20, max_rel_err=worst),
                 provenance=f'TheBridge falsification/V8_ts2_obstruction_check/code/v8_export_capd.py via v8_hp.rational_parts, commit {commit()}')
        json.dump(d, open(os.path.join(OUT, f'ts2_row_{row}.json'), 'w'), indent=1)
        print(row, tag, (str(E), str(L), str(mu2)), 'deg p', sp.Poly(pn, t).degree(), '/', sp.Poly(pdn, t).degree(),
              'deg q', sp.Poly(qn, t).degree(), '/', sp.Poly(qdn, t).degree(), 'selfcheck %.1e' % worst, 'nsing', len(sing), flush=True)
