"""Residual-sign test that CANNOT be called without its null.

I predicted null distributions could not ride on an existing action -- "no action
naturally carries them". quantum found the one that does: THE DIAGNOSTIC'S OWN CALL
SITE. Computing the null inside the function that returns the verdict means the verdict
cannot be obtained without it.

That closes the gap rather than confirming it, and it matters because both of us read
sign counts as evidence today without ever computing the p:

    quantum, 8-point residuals   "scatter, not an arc, adequate here"   p = 0.773
    bridge,   6-point M2 series  "smooth arcs in all three regulators"  p = 0.500

Mine was committed as a finding and withdrawn hours later. Neither of us had the p.

HONEST LIMIT, and quantum stated it against their own guard: the "inconclusive at any
outcome" case bites only at n <= 4. At n=5 a perfectly monotone series already reaches
p = 0.031. So the test has MINIMAL power at small n rather than none, and it is the
p-printed-alongside-the-verdict that does the work, not the guard.

    n=2  best p 0.250  INERT     n=5  best p 0.031  has power
    n=3  best p 0.125  INERT     n=6  best p 0.016  has power
    n=4  best p 0.062  INERT     n=7  best p 0.008  has power
"""
from math import comb


def sign_test(residuals, alpha=0.05):
    """Return (verdict, p, detail). The p is computed here; there is no way to get the
    verdict without it."""
    n = len(residuals)
    if n < 2:
        return "INCONCLUSIVE", 1.0, f"n={n}: no adjacent pairs"
    opp = n - 1
    signs = "".join("+" if x > 0 else "-" for x in residuals)
    changes = sum(1 for i in range(1, n) if signs[i] != signs[i - 1])
    p = sum(comb(opp, k) for k in range(changes + 1)) / 2 ** opp
    best = 1 / 2 ** opp                      # p of the most extreme possible outcome
    if best > alpha:
        return ("INCONCLUSIVE", p,
                f"{signs} ({changes}/{opp} changes). AT n={n} NO OUTCOME REACHES "
                f"alpha={alpha}: the most extreme possible sequence gives p={best:.3f}. "
                f"This test cannot fire here -- do not read the count as evidence.")
    verdict = "STRUCTURED" if p < alpha else "NOT DISTINGUISHABLE FROM SCATTER"
    return verdict, p, f"{signs} ({changes}/{opp} changes), p={p:.3f}"


if __name__ == "__main__":
    print("  today's two readings, with the p neither of us computed:\n")
    for lab, res in (("bridge M2 R1 (committed, later withdrawn)", [-1, 1, 1, 1, 1, -1]),
                     ("bridge Q2 memory law",                      [-1, 1, 1, 1, 1, -1]),
                     ("R6 b, R1",                    [1, -1, -1, 1, 1, 1, 1, -1, -1]),
                     ("a genuinely monotone 9-point", [1, 1, 1, 1, 1, 1, 1, 1, 1])):
        v, p, d = sign_test(res)
        print(f"  {lab:<42} {v}")
        print(f"  {'':<42} {d}\n")
