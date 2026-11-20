"""V25 P4 (i) exact identity for (d_u^2 - w^2 kappa^2) v^k; (ii) null space of admissible E-independent principal parts
from own local-series residues (t = sqrt(z - z1)). Bridge code only."""
import os, json, sympy as sp, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); out = {}
# ---- (i)
z, z1, z2, m1, m2, E, mu, k = sp.symbols('z z1 z2 m1 m2 E mu k')
D = (z - z1)*(z - z2); f0 = 1 - m1/(z - z1) - m2/(z - z2); Dl = sp.expand(sp.cancel(f0*D))
N = sp.expand(E**2*D - mu**2*Dl); Y2 = sp.expand(N*D); dl = z1 - z2
kap2 = dl*((E**2 - mu**2)*dl - mu**2*(m1 - m2))/4
v = (z - z2)/(z - z1); ept = 4*kap2/(mu**2*dl)
res_i = {}
vp = sp.diff(v, z); vpp = sp.diff(v, z, 2); Y2p = sp.diff(Y2, z)
for w in (2, 4):
    # divide both sides by v^(k-2): F' = k v^(k-1) v', F'' = k(k-1) v^(k-2) v'^2 + k v^(k-1) v''
    lhs = Y2*(k*(k - 1)*vp**2 + k*v*vpp) + Y2p*k*v*vp/2 - w**2*kap2*v**2
    rhs = mu**2*dl*(m1*k*(k + sp.Rational(1, 2))*v**3 + ept*(k**2 - sp.Rational(w**2, 4))*v**2 - m2*k*(k - sp.Rational(1, 2))*v)
    d = sp.cancel(sp.together(lhs - rhs))
    # independent spot check with integer k and the undivided form
    spot = [sp.cancel(sp.together(Y2*sp.diff(v**kk, z, 2) + Y2p*sp.diff(v**kk, z)/2 - w**2*kap2*v**kk
            - mu**2*dl*(m1*kk*(kk + sp.Rational(1, 2))*v**(kk + 1) + ept*(kk**2 - sp.Rational(w**2, 4))*v**kk - m2*kk*(kk - sp.Rational(1, 2))*v**(kk - 1))))
            for kk in (-5, -1, 0, 1, 2, 3, 7)]
    res_i[w] = dict(symbolic_k=str(d), integer_k_spots=[str(x) for x in spot]); print('(i) w =', w, 'symbolic-k difference:', d, '| integer k spots:', spot, flush=True)
out['P4i'] = res_i
# ---- (ii) local series residues
mp.mp.dps = 60
K = 12; NT = 2*K + 4
def ser_mul(a, b): return [mp.fsum(a[i]*b[n - i] for i in range(n + 1)) for n in range(NT)]
def ser_inv(a):
    b = [1/a[0]] + [mp.mpf(0)]*(NT - 1)
    for n in range(1, NT): b[n] = -mp.fsum(a[i]*b[n - i] for i in range(1, n + 1))/a[0]
    return b
def ser_sqrt(a):  # a[0] != 0, principal
    b = [mp.sqrt(a[0])] + [mp.mpc(0)]*(NT - 1)
    for n in range(1, NT): b[n] = (a[n] - mp.fsum(b[i]*b[n - i] for i in range(1, n)))/(2*b[0])
    return b
def ser_exp(a):  # a[0] = 0
    b = [mp.mpc(1)] + [mp.mpc(0)]*(NT - 1); da = [(n + 1)*a[n + 1] for n in range(NT - 1)] + [0]
    for n in range(1, NT): b[n] = mp.fsum(da[i]*b[n - 1 - i] for i in range(n))/n
    return b
def poly_in_t2(coeffs_z, Z1):
    """polynomial in z (coeff list, low->high) evaluated at z = Z1 + t^2, as a series in t."""
    s = [mp.mpc(0)]*NT; zp = [mp.mpc(1)] + [mp.mpc(0)]*(NT - 1); base = [Z1, 0, 1] + [0]*(NT - 3)
    for c in coeffs_z:
        s = [s[i] + c*zp[i] for i in range(NT)]; zp = ser_mul(zp, base)
    return s
