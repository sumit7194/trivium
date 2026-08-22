"""STRUCTURAL FLOOR for the conserved-quantity screen — ansatz's suggestion.

My screen had no quantity distinguishing "this run is broken" from "this metric
has nothing". A threshold cannot: it has no floor derived from construction. But
the reducible products ARE conserved, so any screen with an adequate basis must
find AT LEAST as many directions as there are independent reducibles at that degree.

    conserved < floor  =>  THE RUN IS BROKEN, by construction, no interpretation.

Generators, by momentum degree:
  delta=1 (Schwarzschild):  degree 1 -> {E, L};   degree 2 -> {H, L_tot^2}
  delta=2 (ZV deformed):    degree 1 -> {E, L};   degree 2 -> {H}
    (no L_tot^2: ZV is axisymmetric but not spherically symmetric)
"""
import itertools
from math import comb

def floor_at(deg, gens):
    """Count independent monomials of total momentum-degree `deg` built from
    generators with the given degrees. gens = list of generator degrees."""
    n = 0
    # partitions of deg into generator degrees, counted as multisets
    def rec(i, remaining, chosen):
        nonlocal n
        if remaining == 0:
            n += 1; return
        if i >= len(gens): return
        d = gens[i]
        k = 0
        while k*d <= remaining:
            rec(i+1, remaining - k*d, chosen + [(i, k)])
            k += 1
    # multiset over generator TYPES: count monomials, so group generators by degree
    from collections import Counter
    bydeg = Counter(gens)
    def count(deg):
        total = 0
        degs = sorted(bydeg)
        def go(idx, rem, acc):
            nonlocal total
            if rem == 0:
                total += acc; return
            if idx >= len(degs): return
            d = degs[idx]; m = bydeg[d]
            k = 0
            while k*d <= rem:
                go(idx+1, rem - k*d, acc*comb(m + k - 1, k))
                k += 1
        go(0, deg, 1)
        return total
    return count(deg)

if __name__ == "__main__":
    LADDER = {"1.0 (Schwarzschild)": [1,1,2,2],   # E, L (deg 1); H, L_tot^2 (deg 2)
              "2.0 (ZV deformed)":   [1,1,2]}     # E, L (deg 1); H (deg 2)
    print("STRUCTURAL FLOOR — minimum conserved directions any adequate basis must find\n")
    print(f"{'delta':>20} | {'deg 2':>6} | {'deg 4':>6} | {'deg 6':>6}")
    for k, g in LADDER.items():
        print(f"{k:>20} | " + " | ".join(f"{floor_at(d,g):6d}" for d in (2,4,6)))
    print()
    print("ansatz's prover (independent, exact over GF(p)):")
    print(f"{'':>20} |      5 |     14 |     30     <- delta=1")
    print(f"{'':>20} |      4 |      9 |     16     <- delta=2")
    print()
    print("MY SCREEN, measured:")
    print(f"{'':>20} |      5 |      4 |      -     <- delta=1")
    print(f"{'':>20} |      4 |      - |      -     <- delta=2")
    print()
    print("  delta=1 degree 2:  5 >= floor 5   RUN OK")
    print("  delta=2 degree 2:  4 >= floor 4   RUN OK")
    print("  delta=1 degree 4:  4 <  floor 14  *** RUN BROKEN, by construction ***")
    print()
    print("  The degree-4 verdict was reached last night from CALIBRATION -- comparing")
    print("  against a number ansatz supplied. The floor makes it AUTOMATIC and available")
    print("  even where no external prediction exists, which is every delta but these two.")
