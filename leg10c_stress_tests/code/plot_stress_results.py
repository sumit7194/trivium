#!/usr/bin/env python3
"""plot_stress_results.py

Loads stress test results from results/leg10c_stress_results.json and generates a beautiful
four-panel comparison figure to evaluate controls.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    json_path = Path("/Users/sumit/Github/TheBridge/results/leg10c_stress_results.json")
    if not json_path.exists():
        raise FileNotFoundError(f"Stress test results not found at {json_path}")
        
    with open(json_path) as f:
        results = json.load(f)
        
    alphas_str = sorted(results["humility_steering"].keys(), key=float)
    alphas = [float(a) for a in alphas_str]
    
    # Extract humility sweep data
    h_corr = [results["humility_steering"][a]["horizon_correlation"] for a in alphas_str]
    h_lens = [results["humility_steering"][a]["lensing_ratio"] for a in alphas_str]
    h_mass = [results["humility_steering"][a]["epistemic_mass_ratio"] for a in alphas_str]
    
    # Extract random vector steering data
    r_mass = [results["random_vector_steering"][a]["epistemic_mass_ratio"] for a in alphas_str]
    
    # Extract random model baseline data
    rand_model = results["random_model_baseline"]
    rand_corr = rand_model["horizon_correlation"]
    rand_lens = rand_model["lensing_ratio"]
    
    # Plot styling
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Leg 10c: Stress-Testing Attention Gravity in Qwen3-4B\n(Rigorous Control & Falsification Analysis)", 
                 fontsize=16, fontweight='bold', y=0.98)
                 
    # Modern HSL-derived colors
    c_trained = "#8a2be2"   # Violet
    c_random = "#a9a9a9"    # Dark Gray
    c_humility = "#ff007f"  # Magenta
    c_rand_vec = "#ff8c00"  # Orange
    c_variance = "#00ced1"  # Turquoise/Cyan
    
    # ─── Panel 1: Schwarzschild Correlation (Trained vs. Random Weights) ───
    axs[0, 0].bar(["Trained (Baseline)", "Random Weights (Untrained)"], 
                  [h_corr[alphas.index(0.0)], rand_corr], 
                  color=[c_trained, c_random], width=0.5, edgecolor='black', linewidth=1.2)
    axs[0, 0].set_title("T3 Control: Event Horizon Correlation (r)", fontsize=12, fontweight='bold')
    axs[0, 0].set_ylabel("Pearson Correlation Coefficient", fontsize=10)
    axs[0, 0].set_ylim(0, 1.0)
    axs[0, 0].grid(True, linestyle="--", alpha=0.6)
    
    # ─── Panel 2: Lensing Magnification (Trained vs. Random Weights) ───
    axs[0, 1].bar(["Trained (Baseline)", "Random Weights (Untrained)"], 
                  [h_lens[alphas.index(0.0)], rand_lens], 
                  color=[c_trained, c_random], width=0.5, edgecolor='black', linewidth=1.2)
    axs[0, 1].axhline(1.0, color='red', linestyle=':', label="No Lensing (1.0)")
    axs[0, 1].set_title("T3 Control: Lensing Magnification Ratio (A_high / A_low)", fontsize=12, fontweight='bold')
    axs[0, 1].set_ylabel("Lensing Ratio", fontsize=10)
    axs[0, 1].legend()
    axs[0, 1].grid(True, linestyle="--", alpha=0.6)
    
    # ─── Panel 3: Epistemic Mass Ratio (Humility vs. Random Vector) ───
    axs[1, 0].plot(alphas, h_mass, marker='o', color=c_humility, linewidth=2.5, label="Humility Vector Steering")
    axs[1, 0].plot(alphas, r_mass, marker='s', color=c_rand_vec, linewidth=2.0, linestyle="--", label="Random Vector Steering (Control)")
    axs[1, 0].set_title("T2 Control: Epistemic Token Mass Redirection", fontsize=12, fontweight='bold')
    axs[1, 0].set_xlabel("Steering Scale (α_steer)", fontsize=10)
    axs[1, 0].set_ylabel("M_epistemic / M_control", fontsize=10)
    axs[1, 0].set_xticks(alphas)
    axs[1, 0].legend()
    axs[1, 0].grid(True, linestyle="--", alpha=0.6)
    
    # ─── Panel 4: Causal Sanity Check (Upstream vs. Downstream Variance) ───
    # Compute variance of lensing ratio for each layer across all alphas
    raw_data = results["early_vs_late_raw"]
    layer_variances = []
    layers = list(range(36))
    for l in layers:
        l_vals = [raw_data[a][str(l)]["lensing_ratio"] for a in alphas_str]
        layer_variances.append(np.var(l_vals))
        
    axs[1, 1].plot(layers, layer_variances, color=c_variance, linewidth=2.5)
    axs[1, 1].axvline(14, color='red', linestyle='--', label="Steering Layer (14)")
    axs[1, 1].fill_between(layers, 0, layer_variances, where=[l <= 14 for l in layers], color='#ffcccb', alpha=0.5, label="Upstream (Control)")
    axs[1, 1].fill_between(layers, 0, layer_variances, where=[l > 14 for l in layers], color='#e0ffff', alpha=0.5, label="Downstream (Steered)")
    axs[1, 1].set_title("T4 Control: Lensing Ratio Variance Across Sweep", fontsize=12, fontweight='bold')
    axs[1, 1].set_xlabel("Transformer Layer", fontsize=10)
    axs[1, 1].set_ylabel("Metric Variance", fontsize=10)
    axs[1, 1].legend()
    axs[1, 1].grid(True, linestyle="--", alpha=0.6)
    
    plt.tight_layout()
    
    # Save the figure
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10c_stress_comparison.png"
    plt.savefig(out_file, dpi=300)
    print(f"Saved comparison figure to {out_file} 🎨")
    plt.close()

if __name__ == "__main__":
    main()
