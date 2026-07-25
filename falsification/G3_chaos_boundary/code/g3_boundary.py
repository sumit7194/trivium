#!/usr/bin/env python3
"""G3 — where does thin-layer chaos stop being DETECTABLE? (an L9 regime scan on a Tier-G bet)

    python3 g3_boundary.py

Gates frozen in ../PREREGISTRATION.md. G3: "every stationary non-integrable vacuum in our reach has
detectable thin-layer resonance chaos" (MN yes, ZV delta=2 yes — two for two, never scanned).

Structural reason the yes/no framing is inadequate: in Zipoy-Voorhees, delta=1 IS Schwarzschild
(integrable). ansatz proved delta!=1 non-integrable (s97/s98) and exhibited the layer at delta=2 (s106).
So as delta -> 1+ the layer must shrink to zero BY CONTINUITY. G3 is expected false, trivially; the content
is WHERE it fails and HOW the signal scales — a curve, not a boolean (L3).

Two signatures, both required (s106's discipline): frequency drift (the s105 area-blind detector) AND a
finite escape lifetime (chaotic transport sticks then escapes; KAM tori are eternal).

Imports ansatz READ-ONLY. Bridge-solo.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _zv_invariant import metric
from poincare import _rk4, p_on_shell, H_value

OUT = Path(__file__).resolve().parent.parent / "results"

E, LZ = 0.95, 3.0                  # s106's setting
DELTAS = [1.0, 1.02, 1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 2.0]
NX = 9                             # x0 samples inside the long-lived band (bounded compute)
NCROSS = 60                        # crossings per orbit (split-half FFT needs >= ~60)
HSTEP = 0.02
MAXSTEP = 600_000
DRIFT_FIRE = 3.0                   # fire iff drift >= this x the per-delta regular-neighbour floor
ESCAPE_MAX = 0.85                  # and iff the orbit escapes within this fraction of NCROSS


def py_at_px_zero(f, x0, hi=3.0, it=60):
    """§106's initial condition is p_x = 0 — NOT p_y = 0.

    THE BUG THIS FIXES: ZV is reflection-symmetric about the equator, so starting at y=0 with p_y=0 leaves
    the orbit EXACTLY planar (y == 0.00e+00 forever, verified). It then never crosses the section, produces
    no series, and every delta reported "too few clean orbits" — while G3a, the integrable control, passed
    VACUOUSLY on zero orbits. `p_on_shell` solves for p_x given p_y, so p_x=0 is reached by bisecting p_y.
    """
    if p_on_shell(f, x0, 0.0, 0.0, E, LZ) is None:
        return None
    if p_on_shell(f, x0, 0.0, hi, E, LZ) is not None:
        return None                                   # never reaches p_x = 0 within the bracket
    lo = 0.0
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if p_on_shell(f, x0, 0.0, mid, E, LZ) is not None:
            lo = mid
        else:
            hi = mid
    return lo


def crossings(f, x0, n=NCROSS, h=HSTEP):
    """Record equator (y=0) crossings. Returns (radii series, escaped?, max |dH/H|)."""
    py = py_at_px_zero(f, x0)
    if py is None:
        return None, False, 0.0
    p1 = p_on_shell(f, x0, 0.0, py, E, LZ) or 0.0
    s = [x0, 0.0, p1, py]
    H0 = H_value(f, s, E, LZ)
    xs, prev_y, steps, escaped = [], 0.0, 0, False
    while len(xs) < n and steps < MAXSTEP:
        try:
            s = _rk4(f, s, h, E, LZ)
        except (OverflowError, ZeroDivisionError, ValueError):
            escaped = True; break
        steps += 1
        if s[0] < 1.3 or s[0] > 120 or abs(s[1]) > 0.999:
            escaped = True; break
        if prev_y < 0.0 <= s[1]:
            xs.append(s[0])
        prev_y = s[1]
    dH = abs(H_value(f, s, E, LZ) - H0) / max(abs(H0), 1e-300) if xs else 0.0
    return (np.array(xs) if xs else None), escaped, float(dH)


def drift(series, half=None):
    """s105's area-blind frequency drift: does the dominant frequency WANDER between halves?"""
    if series is None or len(series) < 60:
        return 0.0
    a = series - series.mean()
    m = len(a) // 2
    def peak(seg):
        seg = seg - seg.mean()
        if len(seg) < 16 or np.allclose(seg, 0):
            return 0.0
        sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
        k = int(np.argmax(sp[1:]) + 1)
        return k / len(seg)
    f1, f2 = peak(a[:m]), peak(a[m:])
    return abs(f1 - f2) / max(f1, f2, 1e-12)


