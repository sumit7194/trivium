"""Does the zero-mode contribution to B SHRINK with resolution? quantum's hypothesis.

quantum: the zero-mode amplitude is 1/(2mL^2), so it shrinks under continuum refinement.
If its non-common residual carries part of the spread, then some of the s^-2 falloff both
studies report as evidence of universality may be A FINITE-VOLUME ARTIFACT VANISHING
rather than a coefficient becoming universal. It predicts an s-dependence, so it is
testable -- and it is the first mechanism anyone has offered that produces the observed
falloff WITHOUT universality.

With m*L = 1.6 held fixed, m = 1.6/L, so the amplitude 1/(2mL^2) = 1/(3.2 L) goes as 1/L.

    PRE-REGISTERED READINGS, written before the run:
      shift in B falls ~ 1/L        -> quantum's mechanism is live; part of the falloff
                                       is the mode leaving, and universality is weakened
      shift in B roughly CONSTANT   -> the rank-1 term contributes to the log-coefficient
                                       independently of its amplitude, so it cannot
                                       explain an s-dependent falloff; hypothesis dies
      shift GROWS with L            -> neither; something else is going on

Small l throughout so this runs beside the s=6 job.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import REG, entropy
from extract import fit, spread

CFG = {3: (480, 1/300.), 4: (640, 0.0025), 5: (800, 0.002)}
LS  = [24, 32, 40, 48]          # same physical l/L is impossible across s; fixed l is
                                # the honest comparison for an ADDITIVE lattice artifact

def corr(L, m, reg, drop):
    k = 2*np.pi*np.fft.fftfreq(L)
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.sqrt(REG[reg](KX, KY, m*m))
    a, b = 1.0/(2.0*w), w/2.0
    if drop: a[0,0] = 0.0; b[0,0] = 0.0
    return np.fft.ifft2(a).real, np.fft.ifft2(b).real

print(f"  l = {LS} held fixed across s;  m*L = 1.6 held fixed\n")
print(f"  {'s':>2} {'L':>5} {'amp 1/(3.2L)':>13} {'B with':>10} {'B without':>11} "
      f"{'shift':>10} {'shift/amp':>10}")
rows = []
for s, (L, m) in CFG.items():
    S1 = np.array([entropy(*corr(L, m, "nn", False), l, L) for l in LS])
    S2 = np.array([entropy(*corr(L, m, "nn", True ), l, L) for l in LS])
    _, b1 = fit(LS, S1, "3p"); _, b2 = fit(LS, S2, "3p")
    amp = 1.0/(3.2*L); sh = b2 - b1
    rows.append((s, L, amp, b1, b2, sh))
    print(f"  {s:>2} {L:>5} {amp:13.3e} {b1:10.6f} {b2:11.6f} {sh:10.6f} {sh/amp:10.1f}")

print()
L0, sh0 = rows[0][1], rows[0][5]
print(f"  If the shift tracked the amplitude (~1/L), then relative to s=3:")
for s, L, amp, b1, b2, sh in rows:
    print(f"    s={s}: predicted {sh0*L0/L:10.6f}   measured {sh:10.6f}   "
          f"ratio {sh/(sh0*L0/L):6.3f}")
print(f"\n  If instead the shift is CONSTANT in L, the measured column above is flat.")
