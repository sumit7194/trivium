"""V10-MN (addendum 4): the bridge's independent jet-prolongation bound for Manko-Novikov. Metric from the bridge's V9
transcription; exp/sqrt handled in the bridge's own truncated-series evaluator over GF(Q):
  sqrt(b): b(P) must be a rational square r0^2; series r0 (1+e)^(1/2), e = b/b(P) - 1 nilpotent.
  exp(g):  c = g(P) rational; exp(c) := t^(c N) with N = lcm of all such denominators (T = e^(1/N), transcendental);
           remainder sum_k (g-c)^k / k!.
Soundness: true matrix = specialisation of a matrix over Q(T) at a transcendental T, so rank_true = rank_Q(T) >= rank_q(t);
the reported bound can only be over-stated."""
import sys, json, time, random, math
import numpy as np, sympy as sp
from v10_jet import TPS, build, rank_mod, trivial, modq, Q, X, Y
sys.path.insert(0, '../../V9_mn_obstruction_check/code')
import v9_nve as V9

def mn_metric(M, a, beta):
    F = V9.mn_functions(M, a, beta); f, om, e2g, k = F['f'], F['om'], F['e2g'], F['k']
    x, y = V9.x, V9.y
    g = dict(g_TT=-f, g_Tphi=f*om, g_phiphi=-f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2),
             g_xx=k**2/f*e2g*(x**2 - y**2)/(x**2 - 1), g_yy=k**2/f*e2g*(x**2 - y**2)/(1 - y**2))
    return {kk: v.subs({x: X, y: Y}) for kk, v in g.items()}

class Evaluator:
    def __init__(self, P, T, t):
        self.P, self.T, self.t = P, T, t; self.memo = {}; self.N = None
        self.base = {X: T.const(modq(P[0])), Y: T.const(modq(P[1]))}
        self.base[X][1, 0] = 1; self.base[Y][0, 1] = 1
    def exact(self, e):
        v = sp.nsimplify(sp.simplify(e.subs({X: self.P[0], Y: self.P[1]})))
        assert v.is_Rational, f'not rational at the point: {v}'
        return sp.Rational(v)
    def collect_N(self, exprs):
        dens = [1]
        for ex in exprs:
            for node in sp.preorder_traversal(ex):
                if isinstance(node, sp.exp): dens.append(int(self.exact(node.args[0]).q))
        self.N = math.lcm(*dens)
        return self.N
    def tpow(self, cN):  # t^(c N), c N an integer (maybe negative)
        e = int(cN) % (Q - 1); return pow(self.t, e, Q)
    def sqrt_series(self, b):
        T = self.T; a0 = int(b[0, 0])
        ex = sp.nsimplify(sp.Rational(1))  # placeholder
        return a0
    def ev(self, e):
        if e in self.memo: return self.memo[e]
        T = self.T
        if e in self.base: r = self.base[e]
        elif e.is_Number: r = T.const(modq(e))
        elif e.is_Add:
            r = T.zero()
            for a in e.args: r = (r + self.ev(a)) % Q
        elif e.is_Mul:
            r = T.const(1)
            for a in e.args: r = T.mul(r, self.ev(a))
        elif isinstance(e, sp.exp):
            g = self.ev(e.args[0]); c = self.exact(e.args[0])
            assert int(g[0, 0]) == modq(c), 'exp argument constant mismatch'
            d = g.copy(); d[0, 0] = 0
            s = T.const(1); term = T.const(1)
            for k in range(1, T.N + 1):
                term = T.mul(term, d) * pow(k, Q - 2, Q) % Q; s = (s + term) % Q
            r = s * self.tpow(c * self.N) % Q
        elif e.is_Pow and e.exp.is_Rational:
            p, qq = int(e.exp.p), int(e.exp.q)
            b = self.ev(e.base)
            if qq == 1: r = T.pow(b, p)
            elif qq == 2:
                bv = self.exact(e.base); r0 = sp.sqrt(bv)
                assert r0.is_Rational, f'sqrt base not a rational square at the point: {bv}'
                assert int(b[0, 0]) == modq(bv)
                eser = (b * pow(int(b[0, 0]), Q - 2, Q)) % Q; eser[0, 0] = 0
                s = T.const(1); term = T.const(1)
                for k in range(1, T.N + 1):
                    term = T.mul(term, eser); s = (s + term * modq(sp.binomial(sp.Rational(1, 2), k))) % Q
                rt = s * modq(r0) % Q
                r = T.pow(rt, p)
            else: raise ValueError(f'exponent {e.exp}')
        else: raise ValueError(f'unsupported node {type(e)}: {str(e)[:80]}')
        self.memo[e] = r; return r

