"""V17 (PREREGISTRATION.md): which Kerr Killing tensors survive a first-order deformation G = G0 + beta G1?
The bridge's own code: V9 MN transcription, V10 truncated series + Poisson-bracket jet operator (linear in G), and two
formulations computed side by side:
  (A) explicit Kerr basis p_t^i p_phi^j H0^k K^l + jet-level solvability of E0 k1 = -E1 jet(F0);
  (B) joint kernel nullity([[E0,0],[E1,E0]]) - nullity(E0).
All matrix-vector products split the vector into 16-bit halves so int64 never overflows (cf. ansatz's §141 lesson)."""
import sys, os, json, time, itertools, resource
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../V10_ts2_jet_bound/code'))
sys.path.insert(0, os.path.join(HERE, '../../V9_mn_obstruction_check/code'))
import v10_jet as J
import v10_mn as JM
import v9_nve as V9
from v10_jet import TPS, monos, trivial, X, Y

PRIMES = (2**31 - 1, 2**31 - 19)

def set_prime(q):
    J.Q = q; J.INV2 = pow(2, q - 2, q); JM.Q = q

def Q(): return J.Q

# ---------------------------------------------------------------- metric pieces (symbolic, then series)
bsym, Msym, asym = sp.symbols('beta_s M_s a_s')

def mn_g(M, a, beta):
    F = V9.mn_functions(M, a, beta); f, om, e2g, k = F['f'], F['om'], F['e2g'], F['k']
    x, y = V9.x, V9.y
    g = dict(g_TT=-f, g_Tphi=f*om, g_phiphi=-f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2),
             g_xx=k**2/f*e2g*(x**2 - y**2)/(x**2 - 1), g_yy=k**2/f*e2g*(x**2 - y**2)/(1 - y**2))
    return {kk: v.subs({x: X, y: Y}) for kk, v in g.items()}

KEYS = ('g_TT', 'g_Tphi', 'g_phiphi', 'g_xx', 'g_yy')

def g0_and_h(M, a, kind):
    """g0 = Kerr (MN at beta=0); h = d g/d(param) at the base point. kind in {'beta','M','a'}."""
    if kind == 'beta':
        g = mn_g(M, a, bsym); g0 = {k: v.subs(bsym, 0) for k, v in g.items()}
        h = {k: sp.diff(v, bsym).subs(bsym, 0) for k, v in g.items()}
    elif kind == 'M':
        g = mn_g(Msym, a, 0); g0 = {k: v.subs(Msym, M) for k, v in g.items()}
        h = {k: sp.diff(v, Msym).subs(Msym, M) for k, v in g.items()}
    elif kind == 'a':
        g = mn_g(M, asym, 0); g0 = {k: v.subs(asym, a) for k, v in g.items()}
        h = {k: sp.diff(v, asym).subs(asym, a) for k, v in g.items()}
    else: raise ValueError(kind)
    return g0, h

def series(exprs, P, T):
    ev = JM.Evaluator(P, T, 2); ev.collect_N(list(exprs.values()))
    return {k: ev.ev(sp.sympify(v)) for k, v in exprs.items()}

def mm(T, a, b): return T.mul(a, b)

def inv_metric(gs, T):
    q = Q(); tt, tp, pp, xx, yy = (gs[k] for k in KEYS)
    det = (mm(T, tt, pp) - mm(T, tp, tp)) % q; idet = T.inv(det)
    return {(0, 0): mm(T, pp, idet), (0, 1): (-mm(T, tp, idet)) % q, (1, 0): (-mm(T, tp, idet)) % q,
            (1, 1): mm(T, tt, idet), (2, 2): T.inv(xx), (3, 3): T.inv(yy)}

def first_order_inverse(G0, hs, T):
    """G1 = -G0 h G0 (blocks: (t,phi) 2x2, xx, yy)."""
    q = Q(); H = {(0, 0): hs['g_TT'], (0, 1): hs['g_Tphi'], (1, 0): hs['g_Tphi'], (1, 1): hs['g_phiphi']}
    G1 = {}
    for i in (0, 1):
        for j in (0, 1):
            s = T.zero()
            for k in (0, 1):
                for l in (0, 1):
                    s = (s + mm(T, mm(T, G0[(i, k)], H[(k, l)]), G0[(l, j)])) % q
            G1[(i, j)] = (-s) % q
    G1[(2, 2)] = (-mm(T, mm(T, G0[(2, 2)], hs['g_xx']), G0[(2, 2)])) % q
    G1[(3, 3)] = (-mm(T, mm(T, G0[(3, 3)], hs['g_yy']), G0[(3, 3)])) % q
    return G1

