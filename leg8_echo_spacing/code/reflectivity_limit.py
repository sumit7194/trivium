#!/usr/bin/env python3
"""Leg 8 (A4) — reframe the amplitude exclusion as a REFLECTIVITY upper limit (tabula venv).

    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python reflectivity_limit.py

leg 8 v2 excluded echo first-pulse amplitude ≥ A90 (in whitened-noise-σ units). The standard echo-search
product is a *reflectivity* upper limit: the first echo carries a fraction R_eff ≈ (echo amplitude)/(main
ringdown amplitude) of the ringdown back out, so the amplitude exclusion bounds R_eff ≤ A90 / A_ringdown,
with A_ringdown ≈ the ringdown SNR (σ units). This converts leg 8's amplitude exclusion into the more
useful, model-independent reflectivity language. (Honest: a *direct* limit on the wormhole λ is weaker —
see the verdict — so this is the robust restatement, as leg 8 §3 anticipated.)
"""
import json
from pathlib import Path

LEG8 = Path("/Users/sumit/Github/TheBridge/leg8_echo_spacing/results")
OUT = LEG8
# GW150914 220-ringdown matched-filter SNR — LVK ringdown analyses give ~7-8 (deepstrain's overtone_snr ~7).
SNR_RINGDOWN = (7.0, 8.0)


def main():
    print("LEG 8 (A4) — amplitude exclusion → effective-reflectivity upper limit\n")
    d = json.loads((LEG8 / "resolve_exclusion.json").read_text())
    a90_lo, a90_hi = d["A90_in_band_range"]
    print(f"  leg 8 v2 first-echo amplitude exclusion (90%): A90 ∈ [{a90_lo:.2f}, {a90_hi:.2f}] σ "
          f"(whitened-noise units), over {d['n_lambda_in_band']} physical λ-spacings.")
    print(f"  GW150914 220-ringdown SNR (the amplitude scale): ≈ {SNR_RINGDOWN[0]:.0f}–{SNR_RINGDOWN[1]:.0f} σ "
          f"(LVK ringdown analyses).")

    # effective reflectivity R_eff = first-echo amplitude / ringdown amplitude
    r_lo = a90_lo / SNR_RINGDOWN[1]                          # tightest: smallest A90 / largest SNR
    r_hi = a90_hi / SNR_RINGDOWN[0]                          # loosest
    print(f"\n  → EFFECTIVE REFLECTIVITY upper limit (90%):  R_eff ≲ {r_lo:.2f}–{r_hi:.2f}")
    print(f"     i.e. an echo train returning ≳ {r_lo*100:.0f}–{r_hi*100:.0f}% of the ringdown at the searched")
    print(f"     spacings would have been seen and was not. A model-INDEPENDENT statement (the standard")
    print(f"     echo-search product), unlike a raw amplitude exclusion.")

    print(f"\n  VERDICT (honest, per leg 8 §3): the robust result is the reflectivity bound R_eff ≲ {r_hi:.2f}.")
    print(f"  Converting to a limit on the Damour–Solodukhin λ is *weaker and model-dependent*: the observed")
    print(f"  R_eff = R_wall·T² folds in the photon-ring barrier transmission T (<1), so the WALL reflectivity")
    print(f"  bound R_wall ≲ R_eff/T² is looser; and the DS λ→R_wall map is model-specific (λ mainly sets the")
    print(f"  echo SPACING, leg 8's Δt(λ), not the amplitude). So: a clean reflectivity limit; λ stays")
    print(f"  constrained chiefly through the spacing (non-)detection, as leg 8 already reported.")

    (OUT / "reflectivity_limit.json").write_text(json.dumps(
        {"A90_range": [a90_lo, a90_hi], "ringdown_snr": list(SNR_RINGDOWN),
         "R_eff_upper_limit_90pct": [r_lo, r_hi]}, indent=1))
    print(f"\n  wrote results/reflectivity_limit.json")


if __name__ == "__main__":
    main()
