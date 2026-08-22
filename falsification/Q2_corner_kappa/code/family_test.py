"""Does the non-common zero-mode residual survive kernels from OUTSIDE the family?

THE QUESTION. s=6 gave 23.4% of the regulator signal across four kernels -- but all four
are m^2 + f(K2) and all four came from quantum's spec. So the number cannot distinguish
"property of the method" from "property of these four kernels". quantum's own
pre-committed refusal caught this at the moment it would have been read as confirmation.

THE TEST. Add kernels that break the family, at matched resolution, and see whether the
fraction MOVES:
    out5_sumk4   m^2 + K2 + c(K4 - K2)     perturbs along kx^4 + ky^4   (quantum's)
    out6_mixed   m^2 + K2 + c*a*b          perturbs along kx^2 ky^2     (bridge's)
The square lattice has exactly two independent quartic invariants, so these SPAN the
quartic space rather than being two more points in it. Using both tests a direction
neither session chose alone -- which is quantum's provenance objection answered, not
merely acknowledged.

PRE-REGISTERED, before the run:
    fraction moves on either      -> residual is a property of the FAMILY's structure
    fraction survives both        -> intrinsic across two independently chosen spanning
                                     directions. NOT "method-intrinsic" in full: every
                                     kernel here is still a square-lattice m^2 + quartic.
    4-reg and 5/6-reg disagree
      only via the DENOMINATOR    -> adding a kernel widens the signal without adding
                                     residual; report both terms, not just the ratio

SETUP CORRESPONDENCE (PROTOCOL 20): runs at l/L = 0.025..0.125, the study's own grid.
Resolution is matched across the 4-, 5- and 6-kernel fractions, so the comparison is
INTERNAL -- the absolute s does not matter, only that it is the same for all three.
Run at s=3/s=4 rather than s=6 because the question is whether the fraction MOVES.
"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entropy import REG, entropy
from regulators import REG_OUT
from extract import fit

S = int(sys.argv[1]) if len(sys.argv) > 1 else 3
CFG = {3: (480, 1/300.), 4: (640, 0.0025), 5: (800, 0.002)}
L, m = CFG[S]
FRACS = [0.025, 0.05, 0.075, 0.1, 0.125]
LS = [int(round(f*L)) for f in FRACS]
ALL = {**REG, **REG_OUT}

def corr(fn, drop):
    k = 2*np.pi*np.fft.fftfreq(L)
    KX, KY = np.meshgrid(k, k, indexing='ij')
    w = np.sqrt(fn(KX, KY, m*m))
    a, b = 1.0/(2.0*w), w/2.0
    if drop: a[0, 0] = 0.0; b[0, 0] = 0.0
    return np.fft.ifft2(a).real, np.fft.ifft2(b).real

print(f"s={S}  L={L}  m*L={m*L:.2f}  l={LS}   (the study's grid; resolution matched)", flush=True)
B, SH = {}, {}
t0 = time.time()
for name, fn in ALL.items():
    S1 = np.array([entropy(*corr(fn, False), l, L) for l in LS])
    S2 = np.array([entropy(*corr(fn, True ), l, L) for l in LS])
    _, b1 = fit(LS, S1, "3p"); _, b2 = fit(LS, S2, "3p")
    B[name], SH[name] = b1, b2 - b1
    print(f"  {name:<14} B {b1:11.7f}  shift {b2-b1:10.7f}   [{time.time()-t0:.0f}s]", flush=True)

def frac(names):
    bs = [B[n] for n in names]; sh = [SH[n] for n in names]
    sig = max(bs) - min(bs); nc = max(sh) - min(sh)
    return sig, nc, 100*nc/sig

fam = list(REG)
print(f"\n  {'kernels':<34} {'signal':>11} {'non-common':>12} {'ratio':>8}")
for lab, names in (("4 in-family (quantum's spec)",      fam),
                   ("+ out5 sum-k^4  (quantum's)",       fam + ["out5_sumk4"]),
                   ("+ out6 mixed    (bridge's)",        fam + ["out6_mixed"]),
                   ("all six, spanning the quartics",    fam + ["out5_sumk4", "out6_mixed"])):
    sig, nc, r = frac(names)
    print(f"  {lab:<34} {sig:11.3e} {nc:12.3e} {r:7.1f}%")
