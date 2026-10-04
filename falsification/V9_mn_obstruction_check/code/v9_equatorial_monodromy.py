"""V9-eq -- the bridge's reproduction of quantum's MN equatorial row-0 monodromy (pre-registration
PREREG_EQUATORIAL_ROW0.md). Own equations (v9_nve transcription), own t-conversion, scipy DOP853. Reads no quantum file;
the loop specification is transcribed from quantum's cross-session message.
Branch: R(x,y) = sqrt(R0^2 + y^2) with R0 a POSITIVE symbol so sqrt(R0^2)=R0 (exact y-derivatives at y=0), then x = (t+1/t)/2, R0 = (t^2-1)/(2t)."""
import json, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from v9_nve import x, y

t = sp.Symbol('t')
# V9-eq' fix (post-failure): R0 declared positive so sqrt(R0^2 + y^2)|_{y=0} reduces to R0 itself BEFORE substituting
# R0 = (t^2-1)/(2t). Without it the principal sqrt flipped the sign of R on the t<1 sheet (first run: DISAGREES).
R0 = sp.Symbol('R0', positive=True)

def mn_functions_R0(M, a_, beta):
    """Same formulas as v9_nve.mn_functions, with R = sqrt(R0^2 + y^2) (equal to sqrt(x^2+y^2-1) when R0^2 = x^2-1)."""
    M, a_, beta = map(sp.nsimplify, (M, a_, beta))
    chi = a_/M; al = sp.nsimplify((-1 + sp.sqrt(1 - chi**2))/chi); k = sp.sqrt(M**2 - a_**2)
    R = sp.sqrt(R0**2 + y**2); u = x*y/R
    P = [sp.Integer(1), u, (3*u**2 - 1)/2, (5*u**3 - 3*u)/2]
    psi = beta*P[2]/R**3
    A_ = -al*sp.exp(-2*beta*(-1 + sum((x - y)*P[l]/R**(l + 1) for l in range(3))))
    B_ = al*sp.exp(2*beta*(1 + sum((-1)**(3 - l)*(x + y)*P[l]/R**(l + 1) for l in range(3))))
    Am = (x**2 - 1)*(1 + A_*B_)**2 - (1 - y**2)*(B_ - A_)**2
    Bm = (x + 1 + (x - 1)*A_*B_)**2 + ((1 + y)*A_ + (1 - y)*B_)**2
    Cm = (x**2 - 1)*(1 + A_*B_)*(B_ - A_ - y*(A_ + B_)) + (1 - y**2)*(B_ - A_)*(1 + A_*B_ + x*(1 - A_*B_))
    f = sp.exp(2*psi)*Am/Bm
    om = 2*k*sp.exp(-2*psi)*Cm/Am - 4*k*al/(1 - al**2)
    e2g = (x**2 - 1)/(x**2 - y**2)*sp.exp(3*beta**2*(P[3]**2 - P[2]**2)/R**6
            + 2*beta*sum((x - y + (-1)**l*(x + y))*P[l]/R**(l + 1) - 2 for l in range(3)) + 8*beta)*Am/((x**2 - 1)*(1 - al**2)**2)
    return dict(f=f, om=om, e2g=e2g, k=k)

def eq_coeffs_t(M, a_, beta, E, L, mu2):
    F = mn_functions_R0(M, a_, beta); f, om, e2g, k = F['f'], F['om'], F['e2g'], F['k']
    gtt = -f; gtp = f*om; gpp = -f*om**2 + k**2/f*(x**2 - 1)*(1 - y**2)
    gxx_dn = k**2/f*e2g*(x**2 - y**2)/(x**2 - 1); gyy_dn = k**2/f*e2g*(x**2 - y**2)/(1 - y**2)
    det = gtt*gpp - gtp**2
    Gtt, Gtp, Gpp, Gxx, Gyy = gpp/det, -gtp/det, gtt/det, 1/gxx_dn, 1/gyy_dn
    at0 = lambda e: e.subs(y, 0)
    d2 = lambda e: sp.diff(e, y, 2).subs(y, 0)
    E, L, mu2 = map(sp.Integer, (E, L, mu2))
    V0 = at0(Gtt)*E**2 - 2*at0(Gtp)*E*L + at0(Gpp)*L**2
    V2 = d2(Gtt)*E**2 - 2*d2(Gtp)*E*L + d2(Gpp)*L**2
    px2 = (-mu2 - V0)/at0(Gxx)
    A = at0(Gyy); X = at0(Gxx)*(-mu2 - V0); B = sp.Rational(1, 2)*(d2(Gxx)*px2 + V2)
    sub = {x: (t + 1/t)/2, R0: (t**2 - 1)/(2*t)}
    A, B, X = [e.subs(sub) for e in (A, B, X)]
    xt = (t + 1/t)/2; x1 = sp.diff(xt, t); x2 = sp.diff(x1, t)
    half = [a for a in (A + B + X).atoms(sp.Pow) if a.exp.is_Rational and a.exp.q == 2 and a.base.has(t)]
    assert not half, f'square roots of t survive: {half[:2]}'
    pt = -(sp.diff(A, t)/A - sp.diff(X, t)/(2*X)) - x2/x1
    qt = x1**2*A*B/X
    return pt, qt, x1, x2

