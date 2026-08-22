"""s=6 k=0 deletion pass: bound the non-common zero-mode residual at the new rung.

SETUP CORRESPONDENCE (PROTOCOL 20, pre-registered, checkable without seeing the data):
  This runs at the condition the published result runs at, namely l/L = 0.025..0.125,
  the study's own grid, obtained as l = [int(f*L) for f in FRACS] with L = 960.
  It does NOT hold l fixed across resolutions -- that was the error in
  zeromode_scaling.py, which measured a condition the study never operates in.

WHAT IS BEING MEASURED, and why it is not the total shift:
  The corner spread is a DIFFERENCE across regulators, so any part of the zero-mode
  contribution that is common to all four cancels exactly. Only the NON-COMMON residual
  can contaminate it. quantum measures theirs at 22-41% of the regulator signal across
  s=1,2,3 with no trend. This produces the same ratio at s=6, from a different codebase,
  for an honest comparison.

    signal      = max-min of B across the four regulators          (what the claim is about)
    shift_r     = B_with(r) - B_without(r)                          (per regulator)
    non_common  = max-min of shift_r across the four regulators     (what can contaminate)
    ratio       = non_common / signal

REGISTERED OUTCOMES -- and per quantum, checked for a SHARED PREMISE rather than merely
enumerated. All three below vary only the measured ratio; none assumes anything about
how the mode enters B, because that question is already settled analytically
(log(c*l^2) = log c + 2 log l, so the L-dependence moves the constant).
    ratio << quantum's 22-41%  -> the systematic shrinks at high s; the spread means
                                  more at the resolutions the claim relies on
    ratio within 22-41%        -> stable systematic, bound confirmed at a 6th rung
    ratio >> 41%               -> grows with refinement; the spread at high s is
                                  increasingly not measuring regulator difference

NOTE ON POWER: four regulators give a 4-point max-min for both signal and non-common.
That is a small sample and the ratio is a ratio of two ranges -- report it, do not
build a trend on it. (PROTOCOL 20a: if it is too thin to act on, do not send the number
as a result.)
"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import REG, entropy
from extract import fit

L, m = 960, 1/600.
FRACS = [0.025, 0.05, 0.075, 0.1, 0.125]
LS = [int(round(f*L)) for f in FRACS]
REGS = ("nn", "improved", "higher_deriv", "smeared")

def corr(reg, drop):
    k = 2*np.pi*np.fft.fftfreq(L)
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.sqrt(REG[reg](KX, KY, m*m))
    a, b = 1.0/(2.0*w), w/2.0
    if drop: a[0, 0] = 0.0; b[0, 0] = 0.0
    return np.fft.ifft2(a).real, np.fft.ifft2(b).real

print(f"s=6  L={L}  m*L={m*L:.2f}  l/L={FRACS}  ->  l={LS}", flush=True)
print(f"  correspondence: this IS the study's grid, not fixed-l\n", flush=True)
Bw, Bo = [], []
t0 = time.time()
for r in REGS:
    S1 = np.array([entropy(*corr(r, False), l, L) for l in LS])
    S2 = np.array([entropy(*corr(r, True ), l, L) for l in LS])
    _, b1 = fit(LS, S1, "3p"); _, b2 = fit(LS, S2, "3p")
    Bw.append(b1); Bo.append(b2)
    print(f"  {r:<14} B {b1:11.7f}  without {b2:11.7f}  shift {b2-b1:10.7f}  "
          f"[{time.time()-t0:.0f}s]", flush=True)

sig = max(Bw) - min(Bw)
shifts = [o - w for w, o in zip(Bw, Bo)]
nc = max(shifts) - min(shifts)
print(f"\n  regulator signal   (max-min of B)      {sig:.7f}")
print(f"  total shift        (mean)              {np.mean(shifts):.7f}")
print(f"  NON-COMMON residual(max-min of shifts) {nc:.7f}")
print(f"  ratio non-common / signal              {100*nc/sig:.1f}%")
print(f"\n  quantum, same quantity, s=1/2/3: 21.6% / 41.5% / 27.5%")
