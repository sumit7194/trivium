"""V10 -- the bridge's own jet-prolongation upper bound on the dimension of d_t, d_phi-invariant Killing tensors
(PREREGISTRATION.md). Independent of ansatz's _kt_jet.py: own metric handling, own truncated bivariate power series over
GF(q), own Poisson-bracket jet equations, own numpy elimination (no FLINT).

F = sum_{|alpha|=r} K_alpha(X, Y) p^alpha, momenta ordered (p_t, p_phi, p_X, p_Y).
{H, F} = g^XX p_X d_X F + g^YY p_Y d_Y F - 1/2 sum_ab d_X g^ab p_a p_b dF/dp_X - 1/2 sum_ab d_Y g^ab p_a p_b dF/dp_Y.
Jet system E_N: unknowns = Taylor coeffs of K_alpha at P to order N; equations = Taylor coeffs of each p^beta coefficient
of {H, F} to order N-1.  Bound = nullity_q(E_N) >= dim KT for N >= r (injectivity of the r-jet; rank_q <= rank_Q)."""
import sys, json, time, itertools, numpy as np, sympy as sp
sys.path.insert(0, '../../V8_ts2_obstruction_check/code')
Q = 2147483647
INV2 = pow(2, Q - 2, Q)

def modq(v):
    v = sp.Rational(v); n, d = int(v.p), int(v.q)
    assert d % Q != 0, 'prime divides a denominator'
    return n % Q * pow(d % Q, Q - 2, Q) % Q

class TPS:
    """Truncated power series in (u, v) = (X - X0, Y - Y0) to total order N, coefficients mod Q."""
    def __init__(self, N): self.N = N; self.mask = np.add.outer(np.arange(N + 1), np.arange(N + 1)) <= N
    def zero(self): return np.zeros((self.N + 1, self.N + 1), dtype=np.int64)
    def const(self, c): a = self.zero(); a[0, 0] = c % Q; return a
    def mul(self, a, b):
        N = self.N; c = self.zero()
        for i, j in zip(*np.nonzero(a)):
            c[i:, j:] = (c[i:, j:] + int(a[i, j]) * b[:N + 1 - i, :N + 1 - j]) % Q
        c[~self.mask] = 0; return c
    def inv(self, a):
        a00 = int(a[0, 0]); assert a00 % Q != 0, 'series not invertible at the point'
        i00 = pow(a00, Q - 2, Q); e = a * i00 % Q; e[0, 0] = 0; ne = (-e) % Q
        s = self.const(1); term = self.const(1)
        for _ in range(self.N): term = self.mul(term, ne); s = (s + term) % Q
        return s * i00 % Q
    def pow(self, a, n):
        if n < 0: return self.inv(self.pow(a, -n))
        r = self.const(1); b = a
        while n:
            if n & 1: r = self.mul(r, b)
            n >>= 1
            if n: b = self.mul(b, b)
        return r
    def du(self, a): c = self.zero(); c[:-1, :] = a[1:, :] * np.arange(1, self.N + 1)[:, None] % Q; c[~self.mask] = 0; return c
    def dv(self, a): c = self.zero(); c[:, :-1] = a[:, 1:] * np.arange(1, self.N + 1)[None, :] % Q; c[~self.mask] = 0; return c

def evaluate(expr, X, Y, P, T):
    """Exact TPS of a sympy expression (rational in X, Y) at P = (X0, Y0)."""
    memo = {}
    base = {X: T.const(modq(P[0])), Y: T.const(modq(P[1]))}
    base[X][1, 0] = 1; base[Y][0, 1] = 1
    def ev(e):
        if e in memo: return memo[e]
        if e in base: r = base[e]
        elif e.is_Number: r = T.const(modq(e))
        elif e.is_Add:
            r = T.zero()
            for a in e.args: r = (r + ev(a)) % Q
        elif e.is_Mul:
            r = T.const(1)
            for a in e.args: r = T.mul(r, ev(a))
        elif e.is_Pow and e.exp.is_Integer: r = T.pow(ev(e.base), int(e.exp))
        else: raise ValueError(f'unsupported node {type(e)}: {str(e)[:80]}')
        memo[e] = r; return r
    return ev(sp.sympify(expr))

def inverse_metric(g, X, Y, P, T):
    tt, tp, pp, xx, yy = [evaluate(g[k], X, Y, P, T) for k in ('g_TT', 'g_Tphi', 'g_phiphi', 'g_xx', 'g_yy')]
    det = (T.mul(tt, pp) - T.mul(tp, tp)) % Q; idet = T.inv(det)
    return {(0, 0): T.mul(pp, idet), (0, 1): (-T.mul(tp, idet)) % Q, (1, 0): (-T.mul(tp, idet)) % Q,
            (1, 1): T.mul(tt, idet), (2, 2): T.inv(xx), (3, 3): T.inv(yy)}

def monos(d): return [a for a in itertools.product(range(d + 1), repeat=4) if sum(a) == d]

