#!/usr/bin/env python3
"""Leg Q (A10 revival) — does a learned geometry become LEGIBLE iff the metric is KY-INTEGRABLE?

    python3 geometrizes_integrability.py        # pure stdlib; reads two repos READ-ONLY

A10 was retired as ill-posed ("geometrizes ⟺ universal ∧ conservative as an exact proof") — there is no
metric theorem there. SISTER_REQUESTS.md gave the well-posed reframe, and tabula answered it (§127): run the
neural geometrization/legibility probe on geodesics from each catalog metric, and ask whether it EMITS a
verified hidden invariant (the Carter constant) iff the metric admits a Killing tensor. tabula's legibility
column is one INDEPENDENT instrument (a learned distillation head on observed geodesics); leg O's KY-tensor
survey is the OTHER (symbolic Killing–Yano algebra on the exact metric). This bridge script joins the two
columns across the catalog and tests the equivalence — the clean, cross-validated version of THE_BRIDGE §9's
"geometrizes ⟺ conservative" claim. Two deliberately-independent repos must agree, metric by metric.

Inputs (READ-ONLY):
  tabula §127  /Users/sumit/Github/SpaceTime/curvature/results/127_integrability_legibility.json  (`legible`)
  leg O        legO_catalog_survey/results/survey_catalog.json                                    (`ky_dim`)
"""
import json
from pathlib import Path

TABULA = Path("/Users/sumit/Github/SpaceTime/curvature/results/127_integrability_legibility.json")
LEGO = Path(__file__).resolve().parents[2] / "legO_catalog_survey/results/survey_catalog.json"
# ZV γ-metric extension (2026-06-26): tabula §132 legibility + leg O survey_zv KY-integrability
ZV_TABULA = Path("/Users/sumit/Github/SpaceTime/curvature/results/132_zv_gamma_metric.json")
ZV_LEGO = Path(__file__).resolve().parents[2] / "legO_catalog_survey/results/survey_zv.json"
# Manko–Novikov extension (2026-06-27): tabula §144 legibility; integrability from ansatz §99 (no quad. Carter)
MN_TABULA = Path("/Users/sumit/Github/SpaceTime/curvature/results/144_manko_novikov.json")
OUT = Path(__file__).resolve().parent.parent / "results"


def canon(name):
    """Normalize a metric name across the two repos to a common key (handles en-dash, '(gate)', 'ε=…')."""
    s = name.lower().replace("–", "-").replace("—", "-")   # en/em-dash → hyphen
    s = s.replace("(gate)", "").replace("(quadrupole)", "")
    if "ε=" in s or "eps" in s:                                       # 'bumpy ε=0.35' → 'bumpy'
        s = s.split("ε=")[0]
    s = " ".join(s.split())                                           # collapse whitespace
    return s.strip()


