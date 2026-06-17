#!/usr/bin/env python3
"""plot_steered_gravity.py

Loads sweep results from results/leg10b_steered_gravity.json and generates a beautiful
four-panel plot showing the effects of steering on attention gravity metrics.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    json_path = Path("/Users/sumit/Github/TheBridge/results/leg10b_steered_gravity.json")
    if not json_path.exists():
        raise FileNotFoundError(f"Sweep results not found at {json_path}")
        
    with open(json_path) as f:
        results = json.load(f)
        
    # Extract data in order of sorted alphas
    alphas_str = sorted(results.keys(), key=float)
    alphas = [float(a) for a in alphas_str]
    
    decay_exponents = [results[a]["decay_exponent"] for a in alphas_str]
    correlations = [results[a]["horizon_correlation"] for a in alphas_str]
    slopes = [results[a]["horizon_slope"] for a in alphas_str]
    lensing_ratios = [results[a]["lensing_ratio"] for a in alphas_str]
    epistemic_mass_ratios = [results[a]["epistemic_mass_ratio"] for a in alphas_str]

    # Plot styling
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Steered Attention as Gravity in Qwen3-4B\n(Triplets Intellectual Humility Vector at Layer 14)", 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Custom color palette (modern, vibrant HSL-derived colors)
    c_decay = "#8a2be2"    # Violet
    c_horizon = "#00ced1"  # Turquoise/Cyan
    c_lensing = "#ff007f"  # Magenta
    c_mass = "#ff8c00"     # Orange
    
    # Panel 1: Decay Exponent
    axs[0, 0].plot(alphas, decay_exponents, marker='o', color=c_decay, linewidth=2.5, markersize=8)
    axs[0, 0].set_title("H1: Attention Decay Exponent (α_decay)", fontsize=12, fontweight='bold')
    axs[0, 0].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[0, 0].set_ylabel("Fitted Decay Exponent", fontsize=10)
    axs[0, 0].set_xticks(alphas)
    axs[0, 0].grid(True, linestyle="--", alpha=0.6)
    
    # Panel 2: Horizon-Mass Correlation and Slope
    ax2 = axs[0, 1].twinx()
    p1 = axs[0, 1].plot(alphas, correlations, marker='s', color=c_horizon, linewidth=2.5, markersize=8, label="Correlation (r)")
    p2 = ax2.plot(alphas, slopes, marker='^', color="#228b22", linewidth=2.0, linestyle="--", markersize=8, label="Slope (G_eff)")
    axs[0, 1].set_title("H2: Schwarzschild Horizon Scaling", fontsize=12, fontweight='bold')
    axs[0, 1].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[0, 1].set_ylabel("Pearson Correlation (r)", fontsize=10)
    ax2.set_ylabel("Horizon-Mass Slope", fontsize=10)
    axs[0, 1].set_xticks(alphas)
    axs[0, 1].grid(True, linestyle="--", alpha=0.6)
    # Legend for dual axes
    lines = p1 + p2
    labels = [l.get_label() for l in lines]
    axs[0, 1].legend(lines, labels, loc='lower left')
    
    # Panel 3: Lensing Magnification Ratio
    axs[1, 0].plot(alphas, lensing_ratios, marker='D', color=c_lensing, linewidth=2.5, markersize=8)
    axs[1, 0].axhline(1.0, color='gray', linestyle=':', label="No Lensing")
    axs[1, 0].set_title("H3: Lensing Magnification Ratio (A_high / A_low)", fontsize=12, fontweight='bold')
    axs[1, 0].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[1, 0].set_ylabel("Magnification Ratio", fontsize=10)
    axs[1, 0].set_xticks(alphas)
    axs[1, 0].legend()
    axs[1, 0].grid(True, linestyle="--", alpha=0.6)
    
    # Panel 4: Epistemic-to-Control Mass Ratio
    axs[1, 1].plot(alphas, epistemic_mass_ratios, marker='x', color=c_mass, linewidth=2.5, markersize=8, mew=2)
    axs[1, 1].set_title("H4: Epistemic Token Mass Redirection", fontsize=12, fontweight='bold')
    axs[1, 1].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[1, 1].set_ylabel("M_epistemic / M_control", fontsize=10)
    axs[1, 1].set_xticks(alphas)
    axs[1, 1].grid(True, linestyle="--", alpha=0.6)
    
    plt.tight_layout()
    
    # Save the figure
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10b_steered_gravity.png"
    plt.savefig(out_file, dpi=300)
    print(f"Saved figure to {out_file} 🎨")
    plt.close()

if __name__ == "__main__":
    main()
