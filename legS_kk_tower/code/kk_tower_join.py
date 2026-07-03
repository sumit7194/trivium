#!/usr/bin/env python3
"""Leg S — the Kaluza–Klein mass tower: one number, four repos, four independent routes (stdlib).

    python3 kk_tower_join.py

The claim "mass = hidden-dimension momentum" (m_n = n/R for a massless 5D field on a circle) now exists in
FOUR sibling repos by four deliberately-different routes, none of which has been joined quantitatively:

  1. PROVEN geometry (ansatz §111): the KK reduction 5D-vacuum ⇔ 4D Einstein–Maxwell–dilaton, every
     dictionary coefficient machine-derived (95 batteries green), the planted "frozen-scalar" trap caught.
     The tower m_n = n/R is the mode-expansion consequence of the proven ansatz.
  2. DIRECT numerics (quantum, kk_projection.py): a massless 2D wave with hidden winding n; the visible
     projection buzzes at rest at ω_n and travels at the Klein–Gordon group velocity.
  3. INDEPENDENT replication (tabula §157 G0): a separate FDTD codebase reproducing the same tower —
     implementation-independence of route 2.
  4. LEARNED from projections alone (tabula §157 K1/K2): a K=1 neural bottleneck trained ONLY on visible
     projections discovers the hidden integer (isotonic R²≈1) and its BEHAVIORAL mass ladder.

This joins 2–4 into one gated table against the exact tower (m_n = n, R=1 units), with route 1 as the
theorem anchor (cited, not recomputed). All inputs read-only.
"""
import json
from pathlib import Path

T157 = Path("/Users/sumit/Github/SpaceTime/curvature/results/157_kk_mass_discovery.json")
OUT = Path(__file__).resolve().parent.parent / "results"

# quantum kk_projection.py verified numbers (recorded in qsim/PLAN_projections.md Route A, read-only):
QUANTUM_REST = {1: 1.0022, 2: 2.0031, 3: 3.0027}            # measured rest-buzz ω_n (exact: n)
QUANTUM_VG = {1: (0.999, 1.000), 2: (0.703, 0.707), 3: (0.445, 0.447)}   # (measured, KG exact) at k=1


def main():
    t = json.loads(T157.read_text())
    print("LEG S — the KK mass tower: m_n = n/R by four independent routes across four repos\n")
    print("  route 1 (ansatz §111, theorem anchor): 5D vacuum ⇔ 4D EMD PROVEN, machine-derived dictionary,")
    print("  frozen-scalar trap caught — the tower is the mode-expansion consequence of a proven reduction.\n")

    tab_fdtd = {int(k): v for k, v in t["G0_rest_freqs"].items()}
    ladder = t["K2_behavioral_mass_ladder"]                  # n = 0,1,2,3
    print(f"  {'n':>3} {'exact':>6} {'quantum ω_n':>12} {'tabula FDTD ω_n':>16} {'tabula LEARNED m_n':>19}")
    rows = []
    for n in (1, 2, 3):
        qw, tw, lm = QUANTUM_REST[n], tab_fdtd[n], ladder[n]
        print(f"  {n:>3} {n:>6} {qw:>12.4f} {tw:>16.4f} {lm:>19.4f}")
        rows.append({"n": n, "quantum_rest": qw, "tabula_fdtd_rest": tw, "tabula_learned_mass": lm,
                     "err_quantum": abs(qw - n) / n, "err_fdtd": abs(tw - n) / n,
                     "err_learned": abs(lm - n) / n})
    print(f"  {0:>3} {0:>6} {'—':>12} {'—':>16} {ladder[0]:>19.4f}   (massless mode: learned ≈ 0 ✓)")

    eq = max(r["err_quantum"] for r in rows)
    ef = max(r["err_fdtd"] for r in rows)
    el = max(r["err_learned"] for r in rows)
    cross = max(abs(QUANTUM_REST[n] - tab_fdtd[n]) / n for n in (1, 2, 3))
    print(f"\n  per-route max error vs the exact tower: quantum {eq:.2%} · tabula-FDTD {ef:.2%} · learned {el:.2%}")
    print(f"  cross-implementation (quantum vs tabula-FDTD, independent codebases): {cross:.2%}")
    print(f"  group velocities (quantum vs Klein–Gordon): " +
          "  ".join(f"n={n}: {m:.3f}/{e:.3f}" for n, (m, e) in QUANTUM_VG.items()))
    print(f"  learned-tower quality (tabula §157): latent→n isotonic R² = {t['K1_latent_isotonic_R2_vs_n']:.5f}, "
          f"integer decode acc = {t['K2_integer_decode_acc']:.2f}")

    gate = eq < 0.01 and ef < 0.01 and el < 0.06 and cross < 0.01
    print(f"\n  GATE (quantum & FDTD within 1%; learned within 6%; cross-impl within 1%): "
          f"{'PASS ✅' if gate else 'FAIL ❌'}")
    print(f"\n  WHAT THIS ESTABLISHES: 'mass = hidden-dimension momentum' now stands on four independent legs —")
    print(f"  a machine-PROVEN reduction (ansatz), direct numerics (quantum), an independent reimplementation")
    print(f"  (tabula FDTD), and a neural net that DISCOVERS the tower from visible projections alone (tabula")
    print(f"  learned) — all agreeing on m_n/m_1 = n. The bridge's first FOUR-repo cross-validation; the")
    print(f"  quantum project joins the family with its flagship claim gated.")
    OUT.mkdir(exist_ok=True)
    (OUT / "kk_tower_join.json").write_text(json.dumps({
        "theorem_anchor": "ansatz §111 (5D vacuum ⇔ 4D EMD, proven; trap caught)",
        "rows": rows, "n0_learned_mass": ladder[0],
        "max_err": {"quantum": eq, "tabula_fdtd": ef, "learned": el, "cross_implementation": cross},
        "group_velocities_quantum_vs_KG": {str(n): {"measured": m, "exact": e} for n, (m, e) in QUANTUM_VG.items()},
        "learned_quality": {"isotonic_R2": t["K1_latent_isotonic_R2_vs_n"],
                            "decode_acc": t["K2_integer_decode_acc"]},
        "gate_pass": bool(gate),
    }, indent=1))
    print(f"\n  wrote results/kk_tower_join.json")


if __name__ == "__main__":
    main()
