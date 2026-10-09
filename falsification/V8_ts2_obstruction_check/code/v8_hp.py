"""V8-mono HP: high-precision transport for the TS bound-orbit rows (PREREG_TS_V2_MONODROMY.md, HP addendum).
Same equations as v8_ts_monodromy (the bridge's own V8 builder); p(x), q(x) reduced exactly to rational functions in x
(sympy cancel in x, which is small: degrees <= 12), then the xi1 ODE in t, y'' + p_t y' + q_t y = 0 with
p_t = x' p(x(t)) - x''/x', q_t = x'^2 q(x(t)), x = (t + 1/t)/2, is transported by a Taylor-series method in mpmath:
at each centre the coefficient series are computed exactly (truncated series arithmetic), the solution series from the
recurrence y_{n+2} = -[sum_j p_j (n-j+1) y_{n-j+1} + q_j y_{n-j}] / ((n+2)(n+1)), and the step is a fixed fraction of the
distance to the nearest singular point (roots of the denominators mapped to t, plus t = 0, +-1)."""
import sys, json, time, sympy as sp, mpmath as M
sys.argv = sys.argv[:1] + sys.argv[1:]
from v8_ts_monodromy import coeffs, ROWS, x

def rational_parts(tag, E, L, mu2):
    pc, qc, _, _ = coeffs(tag, E, L, mu2)
    out = []
    for e in (pc, qc):
        n, d = sp.fraction(sp.cancel(sp.together(e)))
        out.append((sp.Poly(n, x).all_coeffs(), sp.Poly(d, x).all_coeffs()))
    return out   # [(p_num, p_den), (q_num, q_den)], highest degree first, exact rationals

class Series:
    def __init__(self, K): self.K = K
    def mul(self, a, b):
        K = self.K; c = [M.mpc(0)] * K
        for i, ai in enumerate(a):
            if ai == 0: continue
            for j in range(K - i): c[i + j] += ai * b[j]
        return c
    def inv(self, a):
        K = self.K; b = [M.mpc(0)] * K; b[0] = 1 / a[0]
        for n in range(1, K): b[n] = -sum(a[k] * b[n - k] for k in range(1, n + 1)) / a[0]
        return b
    def poly_at(self, coeffs, xs):            # Horner on a series argument
        r = [M.mpc(0)] * self.K
        for c in coeffs:
            r = self.mul(r, xs); r[0] += c
        return r

def make_stepper(parts, K):
    S = Series(K)
    (pn, pd), (qn, qd) = [[[M.mpf(sp.Rational(c).p) / sp.Rational(c).q for c in cs] for cs in pr] for pr in parts]
    def step(t0, h, y, dy):
        # series of x(t0 + u): (t0 + u)/2 + 1/(2 (t0 + u)); x' and x''/x' likewise
        inv_t = [(-1) ** k / t0 ** (k + 1) for k in range(K)]
        xs = [(t0 + inv_t[0]) / 2, (1 + inv_t[1]) / 2] + [inv_t[k] / 2 for k in range(2, K)]
        x1 = [(xs[k + 1] * (k + 1)) for k in range(K - 1)] + [M.mpc(0)]            # dx/dt series
        x2 = [(x1[k + 1] * (k + 1)) for k in range(K - 1)] + [M.mpc(0)]            # d2x/dt2 series
        P = S.mul(S.mul(x1, S.poly_at(pn, xs)), S.inv(S.poly_at(pd, xs)))
        P = [P[k] - v for k, v in enumerate(S.mul(x2, S.inv(x1)))]
        Q = S.mul(S.mul(S.mul(x1, x1), S.poly_at(qn, xs)), S.inv(S.poly_at(qd, xs)))
        out = []
        for (a0, a1) in ((y[0], dy[0]), (y[1], dy[1])):
            c = [a0, a1]
            for n in range(K - 2):
                s = sum(P[j] * (n - j + 1) * c[n - j + 1] + Q[j] * c[n - j] for j in range(n + 1))
                c.append(-s / ((n + 2) * (n + 1)))
            val = M.polyval(c[::-1], h); der = M.polyval([k * c[k] for k in range(K - 1, 0, -1)], h)
            out.append((val, der))
        return (out[0][0], out[1][0]), (out[0][1], out[1][1])
    return step

