"""V26 addendum D: tr(g_in) on |z| = r for the invisible family (E = 0.8), reusing the V26-B8 model code."""
import os, sys, json, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v26_B8 import Model, kerr_funcs, kerr_family, base_state_kerr, integrate_path
HERE = os.path.dirname(os.path.abspath(__file__))

def trace_circle(E, k, r, rtol):
    f0, S2, cKpp = kerr_family(); m = Model(kerr_funcs(), E)
    Yb = base_state_kerr(S2, cKpp, k)
    Yc = integrate_path(m, [4.0, complex(r)], Yb, k, rtol, conly=True)
    Y0 = np.concatenate([Yc, np.eye(2, dtype=complex).ravel()])
    Y = integrate_path(m, [complex(r), ('circle', 0.0, r)], Y0, k, rtol)
    M = Y[3:].reshape(2, 2)
    return np.trace(M) - 2, abs(np.linalg.det(M) - 1), float(np.max(np.abs(Y[:3] - Yc)))

ref = {1e-3: -4.78512e-9, 1e-2: -4.79093e-7, 1/10: -4.85001e-5}
out = {}; ok = True
for k in (0.0, 1e-3, 1e-2, 1/30, 1/10):
    t13, d, c = trace_circle(0.8, k, 1.35, 1e-13); t11, _, _ = trace_circle(0.8, k, 1.35, 1e-11)
    t16, d16, c16 = trace_circle(0.8, k, 1.6, 1e-13)
    coef = (t13.real/k**2) if k else float('nan')
    rel = abs(t13.real - ref[k])/abs(ref[k]) if k in ref else float('nan')
    inv = abs(t16 - t13)
    gates = d <= 1e-10 and c <= 1e-9 and d16 <= 1e-10 and c16 <= 1e-9 and inv <= 1e-9
    if k == 0: good = abs(t13) <= 1e-9 and gates
    elif k in ref: good = rel <= 1e-2 and gates
    else: good = gates
    ok &= good
    out[k] = dict(tr_minus_2=str(t13), floor=abs(t13 - t11), coef=coef, rel_to_ansatz=rel, r16_diff=inv, det=d, c0ret=c, pass_=good)
    print('k %.4g | tr-2 %.6e%+.1ei (floor %.1e) | coef %.6e | rel to ansatz %.2e | |tr(1.6)-tr(1.35)| %.1e | det %.1e c0ret %.1e | %s'
          % (k, t13.real, t13.imag, abs(t13 - t11), coef, rel, inv, d, c, good), flush=True)
tB, dB, cB = trace_circle(0.8, 0.1, 2.5, 1e-13)
diff = abs(tB - (out[0.1] and complex(out[0.1]['tr_minus_2'])))
fires = diff > 1e-6
print('CONTROL r=2.5, k=0.1: tr-2 = %s, differs from r=1.35 by %.3e -> control fires: %s (det %.1e, c0ret %.1e)' % (tB, diff, fires, dB, cB))
ok &= fires
print('VERDICT D', 'PASS' if ok else 'FAIL')
json.dump(dict(rows={str(k): v for k, v in out.items()}, control=dict(tr_minus_2=str(tB), diff=diff, fires=fires), verdict=ok),
          open(os.path.join(HERE, '../results/v26_D.json'), 'w'), indent=1, default=str)