# ---------------------------------------------------------------- momentum polynomials with series coefficients
class MP:
    def __init__(self, T, d=None): self.T = T; self.d = d or {}
    def add(self, o):
        q = Q(); r = dict(self.d)
        for m, c in o.d.items(): r[m] = (r.get(m, self.T.zero()) + c) % q
        return MP(self.T, r)
    def scale(self, s):  # s: series
        return MP(self.T, {m: mm(self.T, c, s) for m, c in self.d.items()})
    def mul(self, o):
        q = Q(); r = {}
        for m1, c1 in self.d.items():
            for m2, c2 in o.d.items():
                m = tuple(i + j for i, j in zip(m1, m2)); r[m] = (r.get(m, self.T.zero()) + mm(self.T, c1, c2)) % q
        return MP(self.T, r)

def unit(T, i):
    e = [0, 0, 0, 0]; e[i] = 1; return MP(T, {tuple(e): T.const(1)})

def hamiltonian(G, T):
    q = Q(); half = pow(2, q - 2, q); d = {}
    for (i, j), c in G.items():
        e = [0, 0, 0, 0]; e[i] += 1; e[j] += 1; m = tuple(e); d[m] = (d.get(m, T.zero()) + c * half) % q
    return MP(T, d)

def ser_y(P, T):
    s = T.const(J.modq(P[1])); s[0, 1] = 1; return s

def carter(G0, a, P, T):
    """K = (1-y^2) p_y^2 + (a(1-y^2) p_t + p_phi)^2/(1-y^2) - 2 a^2 y^2 H0."""
    q = Q(); y = ser_y(P, T); one = T.const(1)
    s = (one - mm(T, y, y)) % q; sinv = T.inv(s)
    py, pt, pf = unit(T, 3), unit(T, 0), unit(T, 1)
    t1 = py.mul(py).scale(s)
    lin = pt.scale(s * J.modq(a) % q).add(pf)
    t2 = lin.mul(lin).scale(sinv)
    t3 = hamiltonian(G0, T).scale(mm(T, y, y) * ((-2 * J.modq(sp.Rational(a)**2)) % q) % q)
    return t1.add(t2).add(t3)