def residues(Z1, Z2, M1, M2, EE, w):
    """residue of (z - z1)^(-k) e^{w kappa (u - u_P)} du at the branch point z1, k = 1..K."""
    MU = 1
    Dc = [Z1*Z2, -(Z1 + Z2), 1]; Dlc = [Z1*Z2 + M1*Z2 + M2*Z1, -(Z1 + Z2) - M1 - M2, 1]
    Nc = [EE**2*Dc[i] - MU**2*Dlc[i] for i in range(3)]
    Ns = poly_in_t2(Nc, Z1); zm2 = poly_in_t2([Z1 - Z2 - Z1, 1], Z1)   # (z - z2) = (z1 - z2) + t^2
    zm2 = [Z1 - Z2, 0, 1] + [0]*(NT - 3)
    g = ser_sqrt(ser_mul(Ns, zm2)); ig = ser_inv(g)
    Uu = [mp.mpc(0)] + [2*ig[n - 1]/n for n in range(1, NT)]   # u - u_P = int_0^t 2/g
    dl_ = Z1 - Z2; kap = mp.sqrt(dl_*((EE**2 - MU**2)*dl_ - MU**2*(M1 - M2))/4)
    ex = ser_exp([w*kap*c for c in Uu])
    # du = 2 dt/g ; residue of t^{-2k} * ex * 2/g  = coefficient of t^{2k-1} in 2 ex / g
    h = ser_mul(ex, [2*c for c in ig])
    return [h[2*kk - 1] for kk in range(1, K + 1)], kap
cases = {'kerr_type': (0.6j, -0.6j, 1, 1, (0.55, 0.95)),
         'kerrnut_type': (0.5j, -0.5j, 1 - 0.4j, 1 + 0.4j, (0.5, 0.95)),
         'real_poles': (1, -0.5, 0.75, 0.5, (0.3, 0.9))}
res_ii = {}
for name, (Z1, Z2, M1, M2, (Ea, Eb)) in cases.items():
    Z1, Z2, M1, M2 = map(mp.mpc, (Z1, Z2, M1, M2))
    rows = []
    for i in range(20):
        EE = mp.mpf(Ea) + (mp.mpf(Eb) - mp.mpf(Ea))*i/19
        for w in (2, 4): rows.append(residues(Z1, Z2, M1, M2, EE, w)[0])
    A = mp.matrix(rows)
    U_, S_, Vh = mp.svd_c(A)
    sv = [S_[i] for i in range(min(A.rows, A.cols))]
    small = [i for i, s in enumerate(sv) if s < sv[0]*mp.mpf(10)**-40]
    null = [Vh[i, :] for i in small]
    # predicted null vector: principal part of v^3 - (3 m2/(5 m1)) v, v = 1 + dl/(z - z1): coefficients of (z - z1)^-k
    dl_ = Z1 - Z2; pred = [3*dl_ - 3*M2/(5*M1)*dl_, 3*dl_**2, dl_**3] + [0]*(K - 3)
    pn = mp.sqrt(mp.fsum(abs(c)**2 for c in pred)); pred = [c/pn for c in pred]
    if len(null) == 1:
        nv = [mp.conj(null[0][0, j]) for j in range(K)]   # null vector of A = conj of the Vh row
        Ax = max(abs(mp.fsum(A[r_, j]*nv[j] for j in range(K))) for r_ in range(A.rows)); Apred = max(abs(mp.fsum(A[r_, j]*pred[j] for j in range(K))) for r_ in range(A.rows)); ph = mp.fsum(mp.conj(pred[j])*nv[j] for j in range(K))
        align = float(abs(ph)); resid = float(mp.sqrt(mp.fsum(abs(nv[j] - ph*pred[j])**2 for j in range(K))))
    else: align = resid = Ax = Apred = None
    gap = float(sv[small[0] - 1]/sv[small[0]]) if small and small[0] > 0 else None
    r = dict(Ax_null=mp.nstr(Ax, 3) if len(null) == 1 else None, Ax_pred=mp.nstr(Apred, 3) if len(null) == 1 else None, nullity=len(null), sing_vals=[mp.nstr(s, 5) for s in sv], gap=gap, align_with_pred=align, resid_from_pred=resid)
    res_ii[name] = r; print('(ii)', name, r, flush=True)
# negative control: the same with the WRONG line v^3 - (3 m1/(5 m2)) v swapped coefficient should NOT be in the null space (only differs if m1 != m2)
out['P4ii'] = res_ii
json.dump(out, open(os.path.join(HERE, '../results/v25_p4.json'), 'w'), indent=1, default=str)
