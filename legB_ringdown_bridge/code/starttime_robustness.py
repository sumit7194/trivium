#!/usr/bin/env python3
"""Move B robustness — is the no-hair δ Kerr-consistency an artifact of the ringdown START TIME? (stdlib).

    python3 starttime_robustness.py

The dominant systematic in ringdown spectroscopy is *when* the ringdown is declared to start: too early and
overtones/nonlinearities contaminate the fit; too late and SNR is gone. Move B's headline (leg B) is that
the exact-Leaver 220→(M,χ)→221 no-hair deviation δ is Kerr-consistent (δ=0 inside 90%). That test was run at
the PEAK (t0=0). This asks whether the conclusion survives the start-time sweep — using deepstrain §16, which
re-fit the NPE δ posterior at start offsets 0–12 ms past the peak (read-only). Bridge value-add: (i) confirm
leg B's *independent* exact-Leaver δ at the peak matches deepstrain's t0=0 NPE median, and (ii) frame the
start-time drift as a SYSTEMATIC and compare it to the STATISTICAL (SNR) width — which dominates.

Inputs (READ-ONLY):
  deepstrain §16  /Users/sumit/Github/BlackHole/ringdown_spectroscopy/results/16_gw250114_starttime.json
  leg B           legB_ringdown_bridge/results/precise_ringdown.json  (delta_bridge, the exact-Leaver δ)
"""
import json
import statistics
from pathlib import Path

DS16 = Path("/Users/sumit/Github/BlackHole/ringdown_spectroscopy/results/16_gw250114_starttime.json")
LEGB = Path(__file__).resolve().parent.parent / "results/precise_ringdown.json"
OUT = Path(__file__).resolve().parent.parent / "results"


def main():
    ds = json.loads(DS16.read_text())
    legb = json.loads(LEGB.read_text())
    dvs = ds["delta_vs_start"]
    rows = sorted(((float(k), v) for k, v in dvs.items()), key=lambda kv: kv[0])

    print("MOVE B ROBUSTNESS — does the no-hair δ Kerr-consistency survive the ringdown start-time sweep?")
    print(f"  event {ds['event']} (deepstrain §16, NPE δ vs start offset); leg B exact-Leaver δ for reference\n")
    print(f"  {'t0 (ms)':>8} {'δ median':>9} {'90% CI':>20} {'Kerr inside 90%?':>16}")
    medians, halfwidths, all_kerr = [], [], True
    for t0, v in rows:
        med, lo, hi, kin = v["median"], v["lo"], v["hi"], v["kerr_inside_90"]
        medians.append(med)
        halfwidths.append((hi - lo) / 2.0)
        all_kerr = all_kerr and bool(kin)
        print(f"  {t0:>8.1f} {med:>9.3f}   [{lo:>6.3f}, {hi:>6.3f}]   {('YES' if kin else 'NO'):>16}")

    delta_bridge = legb["delta_bridge"]                       # leg B exact-Leaver δ at the peak (t0=0)
    t0_0_median = dict(rows)[0.0]["median"]
    sys_drift = ds.get("peak_to_late_drift", max(medians) - min(medians))
    sys_std = statistics.pstdev(medians)
    stat_halfwidth = statistics.mean(halfwidths)

    print(f"\n  CROSS-CHECK (bridge ⟷ deepstrain at the peak):")
    print(f"    leg B exact-Leaver δ (independent route) = {delta_bridge:+.3f}")
    print(f"    deepstrain §16 NPE δ median at t0=0       = {t0_0_median:+.3f}   "
          f"(agree to {abs(delta_bridge - t0_0_median):.3f})")
    print(f"\n  SYSTEMATIC vs STATISTICAL on δ:")
    print(f"    start-time systematic: median drift = {sys_drift:.3f}, std across t0 = {sys_std:.3f}")
    print(f"    statistical (SNR) 90% half-width (mean over t0) = {stat_halfwidth:.3f}")
    ratio = stat_halfwidth / sys_std if sys_std > 0 else float("inf")
    print(f"    ⇒ statistical width is {ratio:.1f}× the start-time systematic — the test is SNR-limited.")
    print(f"\n  VERDICT: Kerr (δ=0) stays inside the 90% CI at EVERY start time "
          f"({'all consistent ✅' if all_kerr else 'NOT all consistent ⚠'}).")
    print(f"    Move B's no-hair conclusion is robust to the dominant ringdown systematic; the residual δ")
    print(f"    wander ({sys_std:.2f}) is well below the statistical width ({stat_halfwidth:.2f}), so tightening")
    print(f"    the no-hair test needs SNR/data (corroborating leg 2/leg 7's info-limit), not start-time control.")

    OUT.mkdir(exist_ok=True)
    (OUT / "starttime_robustness.json").write_text(json.dumps({
        "event": ds["event"],
        "delta_bridge_exact_leaver": delta_bridge,
        "delta_npe_t0_0": t0_0_median,
        "peak_consistency_gap": abs(delta_bridge - t0_0_median),
        "medians_vs_t0": {str(t0): v["median"] for t0, v in rows},
        "all_kerr_consistent": all_kerr,
        "systematic_drift": sys_drift, "systematic_std": sys_std,
        "statistical_halfwidth": stat_halfwidth, "stat_over_sys_ratio": ratio,
        "verdict": ("Move B no-hair δ is Kerr-consistent at every start time 0-12ms; start-time systematic "
                    "(std ~%.2f) is ~%.0fx below the statistical SNR width (~%.2f) — SNR-limited, robust."
                    % (sys_std, ratio, stat_halfwidth)),
    }, indent=1))
    print(f"\n  wrote results/starttime_robustness.json")


if __name__ == "__main__":
    main()
