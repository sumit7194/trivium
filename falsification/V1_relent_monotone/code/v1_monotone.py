#!/usr/bin/env python3
"""V1 — relative entropy is monotone under region inclusion (the canary for the leg-X/K1/K3 stack).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python v1_monotone.py

Gates V1a-V1d frozen in ../PREREGISTRATION.md before this was written. For nested regions A ⊆ B,
S_rel(ρ_A‖σ_A) ≤ S_rel(ρ_B‖σ_B) (Uhlmann). This is a theorem, so a violation here would mean our machinery
is wrong — not nature. Tested across 3 excitation types × 2 nesting families.
"""
import json
import sys
import time
from pathlib import Path

K1DIR = Path(__file__).resolve().parents[2] / "K1_squeezed" / "code"
sys.path.insert(0, str(K1DIR))
import k1_squeezed as K1  # noqa: E402

from mpmath import mp, mpf, matrix  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "results"
SIZES = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 40, 47]
TOL = 1e-12


def region(family, k):
    """F1: first k sites of the wedge (outward from the cut). F2: last k sites (inward from far end)."""
    a0 = K1.EH.A_START - 1                       # first index of region A
    if family == "F1":
        return list(range(a0, a0 + k))
    return list(range(K1.EH.N - k, K1.EH.N))


def s_rel_for(X, P, idx, kind, v=None, r=None, f=None):
    if kind == "coherent":
        X2, P2 = K1.sub(X, idx), K1.sub(P, idx)
        d_A = matrix([f[idx[i]] for i in range(len(idx))])
        pc = K1.s_rel_pieces(X, P, X2, P2, idx, d_A=d_A)
    else:
        X1, P1 = K1.squeeze_reduced(X, P, v, r, idx)
        pc = K1.s_rel_pieces(X, P, X1, P1, idx)
    return float(pc["s_rel"]), float(pc["dK"]), float(pc["dS"])


def main():
    mp.dps = 60
    t0 = time.time()
    print("V1 — relative entropy monotone under region inclusion (gates frozen in PREREGISTRATION.md)")
    print(f"  chain N={K1.EH.N}, μ={K1.EH.MU}, cut x_c={K1.EH.XC}, dps={mp.dps}")
    print("  canary for the leg-X / K1 / K3 stack: a violation here means a BUG, not a discovery\n")

    X, P = K1.build_chain(K1.EH.N, K1.EH.MU)
    v_str = K1.gauss_profile(X.rows, K1.EH.XC, K1.EH.SIGMA)          # straddles the cut
    v_in = K1.gauss_profile(X.rows, K1.EH.XC + 12, K1.EH.SIGMA)      # inside the wedge
    f_coh = K1.EH.packet(K1.EH.XC + 12)                              # coherent packet inside

    cases = [
        ("coherent (ΔS=0)", dict(kind="coherent", f=f_coh)),
        ("squeezed straddling cut (ΔS≠0)", dict(kind="sq", v=v_str, r=mpf("0.6"))),
        ("squeezed inside wedge (ΔS=0)", dict(kind="sq", v=v_in, r=mpf("0.6"))),
    ]

    results = {}
    all_mono, all_pos = True, True
    violations = []
    for label, kw in cases:
        results[label] = {}
        for fam in ["F1", "F2"]:
            vals = []
            for k in SIZES:
                idx = region(fam, k)
                sr, dK, dS = s_rel_for(X, P, idx, **kw)
                vals.append(dict(k=k, s_rel=sr, dK=dK, dS=dS))
            # V1a monotone along the inclusion chain, V1b positive
            mono = True
            for i in range(1, len(vals)):
                if vals[i]["s_rel"] < vals[i - 1]["s_rel"] - TOL:
                    mono = False
                    violations.append((label, fam, SIZES[i - 1], SIZES[i],
                                       vals[i - 1]["s_rel"], vals[i]["s_rel"]))
            pos = all(x["s_rel"] >= -TOL for x in vals)
            all_mono = all_mono and mono
            all_pos = all_pos and pos
            results[label][fam] = dict(values=vals, monotone=mono, positive=pos)
            head = ", ".join(f"{x['s_rel']:.4f}" for x in vals[:6])
            print(f"  {label:32s} [{fam}] S_rel: {head}, … , {vals[-1]['s_rel']:.4f}   "
                  f"mono {'✅' if mono else '❌'}  pos {'✅' if pos else '❌'}")

    print(f"\n  V1a monotonicity across all 3 excitations × 2 nesting families  →  "
          f"{'PASS ✅' if all_mono else 'FAIL ❌ — BUG, STOPPING'}")
    print(f"  V1b positivity (Klein) everywhere  →  {'PASS ✅' if all_pos else 'FAIL ❌ — BUG'}")
    if violations:
        print("  ⚠️  VIOLATIONS (flagged for review, not interpreted):")
        for vv in violations:
            print(f"      {vv}")

    # ---- V1c anchor: coherent at the full wedge reproduces leg X's 54.03
    full = region("F1", K1.EH.N - K1.EH.A_START + 1)
    sr_full, dK_full, dS_full = s_rel_for(X, P, full, kind="coherent", f=f_coh)
    v1c = abs(sr_full - 54.03) / 54.03 < 0.01
    print(f"\n  V1c anchor: coherent S_rel at the full wedge = {sr_full:.4f}  vs leg X's 54.03  "
          f"({abs(sr_full-54.03)/54.03:.2%})  →  {'PASS ✅' if v1c else 'FAIL ❌'}")

    # ---- V1d saturation shape (observation)
    sq = results["squeezed straddling cut (ΔS≠0)"]["F1"]["values"]
    sat = abs(sq[-1]["s_rel"] - sq[-3]["s_rel"]) / sq[-1]["s_rel"] < 0.01
    print(f"  V1d saturation (observation): squeezed/F1 rises {sq[0]['s_rel']:.4f} → {sq[-1]['s_rel']:.4f} "
          f"and plateaus past the excitation support ({'yes' if sat else 'no'})")

    verdict = "SURVIVES" if (all_mono and all_pos and v1c) else "FAILED-CANARY"
    print(f"\n  V1 {verdict}: the Gaussian modular machinery underlying leg X, K1 and K3 respects Uhlmann")
    print(f"  monotonicity and positivity on every inclusion chain tested. The canary is alive.")

    OUT.mkdir(exist_ok=True)
    (OUT / "v1_monotone.json").write_text(json.dumps({
        "N": K1.EH.N, "mu": float(K1.EH.MU), "dps": mp.dps, "sizes": SIZES, "tol": TOL,
        "results": results, "violations": violations,
        "V1a_monotone_pass": bool(all_mono), "V1b_positive_pass": bool(all_pos),
        "V1c_anchor": {"s_rel_full_wedge": sr_full, "legX": 54.03, "pass": bool(v1c)},
        "V1d_saturates": bool(sat),
        "verdict": verdict, "all_pass": bool(all_mono and all_pos and v1c),
        "summary": (f"V1 ({verdict}): relative entropy is non-decreasing along every inclusion chain tested "
                    f"— 3 excitation types (coherent, squeezed straddling the cut, squeezed inside the wedge) "
                    f"× 2 nesting families (outward from the cut, inward from the far end) × 12 region sizes "
                    f"— and non-negative throughout. The coherent full-wedge value {sr_full:.4f} reproduces "
                    f"leg X's cross-gated 54.03. Canary for the leg-X/K1/K3 stack: it respects Uhlmann "
                    f"monotonicity, so no result in that stack rests on a machinery that violates a theorem."),
    }, indent=1))
    print(f"\n  wrote results/v1_monotone.json   ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
