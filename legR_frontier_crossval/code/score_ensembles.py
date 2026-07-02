#!/usr/bin/env python3
"""Leg R stage 3 (v2) — unblind: tabula's ensemble verdicts vs pre-registered GR ground truth (stdlib)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results"
TRUTH = {
    "C1": ("regular", "EMIT-regular", "Kerr (integrable, regular)"),
    "C2": ("regular", "EMIT-regular", "MN q=0.5 outer — NON-integrable (§144 illegible, leg O no-KY) yet KAM-regular (leg J)"),
    "C3": ("chaotic", "CERTIFY-CHAOS", "di-hole (chaotic, λ=2.09 §79)"),
}


def main():
    v = json.loads((OUT / "frontier_ensembles.json").read_text())
    print("LEG R stage 3 — unblinding: tabula's regime verdict vs bridge's exact-GR ground truth\n")
    print(f"  {'class':>6} {'expected':>15} {'tabula verdict':>15} {'frac_chaotic':>13}  score")
    rows, q1, wrong = [], True, []
    for tag, (truth, expect, desc) in TRUTH.items():
        r = v[tag]
        verdict = r["verdict"]
        fc = r["info"].get("fraction_chaotic")
        correct = verdict == expect
        if truth == "chaotic":
            if verdict == "EMIT-regular":
                wrong.append(tag)
            if tag in ("C1", "C3") and not correct and verdict != "ABSTAIN":
                q1 = False
        else:
            if verdict == "CERTIFY-CHAOS":
                wrong.append(tag)
            if tag in ("C1", "C3") and not correct and verdict != "ABSTAIN":
                q1 = False
        score = "✅ correct" if correct else ("⚠ ABSTAIN (honest)" if verdict == "ABSTAIN" else "❌ WRONG")
        fcs = f"{fc:.3f}" if fc is not None else "—"
        print(f"  {tag:>6} {expect:>15} {str(verdict):>15} {fcs:>13}  {score}")
        rows.append({"class": tag, "expected": expect, "verdict": verdict, "fraction_chaotic": fc,
                     "correct": bool(correct), "desc": desc})

    c1, c2, c3 = v["C1"]["verdict"], v["C2"]["verdict"], v["C3"]["verdict"]
    q1_ok = c1 == "EMIT-regular" and c3 == "CERTIFY-CHAOS"
    dissoc = c2 == "EMIT-regular"
    print(f"\n  Q1 (C1 regular + C3 chaos — GR competence off-menu): {'PASS ✅' if q1_ok else 'see rows'}")
    print(f"  Q3 (zero wrong CONFIDENT verdicts): {'PASS ✅' if not wrong else 'FAIL ❌ ' + str(wrong)}")
    print(f"\n  Q2 — THE DISSOCIATION (C2 = MN q=0.5):")
    if dissoc:
        print(f"    tabula regime-detector: EMIT-regular  (0-1 test sees KAM tori)")
        print(f"    tabula legibility-probe (§144):  ILLEGIBLE / non-integrable")
        print(f"    → the SAME instrument-family gives OPPOSITE verdicts on the SAME exact GR metric — because")
        print(f"      they measure DIFFERENT things: integrability (exact invariant exists?) vs chaos (regular?).")
        print(f"      This is tabula's own EXP-7 dissociation (law-learnability ≠ predictability), instantiated")
        print(f"      on Manko–Novikov, and it MATCHES the bridge's dual ground truth exactly:")
        print(f"      non-integrable (leg O: no KY tensor) YET dynamically regular (leg J: box-dim + freq-drift).")
    else:
        print(f"    C2 verdict = {c2} (not EMIT-regular) — if CERTIFY-CHAOS this CONTRADICTS the bridge's")
        print(f"    box-dim/frequency-drift regularity for MN q=0.5 outer; investigate.")

    verdict = (("Q1 PASS (Kerr→regular, di-hole→chaos, off tabula's menu); zero wrong confident verdicts. "
                "Q2: MN q=0.5 DISSOCIATES — regime-detector regular vs legibility-probe illegible, the EXP-7 "
                "dissociation on a GR metric, matching the bridge's non-integrable-yet-regular ground truth.")
               if (q1_ok and dissoc and not wrong) else
               "Partial — see rows; C2 verdict %s, wrong=%s." % (c2, wrong))
    (OUT / "score_ensembles.json").write_text(json.dumps(
        {"rows": rows, "Q1_pass": q1_ok, "dissociation": dissoc, "wrong_confident": wrong,
         "verdict": verdict}, indent=1))
    print(f"\n  VERDICT: {verdict}")
    print(f"  wrote results/score_ensembles.json")


if __name__ == "__main__":
    main()
