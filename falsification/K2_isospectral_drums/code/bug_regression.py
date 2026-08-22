"""Reproduce the bug the fix was made for, and assert the fix removes it.

WHY. K2's FINDINGS and K5's both rest on a specific signature of the original defect:
the same grid offset in x and y dropped every point on an internal diagonal, which
disconnected each drum into 3 congruent pieces (360/360/120 at n=16), identical between
the two drums -- so the two discrete operators were one matrix relabelled and the claimed
"exact resolution-independent isospectrality" was a triviality.

That number is what JUSTIFIES the correction, and it is not reproducible from HEAD:
k2_drums.py now sets A_OFF, B_OFF = 0.5, 0.25, so running the committed code produces
the FIXED build. You cannot get 360/360/120 out of it.

  A REPAIR CAN ERASE ITS OWN JUSTIFICATION. The evidence for a fix usually lives only in
  the broken version, and fixing is exactly what removes the broken version from the
  repo. Nothing in quantum's 16 catches this -- the number's producer was committed, and
  then edited so it no longer produces it.

So: drive the offsets as a parameter, assert the bug reappears at equal offsets and is
absent at distinct ones.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k2_drums as K

def components(n, a_off, b_off):
    """Connected-component sizes of drum A's interior graph at the given offsets."""
    K.A_OFF, K.B_OFF = a_off, b_off
    mask, _h = K.interior_mask(K.DRUM1, n)
    pts = {(i, j) for i, j in zip(*np.nonzero(mask))}
    seen, sizes = set(), []
    for p in pts:
        if p in seen: continue
        stack, comp = [p], 0
        seen.add(p)
        while stack:
            i, j = stack.pop(); comp += 1
            for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
                q = (i+di, j+dj)
                if q in pts and q not in seen:
                    seen.add(q); stack.append(q)
        sizes.append(comp)
    return sorted(sizes, reverse=True)

n = 16
ok = True
buggy = components(n, 0.5, 0.5)
fixed = components(n, 0.5, 0.25)
print(f"  equal offsets  (0.5, 0.5 )  -> components {buggy}")
print(f"  distinct       (0.5, 0.25)  -> components {fixed}")
want = [360, 360, 120]
g1 = (buggy == want)
g2 = (len(fixed) == 1)
ok = g1 and g2
print(f"\n  {'PASS' if g1 else '*** FAIL ***'}  bug signature reproduces: {want} "
      f"{'' if g1 else f'(got {buggy})'}")
print(f"  {'PASS' if g2 else '*** FAIL ***'}  fix gives a single connected interior "
      f"({len(fixed)} component{'s' if len(fixed)!=1 else ''})")
# And does the guard added to PREVENT the regression actually fire? A guard that has
# never been shown to fail is a decoration (blackhole). laplacian() asserts connectivity.
K.A_OFF, K.B_OFF = 0.5, 0.5
mask, h = K.interior_mask(K.DRUM1, n)
try:
    K.laplacian(mask, h)
    fired = False
except Exception as e:
    fired = True; why = f"{type(e).__name__}: {str(e)[:60]}"
ok = ok and fired
print(f"  {'PASS' if fired else '*** FAIL ***'}  connectivity guard fires on the buggy grid"
      + (f" -- {why}" if fired else " -- IT DID NOT, the guard is a decoration"))

K.A_OFF, K.B_OFF = 0.5, 0.25
mask, h = K.interior_mask(K.DRUM1, n)
try:
    K.laplacian(mask, h); clean = True
except Exception as e:
    clean = False; why2 = f"{type(e).__name__}: {e}"
ok = ok and clean
print(f"  {'PASS' if clean else '*** FAIL ***'}  and does NOT fire on the fixed grid"
      + ("" if clean else f" -- {why2}"))

print(f"\n  {'ALL PASS' if ok else '*** FAILURES ***'}")
sys.exit(0 if ok else 1)
