#!/usr/bin/env python3
"""plot_penrose.py

Generates the decodability curves and draws the Information-Theoretic Penrose 
Diagram of the neural network's causal structure.
"""

import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    results_path = Path("/Users/sumit/Github/TheBridge/results/leg9_horizon.json")
    with open(results_path, "r") as f:
        data = json.load(f)
        
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Left Panel: Decodability R^2 vs Layer Index
    ax0 = axes[0]
    layers = np.arange(7)
    
    # Target y
    ax0.plot(layers, data["y"]["linear"], "o--", color="navy", label="y (Target) - Linear")
    ax0.plot(layers, data["y"]["knn"], "s-", color="navy", label="y (Target) - kNN")
    
    # Invariant z_inv
    ax0.plot(layers, data["z_inv"]["linear"], "o--", color="crimson", label="z_inv (Nontarget) - Linear")
    ax0.plot(layers, data["z_inv"]["knn"], "s-", color="crimson", label="z_inv (Nontarget) - kNN")
    
    # Shortcut z_noise
    ax0.plot(layers, data["z_noise"]["linear"], "o--", color="forestgreen", label="z_noise (Shortcut) - Linear")
    ax0.plot(layers, data["z_noise"]["knn"], "s-", color="forestgreen", label="z_noise (Shortcut) - kNN")
    
    # Horizon threshold
    ax0.axhline(0.05, color="gray", ls=":", label="Horizon Threshold (R^2 = 0.05)")
    
    ax0.set_xlabel("Layer Index (Flow of Time)")
    ax0.set_ylabel("Decodability $R^2$")
    ax0.set_title("Information Decay across Network Layers")
    ax0.set_ylim(-0.2, 1.05)
    ax0.legend(fontsize=8, loc="lower left")
    ax0.grid(True, alpha=0.3)
    
    # 2. Right Panel: Information-Theoretic Penrose Diagram
    ax1 = axes[1]
    
    # Define Penrose grid
    # We map features along the x-axis: Target y = 0, z_inv = 1, z_noise = 2
    # Layer is the y-axis (0 to 6)
    
    # Shading the trapped regions (interior of black holes)
    # z_noise is trapped from layer 0
    ax1.axvspan(1.5, 2.5, ymin=0.0, ymax=1.0, color="gray", alpha=0.3, label="Trapped Region (Black Hole)")
    # z_inv is trapped from layer 2
    ax1.axvspan(0.5, 1.5, ymin=2/6, ymax=1.0, color="gray", alpha=0.3)
    
    # Draw Event Horizon Boundaries
    ax1.hlines(2, 0.5, 1.5, colors="red", linestyles="--", lw=2, label="Event Horizon")
    ax1.hlines(0, 1.5, 2.5, colors="red", linestyles="--", lw=2)
    
    # Draw Singularities (top boundary of trapped regions)
    ax1.hlines(6, 0.5, 2.5, colors="black", linestyles="-", lw=3.5, label="Information Singularity")
    
    # Draw Flow Arrows (Light Cones)
    # y escapes to future null infinity
    ax1.annotate("", xy=(0.0, 6.0), xytext=(0.0, 0.0),
                arrowprops=dict(arrowstyle="->", color="navy", lw=2.5, ls="-"))
    ax1.text(-0.25, 3.0, "Escaping Information", rotation=90, color="navy", fontweight="bold", fontsize=9)
    
    # z_inv flows up but gets trapped at layer 2
    ax1.annotate("", xy=(1.0, 2.0), xytext=(1.0, 0.0),
                arrowprops=dict(arrowstyle="->", color="crimson", lw=2.5, ls="-"))
    ax1.annotate("", xy=(1.0, 6.0), xytext=(1.0, 2.0),
                arrowprops=dict(arrowstyle="->", color="darkred", lw=2.0, ls=":"))
    ax1.text(0.75, 0.8, "Enters Horizon", rotation=90, color="crimson", fontweight="bold", fontsize=9)
    
    # z_noise is trapped immediately
    ax1.annotate("", xy=(2.0, 6.0), xytext=(2.0, 0.0),
                arrowprops=dict(arrowstyle="->", color="darkgreen", lw=2.0, ls=":"))
    ax1.text(1.75, 0.8, "Trapped at Input", rotation=90, color="forestgreen", fontweight="bold", fontsize=9)
    
    # Coordinate Labels
    ax1.text(0.0, 6.2, r"$\mathscr{I}^+$ (Future Null Infinity)", color="navy", ha="center", fontsize=9)
    ax1.text(1.5, 6.2, "Singularity (Information Lost)", color="black", ha="center", fontsize=9)
    
    # Axes settings
    ax1.set_xlim(-0.5, 2.5)
    ax1.set_ylim(-0.5, 6.5)
    ax1.set_xticks([0, 1, 2])
    ax1.set_xticklabels(["y (Target)", "z_inv (Invariant)", "z_noise (Shortcut)"])
    ax1.set_ylabel("Layer Index (Causal Time)")
    ax1.set_title("Information-Theoretic Penrose Causal Diagram")
    ax1.legend(fontsize=8, loc="upper right")
    ax1.grid(True, alpha=0.1)
    
    # Title and layout
    fig.suptitle("Leg 9: Causal Structure of Neural Representation Space", fontsize=14, y=0.98)
    fig.tight_layout()
    
    out_img = Path("/Users/sumit/Github/TheBridge/results/leg9_penrose.png")
    fig.savefig(out_img, dpi=140)
    print(f"Saved figure to {out_img} ✅")

if __name__ == "__main__":
    main()
