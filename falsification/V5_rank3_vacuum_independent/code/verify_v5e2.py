"""V5e' — second-order jet count (adds L_X nabla Riem = 0). Registered AFTER V5e failed; see PREREGISTRATION."""
import sympy as sp
from verify import (X, N, G, metric, christoffel, riemann_up, killing_jet, a, xi, eta, t, s)

def kernel_2nd(g, point):
    Gm = christoffel(g); Rup = riemann_up(Gm)
    Rdn = [[[[sp.cancel(sum(g[i, e] * Rup[e][j][k][l] for e in range(N))) for l in range(N)]
             for k in range(N)] for j in range(N)] for i in range(N)]
    def nR(e, i, j, k, l):  # symbolic nabla_e R_ijkl
        v = sp.diff(Rdn[i][j][k][l], X[e])
        for f in range(N):
            v -= Gm[f][e][i]*Rdn[f][j][k][l] + Gm[f][e][j]*Rdn[i][f][k][l] + Gm[f][e][k]*Rdn[i][j][f][l] + Gm[f][e][l]*Rdn[i][j][k][f]
        return v
    idx4 = [(i, j, k, l) for i in range(N) for j in range(N) for k in range(N) for l in range(N)]
    dRs = {(e,)+q: nR(e, *q) for e in range(N) for q in idx4}          # symbolic
    sub = dict(point)
    Gp = [[[sp.nsimplify(Gm[i][j][k].subs(sub)) for k in range(N)] for j in range(N)] for i in range(N)]
    Rp = {q: sp.nsimplify(Rdn[q[0]][q[1]][q[2]][q[3]].subs(sub)) for q in idx4}
    dRp = {q: sp.nsimplify(sp.simplify(v).subs(sub)) for q, v in dRs.items()}
    # nabla_f nabla_e R_ijkl at the point
    def ddR(f, e, i, j, k, l):
        v = sp.nsimplify(sp.diff(dRs[(e, i, j, k, l)], X[f]).subs(sub))
        for g_ in range(N):
            v -= (Gp[g_][f][e]*dRp[(g_, i, j, k, l)] + Gp[g_][f][i]*dRp[(e, g_, j, k, l)] + Gp[g_][f][j]*dRp[(e, i, g_, k, l)]
                  + Gp[g_][f][k]*dRp[(e, i, j, g_, l)] + Gp[g_][f][l]*dRp[(e, i, j, k, g_)])
        return v
    gp = g.subs(sub); gip = gp.inv()
    xs = sp.symbols('X0:4'); ws = sp.symbols('w0:6')
    pairs = [(i, j) for i in range(N) for j in range(i+1, N)]
    om = sp.zeros(N, N)
    for n_, (i, j) in enumerate(pairs): om[i, j] = ws[n_]; om[j, i] = -ws[n_]
    W = [[sum(gip[e, b]*om[i, b] for b in range(N)) for e in range(N)] for i in range(N)]
    eqs = []
    for (i, j, k, l) in idx4:   # first order: L_X Riem
        eqs.append(sp.expand(sum(xs[e]*dRp[(e, i, j, k, l)] for e in range(N))
            + sum(Rp[(e, j, k, l)]*W[i][e] + Rp[(i, e, k, l)]*W[j][e] + Rp[(i, j, e, l)]*W[k][e] + Rp[(i, j, k, e)]*W[l][e] for e in range(N))))
    for e0 in range(N):         # second order: L_X nabla Riem
        for (i, j, k, l) in idx4:
            q = sum(xs[f]*ddR(f, e0, i, j, k, l) for f in range(N))
            q += sum(dRp[(g_, i, j, k, l)]*W[e0][g_] + dRp[(e0, g_, j, k, l)]*W[i][g_] + dRp[(e0, i, g_, k, l)]*W[j][g_]
                     + dRp[(e0, i, j, g_, l)]*W[k][g_] + dRp[(e0, i, j, k, g_)]*W[l][g_] for g_ in range(N))
            eqs.append(sp.expand(q))
    unk = list(xs) + list(ws)
    M = sp.Matrix([[sp.diff(q, u) for u in unk] for q in eqs])
    return len(unk) - M.rank(), M, Gm

if __name__ == "__main__":
    point = {a: 3, xi: 2, eta: 1, t: 0, s: 0}
    k, M, Gm = kernel_2nd(G, point)
    ok = k == 2
    for idx in (0, 1):
        Xup, nab = killing_jet(G, Gm, idx, point)
        pairs = [(i, j) for i in range(N) for j in range(i+1, N)]
        vec = sp.Matrix(Xup + [nab[i, j] for (i, j) in pairs])
        ok &= sp.simplify(M*vec) == sp.zeros(M.rows, 1)
    kflat, _, _ = kernel_2nd(metric(sp.Integer(0)), {xi: 2, eta: 1, t: 0, s: 0})
    print(f"V5e' second-order kernel dim = {k}  (d_t, d_s in kernel: {ok if k == 2 else 'checked'});  flat control = {kflat} (must be 10)")
    print("V5e':", "PASS -- dim K1 = 2 (upper 2, lower 2)" if ok and kflat == 10 else f"NOT ESTABLISHED -- bound {k}")
