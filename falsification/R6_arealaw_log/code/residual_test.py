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
    rows.append((name, coef[1], sgn, ch, np.abs(res).max()))
    print(f"  {name:<16} {coef[1]:10.4f}  {sgn:<12} {ch:7d}  {np.abs(res).max():10.3e}")

print(f"\n  {len(ns)} points. Scatter would give roughly {len(ns)//2} sign changes.")
few = [r for r in rows if r[3] <= 3]
if few:
    print(f"  -> {len(few)}/{len(rows)} regulators show <=3 changes: SMOOTH ARC, the")
    print(f"     3-parameter form is missing a term and b is absorbing part of it.")
    print(f"     That is R6's own pre-registered UNDECIDED cause, now MEASURED.")
else:
    print(f"  -> all regulators scatter: the 3-parameter form is adequate, and R6's")
    print(f"     pre-registered fold-into-b cause is RULED OUT as the explanation.")
