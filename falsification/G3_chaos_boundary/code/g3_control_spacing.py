"""G3 item 0 — does the boundary survive adequate counting statistics?
Gates frozen in ../PREREG_BOUNDARY.md before this file was written.
delta = 1.3 vs 1.5, identical sampling, ~322 orbits each, N=200.
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
NCROSS, MAXSTEP, DH_MAX, ESC_MAX = 200, 1_200_000, 1e-4, 0.85
EDGES = {"1.0": [9.66667]}     # control: single separatrix edge (topology differs at delta=1)
HALF, STEP = 0.08, 0.0005    # ARM B: matched SPACING (same x0 step as treatment deltas)
OUT = Path(__file__).resolve().parent.parent / "results" / "g3_control_spacing.json"

def py_at_px_zero(f, x0):
    if p_on_shell(f, x0, 0.0, 0.0, E, LZ) is None: return None
    a, b = 0.0, 3.0
    for _ in range(60):
        m = 0.5*(a+b)
        if p_on_shell(f, x0, 0.0, m, E, LZ) is None: b = m
        else: a = m
    return a

def integrate(f, x0):
    py = py_at_px_zero(f, x0)
    if py is None: return None
    p1 = p_on_shell(f, x0, 0.0, py, E, LZ)
    if p1 is None: return None
    s = [x0, 0.0, p1, py]; H0 = H_value(f, s, E, LZ)
    xs, prev, steps, esc, dH = [], 0.0, 0, False, 0.0
    while len(xs) < NCROSS and steps < MAXSTEP:
        try: s = _rk4(f, s, HSTEP, E, LZ)
        except (OverflowError, ZeroDivisionError, ValueError): esc = True; break
        steps += 1
        if s[0] < 1.3 or s[0] > 120 or abs(s[1]) > 0.999: esc = True; break
        if prev < 0.0 <= s[1]:
            xs.append(s[0])
            dH = max(dH, abs(H_value(f, s, E, LZ) - H0)/max(abs(H0), 1e-300))
        prev = s[1]
    a = np.array(xs) if xs else None
    return {"x0": round(x0, 6), "ncross": len(xs), "escaped": bool(esc), "dH": float(dH),
            "series": [float(v) for v in xs],
            "drift_fft": drift_fft(a) if a is not None else None,
            "drift_naff": drift_naff(a) if a is not None else None}

def grid(edges):
    g = set()
    for e in edges:
        n = int(round(HALF/STEP))
        for i in range(-n, n+1):
            g.add(round(e + i*STEP, 6))
    return sorted(g)

if __name__ == "__main__":
    rep = json.loads(OUT.read_text()) if OUT.exists() else {"orbits": {}}
    for d, edges in EDGES.items():
        f = metric(float(d)); got = rep["orbits"].setdefault(d, {})
        g = grid(edges); t0 = time.time()
        print(f"delta={d}: {len(g)} x0 values, {len(got)} already banked", flush=True)
        for i, x0 in enumerate(g):
            k = f"{x0:.6f}"
            if k in got: continue
            o = integrate(f, x0)
            # BANK ONLY WHAT THE ORIGINAL BANKED. g3_overnight.scan() appended an orbit only
            # if drift(ser) was non-None, and drift() returns None below 80 crossings. So the
            # published "4/100 escaped at delta=1.3" counts escapes among SURVIVORS, not among
            # all grid points. Banking immediate plungers here would have made the escape
            # fraction incomparable to the number this run exists to test -- first pass showed
            # 75/75 "escaped" because every point below the separatrix plunges at step 1.
            if o is not None and o["ncross"] >= 80: got[k] = o
            OUT.write_text(json.dumps(rep))                 # checkpoint EVERY orbit
            if (i+1) % 25 == 0:
                ne = sum(1 for v in got.values() if v["escaped"])
                print(f"   {i+1}/{len(g)}  banked={len(got)}  escaped={ne}  [{time.time()-t0:.0f}s]", flush=True)
        ne = sum(1 for v in got.values() if v["escaped"])
        print(f"delta={d}: DONE {len(got)} orbits, {ne} escaped [{time.time()-t0:.0f}s]", flush=True)
    print("done", flush=True)
