"""Zero-mode shift at FIXED l/L -- the condition the study actually runs in.

CORRECTION to zeromode_scaling.py, which held l FIXED across s. The rank-1 eigenvalue is
c*l^2 with c ~ 1/(3.2L):

    fixed l       c*l^2 ~ l^2/L      falls as 1/L
    fixed l/L=r   c*l^2 ~ r^2 L      GROWS as L

Opposite directions -- and the published runs hold l/L fixed (l/L = 0.025..0.125 at
every resolution). The first script justified fixed-l in a comment as "the honest
comparison for an additive lattice artifact". That was an argument, not a measurement,
and it is the same shape as the defence it was written to test.

Readings pre-registered, and this time about the SETUP as well as the outcome:
  shift FALLS with L at fixed l/L -> quantum's vanishing-artifact mechanism survives
  shift GROWS with L              -> mechanism INVERTS; a growing contaminant, worse
  shift flat                      -> contributes a constant offset, cannot explain
                                     an s-dependent falloff either way
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import REG, entropy
from extract import fit

CFG = {3: (480, 1/300.), 4: (640, 0.0025), 5: (800, 0.002)}
FRACS = [0.025, 0.05, 0.075, 0.1, 0.125]        # the study's own l/L grid

def corr(L, m, reg, drop):
    k = 2*np.pi*np.fft.fftfreq(L)
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.sqrt(REG[reg](KX, KY, m*m))
    a, b = 1.0/(2.0*w), w/2.0
    if drop: a[0,0] = 0.0; b[0,0] = 0.0
    return np.fft.ifft2(a).real, np.fft.ifft2(b).real

print(f"  l/L held fixed at {FRACS} -- the study's own grid\n")
print(f"  {'s':>2} {'L':>5} {'l values':>26} {'B with':>10} {'B without':>11} {'shift':>10}")
rows = []
for s, (L, m) in CFG.items():
    ls = [int(round(f*L)) for f in FRACS]
    S1 = np.array([entropy(*corr(L, m, "nn", False), l, L) for l in ls])
    S2 = np.array([entropy(*corr(L, m, "nn", True ), l, L) for l in ls])
    _, b1 = fit(ls, S1, "3p"); _, b2 = fit(ls, S2, "3p")
    rows.append((s, L, b1, b2, b2-b1))
    print(f"  {s:>2} {L:>5} {str(ls):>26} {b1:10.6f} {b2:11.6f} {b2-b1:10.6f}")

import math
print()
for i in range(1, len(rows)):
    (s1,L1,_,_,d1),(s2,L2,_,_,d2) = rows[i-1], rows[i]
    if d1 != 0 and d1*d2 > 0:
        print(f"    L {L1}->{L2}:  shift ~ L^{math.log(d2/d1)/math.log(L2/L1):+.2f}")
    else:
        print(f"    L {L1}->{L2}:  {d1:.6f} -> {d2:.6f}  (sign change or zero; no exponent)")
d0, dN = rows[0][4], rows[-1][4]
if d0*dN > 0:
    k = math.log(dN/d0)/math.log(rows[-1][1]/rows[0][1])
    print(f"    global L={rows[0][1]}->{rows[-1][1]}: L^{k:+.2f}")
    print(f"\n  Published corner falloff is s^-2 = L^-2.00 (L = 160 s).")
    print(f"  Fixed-l measurement gave L^-2.30 and was the WRONG CONDITION.")
