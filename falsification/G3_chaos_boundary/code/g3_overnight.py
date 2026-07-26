#!/usr/bin/env python3
"""G3 overnight — the separatrix hunt at the budget the question actually needs.

    python3 g3_overnight.py          # hours; writes results/g3_overnight.json incrementally

Gates G3a-G3d UNCHANGED from ../PREREGISTRATION.md; the instrument upgrade is frozen in its ADDENDUM.
g3_boundary.py (the first attempt, UNDECIDED(search)) is left untouched and reproducible.

What changed, and why (each answers a named defect from the first run):

  1. CONTINUOUS drift  — parabolic sub-bin interpolation of the FFT peak. The first run's estimator was
     quantized to 2/N = 0.0333 at N=60, ABOVE the 0.027 signal being hunted, so every delta returned an
     identical 6.67e-2 including delta=1.0 (Schwarzschild, provably integrable). Resolution is now set by
     the data, not the bin grid.
  2. HUNT THE SEPARATRIX — the first run scanned x0 in [10,16], the INTERIOR of the long-lived band.
     s106's layer sits at the PLUNGE SEPARATRIX, i.e. the band's EDGE (~8-10 in our probe). We locate the
     plunge<->survive transition per delta by bisection and step finely across it.
  3. s106's actual budget — x0 step 0.002, N=200 crossings (vs 9 samples, N=60).
  4. EACH CONJUNCT VALIDATED SEPARATELY on the control. The `drift AND escape` gate passed vacuously twice
     (first on zero orbits, then on a dead drift conjunct). A conjunctive gate certifies nothing unless each
     conjunct is known to be alive, so the control now checks drift non-degeneracy and escape-liveness
     independently and reports both.

Imports ansatz READ-ONLY. Bridge-solo.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _zv_invariant import metric
from poincare import _rk4, p_on_shell, H_value

OUT = Path(__file__).resolve().parent.parent / "results"
OUT.mkdir(exist_ok=True)

E, LZ = 0.95, 3.0
# ORDER MATTERS: the gates that can VOID the run go FIRST. G3b (delta=2.0 regression) and G3a
# (delta=1.0 control) each void everything downstream, yet both previous runs scheduled delta=2.0 LAST
# and died before reaching it — hours spent on deltas whose verdict a failed G3b would have discarded.
DELTAS = [2.0, 1.0, 1.7, 1.5, 1.3, 1.2, 1.1, 1.05, 1.02]
NCROSS = 200                 # s106's record length (vs 60)
X_STEP = 0.002               # s106's stepping (vs ~0.75)
HALF_WIDTH = 0.10            # scan +/- this around the located separatrix -> ~100 orbits per delta
HSTEP = 0.02
MAXSTEP = 1_200_000
DRIFT_FIRE = 3.0
NCROSS_LONG = 500            # stage-2 record for drift-flagged candidates only
ESCAPE_MAX = 0.85
DH_MAX = 1e-4                # A1 integration guard


def py_at_px_zero(f, x0, hi=3.0, it=60):
    """s106's condition p_x=0. (p_y=0 leaves ZV orbits EXACTLY planar — the first run's bug.)"""
    if p_on_shell(f, x0, 0.0, 0.0, E, LZ) is None:
        return None
    if p_on_shell(f, x0, 0.0, hi, E, LZ) is not None:
        return None
    lo = 0.0
    for _ in range(it):
        m = 0.5 * (lo + hi)
        if p_on_shell(f, x0, 0.0, m, E, LZ) is not None:
            lo = m
        else:
            hi = m
    return lo


def integrate(f, x0, n=NCROSS, maxstep=MAXSTEP):
    py = py_at_px_zero(f, x0)
    if py is None:
        return None, False, 0.0
    s = [x0, 0.0, p_on_shell(f, x0, 0.0, py, E, LZ) or 0.0, py]
    H0 = H_value(f, s, E, LZ)
    xs, prev, steps, esc, dH = [], 0.0, 0, False, 0.0
    while len(xs) < n and steps < maxstep:
        try:
            s = _rk4(f, s, HSTEP, E, LZ)
        except (OverflowError, ZeroDivisionError, ValueError):
            esc = True; break
        steps += 1
        if s[0] < 1.3 or s[0] > 120 or abs(s[1]) > 0.999:
            esc = True; break
        if prev < 0.0 <= s[1]:
            xs.append(s[0])
            # A1 guard, measured ALONG the orbit at each recorded crossing — NOT at the final state.
            #
            # BUG THIS FIXES: dH used to be evaluated once, on the state the loop exited with. For an
            # ESCAPING orbit that state is mid-plunge (x -> 1.3), where fixed-step RK4 loses energy
            # catastrophically. The layer candidate at x0=8.0369 measured dH = 8.3e-2 that way and was
            # discarded as "unclean integration" — yet across all 348 of its recorded crossings the true
            # worst |dH/H| is 1.3e-13, pristine. The guard was therefore rejecting EXACTLY the orbits it
            # was meant to certify: any orbit that escapes fails an end-state energy check by construction,
            # so the A1 guard and the escape conjunct could never both be satisfied.
            #
            # Fourth instance in this run of one failure mode: a criterion evaluated outside the range of
            # the thing it is meant to judge (cf. run 1's drift floor above the signal, run 4's escape
            # window below the documented escape times, and the pgrep pattern that could not match).
            dH = max(dH, abs(H_value(f, s, E, LZ) - H0) / max(abs(H0), 1e-300))
        prev = s[1]
    return (np.array(xs) if xs else None), esc, float(dH)


def survives(f, x0, budget=60_000):
    """Cheap liveness probe used to bisect the plunge<->survive separatrix."""
    py = py_at_px_zero(f, x0)
    if py is None:
        return False
    s = [x0, 0.0, p_on_shell(f, x0, 0.0, py, E, LZ) or 0.0, py]
    for _ in range(budget):
        try:
            s = _rk4(f, s, HSTEP, E, LZ)
        except (OverflowError, ZeroDivisionError, ValueError):
            return False
        if s[0] < 1.3 or s[0] > 120 or abs(s[1]) > 0.999:
            return False
    return True


def find_separatrix(f, lo=4.0, hi=26.0):
    """Locate EVERY plunge<->survive transition and bisect each. Returns a list.

    BUG THIS FIXES (run 2, found after the power cut): the old version scanned upward and returned the
    FIRST surviving x0. If the first grid point already survived it returned that grid EDGE — 5.0000 at
    delta=1.0/1.02/1.05 — without ever bisecting, so those three deltas scanned x0 in [4.9,5.1], the deep
    interior of the stable region, ~1000x below the signal. A silent failure returning a plausible number
    instead of reporting "no transition found" — the same species as every other bug in this campaign.

    It also assumed ONE transition. The probe shows the topology INVERTS with delta: near Schwarzschild
    orbits survive at small x0 and plunge beyond (S->P), while at delta=2 they plunge at small x0, survive
    in a band at 10-14, then plunge again (P->S->P). Two edges, not one, and the count changes with delta.
    """
    grid = np.arange(lo, hi, 0.5)
    states = [(float(x), survives(f, float(x))) for x in grid]
    edges = []
    for (xa, sa), (xb, sb) in zip(states, states[1:]):
        if sa == sb:
            continue                                  # no transition in this cell
        a, b = xa, xb
        for _ in range(30):                           # bisect to well below X_STEP
            m = 0.5 * (a + b)
            if survives(f, m) == sa:
                a = m
            else:
                b = m
        edges.append(round(0.5 * (a + b), 5))
    return edges                                      # [] means genuinely no transition — reported, not faked


def drift(series):
    """Frequency wander between halves, with PARABOLIC SUB-BIN interpolation (kills the 2/N quantum)."""
    if series is None or len(series) < 80:
        return None
    a = series - series.mean()
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
        d = 0.5 * (y0 - y2) / den if den != 0 else 0.0    # sub-bin offset
        return (k + d) / len(seg)

    f1, f2 = peak(a[:m]), peak(a[m:])
    if f1 is None or f2 is None:
        return None
    return abs(f1 - f2) / max(f1, f2, 1e-12)


CKPT = OUT / "g3_overnight.json"


def load_ckpt():
    if not CKPT.exists():
        return {}
    try:
        d = json.loads(CKPT.read_text())
        return d if d.get("x_step") == X_STEP and d.get("ncross") == NCROSS else {}
    except Exception:
        return {}


def save_ckpt(rep):
    tmp = CKPT.with_suffix(".tmp")
    tmp.write_text(json.dumps(rep, indent=1))
    tmp.replace(CKPT)                       # atomic — a power cut mid-write cannot corrupt the checkpoint


def scan(d, rep):
    """Scan one delta, checkpointing EVERY orbit.

    WHY PER-ORBIT: the previous version saved only after a whole delta (55-90 min). Three power cuts came
    faster than that, and run 3 died before completing even delta=2.0 — zero checkpoint, four hours of
    compute lost. Separatrix edges (82-242s to locate) and every finished orbit are now banked immediately,
    so an interrupted run resumes almost exactly where it stopped.
    """
    t0 = time.time()
    f = metric(d)
    part = rep.setdefault("partial", {}).setdefault(str(d), {})

    edges = part.get("edges")
    if edges is None:                                    # edge-finding is expensive — cache it
        edges = find_separatrix(f)
        part["edges"] = edges
        save_ckpt(rep)
    if not edges:
        return {"delta": d, "status": "NO TRANSITION FOUND — reported, not faked", "orbits": [], "edges": []}

    xs = np.unique(np.concatenate([np.arange(e - HALF_WIDTH, e + HALF_WIDTH + 1e-12, X_STEP)
                                   for e in edges]))
    orbits = part.setdefault("orbits", [])
    done = {o["x0"] for o in orbits}
    if done:
        print(f"    resuming delta={d}: {len(done)}/{len(xs)} orbits already banked")
    for i, x0 in enumerate(xs):
        key = round(float(x0), 5)
        if key in done:
            continue
        ser, esc, dH = integrate(f, float(x0))
        dr = drift(ser)
        if dr is not None:
            orbits.append({"x0": key, "drift": dr, "escaped": bool(esc),
                           "ncross": int(len(ser)), "dH": dH, "stage": 1})
        save_ckpt(rep)                                   # every orbit — cuts cost minutes, not hours

    # ---- STAGE 2: the escape check, on drift-flagged candidates ONLY.
    # WHY: s106 documents its layer escaping after 184 and 210 crossings. Our stage-1 cap is 200 and the
    # fire rule wants escape by 170, so BOTH documented escapes fall outside the window — the escape
    # conjunct could not fire by construction (same species as run 1's drift floor sitting above the
    # signal). Raising the cap for every orbit would double a 69-minute delta; almost all orbits are quiet,
    # so only the drift-flagged few are re-run at the longer record.
    clean = [o for o in orbits if o["dH"] < DH_MAX]
    if clean:
        floor = float(np.median([o["drift"] for o in clean]))
        cands = [o for o in clean if o["drift"] >= DRIFT_FIRE * max(floor, 1e-9) and not o.get("stage2")]
        if cands:
            print(f"    stage 2: {len(cands)} drift-flagged candidate(s) re-run to {NCROSS_LONG} crossings")
        for o in cands:
            ser2, esc2, dH2 = integrate(f, o["x0"], n=NCROSS_LONG, maxstep=3_000_000)
            o["stage2"] = True
            o["escaped"] = bool(esc2)
            o["ncross"] = int(len(ser2)) if ser2 is not None else 0
            o["dH"] = dH2
            save_ckpt(rep)
    return {"delta": d, "status": "ok", "separatrix": edges, "n_x0": len(xs),
            "orbits": orbits, "secs": round(time.time() - t0, 1)}


def classify(res):
    orb = [o for o in res.get("orbits", []) if o["dH"] < DH_MAX]
    if len(orb) < 5:
        return {"floor": None, "n_used": len(orb), "n_fired": 0, "fired_x0": [],
                "max_drift": None, "drift_distinct": 0, "any_escape": False}
    ds = np.array([o["drift"] for o in orb])
    floor = float(np.median(ds))
    fired = [o for o in orb if o["drift"] >= DRIFT_FIRE * max(floor, 1e-9)
             and o["escaped"]
             and o["ncross"] <= ESCAPE_MAX * (NCROSS_LONG if o.get("stage2") else NCROSS)]
    return {"floor": floor, "n_used": len(orb), "n_fired": len(fired),
            "fired_x0": [o["x0"] for o in fired], "max_drift": float(ds.max()),
            # conjunct liveness, reported SEPARATELY — the first run's control hid a dead conjunct
            "drift_distinct": int(len(np.unique(np.round(ds, 9)))),
            "any_escape": bool(any(o["escaped"] for o in orb))}


def main():
    print("G3 OVERNIGHT — separatrix hunt at s106's budget (gates unchanged; upgrade in the ADDENDUM)")
    print(f"  N={NCROSS} crossings, x0 step {X_STEP}, +/-{HALF_WIDTH} around the located separatrix")
    print(f"  drift: parabolic sub-bin FFT (the first run was quantized to 2/N={2/60:.4f} > the 0.027 signal)\n")
    rep = {"E": E, "Lz": LZ, "ncross": NCROSS, "x_step": X_STEP, "half_width": HALF_WIDTH, "scan": {}}
    # RESUMABLE at ORBIT granularity — three power cuts is a pattern, not bad luck.
    old = load_ckpt()
    if old:
        rep["scan"] = old.get("scan", {})
        rep["partial"] = old.get("partial", {})
        np_ = sum(len(v.get("orbits", [])) for v in rep["partial"].values())
        print(f"  RESUMING — {len(rep['scan'])} delta(s) complete {sorted(rep['scan'], key=float)}; "
              f"{np_} partial orbit(s) banked\n")
    print(f"  {'delta':>6} | {'separatrix':>10} | {'clean':>5} | {'floor':>9} | {'max drift':>10} | "
          f"{'distinct':>8} | {'esc?':>4} | fired")
    for d in DELTAS:
        if str(d) in rep["scan"]:
            print(f"  {d:6.2f} |  (already done — skipped)")
            continue
        res = scan(d, rep)
        c = classify(res)
        rep["scan"][str(d)] = {"status": res.get("status"), "separatrix": res.get("separatrix"),
                               "secs": res.get("secs"), **c}
        # KEEP the per-orbit data. Popping it lost delta=2.0's 99 orbits on this run, so the
        # two-stage rerun cannot reuse them. Archive instead of discard.
        prt = rep.get("partial", {}).pop(str(d), None)
        if prt:
            rep.setdefault("orbits_archive", {})[str(d)] = prt
        save_ckpt(rep)
        if c["floor"] is None:
            print(f"  {d:6.2f} | {str(res.get('separatrix')):>10} | {c['n_used']:5d} |   (too few clean orbits)")
            continue
        print(f"  {d:6.2f} | {str(res['separatrix']):>10} | {c['n_used']:5d} | {c['floor']:9.2e} | "
              f"{c['max_drift']:10.2e} | {c['drift_distinct']:8d} | {str(c['any_escape']):>4} | "
              f"{c['n_fired']}  [{res.get('secs')}s]")

    rows = rep["scan"]
    ctrl = rows.get("1.0", {})
    # G3a — and now each conjunct must be independently ALIVE, not merely jointly silent
    g3a = (ctrl.get("n_fired", 1) == 0 and (ctrl.get("n_used") or 0) >= 5
           and (ctrl.get("drift_distinct") or 0) >= 5)
    print(f"\n  G3a — integrable control (delta=1.0): fired={ctrl.get('n_fired')}, clean={ctrl.get('n_used')}, "
          f"distinct drift values={ctrl.get('drift_distinct')} (>=5 required — a degenerate estimator "
          f"cannot certify anything)")
    print(f"     →  G3a {'PASS ✅' if g3a else 'FAIL ❌ — control cannot certify; gates VOID'}")
    any_esc = any(v.get("any_escape") for v in rows.values())
    print(f"     escape conjunct alive anywhere in the run? {any_esc}"
          f"{'' if any_esc else '  ⚠️ untested — a fire criterion cannot rest on it'}")

    top = rows.get("2.0", {})
    g3b = top.get("n_fired", 0) > 0
    print(f"\n  G3b — regression at delta=2.0 (s106's layer): fired={top.get('n_fired')} "
          f"at x0={top.get('fired_x0')}")
    print(f"     →  G3b {'PASS ✅' if g3b else 'FAIL ❌ — s106 still does not reproduce'}")

    fired_ds = sorted(float(k) for k, v in rows.items() if v.get("n_fired", 0) > 0 and float(k) != 1.0)
    quiet_ds = sorted(float(k) for k, v in rows.items()
                      if v.get("n_fired", 0) == 0 and float(k) != 1.0 and v.get("floor") is not None)
    if not g3a:
        verdict = "VOID — the integrable control cannot certify (degenerate estimator or too few orbits)"
    elif not g3b:
        verdict = ("UNDECIDED(search) — s106's layer still not reproduced even at its own budget. Reported "
                   "with exactly what was searched; a second failure at the stated resolution would make the "
                   "hunt itself, not the detector's floor, the open question.")
    elif quiet_ds:
        verdict = (f"G3 KILLED as stated — delta={quiet_ds} are proven non-integrable yet show no detectable "
                   f"chaos; detectability boundary delta* = {min(fired_ds)}. The finding is the boundary and "
                   f"the scaling, not the kill (delta=1 is Schwarzschild, so a boundary must exist).")
    else:
        verdict = f"G3 SURVIVES — the layer fires at every non-integrable delta tested, down to {min(fired_ds)}."
    print(f"\n  G3c — fired at {fired_ds}; silent at {quiet_ds}")
    curve = [(float(k), v["max_drift"]) for k, v in rows.items() if v.get("max_drift") and float(k) != 1.0]
    print(f"  G3d — max drift vs delta: {[(d, round(m,4)) for d, m in sorted(curve)]}")
    print(f"\n  VERDICT: {verdict}")
    rep.update({"verdict": verdict, "G3a": bool(g3a), "G3b": bool(g3b),
                "fired_deltas": fired_ds, "quiet_deltas": quiet_ds, "curve": sorted(curve),
                "escape_conjunct_alive": bool(any_esc)})
    save_ckpt(rep)
    print(f"\n  wrote results/g3_overnight.json")


if __name__ == "__main__":
    main()