def kerr_basis(G0, a, r, P, T):
    pt, pf, H0, K = unit(T, 0), unit(T, 1), hamiltonian(G0, T), carter(G0, a, P, T)
    one = MP(T, {(0, 0, 0, 0): T.const(1)})
    def pw(f, n):
        o = one
        for _ in range(n): o = o.mul(f)
        return o
    B, labels = [], []
    for l in range(r // 2 + 1):
        for k in range((r - 2 * l) // 2 + 1):
            rest = r - 2 * l - 2 * k
            for i in range(rest + 1):
                j = rest - i
                B.append(pw(pt, i).mul(pw(pf, j)).mul(pw(H0, k)).mul(pw(K, l))); labels.append((i, j, k, l))
    return B, labels

def jet_vector(F, r, N):
    al = monos(r); st = [(s, t) for s in range(N + 1) for t in range(N + 1 - s)]
    v = np.zeros(len(al) * len(st), dtype=np.int64); k = 0
    for a in al:
        c = F.d.get(a)
        for (s, t) in st:
            if c is not None: v[k] = int(c[s, t])
            k += 1
    for m in F.d:
        assert sum(m) == r, 'non-homogeneous polynomial'
    return v

def matvec(E, v):
    q = Q(); lo = v & 0xFFFF; hi = v >> 16
    a = (E.astype(np.int64) @ lo) % q; b = (E.astype(np.int64) @ hi) % q
    return (a + b * 65536) % q

def rank(A):
    return J.rank_mod(np.ascontiguousarray(A.astype(np.int32)))

def guard():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    st = os.statvfs('/System/Volumes/Data'); free = st.f_bavail * st.f_frsize / 1e9
    if rss > 3.0 or free < 5.0: raise SystemExit(f'GUARD: rss {rss:.2f} GB, disk free {free:.1f} GB')

# ---------------------------------------------------------------- the two formulations
def survivors(G0, G1, a, r, N, P, T, basis=None):
    E0 = J.build(G0, r, N, T); E1 = J.build(G1, r, N, T); guard()
    if basis is None: basis, _ = kerr_basis(G0, a, r, P, T)
    V = np.stack([jet_vector(F, r, N) for F in basis], axis=1)
    # gate: E0 annihilates every basis jet exactly
    gate = all(not np.any(matvec(E0, V[:, i])) for i in range(V.shape[1]))
    rk_basis = rank(V.T.copy())
    Bcols = np.stack([matvec(E1, V[:, i]) for i in range(V.shape[1])], axis=1)
    r0 = rank(E0.copy()); rA = rank(np.hstack([E0, Bcols]).astype(np.int64) % Q())
    SA = V.shape[1] - (rA - r0)
    R_, C_ = E0.shape; Jm = np.zeros((2 * R_, 2 * C_), dtype=np.int32)
    Jm[:R_, :C_] = E0; Jm[R_:, :C_] = E1; Jm[R_:, C_:] = E0; del E1
    guard(); rJ = rank(Jm); del Jm
    nul0 = C_ - r0; SB = (2 * C_ - rJ) - nul0
    return dict(r=r, N=N, P=[str(P[0]), str(P[1])], q=Q(), n_basis=V.shape[1], basis_rank=rk_basis, gate_E0_basis=gate,
                nullity_E0=nul0, S_A=SA, S_B=SB, floor=trivial(r))

def setup(case, M, a, P, N):
    """Returns (G0, G1, a_used) for case in {'mn','dM','da','null','sabotage'}."""
    T = TPS(N)
    kind = {'mn': 'beta', 'dM': 'M', 'da': 'a'}.get(case, 'beta')
    g0, h = g0_and_h(M, a, kind)
    G0 = inv_metric(series(g0, P, T), T)
    if case in ('mn', 'dM', 'da'):
        G1 = first_order_inverse(G0, series(h, P, T), T)
    elif case == 'null':        # G1 = -L_xi G0, xi = (x^3/3) d_x + y^2 d_y (no xy cross term)
        # amendment 3: L_xi differentiates G0, so build it one order higher and truncate (a derivative of a TPS(N)
        # loses its top order; the first run's false 'death' at r = 2 came from exactly that)
        T = TPS(N + 1); G0 = inv_metric(series(g0, P, T), T)
        q = Q(); x = T.const(J.modq(P[0])); x[1, 0] = 1; y = ser_y(P, T)
        xi_x = mm(T, mm(T, x, x), x) * pow(3, q - 2, q) % q; xi_y = mm(T, y, y)
        dxix, dyiy = T.du(xi_x), T.dv(xi_y)
        G1 = {}
        for kk, Gc in G0.items():
            lie = (mm(T, xi_x, T.du(Gc)) + mm(T, xi_y, T.dv(Gc))) % q
            if kk == (2, 2): lie = (lie - 2 * mm(T, Gc, dxix)) % q
            if kk == (3, 3): lie = (lie - 2 * mm(T, Gc, dyiy)) % q
            G1[kk] = (-lie) % q
        Tn = TPS(N); cut = lambda A: (A[:N + 1, :N + 1] * Tn.mask) % q
        G0 = {k: cut(v) for k, v in G0.items()}; G1 = {k: cut(v) for k, v in G1.items()}; T = Tn
    elif case == 'sabotage':    # x*y in the tt slot only
        x = T.const(J.modq(P[0])); x[1, 0] = 1; y = ser_y(P, T)
        G1 = {kk: T.zero() for kk in G0}; G1[(0, 0)] = mm(T, x, y)
    else: raise ValueError(case)
    return G0, G1, T

PARAMS = {'p1': (5, 3), 'p2': (13, 5)}
POINTS = {'PA': (sp.Rational(3, 2), sp.Rational(1, 3)), 'PB': (sp.Integer(2), sp.Rational(-1, 4))}
KERR_COUNT = {1: 2, 2: 5, 3: 8, 4: 14, 5: 20, 6: 30}

def exactness_gate(case, M, a, P, N):
    """Amendment 3 gate: the G0, G1 series used at order N equal the truncation of the order-(N+1) series."""
    A0, A1, _ = setup(case, M, a, P, N); B0, B1, Tb = setup(case, M, a, P, N + 1)
    cut = lambda X_: X_[:N + 1, :N + 1] * TPS(N).mask
    return all(np.array_equal(A0[k] % Q(), cut(B0[k]) % Q()) and np.array_equal(A1[k] % Q(), cut(B1[k]) % Q()) for k in A0)

def run(case, pname, ptname, r, N, qi, asign=+1):
    set_prime(PRIMES[qi]); M, a = PARAMS[pname]; P = POINTS[ptname]
    t0 = time.time(); G0, G1, T = setup(case, M, a, P, N)
    d = survivors(G0, G1, asign * a, r, N, P, T)
    d.update(case=case, params=pname, point=ptname, asign=asign, kerr_count=KERR_COUNT[r], secs=round(time.time() - t0, 1))
    return d

if __name__ == '__main__':
    out = open(os.path.join(HERE, '../results/v17_runs.jsonl'), 'a')
    def log(d): print(json.dumps(d), flush=True); out.write(json.dumps(d) + '\n'); out.flush()
    mode = sys.argv[1]
    if mode == 'sign':          # C0 part 1: which sign of a makes Carter a Kerr Killing tensor in this chart
        for s in (+1, -1): log(run('dM', 'p1', 'PA', 2, 3, 0, s))
    else:
        case, pname, ptname, r, N, qi, s = sys.argv[1:8]
        log(run(case, pname, ptname, int(r), int(N), int(qi), int(s)))
