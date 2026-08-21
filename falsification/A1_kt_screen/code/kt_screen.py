"""A1 — numerical conserved-quantity screen on ZV geodesics.
Gates frozen in ../PREREGISTRATION.md before this file was written.

Counts independent combinations  sum_i c_i(x,y) * m_i(E,L,px,py)  that are constant
along every trajectory, where m_i runs over momentum monomials of exact degree r.

E and L are VARIED across the ensemble (see prereg): in this 2-DOF reduction they
are frozen parameters, so a single (E,L) would make them indistinguishable from any
other constant.
"""
import itertools, sys, json
from pathlib import Path
import numpy as np
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _zv_invariant import metric
from poincare import _rk4, p_on_shell, H_value

HSTEP, NSTEP, BURN = 0.02, 6000, 500
OUT = Path(__file__).resolve().parent.parent / "results"; OUT.mkdir(exist_ok=True)

def integrate(f, x0, E, L, n=NSTEP):
    py = None
    a, b = 0.0, 3.0
    if p_on_shell(f, x0, 0.0, 0.0, E, L) is None: return None
    for _ in range(60):
        m = 0.5*(a+b)
        py = m
        if p_on_shell(f, x0, 0.0, m, E, L) is None: b = m
        else: a = m
    py = a
    p1 = p_on_shell(f, x0, 0.0, py, E, L)
    if p1 is None: return None
    s = [x0, 0.0, p1, py]; H0 = H_value(f, s, E, L)
    X = np.empty((n,4))
    for i in range(n):
        try: s = _rk4(f, s, HSTEP, E, L)
        except (OverflowError, ZeroDivisionError, ValueError): return None
        if s[0] < 1.3 or s[0] > 120 or abs(s[1]) > 0.999: return None
        X[i] = s
    if abs(H_value(f, s, E, L) - H0)/max(abs(H0),1e-300) > 1e-6: return None
    return X[BURN:]

def metric_funcs(f, x, y):
    """The METRIC'S OWN functions as coefficient basis elements.

    FIRST ATTEMPT USED GENERIC POLYNOMIALS IN (x,y) AND FAILED CALIBRATION: 3
    conserved directions at delta=1 where Schwarzschild has 5. The three found were
    E^2, EL, L^2 -- the trivial products of the frozen momenta. H and L_tot^2 were
    MISSING, because H = 1/2(g11 px^2 + g22 py^2) + 1/2 W and the ZV metric
    components are NOT polynomials in (x,y): F = ((x-1)/(x+1))^delta,
    Hzv = ((x^2-1)/(x^2-y^2))^(delta^2). A polynomial coefficient basis cannot
    represent them. That is ansatz's failure mode 2 -- constant/insufficient
    coefficients where the answer needs the metric's own structure -- the same
    defect that lost them Carter at s85.

    W(E,L) = gi_tt E^2 - 2 gi_tphi E L + gi_phiphi L^2, so evaluating W at
    (1,0), (0,1), (1,1) recovers the three inverse-metric components separately."""
    g11 = f["g11"](x, y, 1.0, 0.0); g22 = f["g22"](x, y, 1.0, 0.0)
    tt  = f["W"](x, y, 1.0, 0.0)
    pp  = f["W"](x, y, 0.0, 1.0)
    tp  = (tt + pp - f["W"](x, y, 1.0, 1.0))/2.0
    return [g11, g22, tt, pp, tp]

