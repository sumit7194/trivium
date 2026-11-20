"""V25 addendum C: Bridge check of Gemini Neon's Lemma G3 invariants (C1) and Lemma X-inf residue
asymptotics (C2, C3). Prereg: PREREGISTRATION.md addendum C. Independent implementation (exact sympy for C1,
own mpmath power-series arithmetic for C2/C3); no Neon code used."""
import sympy as sp, mpmath as mp

# ---------------- C1 ----------------
def C1():
    z, z1, z2, m1, m2, E, mu = sp.symbols('z z1 z2 m1 m2 E mu')
    D = (z - z1)*(z - z2)
    f0 = 1 - m1/(z - z1) - m2/(z - z2)
    N = sp.expand(sp.cancel(E**2*D - mu**2*D*f0))
    P4 = sp.Poly(sp.expand(N*D), z)
    c = [P4.coeff_monomial(z**k) for k in (4, 3, 2, 1, 0)]
    b0, b1, b2, b3, b4 = c[0], c[1]/4, c[2]/6, c[3]/4, c[4]
    I = b0*b4 - 4*b1*b3 + 3*b2**2
    J = b0*b2*b4 + 2*b1*b2*b3 - b0*b3**2 - b4*b1**2 - b2**3
    X = (E**2 - mu**2)*(z1 - z2) - mu**2*(m1 - m2)
    S = X**2/(mu**4*m1*m2)
    Ic = (z1 - z2)**2*(X**2 + 3*mu**4*m1*m2)/12
    Jc = -(z1 - z2)**3*X*(2*X**2 + 9*mu**4*m1*m2)/432
    Dc = mu**8*m1**2*m2**2*(z1 - z2)**6*(X**2 + 4*mu**4*m1*m2)/256
    jc = 256*(S + 3)**3/(S + 4)
    d = {'I': sp.simplify(sp.expand(I - Ic)), 'J': sp.simplify(sp.expand(J - Jc)),
         'Disc': sp.simplify(sp.expand(I**3 - 27*J**2 - Dc)),
         'j': sp.simplify(sp.cancel(1728*I**3/(I**3 - 27*J**2) - jc))}
    print('C1 b0 =', sp.factor(b0))
    for k, v in d.items(): print('C1', k, 'difference ->', v)
    return all(v == 0 for v in d.values())

# ------------- series helpers -------------
def smul(a, b, N): return [mp.fsum(a[k]*b[n-k] for k in range(n+1)) for n in range(N)]
def spow(a, p, N):
    b = [a[0]**p] + [0]*(N-1)
    for n in range(1, N):
        b[n] = mp.fsum((p*k - (n-k))*a[k]*b[n-k] for k in range(1, n+1) if k < len(a))/(n*a[0])
    return b
def sexp(a, N):
    assert abs(a[0]) == 0
    b = [mp.mpf(1)] + [0]*(N-1)
    for n in range(1, N):
        b[n] = mp.fsum(k*a[k]*b[n-k] for k in range(1, n+1))/n
    return b
def pad(a, N): return list(a) + [0]*(N-len(a))

def residue(m, w, eps, z1, z2, m1, m2, mu=1):
    """Res_{t=0} Q(1/t) e^{w kappa s(t)} (ds/dt) dt, Q = z^m + z^{m-1}, '+' branch ds/dt -> +eps^{-1/2}."""
    N = m + 2
    P = pad([1, -(z1 + z2), z1*z2], N)
    M2 = m1 + m2
    QN = pad([eps, -eps*(z1 + z2) + mu**2*M2, eps*z1*z2 - mu**2*(m1*z2 + m2*z1)], N)
    g = spow(smul(P, QN, N), mp.mpf(-1)/2, N)          # ds/dt
    s = [0] + [g[n-1]/n for n in range(1, N)]          # s(0)=0
    kap = mp.sqrt((z1 - z2)*(eps*(z1 - z2) - mu**2*(m1 - m2))/4)
    e = sexp([w*kap*x for x in s], N)
    f = smul(smul(pad([1, 1], N), e, N), g, N)         # t^m Q(1/t) = 1 + t
    return f[m-1] if m >= 1 else mp.mpf(0)             # m=0: Q(1/t)=1+t regular -> residue 0

