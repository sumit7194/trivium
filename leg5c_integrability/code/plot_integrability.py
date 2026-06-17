#!/usr/bin/env python3
"""Leg 5c — Plotting Integrability Fingerprints.

Reads results from results/leg5c_integrability_results.json and generates
a comparative visualization of R2(d) curves.
"""

import json
import shutil
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path(__file__).resolve().parent.parent.parent / "results"
BRAIN_DIR = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")

def main():
    json_path = RESULTS / "leg5c_integrability_results.json"
    if not json_path.exists():
        print(f"Error: {json_path} does not exist.")
        return
        
    with open(json_path, "r") as f:
        data = json.load(f)
        
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    
    colors = {"kerr": "#0d9488", "deformed": "crimson"}
    markers = {"kerr": "o", "deformed": "s"}
    labels = {
        "kerr": "Kerr Spacetime (Integrable, ε = 0.0)",
        "deformed": "Deformed Spacetime (Non-Integrable, ε = 0.1)"
    }
    
    dims = [0, 1, 2, 3, 4]
    
    for idx, space in enumerate(["std", "white"]):
        ax = axes[idx]
        space_name = "Standardized" if space == "std" else "Whitened"
        
        for name in ["kerr", "deformed"]:
            means = [data[name][f"{space}_R2"][str(d)][0] for d in dims]
            stds = [data[name][f"{space}_R2"][str(d)][1] for d in dims]
            
            ax.errorbar(dims, means, yerr=stds, fmt=f"{markers[name]}-",
                        label=labels[name], color=colors[name],
                        linewidth=2.5, capsize=4, elinewidth=1.5, ms=8)
                        
            # Highlight knee
            count = data[name]["count"]
            if count in dims:
                ax.plot([count], [means[count]], "o", color="gold", ms=14, markeredgecolor="black", markeredgewidth=1.5, zorder=5)
                
        # Draw threshold line for knee detection
        ax.set_xlabel("bottleneck dimension $d$", fontsize=11)
        ax.set_ylabel("autoencoder reconstruction $R^2$", fontsize=11)
        ax.set_xticks(dims)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=10, loc="lower right")
        ax.set_title(f"{space_name} Space $R^2(d)$", fontsize=12, fontweight="bold", pad=10)
        
    fig.suptitle("Neural Integrability Fingerprints (Leg 5c)\n(Hidden symmetry / Carter constant conservation restricts Kerr trajectories to a 2D torus)", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    
    plot_path = RESULTS / "leg5c_integrability_curves.png"
    fig.savefig(plot_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to {plot_path}")
    
    # Copy to brain artifact directory
    BRAIN_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(plot_path, BRAIN_DIR / "leg5c_integrability_curves.png")
    print(f"Copied plot to brain artifact directory at: {BRAIN_DIR / 'leg5c_integrability_curves.png'}")


if __name__ == "__main__":
    main()
