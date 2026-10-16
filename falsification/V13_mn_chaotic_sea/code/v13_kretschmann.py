"""V13 independent check of tabula's ring-singularity claim (SpaceTime 1e13988): the Kretschmann scalar near the
equatorial B=0 point. The bridge's route differs from tabula's numeric mp.diff:
- the metric is the V9 transcription (v9_nve.mn_functions), not tabula's code;
- first and second metric derivatives are EXACT sympy derivatives, lambdified to mpmath (no finite differencing);
- Christoffel symbols, Riemann and K = R_abcd R^abcd are then assembled numerically at 60 digits.
Line element (prolate, Weyl–Papapetrou):
  ds^2 = -f (dt - w dphi)^2 + (k^2/f)[e^{2g}(x^2-y^2)(dx^2/(x^2-1) + dy^2/(1-y^2)) + (x^2-1)(1-y^2) dphi^2],
  with g_tphi = f w, as in V9 (gtp = f*om; om already includes the -4k al/(1-al^2) constant).
Validation: beta = 0 must reproduce Kerr's closed-form K at three points.
Usage: python v13_kretschmann.py"""
import sys, os, json, itertools
import sympy as sp, mpmath as M
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V9_mn_obstruction_check/code'))
from v9_nve import mn_functions, x, y
M.mp.dps = 60
R = sp.Rational

def metric(Mm, a_, beta):
    F = mn_functions(Mm, a_, beta); f, om, e2g, k = F['f'], F['om'], F['e2g'], F['k']
    gtt = -f; gtp = f*om; gpp = -f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2)
    gxx = k**2/f*e2g*(x**2 - y**2)/(x**2 - 1); gyy = k**2/f*e2g*(x**2 - y**2)/(1 - y**2)
    # coordinate order (t, x, y, phi)
    G = sp.zeros(4, 4); G[0, 0] = gtt; G[0, 3] = G[3, 0] = gtp; G[3, 3] = gpp; G[1, 1] = gxx; G[2, 2] = gyy
    return G, k

class Kret:
    def __init__(self, Mm, a_, beta):
        G, k = metric(Mm, a_, beta); self.k = k; X = (x, y)
        comps = [(0, 0), (0, 3), (3, 3), (1, 1), (2, 2)]
        self.f0 = {c: sp.lambdify((x, y), G[c], 'mpmath') for c in comps}
        self.f1 = {(c, i): sp.lambdify((x, y), sp.diff(G[c], X[i]), 'mpmath') for c in comps for i in range(2)}
        self.f2 = {(c, i, j): sp.lambdify((x, y), sp.diff(G[c], X[i], X[j]), 'mpmath')
                   for c in comps for i in range(2) for j in range(i, 2)}
    def K(self, xv, yv):
        xv, yv = M.mpf(xv), M.mpf(yv)
        g = M.zeros(4, 4); dg = [[M.zeros(4, 4) for _ in range(4)]][0]
        dg = [M.zeros(4, 4) for _ in range(4)]                     # dg[c][a,b] = d_c g_ab (c = coordinate index)
        ddg = [[M.zeros(4, 4) for _ in range(4)] for _ in range(4)]
        for (a, b), fn in self.f0.items():
            g[a, b] = g[b, a] = fn(xv, yv)
        for ((a, b), i), fn in self.f1.items():
            v = fn(xv, yv); dg[1 + i][a, b] = dg[1 + i][b, a] = v
        for ((a, b), i, j), fn in self.f2.items():
            v = fn(xv, yv)
            for (p, q) in ((1 + i, 1 + j), (1 + j, 1 + i)):
                ddg[p][q][a, b] = ddg[p][q][b, a] = v
        gi = g**-1
        n = range(4)
        # Christoffel of the first kind and its derivative: Gam_{abc} = 1/2 (d_b g_ac + d_c g_ab - d_a g_bc)
        Gam = [[[ (dg[b][a, c] + dg[c][a, b] - dg[a][b, c])/2 for c in n] for b in n] for a in n]
        dGam = [[[[ (ddg[d][b][a, c] + ddg[d][c][a, b] - ddg[d][a][b, c])/2 for c in n] for b in n] for a in n] for d in n]
        # Riemann (all lower): R_abcd = d_c Gam_{a b d} - d_d Gam_{a b c} + Gam^e_{bc} Gam_{e a d} - Gam^e_{bd} Gam_{e a c}
        Gup = [[[sum(gi[e, a]*Gam[a][b][c] for a in n) for c in n] for b in n] for e in n]
        Rl = {}
        for a, b, c, d in itertools.product(n, repeat=4):
            Rl[a, b, c, d] = (dGam[c][a][b][d] - dGam[d][a][b][c]
                              + sum(Gup[e][b][c]*Gam[e][a][d] - Gup[e][b][d]*Gam[e][a][c] for e in n))
        # raise all indices and contract
        Ku = M.mpf(0)
        for a, b, c, d in itertools.product(n, repeat=4):
            r = Rl[a, b, c, d]
            if r == 0: continue
            up = M.mpf(0)
            for p, q, s, t in itertools.product(n, repeat=4):
                w = gi[a, p]*gi[b, q]*gi[c, s]*gi[d, t]
                if w != 0: up += w*Rl[p, q, s, t]
            Ku += r*up
        return Ku

def kerr_closed(Mm, a_, xv, yv):
    k = M.sqrt(M.mpf(Mm)**2 - M.mpf(a_)**2); r = Mm + k*M.mpf(xv); c = M.mpf(yv); a = M.mpf(a_)
    r2, ac2 = r**2, a**2*c**2
    return 48*M.mpf(Mm)**2*(r2 - ac2)*((r2 + ac2)**2 - 16*r2*ac2)/(r2 + ac2)**6

if __name__ == '__main__':
    out = {}
    Kk = Kret(1, R(9, 10), 0)
    val = []
    for (xv, yv) in [(2.0, 0.3), (1.5, 0.7), (3.0, -0.2)]:
        num, ex = Kk.K(xv, yv), kerr_closed(1, R(9, 10), xv, yv)
        val.append(dict(x=xv, y=yv, K=M.nstr(num, 20), closed=M.nstr(ex, 20), rel=float(abs(num/ex - 1))))
        print('Kerr check', xv, yv, M.nstr(num, 15), M.nstr(ex, 15), float(abs(num/ex - 1)), flush=True)
    out['kerr_validation'] = val
    for name, (Mm, a_, beta, xs) in {'C0': (1, R(9, 10), R(19, 20)/(R(19, 100))**R(3, 2), '1.92982825852115'),
                                    'F5R': (89, 80, R(13394411, 1186380), '1.92192258791676')}.items():
        Km = Kret(Mm, a_, beta); xs = M.mpf(xs); rows = []
        for side in (+1, -1):
            for d in ('1e-2', '1e-3', '1e-4', '1e-5'):
                xv = xs + side*M.mpf(d); kv = Km.K(xv, 0)
                rows.append(dict(side=side, d=d, K=M.nstr(kv, 12)))
                print(name, 'side', side, 'd', d, 'K', M.nstr(kv, 8), flush=True)
        out[name] = dict(x_s=M.nstr(xs, 15), rows=rows)
    json.dump(out, open(os.path.join(HERE, '../results/v13_kretschmann.json'), 'w'), indent=1)
