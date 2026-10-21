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
