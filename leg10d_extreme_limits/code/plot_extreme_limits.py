#!/usr/bin/env python3
"""plot_extreme_limits.py

Loads sweep results from results/leg10d_extreme_results.json and generates a beautiful
four-panel plot showing the effects of extreme steering on attention gravity metrics
to test the "black hole collapse" hypotheses.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    json_path = Path("/Users/sumit/Github/TheBridge/results/leg10d_extreme_results.json")
    if not json_path.exists():
        raise FileNotFoundError(f"Sweep results not found at {json_path}")
        
    with open(json_path) as f:
        results = json.load(f)
        
    # Extract data in order of sorted alphas
    alphas_str = sorted(results.keys(), key=float)
    alphas = [float(a) for a in alphas_str]
    
    entropies = [results[a]["entropy"] for a in alphas_str]
    horizons = [results[a]["normalized_horizon"] for a in alphas_str]
    correlations = [results[a]["horizon_correlation"] for a in alphas_str]
    slopes = [results[a]["horizon_slope"] for a in alphas_str]
    lensing_ratios = [results[a]["lensing_ratio"] for a in alphas_str]

    # Plot styling
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Extreme Attention Steering & Space-Time Collapse in Qwen3-4B\n(Sweeping Layer 14 Virtue Vector into Singularity Limits)", 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Custom color palette (modern, vibrant HSL-derived colors)
    c_entropy = "#e63946"   # Deep Red (Singularity / Collapse)
    c_horizon = "#1d3557"   # Navy (Event Horizon)
    c_lensing = "#ff007f"   # Magenta (Lensing)
    c_slope = "#2a9d8f"     # Emerald Green
    c_corr = "#f4a261"      # Sandy Orange
    
    # Panel 1: Attention Entropy vs Alpha (H1 Collapse)
    axs[0, 0].plot(alphas, entropies, marker='o', color=c_entropy, linewidth=2.5, markersize=8)
    axs[0, 0].set_title("H1: Attention Entropy (Singularity Collapse)", fontsize=12, fontweight='bold')
    axs[0, 0].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[0, 0].set_ylabel("Average Attention Entropy (bits)", fontsize=10)
    axs[0, 0].grid(True, linestyle="--", alpha=0.6)
    
    # Panel 2: Normalized Event Horizon vs Alpha (H2 Expansion)
    axs[0, 1].plot(alphas, horizons, marker='s', color=c_horizon, linewidth=2.5, markersize=8)
    axs[0, 1].axhline(1.0, color='gray', linestyle=':', label="Full Seq Length")
    axs[0, 1].set_title("H2: Event Horizon Expansion (Gravitational Capture)", fontsize=12, fontweight='bold')
    axs[0, 1].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[0, 1].set_ylabel("Normalized Horizon Size (Rs / N)", fontsize=10)
    axs[0, 1].legend()
    axs[0, 1].grid(True, linestyle="--", alpha=0.6)
    
    # Panel 3: Horizon-Mass Correlation & Slope vs Alpha (H3 Breakdown)
    ax3_twin = axs[1, 0].twinx()
    p1 = axs[1, 0].plot(alphas, correlations, marker='D', color=c_corr, linewidth=2.5, markersize=8, label="Correlation (r)")
    p2 = ax3_twin.plot(alphas, slopes, marker='^', color=c_slope, linewidth=2.0, linestyle="--", markersize=8, label="Slope (G_eff)")
    axs[1, 0].set_title("H3: Space-Time Correlation Breakdown", fontsize=12, fontweight='bold')
    axs[1, 0].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[1, 0].set_ylabel("Pearson Correlation (r)", fontsize=10)
    ax3_twin.set_ylabel("Horizon-Mass Slope (G_eff)", fontsize=10)
    axs[1, 0].grid(True, linestyle="--", alpha=0.6)
    lines = p1 + p2
    labels = [l.get_label() for l in lines]
    axs[1, 0].legend(lines, labels, loc='lower left')
    
    # Panel 4: Lensing Magnification Ratio vs Alpha (H4 Collapse)
    axs[1, 1].plot(alphas, lensing_ratios, marker='x', color=c_lensing, linewidth=2.5, markersize=8, mew=2)
    axs[1, 1].axhline(1.0, color='gray', linestyle=':', label="No Lensing")
    axs[1, 1].set_title("H4: Lensing Magnification Collapse", fontsize=12, fontweight='bold')
    axs[1, 1].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[1, 1].set_ylabel("Lensing Magnification Ratio", fontsize=10)
    axs[1, 1].legend()
    axs[1, 1].grid(True, linestyle="--", alpha=0.6)
    
    plt.tight_layout()
    
    # Save the figure
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10d_extreme_comparison.png"
    plt.savefig(out_file, dpi=300)
    print(f"Saved figure to {out_file} 🎨")
    plt.close()

if __name__ == "__main__":
    main()
