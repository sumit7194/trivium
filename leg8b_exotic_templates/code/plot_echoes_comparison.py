#!/usr/bin/env python3
"""plot_echoes_comparison.py

Loads search results from results/leg8b_echo_results.json and the baseline
head-to-head results, and generates a comparative sensitivity plot showing
the performance reversal under physics-grounded templates.
"""

import json
import os
import shutil
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Path configurations
THE_BRIDGE_RESULTS = Path("/Users/sumit/Github/TheBridge/results")
BASELINE_RESULTS_PATH = Path("/Users/sumit/Github/BlackHole/echoes/results/10_head_to_head.json")
PHYSICS_RESULTS_PATH = THE_BRIDGE_RESULTS / "leg8b_echo_results.json"
BRAIN_DIR = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")

def main():
    if not PHYSICS_RESULTS_PATH.exists():
        print(f"Error: {PHYSICS_RESULTS_PATH} does not exist.")
        return
    if not BASELINE_RESULTS_PATH.exists():
        print(f"Error: {BASELINE_RESULTS_PATH} does not exist.")
        return
        
    with open(PHYSICS_RESULTS_PATH, "r") as f:
        phys_data = json.load(f)
    with open(BASELINE_RESULTS_PATH, "r") as f:
        base_data = json.load(f)
        
    amps = phys_data["recovery"]["amps"]
    
    # Extract baseline (phenomenological) efficiencies
    base_ml = [base_data["eff"]["ml"][str(a)] for a in amps]
    base_cb = [base_data["eff"]["comb"][str(a)] for a in amps]
    
    # Extract physics-grounded efficiencies
    phys_ml = phys_data["recovery"]["ml"]
    phys_cb = phys_data["recovery"]["comb"]
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    
    # Baseline (Phenomenological) curves
    ax.plot(amps, base_ml, "o-", color="#e11d48", label="ML Scorer: Toy Phenomenological", alpha=0.4, lw=1.5, ms=6)
    ax.plot(amps, base_cb, "s--", color="#475569", label="Comb Baseline: Toy Phenomenological", alpha=0.4, lw=1.5, ms=6)
    
    # Physics-Grounded curves
    ax.plot(amps, phys_ml, "o-", color="#be123c", label="ML Scorer: Physics-Grounded (Filtered)", lw=3, ms=8)
    ax.plot(amps, phys_cb, "s--", color="#0f172a", label="Comb Baseline: Physics-Grounded (Filtered)", lw=3, ms=8)
    
    # Threshold line
    ax.axhline(0.5, color="#94a3b8", ls=":", lw=1.2, label="50% Detection Threshold")
    
    # Formatting
    ax.set_xlabel("Injected Echo Amplitude [whitened-σ equivalent, raw-strain injection]", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Recovery Fraction (p < 0.05 vs background)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("GW150914: Sensitivity Degradation and Reversal (Leg 8b)\n"
                 "(Physics-grounded echoes are smoothed by barrier filtering, causing ML scorer to fail)", fontsize=12, fontweight="bold", pad=12)
    
    ax.set_xlim(0.3, 3.2)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(amps)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
    
    fig.tight_layout()
    
    # Save plot
    out_path = THE_BRIDGE_RESULTS / "leg8b_sensitivity_comparison.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved sensitivity comparison plot to {out_path} ✅")
    
    # Copy to brain artifact directory
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_path, BRAIN_DIR / "leg8b_sensitivity_comparison.png")
    print(f"Copied sensitivity comparison plot to brain directory ✅")

if __name__ == "__main__":
    main()
