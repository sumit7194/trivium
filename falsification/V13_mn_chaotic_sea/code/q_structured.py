"""Structured form of the MN polynomial Q (bridge cross-check for quantum's MN field-width fix, 2026-10-21).
Q is defined by (x^2-1)(1-y^2) B^2 - 4 C^2 = A Q (exact polynomial division in x, y, a, b; v13_field._polys).
Claim (proved below by exact symbolic expansion):
    Q = (1 - y^2) X^2 - (x^2 - 1) Y^2 + 4 a b (x^2 - 1)(1 - y^2)^2,
    X = (x + 1)^2 + a b (x - 1)^2,   Y = a (1 + y)^2 + b (1 - y)^2.
The 46-term expanded polynomial becomes 3 structured products; the derivatives follow by the product rule."""
import sympy as sp, mpmath as mp, random
x, y, a, b = sp.symbols('x y a_s b_s')
Am = (x**2 - 1)*(1 + a*b)**2 - (1 - y**2)*(b - a)**2
Bm = (x + 1 + (x - 1)*a*b)**2 + ((1 + y)*a + (1 - y)*b)**2
Cm = (x**2 - 1)*(1 + a*b)*(b - a - y*(a + b)) + (1 - y**2)*(b - a)*(1 + a*b + x*(1 - a*b))
Q, r = sp.div(sp.expand((x**2 - 1)*(1 - y**2)*Bm**2 - 4*Cm**2), Am, x, y, a, b)
assert r == 0
X = (x + 1)**2 + a*b*(x - 1)**2
Y = a*(1 + y)**2 + b*(1 - y)**2
Qs = (1 - y**2)*X**2 - (x**2 - 1)*Y**2 + 4*a*b*(x**2 - 1)*(1 - y**2)**2
print("exact identity Q == structured form:", sp.expand(Q - Qs) == 0)
print("terms: expanded", len(sp.expand(Q).as_ordered_terms()), " structured: 3 products")
# point-value gate at 80 digits (redundant given the exact identity, kept as a numerical cross-check of the transcription)
mp.mp.dps = 80; f1 = sp.lambdify((x, y, a, b), Q, 'mpmath'); f2 = sp.lambdify((x, y, a, b), Qs, 'mpmath')
random.seed(7); worst = mp.mpf(0)
for _ in range(50):
    v = [mp.mpf(random.uniform(1.01, 6)), mp.mpf(random.uniform(-0.99, 0.99)), mp.mpf(random.uniform(-5, 5)), mp.mpf(random.uniform(-5, 5))]
    q1 = f1(*v); worst = max(worst, abs(q1 - f2(*v)) / max(abs(q1), mp.mpf(1)))
print("80-digit point gate, worst relative difference over 50 points:", mp.nstr(worst, 3))
# Kerr check: for beta = 0 the MN a, b are constants (-alpha, alpha); report Q there in structured form

# ---- Notes (2026-10-21, bridge, for quantum's MN field fix; post hoc diagnostics, no verdicts) ----
# At quantum's t = 291 point (x 1.94376, y 0.10345; a = 0.74096, b = -3.22935 from the exact F5-R a, b), with a 1e-6
# box in x, y, a, b (a, b tight), interval width / true linear range:
#   A as written in v13 (two squares) 2.26 vs expanded 6.78;  B as written (two squares) 1.30 vs expanded 11.64;
#   C as written 4.89 vs expanded 8.92; regrouped C2 = (x+y) b [(x+1)(1-y) - (x-1)(1+y) a^2]
#   + (x-y) a [(x-1)(1-y) b^2 - (x+1)(1+y)] (exact) gives 3.59 there but is not uniformly better (2.1-5.5 elsewhere).
# => keep the v13 grouped forms of A, B, C verbatim in codegen (do not expand; check CSE does not undo the grouping).
# ea, eb: Legendre generating function, R^2 - 2uR + 1 = (x-y)^2 and R^2 + 2uR + 1 = (x+y)^2 (verified), so
#   (x-y) sum_{l>=0} P_l(u)/R^{l+1} = 1  and  (x+y) sum_{l>=0} (-1)^l P_l(u)/R^{l+1} = 1, hence
#   ea = -(x-y) sum_{l>=3} P_l(u)/R^{l+1},   eb = (x+y) sum_{l>=3} (-1)^l P_l(u)/R^{l+1}:
#   the small values are TAILS of convergent series (ratio 1/R ~ 0.6 at the swing). The O(1) cancellation is intrinsic
#   to the 3-term truncation; there is no smooth closed form without it -> keep a, b as augmented states.
