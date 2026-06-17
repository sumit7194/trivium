#!/usr/bin/env python3
"""extreme_limits.py

Loads Qwen3-4B, steers at Layer 14 with extreme scales up to +/- 50.0, and computes
attention entropy, event horizon expansion, horizon-mass correlation, and lensing ratios
to test for the "black hole collapse" phenomenon.
"""

import os
import sys
import json
import re
import numpy as np
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.stats import pearsonr

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

class AdditiveSteeringHook:
    def __init__(self, layer_idx, virtue_vector, alpha):
        self.layer_idx = layer_idx
        self.alpha = alpha
        v = torch.tensor(virtue_vector, dtype=torch.float32)
        self.v_normalized = (v / (v.norm() + 1e-10)).unsqueeze(0).unsqueeze(0)
        self.handle = None

    def hook_fn(self, module, input, output):
        hidden = output[0] if isinstance(output, tuple) else output
        device = hidden.device
        v = self.v_normalized.to(device).to(hidden.dtype)
        hidden = hidden + self.alpha * v
        if isinstance(output, tuple):
            return (hidden,) + output[1:]
        return hidden

    def attach(self, model):
        layer = model.model.layers[self.layer_idx]
        self.handle = layer.register_forward_hook(self.hook_fn)

    def detach(self):
        if self.handle:
            self.handle.remove()
            self.handle = None

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-4B", torch_dtype=torch.float16, device_map=None, attn_implementation="eager"
    ).to(device)
    model.eval()
    
    # Load virtue vector
    vector_path = Path("/Users/sumit/Github/Phronesis/mvp/results/vectors/qwen3-4b/triplets-intellectual-humility/last_token/layer_14_virtue_vector.npy")
    virtue_vector = np.load(vector_path)
    
    steer_layer = 14
    steered_layers = list(range(15, 36))
    
    alphas = [-50.0, -20.0, -10.0, -5.0, 0.0, 5.0, 10.0, 20.0, 50.0]
    extreme_results = {}
    
    for alpha in alphas:
        print(f"\nRunning sweep with extreme alpha = {alpha:.1f}...")
        hook = AdditiveSteeringHook(steer_layer, virtue_vector, alpha) if alpha != 0.0 else None
        if hook:
            hook.attach(model)
            
        alpha_entropies = []
        alpha_horizons = []
        alpha_correlations = []
        alpha_slopes = []
        alpha_lensing_ratios = []
        
        for s_idx, sent in enumerate(SENTENCES):
            inputs = tokenizer(sent, return_tensors="pt").to(device)
            input_ids_list = inputs["input_ids"][0].tolist()
            seq_len = len(input_ids_list)
            if seq_len < 5:
                continue
                
            with torch.no_grad():
                outputs = model(**inputs, output_attentions=True)
                
            dist_matrix = np.abs(np.arange(seq_len)[:, None] - np.arange(seq_len))
            idx_i = np.arange(seq_len - 2)
            idx_j = idx_i + 1
            idx_k = idx_i + 2
            
            for l in steered_layers:
                attn = outputs.attentions[l][0].mean(dim=0).cpu().numpy()
                
                # 1. Entropy
                attn_f32 = attn.astype(np.float32)
                entropy = -np.sum(attn_f32 * np.log2(attn_f32 + 1e-10), axis=-1)
                alpha_entropies.append(float(np.mean(entropy)))
                
                # 2. Event Horizon Size
                mass = attn.sum(axis=0)
                mask_threshold = attn >= 0.05
                horizons = np.max(dist_matrix * mask_threshold, axis=0)
                # Normalize horizon by sequence length
                alpha_horizons.append(float(np.mean(horizons) / seq_len))
                
                # 3. Horizon-Mass Correlation
                mass_arr = np.array(mass)
                hor_arr = np.array(horizons)
                if len(mass_arr) >= 3 and np.std(hor_arr) > 0 and np.std(mass_arr) > 0:
                    corr, _ = pearsonr(mass_arr, hor_arr)
                    slope, _ = np.polyfit(mass_arr, hor_arr, 1)
                    alpha_correlations.append(float(corr))
                    alpha_slopes.append(float(slope))
                    
                # 4. Lensing Magnification
                med_mass = np.median(mass)
                attn_ki = attn[idx_k, idx_i]
                mass_j = mass[idx_j]
                high_mask = mass_j > med_mass
                lens_high = attn_ki[high_mask]
                lens_low = attn_ki[~high_mask]
                if len(lens_high) > 0 and len(lens_low) > 0 and np.mean(lens_low) > 0:
                    alpha_lensing_ratios.append(float(np.mean(lens_high) / np.mean(lens_low)))
                    
            if (s_idx + 1) % 10 == 0:
                print(f"  Processed {s_idx + 1}/{len(SENTENCES)} sentences...")
                
        if hook:
            hook.detach()
            
        extreme_results[str(alpha)] = {
            "entropy": float(np.mean(alpha_entropies)),
            "normalized_horizon": float(np.mean(alpha_horizons)),
            "horizon_correlation": float(np.mean(alpha_correlations)) if alpha_correlations else 0.0,
            "horizon_slope": float(np.mean(alpha_slopes)) if alpha_slopes else 0.0,
            "lensing_ratio": float(np.mean(alpha_lensing_ratios)) if alpha_lensing_ratios else 0.0
        }
        
        print(f"Alpha {alpha:.1f} Results:")
        print(f"  Entropy:             {extreme_results[str(alpha)]['entropy']:.4f}")
        print(f"  Normalized Horizon:  {extreme_results[str(alpha)]['normalized_horizon']:.4f}")
        print(f"  Horizon Correlation: {extreme_results[str(alpha)]['horizon_correlation']:.4f}")
        print(f"  Horizon Slope:       {extreme_results[str(alpha)]['horizon_slope']:.4f}")
        print(f"  Lensing Ratio:       {extreme_results[str(alpha)]['lensing_ratio']:.4f}")

    # Save summary results
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10d_extreme_results.json"
    with open(out_file, "w") as f:
        json.dump(extreme_results, f, indent=2)
    print(f"\nSaved extreme limits results to {out_file} ✅")

if __name__ == "__main__":
    main()