def scan_delta(d):
    f = metric(d)
    # locate the bound-orbit window for this delta, then sample it
    # Cheap pre-scan for the LONG-LIVED band: outside it orbits plunge within a few crossings and no
    # frequency series exists. The band moves with delta, so it is located per delta, never assumed.
    band = []
    for x in np.arange(6.0, 26.0, 1.0):
        py = py_at_px_zero(f, float(x))
        if py is None:
            continue
        st = [float(x), 0.0, p_on_shell(f, float(x), 0.0, py, E, LZ) or 0.0, py]
        alive = True
        for _ in range(40_000):
            try:
                st = _rk4(f, st, HSTEP, E, LZ)
            except (OverflowError, ZeroDivisionError, ValueError):
                alive = False; break
            if st[0] < 1.3 or st[0] > 120 or abs(st[1]) > 0.999:
                alive = False; break
        if alive:
            band.append(float(x))
    if not band:
        return {"delta": d, "status": "no long-lived orbits", "orbits": [], "band": []}
    lo, hi = min(band), max(band)
    xs = np.linspace(lo, hi, NX)
    orbits = []
    for x0 in xs:
        ser, esc, dH = crossings(f, float(x0))
        if ser is None or len(ser) < 60:
            continue
        dr = drift(ser)
        orbits.append({"x0": float(x0), "drift": dr, "escaped": bool(esc),
                       "ncross": int(len(ser)), "dH": dH})
    return {"delta": d, "status": "ok", "window": [lo, hi], "orbits": orbits}


def classify(res):
    """Per-delta: floor from the quiet majority; fire = both signatures, with the A1 integration guard."""
    orb = [o for o in res["orbits"] if o["dH"] < 1e-4]          # A1 guard: integration must be clean
    if len(orb) < 5:
        return {"floor": None, "fired": [], "max_drift": None, "n_used": len(orb)}
    ds = np.array([o["drift"] for o in orb])
    floor = float(np.median(ds))                                 # the regular neighbours set the floor
    fired = [o for o in orb
             if o["drift"] >= DRIFT_FIRE * max(floor, 1e-6)
             and o["escaped"] and o["ncross"] <= ESCAPE_MAX * NCROSS]
    return {"floor": floor, "fired": fired, "max_drift": float(ds.max()), "n_used": len(orb)}