def singular_points(parts):
    pts = [M.mpc(0), M.mpc(1), M.mpc(-1)]
    for num, den in parts:
        dc = [M.mpf(sp.Rational(c).p) / sp.Rational(c).q for c in den]
        if len(dc) > 1:
            for xr in M.polyroots(dc, maxsteps=200, extraprec=200):
                s = M.sqrt(xr * xr - 1); pts += [xr + s, xr - s]
    return pts

def transport(step, sing, path, frac):
    y, dy = (M.mpc(1), M.mpc(0)), (M.mpc(0), M.mpc(1))
    for z0, z1 in zip(path[:-1], path[1:]):
        t = z0; d = z1 - z0
        while abs(z1 - t) > 0:
            R = min(abs(t - s) for s in sing); h = min(abs(z1 - t), frac * R)
            hc = d / abs(d) * h
            y, dy = step(t, hc, y, dy); t = t + hc
            if abs(z1 - t) < M.mpf(10) ** (-M.mp.dps + 5): t = z1; break
    return M.matrix([[y[0], y[1]], [dy[0], dy[1]]])

def loop_path(base, c, rho):
    phi0 = M.arg(base - c)
    return [base] + [c + rho * M.expjpi(2 * (phi0 / (2 * M.pi) + M.mpf(j) / 16)) for j in range(17)] + [base]

def invariants(Ms, gw, hw):
    g, h = Ms[gw[0]] * Ms[gw[1]], Ms[hw[0]] * Ms[hw[1]]
    inv = lambda G: (G[0, 0] + G[1, 1]) ** 2 / M.det(G)
    cm = g * h * M.inverse(g) * M.inverse(h)
    return dict(inv_g=inv(g), inv_h=inv(h), comm=cm[0, 0] + cm[1, 1])

def run(row, dps, K, frac):
    M.mp.dps = dps
    tag, (E, L, mu2), base, loops, gw, hw, tg = ROWS[row]
    parts = rational_parts(tag, E, L, mu2)
    step = make_stepper(parts, K); sing = singular_points(parts)
    Ms = {k: transport(step, sing, loop_path(M.mpc(base), M.mpc(c), M.mpf(r)), frac) for k, (c, r) in loops.items()}
    return invariants(Ms, gw, hw), tg

if __name__ == '__main__':
    out = {}
    for row in sys.argv[1:]:
        row = row if row.startswith('C') else int(row); t0 = time.time()
        lo, tg = run(row, 30, 60, M.mpf('0.3')); hi, _ = run(row, 40, 80, M.mpf('0.25'))
        conv = max(abs(hi[k] / lo[k] - 1) for k in hi)
        tgt = dict(inv_g=tg[0], inv_h=tg[1], comm=tg[2])
        agree = max(abs(hi[k] / M.mpc(tgt[k]) - 1) for k in hi)
        verdict = ('REPRODUCED' if agree < 1e-12 else 'DISAGREES' if agree > 1e-8 else 'INCONCLUSIVE') if conv < 1e-20 else 'INCONCLUSIVE'
        print(f'row {row}: conv {M.nstr(conv, 3)}  agree {M.nstr(agree, 3)}  tr[g,h]={M.nstr(hi["comm"], 18)}  '
              f'inv_h={M.nstr(hi["inv_h"], 14)}  -> {verdict}  ({time.time() - t0:.0f}s)', flush=True)
        out[str(row)] = dict(conv=str(conv), agree=str(agree), verdict=verdict, values={k: str(v) for k, v in hi.items()})
    json.dump(out, open('../results/v8_hp_' + '_'.join(sys.argv[1:]) + '.json', 'w'), indent=1)
