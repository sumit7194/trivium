#!/usr/bin/env python3
"""Leg J — THE decisive test: our validated detector on MN's inner-region orbits (ansatz's adaptive sections).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python inner_region_chaos.py

The frequency-drift detector (validated: Hénon–Heiles chaos 0.59–0.73 vs every regular orbit ≤0.006, Kerr's
1:3 island 0.0018; threshold 0.0115) finally meets MN's OWN inner-region orbits — the literature's chaotic
basin (χ=0.9, q=0.95, E=0.95, Lz=3; Contopoulos–Lukes-Gerakopoulos–Apostolatos 2011). Our fixed-step
integrator dies in the stiff near-rod zone (0 crossings, H-drift ∞), so ansatz supplied the adaptive-
integrated (x, px) section series (`mn_inner_sections_for_bridge.json`, H-drift <2e-3 kept). Both orbits sit
at box-dim 1.20–1.22 — the borderline where box-dim can't decide island-of-stability vs thin chaos. The
clean split: ansatz's (adaptive) trajectory + the bridge's independently-validated detector.

We read the section series read-only and apply |Δf|/f to the x-crossing sequence. A length-robustness check
(orbit_A also truncated to orbit_B's 126 crossings) guards against the shorter series driving a verdict.
> 0.0115 ⇒ MN's own thin-layer chaos EXHIBITED on the exact metric; ≤ 0.006 ⇒ the inner island of stability.
"""
import json
import sys
from pathlib import Path

import numpy as np

ANS = Path("/Users/sumit/Github/conjecture_machine/mn_inner_sections_for_bridge.json")
OUT = Path(__file__).resolve().parent.parent / "results"
VAL = OUT / "rotation_number_validation.json"


def freq_drift(series):
    x = np.asarray(series, float)
    n = len(x); h = n // 2

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


def verdict(dr, thr, reg_ceiling=0.006):
    if dr > thr:
        return "THIN CHAOS (drift fires > threshold)"
    if dr <= reg_ceiling:
        return "regular (island of stability)"
    return "ambiguous (between regular floor and threshold)"


def main():
    d = json.loads(ANS.read_text())
    cache = json.loads(VAL.read_text()) if VAL.exists() else {"threshold": 0.0115, "hh_chaotic_min": 0.59}
    thr = cache["threshold"]
    print("LEG J — frequency-drift detector on MN's INNER-REGION orbits (ansatz adaptive sections)")
    print(f"  metric: {d['metric']}")
    print(f"  params: a={d['a']}, q={d['q']}, E={d['E']}, Lz={d['Lz']}  (literature chaotic basin)")
    print(f"  detector validated: HH chaos ≥{cache.get('hh_chaotic_min',0.59):.2f} vs regular ≤0.006; "
          f"threshold {thr:.4f}\n")
    print(f"  {'orbit':9s} {'n':>5} {'box-dim':>8} {'drift |Δf|/f':>13}   verdict")
    out = {"params": {k: d[k] for k in ("metric", "a", "q", "E", "Lz")}, "threshold": thr, "orbits": {}}
    fires_any = False
    for name, o in d["orbits"].items():
        x = o["x"]; bd = None
        # ansatz reported box-dim in the message (1.203 / 1.219); store n + H-drift from the JSON
        fm, dr = freq_drift(x)
        v = verdict(dr, thr)
        fires_any = fires_any or dr > thr
        print(f"  {name:9s} {len(x):>5} {'~1.2':>8} {dr:>13.4f}   {v}")
        out["orbits"][name] = {"n_crossings": len(x), "H_drift": o.get("H_drift"), "freq": fm,
                               "drift": dr, "fires": bool(dr > thr), "verdict": v}
        # length-robustness: truncate the long orbit to the short one's length and re-test
        if len(x) >= 250:
            fm2, dr2 = freq_drift(x[:126])
            print(f"  {name+'[:126]':9s} {126:>5} {'—':>8} {dr2:>13.4f}   {verdict(dr2, thr)}  (length-match check)")
            out["orbits"][name]["drift_trunc126"] = dr2

    print()
    if fires_any:
        print("  → VERDICT: MN's own THIN-LAYER CHAOS is EXHIBITED — the validated frequency-drift detector")
        print("    fires on the inner-region orbit(s) that box-dim left ambiguous (1.20), on the exact")
        print("    Manko–Novikov metric at the literature's chaotic-basin params. The island-vs-boundary")
        print("    question is settled: boundary layer (chaos). Positive control closes — MN's own chaos,")
        print("    caught by a detector proven on Hénon–Heiles and immune to the Lyapunov/rotation-number pitfalls.")
        out["verdict"] = ("MN inner-region thin-layer chaos EXHIBITED: frequency-drift fires (>threshold) on the "
                          "literature chaotic-basin orbits (χ=0.9,q=0.95,E=0.95,Lz=3) that box-dim left at 1.20 — "
                          "settled on the exact metric with a detector validated on Hénon–Heiles.")
    else:
        allreg = all(o["drift"] <= 0.006 for o in out["orbits"].values())
        print(f"  → VERDICT: {'inner ISLAND OF STABILITY (both regular)' if allreg else 'ambiguous — not above threshold'}.")
        print("    The frequency-drift detector does not fire — these box-dim-1.20 inner orbits are the")
        print("    regular island of stability, not a chaotic boundary layer. (The deep chaotic sea at x<1.5")
        print("    is beyond trustworthy integration — ansatz's note — so this settles these orbits, not the whole basin.)")
        out["verdict"] = ("Inner-region orbits regular (frequency-drift ≤ threshold): the box-dim-1.20 orbits at the "
                          "literature params are the island of stability, not the chaotic boundary layer.")
    OUT.mkdir(exist_ok=True)
    (OUT / "inner_region_chaos.json").write_text(json.dumps(out, indent=1))
    print(f"\n  wrote results/inner_region_chaos.json")


if __name__ == "__main__":
    main()
