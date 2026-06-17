#!/usr/bin/env python3
"""plot_lensing_collapse.py

Loads leg11_lensing_collapse.json and plots:
1. Lensing Magnification Curve vs. alpha (fine-grained)
2. Average Token-wise Generation Entropy vs. alpha
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import shutil
from pathlib import Path

def main():
    res_path = Path("/Users/sumit/Github/TheBridge/results/leg11_lensing_collapse.json")
    if not res_path.exists():
        print(f"Error: results file {res_path} not found. Run lensing_and_collapse.py first.")
        return
        
    with open(res_path, "r") as f:
        data = json.load(f)
        
    lensing_data = data["lensing_sweep"]
    gen_data = data["generation_sweep"]
    
    # 1. Parse Lensing Sweep
    lens_alphas = sorted([float(k) for k in lensing_data.keys()])
    lens_values = [lensing_data[str(a)] for a in lens_alphas]
    
    # 2. Parse Generation Sweep
    gen_alphas = sorted([float(k) for k in gen_data.keys()])
    gen_entropies = [gen_data[str(a)]["mean_generation_entropy"] for a in gen_alphas]
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    
    # Panel 1: Lensing Curve
    ax1.plot(lens_alphas, lens_values, color="#0d9488", linewidth=2.5, marker="o", markersize=6, label="Lensing Ratio")
    # Mark the peak lensing
    peak_idx = np.argmax(lens_values)
    peak_alpha = lens_alphas[peak_idx]
    peak_val = lens_values[peak_idx]
    ax1.annotate(f"Peak Lensing: {peak_val:.4f}\nat α={peak_alpha:.1f}", 
                 xy=(peak_alpha, peak_val), 
                 xytext=(peak_alpha - 10, peak_val - 0.8),
                 arrowprops=dict(facecolor="#1e293b", arrowstyle="->", connectionstyle="arc3,rad=-0.2"),
                 fontweight="bold", color="#1e293b", fontsize=10)
                 
    ax1.set_title("Lensing Magnification vs. Steering Scale (α)", fontsize=13, fontweight="bold", pad=15)
    ax1.set_xlabel("Steering Scale (α)", fontsize=11, labelpad=10)
    ax1.set_ylabel("Lensing Ratio (A_high / A_low)", fontsize=11, labelpad=10)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    
    # Panel 2: Coherence Collapse (Generation Entropy)
    ax2.plot(gen_alphas, gen_entropies, color="#6366f1", linewidth=2.5, marker="s", markersize=6, label="Generation Entropy")
    
    # Draw event horizon boundary line (threshold where qualitative collapse occurs)
    # Typically where entropy deviates drastically or stabilizes at a collapsed value
    ax2.axvline(x=25.0, color="#ef4444", linestyle=":", linewidth=2, label="Predicted Event Horizon (α = 25)")
    ax2.annotate("Semantic Event Horizon\n(Output Collapse)", 
                 xy=(25.0, np.mean(gen_entropies)), 
                 xytext=(27.0, np.mean(gen_entropies) + 0.5),
                 arrowprops=dict(facecolor="#ef4444", arrowstyle="->"),
                 fontweight="bold", color="#ef4444", fontsize=10)
                 
    ax2.set_title("Generation Token Entropy vs. Steering Scale (α)", fontsize=13, fontweight="bold", pad=15)
    ax2.set_xlabel("Steering Scale (α)", fontsize=11, labelpad=10)
    ax2.set_ylabel("Mean Token Entropy (bits)", fontsize=11, labelpad=10)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="lower right", frameon=True, facecolor="#f8fafc", edgecolor="none")
    
    plt.tight_layout()
    
    # Save the figure
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_path = out_dir / "leg11_lensing_collapse.png"
    plt.savefig(out_path, dpi=300)
    print(f"Generated plot and saved to {out_path}")
    
    # Copy to the brain artifacts directory
    brain_dir = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")
    brain_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_path, brain_dir / "leg11_lensing_collapse.png")
    print(f"Copied plot to brain artifact directory at: {brain_dir / 'leg11_lensing_collapse.png'}")

if __name__ == "__main__":
    main()
