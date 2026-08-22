"""Does the k=0 mode contribute to my corner coefficient, as it does to quantum's?

quantum found B is 20.4% zero-mode in their study, and that the defensive sentence
claiming immunity -- "the zero mode contributes a constant ~0.002 independent of l" --
was wrong: XA is n x n with n = l^2, so a constant added to every entry is RANK-1 with
eigenvalue c*l^2, contributing log(c*l^2) = 2 log l + const, exactly the form B extracts.

My study is massive (m*L = 1.6 held fixed), so k=0 is regulated rather than singular.
That is a REASON TO EXPECT immunity, which is exactly the kind of unexamined defence
their finding was about. So measure it instead.

Small l only -- the s=6 run has the box.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import REG, entropy
from extract import fit, spread

L, m = 800, 0.002
ls = [30, 40, 50, 60]

def correlators_masked(L, m, reg, drop_zero):
    k = 2*np.pi*np.fft.fftfreq(L)
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.sqrt(REG[reg](KX, KY, m*m))
    invw, wh = 1.0/(2.0*w), w/2.0
    if drop_zero:                      # kill the k=0 Fourier component only
        invw[0, 0] = 0.0; wh[0, 0] = 0.0
    return np.fft.ifft2(invw).real, np.fft.ifft2(wh).real

print(f"  L={L} m*L={m*L}  l={ls}   (small l: the s=6 run has the box)\n")
print(f"  {'regulator':<14} {'B with k=0':>12} {'B without':>12} {'shift':>9}")
Bw, Bo = [], []
for reg in ("nn", "improved", "higher_deriv", "smeared"):
    S1 = np.array([entropy(*correlators_masked(L, m, reg, False), l, L) for l in ls])
    S2 = np.array([entropy(*correlators_masked(L, m, reg, True),  l, L) for l in ls])
    _, b1 = fit(ls, S1, "3p"); _, b2 = fit(ls, S2, "3p")
    Bw.append(b1); Bo.append(b2)
    print(f"  {reg:<14} {b1:12.6f} {b2:12.6f} {100*(b2-b1)/abs(b1):8.2f}%")
print(f"\n  corner SPREAD with k=0   : {spread(Bw):.4f}%")
print(f"  corner SPREAD without    : {spread(Bo):.4f}%   ({100*(spread(Bo)-spread(Bw))/spread(Bw):+.1f}% relative)")
print("\n  What matters for the published claim is the SPREAD, not B: if the mode enters")
print("  every regulator with the same weight it cancels in the difference. quantum's")
print("  did (all four have reg(0,0) = m^2 identically). Check whether mine do.")
for reg in ("nn", "improved", "higher_deriv", "smeared"):
    v = float(REG[reg](np.array(0.0), np.array(0.0), m*m))
    print(f"    reg({reg:<13}) at k=0 = {v:.8f}   (m^2 = {m*m:.8f})")
