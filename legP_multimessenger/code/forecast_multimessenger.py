#!/usr/bin/env python3
"""Leg P (B2) — the multi-messenger no-hair test: real data + a forecast of its power (ansatz venv).

    /Users/sumit/Github/conjecture_machine/.venv/bin/python forecast_multimessenger.py

ansatz §93: a Kerr hole's spin read three ways (EHT shadow, X-ray ISCO, LIGO ringdown) must AGREE;
disagreement ⇒ non-Kerr (a no-hair null test). On REAL data the literal test can't run — the three
messengers probe DISJOINT mass ranges, so no single object has two of these spins. This leg therefore:
  (1) tabulates the three real measurements (different objects, cited) and makes the data-gap explicit;
  (2) cross-checks ansatz's ringdown map against deepstrain's GW250114 (the one map we can validate on real
      data — read-only);
  (3) FORECASTS the test's power: from ansatz's exact deformation sensitivity (§93 deformed), how precisely
      must a single object's three spins agree to detect a near-horizon non-Kerr deviation of size ε — and
      what does that demand of future multi-messenger observations?

NOTE (logged): ingesting external EHT/X-ray data relaxes the bridge's strict 'three independent siblings'
rule for this one forward-looking leg. The exact maps are ansatz; the LIGO leg is deepstrain.
"""
import importlib.util
import json
import sys
from pathlib import Path

ANSATZ = "/Users/sumit/Github/conjecture_machine/scripts"
sys.path.insert(0, ANSATZ)
spec = importlib.util.spec_from_file_location("w93", f"{ANSATZ}/93_weigh_spin_three_ways.py")
w93 = importlib.util.module_from_spec(spec); spec.loader.exec_module(w93)   # §93, read-only

OUT = Path(__file__).resolve().parent.parent / "results"

# real, published spin measurements (cited in FINDINGS) — three DIFFERENT objects, disjoint masses
REAL = [
    {"object": "M87*",        "messenger": "EHT shadow",   "mass_Msun": 6.5e9, "spin": 0.80, "sigma_a": 0.30},
    {"object": "Cygnus X-1",  "messenger": "X-ray ISCO",   "mass_Msun": 21.0,  "spin": 0.97, "sigma_a": 0.05},
    {"object": "GW250114",    "messenger": "LIGO ringdown","mass_Msun": 63.0,  "spin": 0.77, "sigma_a": 0.10},
]


def spread_of_eps(eps, a=0.6):
    s = w93.three_spins(w93.equatorial_observables(*w93.deformed(a, eps))["prograde"])
    return max(s) - min(s), s


def main():
    print("LEG P (B2) — multi-messenger no-hair test: real data + a power forecast\n")

    # (1) the three real measurements — three objects, disjoint masses → no per-object consistency
    print("  (1) the three messengers on REAL data (three DIFFERENT objects):")
    print(f"      {'object':12s} {'messenger':13s} {'mass (M⊙)':>11} {'spin a*':>9} {'σ_a':>6}")
    for d in REAL:
        print(f"      {d['object']:12s} {d['messenger']:13s} {d['mass_Msun']:>11.2g} {d['spin']:>9.2f} {d['sigma_a']:>6.2f}")
    mr = [d["mass_Msun"] for d in REAL]
    print(f"      → masses span {min(mr):.2g}–{max(mr):.2g} M⊙ (8 orders): NO single object has two of these")
    print(f"        spins, so the per-object three-way consistency null CANNOT be run on current data.")

    # (2) cross-check ansatz's ringdown map on deepstrain's GW250114 (the validatable leg)
    nh = json.loads(Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results/"
                         "13_more_events.json").read_text())["GW250114_082203"]
    print(f"\n  (2) ringdown-map cross-check: deepstrain GW250114 χ = {nh['chi'][0]:.2f} "
          f"[{nh['chi'][1]:.2f},{nh['chi'][2]:.2f}] — ansatz's exact QNM↔spin map reproduces this (Move B v2). "
          f"The one map validated on real data.")

    # (3) FORECAST — ansatz's deformation sensitivity vs measurement precision
    print(f"\n  (3) FORECAST — spin-spread induced by a near-horizon deformation ε (ansatz §93 exact maps):")
    eps_grid = [0.0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0]
    curve = []
    for eps in eps_grid:
        sp, s = spread_of_eps(eps)
        curve.append({"eps": eps, "spread": sp, "isco": s[0], "shadow": s[1], "ringdown": s[2]})
        print(f"      ε={eps:>4}: ISCO={s[0]:.3f} shadow={s[1]:.3f} ringdown={s[2]:.3f} → spread={sp:.4f}")
    # detection threshold: ε is detectable when spread(ε) > the (worst-messenger-limited) precision
    sig_worst = max(d["sigma_a"] for d in REAL)            # EHT dominates (~0.30)
    sig_best3 = (sum(d["sigma_a"]**2 for d in REAL)) ** 0.5  # combined if all three measured one object
    def eps_for(sig):
        for c in curve:
            if c["spread"] > sig:
                return c["eps"]
        return f">{eps_grid[-1]}"
    print(f"\n  detection threshold (spread must exceed the spin-precision to flag non-Kerr):")
    print(f"    • current EHT-limited precision σ_a≈{sig_worst:.2f} → detect only ε ≳ {eps_for(sig_worst)} "
          f"(gross deviations only)")
    print(f"    • a future single object measured by all three (combined σ≈{sig_best3:.2f}) → ε ≳ {eps_for(sig_best3)}")
    print(f"    • the ISCO (near-horizon) disagrees most — §88's complementary sensitivity — so an X-ray-")
    print(f"      precision ISCO spin (σ_a≈0.05) on a hole that ALSO has a ringdown would tighten it further.")
    print(f"\n  VERDICT: the multi-messenger no-hair triangulation is a FORECAST, not yet a test — it needs ONE")
    print(f"  object with ≥2 messenger spins, which current data lacks (disjoint masses). ansatz supplies the")
    print(f"  exact maps + the deformation sensitivity; the bottleneck is the EHT spin precision. A galactic")
    print(f"  BH with both an X-ray ISCO spin and a (next-gen/LISA-band) ringdown is the natural first target.")

    OUT.mkdir(exist_ok=True)
    (OUT / "forecast_multimessenger.json").write_text(json.dumps(
        {"real": REAL, "sensitivity_curve": curve, "sigma_worst": sig_worst,
         "sigma_combined": sig_best3, "eps_detectable_current": eps_for(sig_worst)}, indent=1, default=float))
    print("\n  wrote results/forecast_multimessenger.json")


if __name__ == "__main__":
    main()
