#!/usr/bin/env python3
"""Leg N / B3 — discover→verify spans GEOMETRIC ↔ TOPOLOGICAL: leg N's holonomy vs tabula's Chern (stdlib).

    python3 topological_discover_verify.py

leg N certified a GEOMETRIC-phase invariant (geodetic-precession holonomy) with the discover→verify
architecture, and drew the contrast explicitly: the holonomy is *geometric* (it shifts continuously with
spin), **not a protected integer** — it left the genuinely TOPOLOGICAL case open. tabula §120 supplies it: a
DeepSets net over Brillouin-zone plaquettes (summing Berry flux) DISCOVERS the **Chern number** — recovered
to R²=0.99, rounding to the exact integer, quantized across parameter regions, robust to deformation, with
bulk-boundary correspondence. Same learn-then-verify architecture, the opposite end of the geometric↔
topological axis, in a second independent repo.

This bridges the two: it shows the discover→verify instrument is **invariant-agnostic** across the whole
spectrum of hidden geometric structure — dynamical (Killing tensor, Move A) → geometric phase (holonomy,
leg N) → topological charge (Chern, tabula §120) — and that the defining difference is quantitative and
exactly as it should be: leg N's holonomy MOVES under a continuous parameter, tabula's Chern STAYS pinned
to its integer under deformation. tabula §120 is consumed READ-ONLY.
"""
import json
from pathlib import Path

TAB120 = Path("/Users/sumit/Github/SpaceTime/curvature/results/120_chern_number.json")
OUT = Path(__file__).resolve().parent.parent / "results"

# leg N's committed geodetic-precession holonomy (results/holonomy.json / FINDINGS), r=8M:
LEGN_HOLONOMY = {"Schwarzschild": 1.337, "Kerr a=0.6": 1.535, "Kerr a=0.9": 1.636}


def main():
    tab = json.loads(TAB120.read_text())

    # GEOMETRIC (leg N): the holonomy shifts continuously with spin → not protected
    base = LEGN_HOLONOMY["Schwarzschild"]
    geo_shift_max = max(abs(v - base) / base for v in LEGN_HOLONOMY.values())

    # TOPOLOGICAL (tabula §120): the Chern stays pinned to its integer under deformation → protected
    chern_r2 = tab["C1_chern_R2"]
    chern_round_acc = tab["C1_round_accuracy"]
    chern_deform = tab["C2_deform_delta"]          # how far the Chern moves under deformation
    sweep = tab["C2_sweep"]
    bulk_boundary = tab["C3_bulk_boundary_pass"]

    print("LEG N / B3 — discover→verify across the GEOMETRIC ↔ TOPOLOGICAL spectrum (two independent repos)\n")
    print("  The SAME learn-then-verify architecture, two ends of the hidden-structure axis:\n")
    legn_recovery = "1.322 vs 1.316"
    chern_recovery = f"R²={chern_r2:.2f}, round {chern_round_acc:.1f}"
    print(f"  {'':14s} {'invariant':28s} {'blind recovery':16s} {'under a parameter change'}")
    print(f"  {'leg N (B3)':14s} {'geodetic-precession holonomy':28s} {legn_recovery:16s} "
          f"SHIFTS +{geo_shift_max:.0%} with spin (geometric)")
    print(f"  {'tabula §120':14s} {'Chern number (Berry flux)':28s} {chern_recovery:16s} "
          f"STAYS ±{chern_deform:.3f} under deform (topological)")

    print(f"\n  GEOMETRIC end (leg N) — holonomy / orbit at r=8M (continuous, spin-dependent):")
    for k, v in LEGN_HOLONOMY.items():
        print(f"    {k:16s} {v:.3f}   ({'+%.0f%% vs Schwarzschild' % (100*(v-base)/base) if v != base else 'reference'})")
    print(f"  → shifts up to +{geo_shift_max:.0%}: a real continuous geometry, NOT a protected integer.")

    print(f"\n  TOPOLOGICAL end (tabula §120) — Chern number (quantized, protected):")
    print(f"    learned-net recovery: R²={chern_r2:.3f}, integer-round accuracy {chern_round_acc:.2f}")
    print(f"    quantized plateaus across the parameter sweep: {sweep}")
    print(f"    deformation robustness: Chern moves only ±{chern_deform:.3f} (stays on its integer)")
    print(f"    bulk-boundary correspondence (edges iff Chern≠0): {'holds ✅' if bulk_boundary else 'fails'}")
    print(f"  → pinned to integers under deformation: a PROTECTED topological charge.")

    ratio = geo_shift_max / chern_deform if chern_deform > 0 else float("inf")
    print(f"\n  THE CONTRAST, QUANTIFIED: the geometric holonomy moves {ratio:.0f}× more under its parameter")
    print(f"  (+{geo_shift_max:.0%}) than the Chern number does under deformation (±{chern_deform:.1%}) — exactly")
    print(f"  the geometric-vs-topological distinction, now instantiated on BOTH sides by the same architecture.")
    print(f"\n  B3 STRENGTHENED: discover→verify is invariant-agnostic across dynamical (Killing tensor, Move A)")
    print(f"  → geometric-phase (holonomy, leg N) → topological (Chern, tabula §120) hidden structure. The two")
    print(f"  independent repos populate opposite ends of the spectrum with one architecture.")

    OUT.mkdir(exist_ok=True)
    (OUT / "topological_discover_verify.json").write_text(json.dumps({
        "geometric_legN": {"holonomy_r8M": LEGN_HOLONOMY, "max_spin_shift_frac": geo_shift_max,
                           "character": "continuous / spin-dependent (not protected)"},
        "topological_tabula120": {"chern_R2": chern_r2, "round_accuracy": chern_round_acc,
                                  "deform_delta": chern_deform, "sweep_plateaus": sweep,
                                  "bulk_boundary_pass": bulk_boundary,
                                  "character": "quantized / deformation-robust (protected)"},
        "geo_shift_over_topo_shift": ratio,
        "verdict": ("discover→verify is invariant-agnostic across the geometric↔topological spectrum: leg N's "
                    "holonomy shifts +%.0f%% under spin (geometric), tabula §120's Chern stays ±%.3f under "
                    "deformation (topological) — same architecture, two independent repos, opposite ends."
                    % (100 * geo_shift_max, chern_deform)),
    }, indent=1))
    print(f"\n  wrote results/topological_discover_verify.json")


if __name__ == "__main__":
    main()
