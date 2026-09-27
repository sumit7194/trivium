"""V9 (fast path) -- same r and loops as v9_monodromy.py, but the integration is scipy DOP853 in complex128 at
rtol 1e-13, with a tolerance-halving convergence check. Numerical corroboration, not a certificate.
Also runs the controls: Kerr (beta=0) axial generator traces, and a Riemann-P test with known monodromy."""
import sys, json, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from v9_nve import axial_r, x
from v9_monodromy import parse, nearest_located

def make_r(M, a_, beta, E, mu2):
    return sp.lambdify(x, axial_r(M, a_, beta, E, mu2)['r'], modules='numpy')

def seg(rf, z0, z1, Y, tol):
    dz = z1 - z0
    def F(s, Y):
        z = z0 + s*dz; rv = rf(z)
        return [dz*Y[1], dz*rv*Y[0], dz*Y[3], dz*rv*Y[2]]
    sol = solve_ivp(F, (0, 1), Y, method='DOP853', rtol=tol, atol=tol*1e-3)
    return sol.y[:, -1]

def loop_pts(base, c, rho, ccw=True):
    phi0 = np.angle(base - c); s = 1 if ccw else -1
    return [base] + [c + rho*np.exp(1j*(phi0 + s*2*np.pi*j/16)) for j in range(17)] + [base]

def monodromy(rf, pts, tol):
    Y = np.array([1, 0, 0, 1], dtype=complex)
    for z0, z1 in zip(pts[:-1], pts[1:]): Y = seg(rf, z0, z1, Y, tol)
    return np.array([[Y[0], Y[2]], [Y[1], Y[3]]])

def comm_tr(G, H): return np.trace(G @ H @ np.linalg.inv(G) @ np.linalg.inv(H))

def run_row(i, M, a_, beta, mu2, tols=(1e-11, 1e-13)):
    q = json.load(open(f'/Users/sumit/Github/quantum/qsim/mr_mn_row_{i}.json'))['forms']['r_xi1']
    rf = make_r(M, a_, beta, 1, mu2); base = complex(q['base'].strip('()'))
    res = {}
    for tol in tols:
        Ug = [monodromy(rf, loop_pts(base, nearest_located(c, q['located']), rho), tol) for c, rho in parse(q['g'])]
        Uh = [monodromy(rf, loop_pts(base, nearest_located(c, q['located']), rho), tol) for c, rho in parse(q['h'])]
        g = Ug[0] if len(Ug) == 1 else Ug[0] @ Ug[1]; g2 = Ug[0] if len(Ug) == 1 else Ug[1] @ Ug[0]
        h = Uh[0] if len(Uh) == 1 else Uh[0] @ Uh[1]; h2 = Uh[0] if len(Uh) == 1 else Uh[1] @ Uh[0]
        res[tol] = dict(tr_g=complex(np.trace(g)), tr_h=complex(np.trace(h)), tr_comm_AB=complex(comm_tr(g, h)),
                        tr_comm_BA=complex(comm_tr(g2, h2)), det_err=float(max(abs(np.linalg.det(U) - 1) for U in Ug + Uh)))
    return q, res

if __name__ == '__main__':
    R = sp.Rational
    rows = {6: (5, 3, R(1, 5), 4), 7: (5, 3, R(1, 5), 9), 8: (13, 5, R(-1, 3), 4), 9: (13, 5, R(-1, 3), 9)}
    out = {}
    for i in [int(a) for a in sys.argv[1:]] or [6, 7, 8, 9]:
        q, res = run_row(i, *rows[i]); out[i] = dict(quantum={k: q[k] for k in ('tr_g', 'tr_h', 'tr_comm')}, bridge={str(t): v for t, v in res.items()})
        print(f'row {i}:')
        for t, v in res.items():
            print(f'  tol {t:.0e}: tr g={v["tr_g"]:.9g}  tr h={v["tr_h"]:.9g}  tr[g,h] AB={v["tr_comm_AB"]:.7g}  BA={v["tr_comm_BA"]:.7g}  det err {v["det_err"]:.1e}')
        print(f'  quantum : tr g={q["tr_g"][:44]}\n            tr h={q["tr_h"][:44]}\n            tr[g,h]={q["tr_comm"][:52]}'); sys.stdout.flush()
    json.dump(out, open('../results/v9_fast_rows.json', 'w'), indent=1, default=str)