def inverse_metric_mn(g, P, T, t):
    ev = Evaluator(P, T, t); ev.collect_N(list(g.values()))
    tt, tp, pp, xx, yy = [ev.ev(sp.sympify(g[k])) for k in ('g_TT', 'g_Tphi', 'g_phiphi', 'g_xx', 'g_yy')]
    det = (T.mul(tt, pp) - T.mul(tp, tp)) % Q; idet = T.inv(det)
    G = {(0, 0): T.mul(pp, idet), (0, 1): (-T.mul(tp, idet)) % Q, (1, 0): (-T.mul(tp, idet)) % Q,
         (1, 1): T.mul(tt, idet), (2, 2): T.inv(xx), (3, 3): T.inv(yy)}
    return G, ev

def series_identities(g, P, T, t):
    """Gate 2: exp(g)exp(-g) = 1 and (sqrt b)^2 = b on every exp/sqrt node of the metric."""
    ev = Evaluator(P, T, t); ev.collect_N(list(g.values())); bad = 0; n = 0
    for ex in g.values():
        for node in sp.preorder_traversal(ex):
            if isinstance(node, sp.exp):
                a = node.args[0]; p1 = ev.ev(sp.exp(a)); p2 = ev.ev(sp.exp(-a, evaluate=False)) if False else None
                inv_ser = ev.ev(sp.Pow(sp.exp(a), -1))
                bad += int(np.any(T.mul(p1, inv_ser) % Q != T.const(1))); n += 1
            elif node.is_Pow and node.exp == sp.Rational(1, 2):
                s = ev.ev(node); bad += int(np.any(T.mul(s, s) != ev.ev(node.base))); n += 1
    return n, bad

def bound_mn(params, r, Nord, P, t):
    T = TPS(Nord); G, ev = inverse_metric_mn(mn_metric(*params), P, T, t)
    E = build(G, r, Nord, T); shape = list(E.shape); rk = rank_mod(E); del E
    return dict(params=[str(p) for p in params], r=r, N=Nord, P=[str(P[0]), str(P[1])], t=t, Nexp=ev.N, shape=shape,
                rank=rk, bound=shape[1] - rk, trivial=trivial(r))

if __name__ == '__main__':
    R_ = sp.Rational
    mode = sys.argv[1]
    PA, PB = (R_(3, 2), R_(1, 3)), (R_(2), R_(-1, 4))
    P1, P2, KERR = (5, 3, R_(1, 5)), (13, 5, R_(-1, 3)), (5, 3, R_(0))
    rng = random.Random(20261011); t1 = rng.randrange(2, Q - 1)
    out = open('../results/v10_mn_runs.jsonl', 'a')
    def log(d):
        print(json.dumps(d), '= trivial' if d['bound'] == d['trivial'] else ('> trivial' if d['bound'] > d['trivial'] else 'BUG < trivial'), flush=True)
        out.write(json.dumps(d) + '\n'); out.flush()
    if mode == 'gates':
        for r in (1, 2, 3, 4): log(bound_mn(KERR, r, r + 1, PA, t1))
        for params in (P1, P2):
            for P in (PA, PB):
                n, bad = series_identities(mn_metric(*params), P, TPS(6), t1); print('series identities', params, P, n, 'nodes,', bad, 'failures', flush=True)
    else:
        params = P1 if mode == 'p1' else P2
        for P in (PA, PB):
            for r in range(1, 11):
                d = bound_mn(params, r, r + 1, P, t1)
                if d['bound'] > d['trivial']:
                    log(d); t2 = random.Random(7 + r).randrange(2, Q - 1); d = bound_mn(params, r, r + 2, P, t2)
                log(d)
