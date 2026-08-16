"""E5 — the RESPONSE measurement. Every prior number in this item is noise.

A detector's figure of merit is SNR = gain/floor, gain = reported_drift/true_drift.
The floor has been measured repeatedly; the gain has never been measured for either
estimator. An estimator that always returns zero has a perfect floor.

Ground truth: each half of the series is generated at its OWN constant frequency,
with phase held continuous across the join. The estimators split at exactly that
point, so true drift = |fa-fb|/max(fa,fb) EXACTLY, by construction.

Bin offset is controlled explicitly: the estimators see half-series of length
N/2 = 100, so frac(f * 100) is the fractional bin offset that drives the
interpolation bias.

PREDICTIONS COMMITTED BY QUANTUM (vestigium) BEFORE THIS WAS RUN:
  - NAFF gain ~ 1, roughly independent of bin offset.
  - FFT gain NOT ~ 1, and varying with bin offset.
  - FALSIFICATION: if FFT gain is flat and unity, the cancellation is benign and
    its lower floor genuinely wins.
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from naff_drift import drift_fft, drift_naff

N = 200
M = N // 2
AMPS, RATS = (1.0, 0.45, 0.2), (1.0, np.sqrt(2), np.pi / 2)


def series_with_known_drift(fa, rel_drift, rng):
    """First half at fa, second at fb = fa*(1+rel_drift). Phase continuous."""
    fb = fa * (1.0 + rel_drift)
    ph0 = rng.uniform(0, 2 * np.pi, len(AMPS))
    t = np.arange(N, dtype=float)
    # per-tone phase: fa for t<M, then continue at fb
    x = np.zeros(N)
    for A, r, p in zip(AMPS, RATS, ph0):
        phase = np.where(t < M,
                         2 * np.pi * fa * r * t + p,
                         2 * np.pi * fa * r * M + 2 * np.pi * fb * r * (t - M) + p)
        x += A * np.cos(phase)
    true = abs(fa - fb) / max(fa, fb)
    return x, true


if __name__ == "__main__":
    rng = np.random.default_rng(4242)
    # absolute frequencies chosen to sit at controlled fractional bin offsets of the
    # HALF-series (length 100): on-bin, quarter-bin, half-bin, three-quarter-bin.
    OFFSETS = [("on-bin", 0.00), ("quarter", 0.25), ("half", 0.50), ("three-qtr", 0.75)]
    BASE_BIN = 17                                  # 17 cycles per half-series
    TRUE = [1e-4, 1e-3, 1e-2]
    REPS = 200

    print("E5 — GAIN = reported drift / true drift.  Perfect detector reports 1.00.\n")
    for true_d in TRUE:
        print(f"  true drift = {true_d:.0e}")
        print(f"    {'bin offset':>12} | {'FFT gain':>22} | {'NAFF gain':>22}")
        for lab, off in OFFSETS:
            fa = (BASE_BIN + off) / M
            gf, gn = [], []
            for _ in range(REPS):
                x, true = series_with_known_drift(fa, true_d, rng)
                a, b = drift_fft(x), drift_naff(x)
                if a is not None: gf.append(a / true)
                if b is not None: gn.append(b / true)
            gf, gn = np.array(gf), np.array(gn)
            print(f"    {lab:>12} | {np.median(gf):8.3f}  [{np.percentile(gf,16):6.3f},{np.percentile(gf,84):7.3f}] | "
                  f"{np.median(gn):8.3f}  [{np.percentile(gn,16):6.3f},{np.percentile(gn,84):7.3f}]")
        print()

    # ---- the offset-dependence scan: is the FFT gain a function of bin offset?
    print("  GAIN vs FRACTIONAL BIN OFFSET (true drift = 1e-3), 32 offsets:")
    offs = np.linspace(0, 1, 32, endpoint=False)
    gfs, gns = [], []
    for off in offs:
        fa = (BASE_BIN + off) / M
        a_, b_ = [], []
        for _ in range(120):
            x, true = series_with_known_drift(fa, 1e-3, rng)
            u, v = drift_fft(x), drift_naff(x)
            if u is not None: a_.append(u / true)
            if v is not None: b_.append(v / true)
        gfs.append(np.median(a_)); gns.append(np.median(b_))
    gfs, gns = np.array(gfs), np.array(gns)
    print(f"    FFT  gain: min {gfs.min():.3f}  max {gfs.max():.3f}  "
          f"spread {gfs.max()-gfs.min():.3f}  median {np.median(gfs):.3f}")
    print(f"    NAFF gain: min {gns.min():.3f}  max {gns.max():.3f}  "
          f"spread {gns.max()-gns.min():.3f}  median {np.median(gns):.3f}")
    print()
    print("    offset : FFT gain : NAFF gain")
    for o, a, b in zip(offs[::2], gfs[::2], gns[::2]):
        print(f"    {o:6.3f} : {a:8.3f} : {b:9.3f}")

    print("\n  SNR = gain / floor, using the E1 synthetic floors (FFT 5.167e-06, NAFF 1.219e-05):")
    for lab, g, fl in [("FFT ", np.median(gfs), 5.167e-06), ("NAFF", np.median(gns), 1.219e-05)]:
        print(f"    {lab}: gain {g:.3f} / floor {fl:.3e}  ->  SNR {g/fl:,.0f}")