def seg(pf, qf, z0, z1, Y, tol):
    dz = z1 - z0
    def F(s, Y):
        z = z0 + s*dz; P, Q = pf(z), qf(z)
        return [dz*Y[1], dz*(-P*Y[1] - Q*Y[0]), dz*Y[3], dz*(-P*Y[3] - Q*Y[2])]
    return solve_ivp(F, (0, 1), Y, method='DOP853', rtol=tol, atol=tol*1e-3).y[:, -1]

def loop_pts(base, c, rho):
    phi0 = np.angle(base - c)
    return [base] + [c + rho*np.exp(1j*(phi0 + 2*np.pi*j/16)) for j in range(17)] + [base]

def monodromy(pf, qf, pts, tol):
    Y = np.array([1, 0, 0, 1], dtype=complex)
    for z0, z1 in zip(pts[:-1], pts[1:]): Y = seg(pf, qf, z0, z1, Y, tol)
    return np.array([[Y[0], Y[2]], [Y[1], Y[3]]])

def abel_det(pf, pts, n=400):
    xs, ws = np.polynomial.legendre.leggauss(n); s = (xs + 1)/2; w = ws/2; I = 0
    for z0, z1 in zip(pts[:-1], pts[1:]): I += np.sum(w*pf(z0 + s*(z1 - z0)))*(z1 - z0)
    return np.exp(-I)

inv = lambda G: np.trace(G)**2/np.linalg.det(G)
comm = lambda G, H: np.trace(G @ H @ np.linalg.inv(G) @ np.linalg.inv(H))

R = sp.Rational
# Row specifications transcribed from quantum's cross-session messages (no quantum file read). g, h = products of loop M's.
ROWS = {
    0: dict(params=(5, 3, R(1, 5), 1, 0, 4), prov='p1|E=1,L=0,mu2=4', out='v9_equatorial_row0_amended.json',
            base=2.0246153192247602 + 2.100243381102574j,
            loops=dict(a=(0.18574683248165982, 0.10036930953180813), b=(-0.5601946717730222, 0.01330513017617667),
                       c=(-0.14881753262436728, 0.10036930953180813)), g=('a', 'b'), h=('c', 'b'),
            target=dict(inv_g=-313428.5136459282350497 - 106383.3249050493482615j, inv_h=26436.87518302681110765 + 0j,
                        comm=-290240.6602844212393278 - 86714.14718309701690989j)),
    1: dict(params=(5, 3, R(1, 5), 1, 0, 9), prov='p1|E=1,L=0,mu2=9', out='v9_equatorial_row1_a6.json',
            base=2.483596994071131 + 2.5763699891994527j,
            loops=dict(a=(1.2614475105508947 + 0.32152725175852437j, 0.025727621885033154),
                       b=(1.2874032225413898 + 0.23979070891675344j, 0.025727621885033154),
                       c=(-0.16003305636505147, 0.1262521808340563)), g=('a', 'b'), h=('a', 'c'),
            target=dict(inv_g=-2547891.708701964777810606 + 4172532.225771545916124269j,
                        inv_h=-6817.148639232440284151301 + 7154.641062752441547069280j,
                        comm=51202181.92116578640060854 + 30889220.29971538901706583j)),
    2: dict(params=(5, 3, R(1, 5), 1, 1, 4), prov='p1|E=1,L=1,mu2=4', out='v9_equatorial_row2_a6.json',
            base=2.4691717810397047 + 2.5614059326191394j,
            loops=dict(a=(1.0407508871125104 + 0.4677121389555332j, 0.03132088280290887),
                       b=(1.0080515742827576 + 0.36856210426090547j, 0.03132088280290887),
                       c=(0.19761156121947301, 0.1154952476585107)), g=('a', 'b'), h=('a', 'c'),
            target=dict(inv_g=48.16395921732219238937 - 56.11599596601088473492j,
                        inv_h=-12146.88614102791808418 - 6932.690639883441608725j,
                        comm=544.0346538066000467109 - 550.2748225118644843529j)),
    4: dict(params=(13, 5, R(-1, 3), 1, 0, 9), prov='p2|E=1,L=0,mu2=9', out='v9_equatorial_row4_a6.json',
            base=2.6478084529899895 + 2.7467154500979643j,
            loops=dict(a=(1.4630859217922259 + 0.11907670815419788j, 0.07144602489251872),
                       b=(0.844094439134436 + 0.46228514057135917j, 0.038060428501300446),
                       c=(0.4236097945571309, 0.15468191854243515)), g=('a', 'b'), h=('b', 'c'),
            target=dict(inv_g=-54792981.25991847482041863 + 38564787.55385748195701619j,
                        inv_h=112.8409200682702553747621 - 107.4809780833145082690042j,
                        comm=9307412800.054622903634094 - 4874558287.894730114374308j),
            v2_radius=dict(inv_g=5.0e4, inv_h=1.05e-7, comm=3.2e9)),
    3: dict(params=(13, 5, R(-1, 3), 1, 0, 4), prov='p2|E=1,L=0,mu2=4', out='v9_equatorial_row3.json',
            base=2.667119562555136 + 2.7667479123938024j,
            loops=dict(a=(0.307967384242499, 0.20760978472725028), b=(-0.4751366065599529 + 0.22858319755496656j, 0.07700413164438846),
                       c=(-0.7703523566330759 + 0.37656494220755987j, 0.017435697281317466)), g=('a', 'b'), h=('a', 'c'),
            target=dict(inv_g=1345.2758406025942679 - 1011.6353858956783367j, inv_h=-2371.4390654371280839 - 7787.8783024198235091j,
                        comm=-389140.59069213841206 + 1464024.0755057192621j)),
}