def basis(X, EL, deg, cdeg, f):
    """momentum monomials of EXACT degree `deg` in (E,L,px,py) x coefficient functions of (x,y).

    COEFFICIENT SET, minimal and deliberate. Attempt 1 used generic polynomials and
    returned 3 at delta=1 where Schwarzschild has 5 -- H and L_tot^2 both missing,
    because the ZV metric components are not polynomial in (x,y). Attempt 2 threw in
    the metric functions twice and returned 64, which was rank deficiency in my own
    columns being counted as conservation.

    ansatz supplied the exact missing piece, verified {H, L_tot^2} = 0 on delta=1:
        L_tot^2 = (1 - y^2) * py^2  +  L^2 / (1 - y^2)
    The coefficient of L^2 is 1/(1-y^2), NOT A POLYNOMIAL. y = cos(theta), so
    1-y^2 = sin^2(theta) and this is the textbook 1/sin^2(theta). Without it the
    screen returns 4 instead of 5 and the miss looks exactly like a real absence."""
    x, y, px, py = X[:,0], X[:,1], X[:,2], X[:,3]
    E = np.full(len(x), EL[0]); L = np.full(len(x), EL[1])
    mom = []
    for e in itertools.product(range(deg+1), repeat=4):
        if sum(e) == deg:
            mom.append((E**e[0])*(L**e[1])*(px**e[2])*(py**e[3]))
    g11 = np.asarray(f["g11"](x, y, 1.0, 0.0), float)
    g22 = np.asarray(f["g22"](x, y, 1.0, 0.0), float)
    tt  = np.asarray(f["W"](x, y, 1.0, 0.0), float)
    pp  = np.asarray(f["W"](x, y, 0.0, 1.0), float)
    tp  = (tt + pp - np.asarray(f["W"](x, y, 1.0, 1.0), float))/2.0
    one = np.ones_like(x)
    base = [1.0-y*y, 1.0/(1.0-y*y), g11, g22, tt, pp, tp]         # ansatz's 1/(1-y^2) adjoined
    # PRODUCTS UP TO deg//2. A degree-4 conserved quantity is a product of two
    # degree-2 ones, so its coefficient is a PRODUCT of two degree-2 coefficients --
    # e.g. H^2 needs g11^2, which is absent from the base set. Attempt 3 used base
    # functions only and returned 8-11 at degree 4 where Schwarzschild has 14, AND
    # was unstable across tolerance, which is the signature of a span that is short
    # rather than a threshold that is wrong.
    coo = [one]
    for k in range(1, max(1, deg//2)+1):
        for combo in itertools.combinations_with_replacement(range(len(base)), k):
            v = one.copy()
            for j in combo: v = v*base[j]
            coo.append(v)
    for d in range(1, cdeg+1):
        for i in range(d+1):
            coo.append((x**i)*(y**(d-i)))
    return np.column_stack([m*c for m, c in itertools.product(mom, coo)])

def count_conserved(cols, tid, tol):
    """Conserved directions, via ORTHOGONALISE-THEN-COUNT.

    The previous version computed  dim null(Z_centred) - dim null(cols_raw), and at
    degree 4 that was 1008 - 1001 = 7: a small difference of two large,
    threshold-dependent integers. Catastrophic cancellation in a rank estimate, and
    the count swung 7/11/16/16/19 across five tolerances with no stable value.

    Instead: project onto the numerically independent subspace of the raw columns
    FIRST, so the degenerate directions are gone before centring and the answer is a
    direct nullspace dimension rather than a difference.
    """
    C = cols/np.maximum(np.abs(cols).max(0), 1e-300)
    U, sv, Vt = np.linalg.svd(C, full_matrices=False)
    keep = sv/sv.max() >= tol                        # independent subspace of the BASIS
    P = Vt[keep].T                                   # (ncols, rank)
    B = C @ P                                        # samples x rank, full column rank
    Z = np.empty_like(B)
    for t in np.unique(tid):
        m = tid == t
        Z[m] = B[m] - B[m].mean(0)
    Z = Z/np.maximum(np.abs(B).max(0), 1e-300)
    sz = np.linalg.svd(Z, compute_uv=False); sz = sz/sz.max()
    return int((sz < tol).sum()), sz, int((~keep).sum())

if __name__ == "__main__":
    delta = float(sys.argv[1]); deg = int(sys.argv[2]); cdeg = int(sys.argv[3])
    ntraj = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    f = metric(delta)
    rng = np.random.default_rng(11)
    Xs, tid, ELs = [], [], []
    t = 0; tries = 0
    while len(Xs) < ntraj and tries < 4000:
        tries += 1
        E = rng.uniform(0.90, 0.97); L = rng.uniform(2.6, 3.6)
        x0 = rng.uniform(8.0, 16.0)
        X = integrate(f, x0, E, L)
        if X is None: continue
        Xs.append(X); ELs.append((E,L)); tid.append(np.full(len(X), t)); t += 1
    if not Xs:
        print("NO ORBITS"); sys.exit(1)
    cols = np.vstack([basis(X, el, deg, cdeg, f) for X, el in zip(Xs, ELs)])
    tid = np.concatenate(tid)
    step = max(1, len(cols)//(12*cols.shape[1]))     # rows >> cols is enough for rank
    cols, tid = cols[::step], tid[::step]
    print(f"delta={delta}  momentum-degree={deg}  coord-degree={cdeg}  "
          f"orbits={len(Xs)}  basis-dim={cols.shape[1]}  samples={len(cols)}", flush=True)
    for tol in [1e-6, 1e-7, 1e-8, 1e-9, 1e-10]:
        n, s, nd = count_conserved(cols, tid, tol)
        print(f"   tol={tol:.0e}  conserved = {n:3d}   (null(Z)={n+nd}, basis-degenerate={nd})", flush=True)
    _, s, _ = count_conserved(cols, tid, 1e-8)
    print("   smallest 12 normalised singular values:")
    print("     " + "  ".join(f"{v:.2e}" for v in s[-12:]), flush=True)
