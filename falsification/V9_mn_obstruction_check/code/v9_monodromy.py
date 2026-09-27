"""V9 -- monodromy traces of z'' = r(x) z along quantum's loops (inputs: base point, centres, radii, from its row
JSONs), with the bridge's own r and its own integrator (RK4 at mp.dps=30, step-halving convergence check).
Numerical corroboration, NOT an interval certificate."""
import sys, json, time, sympy as sp, mpmath as mp
from v9_nve import axial_r, x
mp.mp.dps = 30

def make_r(M, a_, beta, E, mu2):
    ax = axial_r(M, a_, beta, E, mu2)
    return sp.lambdify(x, ax['r'], modules='mpmath')

def rk4_path(rf, pts, Y, n):
    for z0, z1 in zip(pts[:-1], pts[1:]):
        dz = (z1 - z0)/n; z = z0
        for _ in range(n):
            def F(zz, Y): return [Y[1], rf(zz)*Y[0]]
            k1 = F(z, Y); k2 = F(z + dz/2, [Y[i] + dz/2*k1[i] for i in range(2)])
            k3 = F(z + dz/2, [Y[i] + dz/2*k2[i] for i in range(2)]); k4 = F(z + dz, [Y[i] + dz*k3[i] for i in range(2)])
            Y = [Y[i] + dz/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(2)]; z = z + dz
    return Y

def loop_pts(base, c, rho, ccw=True):
    base, c = mp.mpc(base), mp.mpc(c); phi0 = mp.arg(base - c); s = 1 if ccw else -1
    circ = [c + rho*mp.expj(phi0 + s*2*mp.pi*j/16) for j in range(17)]
    return [base] + circ + [base]

def monodromy(rf, pts, n):
    c1 = rk4_path(rf, pts, [mp.mpc(1), mp.mpc(0)], n); c2 = rk4_path(rf, pts, [mp.mpc(0), mp.mpc(1)], n)
    return mp.matrix([[c1[0], c2[0]], [c1[1], c2[1]]])

def parse(gs):   # "g[1.8415-0.0000j, rad 0.3832]*g[0.5805+0.2051j, rad 0.1231]"
    out = []
    for part in gs.split('*'):
        cc, rr = part.strip()[2:-1].split(', rad ')
        out.append((complex(cc.replace(' ', '')), float(rr)))
    return out

def nearest_located(c, located):
    return min((complex(s.strip('()')) for s in located), key=lambda z: abs(z - c))

if __name__ == '__main__':
    rows = {6: ('p1', 5, 3, sp.Rational(1, 5), 4), 7: ('p1', 5, 3, sp.Rational(1, 5), 9),
            8: ('p2', 13, 5, sp.Rational(-1, 3), 4), 9: ('p2', 13, 5, sp.Rational(-1, 3), 9)}
    which = [int(a) for a in sys.argv[1:]] or [6, 7, 8, 9]
    out = {}
    for i in which:
        tag, M, a_, beta, mu2 = rows[i]
        q = json.load(open(f'/Users/sumit/Github/quantum/qsim/mr_mn_row_{i}.json'))['forms']['r_xi1']
        rf = make_r(M, a_, beta, 1, mu2); base = complex(q['base'].strip('()'))
        loops = {}
        def U(c, rho, n):
            key = (c, rho, n)
            if key not in loops: loops[key] = monodromy(rf, loop_pts(base, c, rho), n)
            return loops[key]
        res = {}
        for n in (80, 160):
            gl = [(nearest_located(c, q['located']), rho) for c, rho in parse(q['g'])]
            hl = [(nearest_located(c, q['located']), rho) for c, rho in parse(q['h'])]
            Ug = [U(c, rho, n) for c, rho in gl]; Uh = [U(c, rho, n) for c, rho in hl]
            prod = lambda L: L[0] if len(L) == 1 else L[0]*L[1]
            prodrev = lambda L: L[0] if len(L) == 1 else L[1]*L[0]
            g, h, g2, h2 = prod(Ug), prod(Uh), prodrev(Ug), prodrev(Uh)
            comm = lambda G, H: mp.trace(G*H*mp.inverse(G)*mp.inverse(H))
            res[n] = dict(tr_g=complex(mp.trace(g)), tr_h=complex(mp.trace(h)), tr_comm_AB=complex(comm(g, h)), tr_comm_BA=complex(comm(g2, h2)),
                          det=[complex(mp.det(Ux)) for Ux in Ug + Uh])
        out[i] = dict(spec=(tag, 1, mu2), quantum=dict(tr_g=q['tr_g'], tr_h=q['tr_h'], tr_comm=q['tr_comm']), bridge=res)
        print(f'row {i} {tag} mu2={mu2}')
        for n in res: print(f'   n={n}: tr g={res[n]["tr_g"]:.8g}  tr h={res[n]["tr_h"]:.8g}  tr[g,h] (AB)={res[n]["tr_comm_AB"]:.6g}  (BA)={res[n]["tr_comm_BA"]:.6g}  |det-1|max={max(abs(d-1) for d in res[n]["det"]):.1e}')
        print(f'   quantum: tr g={q["tr_g"][:40]}  tr h={q["tr_h"][:40]}  tr[g,h]={q["tr_comm"][:48]}'); sys.stdout.flush()
    json.dump(out, open('../results/v9_traces_' + '_'.join(map(str, which)) + '.json', 'w'), indent=1, default=str)
