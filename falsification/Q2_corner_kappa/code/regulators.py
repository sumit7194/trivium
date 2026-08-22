"""Q2a — the four regulators must agree with m^2 + k^2 to O(k^4) as k->0.
quantum: if one does not, that disagreement is the first finding and we stop there.
Gate frozen in ../PREREGISTRATION.md before this file was written.
"""
import numpy as np

def K2(kx, ky):  return (2-2*np.cos(kx)) + (2-2*np.cos(ky))

def K4(kx, ky):
    f = lambda k: (4/3)*(2-2*np.cos(k)) - (1/12)*(2-2*np.cos(2*k))
    return f(kx) + f(ky)

REG = {
    "nn":           lambda kx,ky,m2: m2 + K2(kx,ky),
    "improved":     lambda kx,ky,m2: m2 + K4(kx,ky),
    "higher_deriv": lambda kx,ky,m2: m2 + K2(kx,ky) + 0.25*K2(kx,ky)**2,
    "smeared":      lambda kx,ky,m2: m2 + K2(kx,ky)*np.exp(0.15*K2(kx,ky)),
}

# --- OUT-OF-FAMILY KERNELS, added 2026-08-22 ------------------------------------
# The four above are all of the form m^2 + f(K2), and they came from quantum's spec.
# So a residual measured across them cannot distinguish "property of the method" from
# "property of these four kernels" -- see S6_DELETION.md.
#
# A kernel is outside the family iff it is NOT a function of K2 alone. Testing that
# requires varying the DEGENERACY of K2: along any ray K2 is monotone in the ray
# parameter, so every quantity is trivially a function of it and the claim has no
# content. On a CIRCLE of fixed |k|, K2 is nearly constant while an out-of-family term
# swings. (A ky=0 slice returned "0% spread" and would have passed an in-family kernel.)
#
# *** CORRECTED: OUT5 AND OUT6 ARE THE SAME DIRECTION, NOT TWO. ***
# I first claimed they span the quartic space. They do not, and quantum caught it:
#     kx^4 + ky^4 = |k|^4 - 2 kx^2 ky^2,  and |k|^4 ~ K2^2 is IN-FAMILY
#     so  D + AB/6 ~ K2^2/12,  verified: spread 0.00% at |k| = 0.3 and 0.1
# D alone spreads 67%, AB alone 197%, D + AB/6 spreads ZERO. Each is out of family;
# their combination is in it. They differ by an in-family admixture and a sign.
#
#   *** MODULO THE FAMILY, THE QUARTIC SPACE HAS EXACTLY ONE OUT-OF-FAMILY DIRECTION. ***
#
# This is BETTER for the provenance objection than spanning would have been. quantum's
# worry was that all five kernels were theirs. But independent choosers are OBLIGED to
# land on the same axis -- I picked the mixed term, they picked sum-k^4, and there was
# no third option. Provenance cannot matter when the choice is unique.
#
# So the residual provenance is THE LATTICE AND THE QUARTIC ORDER, and neither of us
# could have introduced a different one without leaving m^2 + (quartic). A genuinely
# second direction needs a sextic term or a different lattice.
#
# Running both is still worth it: one direction with TWO DIFFERENT IN-FAMILY ADMIXTURES.
def AB(kx, ky):  return (2-2*np.cos(kx)) * (2-2*np.cos(ky))

REG_OUT = {
    "out5_sumk4": lambda kx,ky,m2: m2 + K2(kx,ky) + 0.5*(K4(kx,ky) - K2(kx,ky)),
    "out6_mixed": lambda kx,ky,m2: m2 + K2(kx,ky) + 0.5*AB(kx,ky),
}
# Q2a verified for both: (omega^2-k^2)/k^4 finite and converging as k->0.
#   out5  -> -0.0208   out6 -> +0.0833
# Level-set test at |k|=0.3: K2 varies 0.38% around the circle, a*b varies 197%.

if __name__ == "__main__":
    print("Q2a — small-k agreement with m^2 + k^2.  m=0 so the test is on k alone.")
    print("Reporting  (omega^2 - k^2)/k^4  as k->0 along the diagonal: finite => O(k^4) agreement,")
    print("diverging => the regulator differs at O(k^2) and the gate FAILS.\n")
    print(f"{'k':>10} | " + " | ".join(f"{n:>14}" for n in REG))
    rows={n:[] for n in REG}
    for k in [0.2, 0.1, 0.05, 0.025, 0.0125]:
        kx=ky=k/np.sqrt(2); k2=kx*kx+ky*ky
        vals=[]
        for n,f in REG.items():
            w2=f(kx,ky,0.0); r=(w2-k2)/k2**2; rows[n].append(r); vals.append(r)
        print(f"{k:10.4f} | " + " | ".join(f"{v:14.6f}" for v in vals))
    print()
    ok=True
    for n,v in rows.items():
        conv = abs(v[-1]-v[-2]) < 0.05*max(abs(v[-1]),1e-30) or abs(v[-1])<1e-8
        # also check O(k^2) coefficient vanishes: (w2-k2)/k2 -> 0
        kx=ky=0.0125/np.sqrt(2); k2=kx*kx+ky*ky
        o2=(REG[n](kx,ky,0.0)-k2)/k2
        print(f"  {n:>14}:  (w2-k2)/k4 -> {v[-1]:+.6f}   (w2-k2)/k2 -> {o2:+.3e}")
        if abs(o2) > 1e-3: ok=False
    print(f"\n  Q2a: {'PASS — all four agree to O(k^4)' if ok else 'FAIL — a regulator differs at O(k^2)'}")
