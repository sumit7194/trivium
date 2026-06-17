#!/usr/bin/env python3
"""extract_attention.py

Loads Qwen3-4B, extracts layer-by-layer attention matrices on 50 sentences,
and calculates the physical metrics (distance falloff, horizon radius vs. mass,
and gravitational shielding deflection).
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.stats import pearsonr, spearmanr

# 50 diverse sentences for testing
SENTENCES = [
    "General relativity is a theory of gravitation developed by Albert Einstein.",
    "The Schwarzschild radius defines the event horizon of a non-rotating black hole.",
    "Light cannot escape from the strong gravitational field inside the horizon.",
    "Gravitational lensing occurs when a massive object bends the path of light.",
    "Quantum mechanics and general relativity are currently incompatible theories.",
    "A neutron star is the collapsed core of a massive supergiant star.",
    "The Big Bang theory describes the expansion and evolution of our universe.",
    "Dark matter and dark energy make up the majority of the cosmic energy density.",
    "A traversable wormhole requires exotic matter to keep its throat open.",
    "The equivalence principle states that gravitational and inertial mass are equal.",
    "Black holes evaporate slowly over time due to Hawking radiation.",
    "An orbit is the gravitationally curved trajectory of an object in space.",
    "Tidal forces stretch and squeeze bodies moving in a non-uniform field.",
    "The photon sphere is a spherical region where gravity is strong enough for light to orbit.",
    "Gravitational waves are ripples in the curvature of spacetime.",
    "We test general relativity using precise measurements of binary pulsars.",
    "A singularity is a point where the curvature of spacetime becomes infinite.",
    "The cosmological constant is associated with the energy density of empty space.",
    "Active galactic nuclei are powered by accretion onto supermassive black holes.",
    "Cosmic inflation describes a period of extremely rapid expansion in the early universe.",
    "The event horizon telescope captured the first direct image of a black hole shadow.",
    "Frame dragging is an effect where a rotating mass drags spacetime with it.",
    "Birkhoff's theorem states that any spherically symmetric vacuum solution is static.",
    "The Tolman-Oppenheimer-Volkoff equation limits the maximum mass of a neutron star.",
    "We search for primordial black holes as candidates for dark matter.",
    "Spacetime is modeled as a four-dimensional pseudo-Riemannian manifold.",
    "Geodesics represent the straightest possible paths in a curved geometry.",
    "The stress-energy tensor describes the density and flux of energy and momentum.",
    "Gauge theories describe physical forces using local symmetry transformations.",
    "No-arbitrage in financial markets is mathematically equivalent to a flat connection.",
    "Hierarchical structures in data are naturally represented in hyperbolic space.",
    "Neural network activations form complex manifolds in high-dimensional space.",
    "We probe latent representations to measure the legibility of features.",
    "Information bottleneck theory explains how networks compress irrelevant features.",
    "Roger Penrose proved the singularity theorems using topological methods.",
    "Stephen Hawking discovered that black holes have a finite thermodynamic temperature.",
    "The no-hair theorem states that stationary black holes depend only on three parameters.",
    "Quantum gravity aims to describe the quantum behavior of spacetime.",
    "The holographic principle suggests that a volume of space is encoded on its boundary.",
    "A de Sitter universe has a positive cosmological constant and expands exponentially.",
    "Anti-de Sitter space has a negative cosmological constant and is highly symmetric.",
    "The Oppenheimer-Snyder model describes the gravitational collapse of a dust cloud.",
    "We model the cosmic microwave background radiation to measure cosmological parameters.",
    "The Keck observatory measured the orbits of stars around the Sgr A* black hole.",
    "We use numerical relativity to simulate the merger of two black holes.",
    "A standard candle is an astronomical object with a known intrinsic luminosity.",
    "Redshift measures the expansion of light waves as they travel through space.",
    "The Friedmann equations describe the expansion of space in homogeneous universes.",
    "A cosmic string is a hypothetical 1-D topological defect in spacetime.",
    "The Weak Equivalence Principle is tested with high precision in space experiments."
]

def load_model():
    print("Loading Qwen3-4B...")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-4B", torch_dtype=torch.float16, device_map=None, attn_implementation="eager"
    )
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device)
    model.eval()
    print(f"Loaded successfully on {device}")
    return model, tokenizer, device

def main():
    model, tokenizer, device = load_model()
    
    num_layers = model.config.num_hidden_layers
    print(f"\nProcessing {len(SENTENCES)} sentences across {num_layers} layers...")
    
    # Structure to accumulate metrics per layer
    layer_results = {
        l: {
            "r_vals": [], "a_vals": [],          # for H1 distance decay
            "masses": [], "horizons": [],        # for H2 event horizon
            "lens_high": [], "lens_low": []       # for H3 deflection
        }
        for l in range(num_layers)
    }
    
    for s_idx, sent in enumerate(SENTENCES):
        inputs = tokenizer(sent, return_tensors="pt").to(device)
        seq_len = inputs["input_ids"].shape[1]
        if seq_len < 5:
            continue
            
        with torch.no_grad():
            outputs = model(**inputs, output_attentions=True)
            
        # outputs.attentions is a tuple of length num_layers
        # each element has shape (batch, heads, seq_len, seq_len)
        for l in range(num_layers):
            # Average over heads and select batch 0
            attn = outputs.attentions[l][0].mean(dim=0).cpu().numpy() # (seq_len, seq_len)
            
            # 1. Distance Decay (H1)
            # We calculate average attention at each distance r
            for r in range(1, seq_len):
                pairs = []
                for i in range(seq_len):
                    for j in range(seq_len):
                        if abs(i - j) == r:
                            pairs.append(attn[i, j])
                if pairs:
                    layer_results[l]["r_vals"].append(r)
                    layer_results[l]["a_vals"].append(float(np.mean(pairs)))
            
            # 2. Token Mass and Horizon (H2)
            # Mass: sum of attention received by token j
            mass = attn.sum(axis=0) # (seq_len,)
            # Horizon: max distance r where A(i, j) >= 0.05
            horizons = []
            for j in range(seq_len):
                h_rad = 0
                for i in range(seq_len):
                    if attn[i, j] >= 0.05:
                        h_rad = max(h_rad, abs(i - j))
                horizons.append(h_rad)
                layer_results[l]["masses"].append(float(mass[j]))
                layer_results[l]["horizons"].append(float(h_rad))
                
            # 3. Gravitational Lensing (H3)
            # For each adjacent triplet (i, j=i+1, k=i+2):
            # We check if the intermediate token j is high-mass vs. low-mass
            med_mass = np.median(mass)
            for i in range(seq_len - 2):
                j = i + 1
                k = i + 2
                if mass[j] > med_mass:
                    layer_results[l]["lens_high"].append(float(attn[k, i]))
                else:
                    layer_results[l]["lens_low"].append(float(attn[k, i]))
                            
        if (s_idx + 1) % 10 == 0:
            print(f"  Processed {s_idx + 1}/{len(SENTENCES)} sentences...")

    # Summarize results per layer
    summary = {}
    for l in range(num_layers):
        r_arr = np.array(layer_results[l]["r_vals"])
        a_arr = np.array(layer_results[l]["a_vals"])
        mass_arr = np.array(layer_results[l]["masses"])
        hor_arr = np.array(layer_results[l]["horizons"])
        lens_h = np.array(layer_results[l]["lens_high"])
        lens_l = np.array(layer_results[l]["lens_low"])
        
        # H1: Fit power law A(r) = C * r^-alpha
        # log(A) = log(C) - alpha * log(r)
        # Avoid zeros or negatives in average attention
        mask = a_arr > 0
        if np.sum(mask) >= 3:
            log_r = np.log(r_arr[mask])
            log_a = np.log(a_arr[mask])
            slope, intercept = np.polyfit(log_r, log_a, 1)
            alpha = float(-slope)
            # R2
            pred = intercept + slope * log_r
            r2 = float(1 - np.sum((log_a - pred)**2) / np.sum((log_a - log_a.mean())**2))
        else:
            alpha = 0.0
            r2 = 0.0
            
        # H2: Correlation between Mass and Horizon
        if len(mass_arr) >= 3 and np.std(hor_arr) > 0:
            corr_p, _ = pearsonr(mass_arr, hor_arr)
            corr_s, _ = spearmanr(mass_arr, hor_arr)
            corr_p = float(corr_p)
            corr_s = float(corr_s)
        else:
            corr_p = 0.0
            corr_s = 0.0
            
        # H3: Lensing ratio (high-mass intermediate vs. low-mass intermediate)
        mean_high = float(np.mean(lens_h)) if len(lens_h) > 0 else 0.0
        mean_low = float(np.mean(lens_l)) if len(lens_l) > 0 else 0.0
        lensing_ratio = mean_high / mean_low if mean_low > 0 else 1.0
        
        summary[l] = {
            "alpha": alpha,
            "r2_fit": r2,
            "corr_pearson": corr_p,
            "corr_spearman": corr_s,
            "mean_high_mass_lensing": mean_high,
            "mean_low_mass_lensing": mean_low,
            "lensing_ratio": lensing_ratio,
            "r_sample": r_arr.tolist()[:100],  # sample for plotting
            "a_sample": a_arr.tolist()[:100],
            "mass_sample": mass_arr.tolist()[:200],
            "hor_sample": hor_arr.tolist()[:200]
        }
        print(f"Layer {l:2d}: alpha={alpha:5.2f} (R2={r2:5.2f}), corr_pearson={corr_p:5.2f}, lensing_ratio={lensing_ratio:5.2f}")

    # Save summary
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10_attention.json"
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved extraction results to {out_file} ✅")

if __name__ == "__main__":
    main()
