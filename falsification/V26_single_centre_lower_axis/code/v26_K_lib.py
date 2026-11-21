"""V26-K library (Bridge's own code; Neon's scripts not used): rigorous complex-interval enclosure of
H_theta(u) = sqrt(8/5) * int_0^1 x(1-x) (1 + u^-2)/(1 + t)^3 sqrt(alpha + beta t + gamma t^2) dx,  t = x^2/u^2,
alpha = 21(1-theta), beta = 120/7 theta - 18(1-theta), gamma = 1 + 33/7 theta,
over a parameter box theta in [t0,t1], u = x0 + i eta with x0 in [X0,X1], eta in [E0,E1].
x-integration: per cell, midpoint rule with a rigorous second-order remainder:
  int_cell f = h f(xm) + R,  R in (h^3/12) * hull(f''/2 over cell)  (integral form of Taylor; hull is a rectangle).
f''/2 is enclosed by order-2 Taylor jets in x over complex intervals. Cells where sqrt's argument touches the cut
(-inf, 0] fall back to a zeroth-order bound int_cell f in h * hull(f over cell), or a modulus disk."""
import mpmath as mp
iv = mp.iv; iv.dps = 20
def lo(x): return mp.mpf(x.a)
def hi(x): return mp.mpf(x.b)
class C:
    __slots__ = ('re', 'im')
    def __init__(s, re, im=None): s.re = re if isinstance(re, type(iv.mpf(0))) else iv.mpf(re); s.im = iv.mpf(0) if im is None else (im if isinstance(im, type(iv.mpf(0))) else iv.mpf(im))
    def __add__(s, o): o = cc(o); return C(s.re + o.re, s.im + o.im)
    __radd__ = __add__
    def __sub__(s, o): o = cc(o); return C(s.re - o.re, s.im - o.im)
    def __neg__(s): return C(-s.re, -s.im)
    def __mul__(s, o): o = cc(o); return C(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    __rmul__ = __mul__
    def abs2(s): return s.re**2 + s.im**2
    def inv(s):
        d = s.abs2()
        if not d.a > 0: raise ZeroDivisionError
        return C(s.re/d, -s.im/d)
    def hull(s, o): return C(iv.mpf([min(lo(s.re), lo(o.re)), max(hi(s.re), hi(o.re))]), iv.mpf([min(lo(s.im), lo(o.im)), max(hi(s.im), hi(o.im))]))
def cc(o): return o if isinstance(o, C) else C(iv.mpf(o))
class CutError(Exception): pass
def csqrt(z):
    """principal sqrt enclosure if z avoids (-inf, 0]; else CutError"""
    X, Y = z.re, z.im
    if not (X.a > 0 or Y.a > 0 or Y.b < 0): raise CutError
    R = iv.sqrt(z.abs2()); RX = R + X
    low = max(lo(RX), mp.mpf(0))
    if lo(X) > 0: low = max(low, 2*lo(X))
    else:
        den = hi(R - X)
        if den > 0: low = max(low, lo(Y*Y)/den*(1 - mp.mpf(10)**-15))
    if not (hi(RX) > 0 and low > 0): raise CutError
    U = iv.sqrt(iv.mpf([low, hi(RX)])/2)
    if not U.a > 0: raise CutError
    return C(U, Y/(2*U))
# --- order-2 jets: (c0, c1, c2) = (f, f', f''/2), entries C ---
class J:
    __slots__ = ('c',)
    def __init__(s, c0, c1=None, c2=None): s.c = (cc(c0), cc(0) if c1 is None else cc(c1), cc(0) if c2 is None else cc(c2))
    def __add__(s, o):
        o = jj(o); return J(*(a + b for a, b in zip(s.c, o.c)))
    __radd__ = __add__
    def __sub__(s, o):
        o = jj(o); return J(*(a - b for a, b in zip(s.c, o.c)))
    def __mul__(s, o):
        o = jj(o); a, b = s.c, o.c
        return J(a[0]*b[0], a[0]*b[1] + a[1]*b[0], a[0]*b[2] + a[1]*b[1] + a[2]*b[0])
    __rmul__ = __mul__
    def inv(s):
        c0, c1, c2 = s.c; r0 = c0.inv(); r1 = -(c1*r0*r0); r2 = -((c1*r1 + c2*r0)*r0)
        return J(r0, r1, r2)
    def sqrt(s):
        c0, c1, c2 = s.c; s0 = csqrt(c0); i2 = (s0*2).inv(); s1 = c1*i2; s2 = (c2 - s1*s1)*i2
        return J(s0, s1, s2)
def jj(o): return o if isinstance(o, J) else J(cc(o))
def coeffs(th):
    return 21*(1 - th), iv.mpf(120)/7*th - 18*(1 - th), 1 + iv.mpf(33)/7*th
def uinv2(X, E):
    """1/u^2 for u = X + iE as C: conj(u)^2/|u|^4"""
    n2 = X**2 + E**2; n4 = n2*n2
    return C((X**2 - E**2)/n4, -2*X*E/n4)
def f_point(xpt, th, X, E):
    """C enclosure of integrand at x (interval or point) over the param box (zeroth order)"""
    a, b, g = coeffs(th); ui2 = uinv2(X, E)
    x = iv.mpf(xpt); t = C(x*x)*ui2; Q = t*b + t*t*g + a
    Phi = (ui2 + 1)*((t + 1)*(t + 1)*(t + 1)).inv()
    return C(x*(1 - x))*Phi*csqrt(Q)
def f_jet(xcell, th, X, E):
    a, b, g = coeffs(th); ui2 = uinv2(X, E)
    xj = J(C(xcell), C(1), C(0))
    t = xj*xj*J(ui2)
    Q = t*J(C(b)) + t*t*J(C(g)) + J(C(a))
    tp1 = t + 1
    Phi = J(ui2 + 1)*(tp1*tp1*tp1).inv()
    w = xj*(J(C(1)) - xj)
    return w*Phi*Q.sqrt()
def f_modbound(xcell, th, X, E):
    a, b, g = coeffs(th); ui2 = uinv2(X, E)
    x = xcell; t = C(x*x)*ui2; Q = t*b + t*t*g + a
    Phi = (ui2 + 1)*((t + 1)*(t + 1)*(t + 1)).inv()
    B = iv.mpf(hi(x*(1 - x)))*iv.sqrt(Phi.abs2())*iv.sqrt(iv.sqrt(Q.abs2()))
    return hi(B)
def H_enclose(th, X, E, M):
    """C enclosure of H_theta(u) over the parameter box, with M x-cells"""
    re = iv.mpf(0); im = iv.mpf(0); h = mp.mpf(1)/M
    for i in range(M):
        x0, x1 = mp.mpf(i)/M, mp.mpf(i + 1)/M; xc = iv.mpf([x0, x1]); xm = (x0 + x1)/2
        try:
            fm = f_point(xm, th, X, E); jet = f_jet(xc, th, X, E)
            R = jet.c[2]*(h**3/12)
            cell = fm*h + R
        except (CutError, ZeroDivisionError):
            try:
                fz = f_point(xc, th, X, E); cell = fz*h
            except (CutError, ZeroDivisionError):
                B = f_modbound(xc, th, X, E)*h; cell = C(iv.mpf([-B, B]), iv.mpf([-B, B]))
        re += cell.re; im += cell.im
    s = iv.sqrt(iv.mpf(8)/5)
    return C(s*re, s*im)
def H_float(theta, X, E, dps=25):
    mp.mp.dps = dps; u = mp.mpc(X, E)
    a, b, g = 21*(1 - theta), mp.mpf(120)/7*theta - 18*(1 - theta), 1 + mp.mpf(33)/7*theta
    f = lambda x: x*(1 - x)*(1 + u**-2)/(1 + x*x/u**2)**3*mp.sqrt(a + b*x*x/u**2 + g*(x*x/u**2)**2)
    return mp.sqrt(mp.mpf(8)/5)*mp.quad(f, [0, 0.5, 1])
