"""V5 — independent check of high_rank_killing EXP-002, from the object alone.

Imports NOTHING from any sibling repo. Run with any python that has sympy (the conjecture_machine venv is
used only as an interpreter — a VENV edge, not a code edge).

Gates (frozen in ../PREREGISTRATION.md):
  V5a signature (1,3)   V5b Ricci-flat   V5c {H,F}=0   V5d pure part != 0   V5e dim K1 = 2
Controls, each of which must behave as stated or the gate it guards is worthless:
  poison-b  a non-harmonic g_tt        -> Ricci must be NONZERO
  poison-c  F with one sign flipped    -> {H,F} must be NONZERO
  pos-e     d_t, d_s                   -> their 1-jets must lie IN the kernel
  flat-e    a = 0 (flat space)         -> the jet count must return 10, not 2
"""
import sympy as sp

t, s, xi, eta = sp.symbols('t s xi eta', real=True)
a = sp.symbols('a', real=True, nonzero=True)
X = [t, s, xi, eta]
pt, ps, pxi, peta = sp.symbols('p_t p_s p_xi p_eta')
P = [pt, ps, pxi, peta]
rho2 = xi**2 + eta**2
N = 4


def metric(gtt):
    g = sp.zeros(4, 4)
    g[0, 0] = gtt
    g[0, 1] = g[1, 0] = 1
    g[2, 2] = g[3, 3] = 8 * rho2
    return g


G = metric(-4 * a * xi / rho2)
F = (eta * pxi - xi * peta) * (pxi**2 + peta**2) / (32 * rho2) \
    + (a * ps**2 / rho2) * (xi * eta * pxi + sp.Rational(1, 2) * (eta**2 - xi**2) * peta)


def christoffel(g):
    gi = g.inv()
    return [[[sp.simplify(sum(gi[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j])
                                          - sp.diff(g[j, k], X[l])) for l in range(N)) / 2)
              for k in range(N)] for j in range(N)] for i in range(N)]


