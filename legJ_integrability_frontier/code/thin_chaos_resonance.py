#!/usr/bin/env python3
"""Leg J — aim the validated frequency-drift detector at MN's 2/3 resonance (ansatz's exact ICs). (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python thin_chaos_resonance.py

The blind q=0.6 sweep (rotation_number_chaos.py) read regular — but it was the wrong slice: a=0.5, Lz=2.8.
ansatz located the documented thin layer precisely (Contopoulos–Lukes-Gerakopoulos–Apostolatos 2011): the
2/3 resonance at a=0.9, q=0.6, E=0.95, **Lz=3.0** sits at **x0≈7.7**, with the separatrix (where the thin
chaotic layer lives) at the island edges. ansatz's own box-dim only grazes there (1.03) and its λ floors
(0.005) — below their resolution, exactly the regime this detector was built for. This aims the validated
frequency-drift detector at x0∈[7.3,8.1] on that slice, with the q=0 (Kerr) integrable control alongside.

Detector + threshold come from the validated run (rotation_number_validation.json: HH chaos 0.59–0.73 vs
regular ≤0.006, Kerr 1:3 island clean, threshold 0.0115). Reboot-resilient: per-orbit JSONL checkpoint.
If MN q=0.6 drift fires across the bracket where Kerr q=0 stays flat → MN's own thin layer is EXHIBITED.
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
CKPT = OUT / "thin_chaos_resonance.jsonl"
VAL = OUT / "rotation_number_validation.json"
A, E, L = 0.9, 0.95, 3.0                                    # ansatz's target slice (a=χ=0.9, Lz=3.0)
BOUNDS = ((1.05, 60.0), (-1.0, 1.0))
X0S = [round(7.30 + 0.05 * k, 2) for k in range(17)]        # 7.30 … 8.10, the 2/3 separatrix bracket


def freq_drift(series, min_n=100):
    if len(series) < min_n:
        return None, None
    x = np.asarray(series, float); n = len(x); h = n // 2

    def peak(seg):
        seg = (seg - seg.mean()) * np.hanning(len(seg))
        F = np.abs(np.fft.rfft(seg))
        if len(F) < 4:
            return 0.0
        F[0] = 0.0
        k = int(np.argmax(F))
        if 1 <= k < len(F) - 1:
            a, b, c = F[k - 1], F[k], F[k + 1]; den = a - 2 * b + c
            k = k + (0.5 * (a - c) / den if den != 0 else 0.0)
        return k / len(seg)

    f1, f2 = peak(x[:h]), peak(x[h:]); fm = 0.5 * (f1 + f2)
    return fm, (abs(f1 - f2) / fm if fm > 1e-9 else abs(f1 - f2))


def mn_section(f, x0, n=240):
    val = (-1 - f["W"](x0, 0.0, E, L)) / f["g22"](x0, 0.0, E, L)
    if val <= 0:
        return None
    py = math.sqrt(val)
    if py < 0.05:
        return None
    try:
        pts, _, _ = section(f, [x0, 0.0, 0.0, py], E, L, sec_idx=1, sec_val=0.0, rec=(0, 2),
                            n=n, h=0.02, maxst=1_800_000, bounds=BOUNDS)
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    return pts if len(pts) >= 100 else None


def load_done():
    done = set()
    if CKPT.exists():
        for line in CKPT.read_text().splitlines():
            try:
                r = json.loads(line); done.add((r["q"], r["x0"]))
            except (json.JSONDecodeError, KeyError):
                pass
    return done


def main():
    OUT.mkdir(exist_ok=True)
    thr = json.loads(VAL.read_text())["threshold"] if VAL.exists() else 0.0115
    print(f"LEG J — frequency-drift at MN's 2/3 resonance (a={A}, E={E}, Lz={L}); threshold={thr:.4f}")
    print(f"  ansatz target: 2/3 resonance at x0≈7.7, separatrix at the island edges; q=0 Kerr control.\n")
    done = load_done()
    print(f"  {'q':>4} {'x0':>5} {'box-dim':>8} {'freq':>7} {'drift':>8}  flag")
    rows = []
    with CKPT.open("a") as ck:
        for q, label in [(0.0, "Kerr control"), (0.6, "MN bump")]:
            f = build_hamilton_numeric(1.0, A, q)
            for x0 in X0S:
                if (q, x0) in done:
                    continue
                pts = mn_section(f, x0)
                if pts is None:
                    continue
                fm, dr = freq_drift([p[0] for p in pts])
                bd = float(box_dimension(pts)[0])
                fires = bool(dr > thr)
                r = {"q": q, "x0": x0, "box_dim": bd, "freq": fm, "drift": dr, "fires": fires, "n": len(pts)}
                ck.write(json.dumps(r) + "\n"); ck.flush()
                rows.append(r)
                tag = ("<<< CHAOS (drift fires)" if fires else "regular")
                print(f"  {q:>4} {x0:>5.2f} {bd:>8.2f} {fm:>7.4f} {dr:>8.4f}  {tag}", flush=True)

    # reload all (incl. any from a prior interrupted run)
    allrows = [json.loads(l) for l in CKPT.read_text().splitlines() if l.strip()]
    kerr = [r for r in allrows if r["q"] == 0.0]
    mn = [r for r in allrows if r["q"] == 0.6]
    kerr_clean = all(not r["fires"] for r in kerr)
    mn_fires = [r for r in mn if r["fires"]]
    print(f"\n  ASSESSMENT (a={A}, E={E}, Lz={L}, 2/3 resonance bracket):")
    print(f"    Kerr (q=0) control: {'all regular ✅' if kerr_clean else 'FIRES on Kerr ⚠ (false-positive — investigate)'}")
    if mn_fires and kerr_clean:
        x0s = ", ".join(f"{r['x0']}" for r in mn_fires)
        dmax = max(r["drift"] for r in mn_fires)
        bdmax = max(r["box_dim"] for r in mn_fires)
        print(f"    MN q=0.6: drift FIRES at x0 = {x0s} (max drift {dmax:.3f}, box-dim there only {bdmax:.2f})")
        print(f"    → MN's OWN THIN-LAYER CHAOS is EXHIBITED — the validated frequency-drift detector resolves")
        print(f"      the 2/3-resonance separatrix that box-dimension grazes (≤{bdmax:.2f}). Positive control closes.")
        verdict = (f"EXHIBITED: at the documented 2/3 resonance (a=0.9, q=0.6, E=0.95, Lz=3.0), the validated "
                   f"frequency-drift detector fires (drift up to {dmax:.3f}) at x0={x0s} where box-dim only "
                   f"grazes ({bdmax:.2f}) and Kerr stays regular — MN's own thin-layer chaos, on the exact metric.")
    elif kerr_clean:
        print(f"    MN q=0.6: no drift fired across [7.3,8.1] — the q=0.6 outer-region layer is below resolution")
        print(f"      (Nekhoroshev-thin, as ansatz cautioned). Next: push q→0.8 on the same Lz=3.0 slice.")
        verdict = ("Clean at q=0.6 on the 2/3 bracket — the outer-region layer is exponentially thin (ansatz's "
                   "Nekhoroshev caveat). Detector validated; push q→0.8 same slice, or the inner-region orbit.")
    else:
        verdict = "Kerr control fired — detector/threshold needs review at a=0.9 before trusting MN."
    (OUT / "thin_chaos_resonance.json").write_text(json.dumps(
        {"a": A, "E": E, "L": L, "threshold": thr, "rows": sorted(allrows, key=lambda r: (r["q"], r["x0"])),
         "kerr_clean": kerr_clean, "mn_fires": len(mn_fires), "verdict": verdict}, indent=1))
    print(f"\n  wrote results/thin_chaos_resonance.json")


if __name__ == "__main__":
    main()