def main():
    print("G3 — where does thin-layer chaos stop being DETECTABLE? (gates in PREREGISTRATION.md)")
    print(f"  ZV family (delta=1 IS Schwarzschild), E={E}, Lz={LZ}, {NX} x0 per delta, {NCROSS} crossings")
    print(f"  fire = drift >= {DRIFT_FIRE}x floor AND escapes within {ESCAPE_MAX:.0%} of the record\n")
    rep = {"E": E, "Lz": LZ, "deltas": DELTAS, "nx": NX, "ncross": NCROSS}

    print(f"  {'delta':>6} | {'orbits':>6} | {'floor':>9} | {'max drift':>10} | {'ratio':>7} | fired?")
    rows = {}
    for d in DELTAS:
        res = scan_delta(d)
        c = classify(res)
        rows[str(d)] = {"scan": res["status"], **{k: v for k, v in c.items() if k != "fired"},
                        "n_fired": len(c["fired"]),
                        "fired_x0": [round(o["x0"], 4) for o in c["fired"]]}
        if c["floor"] is None:
            print(f"  {d:6.2f} | {c['n_used']:6d} |    (too few clean orbits — not measurable)")
            continue
        ratio = c["max_drift"] / max(c["floor"], 1e-12)
        print(f"  {d:6.2f} | {c['n_used']:6d} | {c['floor']:9.2e} | {c['max_drift']:10.2e} | {ratio:7.1f} | "
              f"{('YES ('+str(len(c['fired']))+')') if c['fired'] else 'no'}")
    rep["scan"] = rows

    # ---- G3a integrable control
    ctrl = rows["1.0"]
    # A control that "passes" because nothing ran is not a control — the first run did exactly that.
    g3a = ctrl.get("n_fired", 0) == 0 and (ctrl.get("n_used") or 0) >= 5
    print(f"\n  G3a — integrable control (delta=1.0 = Schwarzschild): fired = {ctrl.get('n_fired')}, "
          f"clean orbits = {ctrl.get('n_used')} (>=5 required — a control cannot pass on an empty scan)")
    print(f"     →  G3a {'PASS ✅ — detector is not crying wolf' if g3a else 'FAIL ❌ — DETECTOR BROKEN, all gates VOID'}")
    rep["G3a"] = {"pass": bool(g3a), "n_fired": ctrl.get("n_fired")}
    if not g3a:
        rep["verdict"] = "VOID — the detector fires on an integrable metric"
        OUT.mkdir(exist_ok=True); (OUT / "g3_boundary.json").write_text(json.dumps(rep, indent=1))
        print("\n  VERDICT: VOID"); return

    # ---- G3b regression on the known point
    top = rows["2.0"]
    g3b = top.get("n_fired", 0) > 0
    print(f"\n  G3b — regression at delta=2.0 (ansatz s106's exhibited layer): fired = {top.get('n_fired')}, "
          f"max drift {top.get('max_drift')}")
    print(f"     →  G3b {'PASS ✅' if g3b else 'FAIL ❌ — s106 does not reproduce; port wrong, later gates VOID'}")
    rep["G3b"] = {"pass": bool(g3b), "n_fired": top.get("n_fired")}

    # ---- G3c the boundary
    fired_ds = [float(k) for k, v in rows.items() if v.get("n_fired", 0) > 0 and float(k) != 1.0]
    quiet_ds = [float(k) for k, v in rows.items()
                if v.get("n_fired", 0) == 0 and float(k) != 1.0 and v.get("floor") is not None]
    dstar = min(fired_ds) if fired_ds else None
    print(f"\n  G3c — the boundary: fired at delta = {sorted(fired_ds)}")
    print(f"                      silent at delta = {sorted(quiet_ds)}")
    if not g3b:
        verdict = "VOID — G3b regression failed"
    elif quiet_ds:
        verdict = (f"G3 KILLED as stated — delta = {sorted(quiet_ds)} are PROVEN non-integrable (ansatz "
                   f"s97/s98) yet show NO detectable chaos at this resolution. Detectability boundary "
                   f"delta* = {dstar}. Expected, and by continuity: delta=1 is Schwarzschild, so the layer "
                   f"must shrink to nothing. The finding is the boundary and the scaling, not the kill.")
    elif fired_ds:
        verdict = (f"G3 SURVIVES — the layer fires at every non-integrable delta tested, down to "
                   f"{min(fired_ds)}. No boundary found inside the scanned range.")
    else:
        verdict = "UNDECIDED(search) — the layer was not located at ANY delta; the hunt, not the physics, failed."
    rep["G3c"] = {"fired_deltas": sorted(fired_ds), "quiet_deltas": sorted(quiet_ds), "delta_star": dstar}

    # ---- G3d species classification, from the SHAPE of the decline
    curve = [(float(k), v["max_drift"] / max(v["floor"], 1e-12))
             for k, v in rows.items() if v.get("floor") and float(k) != 1.0]
    curve.sort()
    print(f"\n  G3d — the curve (max drift / floor vs delta): "
          f"{[(d, round(r,1)) for d, r in curve]}")
    smooth = None
    if len(curve) >= 4:
        rs = [r for _, r in curve]
        smooth = all(rs[i] <= rs[i + 1] * 1.6 for i in range(len(rs) - 1))
        print(f"     monotone-ish decline toward the floor as delta→1: {smooth}")
        print(f"     →  {'SPECIES-1 (precision): the layer is still there, our detector ran out — crossable' if smooth else 'NOT a smooth decline — an abrupt loss would be a genuine surprise, see FINDINGS'}")
    rep["G3d"] = {"curve": curve, "smooth_decline": smooth}

    print(f"\n  VERDICT: {verdict}")
    rep["verdict"] = verdict
    OUT.mkdir(exist_ok=True)
    (OUT / "g3_boundary.json").write_text(json.dumps(rep, indent=1))
    print(f"\n  wrote results/g3_boundary.json")


if __name__ == "__main__":
    main()
