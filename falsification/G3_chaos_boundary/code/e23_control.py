"""E2 / E3 — both estimators on the SAME freshly integrated orbits.

Gates frozen in ../PREREG_ESTIMATOR.md before any of this was written.

E2 (positive control): NAFF must still find s106's delta=2.0 layer at x0 ~ 8.0369/8.0409.
E3 (negative control): at delta=1.0 (Schwarzschild, TRUE drift exactly 0) NAFF's max/median
    must fall materially below the incumbent's 2980 AND below its own delta=2.0 value --
    i.e. the current ordering, control ranking above deformed spacetimes, must INVERT.
E4 (discrimination, per L13): two-sample KS of delta=2.0 vs delta=1.0, new estimator.

Crossing series are PERSISTED (forward-look item 4), so no future re-analysis needs re-integration.
Same orbits scored by both estimators, so the comparison is exactly like-for-like.
"""
import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
sys.path.insert(0, str(Path(__file__).parent))
from _zv_invariant import metric
from poincare import _rk4, p_on_shell, H_value
from naff_drift import drift_fft, drift_naff

E, LZ, HSTEP = 0.95, 3.0, 0.02
NCROSS, MAXSTEP, DH_MAX = 200, 1_200_000, 1e-4
OUT = Path(__file__).resolve().parent.parent / "results" / "e23_estimator.json"


def py_at_px_zero(f, x0, lo=0.0, hi=3.0):
    if p_on_shell(f, x0, 0.0, lo, E, LZ) is None:
        return None
    a, b = lo, hi
    for _ in range(60):
        m = 0.5 * (a + b)
        if p_on_shell(f, x0, 0.0, m, E, LZ) is None:
            b = m
        else:
            a = m
    return a


def integrate(f, x0):
    py = py_at_px_zero(f, x0)
    if py is None:
        return None
    p1 = p_on_shell(f, x0, 0.0, py, E, LZ)
    if p1 is None:
        return None
    s = [x0, 0.0, p1, py]
    H0 = H_value(f, s, E, LZ)
    xs, prev, steps, esc, dH = [], 0.0, 0, False, 0.0
    while len(xs) < NCROSS and steps < MAXSTEP:
        try:
            s = _rk4(f, s, HSTEP, E, LZ)
        except (OverflowError, ZeroDivisionError, ValueError):
            esc = True; break
        steps += 1
        if s[0] < 1.3 or s[0] > 120 or abs(s[1]) > 0.999:
            esc = True; break
        if prev < 0.0 <= s[1]:
            xs.append(s[0])
            dH = max(dH, abs(H_value(f, s, E, LZ) - H0) / max(abs(H0), 1e-300))
        prev = s[1]
    return {"x0": round(x0, 6), "series": [float(v) for v in xs],
            "ncross": len(xs), "escaped": bool(esc), "dH": float(dH)}


# delta=2.0: fine steps across s106's layer, plus a spread for the median.
# delta=1.0: matched count around its own separatrix (9.66667).
GRIDS = {
    "2.0": sorted(set([round(8.03 + 0.002 * i, 5) for i in range(13)]        # the layer
                      + [round(v, 5) for v in np.arange(7.6, 9.6, 0.08)])),  # the floor
    "1.0": sorted(set([round(9.60 + 0.002 * i, 5) for i in range(13)]
                      + [round(v, 5) for v in np.arange(9.0, 11.0, 0.08)])),
}

if __name__ == "__main__":
    rep = json.loads(OUT.read_text()) if OUT.exists() else {"orbits": {}}
    for d, grid in GRIDS.items():
        f = metric(float(d))
        got = rep["orbits"].setdefault(d, {})
        t0 = time.time()
        print(f"delta={d}: {len(grid)} x0 values", flush=True)
        for i, x0 in enumerate(grid):
            k = f"{x0:.5f}"
            if k in got:
                continue
            o = integrate(f, x0)
            if o is not None and len(o["series"]) >= 80:
                o["drift_fft"] = drift_fft(np.array(o["series"]))
                o["drift_naff"] = drift_naff(np.array(o["series"]))
                got[k] = o
            OUT.write_text(json.dumps(rep))          # checkpoint every orbit
            if (i + 1) % 5 == 0:
                print(f"   {i+1}/{len(grid)}  [{time.time()-t0:.0f}s]", flush=True)
        print(f"delta={d}: {len(got)} usable orbits [{time.time()-t0:.0f}s]", flush=True)
    print("done", flush=True)
