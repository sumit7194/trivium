#!/usr/bin/env python3
"""Leg 7 — Ringdown Intrinsic Dimension: plotting and knee analysis.

Analyzes the bottleneck R²(d) curves, checks preregistered hypotheses,
and generates the comparison plot.
"""

import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent.parent / "results"
DIMS = [0, 1, 2, 3, 4, 5]
TAU = 0.02  # 2% marginal gain threshold


def find_knee(white_r2):
    count = 0
    for d in range(1, len(DIMS)):
        r_prev = white_r2[str(d-1)][0]
        r_curr = white_r2[str(d)][0]
        gain = r_curr - r_prev
        if gain > TAU:
            count += 1
        else:
            break
    return count


def main():
    f = RESULTS / "leg7_count_bottleneck_rd.json"
    with open(f) as fh:
        report = json.load(fh)
        
    verdicts = {}
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    keys = ["locked", "free", "noise"]
    titles = {
        "locked": "Kerr Locked (Family 1)\nPredicted: 2",
        "free": "Kerr Free (Family 2)\nPredicted: 4",
        "noise": "LIGO Noise (Family 3)\nPredicted: 1"
    }
    colors = {
        "locked": "seagreen",
        "free": "navy",
        "noise": "crimson"
    }
    
    for idx, key in enumerate(keys):
        res = report[key]
        std_r2 = [res["std_R2"][str(d)][0] for d in DIMS]
        std_err = [res["std_R2"][str(d)][1] for d in DIMS]
        white_r2 = [res["white_R2"][str(d)][0] for d in DIMS]
        white_err = [res["white_R2"][str(d)][1] for d in DIMS]
        
        knee = find_knee(res["white_R2"])
        verdicts[key] = {
            "resolved_dimension": knee,
            "white_R2_profile": [float(r) for r in white_r2]
        }
        
        ax = axes[idx]
        ax.errorbar(DIMS, std_r2, yerr=std_err, fmt="o-", label="standardized", color="gray", alpha=0.5, capsize=3)
        ax.errorbar(DIMS, white_r2, yerr=white_err, fmt="s-", label="whitened", color=colors[key], capsize=3)
        ax.axvline(knee, color="orange", ls=":", label=f"knee d={knee}")
        ax.set_xlabel("bottleneck dimension d")
        ax.set_ylabel("held-out R²")
        ax.set_ylim(-0.05, 1.05)
        ax.legend(fontsize=8, loc="lower right")
        ax.set_title(titles[key])
        
    h1 = verdicts["locked"]["resolved_dimension"] == 2
    h2 = verdicts["free"]["resolved_dimension"] == 4
    h3 = verdicts["noise"]["resolved_dimension"] == 1
    
    summary = {
        "H1_locked_dim_is_2": bool(h1),
        "H2_free_dim_is_4": bool(h2),
        "H3_noise_dim_collapses_to_1": bool(h3),
        "all_hypotheses_passed": bool(h1 and h2 and h3),
        "verdicts": verdicts
    }
    
    print("\n--- Knee Dimension Counts ---")
    print(f"Family 1 (Locked): resolved={verdicts['locked']['resolved_dimension']} (expected 2) | Pass: {h1}")
    print(f"Family 2 (Free):   resolved={verdicts['free']['resolved_dimension']} (expected 4) | Pass: {h2}")
    print(f"Family 3 (Noise):  resolved={verdicts['noise']['resolved_dimension']} (expected 1) | Pass: {h3}")
    
    with open(RESULTS / "leg7_knee_summary.json", "w") as out_fh:
        json.dump(summary, out_fh, indent=2)
        
    fig.suptitle("Ringdown Waveform Intrinsic Dimension Sweeps\n(LIGO noise collapses the 2D physical parameter space to 1D)")
    fig.tight_layout()
    fig.savefig(RESULTS / "leg7_ringdown_curves.png", dpi=140)
    print(f"Saved results/leg7_ringdown_curves.png + leg7_knee_summary.json")


if __name__ == "__main__":
    main()
