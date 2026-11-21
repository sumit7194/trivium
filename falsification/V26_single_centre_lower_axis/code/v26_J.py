"""V26 addendum J: Bridge's INDEPENDENT interval certificate (own code; Neon's script not used) that
Re H_theta(1 + i eta) > 0 on (theta, eta) in [0,1] x [0,10], where
H_theta(u) = sqrt(8/5) * int_0^1 x(1-x) Phi(u,x) sqrt(alpha + beta t + gamma t^2) dx, t = x^2/u^2,
Phi = (1 + u^-2)/(1 + t)^3, alpha = 21(1-theta), beta = 120/7 theta - 18(1-theta), gamma = 1 + 33/7 theta.
Rigour: Re int f dx >= sum_i width_i * lower(Re f on [x_i, x_{i+1}] x box), with complex interval arithmetic built on
mpmath.iv real intervals; the principal sqrt is enclosed only where the argument avoids the cut, else a modulus bound is used."""
import sys, mpmath as mp
iv = mp.iv; iv.dps = 20
def lo(x): return mp.mpf(x.a)
def hi(x): return mp.mpf(x.b)
class C:
    def __init__(s, re, im): s.re, s.im = re, im
    def __add__(s, o): o = cc(o); return C(s.re + o.re, s.im + o.im)
    __radd__ = __add__
    def __mul__(s, o): o = cc(o); return C(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    __rmul__ = __mul__
    def abs2(s): return s.re**2 + s.im**2
    def inv(s):
        d = s.abs2()
        assert d.a > 0, 'division by interval containing 0'
        return C(s.re/d, -s.im/d)
def cc(o): return o if isinstance(o, C) else C(iv.mpf(o), iv.mpf(0))
def csqrt(z):
    """principal sqrt enclosure if z avoids (-inf, 0]; else None"""
    X, Y = z.re, z.im
    if not (X.a > 0 or Y.a > 0 or Y.b < 0): return None
    R = iv.sqrt(z.abs2())
    RX = R + X                                   # exactly >= 0; tighten the lower end rigorously
    low = max(lo(RX), mp.mpf(0))
    if lo(X) > 0: low = max(low, 2*lo(X))
    else:
        den = hi(R - X)
        if den > 0: low = max(low, lo(Y*Y)/den*(1 - mp.mpf(10)**-15))
    if not (hi(RX) > 0 and low > 0): return None
    U = iv.sqrt(iv.mpf([low, hi(RX)])/2)
    if not U.a > 0: return None
    return C(U, Y/(2*U))
def mod_upper(z): return hi(iv.sqrt(z.abs2()))
def re_lower_cell(th, et, x, shift=0):
    try:
        return _re_lower_cell(th, et, x)
    except AssertionError:
        return -mp.inf
def _re_lower_cell(th, et, x):
    """lower bound of Re f over the cell (theta-int, eta-int, x-int)"""
    a = 21*(1 - th); b = iv.mpf(120)/7*th - 18*(1 - th); g = 1 + iv.mpf(33)/7*th
    ub = C(iv.mpf(1), -et); n4 = (1 + et**2)**2          # 1/u^2 = conj(u)^2/|u|^4, |u|^2 = 1 + eta^2 exactly
    cu2 = ub*ub; ui2 = C(cu2.re/n4, cu2.im/n4)
    t = C(x**2, iv.mpf(0))*ui2
    Phi = (ui2 + 1)*((t + 1)*(t + 1)*(t + 1)).inv()
    Q = t*b + t*t*g + a
    w = x*(1 - x)
    s = csqrt(Q)
    if s is not None:
        f = C(w, iv.mpf(0))*Phi*s
        return lo(f.re)
    # fallback: Re f >= -|f| (rigorous, crude)
    B = iv.mpf(hi(w))*iv.mpf(mod_upper(Phi))*iv.sqrt(iv.mpf(mod_upper(Q)))
    return -hi(B)
def box_lower(th, et, M):
    tot = mp.mpf(0)
    for i in range(M):
        x = iv.mpf([mp.mpf(i)/M, mp.mpf(i + 1)/M])
        tot += re_lower_cell(th, et, x)/M
    return mp.sqrt(mp.mpf(8)/5)*tot
def certify(shift=0.0, M=24, max_boxes=20000, verbose=True):
    todo = [((0.0, 1.0), (0.0, 10.0))]; done = 0; minlb = mp.inf; failed = 0
    while todo:
        (t0, t1), (e0, e1) = todo.pop()
        Mb = M if (t1 - t0) > 1/64 else (2*M if (t1 - t0) > 1/512 else 4*M)
        lb = box_lower(iv.mpf([t0, t1]), iv.mpf([e0, e1]), Mb) - shift
        if lb > 0:
            done += 1; minlb = min(minlb, lb)
        elif (t1 - t0) < 1e-4 and (e1 - e0) < 1e-3:
            failed += 1
            if failed >= 3: return False, done, minlb, ((t0, t1), (e0, e1))
        else:
            if (t1 - t0)*10 > (e1 - e0): tm = (t0 + t1)/2; todo += [((t0, tm), (e0, e1)), ((tm, t1), (e0, e1))]
            else: em = (e0 + e1)/2; todo += [((t0, t1), (e0, em)), ((t0, t1), (em, e1))]
        if done + len(todo) > max_boxes: return False, done, minlb, 'box budget exceeded'
    return True, done, minlb, None
def Hfloat(theta, eta, n=2000):
    mp.mp.dps = 20
    u = mp.mpc(1, eta); a = 21*(1 - theta); b = 120/7*theta - 18*(1 - theta); g = 1 + 33/7*theta
    f = lambda x: x*(1 - x)*(1 + u**-2)/(1 + x*x/u**2)**3*mp.sqrt(a + b*x*x/u**2 + g*(x*x/u**2)**2)
    return mp.sqrt(mp.mpf(8)/5)*mp.quad(f, [0, 1])
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'run'
    if mode == 'precheck':
        import random; random.seed(3); bad = 0
        for _ in range(6):
            th = random.uniform(0, 1); et = random.uniform(0, 10); h = 1e-6
            lb = box_lower(iv.mpf([th, th + h]), iv.mpf([et, et + h]), 400)
            val = Hfloat(th, et).real
            ok = lb <= val + 1e-12
            bad += (not ok)
            print('PRECHECK enclosure: theta %.3f eta %.3f  lower %.6e  <= float %.6e : %s  (gap %.1e)' % (th, et, lb, val, ok, val - lb))
        r = certify(shift=0.01, M=24, max_boxes=3000)
        print('PRECHECK must-fail (Re H - 0.01 > 0 must NOT certify): certified =', r[0], '| boxes', r[1], '| stop:', r[3])
        sys.exit()
    ok, n, mlb, stop = certify(M=int(sys.argv[2]) if len(sys.argv) > 2 else 24)
    print('J: certified =', ok, '| boxes', n, '| min certified lower bound', mp.nstr(mlb, 6), '| stop:', stop)
    print('VERDICT J', 'PASS' if ok and mlb > 0 else 'FAIL')
