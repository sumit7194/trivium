#!/usr/bin/env python3
"""Leg J — frequency-drift detector for THIN-LAYER chaos (resolves what box-dim misses) (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python rotation_number_chaos.py

ansatz §102: MN's geometric chaos is a THIN LAYER near resonances — gross box-dimension grazes it (≤1.22)
because the chaotic band has negligible area. A first attempt (centroid-angle rotation number) FALSE-FLAGGED
Kerr's regular 1:3 resonant island as chaos — the same noise/island pitfall as the naive Lyapunov, so it was
discarded. This uses the robust indicator instead — the **frequency drift** (Laskar-style): the dominant
frequency of an orbit's section coordinate is *constant* for any regular orbit (torus OR resonant island),
and only DRIFTS for chaos. Per orbit: peak frequency of the first half of the section series vs the second
half; |Δf|/f is the chaos flag, immune to resonant islands and area-blind so it can see a thin layer.

Validation is strict: the detector must (1) flag chaotic Hénon–Heiles (E=1/6) and (2) leave EVERY Kerr (q=0,
integrable) orbit regular — *including* the 1:3 island that tripped the first attempt. Only then is the
moderate-q MN scan trustworthy. Reuses ansatz poincare/MN machinery read-only.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from _mn_invariant import build_hamilton_numeric
from poincare import section, box_dimension

OUT = Path(__file__).resolve().parent.parent / "results"
E, L = 0.95, 2.8
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))


def freq_drift(series, min_n=100):
    """Dominant section-frequency of the first half vs second half; relative drift |Δf|/f is the chaos flag.
    Regular (torus or resonant island) → constant frequency → drift ≈ 0; chaos → frequency wanders."""
    if len(series) < min_n:
        return None, None
    x = np.asarray(series, float)
    n = len(x); h = n // 2

    def peak(seg):
        seg = (seg - seg.mean()) * np.hanning(len(seg))
        F = np.abs(np.fft.rfft(seg))
        if len(F) < 4:
            return 0.0
        F[0] = 0.0
        k = int(np.argmax(F))
        if 1 <= k < len(F) - 1:                                   # parabolic sub-bin refinement
            a, b, c = F[k - 1], F[k], F[k + 1]
            den = a - 2 * b + c
            k = k + (0.5 * (a - c) / den if den != 0 else 0.0)
        return k / len(seg)

    f1, f2 = peak(x[:h]), peak(x[h:])
    fm = 0.5 * (f1 + f2)
    return fm, (abs(f1 - f2) / fm if fm > 1e-9 else abs(f1 - f2))


# ---- Hénon–Heiles (validation testbed; integrator mirrors ansatz §84) ----
def _hh_rhs(s):
    x, y, px, py = s
    return [px, py, -x - 2 * x * y, -y - x * x + y * y]


def _hh_rk4(s, h):
    k1 = _hh_rhs(s)
    k2 = _hh_rhs([s[i] + h / 2 * k1[i] for i in range(4)])
    k3 = _hh_rhs([s[i] + h / 2 * k2[i] for i in range(4)])
    k4 = _hh_rhs([s[i] + h * k3[i] for i in range(4)])
    return [s[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]


def hh_section(Eh, y0, py0, n=300, h=0.01, maxst=2_000_000):
    val = 2 * Eh - py0 * py0 - y0 * y0 + 2 * y0**3 / 3
    if val <= 0:
        return []
    s = [0.0, y0, math.sqrt(val), py0]
    pts, prev, st = [], s[0], 0
    while len(pts) < n and st < maxst:
        sn = _hh_rk4(s, h)
        st += 1
        if prev < 0 <= sn[0] and sn[2] > 0:
            fr = prev / (prev - sn[0])
            pts.append((s[1] + fr * (sn[1] - s[1]), s[3] + fr * (sn[3] - s[3])))
        prev = sn[0]
        s = sn
    return pts


def py_onshell(f, x0):
    val = (-1 - f["W"](x0, 0.0, E, L)) / f["g22"](x0, 0.0, E, L)
    return math.sqrt(val) if val > 0 else None


def mn_section(f, x0, n=240):
    py = py_onshell(f, x0)
    if py is None or py < 0.05:
        return None
    try:
        pts, drift, _ = section(f, [x0, 0.0, 0.0, py], E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                                n=n, h=0.02, maxst=1_500_000, bounds=BOUNDS)
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    return pts if len(pts) >= 100 else None


VAL_CACHE = OUT / "rotation_number_validation.json"        # deterministic validation — cache it (reboot-safe)
MN_CKPT = OUT / "rotation_number_mn.jsonl"                 # per-orbit MN checkpoint — resume after a reboot
MN_X0S = [3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]


def run_validation():
    """H-H (chaos testbed) + Kerr (integrable control) → threshold + validated flag. Cached to VAL_CACHE."""
    print("(1) VALIDATE on Hénon–Heiles — regular (E=1/12) vs chaotic (E=1/6); classify by box-dim\n")
    hh_reg, hh_cha = [], []
    for Eh, ys in [(1 / 12, [0.0, 0.1, -0.1, 0.15]), (1 / 6, [0.0, 0.1, -0.05, 0.2])]:
        for y0 in ys:
            pts = hh_section(Eh, y0, 0.0)
            if len(pts) < 100:
                continue
            bd = box_dimension(pts)[0]
            fm, dr = freq_drift([p[0] for p in pts])
            (hh_cha if bd > 1.4 else hh_reg).append(dr)
            print(f"      E={Eh:.4f} y0={y0:+.2f}  box-dim={bd:.2f}  f={fm:.4f}  drift={dr:.4f}  "
                  f"({'CHAOTIC (box-dim>1.4)' if bd > 1.4 else 'regular'})", flush=True)
    print("\n(2) KERR (q=0) integrable control — must all read regular (incl. the 1:3 island)\n")
    fk = build_hamilton_numeric(1.0, 0.5, 0.0)
    kerr = []
    for x0 in [3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]:
        pts = mn_section(fk, x0)
        if pts is None:
            continue
        fm, dr = freq_drift([p[0] for p in pts])
        kerr.append({"x0": x0, "box_dim": float(box_dimension(pts)[0]), "freq": fm, "drift": dr})
        print(f"      x0={x0:.2f}  box-dim={kerr[-1]['box_dim']:.2f}  f={fm:.4f}  drift={dr:.4f}", flush=True)
    reg_ceiling = max(max(r["drift"] for r in kerr), max(hh_reg))
    hh_cha_min = min(hh_cha)
    thr = 2.0 * reg_ceiling
    validated = hh_cha_min > thr and reg_ceiling < hh_cha_min
    val = {"detector": "frequency-drift |Δf|/f (first vs second half of the section series)",
           "hh_regular_max": max(hh_reg), "hh_chaotic_min": hh_cha_min, "n_genuinely_chaotic": len(hh_cha),
           "kerr": kerr, "kerr_drift_max": max(r["drift"] for r in kerr),
           "regular_ceiling": reg_ceiling, "threshold": thr, "validated": bool(validated)}
    print(f"\n  regular ceiling (Kerr ∪ HH-reg) = {reg_ceiling:.4f};  HH-chaotic floor = {hh_cha_min:.4f}")
    print(f"  → threshold = {thr:.4f};  detector "
          f"{'VALIDATED ✅ (no Kerr/island false-positive, HH chaos flagged)' if validated else 'NOT clean ❌'}")
    VAL_CACHE.write_text(json.dumps(val, indent=1))
    return val


def load_done_mn():
    done = {}
    if MN_CKPT.exists():
        for line in MN_CKPT.read_text().splitlines():
            try:
                r = json.loads(line); done[r["x0"]] = r
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def main():
    OUT.mkdir(exist_ok=True)
    # phase 1: validation (cached — never recompute the slow part across reboots)
    if VAL_CACHE.exists():
        val = json.loads(VAL_CACHE.read_text())
        print(f"[resume] validation cached: validated={val['validated']}, threshold={val['threshold']:.4f}\n", flush=True)
    else:
        val = run_validation()
    thr = val["threshold"]
    if not val["validated"]:
        print("\n  STOP: detector does not cleanly separate — thin-layer chaos is below accessible resolution")
        print("  (corroborates ansatz §102 'compute-prohibitive'). Box-dimension stays the verdict.")
        return

    # phase 2: MN q=0.6 thin-chaos hunt — per-orbit checkpoint, resume-safe
    done = load_done_mn()
    print(f"(3) MN q=0.6 thin-chaos hunt (drift > {thr:.4f} AND box-dim < 1.4 ⇒ thin layer box-dim missed)"
          f"{'  [resume: '+str(len(done))+' done]' if done else ''}\n", flush=True)
    fm6 = build_hamilton_numeric(1.0, 0.5, 0.6)
    with MN_CKPT.open("a") as ck:
        for x0 in MN_X0S:
            if x0 in done:
                r = done[x0]
                print(f"      x0={x0:.2f}  box-dim={r['box_dim']:.2f}  drift={r['drift']:.4f}  (cached)", flush=True)
                continue
            pts = mn_section(fm6, x0)
            if pts is None:
                continue
            fm, dr = freq_drift([p[0] for p in pts])
            bd = float(box_dimension(pts)[0])
            r = {"x0": x0, "box_dim": bd, "freq": fm, "drift": dr, "thin_chaos": bool(dr > thr and bd < 1.4)}
            ck.write(json.dumps(r) + "\n"); ck.flush()
            done[x0] = r
            print(f"      x0={x0:.2f}  box-dim={bd:.2f}  f={fm:.4f}  drift={dr:.4f}  "
                  f"{'<<< THIN CHAOS (box-dim missed)' if r['thin_chaos'] else ''}", flush=True)

    # phase 3: aggregate
    rows = [done[x0] for x0 in MN_X0S if x0 in done]
    n_thin = sum(1 for r in rows if r["thin_chaos"])
    final = {"E": E, "L": L, **{k: val[k] for k in ("detector", "threshold", "validated", "kerr")},
             "hh": {"regular_max": val["hh_regular_max"], "chaotic_min": val["hh_chaotic_min"]},
             "mn_q06": {"rows": rows, "n_thin_chaos": n_thin}}
    if n_thin:
        final["verdict"] = (f"Frequency-drift detector (validated: Kerr+islands clean, HH chaos flagged) resolves "
                            f"{n_thin} MN q=0.6 orbit(s) as chaotic that box-dim called regular — the thin layer "
                            f"box-dim misses is RESOLVED.")
        print(f"\n  → THIN LAYER RESOLVED: {n_thin} MN orbit(s) chaotic by drift, regular by box-dim.")
    else:
        final["verdict"] = ("Frequency-drift detector (validated on Hénon–Heiles) finds NO thin layer that box-dim "
                            "missed at MN q=0.6 — these moderate-q orbits are genuinely regular even to the sharper "
                            "tool, strengthening leg J's null with a thin-layer-sensitive instrument.")
        print(f"\n  → No thin layer box-dim missed; moderate-q MN orbits regular even to the sharp detector.")
    (OUT / "rotation_number_chaos.json").write_text(json.dumps(final, indent=1))
    print(f"  wrote results/rotation_number_chaos.json", flush=True)


if __name__ == "__main__":
    main()
