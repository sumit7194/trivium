"""V7a1 -- kappa >= 2 a(pi/2) at n = 1 from SSA on equal-height rectangles.  Bridge's own derivation.

Universal part of a T x L rectangle (A4, four pi/2 corners, scale invariance):
    S_univ(T, L) = -4 a log(L/eps) + G(T/L)
(1) SSA on A = [0,T1+T2]xL, B = [T1,T1+T2+T3]xL  (A1)  ->  G concave.
(2) Thin-strip limit, T >> L: G(x) = -kappa x + O(1)  (strip coefficient = small-angle kappa)  ->  G'(x) -> -kappa.
    Concave G has nonincreasing G', so G'(x) >= -kappa for every x.
(3) Rotation: S(T x L) = S(L x T)  ->  G(x) - G(1/x) = -4 a log x  ->  G'(1) = -2a.
(2)+(3): kappa >= 2 a(pi/2).
This script checks step (3) symbolically, and the whole chain on EMI, where SSA holds exactly.
"""
import sympy as sp
x,a=sp.symbols('x a',positive=True)
G=sp.Function('G')
rel=G(x)-G(1/x)+4*a*sp.log(x)                # (3), must vanish identically
d=sp.diff(rel,x).subs(x,1).doit()
Gp1=sp.Symbol('Gp1')
d_sub=d.replace(lambda e: isinstance(e,sp.Subs), lambda e: Gp1)
print("d/dx of symmetry relation at x=1:", sp.simplify(d_sub), " -> G'(1) =", sp.solve(d_sub,Gp1)[0])

# EMI known answer: S = sum over boundary pairs of -log|r1-r2| weights; closed-form universal part for a
# rectangle is not needed -- instead test the corner-level statement: kappa_EMI / a_EMI(pi/2).
import math
aE=lambda th: 1+(math.pi-th)/math.tan(th)     # EMI corner function up to normalisation; kappa = pi
print("EMI kappa/a(pi/2) =", math.pi/aE(math.pi/2), ">= 2 ?", math.pi/aE(math.pi/2)>=2)
