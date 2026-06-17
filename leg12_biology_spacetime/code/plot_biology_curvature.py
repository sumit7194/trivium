#!/usr/bin/env python3
"""plot_biology_curvature.py

Loads leg12_biology_results.json and plots:
1. Mean edge FRC vs. Stress Scale (gamma) for Chaperone vs. Housekeeping control groups.
2. Network-wide FRC Variance vs. Stress Scale (gamma).
"""

import json
import shutil
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    res_path = Path("/Users/sumit/Github/TheBridge/results/leg12_biology_results.json")
    if not res_path.exists():
        print(f"Error: results file {res_path} not found. Run calculate_curvature.py first.")
        return
        
    with open(res_path, "r") as f:
        data = json.load(f)
        
    species = data["species"]
    gammas_data = data["gammas"]
    species_name = "Yeast" if species == 4932 else "Human"
    
    gammas = sorted([float(g) for g in gammas_data.keys()])
    chaperone_frc = [gammas_data[str(g)]["mean_chaperone_frc"] for g in gammas]
    control_frc = [gammas_data[str(g)]["mean_control_frc"] for g in gammas]
    var_frc = [gammas_data[str(g)]["var_all_frc"] for g in gammas]
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    
    # Panel 1: Curvature Warping (Local FRC)
    ax1.plot(gammas, chaperone_frc, color="#dc2626", linewidth=2.5, marker="o", label="Chaperone-Connected Edges")
    ax1.plot(gammas, control_frc, color="#475569", linewidth=2.5, marker="x", linestyle="--", label="Housekeeping-Only Edges")
    
    ax1.set_title(f"{species_name} PPI Local Edge Curvature Warping", fontsize=13, fontweight="bold", pad=15)
    ax1.set_xlabel("Stress Scale (Chaperone Upregulation γ)", fontsize=11, labelpad=10)
    ax1.set_ylabel("Mean Forman-Ricci Curvature (FRC)", fontsize=11, labelpad=10)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", frameon=True, facecolor="#f8fafc", edgecolor="none")
    
    # Panel 2: Network-wide Variance (Polarization)
    ax2.plot(gammas, var_frc, color="#8b5cf6", linewidth=2.5, marker="s", label="Total Curvature Variance")
    
    ax2.set_title("Network-wide Curvature Variance (Polarization)", fontsize=13, fontweight="bold", pad=15)
    ax2.set_xlabel("Stress Scale (Chaperone Upregulation γ)", fontsize=11, labelpad=10)
    ax2.set_ylabel("Curvature Variance (Var(FRC))", fontsize=11, labelpad=10)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="upper left", frameon=True, facecolor="#f8fafc", edgecolor="none")
    
    plt.tight_layout()
    
    # Save the figure
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_path = out_dir / "leg12_biology_curvature.png"
    plt.savefig(out_path, dpi=300)
    print(f"Generated plot and saved to {out_path}")
    
    # Copy to the brain artifacts directory
    brain_dir = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")
    brain_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_path, brain_dir / "leg12_biology_curvature.png")
    print(f"Copied plot to brain artifact directory at: {brain_dir / 'leg12_biology_curvature.png'}")

if __name__ == "__main__":
    main()