def build(G, r, N, T):
    al = monos(r); be = monos(r + 1); bidx = {b: i for i, b in enumerate(be)}
    st = [(s, t) for s in range(N + 1) for t in range(N + 1 - s)]; cidx = {(a, s, t): k for k, (a, (s, t)) in enumerate(itertools.product(al, st))}
    mn = [(m, n) for m in range(N) for n in range(N - m)]; ridx = {(b, m, n): k for k, (b, (m, n)) in enumerate(itertools.product(be, mn))}
    E = np.zeros((len(ridx), len(cidx)), dtype=np.int64)
    dG = {k: (T.du(v), T.dv(v)) for k, v in G.items()}
    def add(C, a, b, kind, fac):
        for (m, n) in mn:
            row = ridx[(b, m, n)]
            for s in range(m + 1):
                for t in range(n + 1):
                    c = int(C[m - s, n - t])
                    if not c: continue
                    if kind == 0: key, w = (a, s, t), 1
                    elif kind == 1: key, w = (a, s + 1, t), s + 1
                    else: key, w = (a, s, t + 1), t + 1
                    col = cidx[key]; E[row, col] = (E[row, col] + c * w % Q * fac) % Q
    e = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    plus = lambda a, *vs: tuple(x + sum(v[i] for v in vs) for i, x in enumerate(a))
    for a in al:
        add(G[(2, 2)], a, plus(a, e[2]), 1, 1)                       # g^XX p_X d_X F
        add(G[(3, 3)], a, plus(a, e[3]), 2, 1)                       # g^YY p_Y d_Y F
        for q_, k in ((2, 0), (3, 1)):                               # -1/2 d_q g^ab p_a p_b dF/dp_q
            if a[q_] == 0: continue
            am = tuple(x - (i == q_) for i, x in enumerate(a))
            for (i, j), d in dG.items():
                add(d[k], a, plus(am, e[i], e[j]), 0, (Q - INV2) * a[q_] % Q)
    return E

def rank_mod(A):
    A = A % Q; R, C = A.shape; r = 0
    for c in range(C):
        if r == R: break
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0: continue
        p = r + nz[0]
        if p != r: A[[r, p]] = A[[p, r]]
        A[r, c:] = A[r, c:] * pow(int(A[r, c]), Q - 2, Q) % Q
        idx = r + 1 + np.nonzero(A[r + 1:, c])[0]
        if idx.size: A[idx, c:] = (A[idx, c:] - np.outer(A[idx, c], A[r, c:])) % Q
        r += 1
    return r

def trivial(r): return sum(1 for a in range(r + 1) for b in range(r + 1 - a) if (r - a - b) % 2 == 0)

X, Y = sp.symbols('x y', real=True)
def metric(case):
    if case in ('ts35', 'ts45', 'zv'):
        V = {}; exec(open('../../V8_ts2_obstruction_check/code/v8_nve.py').read().split('def vacuum_check')[0], V)   # loader only, no V8 run
        g = V['zv']() if case == 'zv' else V['load']('ts2_metric_components_t1o2.txt' if case == 'ts35' else 'ts2_metric_components_t1o3.txt')
        return {k: g[k].subs({V['x']: X, V['y']: Y}) for k in ('g_TT', 'g_Tphi', 'g_phiphi', 'g_xx', 'g_yy')}
    if case == 'flat':
        return dict(g_TT=sp.Integer(-1), g_Tphi=sp.Integer(0), g_phiphi=X**2*(1 - Y**2), g_xx=sp.Integer(1), g_yy=X**2/(1 - Y**2))
    if case == 'kerr':
        M, a = sp.Integer(1), sp.Rational(1, 2); Sg = X**2 + a**2*Y**2; Dl = X**2 - 2*M*X + a**2
        return dict(g_TT=-(1 - 2*M*X/Sg), g_Tphi=-2*M*a*X*(1 - Y**2)/Sg,
                    g_phiphi=(X**2 + a**2 + 2*M*a**2*X*(1 - Y**2)/Sg)*(1 - Y**2), g_xx=Sg/Dl, g_yy=Sg/(1 - Y**2))

def bound(case, r, N, P):
    T = TPS(N); t0 = time.time()
    G = inverse_metric(metric(case), X, Y, P, T)
    E = build(G, r, N, T); t1 = time.time()
    rk = rank_mod(E); b = E.shape[1] - rk
    return dict(case=case, r=r, N=N, P=[str(P[0]), str(P[1])], shape=list(E.shape), rank=rk, bound=b, trivial=trivial(r),
                t_build=round(t1 - t0, 1), t_rank=round(time.time() - t1, 1))

if __name__ == '__main__':
    case, r, P0, P1 = sys.argv[1], int(sys.argv[2]), sp.Rational(sys.argv[3]), sp.Rational(sys.argv[4])
    Ns = [int(n) for n in sys.argv[5].split(',')] if len(sys.argv) > 5 else [r + 1, r + 2, r + 3]
    for N in Ns:
        res = bound(case, r, N, (P0, P1))
        flag = 'BUG (below trivial)' if res['bound'] < res['trivial'] else ('= trivial' if res['bound'] == res['trivial'] else '> trivial')
        print(json.dumps(res), flag, flush=True)
        with open('../results/v10_runs.jsonl', 'a') as f: f.write(json.dumps(res) + '\n')
        if res['bound'] <= res['trivial']: break