def claimC2(m, eps, m1, m2, mu=1):
    M = (m1 + m2)/2
    return mp.binomial(mp.mpf(-1)/2, m-1)*(2*M*mu**2)**(m-1)*eps**(-m + mp.mpf(1)/2)

def claimC3(m, w, eps, z1, z2, m1, mu=1):
    c = mu**2*m1*(z1 - z2)
    k0 = mp.sqrt((z1 - z2)*(-mu**2*(2*m1))/4)          # kappa(E) at eps=0, same principal branch
    al = w*k0/mp.sqrt(c)
    prod = mp.fprod([al + m - 2*j for j in range(1, m)]) if m > 1 else 1
    return eps**(-mp.mpf(m)/2)*mp.sqrt(c)**(m-1)*prod/mp.factorial(m-1)

def main():
    mp.mp.dps = 60
    ok1 = C1()
    cases = {'kerr-type': (0.6j, -0.6j, 1, 1), 'asym': (1, -0.5, 0.75, 0.5)}
    ok2 = True
    for name, (z1, z2, m1, m2) in cases.items():
        z1, z2, m1, m2 = mp.mpc(z1), mp.mpc(z2), mp.mpf(m1), mp.mpf(m2)
        for m in range(1, 5):
            errs = []
            for eps in (mp.mpf('1e-4'), mp.mpf('1e-6'), mp.mpf('1e-8')):
                r = residue(m, 2, eps, z1, z2, m1, m2) / claimC2(m, eps, m1, m2)
                errs.append(abs(r - 1))
            good = errs[-1] <= 1e-2 and errs[0] >= errs[1] >= errs[2]
            ok2 &= good
            print('C2 %-9s m=%d |ratio-1| at eps 1e-4,1e-6,1e-8: %s %s' % (name, m, ['%.2e' % x for x in errs], good))
    r0 = residue(0, 2, mp.mpf('1e-6'), mp.mpc(1), mp.mpc(-0.5), mp.mpf(0.75), mp.mpf(0.5))
    print('C2 control m=0 residue', r0, '(structural zero)')
    ok2 &= abs(r0) < 1e-40
    # C3: M = 0 dipole
    z1, z2, m1 = mp.mpc(1), mp.mpc(-0.5), mp.mpf(0.5)
    ok3 = True
    for m in range(1, 5):
        errs = []
        for eps in (mp.mpf('1e-4'), mp.mpf('1e-6'), mp.mpf('1e-8')):
            r = residue(m, 2, eps, z1, z2, m1, -m1) / claimC3(m, 2, eps, z1, z2, m1)
            errs.append(abs(r - 1))
        good = errs[-1] <= 1e-2
        ok3 &= good
        print('C3 dipole m=%d |ratio-1| at eps 1e-4,1e-6,1e-8: %s %s' % (m, ['%.2e' % x for x in errs], good))
    eps = mp.mpf('1e-8')
    wi = 1j*mp.sqrt(2)
    sc_i = abs(residue(3, wi, eps, z1, z2, m1, -m1))*eps**1.5
    sc_r = abs(residue(3, 2, eps, z1, z2, m1, -m1))*eps**1.5
    ctrl = sc_i/sc_r
    print('C3 control w=i*sqrt2, m=3: scaled residue %.3e vs w=2 %.3e, ratio %.3e (must be <= 1e-2)' % (sc_i, sc_r, ctrl))
    ok3 &= ctrl <= 1e-2
    print('VERDICT C1', 'PASS' if ok1 else 'FAIL', '| C2', 'PASS' if ok2 else 'FAIL', '| C3', 'PASS' if ok3 else 'FAIL')

if __name__ == '__main__':
    main()
