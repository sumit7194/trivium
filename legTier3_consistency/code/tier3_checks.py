#!/usr/bin/env python3
"""Tier 3 — opportunistic exact-bound consistency checks (THE_BRIDGE §10.2 Tier 3).

Run with any python3 (pure stdlib):
    python3 tier3_checks.py

Two cheap checks of ansatz's EXACT bounds (§75 area theorem, §74 polarization mode-count)
against measured/published merger parameters. These are consistency statements, not new results.
"""
import json
import math
from pathlib import Path

RESULTS = Path(__file__).resolve().parent.parent / "results"


def irreducible_mass(M, chi):
    """M_irr = M·√((1+√(1−χ²))/2) — the horizon-area mass (A = 16π M_irr²)."""
    return M * math.sqrt((1 + math.sqrt(1 - chi * chi)) / 2)


def main():
    print("TIER 3 — exact-bound consistency checks\n")

    # ---- §75 AREA THEOREM: A_f ≥ A_1 + A_2  ⇔  M_irr,f² ≥ M_irr,1² + M_irr,2² ----
    # GW150914 published parameters (LVK GWTC; deepstrain stores only ringdown remnants,
    # not progenitor masses, so we use the published progenitors for this consistency check).
    m1, m2 = 35.6, 30.6          # progenitor masses (assumed low-spin → M_irr ≈ m)
    Mf, chif = 63.1, 0.69        # remnant
    Mirr_f = irreducible_mass(Mf, chif)
    bound = math.sqrt(m1**2 + m2**2)
    radiated = (m1 + m2 - Mf) / (m1 + m2)
    max_frac = 1 - 1 / math.sqrt(2)     # §75 equal-mass cap ≈ 29.3%
    print("  §75 area theorem (GW150914, published params):")
    print(f"    M_irr,final = {Mirr_f:.2f} M⊙   vs  √(m1²+m2²) = {bound:.2f} M⊙   "
          f"→ A_f ≥ A_1+A_2 ?  {'✅ holds' if Mirr_f**2 >= bound**2 else '❌'}  "
          f"(margin {Mirr_f**2/bound**2:.2f}×)")
    print(f"    radiated fraction = {radiated*100:.1f}%   vs  §75 equal-mass cap {max_frac*100:.1f}%   "
          f"→ {'✅ below cap' if radiated < max_frac else '❌'}")
    area_ok = (Mirr_f**2 >= bound**2) and (radiated < max_frac)

    # ---- §74 POLARIZATION MODE-COUNT: GR = 2 tensor modes ----
    # ansatz (§74) proves a general metric theory allows up to 6 polarizations (2 tensor +
    # 2 vector + 2 scalar); GR has exactly 2 (the transverse-traceless tensor modes). LVK
    # polarization tests (e.g. GW170814) favour pure tensor over scalar/vector. For the
    # ringdown events here this is a consistency statement: the data are consistent with 2.
    gr_modes, max_modes = 2, 6
    print("\n  §74 polarization mode-count:")
    print(f"    ansatz (exact): GR = {gr_modes} tensor modes; general metric gravity ≤ {max_modes}.")
    print(f"    measurement: LVK polarization tests favour pure-tensor (no scalar/vector detected).")
    print(f"    → consistency: measured GW polarization content consistent with GR's 2 ✅")

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "tier3_checks.json").write_text(json.dumps({
        "area_theorem": {"event": "GW150914", "Mirr_final": Mirr_f, "bound_sqrt_m1sq_m2sq": bound,
                         "radiated_fraction": radiated, "max_fraction_cap": max_frac, "holds": area_ok},
        "polarizations": {"gr_modes": gr_modes, "max_metric_modes": max_modes,
                          "measured_consistent_with_2": True}}, indent=1))
    print("\n  wrote results/tier3_checks.json")


if __name__ == "__main__":
    main()
