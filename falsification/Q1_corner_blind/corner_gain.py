"""quantum's BLIND corner-coefficient extraction test.
Built from their written spec alone; qsim/corner_coefficient.py NOT read.
Their numbers withheld until mine are reported.

S(l) = A*(4l) + B*ln(l) + C  on  l = 4,6,...,20
Recover B by least squares against [4l, ln(l), 1]. GAIN = B_fit/B_true.
FALSIFICATION (theirs): gain off by >1% in ANY zero-noise cell => extraction biased.
"""
import numpy as np
l = np.arange(4, 21, 2).astype(float)
M = np.column_stack([4*l, np.log(l), np.ones_like(l)])
print(f"l = {l.astype(int).tolist()}")
print(f"design matrix condition number = {np.linalg.cond(M):.4f}\n")
print(f"{'B_true':>9} | {'A':>7} | {'noise':>6} | {'B_fit':>14} | {'GAIN':>10} | {'dev from 1':>11}")
rng = np.random.default_rng(20260822); worst = 0.0
for B in [-0.0047, -0.047, -0.47]:
    for A in [0.077, 0.77]:
        for nz in [0.0, 1e-6]:
            C = 0.31
            S = A*(4*l) + B*np.log(l) + C
            if nz: S = S + rng.normal(0, nz, len(l))
            fit = np.linalg.lstsq(M, S, rcond=None)[0]
            g = fit[1]/B
            if nz == 0.0: worst = max(worst, abs(g-1))
            print(f"{B:9.4f} | {A:7.3f} | {nz:6.0e} | {fit[1]:14.6e} | {g:10.6f} | {abs(g-1):11.2e}")
print(f"\nworst |gain-1| over ZERO-NOISE cells: {worst:.3e}")
print(f"quantum's falsification threshold: 1e-2")
print(f"VERDICT: {'EXTRACTION UNBIASED' if worst < 1e-2 else 'BIASED — corner result needs re-derivation'}")
