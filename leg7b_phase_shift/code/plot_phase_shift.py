#!/usr/bin/env script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
#   "numpy",
# ]
# ///
import json
import shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent.parent / "results"
DIMS = [0, 1, 2, 3, 4, 5]
TAU = 0.03  # 3% marginal gain threshold

def find_knee(white_r2, threshold=TAU):
    count = 0
    for d in range(1, len(DIMS)):
        r_prev = white_r2[str(d-1)][0]
        r_curr = white_r2[str(d)][0]
        gain = r_curr - r_prev
        if gain > threshold:
            count += 1
        else:
            break
    return count

def main():
    f = RESULTS / "leg7b_phase_shift_results.json"
    with open(f) as fh:
        report = json.load(fh)
        
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    
    families = ["locked", "free"]
    keys = ["baseline", "fft_magnitude", "hilbert_envelope"]
    
    colors = {
        "baseline": "crimson",
        "fft_magnitude": "#0d9488",  # Teal
        "hilbert_envelope": "#6366f1"  # Indigo
    }
    
    titles = {
        "baseline": "Baseline (Time-Domain)",
        "fft_magnitude": "FFT Magnitude",
        "hilbert_envelope": "Hilbert Envelope"
    }
    
    print("\n--- Knee Dimension Counts (Leg 7b) ---")
    
    for row_idx, family in enumerate(families):
        family_label = "Locked Kerr (2D M, chi)" if family == "locked" else "Free Kerr (4D M, chi, amp_ratio, phase_diff)"
        print(f"\nFamily: {family.upper()}")
        
        for col_idx, key in enumerate(keys):
            res = report[family][key]
            std_r2 = [res["std_R2"][str(d)][0] for d in DIMS]
            std_err = [res["std_R2"][str(d)][1] for d in DIMS]
            white_r2 = [res["white_R2"][str(d)][0] for d in DIMS]
            white_err = [res["white_R2"][str(d)][1] for d in DIMS]
            
            # Find knees for both std and white at 3% threshold
            knee_std = find_knee(res["std_R2"], threshold=0.03)
            knee_white = find_knee(res["white_R2"], threshold=0.03)
            
            # Let's also compute under 2% threshold to compare
            knee_std_2 = find_knee(res["std_R2"], threshold=0.02)
            knee_white_2 = find_knee(res["white_R2"], threshold=0.02)
            
            print(f"  {key:18s} | std knee (3%/2%) = {knee_std}/{knee_std_2} | white knee (3%/2%) = {knee_white}/{knee_white_2}")
            
            ax = axes[row_idx, col_idx]
            
            # Plot curves
            ax.errorbar(DIMS, std_r2, yerr=std_err, fmt="o-", label="standardized", color="gray", alpha=0.4, capsize=3)
            ax.errorbar(DIMS, white_r2, yerr=white_err, fmt="s-", label="whitened", color=colors[key], capsize=3, linewidth=2.5)
            
            # Draw vertical line for whitened knee at 3%
            ax.axvline(knee_white, color="orange", ls=":", linewidth=2, label=f"knee d={knee_white} (white)")
            # If standard knee is different, draw it too
            if knee_std != knee_white:
                ax.axvline(knee_std, color="forestgreen", ls="--", linewidth=1.5, label=f"knee d={knee_std} (std)")
                
            ax.set_xlabel("bottleneck dimension d", fontsize=10)
            ax.set_ylabel("held-out R²", fontsize=10)
            ax.set_ylim(-0.05, 1.05)
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.legend(fontsize=8, loc="lower right")
            
            ax.set_title(f"{titles[key]}\n{family_label}", fontsize=11, fontweight="bold", pad=10)
            
    fig.suptitle("Resolving Phase-Shift Manifold Curvature in Ringdown Parameter Counting (Leg 7b)\n(Global phase/time shifts inflate time-domain manifolds; FFT magnitude recovers physical parameters)", fontsize=14, fontweight="bold", y=0.99)
    fig.tight_layout()
    
    out_path = RESULTS / "leg7b_phase_shift.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"\nSaved plot to {out_path}")
    
    # Copy to brain artifacts
    brain_dir = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")
    brain_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_path, brain_dir / "leg7b_phase_shift.png")
    print(f"Copied plot to brain artifact directory at: {brain_dir / 'leg7b_phase_shift.png'}")

if __name__ == "__main__":
    main()
