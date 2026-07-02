#!/usr/bin/env python3
"""Leg R stage 3 — unblind: score tabula's verdicts against the pre-registered GR ground truth (stdlib).

    python3 score_verdicts.py

Ground truth (frozen in PREREGISTRATION.md before stage 2 ran): S1–S5 regular (Kerr integrable; Kerr 1:3
island; MN outer ×2; MN inner island orbit_A), S6 thin chaos (MN inner boundary layer, established by the
bridge's validated frequency-drift detector + ansatz's independent reimplementation). Scores P1–P4.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results"
TRUTH = {
    "S1": ("regular", "Kerr a=0.5 (integrable)"),
    "S2": ("regular", "Kerr 1:3 resonant island (the rotation-number trap)"),
    "S3": ("regular", "MN q=0.5 outer (box-dim 1.06, drift 0.0000)"),
    "S4": ("regular", "MN q=0.6 2/3-resonance centre (drift 0.0000)"),
    "S5": ("regular", "MN inner orbit_A — island of stability (drift 0.0000)"),
    "S6": ("chaotic", "MN inner orbit_B — thin boundary layer (drift 0.980)"),
}
REG_OK = {"EMIT-regular"}
CHA_OK = {"CERTIFY-CHAOS"}


def main():
    v = json.loads((OUT / "frontier_verdicts.json").read_text())
    print("LEG R stage 3 — unblinding: tabula's blind verdicts vs pre-registered GR ground truth\n")
    print(f"  {'tag':>4} {'truth':>8} {'tabula verdict':>16} {'K':>7}  score")
    rows, p1_ok, wrong_confident = [], True, []
    for tag, (truth, desc) in TRUTH.items():
        r = v[tag]
        verdict, K = r["verdict"], r.get("K_raw")
        if truth == "regular":
            ok = verdict in REG_OK
            score = "✅ correct" if ok else ("⚠ ABSTAIN (honest, not wrong)" if verdict == "ABSTAIN"
                                             else "❌ FALSE CHAOS")
            if verdict in CHA_OK:
                wrong_confident.append(tag)
            if not ok and verdict != "ABSTAIN":
                p1_ok = False
            if verdict == "ABSTAIN":
                p1_ok = False                                 # P1 demanded EMIT-regular outright
        else:
            ok = verdict in CHA_OK
            score = ("✅ chaos confirmed (3rd instrument!)" if ok else
                     ("✅ ABSTAIN as pre-registered (n<800 floor)" if verdict == "ABSTAIN" else "❌ EMIT on chaos"))
            if verdict in REG_OK:
                wrong_confident.append(tag)
        kstr = f"{K:.3f}" if K is not None else "—"
        print(f"  {tag:>4} {truth:>8} {str(verdict):>16} {kstr:>7}  {score}   ({desc})")
        rows.append({"tag": tag, "truth": truth, "verdict": verdict, "K_raw": K, "desc": desc,
                     "subfloor_note": r.get("subfloor_note")})

    s6 = v["S6"]
    print(f"\n  P1 (S1–S5 all EMIT-regular): {'PASS ✅' if p1_ok else 'not in full — see rows'}")
    print(f"  P2/P3 (S6): verdict = {s6['verdict']};  raw sub-floor K = "
          f"{s6['K_raw']:.3f}" if s6.get("K_raw") is not None else "")
    print(f"  P4 (zero wrong CONFIDENT verdicts): {'PASS ✅' if not wrong_confident else 'FAIL ❌ on ' + str(wrong_confident)}")
    (OUT / "score_verdicts.json").write_text(json.dumps(
        {"rows": rows, "P1_all_regular_emit": p1_ok, "wrong_confident": wrong_confident}, indent=1))
    print(f"\n  wrote results/score_verdicts.json")


if __name__ == "__main__":
    main()
