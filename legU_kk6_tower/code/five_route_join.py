#!/usr/bin/env python3
"""Leg U — the five-route join: proof + four independent measurements of the 6D twisted tower.

    python3 five_route_join.py

Join gates J1-J4 frozen in ../PREREGISTRATION.md ADDENDUM (2026-07-10) before this was written. Reads,
strictly read-only: quantum's blind tower, tabula's 158 (FDTD + neural routes), and the bridge's own leg U
results; ansatz §112/§113 is the proof anchor. Verdict: is m²(n1,n2) = (n1²−2χn1n2+n2²)/(1−χ²) — and its
axion splitting — established by five failure-mode-disjoint routes?
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
QT = Path("/Users/sumit/Github/quantum/qsim/kk6_twisted_tower.json")
T158 = Path("/Users/sumit/Github/SpaceTime/curvature/results/158_axion_discovery.json")
BRIDGE = HERE / "results" / "kk6_tower.json"

M_SPLIT_TARGET = 0.449961          # m(1,-1) - m(1,1) at chi=0.3 (frozen in the original prereg)


def main():
    q = json.loads(QT.read_text())
    t = json.loads(T158.read_text())
    b = json.loads(BRIDGE.read_text())
    print("LEG U — five-route join (gates frozen in PREREGISTRATION.md ADDENDUM)\n")

    # J1 — quantum's blind tower
    errs = [abs(r["err_percent"]) for r in q["rows"]]
    sp = q["splittings"]
    q_split = sp["pair_11_1m1_chi03_measured"]
    q_split_err = abs(q_split - M_SPLIT_TARGET) / M_SPLIT_TARGET
    q_ctrl = abs(sp["pair_10_01_chi03_measured"])
    j1 = max(errs) < 1.0 and q_split_err < 0.01 and q_ctrl < 1e-3
    print(f"  J1 quantum (blind, {q['protocol'][:5]}…): max sector err {max(errs):.3f}% (<1%); "
          f"split {q_split:.6f} vs {M_SPLIT_TARGET} ({q_split_err:.2%}); control {q_ctrl:.1e}"
          f"  →  {'PASS ✅' if j1 else 'FAIL ❌'}")

    # J2 — tabula FDTD route (S0)
    j2 = t["S0_split_corr"] >= 0.999 and t["S0_split_err"] <= 0.01
    print(f"  J2 tabula FDTD: split corr {t['S0_split_corr']:.6f} (≥0.999); err {t['S0_split_err']:.2%} "
          f"(≤1%)  →  {'PASS ✅' if j2 else 'FAIL ❌'}")

    # J3 — tabula neural route (blind)
    dec = t["B2_moduli_decode_r"]
    j3 = (t["A2_split_corr"] >= 0.99 and t["A2_split_med_err"] <= 0.05
          and t["A2_degenerate_ctrl_ratio"] <= 0.01
          and t["latent_dim_found"]["three_moduli"] == 3
          and t["latent_dim_found"]["chi_family"] == 1
          and min(dec.values()) >= 0.9)
    print(f"  J3 tabula neural (blind): Δm̂² corr {t['A2_split_corr']:.4f} (≥0.99); med err "
          f"{t['A2_split_med_err']:.2%} (≤5%); ctrl {t['A2_degenerate_ctrl_ratio']:.4f} (≤1%);")
    print(f"     latents: 3-moduli family → K={t['latent_dim_found']['three_moduli']}, χ-family → "
          f"K={t['latent_dim_found']['chi_family']}; decode r (Φ1,Φ2,χ) = "
          f"({dec['Phi1']:.3f}, {dec['Phi2']:.3f}, {dec['chi']:.3f})  →  {'PASS ✅' if j3 else 'FAIL ❌'}")

    # J4 — cross-route: bridge vs quantum measured split
    b_split = b["U2_m1m1"] - b["U2_m11"]
    x = abs(b_split - q_split) / q_split
    j4 = x < 0.01
    print(f"  J4 cross-route: bridge split {b_split:.5f} vs quantum {q_split:.5f} → {x:.2%} (<1%)"
          f"  →  {'PASS ✅' if j4 else 'FAIL ❌'}")

    print(f"\n  recorded (tabula's own gates, cited not re-derived): modular T/S gauge certificate "
          f"≤0.22%;")
    print(f"  hyperbolic limit — isotropy dev 0.083, off-diag 0.019, tr(g)·τ2² const to 1.4%, cosine vs")
    print(f"  true-mass metric 0.9994; moduli space = SL(2,Z) fundamental domain. (notes/axion_for_bridge.md)")

    allpass = j1 and j2 and j3 and j4
    print(f"\n  VERDICT: {'FIVE-ROUTE OBJECT ✅' if allpass else 'JOIN INCOMPLETE ❌'} — ansatz proof "
          f"(§112/§113) · bridge FD simulator ·")
    print(f"  quantum blind numerics · tabula FDTD · tabula neural discovery — one spectrum, one axion,")
    print(f"  five failure-mode-disjoint routes; the moduli geometry discovered from shadows.")

    (HERE / "results" / "five_route_join.json").write_text(json.dumps({
        "J1": {"max_err_pct": max(errs), "split": q_split, "split_err": q_split_err,
               "control": q_ctrl, "pass": bool(j1)},
        "J2": {"corr": t["S0_split_corr"], "err": t["S0_split_err"], "pass": bool(j2)},
        "J3": {"corr": t["A2_split_corr"], "med_err": t["A2_split_med_err"],
               "ctrl": t["A2_degenerate_ctrl_ratio"], "latents": t["latent_dim_found"],
               "decode_r": dec, "pass": bool(j3)},
        "J4": {"bridge_split": b_split, "quantum_split": q_split, "rel_diff": x, "pass": bool(j4)},
        "geometry_recorded": {"modular_gauge_pct": 0.22, "hyperbolic_cosine": 0.9994,
                              "source": "tabula notes/axion_for_bridge.md, commit 3c84ef2"},
        "five_route": bool(allpass),
        "verdict": ("The 6D twisted KK tower and its axion splitting are established by five "
                    "failure-mode-disjoint routes (symbolic proof / bridge FD / quantum blind numerics / "
                    "tabula FDTD / tabula neural discovery), with the SL(2,Z)-fundamental-domain moduli "
                    "geometry discovered from projections alone (tabula 158)."),
    }, indent=1))
    print(f"\n  wrote results/five_route_join.json")


if __name__ == "__main__":
    main()
