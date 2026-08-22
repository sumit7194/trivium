"""Fit the entropy-phase memory law and HOLD-OUT VALIDATE it.

The s=6 decision rests entirely on extrapolating this law one step beyond the measured
range. An unvalidated extrapolation is what produced my retracted 7.31-9.37 GB range,
and before that ansatz's 4.75 GiB/prime. So the law is not quoted without the hold-out
errors beside it. (Method: quantum. In a committed script rather than a heredoc, which
is the other thing today keeps teaching.)

Data: one point per FRESH process, current RSS, baseline subtracted -- ru_maxrss and a
reused interpreter both corrupt this, see PEAK_MEASUREMENT.md.
"""
import math, sys

# (l, entropy-phase peak in GB), s=5, regulator nn
PTS = [(40, 0.229), (50, 0.477), (60, 0.928), (70, 1.669), (80, 2.808), (100, 6.539)]

def fit(pts):
    """Power law through the log-log least-squares line. Returns (exponent, prefactor)."""
    n = len(pts)
    xs = [math.log(l) for l, _ in pts]; ys = [math.log(p) for _, p in pts]
    mx, my = sum(xs)/n, sum(ys)/n
    k = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
    return k, math.exp(my - k*mx)

print("HOLD-OUT VALIDATION — fit on the points below the cut, predict the next one\n")
print("   cut   fitted on        exp    predicted    measured    error")
worst = 0.0
for i in range(3, len(PTS)):
    train, (lh, ph) = PTS[:i], PTS[i]
    k, a = fit(train)
    pred = a * lh**k
    err = 100*abs(pred-ph)/ph
    worst = max(worst, err)
    print(f"  l<{lh:<4} {str([l for l,_ in train]):<16} {k:5.2f}   "
          f"{pred:7.3f} GB   {ph:7.3f} GB   {err:5.1f}%")

k, a = fit(PTS)
print(f"\n  full fit: exponent {k:.2f}, prefactor {a:.3e}")
print(f"  structural expectation is 4 (matrices are n x n with n = l^2, so mem ~ n^2 = l^4)")
print(f"  worst one-step hold-out error: {worst:.1f}%\n")

for s, lmax in ((5, 100), (6, 120)):
    p = a * lmax**k
    band = p * (1 + worst/100)
    print(f"  s={s} (l={lmax}): {p:6.2f} GB   worst-case-error band up to {band:6.2f} GB")
# The free power law's hold-out errors were 6.7 / 6.8 / 6.7 percent -- SAME SIZE, SAME
# DIRECTION every time. A one-directional error of constant magnitude is a mis-specified
# model, not measurement scatter: the fitted exponent keeps landing below the true local
# one because the pure power law has no room for the fixed overhead. So test the
# STRUCTURAL form instead -- exponent FIXED at 4 from n = l^2, fitting only scale and
# offset. Fewer free parameters, and it should win if the structural claim is right.

def fit_structural(pts):
    """p = a*l^4 + c. Exponent is NOT fitted -- it comes from the matrix structure."""
    n = len(pts); X = [l**4 for l, _ in pts]; Y = [p for _, p in pts]
    mx, my = sum(X)/n, sum(Y)/n
    a = sum((x-mx)*(y-my) for x, y in zip(X, Y)) / sum((x-mx)**2 for x in X)
    return a, my - a*mx

print("\nSTRUCTURAL FORM — exponent fixed at 4, only scale and offset fitted\n")
worst_s = 0.0
for i in range(3, len(PTS)):
    train, (lh, ph) = PTS[:i], PTS[i]
    aa, cc = fit_structural(train)
    pred = aa*lh**4 + cc
    err = 100*abs(pred-ph)/ph; worst_s = max(worst_s, err)
    print(f"  fit l<{lh:<4} -> predict {pred:6.3f} GB   measured {ph:6.3f} GB   {err:4.1f}%")
aa, cc = fit_structural(PTS)
print(f"\n  a = {aa:.3e}   c = {cc:+.3f} GB (fixed overhead)")
print(f"  worst hold-out: {worst_s:.1f}%   vs {worst:.1f}% for the free power law, "
      f"whose errors were all one-directional")
print(f"  THE MODEL WITH FEWER FREE PARAMETERS PREDICTS BETTER -- which is the evidence")
print(f"  that l^4 is the mechanism and not merely a good fit.")
print(f"\n  s=6 (l=120) structural: {aa*120**4+cc:6.2f} GB")
print(f"  s=6 (l=120) free law  : {a*120**k:6.2f} GB")
print(f"  s=6, quantum's independent study, different code: 14.4 GB")
print("\n  Best box reading of the day: 7.0 GB free / 10.1 GB available.")
print("  Three estimates spanning 12.4-14.4 GB. s=6 misses on every one of them.")
