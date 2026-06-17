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

def find_knee(white_r2):
    count = 0
    for d in range(1, len(DIMS)):
        r_prev = white_r2[str(d-1)][0]
        r_curr = white_r2[str(d)][0]
        gain = r_curr - r_prev
        if gain > TAU:
            count += 1
        else:
            break
    return count

def main():
    f = RESULTS / "leg7b_phase_shift_results.json"
    with open(f) as fh:
        report = json.load(fh)
        
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    
    keys = ["baseline", "fft_magnitude", "hilbert_envelope"]
    titles = {
        "baseline": "Baseline (Time-Domain)\nPredicted Knee: 4 (Curved Manifold)",
        "fft_magnitude": "FFT Magnitude\nPredicted Knee: 2 (Decoupled Phase)",
        "hilbert_envelope": "Hilbert Envelope\nPredicted Knee: <=2 (Decayed Envelope)"
    }
    colors = {
        "baseline": "crimson",
        "fft_magnitude": "#0d9488",  # Teal
        "hilbert_envelope": "#6366f1"  # Indigo
    }
    
    summary = {}
    
    for idx, key in enumerate(keys):
        res = report[key]
        std_r2 = [res["std_R2"][str(d)][0] for d in DIMS]
        std_err = [res["std_R2"][str(d)][1] for d in DIMS]
        white_r2 = [res["white_R2"][str(d)][0] for d in DIMS]
        white_err = [res["white_R2"][str(d)][1] for d in DIMS]
        
        knee = find_knee(res["white_R2"])
        summary[key] = knee
        
        ax = axes[idx]
        ax.errorbar(DIMS, std_r2, yerr=std_err, fmt="o-", label="standardized", color="gray", alpha=0.5, capsize=3)
        ax.errorbar(DIMS, white_r2, yerr=white_err, fmt="s-", label="whitened", color=colors[key], capsize=3, linewidth=2.5)
        ax.axvline(knee, color="orange", ls=":", linewidth=2, label=f"knee d={knee}")
        ax.set_xlabel("bottleneck dimension d", fontsize=11)
        ax.set_ylabel("held-out R²", fontsize=11)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=9, loc="lower right")
        ax.set_title(titles[key], fontsize=12, fontweight="bold", pad=10)
        
    print("\n--- Knee Dimension Counts ---")
    for key, val in summary.items():
        print(f"Representation: {key:18s} | resolved count = {val}")
        
    fig.suptitle("Resolving Phase-Shift Manifold Curvature in Ringdown Parameter Counting (Leg 7b)\n(Fourier magnitude and Hilbert envelope recover the true 2-parameter physical dimensionality)", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    
    out_path = RESULTS / "leg7b_phase_shift.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to {out_path}")
    
    # Copy to brain artifacts
    brain_dir = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")
    brain_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_path, brain_dir / "leg7b_phase_shift.png")
    print(f"Copied plot to brain artifact directory at: {brain_dir / 'leg7b_phase_shift.png'}")

if __name__ == "__main__":
    main()