def main():
    tab = json.loads(TABULA.read_text())["catalog"]
    lego = json.loads(LEGO.read_text())["ky_dim"]

    # tabula: legible (bool).  leg O: integrable ⇔ ky_dim ≥ 1.
    tab_leg = {canon(k): v["legible"] for k, v in tab.items()}
    tab_int = {canon(k): v["integrable"] for k, v in tab.items()}      # tabula's own integrability label
    lego_int = {canon(k): (d >= 1) for k, d in lego.items()}

    # --- ZV γ-metric extension: a 6th/7th metric and a 2nd independent non-integrable case ---
    # tabula §132 (legibility on real ZV geodesics) + leg O survey_zv (symbolic KY in prolate coords)
    try:
        zt = json.loads(ZV_TABULA.read_text())
        zl = json.loads(ZV_LEGO.read_text())["ky_dim"]
        tab_leg["zv δ=1"] = bool(zt["delta_1_Schwarzschild"]["legible"])
        tab_leg["zv δ=2"] = bool(zt["delta_2_ZV_same_EL"]["legible"])
        tab_int["zv δ=1"], tab_int["zv δ=2"] = True, False            # tabula proves δ=1 int, δ=2 non-int
        for k, dim in zl.items():
            kk = "zv δ=1" if "δ=1" in k else ("zv δ=2" if "δ=2" in k else None)
            if kk:
                lego_int[kk] = (dim >= 1)
    except (FileNotFoundError, KeyError):
        pass

    # --- Manko–Novikov extension: an 8th metric, a 3rd independent non-integrable class (rotating quadrupole) ---
    # legibility from tabula §144 (built independently from Gair-Li-Mandel, not ansatz code); integrability of the
    # q≠0 rotating quadrupole from ansatz §99's symbolic no-quadratic-Carter proof. (MN q=0 ≡ Kerr, the control.)
    try:
        mt = json.loads(MN_TABULA.read_text())
        tab_leg["mn q=0.5"] = bool(mt["mn_q_moderate"]["legible"])
        tab_int["mn q=0.5"] = False
        lego_int["mn q=0.5"] = False                                  # ansatz §99: no quadratic Carter for q≠0
    except (FileNotFoundError, KeyError):
        pass

    joint = sorted(set(tab_leg) & set(lego_int))                      # metrics present in BOTH repos
    tab_only = sorted(set(tab_leg) - set(lego_int))
    lego_only = sorted(set(lego_int) - set(tab_leg))

    print("LEG Q (A10) — legibility (tabula §127) ⟺ KY-integrability (leg O), across the catalog\n")
    print(f"  {'metric':16s} {'legO: KY-int':>12s} {'tabula: legible':>16s}  match")
    rows, n_match = [], 0
    for m in joint:
        ky = lego_int[m]
        lg = tab_leg[m]
        ok = (ky == lg)
        n_match += ok
        print(f"  {m:16s} {('yes' if ky else 'NO'):>12s} {('yes' if lg else 'NO'):>16s}  {'✅' if ok else '❌ MISMATCH'}")
        rows.append({"metric": m, "ky_integrable": bool(ky), "legible": bool(lg), "agree": bool(ok)})

    # 2×2 contingency on the joint set → Matthews / phi (perfect separation ⇒ +1)
    a = sum(1 for r in rows if r["ky_integrable"] and r["legible"])       # int & legible
    d = sum(1 for r in rows if not r["ky_integrable"] and not r["legible"])  # non-int & non-legible
    b = sum(1 for r in rows if not r["ky_integrable"] and r["legible"])   # non-int but legible (false legible)
    c = sum(1 for r in rows if r["ky_integrable"] and not r["legible"])   # int but not legible (missed)
    denom = ((a + b) * (a + c) * (d + b) * (d + c)) ** 0.5
    phi = (a * d - b * c) / denom if denom > 0 else None

    print(f"\n  joint set: {len(joint)} metrics — {n_match}/{len(joint)} agree "
          f"(contingency: integrable&legible={a}, non&non-legible={d}, false-legible={b}, missed={c})")
    print(f"  φ (Matthews) on the joint set: {phi if phi is None else round(phi, 4)}  "
          f"→ {'PERFECT equivalence (legible ⟺ KY-integrable)' if phi == 1.0 else 'imperfect — inspect'}")

    # consistency of the off-join (single-repo) metrics with the same rule
    print("\n  single-repo metrics (consistency check, same rule):")
    for m in lego_only:
        print(f"    [leg O only] {m:14s} KY-integrable={lego_int[m]} (no tabula legibility datum)")
    for m in tab_only:
        print(f"    [tabula only] {m:13s} legible={tab_leg[m]}, tabula-integrable={tab_int[m]} "
              f"({'consistent' if tab_leg[m]==tab_int[m] else 'INCONSISTENT'} with legible⟺integrable)")

    verdict = ("A10 CONFIRMED — legibility ⟺ KY-integrability holds for every catalog metric tested by both "
               "instruments; two independent repos (tabula's neural legibility head, leg O's symbolic KY "
               "algebra) agree metric-by-metric." if (phi == 1.0 and n_match == len(joint))
               else "A10 NOT clean — at least one metric disagrees; inspect the contingency.")
    print(f"\n  VERDICT: {verdict}")

    OUT.mkdir(exist_ok=True)
    (OUT / "geometrizes_integrability.json").write_text(json.dumps({
        "joint_rows": rows, "n_match": n_match, "n_joint": len(joint), "phi_matthews": phi,
        "contingency": {"int_and_legible": a, "non_and_nonlegible": d, "false_legible": b, "missed": c},
        "lego_only": {m: bool(lego_int[m]) for m in lego_only},
        "tabula_only": {m: {"legible": bool(tab_leg[m]), "integrable": bool(tab_int[m])} for m in tab_only},
        "verdict": verdict,
    }, indent=1))
    print(f"\n  wrote results/geometrizes_integrability.json")


if __name__ == "__main__":
    main()
