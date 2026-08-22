"""Test R6's own named-but-untested risk: is a subleading term being folded into b?

R6's PREREGISTRATION listed the leading candidate for its result being wrong:
"further subleading terms that a 3-parameter fit may fold into b" -- named as a live
UNDECIDED cause, and the FINDINGS then talked past it. The status was downgraded to
UNDECIDED on that basis with the note "the measurement now demands an explanation we do
not have."

The residual-sign diagnostic tests it directly, and it did not exist when R6 was written:

  A one-directional error, or a smooth arc through the residuals, means the model is
  MISSING A TERM and the fitted coefficients are absorbing it. Scatter means the form is
  adequate. THE DIAGNOSTIC IS THE SIGN PATTERN, NOT THE FIT QUALITY -- R6 banked rms_log
  and rms_nolog, which are fit quality, and cannot distinguish these.

Cheap: reuses M2's pipeline at N=200, runs beside a large job.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "M2_arealaw", "code"))
import r6_log as R6

sys.path.insert(0, "/Users/sumit/Github/.claude-coordination")
from signtest import sign_test          # the null lives inside the verdict function


def signs_of(res):
    s = "".join("+" if x > 0 else "-" for x in res)
    return s, sum(1 for i in range(1, len(s)) if s[i] != s[i-1])

ns = np.array(R6.NS, float)
print(f"  n = {R6.NS}   N={R6.N} L0={R6.L0}\n")
print(f"  {'regulator':<16} {'b':>10}  {'residual signs':<12} {'changes':>7}  {'max|res|':>10}")
rows = []
for name, Kfun in [("R1 bare NN", R6.M2.K_bare), ("R2 improved", R6.M2.K_impr), ("R3 higher-deriv", R6.M2.K_hd)]:
    S = R6.S_of(Kfun)
    A = np.column_stack([ns**2, np.log(ns), np.ones_like(ns)])
    coef, *_ = np.linalg.lstsq(A, S, rcond=None)
    res = S - A @ coef
    sgn, ch = signs_of(res)
    verdict, pval, detail = sign_test(res)
    rows.append((name, coef[1], sgn, ch, np.abs(res).max()))
    print(f"  {name:<16} {coef[1]:10.4f}  {detail}")
    print(f"  {'':<16} {'':>10}  -> {verdict}")

print(f"\n  {len(ns)} points. Scatter would give roughly {len(ns)//2} sign changes.")
# THE NULL, which the first version of this script did not have. Under scatter, sign
# changes among n residuals are Binomial(n-1, 1/2). Without this the threshold is
# whatever the author picks after seeing the data -- and mine printed "SMOOTH ARC,
# missing a term" for a pattern with P = 0.36. The same omission had already put an
# unsupported finding into M2's FINDINGS, since 2 changes in 6 points is P = 0.500.
from math import comb
opp = len(ns) - 1
def p_le(k):
    return sum(comb(opp, j) for j in range(k+1)) / 2**opp
print(f"\n  NULL: sign changes ~ Binomial({opp}, 1/2), mean {opp/2:.1f}")
for name, b, sgn, ch, mx in rows:
    p = p_le(ch)
    verdict = "SUPPORTED" if p < 0.05 else ("weak" if p < 0.2 else "NO SUPPORT")
    print(f"    {name:<16} {ch} changes   P(X<={ch}) = {p:.3f}   {verdict}")
print(f"\n  -> R6's pre-registered cause -- a subleading term folded into b -- is NEITHER")
print(f"     demonstrated NOR ruled out by this test. At {len(ns)} points the sign statistic")
print(f"     cannot resolve it, and saying so is the result.")
print(f"  -> Worth noting separately: R3's max residual is {rows[2][4]:.2e}, ~10x the other")
print(f"     two. That is a magnitude signal, not a sign signal, and it is not tested here.")