if __name__ == '__main__':
    import sys
    row = ROWS[int(sys.argv[1]) if len(sys.argv) > 1 else 0]
    pt, qt, x1, x2 = eq_coeffs_t(*row['params'])
    out = {}
    # Gate 1: back-convert at t = 2 (x = 5/4) and compare with the bridge's committed 50-digit provenance values
    prov = json.load(open('../results/v9_equatorial_provenance.json'))[row['prov']]['5/4']
    px = ((pt + x2/x1)/x1).subs(t, 2); qx = (qt/x1**2).subs(t, 2)
    px, qx = sp.N(px, 40), sp.N(qx, 40)
    e1 = max(abs(px/sp.Float(prov['p'], 50) - 1), abs(qx/sp.Float(prov['q'], 50) - 1))
    out['gate1_rel_err'] = float(e1); print('gate 1 provenance rel err:', float(e1), 'PASS' if e1 < 1e-12 else 'FAIL', flush=True)
    if e1 >= 1e-12: json.dump(out, open('../results/' + row['out'], 'w'), indent=1); raise SystemExit
    pf = sp.lambdify(t, pt, modules='numpy', cse=True); qf = sp.lambdify(t, qt, modules='numpy', cse=True)
    base, loops, target = row['base'], row['loops'], row['target']
    res = {}
    for tol in (1e-11, 1e-13):
        Ms = {k: monodromy(pf, qf, loop_pts(base, c, r), tol) for k, (c, r) in loops.items()}
        (g1, g2_), (h1, h2_) = row['g'], row['h']
        g, h = Ms[g1] @ Ms[g2_], Ms[h1] @ Ms[h2_]; g2, h2 = Ms[g2_] @ Ms[g1], Ms[h2_] @ Ms[h1]
        res[tol] = dict(inv_g=inv(g), inv_h=inv(h), comm=comm(g, h), comm_rev=comm(g2, h2),
                        abel=max(abs(np.linalg.det(Ms[k])/abel_det(pf, loop_pts(base, c, r)) - 1) for k, (c, r) in loops.items()))
        v = res[tol]; print(f'tol {tol:.0e}: tr2/det g={v["inv_g"]:.12g}  tr2/det h={v["inv_h"]:.12g}  tr[g,h]={v["comm"]:.12g}'
                            f'  (reversed order {v["comm_rev"]:.8g})  Abel rel err {v["abel"]:.1e}', flush=True)
    lo, hi = res[1e-11], res[1e-13]
    conv = max(abs(hi[k]/lo[k] - 1) for k in target); agree = {k: abs(hi[k]/target[k] - 1) for k in target}
    abel_ok = max(lo['abel'], hi['abel']) < 1e-8
    print('gate 2 Abel:', 'PASS' if abel_ok else 'FAIL', ' gate 3 convergence rel:', f'{conv:.1e}', 'PASS' if conv < 1e-7 else 'FAIL')
    print('agreement with quantum (rel):', {k: f'{v:.1e}' for k, v in agree.items()})
    if abel_ok and conv < 1e-7:
        verdict = 'REPRODUCED' if max(agree.values()) < 1e-7 else ('DISAGREES' if max(agree.values()) > 1e-5 else 'INCONCLUSIVE')
        if verdict != 'REPRODUCED' and 'v2_radius' in row:   # row-4 addendum rule: inside quantum's own v2 ball = CONSISTENT
            inside = all(abs(hi[k] - target[k]) <= row['v2_radius'][k] for k in target)
            verdict = 'CONSISTENT (inside v2 enclosures)' if inside else 'DISAGREES'
    else: verdict = 'INCONCLUSIVE'
    print('VERDICT:', verdict)
    out.update(dict(results={str(k): {kk: str(vv) for kk, vv in v.items()} for k, v in res.items()}, convergence=conv,
                    agreement={k: v for k, v in agree.items()}, verdict=verdict))
    json.dump(out, open('../results/' + row['out'], 'w'), indent=1, default=str)
