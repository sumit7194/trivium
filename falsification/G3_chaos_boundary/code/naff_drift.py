"""NAFF-style frequency estimator, and E1: its floor against the incumbent.

Gates frozen in ../PREREG_ESTIMATOR.md before this file was written.

The incumbent `drift()` takes the FFT bin peak with parabolic sub-bin interpolation.
This refines omega continuously by maximising the Hanning-windowed Fourier amplitude
    A(w) = | sum_t x(t) w(t) exp(-i w t) |
seeded at the FFT peak. Same half-split, same |f1-f2|/max(f1,f2) output, so the
comparison is like-for-like and only the frequency estimate changes.
"""
import numpy as np

# ---------------------------------------------------------------- incumbent
def drift_fft(series):
    """VERBATIM from g3_overnight.py:153 — the estimator being replaced."""
    if series is None or len(series) < 80:
        return None
    a = np.asarray(series, float); a = a - a.mean()
    m = len(a) // 2

    def peak(seg):
        seg = seg - seg.mean()
        if len(seg) < 32 or np.allclose(seg, 0):
            return None
        sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
        if len(sp) < 4:
            return None
        k = int(np.argmax(sp[1:]) + 1)
        if k <= 0 or k >= len(sp) - 1:
            return k / len(seg)
        y0, y1, y2 = sp[k - 1], sp[k], sp[k + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if den != 0 else 0.0
        return (k + d) / len(seg)

    f1, f2 = peak(a[:m]), peak(a[m:])
    if f1 is None or f2 is None:
        return None
    return abs(f1 - f2) / max(f1, f2, 1e-12)


# ---------------------------------------------------------------- NAFF
def naff_freq(seg, n_refine=60):
    """Dominant frequency (cycles/sample) by continuous maximisation of the
    Hanning-windowed Fourier amplitude, seeded at the FFT peak.

    Golden-section search inside the seed bin's neighbourhood. No SciPy dependency,
    so this can run anywhere the scan runs.
    """
    seg = np.asarray(seg, float)
    seg = seg - seg.mean()
    n = len(seg)
    if n < 32 or np.allclose(seg, 0):
        return None
    w = np.hanning(n)
    xw = seg * w
    sp = np.abs(np.fft.rfft(xw))
    if len(sp) < 4:
        return None
    k = int(np.argmax(sp[1:]) + 1)
    t = np.arange(n)

    def amp(f):                       # f in cycles/sample
        ph = np.exp(-2j * np.pi * f * t)
        return abs(np.dot(xw, ph))

    # bracket: one bin either side of the seed
    lo, hi = max((k - 1) / n, 1e-9), min((k + 1) / n, 0.5)
    gr = (np.sqrt(5) - 1) / 2
    c, d = hi - gr * (hi - lo), lo + gr * (hi - lo)
    fc, fd = amp(c), amp(d)
    for _ in range(n_refine):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - gr * (hi - lo); fc = amp(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + gr * (hi - lo); fd = amp(d)
        if hi - lo < 1e-14:
            break
    return 0.5 * (lo + hi)


def drift_naff(series):
    """Same contract as drift_fft; only the frequency estimate differs."""
    if series is None or len(series) < 80:
        return None
    a = np.asarray(series, float); a = a - a.mean()
    m = len(a) // 2
    f1, f2 = naff_freq(a[:m]), naff_freq(a[m:])
    if f1 is None or f2 is None:
        return None
    return abs(f1 - f2) / max(f1, f2, 1e-12)


# ---------------------------------------------------------------- E1
if __name__ == "__main__":
    rng = np.random.default_rng(20260815)     # same seed as the FINDINGS synthetic
    N, DRAWS = 200, 400

    def synth():
        """EXACTLY quasiperiodic, 3 incommensurate tones -> TRUE drift is 0."""
        t = np.arange(N)
        f0 = rng.uniform(0.08, 0.30)
        ph = rng.uniform(0, 2 * np.pi, 3)
        return sum(A * np.cos(2 * np.pi * f0 * r * t + p)
                   for A, r, p in zip((1.0, .45, .2), (1.0, np.sqrt(2), np.pi / 2), ph))

    series = [synth() for _ in range(DRAWS)]
    print("E1 — synthetic zero-true-drift series, N=200, 400 draws, 3 incommensurate tones.")
    print("Whatever an estimator returns here is its OWN noise.\n")
    print(f"{'estimator':>12} | {'median':>11} | {'90th pct':>11} | {'max':>11} | {'max/median':>11}")
    out = {}
    for lab, fn in [("FFT (old)", drift_fft), ("NAFF (new)", drift_naff)]:
        d = np.array([x for x in (fn(s) for s in series) if x is not None])
        d = np.maximum(d, 1e-18)
        out[lab] = d
        print(f"{lab:>12} | {np.median(d):11.3e} | {np.percentile(d,90):11.3e} | "
              f"{d.max():11.3e} | {d.max()/np.median(d):11.0f}")

    o, n_ = out["FFT (old)"], out["NAFF (new)"]
    imp_med = np.median(o) / np.median(n_)
    imp_mm = (o.max()/np.median(o)) / (n_.max()/np.median(n_))
    print(f"\n  median floor improvement : {imp_med:,.1f}x   (E1 PASS requires >= 10x)")
    print(f"  max/median improvement   : {imp_mm:,.1f}x")
    print(f"\n  E1: {'PASS' if imp_med >= 10 else 'FAIL'}")
    print(f"\n  For scale, the run's delta=1.0 floor was 2.9e-06 and its max/median 2980.")
