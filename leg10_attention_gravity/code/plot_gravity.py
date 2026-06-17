#!/usr/bin/env python3
"""plot_gravity.py

Loads the attention extraction results and generates a three-panel plot:
1. Newtonian power-law decay of attention with distance.
2. Schwarzschild event horizon scaling against token mass.
3. Gravitational lensing shielding ratio across all layers.
"""

import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    results_path = Path("/Users/sumit/Github/TheBridge/results/leg10_attention.json")
    with open(results_path, "r") as f:
        data = json.load(f)
        
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # We choose a representative middle layer (e.g., Layer 14) for the scatter plots
    rep_layer = "14"
    layer_data = data[rep_layer]
    
    # 1. Panel 1: Distance Decay (H1) for Representative Layer
    ax0 = axes[0]
    r_vals = np.array(layer_data["r_sample"])
    a_vals = np.array(layer_data["a_sample"])
    
    # Average unique r values to show a clean trend
    unique_r = np.unique(r_vals)
    mean_a = []
    for r in unique_r:
        mean_a.append(np.mean(a_vals[r_vals == r]))
    unique_r = np.array(unique_r)
    mean_a = np.array(mean_a)
    
    ax0.scatter(unique_r, mean_a, color="navy", alpha=0.7, edgecolors="none", label="Mean Attention")
    
    # Fit line
    alpha = layer_data["alpha"]
    r2_fit = layer_data["r2_fit"]
    
    # Fit line on log-log: log(A) = C - alpha * log(r) => A = exp(C) * r^-alpha
    mask = mean_a > 0
    if np.sum(mask) >= 2:
        slope, intercept = np.polyfit(np.log(unique_r[mask]), np.log(mean_a[mask]), 1)
        fit_r = np.linspace(1, max(unique_r), 100)
        fit_a = np.exp(intercept) * (fit_r ** slope)
        ax0.plot(fit_r, fit_a, color="crimson", lw=2.0, 
                 label=f"Power Law Fit: $r^{{{slope:.2f}}}$\n$R^2 = {r2_fit:.2f}$")
        
    ax0.set_xscale("log")
    ax0.set_yscale("log")
    ax0.set_xlabel("Token Distance $r$")
    ax0.set_ylabel("Attention Weight $A(r)$")
    ax0.set_title(f"Attention Falloff vs. Distance (Layer {rep_layer})")
    ax0.legend()
    ax0.grid(True, which="both", alpha=0.2)
    
    # 2. Panel 2: Schwarzschild Horizon vs Mass (H2)
    ax1 = axes[1]
    mass_vals = np.array(layer_data["mass_sample"])
    hor_vals = np.array(layer_data["hor_sample"])
    
    # Add a bit of jitter to horizon values (since they are integers) to make scatter legible
    jittered_hor = hor_vals + np.random.normal(0, 0.15, size=len(hor_vals))
    
    ax1.scatter(mass_vals, jittered_hor, color="navy", alpha=0.5, edgecolors="none")
    
    # Fit line: Horizon = slope * Mass + intercept
    if len(mass_vals) >= 2:
        slope, intercept = np.polyfit(mass_vals, hor_vals, 1)
        fit_m = np.linspace(min(mass_vals), max(mass_vals), 100)
        fit_h = slope * fit_m + intercept
        corr_p = layer_data["corr_pearson"]
        ax1.plot(fit_m, fit_h, color="crimson", lw=2.0,
                 label=f"Linear Fit (slope={slope:.2f})\nCorr $r = {corr_p:.2f}$")
                 
    ax1.set_xlabel("Token Gravitational Mass $M_j$")
    ax1.set_ylabel("Event Horizon Radius $R_s$ (jittered)")
    ax1.set_title(f"Event Horizon $R_s$ vs. Mass $M$ (Layer {rep_layer})")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 3. Panel 3: Lensing Deflection across Layers (H3)
    ax2 = axes[2]
    layers = sorted([int(k) for k in data.keys()])
    ratios = [data[str(l)]["lensing_ratio"] for l in layers]
    
    ax2.plot(layers, ratios, "o-", color="navy", lw=2.0, label="Shielding Ratio")
    ax2.axhline(1.0, color="gray", ls="--", label="No Lensing")
    ax2.axhline(0.80, color="red", ls=":", label="H3 Success Gate (20% reduction)")
    
    ax2.set_xlabel("Model Layer Index")
    ax2.set_ylabel("Lensing Ratio: $A_{high} / A_{low}$")
    ax2.set_title("Gravitational Lensing Shielding Ratio")
    ax2.set_ylim(0.4, 1.2)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle("Leg 10: Attention as Gravity in Qwen3-4B", fontsize=14, y=0.98)
    fig.tight_layout()
    
    out_img = Path("/Users/sumit/Github/TheBridge/results/leg10_attention_gravity.png")
    fig.savefig(out_img, dpi=140)
    print(f"Saved figure to {out_img} ✅")

if __name__ == "__main__":
    main()
