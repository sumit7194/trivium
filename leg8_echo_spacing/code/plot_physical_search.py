#!/usr/bin/env python3
"""plot_physical_search.py

Plots the physical spacing relation and the p-value significance sweep for the 
Damour-Solodukhin wormhole model on GW150914 post-merger data.
"""

import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    results_path = Path("/Users/sumit/Github/TheBridge/results/leg8_echo_spacing.json")
    with open(results_path, "r") as f:
        data = json.load(f)
        
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # Colors and styles
    styles = {
        "planckian_static": {"color": "navy", "ls": "--", "label": "Planckian Static"},
        "planckian_rotating": {"color": "navy", "ls": "-", "label": f"Planckian Rotating (a={data['spin']})"},
        "macroscopic_static": {"color": "crimson", "ls": "--", "label": "Macro Static"},
        "macroscopic_rotating": {"color": "crimson", "ls": "-", "label": f"Macro Rotating (a={data['spin']})"},
    }
    
    # 1. Left Panel: Spacing delta_t vs log10(lambda)
    ax0 = axes[0]
    
    # Planckian Static
    p_stat = data["planckian"]["static"]
    ax0.plot(np.log10(p_stat["lambdas"]), p_stat["spacings"], **styles["planckian_static"])
    
    # Planckian Rotating
    p_rot = data["planckian"]["rotating"]
    ax0.plot(np.log10(p_rot["lambdas"]), p_rot["spacings"], **styles["planckian_rotating"])
    
    # Macroscopic Static
    m_stat = data["macroscopic"]["static"]
    ax0.plot(np.log10(m_stat["lambdas"]), m_stat["spacings"], **styles["macroscopic_static"])
    
    # Macroscopic Rotating
    m_rot = data["macroscopic"]["rotating"]
    ax0.plot(np.log10(m_rot["lambdas"]), m_rot["spacings"], **styles["macroscopic_rotating"])
    
    # Literature prediction line
    ax0.axhline(0.2925, color="gray", ls=":", lw=1.2)
    ax0.text(-20.5, 0.30, "Literature spacing dt = 0.2925 s", fontsize=8, color="gray")
    
    ax0.set_xlabel(r"Wormhole deviation $\log_{10}(\lambda)$")
    ax0.set_ylabel("Echo spacing $\Delta t$ [s]")
    ax0.set_title("Physical Spacing vs Wormhole Parameter")
    ax0.legend(fontsize=8)
    ax0.grid(True, alpha=0.3)
    
    # 2. Right Panel: p-value vs log10(lambda)
    ax1 = axes[1]
    
    ax1.plot(np.log10(p_stat["lambdas"]), p_stat["p_values"], **styles["planckian_static"])
    ax1.plot(np.log10(p_rot["lambdas"]), p_rot["p_values"], **styles["planckian_rotating"])
    ax1.plot(np.log10(m_stat["lambdas"]), m_stat["p_values"], **styles["macroscopic_static"])
    ax1.plot(np.log10(m_rot["lambdas"]), m_rot["p_values"], **styles["macroscopic_rotating"])
    
    # Significance thresholds
    ax1.axhline(0.05, color="orange", ls="-.", lw=1.0, label="Significance p = 0.05")
    ax1.axhline(0.01, color="red", ls="-.", lw=1.0, label="Significance p = 0.01")
    
    # Shading the consistent region
    ax1.axhspan(0.05, 1.0, color="green", alpha=0.05, label="Consistent with noise (null)")
    
    ax1.set_xlabel(r"Wormhole deviation $\log_{10}(\lambda)$")
    ax1.set_ylabel("Empirical p-value")
    ax1.set_title("GW150914 On-Source Significance vs Noise Background")
    ax1.set_yscale("log")
    ax1.set_ylim(0.003, 1.1)
    ax1.legend(fontsize=8, loc="lower right")
    ax1.grid(True, which="both", alpha=0.2)
    
    # Title and layout
    fig.suptitle(f"Leg 8: Exact Physical Echo Search Constraints (GW150914)", fontsize=14, y=0.98)
    fig.tight_layout()
    
    out_img = Path("/Users/sumit/Github/TheBridge/results/leg8_echo_spacing.png")
    fig.savefig(out_img, dpi=140)
    print(f"Saved figure to {out_img} ✅")

if __name__ == "__main__":
    main()
