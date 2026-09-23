"""V8a -- exact vacuum re-check at fresh random rational points (bridge's own Ricci code), plus the equatorial
evenness. Metric depends on (x, y) only. Derivatives of components taken symbolically, then evaluated exactly;
Christoffels and Ricci assembled from the numbers. Control: a 3% bump of g_xx must break it."""
import sympy as sp, random, itertools, sys
ns = {}; exec(open('v8_nve.py').read().split("def zv():")[0], ns)
x, y, load = ns['x'], ns['y'], ns['load']
def ricci_max(g, pt, bump=False):
    M = sp.Matrix([[g['g_TT'], 0, 0, g['g_Tphi']], [0, g['g_xx']*(1 + (sp.Rational(3, 100)*x*y if bump else 0)), 0, 0],
                   [0, 0, g['g_yy'], 0], [g['g_Tphi'], 0, 0, g['g_phiphi']]])
    X = [None, x, y, None]
    def d(e, i): return sp.Integer(0) if X[i] is None else sp.diff(e, X[i])
    M0 = M.subs(pt); Mi = M0.inv()
    dM = [[[d(M[a, b], k).subs(pt) for k in range(4)] for b in range(4)] for a in range(4)]
    ddM = [[[[d(d(M[a, b], k), l).subs(pt) for l in range(4)] for k in range(4)] for b in range(4)] for a in range(4)]
    # Gamma^a_bc and its derivatives d_k Gamma^a_bc = d_k(g^ad) Gamma_dbc + g^ad d_k Gamma_dbc ; d_k g^ad = -g^ae d_k g_ef g^fd
    Gl = [[[(dM[dd][b][c] + dM[dd][c][b] - dM[b][c][dd])/2 for c in range(4)] for b in range(4)] for dd in range(4)]
    dGl = [[[[(ddM[dd][b][c][k] + ddM[dd][c][b][k] - ddM[b][c][dd][k])/2 for k in range(4)] for c in range(4)] for b in range(4)] for dd in range(4)]
    dMi = [[[-sum(Mi[a, e]*dM[e][f][k]*Mi[f, dd] for e in range(4) for f in range(4)) for k in range(4)] for dd in range(4)] for a in range(4)]
    G = [[[sum(Mi[a, dd]*Gl[dd][b][c] for dd in range(4)) for c in range(4)] for b in range(4)] for a in range(4)]
    dG = [[[[sum(dMi[a][dd][k]*Gl[dd][b][c] + Mi[a, dd]*dGl[dd][b][c][k] for dd in range(4)) for k in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    worst = 0
    for b, c in itertools.product(range(4), range(4)):
        Rbc = sum(dG[a][b][c][a] - dG[a][b][a][c] for a in range(4)) + sum(G[a][a][e]*G[e][b][c] - G[a][c][e]*G[e][b][a] for a in range(4) for e in range(4))
        worst = max(worst, abs(sp.nsimplify(Rbc)))
    return worst
random.seed(2026_09_24)
for fn in ['ts2_metric_components_t1o2.txt', 'ts2_metric_components_t1o3.txt']:
    g = load(fn)
    ev = all(sp.cancel(sp.together(g[k] - g[k].subs(y, -y))) == 0 for k in ['g_TT', 'g_Tphi', 'g_phiphi', 'g_xx', 'g_yy'])
    res = []
    for _ in range(3):
        pt = {x: sp.Rational(random.randint(1500, 5000), 1000), y: sp.Rational(random.randint(-700, 700), 1000)}
        res.append(ricci_max(g, pt))
    ctrl = ricci_max(g, {x: sp.Rational(2), y: sp.Rational(1, 3)}, bump=True)
    print(fn, ' even_in_y:', ev, '  max|R_ab| at 3 fresh points:', [str(r) for r in res], '  bump control |R|:', sp.N(ctrl, 4)); sys.stdout.flush()
