"""V13 periodic-orbit search on the section Σ = {y = 0, p_y > 0}, coordinates (x, p_x) (prereg §5, A7).
P^n is computed with v13_orbit at rtol 1e-13 in the BASE domain (so a periodic orbit can be found even if it later
proves to leave D). Newton on P^n(z) - z = 0 uses the exact variational Jacobian (v13_var). Every converged orbit is
then:
  - checked for area preservation, det DP^n = 1 to 1e-5 (a numerical sanity gate), and classified by its trace:
    |tr| < 2 elliptic, |tr| > 2 hyperbolic;
  - re-integrated for n returns in the B9 domain, with WHOLE-orbit-in-D recorded, plus its minimum x - 1 and R
    along the returns;
  - deduplicated across periods and seeds (orbit points within 1e-6).
Usage: python v13_upo.py <point> <E> <ell> <nmax> <seed-grid nx> <seed-grid np>"""
import sys, os, json, math, subprocess
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from v13_orbit import make
from v13_geometry import Point
from v13_screen import POINTS, RES
from v13_var import make_var
RT = 1e-13

class SectionMap:
    def __init__(self, M, a_, beta, E, Lz):
        self.base = make(M, a_, beta, sp.nsimplify(E), sp.nsimplify(Lz), domain='base')
        self.b9 = make(M, a_, beta, sp.nsimplify(E), sp.nsimplify(Lz), domain='B9')
        self.sj = make_var(M, a_, beta, sp.nsimplify(E), sp.nsimplify(Lz))
    def P(self, x, px, n, b9=False):
        integ = (self.b9 if b9 else self.base)[0]
        oc, nc, tau, drift, steps, sec = integ(x, px, n, RT, RT*1e-3, 1e9, 50_000_000)
        if nc < n: return None, sec[:nc], oc
        return np.array([sec[n - 1, 0], sec[n - 1, 1]]), sec[:nc], oc
    def jac(self, z, n):
        """Exact variational Jacobian of P^n on (x, p_x) (v13_var); replaces the finite-difference version, which lost
        area preservation on strongly hyperbolic orbits."""
        _, J = self.sj(float(z[0]), float(z[1]), n)
        return J

def newton(S, z0, n, it=30, tol=1e-11):
    z = np.array(z0, float)
    for _ in range(it):
        Pz, _, _ = S.P(*z, n)
        if Pz is None: return None
        F = Pz - z
        if np.max(np.abs(F)) < tol: return z
        J = S.jac(z, n)
        if J is None: return None
        try: dz = np.linalg.solve(J - np.eye(2), -F)
        except np.linalg.LinAlgError: return None
        lam = 1.0
        while lam > 1e-3:
            zn = z + lam*dz; Pn, _, _ = S.P(*zn, n)
            if Pn is not None and np.max(np.abs(Pn - zn)) < np.max(np.abs(F)): break
            lam *= 0.5
        z = zn
    return None

def minimal_period(S, z, n):
    for m in range(1, n):
        if n % m == 0:
            Pm, _, _ = S.P(*z, m)
            if Pm is not None and np.max(np.abs(Pm - z)) < 1e-8: return m
    return n

if __name__ == '__main__':
    pt, E, ell, nmax, nx, npx = sys.argv[1], sp.nsimplify(sys.argv[2]), sp.nsimplify(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    M, a_, beta = POINTS[pt]; S = SectionMap(M, a_, beta, E, ell*sp.nsimplify(M)); G = Point(pt)
    comps = [c for c in G.bounded(float(E), float(ell), 1.0 + 1e-9) if not c['nan_edge'] and c['hi'] - c['lo'] > 0.05]
    found = []
    for c in comps:
        for x0 in np.linspace(c['lo'], c['hi'], nx + 2)[1:-1]:
            q = S.base[4](x0, 0.0); rest = -1.0 - q[6]
            if not (rest > 0 and q[0] > 0): continue
            pm = math.sqrt(rest/q[0])
            for px0 in np.linspace(-0.95*pm, 0.95*pm, npx):
                for n in range(1, nmax + 1):
                    z = newton(S, (x0, px0), n)
                    if z is None: continue
                    m = minimal_period(S, z, n)
                    if any(f['period'] == m and min(np.hypot(*(np.array(p) - z)) for p in f['points']) < 1e-6 for f in found): continue
                    J = S.jac(z, m); tr, det = float(np.trace(J)), float(np.linalg.det(J))
                    pts = [z.tolist()]; zz = z.copy()
                    for _ in range(m - 1):
                        zz, _, _ = S.P(*zz, 1); pts.append(zz.tolist())
                    _, secb9, oc9 = S.P(*z, m, b9=True)
                    in_D = len(secb9) >= m
                    ev = np.linalg.eigvals(J); vecs = np.linalg.eig(J)[1]
                    rec = dict(period=m, points=pts, trace=tr, det=det, area_ok=abs(det - 1) < 1e-5,
                               type='hyperbolic' if abs(tr) > 2 else 'elliptic', eigvals=[complex(v).__repr__() for v in ev],
                               eigvecs=[[complex(v).__repr__() for v in col] for col in vecs.T], whole_orbit_in_D=bool(in_D),
                               min_xm1=min(p[0] - 1 for p in pts), min_R=min(math.sqrt(p[0]**2 - 1) for p in pts))
                    found.append(rec); print(m, rec['type'], [round(v, 6) for v in z], 'tr', round(tr, 4), 'det-1', f'{det-1:.1e}', 'inD', in_D, flush=True)
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=HERE).stdout.strip()
    json.dump(dict(point=pt, E=str(E), ell=str(ell), nmax=nmax, grid=(nx, npx), commit=commit, upos=found),
              open(os.path.join(RES, f'v13_upo_{pt}_{E}_{ell}.json'.replace('/', 'o')), 'w'), indent=1)
