"""V26 L-num (PREREGISTRATION.md, ccafd13): Ernst equation for xi = (1-e)/(1+e) solved order by order in 1/r,
xi = sum_n r^-(n+1) F_n(u), u = cos(theta), from upper-axis moments m_n = F_n(1). Exact Gaussian rationals.
Checks F_n(-1) = (-1)^n m_n (rule L: xi_- = -xi_+), and the two wrong guesses. Bridge code."""
import os, json, random, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
u = sp.symbols('u'); I = sp.I

def lap_coeff(F, n):
    """coefficient of r^-(n+3) in Laplacian of r^-(n+1) F(u): n(n+1)F + ((1-u^2)F')'."""
    return sp.expand(n*(n + 1)*F + sp.diff((1 - u**2)*sp.diff(F, u), u))

def solve(mx, my, N):
    """xi with axis moments mx, eta (= conj xi as an independent field) with moments my. Equations:
    (xi eta - 1) Lap xi = 2 eta (grad xi . grad xi), and the same with xi <-> eta."""
    Fx, Fy = [], []
    for n in range(N + 1):
        cx = sp.symbols('a0:%d' % (n + 1)); cy = sp.symbols('b0:%d' % (n + 1))
        Px = sum(c*u**k for k, c in enumerate(cx)); Py = sum(c*u**k for k, c in enumerate(cy))
        Fx.append(None); Fy.append(None)
        # assemble with symbols then solve
        r = sp.symbols('r', positive=True)
        X = sum(r**-(k + 1)*(Fx[k] if Fx[k] is not None else Px) for k in range(n + 1))
        Y = sum(r**-(k + 1)*(Fy[k] if Fy[k] is not None else Py) for k in range(n + 1))
        def eq(A, B):
            lap = sp.diff(r**2*sp.diff(A, r), r)/r**2 + sp.diff((1 - u**2)*sp.diff(A, u), u)/r**2
            grad2 = sp.diff(A, r)**2 + (1 - u**2)*sp.diff(A, u)**2/r**2
            return (A*B - 1)*lap - 2*B*grad2
        eqs = []
        for A, B in ((X, Y), (Y, X)):
            e = sp.expand(eq(A, B)*r**(n + 3))
            s = sp.expand(e.subs(r, 1/sp.Symbol('t')))
            t = sp.Symbol('t'); c0 = sp.expand(s).coeff(t, 0)
            eqs += sp.Poly(c0, u).all_coeffs() if c0 != 0 else []
        eqs += [Px.subs(u, 1) - mx[n], Py.subs(u, 1) - my[n]]
        sol = sp.solve(eqs, list(cx) + list(cy), dict=True)
        if len(sol) != 1: raise RuntimeError('order %d: %d solutions' % (n, len(sol)))
        Fx[-1] = sp.expand(Px.subs(sol[0])); Fy[-1] = sp.expand(Py.subs(sol[0]))
        if Fx[-1].free_symbols - {u} or Fy[-1].free_symbols - {u}: raise RuntimeError('order %d underdetermined' % n)
    return Fx, Fy

def run(seed, N, real=False):
    rng = random.Random(seed)
    mx = [sp.Rational(rng.randint(-9, 9), rng.randint(1, 5)) + (0 if real else I*sp.Rational(rng.randint(-9, 9), rng.randint(1, 5))) for _ in range(N + 1)]
    mx[0] = sp.Rational(1) + (0 if real else I*sp.Rational(rng.randint(-3, 3), 2))   # mass (+ NUT-like part allowed at the series level)
    my = [sp.conjugate(m) for m in mx]
    Fx, Fy = solve(mx, my, N)
    rows = []
    for n in range(N + 1):
        lo = sp.simplify(Fx[n].subs(u, -1))
        rows.append(dict(n=n, m=str(mx[n]), F_at_minus1=str(lo),
                         ruleL=bool(sp.simplify(lo - (-1)**n*mx[n]) == 0),
                         mirror_guess=bool(sp.simplify(lo - mx[n]) == 0),
                         conj_guess=bool(sp.simplify(lo + (-1)**n*sp.conjugate(mx[n])) == 0)))
    return dict(seed=seed, real=real, N=N, rows=rows,
                L_all=all(r['ruleL'] for r in rows),
                mirror_all=all(r['mirror_guess'] for r in rows), conj_all=all(r['conj_guess'] for r in rows))

if __name__ == '__main__':
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    out = []
    for seed, real in ((1, False), (2, False), (3, False), (4, True)):
        r = run(seed, N, real); out.append(r)
        print('seed', seed, 'real' if real else 'complex', '| rule L all orders:', r['L_all'],
              '| mirror guess all:', r['mirror_all'], '| conj guess all:', r['conj_all'], flush=True)
    json.dump(out, open(os.path.join(HERE, '../results/v26_L.json'), 'w'), indent=1)