def riemann_up(Gm):
    # R^i_{jkl}
    R = [[[[0] * N for _ in range(N)] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    R[i][j][k][l] = sp.simplify(
                        sp.diff(Gm[i][l][j], X[k]) - sp.diff(Gm[i][k][j], X[l])
                        + sum(Gm[i][k][m] * Gm[m][l][j] - Gm[i][l][m] * Gm[m][k][j] for m in range(N)))
    return R


def ricci(Rup):
    return sp.Matrix(N, N, lambda j, l: sp.simplify(sum(Rup[i][j][i][l] for i in range(N))))


def poisson(H_, F_):
    return sp.simplify(sum(sp.diff(H_, X[i]) * sp.diff(F_, P[i]) - sp.diff(H_, P[i]) * sp.diff(F_, X[i])
                           for i in range(N)))


def hamiltonian(g):
    gi = g.inv()
    return sp.Rational(1, 2) * sum(gi[i, j] * P[i] * P[j] for i in range(N) for j in range(N))


def jet_kernel_dim(g, point, use_gradR=True):
    """Upper bound on dim(Killing algebra): admissible 1-jets (X^e, omega_ab) at `point`
    satisfying L_X Riem = 0 (and L_X grad Riem = 0 if use_gradR)."""
    Gm = christoffel(g)
    Rup = riemann_up(Gm)
    # lower first index: R_{abcd} = g_{ae} R^e_{bcd}
    Rdn = [[[[sp.simplify(sum(g[i, e] * Rup[e][j][k][l] for e in range(N)))
              for l in range(N)] for k in range(N)] for j in range(N)] for i in range(N)]

    def nabla_R(e, i, j, k, l):
        v = sp.diff(Rdn[i][j][k][l], X[e])
        for f in range(N):
            v -= Gm[f][e][i] * Rdn[f][j][k][l] + Gm[f][e][j] * Rdn[i][f][k][l] \
                + Gm[f][e][k] * Rdn[i][j][f][l] + Gm[f][e][l] * Rdn[i][j][k][f]
        return v

    sub = dict(point)
    gp = g.subs(sub)
    gip = gp.inv()
    Rp = [[[[Rdn[i][j][k][l].subs(sub) for l in range(N)] for k in range(N)] for j in range(N)] for i in range(N)]
    dRp = [[[[[sp.nsimplify(sp.simplify(nabla_R(e, i, j, k, l)).subs(sub)) for l in range(N)]
              for k in range(N)] for j in range(N)] for i in range(N)] for e in range(N)] if use_gradR else None

    # unknowns: X^0..X^3, omega_ab for a<b (6)
    xs = sp.symbols('X0:4')
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    ws = sp.symbols('w0:6')
    omega = sp.zeros(N, N)
    for n_, (i, j) in enumerate(pairs):
        omega[i, j] = ws[n_]
        omega[j, i] = -ws[n_]
    # W_a^e = nabla_a X^e = g^{eb} omega_{ab}
    W = [[sum(gip[e, b] * omega[i, b] for b in range(N)) for e in range(N)] for i in range(N)]

    eqs = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    expr = sum(xs[e] * (dRp[e][i][j][k][l] if use_gradR else 0) for e in range(N)) if use_gradR else 0
                    if not use_gradR:
                        # need nabla R even for first-order condition
                        raise ValueError
                    expr += sum(Rp[e][j][k][l] * W[i][e] + Rp[i][e][k][l] * W[j][e]
                                + Rp[i][j][e][l] * W[k][e] + Rp[i][j][k][e] * W[l][e] for e in range(N))
                    eqs.append(sp.expand(expr))
    unknowns = list(xs) + list(ws)
    M = sp.Matrix([[sp.diff(q, u) for u in unknowns] for q in eqs])
    rank = M.rank()
    return len(unknowns) - rank, M, unknowns, gp, Gm


def killing_jet(g, Gm, vec_index, point):
    """Jet (X^e, omega_ab) of the coordinate Killing vector d_{vec_index}, evaluated at point."""
    sub = dict(point)
    Xup = [1 if e == vec_index else 0 for e in range(N)]
    Xdn = [sum(g[b, e] * Xup[e] for e in range(N)) for b in range(N)]
    nab = sp.Matrix(N, N, lambda i, b: sp.simplify(sp.diff(Xdn[b], X[i])
                                                    - sum(Gm[c][i][b] * Xdn[c] for c in range(N))))
    return [sp.nsimplify(v) for v in Xup], nab.subs(sub)


def report(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{('  ' + detail) if detail else ''}")
    return ok


if __name__ == "__main__":
    allok = True
    print("V5 — independent check of the rank-3 Lorentzian vacuum pp-wave\n")

    # V5a
    pt0 = {a: 3, xi: 2, eta: 1, t: 0, s: 0}
    ev = [complex(v).real for v in G.subs(pt0).evalf().eigenvals(multiple=True)]
    nneg = sum(1 for v in ev if v < 0)
    allok &= report("V5a signature (1,3)", nneg == 1, f"negative eigenvalues: {nneg}")

    # V5b + poison
    Gm = christoffel(G)
    Ric = ricci(riemann_up(Gm))
    allok &= report("V5b Ricci-flat", Ric == sp.zeros(4, 4))
    Gbad = metric(-4 * a * xi**2 / rho2)
    Ricbad = ricci(riemann_up(christoffel(Gbad)))
    allok &= report("  poison-b (non-harmonic g_tt) must be NON-flat", Ricbad != sp.zeros(4, 4))

    # V5c + poison
    H = hamiltonian(G)
    br = poisson(H, F)
    allok &= report("V5c {H,F} = 0", br == 0)
    Fbad = (eta * pxi - xi * peta) * (pxi**2 + peta**2) / (32 * rho2) \
        - (a * ps**2 / rho2) * (xi * eta * pxi + sp.Rational(1, 2) * (eta**2 - xi**2) * peta)
    allok &= report("  poison-c (one sign flipped) must be NONZERO", poisson(H, Fbad) != 0)

    # V5d
    pure = sp.simplify(F.subs({pt: 0, ps: 0}))
    allok &= report("V5d pure (p_xi,p_eta) part nonzero", pure != 0, f"F|pt=ps=0 = {pure}")

    # V5e: jet-count upper bound, with its controls
    point = {a: 3, xi: 2, eta: 1, t: 0, s: 0}
    k, M, unk, gp, _ = jet_kernel_dim(G, point)
    allok &= report("V5e dim K1 <= 2 (jet count at one point)", k == 2, f"kernel dim = {k}")
    for idx, nm in [(0, "d_t"), (1, "d_s")]:
        Xup, nab = killing_jet(G, Gm, idx, point)
        pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
        antisym = sp.simplify(nab + nab.T) == sp.zeros(4, 4)
        vec = sp.Matrix(Xup + [nab[i, j] for (i, j) in pairs])
        in_ker = sp.simplify(M * vec) == sp.zeros(M.rows, 1)
        allok &= report(f"  pos-e: {nm} is Killing and its jet lies in the kernel", antisym and in_ker)
    kflat, *_ = jet_kernel_dim(metric(sp.Integer(0)), {xi: 2, eta: 1, t: 0, s: 0})
    allok &= report("  flat-e: at a=0 (flat space) the count must return 10", kflat == 10, f"kernel dim = {kflat}")

    print("\nVERDICT:", "ALL GATES AND CONTROLS PASS -- irreducible in the polynomial sense, independently"
          if allok else "A GATE OR CONTROL FAILED -- see above; the claim is not confirmed by this route")
